import { Arrow } from './Icons';

// Closed preview only: no submit handler, storage or collection endpoint.
export default function ComingSoon() {
  return <section className="coming-soon" id="coming-soon" aria-labelledby="launch-heading">
    <div className="launch-copy">
      <span className="label gold"><span className="status-dot"/> THE NEXT CHAPTER</span>
      <h2 id="launch-heading">More history to come.</h2>
      <p>The collection and companion book are taking shape. A puzzle around the history is still to come.</p>
      <a className="text-link" href="#archive">Explore the published stories <Arrow/></a>
    </div>
    <aside className="launch-list" aria-labelledby="launch-list-heading">
      <span className="label">LAUNCH UPDATES</span>
      <h3 id="launch-list-heading">Email registration opens soon</h3>
      <p id="launch-status" className="launch-status">Signups are not open yet.</p>
      <details className="launch-preview-details"><summary>View the signup preview</summary>
        <div className="launch-form-preview" aria-describedby="launch-status launch-privacy">
          <label htmlFor="launch-email">Email address</label>
          <input id="launch-email" type="email" placeholder="you@example.com" autoComplete="off" disabled aria-describedby="launch-status launch-privacy"/>
          <label className="launch-consent"><input type="checkbox" disabled/><span>I’d like HISTROVE launch announcements and puzzle launch updates by email. I can unsubscribe at any time.</span></label>
          <button className="gold-button" type="button" disabled aria-describedby="launch-status">Join the launch list <Arrow/></button>
        </div>
      </details>
      <p id="launch-privacy" className="launch-privacy">This page does not collect or store email addresses. A privacy notice and email confirmation step will be available before signups open.</p>
    </aside>
  </section>;
}
