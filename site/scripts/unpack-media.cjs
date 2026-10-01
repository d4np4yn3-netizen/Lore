// Materialize the individually addressable, hash-verified web-only display files.
const fs=require('node:fs');const path=require('node:path');const crypto=require('node:crypto');
const root=path.join(__dirname,'..'), index=require('../media/index.json'),packs=new Map();
for(const asset of index.assets){
 if(!/^(archive|closeups)\/[a-zA-Z0-9.-]+\.webp$/.test(asset.path))throw new Error('Invalid media path');
 if(!packs.has(asset.pack))packs.set(asset.pack,fs.readFileSync(path.join(root,'media',asset.pack)));
 const bytes=packs.get(asset.pack).subarray(asset.offset,asset.offset+asset.length);
 if(crypto.createHash('sha256').update(bytes).digest('hex')!==asset.sha256)throw new Error('Media integrity mismatch: '+asset.path);
 const dest=path.join(root,'public',asset.path);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,bytes);
}
console.log(`Verified and prepared ${index.assets.length} individual website images`);
