#!/usr/bin/env python3
"""Offline guardrails for the profile's intentionally small Markdown/SVG surface."""

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
SVG_TAGS = {"svg", "title", "desc", "defs", "linearGradient", "stop", "pattern",
            "path", "rect", "text", "g", "circle", "line", "polyline", "polygon", "ellipse"}


def local_file(target: str, root: Path) -> Path:
    url = urlsplit(target)
    if url.scheme or url.netloc or not url.path or url.query:
        raise ValueError(f"Expected a local file: {target}")
    path = (root / unquote(url.path)).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing file or path outside repository: {target}")
    return path


def validate_link(target: str, root: Path) -> None:
    url = urlsplit(target)
    if target.startswith("#"):
        return
    if url.scheme == "https" and url.netloc and not url.username and not url.password:
        return
    if url.scheme == "mailto" and "@" in url.path and not url.netloc:
        return
    local_file(target, root)


def validate_svg(path: Path) -> None:
    data = path.read_bytes()
    if len(data) > 100_000 or re.search(br"<!\s*(DOCTYPE|ENTITY)", data, re.I):
        raise ValueError(f"SVG is oversized or contains a DTD/entity: {path}")
    tree = ET.fromstring(data)
    if tree.tag != f"{{{SVG_NS}}}svg" or "viewBox" not in tree.attrib:
        raise ValueError(f"SVG needs the SVG namespace and a viewBox: {path}")
    for element in tree.iter():
        if element.tag not in {f"{{{SVG_NS}}}{tag}" for tag in SVG_TAGS}:
            raise ValueError(f"Unsupported SVG element: {element.tag}")
        for key, value in element.attrib.items():
            attr = key.rsplit("}", 1)[-1].lower()
            if attr.startswith("on") or attr in {"href", "style", "src"}:
                raise ValueError(f"Active or external SVG attribute: {key}")
            # Paint servers may only reference an ID in this same SVG.
            if "url(" in value.lower() and not re.fullmatch(r"url\(#[\w-]+\)", value):
                raise ValueError("SVG paint reference must be local")


class ProfileHTML(HTMLParser):
    def __init__(self, root: Path):
        super().__init__()
        self.root = root
        self.images = []
        self.details = 0

    def handle_starttag(self, tag, attrs):
        if tag not in {"p", "img", "details", "summary", "br", "a"}:
            raise ValueError(f"Unsupported README HTML element: {tag}")
        allowed = {"align", "src", "width", "height", "alt", "href"}
        if any(key not in allowed for key, _ in attrs):
            raise ValueError("Unsupported README HTML attribute")
        attrs = dict(attrs)
        if tag == "details":
            self.details += 1
        if tag == "a":
            validate_link(attrs.get("href", ""), self.root)
        if tag == "img":
            if not attrs.get("alt", "").strip():
                raise ValueError("Profile artwork needs descriptive alt text")
            path = local_file(attrs.get("src", ""), self.root)
            if path.suffix != ".svg":
                raise ValueError("Profile artwork must be a reviewed local SVG")
            validate_svg(path)
            self.images.append(path)

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "details":
            self.details -= 1
            if self.details < 0:
                raise ValueError("Unbalanced details elements")


def validate(root: Path = ROOT) -> None:
    content = (root / "README.md").read_text(encoding="utf-8")
    if re.search(r"!\[", content):
        raise ValueError("Use the single local HTML hero instead of Markdown images")
    parser = ProfileHTML(root)
    parser.feed(content)
    parser.close()
    if parser.details:
        raise ValueError("Unclosed details element")
    if len(parser.images) != 1:
        raise ValueError("Keep one local hero image to preserve the minimal design")
    if len(re.findall(r"^# ", content, re.M)) != 1:
        raise ValueError("Use exactly one main Markdown heading")
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content):
        validate_link(target, root)
    print("Profile checks passed: local artwork, safe link schemes, and basic structure.")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, ET.ParseError, OSError) as exc:
        print(f"Profile validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
