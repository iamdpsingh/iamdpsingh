"""Data integrity, project-editing, and text-only output regression tests."""
import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch

from scripts import build_profile
from scripts.refresh_activity import CalendarParser


class ProfileDataTests(unittest.TestCase):
    def calendar(self, omit_tooltip=False):
        today = datetime.now(timezone.utc).date()
        html=[]
        for i in range(365):
            day = today - timedelta(days=364-i)
            html.append(f'<td data-date="{day}" data-level="1" id="day-{i}"></td>')
            if not (omit_tooltip and i == 0):
                html.append(f'<tool-tip for="day-{i}">1 contribution on a day.</tool-tip>')
        return ''.join(html)

    def test_calendar_recovers_daily_counts(self):
        parser=CalendarParser()
        parser.feed(self.calendar())
        days=parser.days()
        self.assertEqual(len(days),365)
        self.assertEqual(sum(day['count'] for day in days),365)
        self.assertEqual(days[-1]['date'],datetime.now(timezone.utc).date().isoformat())

    def test_missing_tooltip_stops_refresh(self):
        parser=CalendarParser()
        parser.feed(self.calendar(omit_tooltip=True))
        with self.assertRaises(ValueError):
            parser.days()

    def test_duplicate_calendar_cell_is_rejected(self):
        parser=CalendarParser()
        day=datetime.now(timezone.utc).date()
        cell=f'<td data-date="{day}" data-level="0" id="day"></td>'
        with self.assertRaises(ValueError):
            parser.feed(cell+cell)

    def test_new_project_can_be_added_with_one_json_entry(self):
        projects=json.loads((build_profile.ROOT/'data/projects.json').read_text())
        projects.append({'name':'Example added project','url':'https://github.com/iamdpsingh/example',
                         'category':'Data & analytics','description':'A new data pipeline.'})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            (root/'data/projects.json').write_text(json.dumps(projects))
            with patch.object(build_profile,'ROOT',root):
                loaded=build_profile.project_catalog()
            self.assertEqual(len(loaded),len(projects))
            self.assertEqual(sum(p.get('featured') is True for p in loaded),3)

    def test_unknown_category_does_not_silently_hide_a_project(self):
        projects=json.loads((build_profile.ROOT/'data/projects.json').read_text())
        projects.append({'name':'Example','category':'typo','description':'This must fail.'})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            (root/'data/projects.json').write_text(json.dumps(projects))
            with patch.object(build_profile,'ROOT',root), self.assertRaises(ValueError):
                build_profile.project_catalog()

    def test_checked_in_activity_sum_matches_daily_data(self):
        snapshot=json.loads((build_profile.ROOT/'data/contributions.json').read_text())
        self.assertEqual(snapshot['total'],sum(day['count'] for day in snapshot['days']))
        self.assertEqual(snapshot['source'],'https://github.com/users/iamdpsingh/contributions')

    def test_build_is_text_only_and_repeatable(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            for name in ('projects.json','contributions.json'):
                (root/'data'/name).write_bytes((build_profile.ROOT/'data'/name).read_bytes())
            (root/'README.md').write_text('## Background\nPreserved education and experience.\n')
            with patch.object(build_profile,'ROOT',root):
                build_profile.main()
                once=(root/'README.md').read_text()
                build_profile.main()
                self.assertEqual(once,(root/'README.md').read_text())
            for forbidden in ('<img', '<picture', '<svg', '<style', '<script', '!['):
                self.assertNotIn(forbidden,once)
            self.assertIn('Preserved education and experience.',once)
            self.assertIn('GitHub activity',once)


if __name__ == '__main__':
    unittest.main()
