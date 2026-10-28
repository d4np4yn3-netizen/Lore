from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,binary_dilation

R=Path('/workspace/scratch/58d5f7ed8606/card100-new-sheriff')
Q=R/'manual-v9';Q.mkdir(exist_ok=True)
base_path=R/'sharpness-qa-v8/100-published-raw-v6.png'
donor_path=R/'100-the-new-sheriff-art-v8-horizontal-edge-no-dollar.png'
assert hashlib.sha256(base_path.read_bytes()).hexdigest()=='1062d25bce6e61747cf5dc0bbc06072d22d797e5ab235982e2b5c04df82124c4'
base=np.array(Image.open(base_path).convert('RGB'))
donor=np.array(Image.open(donor_path).convert('RGB'))
H,W=base.shape[:2]

def polygon(points):
    im=Image.new('L',(W,H));ImageDraw.Draw(im).polygon(points,fill=255)
    return np.array(im)>0

def feather(mask,width):
    return np.minimum(distance_transform_edt(mask)/width,1.0)*mask

# Region1: sign, own bracket and cyan spill. No other scene elements.
sign=polygon([(57,421),(149,419),(158,520),(151,533),(92,535),(56,494)])
sign |= polygon([(98,510),(126,510),(126,606),(98,590)])
alpha_sign=feather(sign,8)

# Region2: only exposed extra backing slab; the exact original paper and hand stay protected.
backing=polygon([(777,292),(980,171),(988,425),(793,506),(777,505)])
wanted_protection=polygon([(807,315),(946,226),(955,228),(968,432),(816,494)])
main_protection=polygon([(779,509),(998,410),(1013,861),(783,868)])
hand_protection=np.zeros((H,W),bool);hand_protection[390:560,:791]=True
protected=wanted_protection|main_protection|hand_protection
backing &= ~protected
alpha_backing=feather(backing,4)

# Region3: only blank lower-paper/pin strip and immediately exposed wood, below all date lettering.
bottom=polygon([(783,804),(1009,804),(1013,891),(783,877)])
alpha_bottom=feather(bottom,5)

# Keep original crisp parchment above the new edge instead of importing the softer donor band.
# Only reconstruct the old right tack footprint before moving its sharp original pixels upward.
bottom_donor=donor.astype(float).copy()
bottom_donor[804:831,788:1007]=base[804:831,788:1007]
yy,xx=np.mgrid[804:831,975:1007]
norm=((xx-992)/17)**2+((yy-831)/20)**2
a=np.clip((1-norm)/0.25,0,1)
bottom_donor[804:831,975:1007]=bottom_donor[804:831,975:1007]*(1-a[:,:,None])+base[804:831,940:972]*a[:,:,None]

out=base.astype(float)
for name,alpha in [('sign',alpha_sign),('backing',alpha_backing),('bottom',alpha_bottom)]:
    pixels=bottom_donor if name=='bottom' else donor
    out=out*(1-alpha[:,:,None])+pixels*alpha[:,:,None]
    Image.fromarray(np.uint8(alpha*255)).save(Q/f'{name}-alpha.png')

# Restore the sharp ORIGINAL corner tacks in the corrected positions within region3.
# These are source pixels, not freshly generated details; feather only their parchment perimeter.
pin_masks=[]
for name,box,offset in [('left',(789,830,812,856),(0,-26)),('right',(978,815,1005,846),(-2,-12))]:
    x0,y0,x1,y1=box;dx,dy=offset
    ph,pw=y1-y0,x1-x0
    yy,xx=np.mgrid[0:ph,0:pw]
    norm=((xx-(pw-1)/2)/((pw-1)/2))**2+((yy-(ph-1)/2)/((ph-1)/2))**2
    a=np.clip((1-norm)/0.22,0,1)
    tx0,ty0=x0+dx,y0+dy;tx1,ty1=x1+dx,y1+dy
    out[ty0:ty1,tx0:tx1]=out[ty0:ty1,tx0:tx1]*(1-a[:,:,None])+base[y0:y1,x0:x1]*a[:,:,None]
    m=np.zeros((H,W),bool);m[ty0:ty1,tx0:tx1]=a>0;pin_masks.append(m)

final=np.clip(np.rint(out),0,255).astype('uint8')
union=sign|backing|bottom
for m in pin_masks:union|=m
diff=np.any(final!=base,axis=2)
assert not np.any(diff&~union)
checks={}
for name,box in [('face_hair',(420,360,680,670)),('raised_hand',(725,395,791,560)),('main_text',(815,535,990,800)),('wanted_portrait',(830,340,950,425)),('lantern',(640,100,775,315))]:
    x0,y0,x1,y1=box;checks[name]=bool(np.array_equal(final[y0:y1,x0:x1],base[y0:y1,x0:x1]))
assert all(checks.values()),checks
path=R/'100-the-new-sheriff-art-v9-crisp-restored-candidate.png'
Image.fromarray(final).save(path)
Image.fromarray(np.uint8(union)*255).save(Q/'authorized-union-mask.png')
Image.fromarray(np.uint8(diff)*255).save(Q/'actual-diff-mask.png')
overlay=base.copy();overlay[union]=np.uint8(overlay[union]*0.45+np.array([0,240,255])*0.55)
Image.fromarray(overlay).save(Q/'mask-overlay.png')
ys,xs=np.where(diff)
audit={'base_sha256':hashlib.sha256(base_path.read_bytes()).hexdigest(),'donor_sha256':hashlib.sha256(donor_path.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':[W,H],'changed_pixels':int(diff.sum()),'authorized_union_pixels':int(union.sum()),'outside_union_changed_pixels':int((diff&~union).sum()),'protected_native_patches_byte_identical':checks,'output_path':str(path),'scope':'Three authorized localized corrections only; full-image base remains crisp publishedv6. No global sharpening/resampling/generation.'}
(Q/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
for name,box in [('wanted',(770,165,1000,515)),('bottom',(775,795,1020,875)),('sign',(30,395,190,560))]:
    im=Image.fromarray(final).crop(box);im.resize((im.width*3,im.height*3)).save(Q/f'{name}-after.png')
