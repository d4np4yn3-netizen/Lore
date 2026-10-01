import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
export function Header({ detail = false }) {
  return <header className="site-header"><Link className="brand" href="/" aria-label="LORE home"><Image src="/brand/logo.svg" width={91} height={72} alt="LORE" priority /></Link><span className="header-edition">CRYPTO <span>/</span> SEASON ONE</span><nav className="header-nav" aria-label="Main navigation"><Link href="/#archive">The archive</Link><Link className="about-link" href="/#about">About LORE</Link>{detail ? <Link className="header-action" href="/#archive"><Arrow direction="left"/> Back to timeline</Link> : <a className="header-action" href="#archive">Explore <Arrow direction="down" /></a>}</nav></header>;
}
export function Footer(){return <footer className="site-footer"><div><Image src="/brand/logo.svg" width={135} height={106} alt="LORE"/><p>COLLECT THE INTERNET.</p></div><div className="footer-right"><a href="#top">Back to top <Arrow direction="left"/></a><span>© 2026 LORE · CRYPTO SEASON ONE</span><small>Illustrated history. Original collectible artwork.</small></div></footer>}
