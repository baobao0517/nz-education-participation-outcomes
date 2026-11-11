"""Reproduce NZ education portfolio aggregates from Education Counts official public data.

Inputs:
 - data/verified/attendance_term2_regional_2022_2026.csv (validated 90-record extract)
 - data/raw/Machine-readable-school-leavers-2015-2025.zip (official, not committed)
Outputs:
 - data/verified/* aggregate CSVs
 - outputs/dashboard_data.json
 - outputs/validation_summary.json

No causal modelling, no individual-level data. A leaver may belong to multiple
ethnic categories, so 'All Leavers' is the sole denominator for unique totals.
"""
from __future__ import annotations
import csv,io,json,zipfile
from pathlib import Path
from collections import defaultdict,Counter
from statistics import mean
ROOT=Path(__file__).resolve().parents[1]
VERIFIED=ROOT/'data'/'verified'; RAW=ROOT/'data'/'raw'; OUT=ROOT/'outputs'
REGIONS=['Auckland','Bay of Plenty','Canterbury','Gisborne',"Hawke's Bay",'Manawatū-Whanganui', 'Marlborough','Nelson','Northland','Otago','Southland','Taranaki','Tasman','Waikato','Wellington','West Coast']
GROUPS={'eqi':['Fewer','Moderate','More','Unassigned'], 'age':['Left before 17th birthday','Stayed until age 17 or above'], 'ethnicity':['Māori','Pacific','European/Pākehā','Asian','MELAA','Other']}
ATT_FILE=VERIFIED/'attendance_term2_regional_2022_2026.csv'
ZIP_FILE=RAW/'Machine-readable-school-leavers-2015-2025.zip'
OUT.mkdir(exist_ok=True)

def round2(value):return round(value,2)
def rd_csv(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(path,rows,keys=None):
 if not rows: raise ValueError('Cannot write no rows: '+str(path))
 with path.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=keys or list(rows[0]));writer.writeheader();writer.writerows(rows)

def attendance_data():
 rows=rd_csv(ATT_FILE); seen=set();by={}
 assert len(rows)==90, ('attendance_count',len(rows))
 for r in rows:
  year=int(r['year']); region=r['region'];term=int(r['term']);n=int(r['students']);y=int(r['regular_students']);v=float(r['regular_attendance_pct'])
  assert term==2 and 2022<=year<=2026 and region in REGIONS+['All','Area Outside']
  assert (year,region) not in seen
  seen.add((year,region))
  assert 0<=y<=n and abs(100*y/n-v)<=0.07
  by[(year,region)]={'year':year,'region':region,'students':n,'attending_regularly':y,'rate':v}
 for year in range(2022,2027):
  assert all((year,r) in by for r in REGIONS+['All','Area Outside'])
  assert sum(by[(year,r)]['students'] for r in REGIONS+['Area Outside'])==by[(year,'All')]['students']
  assert sum(by[(year,r)]['attending_regularly'] for r in REGIONS+['Area Outside'])==by[(year,'All')]['attending_regularly']
 return by

def ncea_data():
 c=defaultdict(lambda:[0,0]);total_rows=0;rows_2025=0;nonqualification=Counter();duplicate_key=Counter()
 with zipfile.ZipFile(ZIP_FILE) as z:
  files=[n for n in z.namelist() if n.lower().endswith('.csv')]
  assert len(files)==1,files
  with z.open(files[0]) as raw:
   reader=csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8-sig',newline=''))
   for f in ('Year: Left School','Student: Ethnic Group','Student: Age (Retention To 17)','Qualification: Level 2 or Above','School: Equity Index Group','Region: Regional Council','Students (∑ Values)'):
    assert f in reader.fieldnames,f
   for row in reader:
    total_rows+=1;year=int(row['Year: Left School']); rows_2025+=year==2025
    reg=row['Region: Regional Council'].removesuffix(' Region'); ethn=row['Student: Ethnic Group']
    status=row['Qualification: Level 2 or Above']
    assert status in ('NCEA Level 2 or above','Below NCEA Level 2'),status
    n=int(row['Students (∑ Values)']);ach=(status=='NCEA Level 2 or above'); assert n>=0
    if ethn=='All Leavers':
     for k in [('history',year,reg,''),('overall',year,reg,'')]:
      c[k][0]+=n;c[k][1]+=n if ach else 0
     if year==2025:
      for kind,category in [('eqi',row['School: Equity Index Group'] or 'Unassigned'),('age',row['Student: Age (Retention To 17)'] or 'Unassigned')]:
       assert category in GROUPS[kind],(kind,category)
       c[(kind,year,reg,category)][0]+=n;c[(kind,year,reg,category)][1]+=n if ach else 0
    elif year==2025:
     assert ethn in GROUPS['ethnicity'],ethn
     c[('ethnicity',year,reg,ethn)][0]+=n;c[('ethnicity',year,reg,ethn)][1]+=n if ach else 0
 assert total_rows==365292,(total_rows,rows_2025)
 assert rows_2025==35889
 assert c[('overall',2025,'Not Applicable','')]==[6045,2560]
 assert sum(c[('overall',2025,r,'')][0] for r in REGIONS)==64741
 assert sum(c[('overall',2025,r,'')][1] for r in REGIONS)==52502
 assert sum(c[('overall',2025,r,'')][0] for r in REGIONS+['Not Applicable'])==70786
 assert sum(c[('overall',2025,r,'')][1] for r in REGIONS+['Not Applicable'])==55062
 for r in REGIONS+['Not Applicable']:
  if r in REGIONS:assert c[('overall',2025,r,'')][0]>0
  if r in REGIONS:
   n=c[('overall',2025,r,'')][0]
   assert sum(c[('eqi',2025,r,g)][0] for g in GROUPS['eqi'])==n
   assert sum(c[('age',2025,r,g)][0] for g in GROUPS['age'])==n
 return c,total_rows,rows_2025

def share(y,n):return round(100*y/n,2) if n else None

def build():
 a=attendance_data();c,total_rows,rows_2025=ncea_data()
 att_national=[{'year':y,'rate':a[(y,'All')]['rate'],'students':a[(y,'All')]['students']} for y in range(2022,2027)]
 ncea_nat={}
 for year in range(2015,2026):
  n=sum(c[('overall',year,r,'')][0] for r in REGIONS+['Not Applicable'])
  success=sum(c[('overall',year,r,'')][1] for r in REGIONS+['Not Applicable'])
  assert n>0
  ncea_nat[year]=dict(year=year,rate=round(100*success/n,1),rate_exact=100*success/n,leavers=n,attaining=success)
 assert ncea_nat[2025]['rate']==77.8 and ncea_nat[2019]['rate']==80.9
 regions=[];attendance_series=[];ncea_series=[];subgroups=[]
 for reg in REGIONS:
  attendance=[{'year':y,'rate':a[(y,reg)]['rate'],'national':a[(y,'All')]['rate'],'gap':round(a[(y,reg)]['rate']-a[(y,'All')]['rate'],2),'students':a[(y,reg)]['students']} for y in range(2022,2027)]
  ncea=[]
  for year in range(2015,2026):
   n,ach=c[('overall',year,reg,'')];assert n>0
   rate=round(100*ach/n,1); nat=ncea_nat[year]['rate']
   ncea.append({'year':year,'rate':rate,'national':nat,'gap':round(rate-nat,2),'leavers':n,'attaining':ach})
  a2025=attendance[-2];a2026=attendance[-1];n2025=ncea[-1]
  years_att=sum(x['gap']<0 for x in attendance)
  years_ncea=sum(x['gap']<0 for x in ncea if x['year']>=2019)
  age_n=c[('age',2025,reg,'Left before 17th birthday')][0]; total_n=n2025['leavers']
  more_n=c[('eqi',2025,reg,'More')][0]
  annual=round((a2026['rate']-attendance[0]['rate'])/4,3)
  regions.append({'region':reg,'attendance2026':a2026['rate'],'attendance2025':a2025['rate'],'attendanceGap2026':a2026['gap'],'attendanceGap2025':a2025['gap'],
   'annualImprovement':annual,'latestImprovement':round(a2026['rate']-a2025['rate'],1),
   'attendanceYearsBelow':years_att,'attendanceAverageGap':round(mean(v['gap'] for v in attendance),2),
   'ncea2025':n2025['rate'],'nceaGap2025':n2025['gap'],'nceaYearsBelow2019_2025':years_ncea,
   'nceaAverageGap2019_2025':round(mean(v['gap'] for v in ncea if v['year']>=2019),2),
   'leavers2025':total_n,'attaining2025':n2025['attaining'],'students2026':a[(2026,reg)]['students'],
   'earlyLeavingShare2025':share(age_n,total_n),'moreBarriersShare2025':share(more_n,total_n),
   'nceaChange2023_2025':round(ncea[-1]['rate']-next(v['rate'] for v in ncea if v['year']==2023),1)})
  attendance_series.extend({'region':reg,**row} for row in attendance)
  ncea_series.extend({'region':reg,**row} for row in ncea)
  for kind,groups in GROUPS.items():
   for group in groups:
    n,ach=c[(kind,2025,reg,group)]
    pooled_n=sum(c[(kind,2025,r,group)][0] for r in REGIONS)
    pooled_ach=sum(c[(kind,2025,r,group)][1] for r in REGIONS)
    if n:
     subgroups.append({'region':reg,'dimension':kind,'group':group,'n':n,'achieved':ach,'rate':share(ach,n),
       'pooledRate':share(pooled_ach,pooled_n),'pooledN':pooled_n,
       'differencePp':round(100*ach/n-100*pooled_ach/pooled_n,2),
       'compositionShare':share(n,total_n) if kind!='ethnicity' else None,
       'smallCell':n<30})
 # Public disclosure control: mask all original subgroup values for n < 30
 # in BOTH the website's embedded JSON and the versioned public CSV export.
 # Hiding them only in the visual would expose exact values via View Source.
 for item in subgroups:
  if item['smallCell']:
   for confidential in ('n','achieved','rate','differencePp','compositionShare'):
    item[confidential]=None
 assert len(regions)==16 and len(attendance_series)==80 and len(ncea_series)==176
 assert len({r['region'] for r in regions})==16
 assert sorted(r['region'] for r in regions if r['attendanceGap2025']<0 and r['nceaGap2025']<0)==sorted(['Gisborne','Northland','West Coast','Waikato','Marlborough','Manawatū-Whanganui',"Hawke's Bay"])
 assert sorted(r['region'] for r in regions if r['attendanceYearsBelow']==5)[:1]
 meta={'title':'NZ Education Participation & Outcomes Insights','prepared':'2026-11-11','regions':16,'attendanceYears':[2022,2023,2024,2025,2026],
  'nceaYears':[2019,2020,2021,2022,2023,2024,2025], 'nationalAttendance2026':64.3,'nationalAttendance2025':58.4,'nationalNcea2025':77.8,
  'attendanceTarget2030':80.0,'referenceNotes':'Attendance uses Term 2; 2026 current view, 2025 paired with 2025 school leavers. National published NCEA includes region Not Applicable.',
  'sourceAttendance':'https://www.educationcounts.govt.nz/statistics/attendance','sourceNcea':'https://www.educationcounts.govt.nz/statistics/school-leavers'}
 payload={'meta':meta,'attendanceNational':att_national,'nceaNational':[ncea_nat[y] for y in range(2019,2026)],'regions':regions,
          'attendanceHistory':attendance_series,'nceaHistory':[v for v in ncea_series if v['year']>=2019], 'subgroups':subgroups}
 (OUT/'dashboard_data.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 write_csv(VERIFIED/'attendance_regional_trends_2022_2026.csv',attendance_series)
 write_csv(VERIFIED/'ncea_regional_trends_2019_2025.csv',[v for v in ncea_series if v['year']>=2019])
 write_csv(VERIFIED/'ncea_2025_subgroups.csv',subgroups)
 write_csv(VERIFIED/'regional_dashboard_2025_2026.csv',regions)
 validation={'source_attendance_rows':90,'source_ncea_raw_rows':total_rows,'source_ncea_2025_rows':rows_2025,
             'regional_councils':16,'regional_attendance_rows':80,'regional_ncea_rows_2019_2025':112,
             'ncea_2025_national_leavers':70786,'ncea_2025_national_attaining':55062,
             'ncea_2025_region_attributed_leavers':64741,'ncea_2025_region_attributed_attaining':52502,
             'ncea_2025_unattributed_leavers':6045,'ncea_2025_unattributed_attaining':2560,
             'ncea_2025_all_nz_pct':round(100*55062/70786,2),'ncea_2025_attributed_regions_pct':round(100*52502/64741,2),
             'checks':['2022–2026 Term 2 source shares match counted regular students (±0.07pp publication rounding)',
              'Each year 16 regions + Area Outside attendance counts reconcile exactly to national All',
              'School leaver All Leavers only for unique counts; ethnicity groups separately parsed',
              '2025 school leaver national totals and regions + Not Applicable reconcile exactly',
              '2025 EQI and age buckets reconcile to each region distinct leaver total',
              'No region/year duplicates in attendance; all 16 regions represented 2019–2025 NCEA']}
 (OUT/'validation_summary.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
 print('Built verified data payload: national 2026',att_national[-1], 'national NCEA2025',ncea_nat[2025])
 print('2025 dual-low:',[r['region'] for r in regions if r['attendanceGap2025']<0 and r['nceaGap2025']<0])
 print('persistent 2019-25:',[r['region'] for r in regions if r['nceaYearsBelow2019_2025']==7])
 print('2025 quadrant counts:',Counter(('low' if r['attendanceGap2025']<0 else 'high' if r['attendanceGap2025']>0 else 'equal', 'low' if r['nceaGap2025']<0 else 'high') for r in regions))
 print('Validation:',json.dumps(validation,ensure_ascii=False))

if __name__=='__main__':build()
