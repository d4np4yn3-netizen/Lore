import chapter001 from './content/001.json';

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
];

export const getCard = slug => cards.find(card => card.slug === slug);
