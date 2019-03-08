from pyls_cwrap.wrap import Kind, beautify, joiner, splitter


def test_splitter():
    source = 'a=1\r\n# c1\r\n# c2\r\n\r\n# c3\r\nb=1\r\n'
    output = list(splitter(source))
    assert output[0] == (Kind.CODE, 'a=1')
    assert output[1] == (Kind.COMMENT, 'c1')
    assert output[2] == (Kind.COMMENT, 'c2')
    assert output[3] == (Kind.CODE, '')
    assert output[4] == (Kind.COMMENT, 'c3')
    assert output[5] == (Kind.CODE, 'b=1')


def test_joiner():
    source = 'a=1\r\n# c1\r\n# c2\r\n\r\n# c3\r\nb=1\r\n'
    output = list(joiner(source))
    assert output[0] == (Kind.CODE, 'a=1')
    assert output[1] == (Kind.COMMENT, 'c1 c2')
    assert output[2] == (Kind.CODE, '')
    assert output[3] == (Kind.COMMENT, 'c3')
    assert output[4] == (Kind.CODE, 'b=1')


def test_joiner_wide_character():
    source = 'a=1\r\n# c1あ\r\n# いc2\r\n\r\n# c3\r\nb=1\r\n'
    output = list(joiner(source))
    assert output[0] == (Kind.CODE, 'a=1')
    assert output[1] == (Kind.COMMENT, 'c1あいc2')
    assert output[2] == (Kind.CODE, '')
    assert output[3] == (Kind.COMMENT, 'c3')
    assert output[4] == (Kind.CODE, 'b=1')


def test_beautify():
    source = ('a=1\r\n\r\n# あいうえおかきく\r\n# けこabc def ghi jkl mno pqr'
              'さしすせとなにぬねのabc def\r\n# hij klm aaaaaaaaaaaaaaaaa\r\n')
    answer = ('a=1\r\n\r\n# あいうえお\r\n# かきくけこ\r\n# abc def\r\n# ghi jkl'
              '\r\n# mno\r\n# pqrさしす\r\n# せとなにぬ\r\n# ねのabc\r\n# def '
              'hij\r\n# klm\r\n# aaaaaaaaaaaaaaaaa\r\n')
    assert beautify(source, 10) == answer
    answer = ('a=1\r\n\r\n# あいうえおかきくけこabc def ghi jkl mno pqrさしす\r\n# '
              'せとなにぬねのabc def hij klm aaaaaaaaaaaaaaaaa\r\n')
    assert beautify(source, 50) == answer

    beautify(source, 10)
