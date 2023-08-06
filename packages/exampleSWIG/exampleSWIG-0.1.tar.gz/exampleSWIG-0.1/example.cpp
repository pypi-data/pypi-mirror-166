// example.cpp

#include "example.h"

void example::say_hello(void) {
    cout << "hello python,I am C++" << endl;
}

void example::change(int din) {
    num = din;
}

int example::get_num(void) {
    return num;
}
