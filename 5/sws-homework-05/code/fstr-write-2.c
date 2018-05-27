#include <stdio.h>
#include <string.h>
int try_login(char * user, char * pass, 
	      char * validuser, char * validpass) {
  int status = 0x42; // Logged out
  if (strcmp(user, validuser) == 0 && 
      strcmp(pass, validpass) == 0)
    status = 0x17; // Logged in
  else {
    printf("Username or password invalid. Username: ");
    printf(user);
    printf("\n\n&status=%08x, status=%08x\n\n", 
	   &status, status);
  }
  return status;
}
main(int argc, char * argv[]) {
  if (argc != 3) { 
    printf("Provide username and password!\n");
    return -1;
  }
  if (0x17 == try_login(argv[1], argv[2], "root", "geheim"))
    printf("Login successful. Have fun!\n");
  else 
    printf("ACCESS DENIED.\n");
}
