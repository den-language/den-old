from module import DenModule

text = """
int add() => {
    int: x = 10;
    ret 10;
}

int daw() => {
    int: y = 10;
    ret 10;
}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
