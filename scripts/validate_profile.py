#!/usr/bin/env python3
"""Offline guardrails for the profile's intentionally small Markdown/SVG surface."""

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.build_profile import AVATAR_STYLE
SVG_NS = "http://www.w3.org/2000/svg"
SVG_TAGS = {"svg", "title", "desc", "defs", "linearGradient", "radialGradient", "stop", "pattern",
            "path", "rect", "text", "g", "circle", "line", "polyline", "polygon", "ellipse", "style"}


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


def validate_svg(path: Path, max_bytes=100_000) -> None:
    data = path.read_bytes()
    if len(data) > max_bytes or b"<?" in data or re.search(br"<!\s*(DOCTYPE|ENTITY)", data, re.I):
        raise ValueError(f"SVG is oversized or contains a DTD/entity: {path}")
    tree = ET.fromstring(data)
    if tree.tag != f"{{{SVG_NS}}}svg" or "viewBox" not in tree.attrib:
        raise ValueError(f"SVG needs the SVG namespace and a viewBox: {path}")
    for element in tree.iter():
        if element.tag not in {f"{{{SVG_NS}}}{tag}" for tag in SVG_TAGS}:
            raise ValueError(f"Unsupported SVG element: {element.tag}")
        if element.tag == f"{{{SVG_NS}}}style" and element.text != AVATAR_STYLE:
            raise ValueError("Only the reviewed finite avatar-print CSS is allowed")
        for key, value in element.attrib.items():
            attr = key.rsplit("}", 1)[-1].lower()
            if attr.startswith("on") or attr in {"href", "style", "src"}:
                raise ValueError(f"Active or external SVG attribute: {key}")
            # Paint servers may only reference an ID in this same SVG.
            if "url(" in value.lower() and not re.fullmatch(r"url\(#[\w-]+\)", value):
                raise ValueError("SVG paint reference must be local")


IMAGE_HOSTS = {
    "capsule-render.vercel.app", "readme-typing-svg.demolab.com", "img.shields.io",
    "komarev.com", "user-images.githubusercontent.com", "skillicons.dev",
    "upload.wikimedia.org", "seaborn.pydata.org", "raw.githubusercontent.com",
    "profilinator.rishav.dev", "github-readme-stats-eight-theta.vercel.app",
    "github-readme-streak-stats.herokuapp.com",
}
LEGACY_STYLES = {
    "display: flex; align-items: flex-start; justify-content: center;",
    "border-radius: 8px;",
}


def validate_image(target, root):
    url = urlsplit(target)
    if url.scheme or url.netloc:
        if url.scheme != "https" or url.netloc not in IMAGE_HOSTS:
            raise ValueError("Image host is not part of the restored original profile")
        return
    path = local_file(target,root)
    relative=path.relative_to(root.resolve()).as_posix()
    if re.fullmatch(r"assets/avatar-print-(?:dark|light)(?:-mobile)?(?:-static)?\.svg",relative):
        validate_svg(path,max_bytes=350_000)
        return
    if relative not in {"gitartwork.svg", "profile-3d-contrib/profile-night-view.svg"}:
        raise ValueError("Unreviewed local profile artwork")
    tree = ET.parse(path)
    for element in tree.iter():
        if element.tag.rsplit("}",1)[-1] in {"script","foreignObject"}:
            raise ValueError("Active content in local contribution artwork")
        for key,value in element.attrib.items():
            attr=key.rsplit("}",1)[-1].lower()
            if attr.startswith("on"):
                raise ValueError("SVG event handlers are forbidden")
            if attr == "href" and not value.startswith("#"):
                validate_link(value,root)


class ProfileHTML(HTMLParser):
    def __init__(self,root):
        super().__init__()
        self.root=root
        self.details=0
        self.images=[]

    def handle_starttag(self,tag,attrs):
        if tag not in {"p","div","h3","table","tr","td","b","i","img","picture","source","details","summary","br","a"}:
            raise ValueError(f"Unsupported README HTML element: {tag}")
        allowed={"align","src","srcset","media","width","height","alt","href","style","valign","clear"}
        if any(key not in allowed for key,_ in attrs):
            raise ValueError("Unsupported README HTML attribute")
        attrs=dict(attrs)
        if "style" in attrs and attrs["style"] not in LEGACY_STYLES:
            raise ValueError("Only the restored original inline layout styles are allowed")
        if tag == "details":
            self.details+=1
        if tag == "a":
            validate_link(attrs.get("href",""),self.root)
        if tag in {"img","source"}:
            if tag == "img" and "alt" not in attrs:
                raise ValueError("Images need an alt attribute; decorative images use an empty one")
            target=attrs.get("srcset" if tag == "source" else "src","")
            validate_image(target,self.root)
            self.images.append(target)

    handle_startendtag=handle_starttag

    def handle_endtag(self,tag):
        if tag == "details":
            self.details-=1
            if self.details<0:
                raise ValueError("Unbalanced details elements")


def validate(root=ROOT):
    content=(root/"README.md").read_text(encoding="utf-8")
    parser=ProfileHTML(root)
    parser.feed(content)
    parser.close()
    if parser.details:
        raise ValueError("Unclosed details element")
    # Markdown badges and ordinary Markdown links both need validated destinations.
    for match in re.finditer(r"(!?)\[[^\]]*\]\(([^\s)]+)\)",content):
        if match[1]:
            validate_image(match[2],root)
        else:
            validate_link(match[2],root)
    print("Profile checks passed: original-layout HTML, reviewed image hosts, and safe link schemes.")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, ET.ParseError, OSError) as exc:
        print(f"Profile validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
