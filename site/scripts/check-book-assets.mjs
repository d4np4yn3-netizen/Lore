import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const site=path.resolve(import.meta.dirname,'..'),repo=path.resolve(site,'..');const root='book/crypto-season-01/histrove-v1/';
const read=p=>JSON.parse(fs.readFileSync(path.join(repo,p),'utf8'));const manifest=read(root+'manifest.json'),qa=read(root+'qa.json'),media=read('site/app/cards/media.json');
const hash=p=>createHash('sha256').update(fs.readFileSync(path.join(repo,p))).digest('hex');
assert.equal(manifest.books.length,46);assert.equal(qa.books.length,39);
for(const book of manifest.books){assert.equal(hash(book.newPdf),book.pdfSHA256);assert.equal(hash(book.chapter),book.chapterSHA256);assert.equal(media[book.slug].originalBook,book.newPdf);for(const page of book.pages){assert.equal(hash('site/public'+page.new),page.sha256);}}
for(const q of qa.books){assert.equal(q.pageCount,2);for(const key of ['originalArtworkStreamsIdentical','artPageRenderPixelIdentical','unchangedPixelsOutsideBrandTextRegions','wordChangesOnlyLOREtoHISTROVE','sourceUrisUnchanged','fontSizeAndLeadingUnchanged'])assert.equal(q[key],true,q.number+' '+key);assert.equal(q.outsideChangedPixels144dpi,0);assert.equal(q.remainingOldBrandTextCount,0);}
console.log('PASS: 46 current PDF/chapter hashes and 92 preview hashes; original 39 recorded brand-only PDF pixel, native-art, semantic-copy and source-URI QA verified');
