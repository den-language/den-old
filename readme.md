# The Den Programming Language

![CI status](https://img.shields.io/github/workflow/status/MonliH/den/Quality?style=for-the-badge)

Den is a compiled programming language that is designed to be fast, simple, and modern.

```
entry => {  # No arguments so we can skip the parenthesis
    int: x;
    int: y = &x - 1;  # Create a relationship between x and y

    x = 10;
    # Now y is 9

    x = 1203;
    # Now y is 1202
}

int add(int: x, int: y) => x+y;  # Define add function
int mul(int: x, int: y) => x*y;  # Define mul function
```

[Changelog](./changelog.md)
