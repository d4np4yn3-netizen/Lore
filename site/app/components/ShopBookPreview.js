'use client';
import { useEffect, useRef, useState } from 'react';
import { CardDialog } from './ReadingRoom';
import { Book } from './Icons';

// Keep the reader on the shop route: Close, Escape and Back return to the product.
export default function ShopBookPreview({ card }) {
  const [open, setOpen] = useState(false);
  const trigger = useRef(null);
  const returnPoint = useRef(null);
  const hasOpened = useRef(false);
  useEffect(() => {
    const sync = () => setOpen(window.location.hash === '#book-preview');
    sync();
    window.addEventListener('popstate', sync);
    return () => window.removeEventListener('popstate', sync);
  }, []);
  function openPreview(event) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    returnPoint.current = window.scrollY;
    window.history.replaceState(window.history.state, '', '#companion-book');
    window.history.pushState({ ...window.history.state, histroveShopBook: true }, '', '#book-preview');
    setOpen(true);
  }
  function closePreview() {
    if (window.history.state?.histroveShopBook) window.history.back();
    else {
      window.history.replaceState(window.history.state, '', '#companion-book');
      setOpen(false);
      requestAnimationFrame(() => document.getElementById('companion-book')?.scrollIntoView());
    }
  }
  useEffect(() => {
    if (open) { hasOpened.current = true; return; }
    if (!hasOpened.current) return;
    if (returnPoint.current !== null) window.scrollTo({ top: returnPoint.current, behavior: 'instant' });
    else document.getElementById('companion-book')?.scrollIntoView({ behavior: 'instant', block: 'start' });
    trigger.current?.focus({ preventScroll: true });
  }, [open]);
  return <>
    <a ref={trigger} className="retail-cta" href="/?moment=pizza-day&view=book&return=shop" onClick={openPreview}>Preview the book pages <Book/></a>
    {open && <CardDialog card={card} initialTab="book" onClose={closePreview} closeLabel="Close book preview and return to the shop"/>}
  </>;
}
