import fs from 'node:fs';
import assert from 'node:assert/strict';
const source=fs.readFileSync('app/page.js','utf8');
const match=source.match(/useEffect\(\(\)=>\{(if\(isGrid\)return;.*?)\},\[isGrid\]\);/s);
assert(match,'Active-year effect is present');
const listeners=new Map(),queue=new Map();let active,token=0,disconnects=0;
const years=[1982,2008,2017,2018],tops=[-10000,-8000,-4000,400];
const sections=years.map((year,i)=>({dataset:{year:String(year)},getBoundingClientRect:()=>({top:tops[i]})}));
const window={innerHeight:761,addEventListener:(name,fn,options)=>listeners.set(name,{fn,options}),removeEventListener:(name,fn)=>{assert.equal(listeners.get(name)?.fn,fn);listeners.delete(name);}};
let observeCallback;
class Observer{constructor(fn){observeCallback=fn;}observe(){}disconnect(){disconnects++;}}
const raf=fn=>{const id=++token;queue.set(id,fn);return id;};
const cancel=id=>queue.delete(id);
const mount=new Function('isGrid','years','document','window','IntersectionObserver','requestAnimationFrame','cancelAnimationFrame','setActiveYear',match[1]);
const cleanup=mount(false,years,{querySelectorAll:()=>sections},window,Observer,raf,cancel,y=>{active=y;});
const flush=()=>{const callbacks=[...queue.values()];queue.clear();callbacks.forEach(fn=>fn());};
const emit=name=>{listeners.get(name).fn();flush();};
assert.equal(active,2017);assert.equal(listeners.get('scroll').options.passive,true);
// A direct 048 anchor can finish below the selection line without crossing another observer threshold.
tops[3]=140;emit('scroll');assert.equal(active,2018);
// Ordinary year selection and earlier anchors use the same position-derived result.
tops[2]=140;tops[3]=1800;emit('hashchange');assert.equal(active,2017);
tops[1]=140;tops[2]=2500;emit('scroll');assert.equal(active,2008);
tops[0]=140;tops[1]=2400;emit('scroll');assert.equal(active,1982);
// Back/Forward-style restored positions and a resize are recalculated from settled geometry.
tops.splice(0,4,-10000,-8000,-4000,140);emit('scroll');assert.equal(active,2018);
tops[3]=350;window.innerHeight=500;emit('resize');assert.equal(active,2017);
window.innerHeight=1000;emit('resize');assert.equal(active,2018);
listeners.get('scroll').fn();listeners.get('scroll').fn();observeCallback();assert.equal(queue.size,1);
cleanup();assert.equal(queue.size,0);assert.equal(listeners.size,0);assert.equal(disconnects,1);
assert.equal(mount(true,years,{},window,Observer,raf,cancel,()=>{}),undefined);
console.log('PASS: 048 direct-anchor scroll, ordinary/earlier year anchors, restored Back/Forward positions, resize, coalescing and cleanup use the correct position-derived active year');
