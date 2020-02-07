from module import DenModule

text = """
int test1() => {
    int: x = -(1-10)*10+10;
    ret 10;
}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
