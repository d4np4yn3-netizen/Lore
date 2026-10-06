# Current Crypto print master v1.2 — approved framing, 6 October 2026

Dan approved the exact 001 v1.2 proof and authorised the 39-card rollout and a matching shared back. For **new Crypto print derivatives**, use `cards/crypto/master/print-v1.2` and its renderer/templates. This supersedes the 24 September print-v1.0 geometry below; creator masters and original approved artwork are unchanged.

Current delivery folder: `cards/crypto/print-ready/v1.2`. Canvas 816×1110 at 300 DPI, cut 744×1038, safe 684×981. Frame margins are 3.080 mm on all four straight sides for fronts; shared back 3.048 mm. The approved template is 900×1287.625 units, scale 672/886, translated equally by 66.690744921 in x and y. Illustration fills proportionally with the approved slight side crop. Preserve exact source image bytes, approved per-card artwork offsets, wording, rarity, font styles, logo paths and QR payload. Header/footer repositioning is the specific authorised exception.

See `cards/crypto/master/print-v1.2/approval.json` and `print-spec.json`. Keep the old masters and all historical print files. The 39 published numbered cards have active `print_ready` records in `cards/crypto/current-cards.json`; the three unnumbered archived designs keep their old records and placeholder QR status. Future cards must start with the new print template and follow the normal art/copy approval workflow. Physical printer/sample acceptance remains a separate status; do not infer it from visual approval or automated QA.

# Crypto collection rules — Season One

Approved direction recorded 19 September 2026. This collection-specific addendum
implements Dan's crypto decisions; creator collections retain six moments per creator.

| Item | Crypto rule |
| --- | --- |
| Launch order | Season One: Crypto; Season Two: Gaming Creators |
| Subject | One documented crypto-history event per card |
| Rarity | Assign each event one of Common, Uncommon, Rare, Epic, Legendary or Mythic |
| Scarcity | Higher rarity means smaller print quantities; counts and pack odds remain undecided |
| Finish | Standard and foil versions available for every card; foil is a finish, not a seventh rarity |
| Under the rarity | Event date, formatted DD MMM YYYY, in the existing counter position |
| Collection numbering | Season One working scope: 100 distinct event cards. Chronological three-digit collector numbers are the approved direction; 001 is Blind Signatures. Freeze the remaining 002–100 sequence after the proposed selection is agreed. Standard and foil share a number. |
| Footer | Approved 26 September 2026: `CRYPTO • SEASON 01 • NNN/100`, e.g. `CRYPTO • SEASON 01 • 001/100`. The 11 existing print derivatives retain their historical unnumbered footer until their collector numbers are locked and their new exports reviewed. |
| Subject label | Event's subject or network, e.g. BITCOIN, in the existing creator-name field |
| Format | LORE-FRONT-v4 visual geometry with approved LORE-CRYPTO-PRINT-v1.0 print derivative, six rarity colours, collection-specific approved art style, shared back v5 |

Do not make six rarity versions of one event. Standard and foil share the same
event, assigned rarity, artwork and wording. Production quantities must account
for both finishes; do not publish invented edition totals or pull rates.

## Layout and artwork

Keep LORE-FRONT-v4 geometry, badge padding, logo asset, title and QR placement. The approved field differences are: event date replaces the creator moment counter, subject replaces creator name, and the crypto season label replaces the creator footer. **Crypto print derivatives additionally use the approved phrase typography override in LORE-CRYPTO-PRINT-v1.0: the moment phrase is 25 units and 700 bold, retaining its position, tracking and rarity colour.** Do not apply this crypto-only phrase change to creator cards.

Use the existing renderer and BOTH exact approved art references, HODL v2 AND
Birth of Doge v2, before every new crypto card and revision. Inspect and supply
both art files directly to generation; typeset text in the existing fields. Read
[ART-STYLE.md](ART-STYLE.md) and [the style lock](style-reference-lock.json).
Crypto and Creator cards are separate products with separate drawing directions.
Both full illustrations, including backgrounds, props and creatures, are mandatory
crypto style references. Retain the exact brand
assets; generate illustrations separately. All objects and scenery must share
the drawn anime treatment. Easter eggs belong naturally in the scene's ink,
perspective and lighting, with evidence distinguishing fact from interpretation.

The first Pizza Day approval is an exact 1060 × 1484 raster preview. Preserve
its bytes and the separate selected illustration. No matching editable SVG was
retrieved. Do not call this preview a verified deterministic template export or
printer-ready artwork. Any future editable reconstruction must be compared with
this selection and reviewed for visible differences.

## Approved print master — 24 September 2026

Dan approved [LORE-CRYPTO-PRINT-v1.0](master/print-v1/README.md) for all six crypto rarities. The printer master is **816 × 1110 px at 300 DPI**, with **744 × 1038 px cut** and **684 × 981 px safe area**. The complete approved LORE front is uniformly inset with `translate(46.515 48.921) scale(0.8033)`; it is never stretched.

Use this print master for every new or rebuilt Crypto Season One front. The existing outer rarity border lands about **1.40 mm inside the cut at its nearest stroke edge**. Preserve the source artwork and all card-specific wording when converting approved cards. All 11 previously approved crypto fronts already have separate print derivatives with the bleed/cut/safe geometry and bold crypto phrase. Dan confirmed this phrase treatment again on 26 September 2026 after comparing the original and print-ready Doge crops.

Going forward, create the print-layout proof as part of each card's visual/copy review and save the approved illustration plus its printer-sized derivative together after sign-off. Do not wait for a second collection-wide conversion pass. A visually approved illustration can have a **review-only** print proof while its phrase, number or QR remains undecided; do not mark that proof as print released. The approved extended footer is a text-field change; retain the same locked front proportions and inset.

## Approved style migration

The four approved crypto cards completed style migration on 20 September 2026.
Dan then required BOTH HODL v2 and Birth of Doge v2 before every card. Preserve
old versions and review new work one card at a time. New approvals do not change
the pinned pair automatically. First Transfer is paused at Dan's request; follow
[the queue](STYLE-MIGRATION.md) for a different next design.

## Date and source evidence

Use the date of the represented event, not automatically the first discussion
or proposal date. Record request, completion and announcement dates separately
where they differ. Uncertain dates must remain uncertain; never invent a day.

Pizza Day uses **22 MAY 2010**: the offer was posted on 18 May, followed up on
21 May, and successful exchange confirmed on 22 May. The card depicts the
completed exchange. Source evidence is recorded beside the card.

Keep short source-backed moment phrases under the title. Exact excerpts may use
normalised capitals and punctuation; editorial wording must be labelled as such.
Screen timestamps, transaction/block times and delivery times are different
claims. A blockchain timestamp does not establish the minute a pizza arrived.

## Editorial coverage — approved direction, 20 September 2026

Dan requested the good, bad and ugly of crypto history: crashes, hacks, bans and
the wider culture, alongside achievements. His exact wording is preserved in
the Whitepaper approval record. Interpret “food” in that instruction as “good”
in context; Pizza Day already covers a literal food moment.

Cover breakthroughs and adoption, memes and communities, scams and fraud,
market crashes and institutional collapses, hacks and exploits, and bans or
regulatory shocks. Rarity reflects the selected event's place in the collection,
not moral approval of a person or scheme. Continue one documented event per card,
one rarity per event, both finishes, and both mandatory style references.

Candidate topics in EDITORIAL-BACKLOG.md are editorial options, not an approved
set size, rarity allocation or completed card. Research the exact event/date
before building. Distinguish an investor or meme participant from the organiser
of a fraud, and allegations from adjudicated facts. Symbolic Easter eggs should
be recorded as interpretation, not documentary props or evidence.

## Release and scope

Visual approval, historical verification, permission review, functional QR and
print release are separate statuses. Current Pizza Day QR is a demo placeholder.
Prepare printer-specific derivatives separately after receiving the actual
template and test readability and QR scanning at finished size.

SIX MOMENTS. ONE ICON. remains the creator-set line, not a crypto set-size claim.
COLLECT THE INTERNET. and ICONS ARE MADE OF MOMENTS. remain the brand lines.
The optional small NFT companion and possible revenue sharing are ideas under
consideration, not approved buyer entitlements or a launched product.

## Cross-card Easter eggs — approved direction, 27 September 2026

Dan wants recognisable items from one card hidden naturally inside other card illustrations as a recurring feature across the 100-card collection. The returning Blind Signatures envelope in 003 establishes the approach.

Build an object inventory as artwork is approved: source card, exact approved art path, distinctive object, and receiving-card placement/status. Reuse identifiable approved objects; do not invent the final objects of cards not yet designed. There is no requirement for every card to contain a crossover or for equal numbers on each card.

After all 100 illustrations exist, review the complete collection together and propose a deliberate pass adding suitable connections to earlier cards. Preserve their approved masters and present edited successors for review before promotion. This direction authorises planning the collection-wide pass, not silently changing existing approved art now.

Keep crossovers subtle, legible at card size and consistent with each scene's perspective, lighting and locked HODL/Doge art style. Record their source and meaning for the book and website, distinguishing intentional connections or forward references from historical props. The active inventory is [CROSS-CARD-ITEMS.md](CROSS-CARD-ITEMS.md).
