# Basic Web Analytics — 25 October 2026

`@vercel/analytics/next` 2.0.1 in the existing Next.js app. Only consented public
pageviews; no custom events, user IDs, form content, replay, checkout or signup.

## Visitor control
- No SDK injection before explicit or valid remembered acceptance.
- Equal accept/decline choices; reversible footer control.
- Only choice/version/date in localStorage; choice expires after 180 days.
- Each pageview is rechecked, allowlisted and stripped of query/hash.
- Unknown paths, puzzle routes and custom events are discarded.
- Withdrawal immediately blocks the SDK callback. A verified saved withdrawal
  reloads to unload it. Failed storage never reloads into an older acceptance;
  a warning explains the page-only choice and how to remove an older preference.
- Changing a browser preference does not erase statistics already received.

Vercel can process referrer, browser/device and approximate location. Page-URL
filtering is not referrer filtering. No analytics cookies are enabled. The UI
links the provider privacy explanation without inventing a business identity
or claiming to replace a full site privacy notice.

## Costs / rollback
The owner approved basic metered Pro collection after disclosure. No plan,
Analytics Plus, billing limits or team-wide pause settings are changed.
Docs on 25 October 2026: $0.03/1,000 events using shared Pro usage credit;
no analytics-only hard cap is claimed.

Set `WEB_ANALYTICS_ENABLED = false` in `app/analytics-config.mjs` and redeploy to
stop the integration and its consent UI. Vercel also offers a per-project
Analytics disable control. Do not implicitly alter broader billing settings.

## Verification
Run `npm run test:analytics` and `npm run build`. Preserve existing tests/data;
known catalogue assertions are outside this analytics change. Before publishing,
recheck main and all catalogue/media/book/QR paths. After deployment, check first
visit, decline, reopen/accept, navigation, reload and withdrawal. Inspect script
gating and provider ingestion. Record network-inspection limits honestly.

Vercel ignores headless/automated clients: zero requests alone is not proof;
verify a positive accepted pageview before trusting negative results.

Official references:
- https://vercel.com/docs/analytics/quickstart
- https://vercel.com/docs/analytics/privacy-policy
- https://vercel.com/docs/analytics/redacting-sensitive-data
- https://vercel.com/docs/analytics/limits-and-pricing
- https://vercel.com/docs/spend-management
