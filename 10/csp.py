#!/usr/bin/env python3

import sys
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from html import escape
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')


main_doc = '''
<!doctype html>
<html>
<head>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<link rel="stylesheet" type="text/css" href="/style.css">
</head>
<body>
<h1>SEC Playground</h1>
<iframe src="https://sec.uni-stuttgart.de"></iframe>
<br>
<button id='mybutton'>Resize iframe</button>
<script>
$('#mybutton').click(function() {{
  $('iframe').toggleClass('fullwidth');
}})
</script>
{result}
</body></html>
'''

style_doc = '''
iframe {
 border: solid red 5px;
 width: 400px;
 height: 200px;
}

iframe.fullwidth {
 width: 100%;
}
'''


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_dict = urlparse(self.path)  # parse URL string into dictionary
        get_dict = parse_qs(url_dict.query)  # select query string from URL dictionary

        if url_dict.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css;charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(style_doc, 'UTF-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.send_header('Content-Security-Policy', 'frame-src \'self\'')
        self.send_header('X-XSS-Protection', '0') # disables XSS protection in the browser

        self.end_headers()

        result = ''

        if 'lookup' in get_dict:
            lookup = get_dict['lookup'][0]
            result = f'<h3>Search Results for {lookup}</h3>'

        output = main_doc.format(result=result)
        self.wfile.write(bytes(output, 'UTF-8'))

if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print ("Starting web server on http://localhost:8081/")
    server.serve_forever()
