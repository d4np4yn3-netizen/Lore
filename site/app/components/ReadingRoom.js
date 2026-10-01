'use client';
import { useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ASSET_ORIGIN, titleCase } from '../cards/experience';
import closeups from '../cards/closeups.json';
import { Editorial } from './Editorial';
import { Arrow, Book, Expand, Close } from './Icons';
const tabs = [['story','The story'],['art','Full artwork'],['clues','Easter eggs'],['book','Book pages']];

function Media({ asset, alt, ...props }) { return <Image src={asset.src} width={asset.width} height={asset.height} alt={alt} {...props}/>; }
export function ReadingRoom({ card, onClose, standalone = false, onNavigate, previous, next }) {
  const [tab,setTab] = useState('story');
  const [zoom,setZoom] = useState(false);
  const [page,setPage] = useState(0);
  const [selectedClue,setSelectedClue] = useState(null);
  const [inspectBox,setInspectBox] = useState(null);
  const artViewer=useRef(null);
  const bookViewer=useRef(null);
  useEffect(()=>{if(tab==='book'&&bookViewer.current){bookViewer.current.scrollLeft=zoom&&window.matchMedia('(min-width:761px)').matches?page*780:0;bookViewer.current.scrollTop=0;}},[tab,page,zoom]);
  useEffect(()=>{if(tab==='art'&&zoom&&inspectBox&&artViewer.current){const viewer=artViewer.current;const img=viewer.querySelector('img');viewer.scrollLeft=(inspectBox.x+inspectBox.w/2)*img.clientWidth-viewer.clientWidth/2;viewer.scrollTop=(inspectBox.y+inspectBox.h/2)*img.clientHeight-viewer.clientHeight/2;}},[tab,zoom,inspectBox]);
  const tabList=useRef(null);
  const content=useRef(null);
  function chooseTab(value){setTab(value);setZoom(false);setInspectBox(null);setSelectedClue(null);const room=content.current?.closest('dialog');if(room)room.scrollTop=0;}
  function inspectClue(index){setSelectedClue(index);requestAnimationFrame(()=>content.current?.querySelector('.closeup-controls button')?.focus({preventScroll:true}));const room=content.current?.closest('dialog');if(room)room.scrollTop=0;else content.current?.scrollIntoView({block:'start'});}
  function tabKeys(event){
    const i=tabs.findIndex(t=>t[0]===tab);
    const direction=event.key==='ArrowRight'?1:event.key==='ArrowLeft'?-1:0;
    const index=event.key==='Home'?0:event.key==='End'?tabs.length-1:direction?(i+direction+tabs.length)%tabs.length:null;
    if(index===null)return;event.preventDefault();chooseTab(tabs[index][0]);tabList.current.querySelectorAll('[role="tab"]')[index].focus();
  }
  return <div className={'reading-room'+(standalone?' standalone':'')}>
    <div className="reading-header"><div><span className="label gold">CRYPTO / {card.number}</span><h1 id="reading-title">{titleCase(card.title)}</h1></div>{onClose ? <button className="icon-button close-reading" aria-label="Close story and return to timeline" onClick={onClose}><Close/></button> : <Link className="back-link" href={'/#moment-'+card.slug}><Arrow direction="left"/> Timeline</Link>}</div>
    <div className="reading-meta"><span>{card.date}</span><span>{card.subject}</span><span className={'rarity '+card.rarity.toLowerCase()}>{card.rarity}</span></div>
    <div className="reading-tabs" role="tablist" aria-label="Explore this moment" ref={tabList} onKeyDown={tabKeys}>{tabs.map(([key,label])=><button key={key} role="tab" id={'tab-'+key} aria-controls={'panel-'+key} aria-selected={tab===key} tabIndex={tab===key?0:-1} onClick={()=>chooseTab(key)}>{label}{key==='clues' && <span>{card.eggs.length}</span>}</button>)}</div>
    <div className="reading-content" ref={content}>
      <section role="tabpanel" id={'panel-'+tab} aria-labelledby={'tab-'+tab} tabIndex={0}>
        {tab==='story' && <div className="story-layout"><div className="story-art"><button className="art-button" onClick={()=>chooseTab('art')} aria-label={'Explore the full artwork for '+card.title}><Media asset={card.media.artwork} alt={'Full illustration for '+titleCase(card.title)} sizes="(max-width: 760px) 90vw, 48vw" priority/><span>EXPLORE THE FULL ART <Expand/></span></button><p className="art-caption">ORIGINAL LORE ARTWORK <span>{card.id} / SEASON ONE</span></p></div><article className="story-copy"><p className="moment-phrase">{card.phrase}</p>{card.story.map((paragraph,i)=><p key={i}><Editorial text={paragraph}/></p>)}<button className="text-button" onClick={()=>chooseTab('clues')}>Look closer. Discover {card.eggs.length} details <Arrow/></button><details className="source-note"><summary>Sources &amp; the artist’s interpretation</summary><p><Editorial text={card.sourceNote}/></p></details></article></div>}
        {tab==='art' && <div className="art-panel"><div className="panel-intro"><div><span className="label gold">BEYOND THE CARD</span><h2>Every detail, in full.</h2><p>The complete illustration, without the card frame. Zoom in and take a closer look.</p></div><button className="outline-button" onClick={()=>setZoom(!zoom)} aria-pressed={zoom}><Expand/>{zoom?'Fit artwork':'Zoom artwork'}</button></div><div ref={artViewer} className={'art-viewer'+(zoom?' zoomed':'')} tabIndex={0} aria-label="Artwork viewer. When zoomed, scroll to explore."><Media asset={card.media.artwork} alt={'Complete approved illustration for '+titleCase(card.title)} sizes="(max-width:760px) 95vw, 1000px"/></div><div className="art-downloads"><a className="text-link" href={ASSET_ORIGIN+card.media.originalArt} target="_blank" rel="noopener noreferrer">Open original artwork ↗</a><a className="text-link" href={ASSET_ORIGIN+card.image} target="_blank" rel="noopener noreferrer">View collectible card ↗</a></div></div>}
        {tab==='clues' && <div className="clues-panel"><div className="panel-intro"><div><span className="label gold">HIDDEN IN PLAIN SIGHT</span><h2>A story inside the story.</h2><p>Historical references, visual metaphors and callbacks to other moments. Look closely.</p></div><span className="clue-count">{String(card.eggs.length).padStart(2,'0')} <small>DETAILS TO DISCOVER</small></span></div><div className="clue-grid" hidden={selectedClue!==null}>{card.eggs.map((egg,i)=>{const crop=closeups[card.id]?.[i];return <article className="clue" key={egg.title}>{crop ? <button className="clue-image" onClick={()=>inspectClue(i)} aria-label={'Enlarge detail: '+egg.title}><Image src={crop.src} alt={crop.alt} width={crop.width} height={crop.height} sizes="(max-width:760px) 90vw, 40vw"/><span><Expand/></span></button> : <button className="clue-context" onClick={()=>chooseTab('art')}>Explore in the full artwork <Arrow/></button>}<div className="clue-text"><span className="clue-number">{String(i+1).padStart(2,'0')}</span><div><h3>{egg.title}</h3><p><Editorial text={egg.text}/></p></div></div></article>})}</div>{selectedClue!==null && <div className="closeup-inspector"><div className="closeup-controls"><button className="text-button" onClick={()=>{const index=selectedClue;setSelectedClue(null);requestAnimationFrame(()=>content.current?.querySelectorAll('.clue-image')[index]?.focus({preventScroll:true}));}}><Arrow direction="left"/> All details</button><span className="label gold">{selectedClue+1} / {card.eggs.length}</span></div><div className="closeup-stage"><Image src={closeups[card.id][selectedClue].src} width={closeups[card.id][selectedClue].width} height={closeups[card.id][selectedClue].height} alt={closeups[card.id][selectedClue].alt} sizes="(max-width:760px) 90vw, 900px"/></div><div className="closeup-explanation"><span className="label gold">DETAIL {String(selectedClue+1).padStart(2,'0')}</span><h3>{card.eggs[selectedClue].title}</h3><p><Editorial text={card.eggs[selectedClue].text}/></p><button className="outline-button" onClick={()=>{const box=closeups[card.id][selectedClue].bbox;chooseTab('art');setZoom(true);setInspectBox(box);}}>Find it in the full artwork <Expand/></button></div><div className="closeup-navigation"><button className="outline-button" disabled={selectedClue===0} onClick={()=>inspectClue(selectedClue-1)}><Arrow direction="left"/> Previous detail</button><button className="outline-button" disabled={selectedClue===card.eggs.length-1} onClick={()=>inspectClue(selectedClue+1)}>Next detail <Arrow/></button></div></div>}<details className="source-note"><summary>Sources &amp; the artist’s interpretation</summary><p><Editorial text={card.sourceNote}/></p></details></div>}
        {tab==='book' && <div className="book-panel"><div className="panel-intro"><div><span className="label gold">THE COMPANION BOOK</span><h2>Turn the page.</h2><p>Full-bleed art. The history behind it. Read the two-page spread.</p></div><div className="book-actions"><button className="outline-button" onClick={()=>setZoom(!zoom)} aria-pressed={zoom}><Expand/>{zoom?'Fit pages':'Enlarge pages'}</button><a className="outline-button" href={ASSET_ORIGIN+card.media.originalBook} target="_blank" rel="noopener noreferrer"><Book/> Open PDF ↗</a></div></div><div className="book-page-switch"><button className={page===0?'active':''} onClick={()=>setPage(0)} aria-pressed={page===0}>01 / Artwork</button><button className={page===1?'active':''} onClick={()=>setPage(1)} aria-pressed={page===1}>02 / The story</button></div><div ref={bookViewer} className={'book-spread'+(zoom?' book-zoomed':'')} tabIndex={0} aria-label="Book reader. Enlarge pages and scroll for a closer look.">{card.media.pages.map((asset,i)=><button key={asset.src} className={'book-leaf'+(page===i?' selected':'')} onClick={()=>{setPage(i);setZoom(!zoom);}} aria-label={(zoom?'Fit':'Enlarge')+' book page '+(i+1)}><Media asset={asset} alt={titleCase(card.title)+' companion book page '+(i+1)+(i===0?', full artwork':', history and details')} sizes="(max-width:760px) 94vw, 45vw"/></button>)}</div><p className="book-caption">TWO-PAGE EDITORIAL SPREAD <span>OPEN THE PDF FOR FULL-SIZE READING ↗</span></p></div>}
      </section>
      <div className="reading-bottom"><Link href={'/cards/'+card.slug} className="permalink">Permanent story link ↗</Link><div>{previous && (onNavigate?<button onClick={()=>onNavigate(previous)} aria-label={'Previous moment: '+previous.title}><Arrow direction="left"/>Previous</button>:<Link href={'/cards/'+previous.slug}><Arrow direction="left"/>Previous</Link>)}{next && (onNavigate?<button onClick={()=>onNavigate(next)} aria-label={'Next moment: '+next.title}>Next moment<Arrow/></button>:<Link href={'/cards/'+next.slug}>Next moment<Arrow/></Link>)}</div></div>
    </div>
  </div>;
}

export function CardDialog({ card, onClose, onNavigate, previous, next }) {
  const dialog=useRef(null);
  useEffect(()=>{
    const el=dialog.current;const active=document.activeElement;const overflow=document.body.style.overflow;
    if(!el.open) el.showModal();document.body.style.overflow='hidden';
    return ()=>{document.body.style.overflow=overflow;el.close();if(active instanceof HTMLElement)active.focus({preventScroll:true});};
  },[]);
  useEffect(()=>{dialog.current.scrollTop=0;},[card.slug]);
  return <dialog ref={dialog} className="card-dialog" aria-labelledby="reading-title" onCancel={e=>{e.preventDefault();onClose();}} onClick={e=>{if(e.target===dialog.current)onClose();}}><ReadingRoom key={card.slug} card={card} onClose={onClose} onNavigate={onNavigate} previous={previous} next={next}/></dialog>;
}
