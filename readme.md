# The Den Programming Language

<---
[![Codacy Badge](https://img.shields.io/codacy/grade/bdc3b36eff354ef3add854b40115ad53?style=for-the-badge)](https://www.codacy.com/manual/MonliH/den)
-->

Den is a compiled programming language that is designed to be fast, simple, and modern.

```den
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
[Codacy](https://www.codacy.com/manual/MonliH/den)

# Run

Help - `python3.8 den/ --help`

Running tests:

```bash
pyenv shell 3.8.1
pip install -r requirements.txt
python3.8 -m pytest --cov=.  # --cov for code cov 
```
