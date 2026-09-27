import { permanentRedirect } from 'next/navigation';

// Preserve the stable destination printed on the approved 004 card.
export default function Crypto004() {
  permanentRedirect('/cards/rpow');
}
