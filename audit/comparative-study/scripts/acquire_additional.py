"""Expand corpus using image identifiers published by Wiens et al. (2017)."""
from acquire import *

MORE=[
 ('tochatwi',122,'0122MR0007650000200768E01_DXXX'),
 ('point_lake',302,'0302MR0012570100203802E01_DXXX'),
 ('point_lake_305a',305,'0305MR0012620110203874E01_DXXX'),
 ('point_lake_305b',305,'0305MR0012620080203871E01_DXXX'),
 ('twin_cairns',343,'0343MR0013880020301096E01_DXXX'),
 ('twin_cairns_b',343,'0343MR0013880040301098E01_DXXX'),
 ('winnipesaukee',654,'0654MR0027730000401977E01_DXXX'),
 ('shaler_306',306,'0306MR0012670140203944E01_DXXX'),
 ('shaler_pipe',308,'0308MR0012730520204018E01_DXXX'),
 ('shaler_pits',121,'0121MR0007560110200724E01_DXXX'),
 ('snake',173,'0173MR0009260660201874E01_DXXX'),
]
PDF='https://oro.open.ac.uk/48689/1/__science_research_SPS_Forschung_MSL_papers_Wiens_Fireringsetc_forORO_Hollow_Concretions_%26_Voids_in_Gale_Seds_Wiens_for_archive.pdf'

def main():
    path=OUT/'image-manifest.json'; manifest=json.loads(path.read_text())
    with ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(raw_job,MORE))
    for row in rows:
        row['selection']='Published geological challenge set; Wiens et al. 2017 supplementary image identifiers'
        row['citation_url']=PDF
    # Prefer actual originals over page preview thumbnails.
    for name in ['jura','sheepbed','gatorback','garden_city','blackthorn']:
        old=next(r for r in manifest['images'] if r['id']==name)
        url=old['resolved_url'].split('/jcr:')[0]
        if name=='jura': url='https://assets.science.nasa.gov/content/dam/science/psd/photojournal/pia/pia22/pia22211/PIA22211.jpg'
        try:
            updated=image_record(name,url,'curated_analogue',{'caption_url':old['caption_url'],'caption_sha256':old['caption_sha256']})
            manifest['images']=[updated if r['id']==name else r for r in manifest['images']]
        except Exception as e: print(name,str(e))
    for stem,url in [('wiens2017-hollow-concretions',PDF),('wiens2015-cylindrical','https://www.hou.usra.edu/meetings/lpsc2015/pdf/1249.pdf')]:
        try:
            data,final,ct=fetch(url);(OUT/'sources'/f'{stem}.pdf').write_bytes(data)
        except Exception as e: print(stem,str(e))
    manifest['images']=[r for r in manifest['images'] if r['id'] not in {x['id'] for x in rows}]+rows
    path.write_text(json.dumps(manifest,indent=2))
    for row in rows:print(row['id'],row.get('error',f"{row.get('width')}x{row.get('height')}"))

if __name__=='__main__':main()
