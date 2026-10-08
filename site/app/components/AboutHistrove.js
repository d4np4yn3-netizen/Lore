import Link from 'next/link';
import { Arrow } from './Icons';

export default function AboutHistrove({ publishedCount }) {
  return <section className="about-histrove" id="about" aria-labelledby="about-heading">
    <div className="about-intro">
      <span className="label gold">ABOUT HISTROVE</span>
      <h2 id="about-heading">Real moments.<br/><em>Illustrated history.</em></h2>
      <p>HISTROVE brings crypto history into a physical card collection, a companion book and an online archive.</p>
      <p>Crypto Season One is a 100-card collection in the making. The first {publishedCount} moments are available to explore here, from the ideas before Bitcoin to the communities and turning points that followed.</p>
      <Link className="text-link" href="/shop">See the collection taking shape <Arrow/></Link>
    </div>
    <div className="editorial-principles">
      <span className="label gold">HOW TO READ THE ARCHIVE</span>
      <article><span>01</span><div><h3>The history</h3><p>Every story includes a source note. Follow its references for the historical record behind the moment.</p></div></article>
      <article><span>02</span><div><h3>The interpretation</h3><p>The illustrations use imagined scenes, visual metaphors and callbacks. Source notes distinguish that interpretation from documented events.</p></div></article>
      <article><span>03</span><div><h3>The details</h3><p>Explore the artwork, discover the meaning of its hidden details, then read the companion book pages alongside the story.</p></div></article>
      <Link className="text-link" href="/cards/the-whitepaper">Read a story and its sources <Arrow/></Link>
    </div>
  </section>;
}
