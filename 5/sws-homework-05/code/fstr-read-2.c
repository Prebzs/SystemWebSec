#include <stdio.h>
#include <string.h>
int try_login(char * user, char * pass, 
	      char * validuser, char * validpass) {
  int logged_in = 0;
  if (strcmp(user, validuser) == 0 && 
      strcmp(pass, validpass) == 0)
    logged_in = 1;
  else {
    printf("Username or password invalid. Username: ");
    printf(user);
    printf("\n");
  }
  return logged_in;
}
main(int argc, char * argv[]) {
  if (argc != 3) { 
    printf("No username and password!\n");
    return -1;
  }
  if (try_login(argv[1], argv[2], "root", "passwd") == 1)
    printf("Login successful. Have fun!\n");
  else 
    printf("ACCESS DENIED!\n");
}
