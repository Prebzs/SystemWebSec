#include <stdlib.h>
#include <stdio.h>
#include <string.h>
main(int argc, char *argv[]) {
  char *in;
  if (argc < 2) {
    printf("At least one argument required!\n");
    return -1;
  }
  if (atoi(argv[1]) == 1) {
    in = malloc(64);
    printf("Enter argument: ");
    fgets(in,64,stdin);
  }
  else {
    in = malloc(32);
    printf("Enter argument: ");
    fgets(in,32,stdin);
  }
  /* Do something with in */
  printf("in=%s\n",in);
}

