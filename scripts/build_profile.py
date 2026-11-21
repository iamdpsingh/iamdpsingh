#!/usr/bin/env python3
"""Preserve the original profile layout and add source-scoped project cards."""
import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def safe_url(value):
    target = urlsplit(value)
    if (target.scheme != 'https' or not target.netloc or target.username or target.password
            or any(c in value for c in '\r\n <>"')):
        raise ValueError('Project and source links must be ordinary HTTPS URLs')
    return value


def plain(value):
    if not isinstance(value, str) or not value.strip() or any(c in value for c in '\n\r<>`[]'):
        raise ValueError('Use nonempty plain text for project copy')
    return value


def project_catalog():
    projects = json.loads((ROOT/'data/additional-projects.json').read_text())
    if not isinstance(projects,list):
        raise ValueError('Additional projects must be a JSON list')
    seen = set()
    for p in projects:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['id']) or p['id'] in seen:
            raise ValueError('Project IDs must be unique lowercase slugs')
        seen.add(p['id'])
        for key in ('name','summary'):
            plain(p[key])
        safe_url(p['url'])
        for key in ('stack','badges','highlights'):
            if not isinstance(p.get(key,[]),list):
                raise ValueError(f'{key} must be a list')
            for value in p.get(key,[]):
                plain(value)
        if p.get('period'):
            plain(p['period'])
        if p.get('card_title'):
            plain(p['card_title'])
        if p.get('button'):
            plain(p['button'])
        if p.get('emoji'):
            plain(p['emoji'])
        for source in p.get('sources',[]):
            safe_url(source)
        for item in p.get('evidence',[]):
            for key in ('id','status','claim','scope'):
                plain(item[key])
    return projects


def card(p):
    title=p.get('card_title',p['name'])
    parts=['<td width="50%" valign="top">','',f'### {p.get("emoji", "🚀")} {title}',p['summary'],'']
    logos={"Python":("python","00FFFF"),"FastAPI":("fastapi","00FFFF"),
           "PostgreSQL":("postgresql","4169E1"),"Next.js":("nextdotjs","FFFFFF"),
           "PySpark":("apachespark","E25A1C"),"BigQuery":("googlebigquery","00FFFF"),
           "Airflow":("apacheairflow","FF007F")}
    for label in p.get('badges',p.get('stack',[])[:4]):
        badge=quote(label.replace('-','--'),safe='')
        logo,color=logos.get(label,(None,"F97316"))
        icon=f'&logo={logo}&logoColor={color}' if logo else ''
        parts.append(f'![{label}](https://img.shields.io/badge/{badge}-050505?style=flat-square{icon})')
    label=p.get('button','View Project')
    badge=quote(label.replace(' ','_'),safe='')
    logo='github' if urlsplit(p['url']).netloc=='github.com' else 'vercel'
    parts += ['',f'<a href="{escape(p["url"],quote=True)}"><img src="https://img.shields.io/badge/{badge}-F97316?style=for-the-badge&logo={logo}&logoColor=white" alt="{escape(label+": "+title,quote=True)}" /></a>','']
    if p.get('period') or p.get('highlights') or p.get('evidence'):
        parts += ['<details>','<summary>Project details & evidence</summary>','']
        if p.get('period'):
            parts += [f'*Activity observed: {p["period"]}.*','']
        parts += ['- '+highlight for highlight in p.get('highlights',[])]
        if p.get('stack'):
            parts += ['','**Stack:** '+', '.join(p['stack'])+'.']
        parts += ['',f'[Full evidence & scope](docs/PROJECT_EVIDENCE.md#{p["id"]})','','</details>','']
    parts.append('</td>')
    return '\n'.join(parts)


def build_projects(projects):
    rows=[]
    for i in range(0,len(projects),2):
        cells=[card(p) for p in projects[i:i+2]]
        if len(cells)==1:
            cells.append('<td width="50%" valign="top"></td>')
        rows.append('<tr>\n'+'\n'.join(cells)+'\n</tr>')
    return '\n'.join(rows)


def evidence_document(projects):
    lines=['# Project evidence and scope','',
           'These are the owner-supplied, dated project records. OBSERVED, IMPLEMENTED, and REPORTED',
           'retain the meanings and limitations supplied by the owner. This profile update does not',
           'rerun the historical test suites, restore drills, production workloads, or provider gates.','',
           'The Rolewisp website could not be read by the web verification tool during this update;',
           'its URL is retained as supplied, without asserting present availability. The supplied',
           'Immune System source files were inspected: the diagnosis client is heuristic, the risk',
           'agent has explicit safety boundaries, and all five domain job families are present.','']
    for p in projects:
        lines += ['## '+p['id'].replace('-',' ').title(),'',f'**{p["name"]}**','']
        if p.get('period'):
            lines += ['Activity observed: '+p['period']+'.','']
        if p.get('stack'):
            lines += ['Stack: '+', '.join(p['stack'])+'.','']
        for item in p.get('evidence',[]):
            lines += [f'### {item["id"]} — {item["status"]}','',item['claim'],'',
                      '**Scope and limits:** '+item['scope'],'']
        lines += ['### Sources','']
        for n,url in enumerate(p.get('sources',[p['url']]),1):
            name=urlsplit(url).path.rsplit('/',1)[-1] or 'Application'
            lines.append(f'- [{name} ({n})]({url})')
        lines.append('')
    return '\n'.join(lines)


def replace_block(text,start,end,body):
    if text.count(start)!=1 or text.count(end)!=1:
        raise ValueError('Template markers must occur exactly once')
    pattern=re.escape(start)+r'.*?'+re.escape(end)
    return re.sub(pattern,lambda _:start+'\n'+body+'\n'+end,text,flags=re.S)


def engineering_profile(root):
    """Four small, static SVGs: light/dark and desktop/mobile; no external resources."""
    paths=[('Job sources','Python / PostgreSQL','Rolewisp'),
           ('Fleet telemetry','Pub/Sub / Dataflow','Fleet analytics'),
           ('Pipeline signals','Python / PySpark','Immune System')]
    directory=root/'assets'
    directory.mkdir(exist_ok=True)
    for theme in ('dark','light'):
        dark=theme=='dark'
        bg,card,ink,muted,line=('#050505','#131110','#fafafa','#bab2ad','#45352c') if dark else ('#faf9f6','#ffffff','#171717','#625b55','#ded3c9')
        accent='#F97316' if dark else '#a74213'
        for mobile in (False,True):
            w,h=(640,575) if mobile else (1080,350)
            parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
                   '<title id="title">Three project paths from source to shipped application</title>',
                   '<desc id="desc">Job sources through Python and PostgreSQL to Rolewisp; fleet telemetry through Pub/Sub and Dataflow to fleet analytics; pipeline signals through Python and PySpark to the Immune System.</desc>',
                   f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{bg}" stroke="{line}"/>']
            def text(x,y,value,size=20,color=ink,weight=400,extra=''):
                return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'
            if mobile:
                for i,(source,stack,project) in enumerate(paths):
                    y=20+i*181
                    parts += [f'<rect x="18" y="{y}" width="604" height="165" rx="10" fill="{card}" stroke="{line}"/>',
                              text(36,y+39,f'0{i+1} / {project}',28,ink,600),
                              text(36,y+78,source,23,muted),
                              f'<path d="M44 {y+88}V{y+112}M39 {y+107}L44 {y+112}L49 {y+107}" fill="none" stroke="{accent}" stroke-width="2"/>',
                              text(64,y+130,stack,24,accent,500)]
            else:
                for x,label in ((28,'SOURCE'),(410,'PROCESSING'),(792,'PROJECT')):
                    parts.append(text(x,32,label,13,muted,600,'letter-spacing="2"'))
                for i,row in enumerate(paths):
                    y=58+i*94
                    for x,label in zip((24,406,788),row):
                        parts += [f'<rect x="{x}" y="{y}" width="268" height="68" rx="9" fill="{card}" stroke="{line}"/>',
                                  text(x+134,y+42,label,20,accent if x==788 else ink,600 if x==788 else 400,'text-anchor="middle"')]
                    for start,end in ((292,406),(674,788)):
                        cy=y+34
                        parts.append(f'<path d="M{start} {cy}H{end-7}M{end-14} {cy-5}L{end-7} {cy}L{end-14} {cy+5}" stroke="{accent}" stroke-width="2" fill="none"/>')
            parts.append('</svg>')
            filename=f'project-dag-{theme}'+('-mobile' if mobile else '')+'.svg'
            (directory/filename).write_text('\n'.join(parts)+'\n')
    manifest=json.loads((root/'data/capabilities.json').read_text())
    if manifest.get('callable_mcp_server') is not False:
        raise ValueError('The illustrative manifest must not claim to be a running MCP server')
    return '''### Source → system → product

<picture>
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset="assets/project-dag-light-mobile.svg" />
  <source media="(max-width: 600px)" srcset="assets/project-dag-dark-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/project-dag-light.svg" />
  <img src="assets/project-dag-dark.svg" width="100%" alt="Three project paths: job sources to Rolewisp; fleet telemetry to fleet analytics; pipeline signals to the Data Pipeline Immune System." />
</picture>

[Rolewisp](https://rolewisp.vercel.app/) · [Fleet analytics](https://github.com/iamdpsingh/Project-5-Enterprise-Supply-Chain-Logistics-Data-Platform-with-Real-Time-Fleet-Analytics-on-GCP) · [Immune System](https://github.com/iamdpsingh/Data-Pipeline-Immune-System)

<details>
<summary>About me, as SQL</summary>

```sql
SELECT
    'Dhruv Pratap Singh' AS name,
    'Data Engineer' AS role,
    'Python / SQL / GCP' AS stack;
```

| name | role | stack |
| --- | --- | --- |
| Dhruv Pratap Singh | Data Engineer | Python / SQL / GCP |

</details>

<details>
<summary>Capability manifest</summary>

A portfolio capability description, not a running MCP server or callable tool registry.

```json
'''+json.dumps(manifest,indent=2)+'''
```

[Inspect the manifest source](data/capabilities.json)

</details>'''


def main():
    projects=project_catalog()
    content=(ROOT/'templates/profile.md').read_text()
    content=replace_block(content,'<!-- ENGINEERING_PROFILE_START -->','<!-- ENGINEERING_PROFILE_END -->',engineering_profile(ROOT))
    content=replace_block(content,'<!-- ADDITIONAL_PROJECTS_START -->','<!-- ADDITIONAL_PROJECTS_END -->',build_projects(projects))
    snapshot=json.loads((ROOT/'data/contributions.json').read_text())
    if snapshot['total'] != sum(day['count'] for day in snapshot['days']):
        raise ValueError('Contribution total must match dated daily data')
    activity=(f'**{snapshot["total"]:,} contributions** in GitHub\'s last-year calendar '
              f'({snapshot["days"][0]["date"]}–{snapshot["days"][-1]["date"]}); snapshot {snapshot["fetched_on"]}. '
              '[Source and daily data](data/contributions.json).')
    content=replace_block(content,'<!-- ACTIVITY_SUMMARY_START -->','<!-- ACTIVITY_SUMMARY_END -->',activity)
    month=datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%B %Y')
    date_badge=f'<p align="center">\n  <img src="https://img.shields.io/badge/Last%20Updated-{quote(month)}-2E9EF7?style=for-the-badge" alt="Last Updated: {month}" />\n</p>'
    content=replace_block(content,'<!--DATE_START-->','<!--DATE_END-->',date_badge)
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/PROJECT_EVIDENCE.md').write_text(evidence_document(projects))
    (ROOT/'README.md').write_text(content)
    print(f'Restored original layout with {len(projects)} additional project cards and scoped evidence')


if __name__ == '__main__':
    main()
