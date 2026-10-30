import Link from 'next/link';
import { Header, Footer } from '../components/SiteChrome';
import { Arrow } from '../components/Icons';
import { absoluteUrl, SITE_NAME } from '../site-config';
import styles from './season-two.module.css';

const title = 'Help shape Season Two | HISTROVE';
const description = 'Preview HISTROVE Season Two: a planned 50-card crypto-history collection shaped by community suggestions. The suggestion form is not open yet.';
export const metadata = {
  title, description, alternates: { canonical: absoluteUrl('/season-two') },
  openGraph: { title, description, type: 'website', siteName: SITE_NAME, url: absoluteUrl('/season-two'), images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
};

export default function SeasonTwoPage() {
  return <div id="top"><a className="skip-link" href="#season-two-main">Skip to Season Two</a><Header seasonTwo/>
    <main className={styles.page} id="season-two-main">
      <section className={styles.hero} aria-labelledby="season-two-title"><div><span className="label gold">CRYPTO / SEASON TWO / IN DEVELOPMENT</span><h1 id="season-two-title">50 new cards.<br/><span>Help choose<br/>the moments.</span></h1><p className={styles.lead}>The next chapter starts with the stories you think deserve to be remembered.</p><p>We’re shaping a 50-card crypto season with ideas from the community. The breakthroughs, the turning points, the strange little moments that became part of the culture. Which one would you put on a card?</p><a className="gold-button" href="#suggestion-preview">See how to take part <Arrow direction="down"/></a></div><aside className={styles.count} aria-label="A planned collection of 50 cards"><span className="label">THE NEXT COLLECTION</span><strong>50</strong><span className="label gold">MOMENTS TO CHOOSE</span><p>Community ideas.<br/>Carefully researched stories.</p><small>Final selection to be confirmed.</small></aside></section>
      <section className={styles.process} aria-labelledby="season-two-process-title"><div><span className="label gold">HOW IT WILL TAKE SHAPE</span><h2 id="season-two-process-title">Your ideas.<br/>An editorial eye.</h2><p>When submissions open, suggestions will go to private editorial review—not straight onto the website. A suggestion will not guarantee a place in the collection.</p></div><ol><li><span>01</span><div><h3>Suggest a moment</h3><p>Name the event, give its date and explain why it matters. Add a credible public source.</p></div></li><li><span>02</span><div><h3>Research and review</h3><p>We’ll check the history, consider the sources and look at how each idea fits the wider collection.</p></div></li><li><span>03</span><div><h3>Shape the next 50</h3><p>Community suggestions will inform the season. The final selection remains editorial; this is not a binding vote or a competition.</p></div></li></ol></section>
      <section className={styles.suggestions} id="suggestion-preview" aria-labelledby="suggestion-title"><div><span className="label gold">START WITH A STORY</span><h2 id="suggestion-title">Which moment deserves a card?</h2><p>Four things will help us understand your idea. Write in your own words and link to a source rather than copying an article.</p><p>A suggestion will not sign you up for marketing emails.</p></div><div>
        <div className={styles.notice} id="suggestion-status"><strong>Preview only · Suggestions are not open yet.</strong><p>Private response storage has been set up and tested. Public suggestions remain closed while the privacy information is reviewed. These fields are disabled: this page does not send, collect or save suggestions.</p></div>
        {/* Deliberately not a form: no endpoint, submit handler or false success state. */}
        <fieldset className={styles.preview} disabled aria-describedby="suggestion-status suggestion-privacy"><legend>Preview of the suggestion details</legend>
          <label htmlFor="suggestion-moment">Crypto moment <span>Required when open</span></label><input id="suggestion-moment" type="text" placeholder="Name the event" autoComplete="off"/>
          <label htmlFor="suggestion-date">Date or period <span>Required when open</span></label><p id="date-hint">A day, month or year. Say if the exact date is uncertain.</p><input id="suggestion-date" type="text" placeholder="When did it happen?" autoComplete="off" aria-describedby="date-hint"/>
          <label htmlFor="suggestion-reason">Why does it deserve a card? <span>Required when open</span></label><textarea id="suggestion-reason" rows={5} placeholder="What happened, and why should it be remembered?"/>
          <label htmlFor="suggestion-source">Credible source link <span>Required when open</span></label><p id="source-hint">A public original announcement, document, archive or reliable report.</p><input id="suggestion-source" type="url" placeholder="https://…" autoComplete="off" aria-describedby="source-hint"/>
          <button className="gold-button" type="button" disabled>Suggestion form opens soon <Arrow/></button>
        </fieldset>
        <p className={styles.privacy} id="suggestion-privacy">Please don’t include contact details, private keys, wallet details or other personal information in a suggestion. Submitting an idea will not subscribe you to emails. <Link href="/season-two/privacy">Review the draft suggestions privacy information</Link>.</p>
      </div></section>
      <section className={styles.returnSection} aria-labelledby="season-one-return-title"><div><span className="label gold">WHILE THE NEXT CHAPTER TAKES SHAPE</span><h2 id="season-one-return-title">Discover Season One.</h2><p>Explore the collection that started it, from the ideas before Bitcoin to the culture that followed.</p></div><Link className="outline-button" href="/timeline?layout=grid">View all Season One cards <Arrow/></Link></section>
    </main><Footer seasonTwo/>
  </div>;
}
