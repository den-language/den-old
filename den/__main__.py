from module import DenModule
from helpers.color import init_color
from helpers import location

init_color()

text = """
int func1(int: z) => {
    ret z;
}

int func2(int: z) => {
    ret z;
}

int test(int: y) => {
    int: x = func1(func2(10));
    ret ad;
}
"""

module = DenModule("test.den", text=text)
module.generate()
