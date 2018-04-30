#include <stdio.h>

void myfunction(int a) {
        long some_long;
        char * some_strings[2];
        some_long = 42;
        some_strings[0] = "foo";
        some_strings[1] = "bar";
        some_long -= 19;
        printf("%ld\n%d\n%s\n", some_long, a, some_strings[0]);
}
int main () {
        int x = 0;
        myfunction(x);
}
