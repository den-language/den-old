from module import DenModule

text = """
int test1(int: z) => {
    int: x = test2(z);
    ret x;
}

int test2(int: y) => {
    ret y;
}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
