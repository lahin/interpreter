import pytest
from calc1 import Lexer, Interpreter, INTEGER, OPERATOR, EOF


def test_skip_whitespaces_advances_pos():
    text = "     3+4"
    pos = 0
    expected_pos = 5
    returned_pos = Lexer.skip_whitespaces(text, pos)
    assert text[returned_pos] == "3"
    assert returned_pos == expected_pos


def test_skip_whitespaces_no_position_change():
    text = "3+4"
    pos = 0
    expected_pos = 0
    returned_pos = Lexer.skip_whitespaces(text, pos)
    assert text[returned_pos] == "3"
    assert returned_pos == expected_pos
