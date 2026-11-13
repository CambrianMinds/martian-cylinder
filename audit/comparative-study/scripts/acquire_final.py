from acquire import *
def main():
    path=OUT/'image-manifest.json';m=json.loads(path.read_text())
    record=page_job(('haroldswick','https://science.nasa.gov/resource/stick-shape-rice-size-features-on-martian-rock-haroldswick/'))
    if 'path' in record:
        url=record['resolved_url'].split('/jcr:')[0]
        record=image_record('haroldswick',url,'curated_analogue',{'caption_url':record['caption_url']})
    m['images']=[record if r['id']=='haroldswick' else r for r in m['images']]
    for name,url in [('rubin2017-pipes','https://schiebershalemudstoneresearchlab.org/PDF/Rubin-et-al-2017-Geology-sediment-pipes.pdf')]:
        try:
            data,_,_=fetch(url);(OUT/'sources'/f'{name}.pdf').write_bytes(data)
        except Exception as e:print(name,e)
    path.write_text(json.dumps(m,indent=2));print(record.get('width'),record.get('height'))
if __name__=='__main__':main()
