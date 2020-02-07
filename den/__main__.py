from module import DenModule

text = """
int add() => {

}
"""

module = DenModule("test.den")
module.add_text(text)
module.generate()
