"""Persist visual screening independently of numerical fit quality."""
from pathlib import Path
import csv
import hashlib
import json

BASE=Path(__file__).resolve().parents[1]


def main():
    with (BASE/'image-manifest.csv').open(encoding='utf-8') as stream:
        products=[row for row in csv.DictReader(stream)
                  if row['processing_level']!='published field photograph']
    cases=[]
    for product in products:
        identifier=product['product_id']
        if identifier.startswith('0173'):
            setting='Yellowknife Bay, Sheepbed/Gillespie contact'
            morphology='Raised ring with partly concentric fabric. One section is exposed in bedrock.'
            decision='Eligible for partial geometric comparison'
            original_object='yellowknife-ring'
            scale='Paper text 7 cm and Table 1 10 cm disagree. Neither value supplies exact range here.'
            n,d='one exposed section','unobservable'
        elif identifier.startswith('1051'):
            setting='Marias Pass, Murray formation'
            morphology='Two separate ring structures. Larger-ring foreground arc is measured. Overlying debris obscures contacts.'
            decision='Eligible for partial geometric comparison';original_object='hewolf-pair'
            scale='Published diameters 7 and 36 cm for two distinct objects.'
            n,d='one exposed section per object','unobservable'
        elif identifier.startswith('052'):
            setting='Dingo Gap, Tappers'
            morphology='Annular rim and shallow bowl, rough wall and voids. Parts of outer margin overlap soil and shadow.'
            decision='Ambiguous boundary identification';original_object='tappers'
            scale='Published approximately 60-70 cm diameter.'
            n,d='one section visible, precise material/relief contour ambiguous','no complete axial generator'
        else:
            setting='150 m west of Dingo Gap'
            morphology='One irregular ring/section in a terrain view. Rover hardware occupies foreground.'
            decision='Eligible for partial geometric comparison';original_object='west-dingo-ring'
            scale='Published approximately 20 cm.'
            n,d='one section in context, not traced','unobservable'
        measured=identifier in ['0173ML0009261020105119E01_DRXX','0173MR0009261020201910E01_DRXX',
                                '1051ML0046250040306086E01_DRXX']
        product.update(eligibility=decision)
        product['sol']=str(int(product['sol']))
        cases.append({'case_id':identifier,'object_id':original_object,'setting':setting,
                      'mechanism_category':'interpreted sediment injection pipe',
                      'source':'Rubin et al. 2017 and supplement 2017002',
                      'dimensions':scale,'exposure':'embedded outcrop section',
                      'morphology':morphology,'N':n,'R':'unobservable', 'D':d,
                      'eligibility':decision,'measured':measured,
                      'reason': 'Required R and D families unavailable. Partial-rim measurements only.' if measured else
                                'Screening/context retained. No station extraction completed for this view.',
                      'annotation':'Single analyst, original PDS image viewed. No independent blind annotation.',
                      'rover_exclusion': 'All rover foreground is excluded from geological comparison.' if identifier.startswith(('NLB','NRB')) else '',
                      'orientation':'Oblique view of exposed cross section. Full object axis is concealed.'})
    supplementary=[
        ('rubin-4a','Carmel/Page near Escalante, Utah','interpreted fluidized-sediment pipe',
         'Eroding column, resistant rim, crude concentric fabric. Base remains embedded.','one top section','side margin visible','Eligible for partial geometric comparison','rubin2017.pdf'),
        ('rubin-4b','Carmel/Page near Escalante, Utah','interpreted fluidized-sediment pipe',
         'One section with eccentric, crinkly layers.','one section','unobservable','Eligible for partial geometric comparison','rubin2017.pdf'),
        ('paria-5b','Paria Plateau site 3/4, Utah','interpreted liquefaction/fluidization pipe',
         'Small exposed sandstone column with a rough top and embedded base.','one top section','side margin visible','Eligible for partial geometric comparison','nautilus.pdf'),
        ('paria-5c','Paria Plateau site 3/4, Utah','interpreted liquefaction/fluidization pipe',
         'Tall resistant column, rounded side and embedded base, metre scale bar.','top partly visible','side margin visible','Eligible for partial geometric comparison','nautilus.pdf'),
        ('loope-6b','Navajo Sandstone, south-central Utah','iron-oxide reaction-front concretion',
         'Long exposed rinded pipes weathered from host sandstone. This is a distinct cementation mechanism.','some cross sections','side margins visible','Eligible for partial geometric comparison','loope2011.pdf'),
        ('hunter-12','Southern San Juan Basin, New Mexico','probable solution-collapse pipe',
         'Large exposed pipe and host strata. Collapse interpretation kept separate from upward injection.','unclear','column margin visible','Insufficient observational geometry','hunter1992.pdf')]
    for identifier,setting,mechanism,morphology,n,d,decision,file in supplementary:
        source=BASE/'sources'/file
        source_urls={
            'rubin2017.pdf':'https://schiebershalemudstoneresearchlab.org/PDF/Rubin-et-al-2017-Geology-sediment-pipes.pdf',
            'nautilus.pdf':'https://pdfs.semanticscholar.org/662e/74839bf014863d96bb204f4543ea7c213c2e.pdf',
            'loope2011.pdf':'https://eas2.unl.edu/~dloope/pdf/MorphologicClues2011.pdf',
            'hunter1992.pdf':'https://pubs.usgs.gov/bul/1808l/report.pdf'}
        cases.append(dict(case_id=identifier,object_id=identifier,setting=setting,mechanism_category=mechanism,
            source=file,dimensions='Publication scale information only. No new physical measurement.',
            exposure='Published field photograph',morphology=morphology,N=n,R='unobservable',D=d,
            eligibility=decision,measured=False,reason='Original camera arrays and calibration unavailable. Publication image inspected for observability only.',
            annotation='Single analyst screening of primary publication. No subpixel metrology on printed figures.',
            orientation='Camera pose unavailable',rover_exclusion=''))
        products.append(dict(case_id=identifier,product_id='publication view '+identifier,
            instrument='field camera undocumented',acquisition_date='undocumented',sol='',processing_level='published field photograph',
            width='',height='',sample_bits='',path='sources/'+file,url=source_urls[file],
            sha256=hashlib.sha256(source.read_bytes()).hexdigest(),label_sha256='',
            eligibility=decision,optical_blur='original pixels unavailable'))
    (BASE/'boundary-inventory/screening.json').write_text(json.dumps(cases,indent=2)+'\n')
    fields=list(products[0])
    with (BASE/'image-manifest.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(products)
    print('Screened',len(cases),'views. Full N+R+D eligibility:',0)


if __name__=='__main__':
    main()
