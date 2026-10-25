export const ANALYTICS_PREFERENCE_KEY = 'histrove.analytics.v1';
export const PREFERENCE_MAX_AGE = 180 * 24 * 60 * 60 * 1000;

export function parsePreference(value, now = Date.now()) {
  try {
    const preference = JSON.parse(value);
    if (preference?.version !== 1 || !['accepted', 'declined'].includes(preference.choice)) return null;
    if (!Number.isFinite(preference.savedAt) || preference.savedAt > now || now - preference.savedAt >= PREFERENCE_MAX_AGE) return null;
    return preference.choice;
  } catch {
    return null;
  }
}

export function encodePreference(choice, now = Date.now()) {
  if (!['accepted', 'declined'].includes(choice)) throw new Error('Invalid analytics choice');
  return JSON.stringify({ version: 1, choice, savedAt: now });
}

export function savePreference(storage, choice, now = Date.now()) {
  try {
    storage.setItem(ANALYTICS_PREFERENCE_KEY, encodePreference(choice, now));
    return parsePreference(storage.getItem(ANALYTICS_PREFERENCE_KEY), now) === choice;
  } catch {
    // Remove an older acceptance if saving a withdrawal fails. Never reload on failure.
    if (choice === 'declined') {
      try { storage.removeItem(ANALYTICS_PREFERENCE_KEY); } catch { /* Show the storage warning. */ }
    }
    return false;
  }
}

// Only public catalogue pages. Drop unknown paths, custom events and every query/hash.
export function sanitizePageview(event, { allowed, origin, allowedPaths }) {
  if (!allowed || event?.type !== 'pageview') return null;
  try {
    const url = new URL(event.url);
    if (url.origin !== origin || !allowedPaths.has(url.pathname)) return null;
    return { type: 'pageview', url: `${url.origin}${url.pathname}` };
  } catch {
    return null;
  }
}
