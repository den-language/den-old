from den.lexer import DenLexer

def test_comment():
    lexer = DenLexer()
    data = "# I should be ignored"
    assert len(list(lexer.tokenize(data))) == 0

def test_literal():
    lexer = DenLexer()
    for literal in "{}():,=+-*/&":
        assert list(lexer.tokenize(literal))[0].type == literal

def test_id():
    lexer = DenLexer()
    data = "hellotest testty test test"
    tokens = list(lexer.tokenize(data))
    assert len(tokens) == 4
    for token, content in zip(tokens, data.split(" ")):
        assert token.type == "ID"
        assert token.value == content

def test_fat_arrow():
    lexer = DenLexer()
    data = "=>"
    assert list(lexer.tokenize(data))[0].type == "FAT_ARROW"

def test_newline():
    lexer = DenLexer()
    data = "\n\n\n\n"
    tokens = list(lexer.tokenize(data))
    assert len(tokens) == 0
