#include <stdio.h>

void blub() {
	int a;
	int b;
	b = 0x17;
	a = b - 0xf;

	printf("&d", a);
}

int main() {
	blub();
	return 0;
}
