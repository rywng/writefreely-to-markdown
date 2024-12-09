from writefreely_to_markdown.lib import frontmatter
from datetime import datetime


def test_desc_extraction_no_tags():
    body = ".. including fonts and cursor themes\n\n\u003c!--more--\u003e\n\n## Cursor themes\n\nRun this:\n\n```bash\nflatpak --user override --filesystem=/usr/share/icons/:ro\n```\n\n## Fonts\n\nInstall `gnome-base/gnome-settings-daemon`\n"
    assert (
        frontmatter.get_description_from_body(body)
        == ".. including fonts and cursor themes."
    )

    # def test_desc_extraction_has_tag_like():
    body = "Workaround for [this](https://github.com/go-gitea/gitea/issues/14722#issuecomment-781293156) GitHub problem\n\n\u003c!--more--\u003e\n\n## Create gpg key\n\n``              `bash\nsudo -i -u gitea\ncd data/home\ncat .gitconfig\n```\n\nTo get the default id and email for gitea\n\nGenerate keys for"
    assert (
        frontmatter.get_description_from_body(body)
        == "Workaround for [this](https://github.com/go-gitea/gitea/issues/14722#issuecomment-781293156) GitHub problem."
    )

    # def test_desc_extraction_has_tag():
    body = "\u003e Update: On latest version of SwayWM, everything works OOTB with Fcitx5\n\nTo input CJK (Chinese, Japanese and Korean) languages in Linux Minecraft, you can install this mod [CocoaInput](https://legacy.curseforge.com/minecraft/mc-mods/cocoainput).\n\nIf that's the case, I won't bother writing an article about it. The thing is that the mod is only officially available for `1.7` to `1.18`, for the latest Minecraft `1.19` to `1.20`, you'll need to compile the mod binary from an updated fork of it.\n\n#linux #gnome #minecraft\n\n\u003c!--more--\u003e\n\n"
    tags = ["linux", "gnome", "minecraft"]
    assert (
        frontmatter.get_description_from_body(body, tags)
        == "\u003e Update: On latest version of SwayWM, everything works OOTB with Fcitx5. To input CJK (Chinese, Japanese and Korean) languages in Linux Minecraft, you can install this mod [CocoaInput](https://legacy.curseforge.com/minecraft/mc-mods/cocoainput). If that's the case, I won't bother writing an article about it. The thing is that the mod is only officially available for `1.7` to `1.18`, for the latest Minecraft `1.19` to `1.20`, you'll need to compile the mod binary from an updated fork of it."
    )

    # def test_desc_extraction_has_tag_no_desc():
    body = "#linux #gentoolinux #systemd\n\n\u003c!--more--\u003e\n\n"
    tags = ["gentoolinux", "systemd", "linux"]
    assert frontmatter.get_description_from_body(body, tags) is None


def test_frontmatter_generation():
    expected = """title = "title"
description = "desc"
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
            "desc",
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


def test_frontmatter_content_extraction():
    # No tags
    body = ".. including fonts and cursor themes\n\n\u003c!--more--\u003e\n\n## Cursor themes\n\nRun this:\n\n```bash\nflatpak --user override --filesystem=/usr/share/icons/:ro\n```\n\n## Fonts\n\nInstall `gnome-base/gnome-settings-daemon`\n"

    assert (
        frontmatter.get_content_from_body(body)
        == "## Cursor themes\n\nRun this:\n\n```bash\nflatpak --user override --filesystem=/usr/share/icons/:ro\n```\n\n## Fonts\n\nInstall `gnome-base/gnome-settings-daemon`"
    )

    body = "stuff without more"
    assert frontmatter.get_content_from_body(body) == body

    body = "#linux #gentoolinux #systemd\n\n\u003c!--more--\u003e\n\n### Why I stopped using OpenRC"
    assert frontmatter.get_content_from_body(body) == "### Why I stopped using OpenRC"
