import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
export function Header({ shop = false }) {
  return <header className="site-header"><Link className="brand" href="/" aria-label="HISTROVE home"><Image src="/brand/histrove-logo.png" width={144} height={72} alt="HISTROVE" priority /></Link><span className="header-edition">CRYPTO <span>/</span> SEASON ONE</span><nav className="header-nav" aria-label="Main navigation"><Link href="/#archive">The archive</Link><Link className="about-link" href="/#about">About HISTROVE</Link><Link className="header-action shop-action" href="/shop" aria-current={shop ? 'page' : undefined}>Shop <Arrow/></Link></nav></header>;
}
export function Footer(){return <footer className="site-footer"><div><Image src="/brand/histrove-logo.png" width={200} height={100} alt="HISTROVE"/><p>History Worth Holding</p></div><div className="footer-right"><a href="#top">Back to top <Arrow direction="left"/></a><span>© 2026 HISTROVE · CRYPTO SEASON ONE</span><small>Illustrated history. Original collectible artwork.</small></div></footer>}
