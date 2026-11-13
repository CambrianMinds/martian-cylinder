"""Acquire and hash explicit Curiosity images and NASA caption pages."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit
from concurrent.futures import ThreadPoolExecutor
from html import unescape
import hashlib, json, re, time
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audit/comparative-study'
PAGES={
 'sheepbed': 'https://science.nasa.gov/resource/spherules-in-yellowknife-bay-unannotated/',
 'jura': 'https://science.nasa.gov/photojournal/crystal-shapes-and-two-toned-veins-on-martian-ridge/',
 'haroldswick': 'https://www.jpl.nasa.gov/images/pia22213-stick-shaped-features-on-martian-rock/',
 'naukluft': 'https://www.nasa.gov/image-article/sandstone-nodule-beside-naukluft-plateau-mount-sharp-mars/',
 'gatorback': 'https://science.nasa.gov/photojournal/curiosity-finds-gator-back-rocks-on-greenheugh/',
 'blackthorn': 'https://science.nasa.gov/image-article/apod-2022-march-9-a-flower-shaped-rock-on-mars/',
 'garden_city': 'https://science.nasa.gov/resource/garden-city-vein-complex-on-lower-mount-sharp-mars/',
 'vein_crystal': 'https://science.nasa.gov/resource/crystal-growth-texture-in-light-vein-at-garden-city/',
 'sticks_3810': 'https://science.nasa.gov/blog/sols-3812-3813-tiny-sticks-poking-out-at-us/',
 'nodules_3145': 'https://science.nasa.gov/blog/sols-3146-3148-keep-your-shoes-on/',
}
RAWS=[
 ('sol3556_585',3556,'3556MR1025170721700585C00_DXXX'),
 ('sol3556_584',3556,'3556MR1025170711700584C00_DXXX'),
 ('sol3556_586',3556,'3556MR1025170731700586C00_DXXX'),
 ('sol3415_182',3415,'3415MR1016480001600182C00_DXXX'),
 ('sol3415_181',3415,'3415MR1016440141600181C00_DXXX'),
 ('sol1850_4976',1850,'1850MR0096810000204976C00_DXXX'),
 ('sol0753_3753',753,'0753MR0032370300403753C00_DXXX'),
 ('sol0840_885',840,'0840MR0037360500500885C00_DXXX'),
]

def fetch(url):
    req=Request(url,headers={'User-Agent':'Curiosity-geological-comparison/1.0 (research; NASA public imagery)'})
    with urlopen(req,timeout=40) as r:
        return r.read(),r.url,r.headers.get('Content-Type','')

def image_record(name,url,role,extra=None):
    p=OUT/'images'/f'{name}.jpg'
    data,final,ct=fetch(url)
    p.write_bytes(data)
    with Image.open(p) as im:
        im.verify()
    with Image.open(p) as im:
        w,h=im.size;mode=im.mode
    return dict(id=name,url=url,resolved_url=final,path=p.relative_to(ROOT).as_posix(),
        sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),width=w,height=h,mode=mode,
        role=role,**(extra or {}))

def page_job(item):
    name,url=item
    try:
        data,final,ct=fetch(url)
        (OUT/'sources'/f'{name}.html').write_bytes(data)
        s=data.decode('utf-8',errors='replace')
        candidates=[]
        # The page's actual downloadable image links take precedence over thumbnails.
        for pattern in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',
                        r'(?:href|src)=["\']([^"\']+\.(?:jpg|jpeg|png)(?:\?[^"\']*)?)["\']']:
            for val in re.findall(pattern,s,re.I):
                u=urljoin(final,unescape(val))
                if u not in candidates: candidates.append(u)
        (OUT/'sources'/f'{name}-image-links.json').write_text(json.dumps(candidates,indent=2))
        # Download hero provisionally; atlas review checks subject and annotations.
        record=image_record(name,candidates[0],'curated_analogue',{'caption_url':final}) if candidates else {'id':name,'error':'no image links'}
        record['caption_sha256']=hashlib.sha256(data).hexdigest()
        return record
    except Exception as e:
        return {'id':name,'caption_url':url,'error':str(e)}

def raw_job(item):
    name,sol,prod=item
    url=f'https://mars.nasa.gov/msl-raw-images/msss/{sol:05d}/mcam/{prod}.jpg'
    try: return image_record(name,url,'whole_frame',{'sol':sol,'product_id':prod,'camera':'Mastcam Right'})
    except Exception as e: return {'id':name,'url':url,'error':str(e)}

def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(raw_job,RAWS))+list(pool.map(page_job,PAGES.items()))
    (OUT/'image-manifest.json').write_text(json.dumps({'retrieved_date':'2026-11-13','images':rows},indent=2))
    for row in rows: print(row['id'],row.get('error',f"{row.get('width')}x{row.get('height')}"))

if __name__=='__main__':main()
