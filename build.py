#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import shutil
import tempfile


MARKER = "<!-- Added automatrcally by build.sh script-->"
SRC_DIR = "src"
BUILD_DIR = "build"


def build_css_path(index_file: str) -> str:
    """
    Build relative CSS path for an index.html located inside BUILD_DIR.

    Examples:
        build/index.html                  -> css/styles.css
        build/blog/index.html             -> ../css/styles.css
        build/blog/posts/index.html       -> ../../css/styles.css
    """
    rel_path = os.path.relpath(index_file, BUILD_DIR)
    rel_dir = os.path.dirname(rel_path)

    if rel_dir in ("", "."):
        return "css/styles.css"

    depth = len([part for part in rel_dir.split(os.sep) if part])
    return "../" * depth + "css/styles.css"


def process_index_file(index_file: str) -> None:
    with open(index_file, "r", encoding="utf-8", newline="") as f:
        first_line = f.readline()
        first_line = first_line.rstrip("\n")

        if first_line == MARKER:
            return

        f.seek(0)
        original_content = f.read()

    css_path = build_css_path(index_file)

    header = f"""<!-- Added automatically by build.sh script-->
<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <link rel="stylesheet" href="{css_path}">
    <title>gfaerny</title>
  </head>

  <body>
    <div class="container">
      <header>
        <h1><a href="https://gfaerny.me">gfaerny</a></h1>
        <p class="meta">
          Email:
          <a href="mailto:mail@gfaerny.me">mail@gfaerny.me</a><br>
          <a href="https://github.com/gfaerny/">Github</a> —
          <a href="https://gfaerny.bandcamp.com">Bandcamp</a> —
          <a href="https://soundcloud.com/gfaerny">Soundcloud</a> —
          <a rel="me" href="https://mastodon.art/@gfaerny">Mastodon</a>
        </p>
      </header>

      <main>
"""

    footer = """

      </main>
      <footer style="margin-top:28px;color:#7e7e7e;font-size:13px;">
        © <span id="year"></span> — Ilia Abolghasemi (gfaerny) — Under Boost license
        <br>
        last update of this page -> Feb 14 , 2026
      </footer>
    </div>

    <script>
      // Automatically display the current year
      document.getElementById('year').textContent = new Date().getFullYear();
    </script>
  </body>
</html>
"""

    out_dir = os.path.dirname(index_file) or "."
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        delete=False,
        dir=out_dir,
    ) as tf:
        tmp_name = tf.name
        tf.write(header)
        tf.write(original_content)
        tf.write(footer)
        tf.flush()

    shutil.move(tmp_name, index_file)


def copy_src_to_build() -> None:

    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    shutil.copytree(SRC_DIR, BUILD_DIR)


def process_build_tree() -> None:
    for root, dirs, files in os.walk(BUILD_DIR, topdown=True):
        if "index.html" in files:
            index_file = os.path.join(root, "index.html")
            process_index_file(index_file)


def main() -> int:
    copy_src_to_build()
    process_build_tree()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
