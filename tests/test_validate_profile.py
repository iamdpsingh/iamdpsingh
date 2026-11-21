"""Regression checks for active SVG content, remote images, and unsafe links."""

import tempfile
import unittest
from pathlib import Path

from scripts.validate_profile import ProfileHTML, local_file, validate, validate_link, validate_svg


class ProfileSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.svg = self.root / "art.svg"
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="url(#heat)"/></svg>')

    def test_repository_profile(self):
        validate()

    def test_static_svg_passes(self):
        validate_svg(self.svg)

    def test_active_svg_is_rejected(self):
        for payload in ('<script>alert(1)</script>', '<foreignObject/>',
                        '<rect onload="alert(1)"/>', '<a href="https://example.org"/>',
                        '<rect fill="url(https://example.org/image)"/>', '<animate/>'):
            with self.subTest(payload=payload):
                self.svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">{payload}</svg>')
                with self.assertRaises(ValueError):
                    validate_svg(self.svg)

    def test_entities_are_rejected(self):
        self.svg.write_text('<!DOCTYPE svg [<!ENTITY test "hi">]><svg/>')
        with self.assertRaises(ValueError):
            validate_svg(self.svg)

    def test_unsafe_links_are_rejected(self):
        for link in ('javascript:alert(1)', 'data:text/html,hello', '//example.org',
                     'http://example.org', 'https://user:password@example.org'):
            with self.subTest(link=link), self.assertRaises(ValueError):
                validate_link(link, self.root)

    def test_supported_links(self):
        for link in ('https://github.com/iamdpsingh', 'mailto:hello@example.org', '#toolkit', 'art.svg'):
            validate_link(link, self.root)

    def test_path_escape_and_symlink_are_rejected(self):
        with self.assertRaises(ValueError):
            local_file('../README.md', self.root)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'outside.svg'
            target.write_text('outside')
            (self.root / 'link.svg').symlink_to(target)
            with self.assertRaises(ValueError):
                local_file('link.svg', self.root)

    def test_remote_image_and_missing_alt_are_rejected(self):
        for image in ('<img src="https://example.org/a.svg" alt="Remote"/>', '<img src="art.svg"/>'):
            with self.subTest(image=image), self.assertRaises(ValueError):
                ProfileHTML(self.root).feed(image)

    def test_markdown_remote_image_is_rejected(self):
        (self.root / "README.md").write_text("# Profile\n![Tracker](https://example.org/pixel.svg)")
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_unreviewed_local_artwork_is_rejected(self):
        assets = self.root / "assets"
        assets.mkdir()
        (assets / "profile-banner.svg").write_bytes(self.svg.read_bytes())
        (assets / "stats.svg").write_bytes(self.svg.read_bytes())
        hero = '<img src="assets/profile-banner.svg" alt="Hero"/>'
        for extra in (hero, '<img src="assets/stats.svg" alt="Old statistics"/>'):
            with self.subTest(extra=extra):
                (self.root / "README.md").write_text("# Profile\n" + hero + extra)
                with self.assertRaises(ValueError):
                    validate(self.root)

    def test_external_portraits_and_unreviewed_css_are_rejected(self):
        for content in ('<image href="https://example.org/photo.jpg"/>',
                        '<image href="data:image/svg+xml;base64,PHN2Zy8+"/>',
                        '<style>@import "https://example.org/style.css";</style>',
                        '<style>.x { animation: spin 1s infinite; }</style>'):
            with self.subTest(content=content):
                self.svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">{content}</svg>')
                with self.assertRaises(ValueError):
                    validate_svg(self.svg)

    def test_source_elements_cannot_load_remote_images(self):
        with self.assertRaises(ValueError):
            ProfileHTML(self.root).feed('<picture><source srcset="https://example.org/a.svg"/></picture>')

    def test_active_readme_html_is_rejected(self):
        for html in ('<script>alert(1)</script>', '<img src="art.svg" alt="Art" onload="x"/>'):
            with self.subTest(html=html), self.assertRaises(ValueError):
                ProfileHTML(self.root).feed(html)


if __name__ == '__main__':
    unittest.main()
