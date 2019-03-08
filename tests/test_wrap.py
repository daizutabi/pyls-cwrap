from pyls_cwrap.wrap import Kind, beautify, joiner, splitter, wrap


def test_splitter():
    source = "a=1\n# c1\n# c2\n\n# c3\nb=1\n"
    output = list(splitter(source))
    assert output[0] == (Kind.CODE, "a=1")
    assert output[1] == (Kind.COMMENT, "c1")
    assert output[2] == (Kind.COMMENT, "c2")
    assert output[3] == (Kind.CODE, "")
    assert output[4] == (Kind.COMMENT, "c3")
    assert output[5] == (Kind.CODE, "b=1")


def test_joiner():
    source = "a=1\n# c1\n# c2\n\n# c3\nb=1\n"
    output = list(joiner(source))
    assert output[0] == (Kind.CODE, "a=1")
    assert output[1] == (Kind.COMMENT, "c1 c2")
    assert output[2] == (Kind.CODE, "")
    assert output[3] == (Kind.COMMENT, "c3")
    assert output[4] == (Kind.CODE, "b=1")


def test_joiner_wide_character():
    source = "a=1\n# c1あ\n# いc2\n\n# c3\nb=1\n"
    output = list(joiner(source))
    assert output[0] == (Kind.CODE, "a=1")
    assert output[1] == (Kind.COMMENT, "c1あいc2")
    assert output[2] == (Kind.CODE, "")
    assert output[3] == (Kind.COMMENT, "c3")
    assert output[4] == (Kind.CODE, "b=1")


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


def test_beautify():
    source = (
        "a=1\n\n# あいうえおかきく\n# けこabc def ghi jkl mno pqr"
        "さしすせとなにぬねのabc def\n# hij klm aaaaaaaaaaaaaaaaa\n"
    )
    answer = (
        "a=1\n\n# あいうえお\n# かきくけこ\n# abc def\n# ghi jkl\n# mno\n"
        "# pqrさしす\n# せとなにぬ\n# ねのabc\n# def hij\n# klm\n# aaaa"
        "aaaaaaaaaaaaa\n"
    )
    assert beautify(source, 10) == answer
    answer = (
        "a=1\n\n# あいうえおかきくけこabc def ghi jkl mno pqrさしす\n# "
        "せとなにぬねのabc def hij klm aaaaaaaaaaaaaaaaa\n"
    )
    assert beautify(source, 50) == answer
