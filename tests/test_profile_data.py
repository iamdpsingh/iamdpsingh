"""Calendar integrity, original-layout preservation, and evidence-scope tests."""
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
        projects=json.loads((build_profile.ROOT/'data/additional-projects.json').read_text())
        projects.append({'id':'example-project','name':'Example project',
                         'url':'https://github.com/iamdpsingh/example',
                         'summary':'A new data pipeline.'})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            (root/'data/additional-projects.json').write_text(json.dumps(projects))
            with patch.object(build_profile,'ROOT',root):
                loaded=build_profile.project_catalog()
            self.assertEqual(len(loaded),len(projects))
            self.assertIn('Example project',build_profile.build_projects(loaded))

    def test_project_copy_cannot_inject_html(self):
        projects=json.loads((build_profile.ROOT/'data/additional-projects.json').read_text())
        projects[0]['summary']='<script>bad()</script>'
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            (root/'data/additional-projects.json').write_text(json.dumps(projects))
            with patch.object(build_profile,'ROOT',root), self.assertRaises(ValueError):
                build_profile.project_catalog()

    def test_checked_in_activity_sum_matches_daily_data(self):
        snapshot=json.loads((build_profile.ROOT/'data/contributions.json').read_text())
        self.assertEqual(snapshot['total'],sum(day['count'] for day in snapshot['days']))
        self.assertEqual(snapshot['source'],'https://github.com/users/iamdpsingh/contributions')

    def test_original_layout_and_all_evidence_scopes_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'data').mkdir()
            (root/'templates').mkdir()
            for name in ('additional-projects.json','contributions.json','avatar-pattern.json'):
                (root/'data'/name).write_bytes((build_profile.ROOT/'data'/name).read_bytes())
            template=(build_profile.ROOT/'templates/profile.md').read_text()
            (root/'templates/profile.md').write_text(template)
            with patch.object(build_profile,'ROOT',root):
                build_profile.main()
                once=(root/'README.md').read_text()
                build_profile.main()
                self.assertEqual(once,(root/'README.md').read_text())
                projects=build_profile.project_catalog()
            self.assertIn('capsule-render.vercel.app',once)
            self.assertIn('readme-typing-svg.demolab.com',once)
            self.assertIn('V-INDEX / Rolewisp',once)
            self.assertIn('Data Pipeline Immune System',once)
            # Existing project cards and education remain byte-for-byte unchanged.
            start='<!-- ADDITIONAL_PROJECTS_END -->'
            end='<!-- ACTIVITY_SUMMARY_START -->'
            self.assertEqual(template.split(start)[1].split(end)[0],once.split(start)[1].split(end)[0])
            evidence=(root/'docs/PROJECT_EVIDENCE.md').read_text()
            for project in projects:
                for claim in project.get('evidence',[]):
                    self.assertIn(claim['scope'],evidence)
                    self.assertIn(claim['status'],evidence)
            self.assertIn('heuristic, not a verified live LLM integration',once)
            self.assertIn('Dated snapshot, not a live count',once)


if __name__ == '__main__':
    unittest.main()
