import pytest

from pyls_cwrap.splitter import source_splitter, splitter


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_source_splitter(nl):
    source = "a=1\n# c1\n# c2\n\n# c3\nb=1\n"
    source = source.replace("\n", nl)
    output = list(source_splitter(source))
    assert output[0] == ("Code", "a=1")
    assert output[1] == ("Comment", "# c1")
    assert output[2] == ("Comment", "# c2")
    assert output[3] == ("Comment", "")
    assert output[4] == ("Comment", "# c3")
    assert output[5] == ("Code", "b=1")


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
def test_splitter_escpae(nl):
    source = "a=1\n# # header\n# c2\n# ~~~\n# ```\n# a=1\n# ```\n# ~~~\n# c3\n"
    source = source.replace("\n", nl)
    output = list(splitter(source))

    assert output == [
        ("Code", "a=1"),
        ("Escape", "# # header"),
        ("Comment", "c2"),
        ("Escape", "# ~~~"),
        ("Escape", "# ```"),
        ("Escape", "# a=1"),
        ("Escape", "# ```"),
        ("Escape", "# ~~~"),
        ("Comment", "c3"),
        ("Code", ""),
    ]


@pytest.mark.parametrize("nl", ["\n", "\r\n"])
def test_splitter_string(nl):
    source = "# abc\nsource='''\n# a=1\n# b=1\n'''\n# c=1\n"
    source = source.replace("\n", nl)
    output = list(splitter(source))

    assert output == [
        ("Comment", "abc"),
        ("Code", f"source='''{nl}# a=1{nl}# b=1{nl}'''"),
        ("Comment", "c=1"),
        ("Code", ""),
    ]
