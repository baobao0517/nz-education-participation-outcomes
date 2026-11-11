"""Build readable HTML copies of Markdown docs for GitHub Pages.
Optional documentation dependency: `pip install mistune>=3`.
The dashboard itself has no external dependencies.
"""
from pathlib import Path
import mistune
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
md=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])
PAGES={'EXECUTIVE_SUMMARY.md':'executive-summary.html','METHODOLOGY.md':'methodology.html','DATA_VALIDATION.md':'validation.html','SOURCES.md':'sources.html'}
CSS='''
:root{color-scheme:light}*{box-sizing:border-box}body{background:#f5f8f9;color:#253749;margin:0;font:15px/1.75 system-ui,-apple-system,'Segoe UI',sans-serif}header{background:#142b3f;color:white;padding:18px 0}header a{color:#d6f4ef;text-decoration:none;font-weight:700}main{max-width:900px;margin:32px auto 65px;padding:42px 54px;background:white;border:1px solid #e0e8eb;border-radius:15px;box-shadow:0 6px 25px #142b3f0c}h1,h2,h3{color:#142b3f;line-height:1.2;letter-spacing:-.025em}h1{font-size:36px}h2{font-size:24px;margin-top:40px;padding-top:15px;border-top:1px solid #e2ecee}h3{font-size:18px;margin-top:25px}a{color:#078d91;text-underline-offset:3px}p{margin:14px 0}table{border-collapse:collapse;width:100%;margin:20px 0;font-size:13px;overflow-x:auto;display:block}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #e4eded;vertical-align:top}th{background:#f0f7f6;color:#285d65;font-size:12px}blockquote{margin:20px 0;border-left:3px solid #078d91;padding:5px 15px;background:#f1f8f7}code{font:13px/1.55 ui-monospace,monospace;background:#edf3f5;border-radius:4px;padding:2px 5px}pre{background:#eaf2f5;padding:17px;border-radius:8px;overflow-x:auto}pre code{padding:0}li{margin:6px 0}strong{color:#163247}footer{color:#697b86;font-size:12px;margin:20px 0}.wrap{width:min(94%,1000px);margin:auto}@media(max-width:650px){main{padding:23px 20px;margin:15px 10px}h1{font-size:29px}h2{font-size:22px}}
'''
for source,output in PAGES.items():
 title=source.removesuffix('.md').replace('_',' ').title()
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | NZ Education Insights</title><style>{CSS}</style></head><body><header><div class="wrap"><a href="./index.html">← NZ Education Insights · Interactive Dashboard</a></div></header><main>{md((DOCS/source).read_text(encoding='utf-8'))}<footer>Independent education analytics portfolio · Data as of 11 November 2026 · Source: Education Counts / Ministry of Education</footer></main></body></html>'''
 (DOCS/output).write_text(html,encoding='utf-8')
 print('Wrote',output)
