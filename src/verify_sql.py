"""Run and independently check the published SQL examples using Python's sqlite3."""
from pathlib import Path
import sqlite3,csv,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data'/'verified'
rows=lambda fn: list(csv.DictReader((BASE/fn).open(encoding='utf-8-sig',newline='')))
con=sqlite3.connect(':memory:');con.row_factory=sqlite3.Row
con.executescript('''
CREATE TABLE attendance(year INTEGER,region TEXT,rate REAL,gap REAL,students INTEGER);
CREATE UNIQUE INDEX a_unique ON attendance(year,region);
CREATE TABLE ncea(year INTEGER,region TEXT,rate REAL,gap REAL,leavers INTEGER);
CREATE UNIQUE INDEX n_unique ON ncea(year,region);
CREATE TABLE subgroups(region TEXT,dimension TEXT,grp TEXT,n INTEGER,rate REAL,pooledRate REAL,differencePp REAL);
''')
att=rows('attendance_regional_trends_2022_2026.csv')
con.executemany('INSERT INTO attendance VALUES (?,?,?,?,?)',[(int(r['year']),r['region'],float(r['rate']),float(r['gap']),int(r['students'])) for r in att])
ncea=rows('ncea_regional_trends_2019_2025.csv')
con.executemany('INSERT INTO ncea VALUES (?,?,?,?,?)',[(int(r['year']),r['region'],float(r['rate']),float(r['gap']),int(r['leavers'])) for r in ncea])
groups=rows('ncea_2025_subgroups.csv')
con.executemany('INSERT INTO subgroups VALUES (?,?,?,?,?,?,?)',[(r['region'],r['dimension'],r['group'],int(r['n']),float(r['rate']),float(r['pooledRate']),float(r['differencePp'])) for r in groups if r['n'] and r['rate']])
assert len(att)==80 and len(ncea)==112
sql='\n'.join(line for line in (ROOT/'sql'/'education_insights.sql').read_text(encoding='utf-8').splitlines() if not line.lstrip().startswith('--'))
# Split on ';' and execute each statement separately; leading comments are valid SQLite SQL.
queries=[q.strip()+';' for q in sql.split(';') if q.strip() and any(x in q.upper() for x in ('SELECT','WITH'))]
assert len(queries)==4,len(queries)
results=[[dict(row) for row in con.execute(q)] for q in queries]
assert len(results[0])==16 and len(results[1])==16 and len(results[2])==16 and len(results[3])>25
assert abs(next(r['annual_improvement_pp_per_year'] for r in results[0] if r['region']=='Gisborne')-5.275)<0.001
assert next(r['below_nz_years_2019_2025'] for r in results[1] if r['region']=='Northland')==7
assert sum(r['descriptive_quadrant']=='Dual gap' for r in results[2])==7
assert next(r['descriptive_quadrant'] for r in results[2] if r['region']=='Tasman')=='Mismatch'
assert next(r['descriptive_quadrant'] for r in results[2] if r['region']=='Bay of Plenty')=='Mismatch'
print('SQLite verification: all 4 analytical queries passed; joined 16 region pairs, 7 dual-gap cases.')
