import { redirect } from 'next/navigation';

// Stable printed-card URL. Use a temporary redirect until the card's own
// story and Easter-egg page is approved, so scans can follow that page later.
export default function Crypto002() {
  redirect('https://nakamotoinstitute.org/library/cypherpunk-manifesto/');
}
