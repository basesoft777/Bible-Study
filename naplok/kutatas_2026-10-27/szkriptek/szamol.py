R=7_200_000; plat=0.02*R
ment=1_936_800; mw=322_800*12; gm=373_200*12
def atal(bev, mod):
    inc=bev*0.55; adoz=max(0,inc-ment); szja=adoz*0.15
    if mod=='mellek': tb=adoz*0.185; sz=adoz*0.13
    elif mod=='fo_min': tb=max(inc,mw)*0.185; sz=max(inc,mw)*0.13
    else: tb=max(inc,gm)*0.185; sz=max(inc,gm)*0.13
    return bev-szja-tb-sz, szja,tb,sz
for m in ['mellek','fo_min','fo_gar']:
    print('B1',m,[round(x) for x in atal(R-plat,m)] if False else [round(x) for x in atal(R,m)], round(atal(R,m)[0]-plat))
vat=R*27/127; mor=0.05*R+3600*175; got=R-vat-mor
print('vat',round(vat),'mor',mor,'got',round(got))
for m in ['mellek','fo_min']:
    print('B2',m,[round(x) for x in atal(got,m)])
