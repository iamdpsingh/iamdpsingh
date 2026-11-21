#!/usr/bin/env python3
"""Read GitHub's public calendar; save numbers only, never third-party SVG or code."""
import json
import re
import urllib.request
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://github.com/users/iamdpsingh/contributions"


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.counts = {}
        self.tooltip = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and 'data-date' in attrs:
            day = date.fromisoformat(attrs['data-date']).isoformat()
            level = int(attrs['data-level'])
            if level not in range(5) or attrs['id'] in self.cells:
                raise ValueError('Unexpected calendar level or duplicate cell')
            self.cells[attrs['id']] = {'date': day, 'level': level}
        if tag == 'tool-tip':
            self.tooltip = attrs.get('for')
            self.parts = []

    def handle_data(self, text):
        if self.tooltip:
            self.parts.append(text)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tooltip:
            match = re.fullmatch(r'\s*(No|[\d,]+) contributions? on .+\.\s*', ''.join(self.parts))
            if match:
                self.counts[self.tooltip] = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
            self.tooltip = None

    def days(self):
        days = []
        for key, day in self.cells.items():
            if key not in self.counts:
                raise ValueError('Missing contribution tooltip; GitHub markup may have changed')
            days.append({**day, 'count': self.counts[key]})
        days.sort(key=lambda day: day['date'])
        dates = [date.fromisoformat(day['date']) for day in days]
        if not 350 <= len(days) <= 380 or len(set(dates)) != len(dates):
            raise ValueError('Unexpected calendar size or duplicate dates')
        if any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
            raise ValueError('Contribution dates must be contiguous')
        if abs((dates[-1] - datetime.now(timezone.utc).date()).days) > 2:
            raise ValueError('GitHub returned an out-of-date calendar')
        return days


class GitHubRedirectsOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        from urllib.parse import urlsplit
        target = urlsplit(newurl)
        if target.scheme != 'https' or target.netloc != 'github.com':
            raise ValueError('Unexpected calendar redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def main():
    request = urllib.request.Request(SOURCE, headers={'User-Agent': 'iamdpsingh-profile/1.0'})
    with urllib.request.build_opener(GitHubRedirectsOnly()).open(request, timeout=20) as response:
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError('Calendar response is oversized')
    parser = CalendarParser()
    parser.feed(raw.decode('utf-8'))
    days = parser.days()
    header = re.search(r'([\d,]+)\s+contributions\s+in the last year', raw.decode('utf-8'))
    total = sum(day['count'] for day in days)
    if not header or int(header[1].replace(',', '')) != total:
        raise ValueError('Calendar cells do not match the GitHub total')
    snapshot = {'username': 'iamdpsingh', 'source': SOURCE,
                'fetched_on': datetime.now(timezone.utc).date().isoformat(),
                'total': total, 'days': days}
    destination = ROOT / 'data/contributions.json'
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot, indent=2) + '\n')
    temporary.replace(destination)
    print(f'Saved {len(days)} days and {total:,} contributions from GitHub')


if __name__ == '__main__':
    main()
