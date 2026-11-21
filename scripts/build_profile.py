#!/usr/bin/env python3
"""Build a text-only GitHub profile from a simple project catalog and real activity."""
import json
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def project_catalog():
    projects = json.loads((ROOT / 'data/projects.json').read_text())
    if not isinstance(projects, list) or sum(p.get('featured') is True for p in projects) != 3:
        raise ValueError('Choose exactly three featured projects')
    seen = set()
    for project in projects:
        for key in ('name', 'description', 'category'):
            value = project[key]
            if not isinstance(value, str) or not value.strip() or any(c in value for c in '\n\r[]<>`'):
                raise ValueError(f'Invalid project {key}')
        if project['name'] in seen:
            raise ValueError('Duplicate project name')
        seen.add(project['name'])
        for key in ('url', 'demo'):
            if key in project and not (project[key].startswith('https://') and not any(c in project[key] for c in ' \r\n<>()[\\')):
                raise ValueError('Project links must be HTTPS and contain no Markdown delimiters')
        if not project.get('featured') and project['category'] not in {'Data & analytics', 'Applications & AI', 'IoT & hardware'}:
            raise ValueError('Use a supported catalog category')
        if project.get('featured') and not project.get('url'):
            raise ValueError('Featured projects need repository links')
    return projects


def build_projects(projects):
    featured = [p for p in projects if p.get('featured')]
    lines = ['<!-- PROJECTS_START -->', '## Selected projects', '']
    for n, project in enumerate(featured,1):
        name = project['name']
        stack = project.get('stack', '')
        if not isinstance(stack, str) or any(c in stack for c in '\n\r`<>'):
            raise ValueError('Project stack must be plain text')
        chips = ' '.join(f'`{tool}`' for tool in stack.split(' / ') if tool)
        lines += [f'### [{name}]({project["url"]})', '', project['description'], '', chips, '']
    lines += ['<details>', '<summary>Explore previous projects — data, applications, and hardware</summary>', '']
    for category in ('Data & analytics','Applications & AI','IoT & hardware'):
        lines += [f'**{category}**','']
        for project in projects:
            if project.get('featured') or project['category'] != category:
                continue
            name = f'[{project["name"]}]({project["url"]})' if project.get('url') else project['name']
            line = f'- **{name}** — {project["description"]}'
            if project.get('demo'):
                line += f' [Live demo]({project["demo"]}).'
            lines.append(line)
        lines.append('')
    lines += ['[Browse all repositories](https://github.com/iamdpsingh?tab=repositories)', '', '</details>', '<!-- PROJECTS_END -->']
    return '\n'.join(lines)


def activity_text():
    snapshot = json.loads((ROOT / 'data/contributions.json').read_text())
    days = snapshot['days']
    if snapshot['total'] != sum(day['count'] for day in days):
        raise ValueError('Contribution total does not match daily counts')
    active = sum(day['count'] > 0 for day in days)
    last = date.fromisoformat(days[-1]['date'])
    sunday = last - timedelta(days=(last.weekday()+1)%7+12*7)
    by_day = {day['date']: day for day in days}
    rows = []
    for offset, label in enumerate(('Su','Mo','Tu','We','Th','Fr','Sa')):
        cells = []
        for week in range(13):
            day = (sunday+timedelta(days=week*7+offset)).isoformat()
            entry = by_day.get(day)
            if entry is None:
                cells.append(' ')
                continue
            level = int(entry['level'])
            if level not in range(5) or entry['count'] < 0:
                raise ValueError('Invalid activity cell')
            cells.append('.:+*#'[level])
        rows.append(label+'  '+' '.join(cells))
    chart = '\n'.join(rows)
    return f'''## GitHub activity

```text
Contributions  {snapshot['total']:,}
Active days    {active}
Refreshed      {snapshot['fetched_on']}
```

GitHub's last-year calendar: {days[0]['date']} to {days[-1]['date']}.

<details>
<summary>Recent 13 weeks as plain text</summary>

```text
{chart}

. none   : low   + moderate
* high   # highest
```

Intensity follows GitHub's calendar levels. Each column is one week.

</details>

[View activity on GitHub](https://github.com/iamdpsingh?tab=overview) · [Inspect daily data](data/contributions.json)

'''


def main():
    projects = project_catalog()
    project_section = build_projects(projects)
    readme = ROOT / 'README.md'
    existing = readme.read_text()
    background = existing[existing.index('## Background'):]
    portrait = ''
    portrait_path = ROOT / 'data/portrait.txt'
    if portrait_path.exists():
        art = portrait_path.read_text().rstrip('\n')
        if re.search(r'[^ .:\-=+*#%@\n]', art) or len(art.splitlines()) > 24 or any(len(line)>36 for line in art.splitlines()):
            raise ValueError('ASCII portrait must stay within its small, text-only palette')
        portrait = '<details>\n<summary>portrait.txt / my GitHub photo, rendered as text</summary>\n\n```text\n'+art+'\n```\n\nASCII rendering of my current GitHub avatar.\n\n</details>\n\n'
    intro = '''# Dhruv Pratap Singh

`data engineer` / `full-stack developer`

[work/](#selected-projects) / [stack/](#stack) / [activity.log](#github-activity) / [about.txt](#background)

```text
            data
             |
  ingest -- transform -- serve
  Python      SQL        apps
```

I build cloud pipelines, analytical models, and applications that make data useful.

[Portfolio](https://iamdpsingh-github-io.vercel.app/) / [LinkedIn](https://www.linkedin.com/in/dhruvpratapsingh30/) / [Email](mailto:dhruvpratapsingh30.official2.o@gmail.com)

'''
    stack = '''## Stack

- **Data:** Python, SQL, BigQuery, Airflow, dbt, Pandas.
- **Cloud & applications:** Google Cloud, PostgreSQL, Next.js, TypeScript, FastAPI, Flask.
- **Analytics & ML:** Power BI, Scikit-learn, XGBoost, Matplotlib, Seaborn.
- **Currently exploring:** PySpark, Kafka, Docker, Terraform.

<details>
<summary>Additional tools from projects and coursework</summary>

R, NumPy, Jupyter, SciPy, TensorFlow, PyTorch, OpenCV, Tableau, Databricks, Apache Spark, Delta Lake, Kubernetes, Linux, Raspberry Pi, MySQL, MongoDB, React, Node.js, JavaScript, and GitHub.

</details>

'''
    content = intro+portrait+project_section+'\n\n'+stack+activity_text()+background
    readme.write_text(content,encoding='utf-8')
    print(f'Built text-only profile: {len(projects)} projects and real contribution activity')


if __name__ == '__main__':
    main()
