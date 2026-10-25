'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { Analytics } from '@vercel/analytics/next';
import { ANALYTICS_PREFERENCE_KEY, parsePreference, savePreference, sanitizePageview } from '../analytics-policy.mjs';

const ConsentContext = createContext(null);

export function AnalyticsPreferences() {
  const consent = useContext(ConsentContext);
  if (!consent) return null;
  return <button type="button" className="analytics-preferences" onClick={consent.openPreferences}>Analytics preferences</button>;
}

export default function AnalyticsConsentProvider({ children, allowedPaths }) {
  const [choice, setChoice] = useState(null);
  const [ready, setReady] = useState(false);
  const [open, setOpen] = useState(false);
  const [storageWarning, setStorageWarning] = useState(false);
  const allowed = useRef(false);
  const persisted = useRef(false);
  const heading = useRef(null);
  const returnFocus = useRef(null);
  const publicPaths = useMemo(() => new Set(allowedPaths), [allowedPaths]);

  const stop = useCallback(() => {
    // Unmounting Analytics does not remove the injected SDK. Stop its callback too.
    allowed.current = false;
    window.va?.('beforeSend', () => null);
  }, []);

  useEffect(() => {
    function readChoice() {
      let saved = null;
      try { saved = parsePreference(window.localStorage.getItem(ANALYTICS_PREFERENCE_KEY)); } catch { /* Default to no collection. */ }
      allowed.current = saved === 'accepted';
      persisted.current = saved !== null;
      setChoice(saved);
      setOpen(saved === null);
      return saved;
    }
    readChoice();
    setReady(true);
    function onStorage(event) {
      if (event.key !== null && event.key !== ANALYTICS_PREFERENCE_KEY) return;
      const previouslyAllowed = allowed.current;
      const saved = readChoice();
      if (previouslyAllowed && saved !== 'accepted') {
        stop();
      }
    }
    window.addEventListener('storage', onStorage);
    return () => { window.removeEventListener('storage', onStorage); stop(); };
  }, [stop]);

  const beforeSend = useCallback(event => {
    let stillAllowed = allowed.current;
    // Check again per event: expiry/another tab's withdrawal must fail closed.
    if (stillAllowed && persisted.current) {
      try { stillAllowed = parsePreference(window.localStorage.getItem(ANALYTICS_PREFERENCE_KEY)) === 'accepted'; }
      catch { stillAllowed = false; }
    }
    return sanitizePageview(event, { allowed: stillAllowed, origin: window.location.origin, allowedPaths: publicPaths });
  }, [publicPaths]);

  const openPreferences = useCallback(event => {
    returnFocus.current = event.currentTarget;
    setOpen(true);
    requestAnimationFrame(() => heading.current?.focus());
  }, []);
  const context = useMemo(() => ({ openPreferences }), [openPreferences]);

  function saveChoice(next) {
    const revoking = allowed.current && next === 'declined';
    if (next === 'declined') stop();
    persisted.current = false;
    try { persisted.current = savePreference(window.localStorage, next); }
    catch { /* Access to localStorage itself may be blocked. */ }
    allowed.current = next === 'accepted';
    setChoice(next);
    setStorageWarning(!persisted.current);
    setOpen(!persisted.current);
    returnFocus.current?.focus();
    // Clear the SDK and its listeners after withdrawal, not just the React component.
    if (revoking && persisted.current) window.location.reload();
  }

  return <ConsentContext.Provider value={context}>
    {children}
    {ready && choice === 'accepted' ? <Analytics beforeSend={beforeSend} debug={false} /> : null}
    {ready && open ? <section className="analytics-choice" aria-labelledby="analytics-heading">
      <div className="analytics-choice-copy">
        <h2 id="analytics-heading" ref={heading} tabIndex={-1}>Optional page analytics</h2>
        <p>May HISTROVE use Vercel Web Analytics to understand which pages are useful? Nothing is sent to this analytics service until you accept. Declining will not affect the site.</p>
        {storageWarning ? <p role="status">Your browser could not save this choice. It applies to this page only. If you previously accepted, clear this site’s stored data before your next visit to remove that older preference.</p> : null}
        <details>
          <summary>What is collected and how to change your choice</summary>
          <p>Vercel receives page views, referring websites and technical information such as browser, device type and approximate location. It produces aggregate statistics without analytics cookies or cross-site tracking. Its visitor-session hash lasts up to 24 hours. We strip page query strings and fragments and do not send custom events, account identifiers or form entries.</p>
          <p>We store only this preference and its date in your browser. Your choice expires after 180 days. If browser storage is unavailable, your choice applies only to this page. Use “Analytics preferences” in the footer to change it. Declining stops further collection and normally reloads this page; it does not erase statistics already received.</p>
          <p><a href="https://vercel.com/docs/analytics/privacy-policy" target="_blank" rel="noreferrer">Vercel’s analytics privacy explanation</a></p>
        </details>
      </div>
      <div className="analytics-choice-actions">
        <button type="button" onClick={() => saveChoice('accepted')}>Accept analytics</button>
        <button type="button" onClick={() => saveChoice('declined')}>Decline analytics</button>
        {choice ? <button type="button" onClick={() => { setOpen(false); returnFocus.current?.focus(); }}>Keep current choice</button> : null}
      </div>
    </section> : null}
  </ConsentContext.Provider>;
}
