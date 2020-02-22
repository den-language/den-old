# The Den Programming Language

Den is a compiled programming language that is designed to be fast, simple, and modern.

```den
pub entry => {  # No arguments so we can skip the parenthesis
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

[Changelog](./changelog.md)&nbsp;&nbsp;[Codacy](https://www.codacy.com/manual/MonliH/den)&nbsp;&nbsp;[Trello](https://trello.com/b/gqVgP9Yf/the-den-programming-language)

## Run

Help - `python3.8 den/ --help`

Running tests:

```bash
pyenv shell 3.8.1
pip install -r requirements.txt
python3.8 -m pytest --cov=.  # --cov for code cov 
```

Note: code coverage right now is bad because tests are not rigorous enough; subject to change.

## Notes

* Functions are private by default, meaning they can be used in the file they are defined in, but **ONLY** in the file they are defined in.
