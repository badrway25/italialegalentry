#!/usr/bin/env python
"""Django management entry point for Italy Legal Entry."""

import contextlib
import os
import sys


def _force_utf8_output() -> None:
    """
    Make stdout and stderr carry the text this project actually writes.

    A Windows console defaults to cp1252, which cannot encode an em dash, an arrow, a French
    apostrophe or a single letter of Arabic — and this project's commands write all four. The
    failure is not cosmetic: `UnicodeEncodeError` is raised from the write, so a command that has
    already done its work dies while explaining itself, with a traceback that looks like the work
    failed. `seed_legal_rules` seeded correctly and then crashed on the arrow in the sentence
    describing the review chain.

    Fixed here rather than in each command, because it had already been patched twice in two
    different commands before anybody noticed it was the same bug. `errors="replace"` keeps a
    console that genuinely cannot render a glyph from taking the command down with it.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        # A redirected or already-closed stream may refuse; that is not worth failing over.
        with contextlib.suppress(ValueError, OSError):
            reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    _force_utf8_output()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
