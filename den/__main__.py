from module import DenModule

text = """
int test1(int: x) => {
    ret x;
}

int test2() => {
    int: y = -(1-10)*10+10;
    ret y;
}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
