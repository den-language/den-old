from module import DenModule

text = """
int func1(int: z) => {
    ret z;
}

int func2(int: z) => {
    ret z;
}

int test(int: y) => {
    int: x = func1(func2(10));
    ret y;
}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
