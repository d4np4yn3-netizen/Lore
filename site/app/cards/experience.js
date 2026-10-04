import { cards } from './data';
import media from './media.json';
export const ASSET_ORIGIN = 'https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/ac8d3634de5bf6e2e40a8692e751b2f0df0d281e/';
export const archiveCards = cards.map(card => ({ ...card, id: card.number.split('/')[0], year: Number(card.date.match(/\d{4}/)[0]), media: media[card.slug] }));
export const years = [...new Set(archiveCards.map(card => card.year))];
export const yearNotes = {
  1982: ['The idea before the coin.', 'Privacy becomes a question of mathematics.'],
  1993: ['A movement finds its voice.', 'Cypherpunks put their principles into code.'],
  1997: ['The cost of a computation.', 'Proof of work takes an early, practical form.'],
  2004: ['One step closer.', 'Reusable proof of work connects the dots.'],
  2008: ['Nine pages. A new possibility.', 'The Bitcoin whitepaper arrives.'],
  2009: ['The network comes to life.', 'A first block. A first transfer.'],
  2010: ['An experiment enters the world.', 'Pizza, free coins, a bug and a mining pool.'],
  2011: ['Beyond the screen.', 'Donations, physical coins and digital silver.'],
  2012: ['The rules keep their promise.', 'The block reward is cut in half.'],
  2013: ['Crypto finds its culture.', 'New ideas, everyday uses and unforgettable memes.'],
  2014: ['A much wider world.', 'Community, privacy, art and hard lessons.'],
  2015: ['A network and its rules.', 'New York regulates virtual-currency businesses as Ethereum’s Frontier goes live.'],
  2016: ['A crisis and a choice.', 'The DAO exploit and Ethereum split test the security of smart contracts and the choices of a young community.'],
};
export const titleCase = title => title.toLowerCase().replace(/(^|[\s—])\S/g, c => c.toUpperCase()).replace('Mt. Gox','Mt. Gox').replace('Rpow','RPOW').replace('Hodl','HODL').replace('Wikileaks','WikiLeaks').replace('Bitlicense','BitLicense').replace('Dao','DAO');


export const chapters = [
  {number:'01',start:1982,range:'1982 — 2004',title:'Before Bitcoin.',copy:'From private signatures to reusable proof of work, the ideas that made a different kind of money possible.'},
  {number:'02',start:2008,range:'2008 — 2012',title:'An idea becomes a network.',copy:'A whitepaper becomes working code. People send it, spend it, mine it and discover what it can do.'},
  {number:'03',start:2013,range:'2013 — 2016',title:'The culture takes shape.',copy:'New communities and possibilities arrive, alongside failures and hard lessons. Crypto becomes much more than a technical experiment.'},
];
