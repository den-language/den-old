

class Builder:
    def __init__(self, filename):
        self.filename = filename
        self.sections = {"FRONT": [], "IMPORTS": [], "MAIN": [], "OUT": []}

    def push(self, section, contents):
        self.sections[section].append(contents)

    def output(self):
        return "\n".join(sum(self.sections.values(), []))
