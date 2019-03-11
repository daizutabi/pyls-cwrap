import pytest

from pyls_cwrap.format import format_text, joiner, splitter, wrap


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_splitter(nl):
    source = "a=1\n# c1\n# c2\n\n# c3\nb=1\n"
    source = source.replace("\n", nl)
    output = list(splitter(source))
    assert output[0] == ("Code", "a=1")
    assert output[1] == ("Comment", "c1")
    assert output[2] == ("Comment", "c2")
    assert output[3] == ("Code", "")
    assert output[4] == ("Comment", "c3")
    assert output[5] == ("Code", "b=1")


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_joiner(nl):
    source = "a=1\n# c1\n# c2\n\n# c3\nb=1\n"
    source = source.replace("\n", nl)
    output = list(joiner(source))
    assert output[0] == ("Code", "a=1")
    assert output[1] == ("Comment", "c1 c2")
    assert output[2] == ("Code", "")
    assert output[3] == ("Comment", "c3")
    assert output[4] == ("Code", "b=1")


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_joiner_wide_character(nl):
    source = "a=1\n# c1あ\n# いc2\n\n# c3\nb=1\n"
    source = source.replace("\n", nl)
    output = list(joiner(source))
    assert output[0] == ("Code", "a=1")
    assert output[1] == ("Comment", "c1あいc2")
    assert output[2] == ("Code", "")
    assert output[3] == ("Comment", "c3")
    assert output[4] == ("Code", "b=1")


def test_wrap():
    line = "abc def ghi jkl mno pqr stu vwxyz."
    output = list(wrap(line, 9))
    assert output[0] == "# abc def"
    assert output[1] == "# ghi jkl"
    assert output[2] == "# mno pqr"
    assert output[3] == "# stu"
    assert output[4] == "# vwxyz."

    output = list(wrap(line, 14))
    assert output[0] == "# abc def ghi"
    assert output[1] == "# jkl mno pqr"
    assert output[2] == "# stu vwxyz."


def test_wrap_wide_character():
    line = "abcあ def gいhi jkl mnoうpqr stえおかきく."
    output = list(wrap(line, 18))
    assert output[0] == "# abcあ def gいhi"
    assert output[1] == "# jkl mnoうpqr"
    assert output[2] == "# stえおかきく."


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_format_text(nl):
    source = (
        "a=1\n\n# あいうえおかきく\n# けこabc def ghi jkl mno pqr"
        "さしすせとなにぬねのabc def\n# hij klm aaaaaaaaaaaaaaaaa\n"
    ).replace("\n", nl)
    answer = (
        "a=1\n\n# あいうえお\n# かきくけこ\n# abc def\n# ghi jkl\n# mno\n"
        "# pqrさしす\n# せとなにぬ\n# ねのabc\n# def hij\n# klm\n# aaaa"
        "aaaaaaaaaaaaa\n"
    ).replace("\n", nl)
    assert format_text(source, 10) == answer
    answer = (
        "a=1\n\n# あいうえおかきくけこabc def ghi jkl mno pqrさしす\n# "
        "せとなにぬねのabc def hij klm aaaaaaaaaaaaaaaaa\n"
    ).replace("\n", nl)
    assert format_text(source, 50) == answer


def test_escape():
    source = "a=1\n# # Test\n# ~~~abc\n# a=1\n# b=1\n# ~~~\n# a\n# b\n"
    answer = "a=1\n# # Test\n# ~~~abc\n# a=1\n# b=1\n# ~~~\n# a b\n"
    assert format_text(source, 50) == answer


def test_header():
    source = "a=1\n# # Test\n# acd\n# b\n"
    answer = "a=1\n# # Test\n# acd b\n"
    assert format_text(source) == answer
