import Image from 'next/image';
import { Arrow } from './Icons';

// Deliberately closed until a real provider, privacy notice and consent flow are approved.
// No submission handler, email state, storage, analytics event or collection endpoint.
export default function ComingSoon() {
  return <section className="coming-soon" id="coming-soon" aria-labelledby="launch-heading">
    <div className="launch-copy">
      <span className="label gold"><span className="status-dot"/> COMING SOON / CRYPTO SEASON ONE</span>
      <h2 id="launch-heading">The collection.<br/><em>The next chapter.</em></h2>
      <p>Collectible cards. A companion book. A puzzle taking shape around the history.</p>
      <p className="launch-detail">Explore the archive today. Launch details and the first look at the puzzle are still to come.</p>
      <a className="text-link" href="#archive">Discover the moments <Arrow/></a>
      <div className="launch-signature"><Image src="/brand/histrove-crown.svg" width={29} height={29} alt=""/><span>History Worth Holding</span></div>
    </div>
    <div className="launch-list" aria-labelledby="launch-list-heading">
      <span className="label">THE LAUNCH LIST</span>
      <h3 id="launch-list-heading">Be first to hear.</h3>
      <p id="launch-status" className="launch-status"><span className="status-dot"/> Email registration opens soon</p>
      <div className="launch-form-preview" aria-describedby="launch-status launch-privacy">
        <label htmlFor="launch-email">Email address</label>
        <input id="launch-email" type="email" placeholder="you@example.com" autoComplete="off" disabled aria-describedby="launch-status launch-privacy"/>
        <label className="launch-consent"><input type="checkbox" disabled/><span>I’d like HISTROVE launch announcements and puzzle launch updates by email. I can unsubscribe at any time.</span></label>
        <button className="gold-button" type="button" disabled aria-describedby="launch-status">Join the launch list <Arrow/></button>
      </div>
      <p id="launch-privacy" className="launch-privacy">Registration is not open yet. This page does not collect or store email addresses. The privacy notice and email confirmation step will be available before signups open.</p>
    </div>
  </section>;
}
