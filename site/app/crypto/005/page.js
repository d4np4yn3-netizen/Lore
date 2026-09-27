import { permanentRedirect } from 'next/navigation';

// Preserve the stable destination printed on the approved 005 card.
export default function Crypto005() {
  permanentRedirect('/cards/the-whitepaper');
}
