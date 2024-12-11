from writefreely_to_markdown.lib import frontmatter
from datetime import datetime


def test_frontmatter_generation():
    expected = """title = "title"
date = 2000-01-03T00:00:00
updated = 2000-01-03T00:00:00
draft = true
slug = "test-slug"
authors = ["Test author"]

[taxonomies]
tags = ["linux", "pytest"]
language = "en"
"""
    assert (
        frontmatter.get_frontmatter(
            "title",
            datetime.fromisocalendar(2000, 1, 1),
            datetime.fromisocalendar(2000, 1, 1),
            True,
            "test-slug",
            ["Test author"],
            ["linux", "pytest"],
            "en",
        ).as_string()
        == expected
    )
