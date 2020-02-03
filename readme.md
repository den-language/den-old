# The Den Programming Language

Den is a compiled programming language that is designe to be fast, simple, and modern.

```
entry => {  # no arguments so we can skip the parenthesis
    int: x;
    int: y = &x - 1;  # Create a relationship between x and y

    x = 10;
    # Now y is 9

    x = 1203;
    # Now y is 1202
}

add(int: x, int: y) => x+y;  # define add function
mul(x, y) => x*y;  # define mul function
```
