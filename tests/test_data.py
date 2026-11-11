import json,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'outputs'/'dashboard_data.json').read_text(encoding='utf-8'))
V=json.loads((ROOT/'outputs'/'validation_summary.json').read_text(encoding='utf-8'))
REG={r['region']:r for r in D['regions']}
class TestData(unittest.TestCase):
 def test_source_reconciliation(self):
  self.assertEqual((V['source_ncea_raw_rows'],V['ncea_2025_national_leavers'],V['ncea_2025_national_attaining']),(365292,70786,55062))
  self.assertEqual(V['ncea_2025_region_attributed_leavers']+V['ncea_2025_unattributed_leavers'],V['ncea_2025_national_leavers'])
  self.assertEqual(V['ncea_2025_region_attributed_attaining']+V['ncea_2025_unattributed_attaining'],V['ncea_2025_national_attaining'])
 def test_coverage(self):
  self.assertEqual(len(D['regions']),16)
  self.assertEqual(len(D['attendanceHistory']),80)
  self.assertEqual(len(D['nceaHistory']),112)
  self.assertEqual(len({r['region'] for r in D['regions']}),16)
 def test_national_benchmarks(self):
  self.assertEqual(D['attendanceNational'][0]['rate'],39.6)
  self.assertEqual(D['attendanceNational'][-1]['rate'],64.3)
  self.assertEqual(D['nceaNational'][-1]['rate'],77.8)
 def test_2025_dual_gap(self):
  cases=[r['region'] for r in D['regions'] if r['attendanceGap2025']<0 and r['nceaGap2025']<0]
  self.assertEqual(len(cases),7)
  self.assertTrue({'Gisborne','Northland','Waikato'}.issubset(cases))
 def test_persistence_and_tasman(self):
  for r in ('Gisborne','Northland','Waikato'):
   self.assertEqual(REG[r]['attendanceYearsBelow'],5)
   self.assertEqual(REG[r]['nceaYearsBelow2019_2025'],7)
  self.assertAlmostEqual(REG['Tasman']['attendanceGap2025'],3.0)
  self.assertAlmostEqual(REG['Tasman']['nceaGap2025'],-5.0)
 def test_subgroup_composition(self):
  for region in REG:
   row=[v for v in D['subgroups'] if v['region']==region and v['dimension']=='eqi']
   self.assertLessEqual(sum(v['n'] for v in row if v['n'] is not None),REG[region]['leavers2025'])
  self.assertTrue(any(r['smallCell'] for r in D['subgroups']))
  self.assertTrue(all(r['n'] is None and r['rate'] is None and r['achieved'] is None for r in D['subgroups'] if r['smallCell']))
 def test_dashboard_build(self):
  html=(ROOT/'docs'/'index.html').read_text(encoding='utf-8')
  self.assertIn('NZ Education',html)
  self.assertIn('portfolio-data',html)
  self.assertNotIn('__DASHBOARD_DATA__',html)
  self.assertIn('2030 target',html)
  self.assertGreater(len(html),70000)
 def test_methods_docs_present(self):
  for f in ('METHODOLOGY.md','DATA_VALIDATION.md','EXECUTIVE_SUMMARY.md','SOURCES.md'):
   self.assertTrue((ROOT/'docs'/f).exists(),f)
if __name__=='__main__':unittest.main()
