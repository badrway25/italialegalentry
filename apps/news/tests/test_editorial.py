import pytest
from django.core.exceptions import ValidationError

from news.editorial import Block, blocks, clean_link_list, plain_text, validate_link_list


def test_blocks_paragraphs_headings_and_lists():
    body = "Intro.\r\n\r\n## Titre 2\n\n### Titre 3\n\n- a\n- b\n\nLigne 1\nLigne 2\n\n\n"
    result = blocks(body)
    assert result == [
        Block("p", "Intro."),
        Block("h2", "Titre 2"),
        Block("h3", "Titre 3"),
        Block("ul", items=("a", "b")),
        Block("p", "Ligne 1\nLigne 2"),
    ]


def test_blocks_never_interpret_html():
    result = blocks("<script>alert(1)</script>\n\n## <b>x</b>")
    assert result[0] == Block("p", "<script>alert(1)</script>")
    assert result[1] == Block("h2", "<b>x</b>")


def test_blocks_empty():
    assert blocks("") == []
    assert blocks("\n\n  \n") == []


def test_plain_text_flattens_and_truncates():
    full = plain_text("## T\n\nParagraphe un.\n\n- x\n- y")
    assert full == "T Paragraphe un. x y"
    text = plain_text("## T\n\nParagraphe un.\n\n- x\n- y", limit=10)
    assert text.startswith("T Paragr")
    assert text.endswith("…")
    assert len(text) <= 10


@pytest.mark.parametrize(
    "value",
    [
        "not a list",
        [{"label": "", "url": "https://example.org"}],
        [{"label": "ok", "url": "ftp://example.org"}],
        [{"label": "ok", "url": "javascript:alert(1)"}],
        [{"label": "ok"}],
        [{"label": "ok", "url": "https://example.org", "onclick": "x"}],
        ["https://example.org"],
    ],
)
def test_validate_link_list_rejects(value):
    with pytest.raises(ValidationError):
        validate_link_list(value)


def test_clean_link_list_normalises():
    cleaned = clean_link_list([{"label": "  Normattiva ", "url": " https://www.normattiva.it/ "}])
    assert cleaned == [{"label": "Normattiva", "url": "https://www.normattiva.it/"}]
    assert clean_link_list([]) == []
    assert clean_link_list(None) == []
