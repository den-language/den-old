def find_column(text, index):
    last_cr = text.rfind("\n", 0, index)
    if last_cr < 0:
        last_cr = 0
    column = (index - last_cr) + 1
    return column
