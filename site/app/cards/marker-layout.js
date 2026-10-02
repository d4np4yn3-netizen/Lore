// Keep touch targets apart while retaining each exact artwork anchor for its leader line.
export function placeClueMarkers(crops, width, height) {
  const inset = 24, distance = 52;
  const clampX = x => Math.min(width-inset, Math.max(inset,x));
  const clampY = y => Math.min(height-inset, Math.max(inset,y));
  const placed=[];
  for(const crop of crops){
    const anchorX=(crop.bbox.x+crop.bbox.w/2)*width;
    const anchorY=(crop.bbox.y+crop.bbox.h/2)*height;
    let point={x:clampX(anchorX),y:clampY(anchorY)};
    const available=p=>placed.every(other=>Math.hypot(p.x-other.x,p.y-other.y)>=distance);
    if(!available(point)){
      let best=null;
      // An increasing radius preserves proximity to the source detail without overlap.
      for(let radius=12;radius<Math.max(width,height)&&!best;radius+=8){
        for(let step=0;step<32;step++){
          const angle=step*Math.PI/16;
          const candidate={x:clampX(anchorX+Math.cos(angle)*radius),y:clampY(anchorY+Math.sin(angle)*radius)};
          if(available(candidate)){best=candidate;break;}
        }
      }
      if(best)point=best;
    }
    placed.push({...point,anchorX,anchorY});
  }
  return placed;
}
