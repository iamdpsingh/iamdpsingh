#!/usr/bin/env python3
"""Preserve the original profile layout and add source-scoped project cards."""
import json
import math
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


# Exact reviewed CSS: each row prints once; the last dot row finishes at 2.955 seconds.
AVATAR_STYLE = ('@media (prefers-reduced-motion: no-preference) {\n'
                '  .ink { animation: print-row .12s steps(1,end) 1 both; }\n'
                + ''.join(f'  .r{i} {{ animation-delay: {i*45}ms; }}\n' for i in range(64))
                + '}\n@keyframes print-row { from { opacity: 0; } to { opacity: 1; } }')


def avatar_print(root,snapshot):
    pattern=json.loads((root/'data/avatar-pattern.json').read_text())
    lines=pattern['lines']
    if (len(lines)!=64 or any(len(line)!=64 for line in lines)
            or any(char not in '0123456789abcdef' for line in lines for char in line)):
        raise ValueError('Avatar pattern must be a 64-by-64 luminance grid')
    total=snapshot['total']
    active=sum(day['count']>0 for day in snapshot['days'])
    directory=root/'assets'
    directory.mkdir(exist_ok=True)
    for theme in ('dark','light'):
        dark=theme=='dark'
        bg,ink,muted,border=('#080808','#eeeeee','#aaa6a2','#35312e') if dark else ('#faf9f6','#181818','#68625c','#d6d0c9')
        for mobile in (False,True):
            w,h=(640,910) if mobile else (1080,460)
            left,top,step=(36,47,8.8) if mobile else (24,32,6)
            body=[f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{bg}" stroke="{border}"/>']
            def text(x,y,value,size=18,color=ink,weight=400,extra=''):
                return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Courier New, monospace" '
                        f'font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>')
            body.append(text(left,top-17,'AVATAR / HALFTONE',12,muted,600))
            rows=[]
            for row,line in enumerate(lines):
                dots=[]
                for column,hex_value in enumerate(line):
                    level=int(hex_value,16)/15
                    density=level if dark else 1-level
                    radius=round(math.sqrt(density)*step*.48,2)
                    if radius < .15:
                        continue
                    cx=left+(column+.5)*step
                    cy=top+(row+.5)*step
                    dots.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{radius:g}"/>')
                rows.append(f'<g class="ink r{row}" fill="{ink}">'+''.join(dots)+'</g>')
            if mobile:
                x,y=36,670
                body.append(f'<path d="M36 630H604" stroke="{border}"/>')
                name_size,body_size,line_space=28,21,36
            else:
                x,y=490,80
                body.append(f'<path d="M458 28V432" stroke="{border}"/>')
                name_size,body_size,line_space=33,21,44
            body.append(text(x,y,'Dhruv Pratap Singh',name_size,ink,600))
            body.append(text(x,y+line_space,'Data Engineer / Full-Stack',body_size,muted))
            body.append(text(x,y+2*line_space,'PUBLIC ACTIVITY SNAPSHOT',14,muted,600))
            body.append(text(x,y+3*line_space,f'contributions   {total:,}',body_size))
            body.append(text(x,y+4*line_space,f'active days     {active}',body_size))
            body.append(text(x,y+5*line_space,f'updated         {snapshot["fetched_on"]}',body_size))
            if not mobile:
                body.append(text(x,386,'Python / SQL / Google Cloud',18,muted))
                body.append(text(x,417,'github.com/iamdpsingh',15,muted))
            for static in (False,True):
                filename=f'avatar-print-{theme}'+('-mobile' if mobile else '')+('-static' if static else '')+'.svg'
                style='' if static else '<style>'+AVATAR_STYLE+'</style>'
                svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
                     '<title id="title">Dhruv Pratap Singh — avatar formed from halftone dots</title>'
                     f'<desc id="desc">Pattern portrait derived from his GitHub avatar. Public contribution snapshot: {total:,} contributions, {active} active days, refreshed {snapshot["fetched_on"]}.</desc>'
                     +style+''.join(body+rows)+'</svg>\n')
                (directory/filename).write_text(svg)
    return '''<picture>
  <source media="(prefers-color-scheme: light) and (prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/avatar-print-light-mobile-static.svg" />
  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/avatar-print-dark-mobile-static.svg" />
  <source media="(prefers-color-scheme: light) and (prefers-reduced-motion: reduce)" srcset="assets/avatar-print-light-static.svg" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/avatar-print-dark-static.svg" />
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset="assets/avatar-print-light-mobile.svg" />
  <source media="(max-width: 600px)" srcset="assets/avatar-print-dark-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/avatar-print-light.svg" />
  <img src="assets/avatar-print-dark.svg" width="100%" alt="Dhruv Pratap Singh's GitHub avatar formed from printed halftone dots, beside a dated public contribution snapshot." />
</picture>

[Activity source and refresh date](data/contributions.json) · [Portrait pattern source](data/avatar-pattern.json)'''


def main():
    projects=project_catalog()
    content=(ROOT/'templates/profile.md').read_text()
    content=replace_block(content,'<!-- ADDITIONAL_PROJECTS_START -->','<!-- ADDITIONAL_PROJECTS_END -->',build_projects(projects))
    snapshot=json.loads((ROOT/'data/contributions.json').read_text())
    if snapshot['total'] != sum(day['count'] for day in snapshot['days']):
        raise ValueError('Contribution total must match dated daily data')
    content=replace_block(content,'<!-- AVATAR_PRINT_START -->','<!-- AVATAR_PRINT_END -->',avatar_print(ROOT,snapshot))
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
