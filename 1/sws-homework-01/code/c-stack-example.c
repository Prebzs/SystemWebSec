void do_something(int a, int * b) {
  int c;
  int d;

  c = a + *b;
}

int main() {
  int e;
  int f;
  int g;

  e = 42;
  
  do_something(23, &e);
}
