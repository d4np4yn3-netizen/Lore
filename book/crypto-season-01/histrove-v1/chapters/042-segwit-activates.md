# 042 - SegWit Activates

24 AUG 2017 / UNCOMMON

BITCOIN UPGRADED.

## The story

On 24 August 2017, Segregated Witness, or SegWit, activated on Bitcoin at block 481,824. The soft-fork upgrade changed how transactions carry validation data and how block capacity is measured, while continuing Bitcoin's existing chain.

SegWit moved signatures and related validation data into a separate witness structure. That witness remains part of Bitcoin's blockchain and is cryptographically committed through the block's coinbase transaction. Separating it from the data used to calculate a transaction's ID did not mean moving it off-chain.

For transactions spending only SegWit inputs, the upgrade fixed nonintentional transaction-ID malleability: changing a signature could no longer change the txid. This made it easier to build reliable chains of unconfirmed transactions, an important foundation for payment-channel systems such as Lightning.

SegWit also introduced a limit of 4,000,000 weight units per block. Base data counts four units per byte; witness data counts one. The extra usable capacity depends on the transaction mix. It is not a promise of four megabytes of ordinary transaction data or four times as many payments.

The two bulls show Bitcoin before and after the upgrade. The smaller bull carries bundled paperwork; the larger one separates gold transaction tiles from blue witness channels. They represent one network evolving, not two rival coins. The lightning hints at technology built on that foundation later, and the stronger form makes no promise about price.

## Details in the artwork

1. **THE 481,824 PLAQUE** The stone plaque marks the Bitcoin block where SegWit became active on 24 August 2017. It anchors the transformation to a specific point in the chain.
2. **THE BIP 141 PLATE** The larger bull's armour names the Bitcoin Improvement Proposal defining SegWit's consensus rules, including its witness commitment and block-weight limit. It is a technical reference, not a manufacturer's badge.
3. **GOLD AND BLUE CHANNELS** Gold transaction tiles and blue witness channels make the data separation visible. Both belong to the same Bitcoin transaction and blockchain. The colours are an artistic key, not a literal protocol diagram.
4. **THE LIGHTNING FORESHADOW** The bolt and storm point toward Lightning payment channels. They foreshadow later development; Lightning Labs announced its first lnd mainnet beta in March 2018, after SegWit's activation.

## Source and art note

Sources: [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki); [Bitcoin Core: mainnet activation height](https://github.com/bitcoin/bitcoin/blob/master/src/kernel/chainparams.cpp); [Block 481,824 record](https://blockstream.info/block/0000000000000000001c8018d9cb3b742ef25114f27563e3fc4a1902167f9893); [Bitcoin Core: SegWit benefits](https://bitcoincore.org/en/2016/01/26/segwit-benefits/); [Lightning Labs: lnd mainnet beta](https://lightning.engineering/posts/2018-03-15-lnd-beta/). The bulls, armour, channels and storm are visual metaphors. BITCOIN UPGRADED. is editorial wording, not a quotation or a price prediction. No affiliation or endorsement is implied.
