#!/usr/bin/env python3

import sys
import secrets
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from http import cookies
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')
import sqlite3
import random
from reset_database import reset_database

DATABASE_FILE = 'website.sqlite3'

form_doc1 = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
<form method="post">
    User: <input name="user"> <br>
    Password: <input name="pass" type="password">
    <input type="hidden" name="csrftoken" value="
'''

form_doc2 = '''
">
<br>
<input type="submit" name="action" value="login">
</form>
</body></html>
'''


authenticated_doc = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
You are logged in as {username}!
<form method="post">
    <input type="submit" name="action" value="logout">
</form>
<br>
If you are an administrator, you can use the <a href="/admin">admin interface</a>.
</body></html>
'''

success = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
Welcome, {user}!
</html></body>
'''

fail = '''
<!doctype html>
<html><body style="color:red;">
<h1>SEC Intranet</h1>
{message}
</html></body>
'''

sessions = {}

csrftokens = {}


class MyHandler(BaseHTTPRequestHandler):
    saved_headers = []
    
    def get_or_create_session(self):
        cookie_dict = cookies.SimpleCookie(self.headers['Cookie'])

        if 'sid' in cookie_dict:
            sid = cookie_dict['sid'].value

        if 'sid' not in cookie_dict or sid not in sessions:
            sid = secrets.token_urlsafe()  # generate some random token
            self.saved_headers = [('Set-Cookie', 'sid=' + sid)]
            sessions[sid] = {}  # the session is initially empty

        return sid

    
    def do_GET(self):
        sid = self.get_or_create_session()
        if 'username' in sessions[sid]:
            self.send_response_headers_and_body(authenticated_doc.format(username=sessions[sid]['username']))
        else:
            csrftokens[self.client_address[0]] = secrets.token_urlsafe()
            self.send_response_headers_and_body(form_doc1 + csrftokens[self.client_address[0]] + form_doc2)
            

    def do_POST(self):
        sid = self.get_or_create_session()
        content_length = self.headers['Content-Length']
        body = self.rfile.read(int(content_length))
        post_dict = parse_qs(str(body, 'UTF-8'))

        action = post_dict['action'][0]
        
        if action == 'login' and post_dict['csrftoken'][0].rstrip().lstrip() == csrftokens[self.client_address[0]]:
                             
            post_user = post_dict['user'][0]
            post_pass = post_dict['pass'][0]

            connection = sqlite3.connect(DATABASE_FILE)  # could also be replaced by a connection to a remote sql server, e.g., a mysql instance
            sql = "SELECT username FROM users WHERE username = ? AND password = ?"
            print (f"Executing SQL: {sql}")
            res = connection.execute(sql, (post_user, post_pass))
            entry = res.fetchone()
            if entry is None:
                self.send_response_headers_and_body(fail.format(message="Wrong username or password!"))
                return
            else:
                print ("Successful login!")
                sessions[sid]['username'] = post_user
                self.redirect('/')
                return

        else:
            sessions[sid] = {}
            self.send_response_headers_and_body(form_doc1 + csrftokens[self.client_address[0]] + form_doc2)
            return
                

    def send_response_headers_and_body(self, output):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        for header, value in self.saved_headers:  # we use saved_headers to store headers for this particular response in get_or_create_session
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(bytes(output, 'UTF-8'))

    def redirect(self, target):
        self.send_response(303)
        self.send_header('Location', target)
        self.end_headers()


# We extend the class MyHandler to define an admin interface. The
# extended class overwrites the base class so that we do not have to
# change anything in the surrounding code.
class MyHandler(MyHandler):
    admin_doc = '''
    <!doctype html>
    <html>
    <h1>SEC Intranet - Admin Area</h1>
    <a href='/'>Return to home</a>
    <table>{rows}</table>
    Never store passwords in plain text as we do in this example!
    <form method='post'>
    <input type="submit" value="RESET DATABASE" name='submit'/>
    </form>
    <form method='post'>
    <input name='newUser' />
    <input name='newPassword' />
    <input type='submit' value='Add new user' name='submit'/>
    </form>
    <style>
    table {{ border: 1px solid black; border-collapse: collapse; }}
    th, td {{ border: 1px solid black; padding: 3px; }}
    </style>
    </html>'''
    
    def do_GET(self):
        if self.path != '/admin':
            return super().do_GET()
        
        sid = self.get_or_create_session()

        if not 'username' in sessions[sid]:
            self.send_response_headers_and_body(fail.format(message="Not logged in! <a href='/'>Return to home</a>"))
            return

        username = sessions[sid]['username']
        
        connection = sqlite3.connect(DATABASE_FILE)

        sql = "SELECT username FROM users WHERE username = ? AND privileges = 'all'"
        print (f"Executing SQL: {sql}")
        res = connection.execute(sql, (username,))
        entry = res.fetchone()
        if entry is None:
            self.send_response_headers_and_body(fail.format(message="Not enough privileges! <a href='/'>Return to home</a>"))
            return

        res = connection.execute("SELECT id, username, password, signed_up, privileges FROM users");
        rows = '<tr> <th>id</th> <th>username</th> <th>password</th> <th>signed_up</th> <th>privileges</th> </tr>'
        for row in res:
            rows += f'<tr> <td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td> <td>{row[3]}</td> <td>{row[4]}</td> </tr>'

        self.send_response_headers_and_body(self.admin_doc.format(rows=rows))

    def do_POST(self):
        if self.path != '/admin':
            return super().do_POST()

        content_length = self.headers['Content-Length']
        body = self.rfile.read(int(content_length))
        post_dict = parse_qs(str(body, 'UTF-8'))
        
        if post_dict['submit'][0] == 'Add new user':
            connection = sqlite3.connect(DATABASE_FILE)  # could also be replaced by a connection to a remote sql server, e.g., a mysql instance
            sql = "INSERT INTO users (id, username, password, signed_up, privileges) VALUES (?, ?, ?, ?, ?)"
            print (f"Executing SQL: {sql}")
            connection.execute(sql, (random.randint(0, 9999999), post_dict['newUser'][0], post_dict['newPassword'][0], '2018-06-24', 'user')) # should be auto_increment instead of using random numbers)
            connection.commit()
            self.redirect('/admin')
            
        if post_dict['submit'][0] == 'RESET DATABASE':
            reset_database()
            self.redirect('/admin')


        
if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print ("Starting web server on http://localhost:8081/")
    print ("Admin interface at http://localhost:8081/admin")
    server.serve_forever()
