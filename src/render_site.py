"""Build a standalone, dependency-free interactive public dashboard."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'outputs'/'dashboard_data.json').read_text(encoding='utf-8'))
tpl=(ROOT/'src'/'dashboard_template.html').read_text(encoding='utf-8')
assert tpl.count('__DASHBOARD_DATA__')==1
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=tpl.replace('__DASHBOARD_DATA__',payload)
out=ROOT/'docs'/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html,encoding='utf-8')
print('Dashboard written',out,'bytes',out.stat().st_size)
