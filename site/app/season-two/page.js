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
    <main className={`${styles.page} ${styles.artPage}`} id="season-two-main">
      <section className={styles.hero} aria-labelledby="season-two-title">
        <div className={styles.heroCopy}><span className="label gold">CRYPTO / SEASON TWO / IN DEVELOPMENT</span>
          <h1 id="season-two-title">50 new cards.<br/><span>Which moments<br/>make the cut?</span></h1>
          <p>Help shape the next chapter of crypto history. Bring us the stories you think deserve a card.</p>
          <a className="gold-button" href="#suggestion-preview">See how to take part <Arrow direction="down"/></a>
        </div>
        <div className={styles.heroArt}>
          <div className={styles.artDuo}>
            <figure><img src="/archive/038-art.webp" width="1060" height="1484" alt="Season One CryptoPunks illustration"/></figure>
            <figure><img src="/archive/046-art.webp" width="1060" height="1484" alt="Season One CryptoKitties illustration"/></figure>
          </div>
          <p className={styles.artCredit}>A taste of our art: Season One illustrations. Season Two artwork is still to come.</p>
        </div>
      </section>
      <section className={styles.process} aria-label="How suggestions will take shape"><ol>
        <li><span>01</span><div><h2>Pick a moment</h2><p>The breakthroughs, turning points and strange little stories worth remembering.</p></div></li>
        <li><span>02</span><div><h2>Tell us why</h2><p>Add the date, your reason and a credible public source.</p></div></li>
        <li><span>03</span><div><h2>We research &amp; select</h2><p>Ideas go to private editorial review. The final 50 aren’t decided by a vote.</p></div></li>
      </ol></section>
      <section className={styles.suggestions} id="suggestion-preview" aria-labelledby="suggestion-title">
        <div><span className="label gold">START WITH A STORY</span><h2 id="suggestion-title">Your idea could inspire<br/>the next collection.</h2><p>Four details. No marketing signup.</p>
          <details className={styles.details}><summary>How suggestions will be used</summary><p>Suggestions inform the collection but do not guarantee inclusion. Final selection remains editorial; this is not a competition. Please write in your own words and link to a source, rather than copying an article.</p><p>Private response storage has been set up and tested. Public suggestions remain closed while the privacy information is reviewed. This page does not send, collect or save suggestions.</p><p><Link href="/season-two/privacy">Review the draft suggestions privacy information</Link>.</p></details>
        </div>
        <div className={styles.formBox}>
          <div className={styles.notice} id="suggestion-status">Suggestions open soon. These preview fields are disabled.</div>
          {/* Deliberately not a form: no endpoint, submit handler or false success state. */}
          <fieldset className={styles.preview} disabled aria-describedby="suggestion-status suggestion-privacy"><legend className={styles.srOnly}>Preview of the suggestion details</legend>
            <div className={styles.pair}><div><label htmlFor="suggestion-moment">Crypto moment</label><input id="suggestion-moment" type="text" placeholder="Name the event" autoComplete="off"/></div><div><label htmlFor="suggestion-date">Date or period</label><input id="suggestion-date" type="text" placeholder="When did it happen?" autoComplete="off"/></div></div>
            <label htmlFor="suggestion-reason">Why does it deserve a card?</label><textarea id="suggestion-reason" rows={3} placeholder="What happened, and why should it be remembered?"/>
            <label htmlFor="suggestion-source">Credible source link</label><input id="suggestion-source" type="url" placeholder="https://…" autoComplete="off"/>
            <button className="gold-button" type="button" disabled>Suggestion form opens soon <Arrow/></button>
          </fieldset>
          <p className={styles.privacy} id="suggestion-privacy">No information is collected in this preview. Please don’t include personal information or wallet details.</p>
        </div>
      </section>
    </main><Footer seasonTwo/>
  </div>;
}
