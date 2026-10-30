import Link from 'next/link';
import { Arrow } from './Icons';
import styles from '../season-two/season-two.module.css';

export default function SeasonTwoTeaser() {
  return <section className={styles.teaser} aria-labelledby="season-two-teaser-title">
    <div><span className="label gold">LOOKING AHEAD / SEASON TWO</span><h2 id="season-two-teaser-title">50 new cards.<br/>Help choose the moments.</h2></div>
    <div><p>The next crypto season starts with the moments you remember. Help shape a community-inspired collection, one story at a time.</p><Link className="text-link" href="/season-two">Explore Season Two <Arrow/></Link></div>
  </section>;
}
