from pathlib import Path
from html import escape
import json, re
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site/index.html'
resources=json.loads((ROOT/'content/resources.json').read_text())
courses=json.loads((ROOT/'content/courses.json').read_text())

def replace_block(html, marker, text):
    pattern=fr'(<!-- {marker}_BEGIN -->)(.*?)(<!-- {marker}_END -->)'
    result,n=re.subn(pattern,lambda m:m.group(1)+'\n'+text+'\n'+m.group(3),html,flags=re.DOTALL)
    if n!=1: raise RuntimeError(f'Expected one {marker} block, got {n}')
    return result

def course_card(c):
    code=escape(c['id'])
    tags=''.join(f'<span class="course-tag">{escape(t)}</span>' for t in c['features'])
    return f'<a class="course-card {escape(c["class"])}" href="https://rhhanson-umd.github.io/{code}/" aria-label="Open {code} site"><div class="course-card-top"><span class="course-number">{code.replace("-"," ")}</span><span class="course-arrow" aria-hidden="true">&nearr;</span></div><h3>{escape(c["name"])}</h3><p>{escape(c["description"])}</p><div class="course-tags">{tags}</div></a>'

def card(r):
    search=(r['name']+' '+r['desc']+' '+' '.join(r['tags'])).lower()
    return f'<a class="resource-card" href="{escape(r["url"])}" target="_blank" rel="noopener noreferrer" data-category="{escape(r["category"])}" data-search="{escape(search,quote=True)}"><span class="resource-meta">{escape(r["url"].split("/")[2])} <span aria-hidden="true">&nearr;</span></span><strong>{escape(r["name"])}</strong><span class="resource-description">{escape(r["desc"])}</span><span class="tagline">{escape(" / ".join(r["tags"][:2]))}</span></a>'

def group(g):
    cards='\n'.join(card(r) for r in resources['resources'] if r['category']==g['id'])
    return f'<section class="resource-group" data-category-group="{escape(g["id"])}" aria-labelledby="heading-{escape(g["id"])}"><div class="resource-group-head"><span class="group-number">{escape(g["code"])}</span><div><h3 id="heading-{escape(g["id"])}">{escape(g["name"])}</h3><p>{escape(g["description"])}</p></div></div><div class="resource-grid">{cards}</div></section>'

known={g['id'] for g in resources['categories']}
for r in resources['resources']:
    if r['category'] not in known: raise ValueError(f'Unknown category: {r["category"]}')
html=SITE.read_text()
html=replace_block(html,'COURSES','\n'.join(map(course_card,courses)))
filters='<button class="filter-chip is-active" data-filter="all" aria-pressed="true">All resources</button>'+'\n'.join(f'<button class="filter-chip" data-filter="{escape(g["id"])}" aria-pressed="false">{escape(g["name"])}</button>' for g in resources['categories'])
html=replace_block(html,'FILTERS',filters)
html=replace_block(html,'RESOURCES','\n'.join(map(group,resources['categories'])))
html=re.sub(r'<div class="resource-counter" id="resource-counter" aria-live="polite">[^<]*</div>',f'<div class="resource-counter" id="resource-counter" aria-live="polite">{len(resources["resources"])} resources</div>',html)
SITE.write_text(html)
print(f'Built portal: {len(courses)} course cards, {len(resources["resources"])} reference links.')
