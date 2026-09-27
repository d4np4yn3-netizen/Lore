import chapter001 from './content/001.json';
import chapter002 from './content/002.json';
import chapter003 from './content/003.json';

export const cards = [
  {
    slug: 'blind-signatures',
    title: 'BLIND SIGNATURES',
    rarity: 'LEGENDARY',
    date: '1982',
    subject: 'DAVID CHAUM',
    phrase: 'UNTRACEABLE PAYMENTS.',
    image: 'cards/crypto/season-01/blind-signatures-master-01/LORE-Blind-Signatures-Legendary-v1-Print-v2.png',
    ...chapter001,
    source: 'https://chaum.com/wp-content/uploads/2022/01/Chaum-blind-signatures.pdf',
    number: '001/100',
  },
  {
    slug: 'cypherpunk-manifesto',
    title: 'CYPHERPUNK MANIFESTO',
    rarity: 'EPIC',
    date: '9 MAR 1993',
    subject: 'ERIC HUGHES',
    phrase: 'CYPHERPUNKS WRITE CODE.',
    image: 'cards/crypto/season-01/the-cypherpunk-manifesto-master-01/LORE-Cypherpunk-Manifesto-Epic-002-Print-v2.png',
    ...chapter002,
    source: 'https://nakamotoinstitute.org/library/cypherpunk-manifesto/',
    number: '002/100',
  },
  {
    slug: 'hashcash',
    title: 'HASHCASH POSTAGE',
    rarity: 'RARE',
    date: '28 MAR 1997',
    subject: 'ADAM BACK',
    phrase: 'VERIFIED INSTANTLY.',
    image: 'cards/crypto/season-01/hashcash-master-01/LORE-Hashcash-Rare-003-Print-v1.png',
    ...chapter003,
    source: 'https://www.hashcash.org/papers/announce.txt',
    number: '003/100',
  },
];

export const getCard = slug => cards.find(card => card.slug === slug);
