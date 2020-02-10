from module import DenModule
from helpers.color import init_color
from helpers.llvm_gen import initialize

init_color()
initialize()

text = """
int func1(int: z) => {
    ret z;
}

int func2(int: z) => {
    ret z;
}

int test(int: y) => {
    int: x = func1(func2(y));
    ret x;
}

entry => {
    int: x = test(1239);
}
"""

module = DenModule("test.den", text=text, debug=True)
module.generate()
