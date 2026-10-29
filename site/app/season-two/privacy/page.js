import Link from 'next/link';
import { Header, Footer } from '../../components/SiteChrome';
import styles from '../season-two.module.css';

export const metadata = {
  title: 'Suggestions privacy information — draft | HISTROVE',
  description: 'Review the proposed handling of HISTROVE Season Two suggestions. Public submissions remain closed.',
  robots: { index: false, follow: false },
};

export default function SuggestionsPrivacyPage() {
  return <div id="top"><a className="skip-link" href="#suggestions-privacy-main">Skip to suggestions privacy information</a><Header seasonTwo/>
    <main className={styles.page} id="suggestions-privacy-main"><article className={styles.privacyNotice}>
      <span className="label gold">SEASON TWO / PRIVACY REVIEW</span>
      <h1>Your ideas.<br/>Handled with care.</h1>
      <div className={styles.notice}><strong>Draft for review · Public suggestions remain closed.</strong><p>This describes the planned suggestion process. The final controller identification, lawful basis and Google service/transfer information still need review before public collection begins. It is not a final live privacy notice.</p></div>
      <h2>Who handles suggestions?</h2>
      <p>HISTROVE is an independently run history project. The project owner manages suggestions and decides how they are reviewed. For questions about a suggestion or personal information in it, contact <a href="mailto:hello@histrove.co.uk">hello@histrove.co.uk</a>.</p>
      <h2>What the form asks for</h2>
      <ul><li>The crypto moment.</li><li>Its date or approximate period.</li><li>Why it deserves a card.</li><li>A credible public source link.</li></ul>
      <p>Google Forms also records the submission time. The form does not ask for a name or collect an email address with the response. Please don’t include contact details, private keys, wallet details or other private personal information. Free-text answers and linked sources can still contain personal information, so this is not a promise of complete anonymity.</p>
      <h2>Why suggestions are reviewed</h2>
      <p>Suggestions help HISTROVE research crypto-history moments and curate the planned 50-card collection. They are reviewed privately, not posted automatically or put to a binding vote. Selected moments may inform the collection; submitting does not guarantee inclusion or a prize.</p>
      <p>A suggestion does not subscribe anyone to marketing emails. Email signup is a separate feature and remains closed.</p>
      <h2>Where responses are kept</h2>
      <p>Responses are stored in Google Forms and a linked Google Sheet. Direct access to both is restricted to the HISTROVE owner. Other respondents cannot view a response summary or the spreadsheet.</p>
      <p>Google operates these services and may process technical or account information under its service terms. Read <a href="https://policies.google.com/privacy" rel="noopener noreferrer">Google’s privacy information</a>. The applicable service terms and any international-transfer information will be checked before launch; this draft does not claim UK-only storage.</p>
      <h2>How long suggestions are kept</h2>
      <p>Unselected suggestions will be reviewed and deleted after 12 months, in both Google Forms and the linked Sheet. Selected ideas may be retained for the collection’s editorial and research purposes, not for unrelated marketing. This is an owner-managed retention process, not automatic deletion.</p>
      <h2>Lawful basis — still under review</h2>
      <p>Legitimate interests is proposed for the limited purpose of reviewing voluntarily submitted history ideas and curating the collection. It has not yet been adopted: the purpose, necessity and impact on people must be assessed before any public collection of personal information. No marketing consent is inferred from a suggestion.</p>
      <h2>Questions, requests and complaints</h2>
      <p>Contact <a href="mailto:hello@histrove.co.uk">hello@histrove.co.uk</a> to ask about personal information in a suggestion, request access, correction or deletion, or raise a concern. Where applicable, you may also request restriction of processing or object to its use. The final notice will explain the rights that apply to the chosen lawful basis.</p>
      <p>Because the form does not collect contact details, include the moment and approximate submission date so the response can be located. Do not send identity documents unless they are genuinely needed and specifically requested.</p>
      <p>You can also <a href="https://ico.org.uk/make-a-complaint/" rel="noopener noreferrer">raise a data-protection complaint with the UK Information Commissioner’s Office</a>.</p>
      <Link className={styles.returnLink} href="/season-two#suggestion-preview">Back to the Season Two preview</Link>
    </article></main><Footer seasonTwo/>
  </div>;
}
