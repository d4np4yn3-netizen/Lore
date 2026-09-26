import { permanentRedirect } from 'next/navigation';

// Preserve the QR destination printed on 002 when its page moves or a custom domain is added.
export default function Crypto002() {
  permanentRedirect('/cards/cypherpunk-manifesto');
}
