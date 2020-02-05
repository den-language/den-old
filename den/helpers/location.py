class Location:
    def __init__(self, sline, scol, eline=None, ecol=None):
        self.sline = sline
        self.scol = scol
        if eline == None:
            self.eline = self.sline
        else:
            self.eline = eline

        if ecol == None:
            self.ecol = self.scol
        else:
            self.ecol = ecol
