#include <stdio.h>
#include <string.h>
char foo[] = "zweiundvier\0zig";
void function () {
        char buffer1[8];
        char buffer2[3];
	char buffer3[4];
        strcpy(buffer3, foo);
        printf("%s\n", buffer2);
}
int main () {
        function();
}
