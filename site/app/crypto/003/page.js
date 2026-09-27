import { permanentRedirect } from 'next/navigation';

// Preserve the QR destination printed on 003 when its page moves or a custom domain is added.
export default function Crypto003() {
  permanentRedirect('/cards/hashcash');
}
