"""Extract / validate official Education Counts Term 2 Regional Council attendance.

Uses artifact_tool to read the Excel source; run once when source XLSX changes.
Source file is intentionally not distributed in the GitHub repository.
"""
from __future__ import annotations
import csv
from collections import Counter,defaultdict
from pathlib import Path
from artifact_tool import Blob,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data'/'raw'/'Regular-attendance-data-2022-2026-Term2.xlsx'
OUT=ROOT/'data'/'verified'/'attendance_term2_regional_2022_2026.csv'
REGIONS=['Auckland','Bay of Plenty','Canterbury','Gisborne',"Hawke's Bay",'Manawatū-Whanganui','Marlborough','Nelson','Northland','Otago','Southland','Taranaki','Tasman','Waikato','Wellington','West Coast']

def main():
 w=SpreadsheetFile.import_xlsx(Blob.load(str(SOURCE)))
 sheet=w.worksheets.get_item('Regional Council')
 values=sheet.get_range('A7:I330').values
 records=[];seen=set()
 for r in values:
  if len(r)<9 or not isinstance(r[0],(int,float)) or int(r[0]) not in range(2022,2027):continue
  if r[1]!=2:continue
  name=str(r[2]).removesuffix(' Region').strip()
  if name not in REGIONS+['All','Area Outside']:continue
  key=(int(r[0]),name)
  if key in seen: raise ValueError(f'Duplicate attendance year/region {key}')
  seen.add(key)
  total,regular=int(r[3]),int(r[4]); rate=float(r[8]); calc=100*regular/total
  if abs(calc-rate)>0.07:raise ValueError(f'Attendance count ratio mismatch {key}: {calc} != {rate}')
  records.append({'year':int(r[0]),'term':2,'region':name,'students':total,'regular_students':regular,'regular_attendance_pct':rate})
 for year in range(2022,2027):
  group=[v for v in records if v['year']==year]
  names={v['region'] for v in group}
  missing=set(REGIONS+['All','Area Outside'])-names
  if missing:raise ValueError(f'Missing {year}: {missing}')
  nz=next(v for v in group if v['region']=='All')
  if sum(v['students'] for v in group if v['region']!='All')!=nz['students']:raise ValueError('National student denominator mismatch')
  if sum(v['regular_students'] for v in group if v['region']!='All')!=nz['regular_students']:raise ValueError('National regular numerator mismatch')
 OUT.parent.mkdir(parents=True,exist_ok=True)
 with OUT.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(sorted(records,key=lambda x:(x['year'],x['region'])))
 print('Validated official attendance source:',len(records),'rows, 16 councils + national + area outside, 2022-2026 Term 2')
 print('National rates:',{v['year']:v['regular_attendance_pct'] for v in records if v['region']=='All'})

if __name__=='__main__':main()
