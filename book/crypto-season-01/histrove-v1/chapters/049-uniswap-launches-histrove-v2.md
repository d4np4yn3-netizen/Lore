# 049 - Uniswap Launches

02 NOV 2018 / ETHEREUM / LEGENDARY

LIQUIDITY, PAIRED.

## The story

On 2 November 2018, the final day of Devcon 4 in Prague, Hayden Adams announced Uniswap and deployed its exchange contracts to Ethereum mainnet. After more than a year of development, a small application was ready to let people swap assets through on-chain code.

Uniswap V1 paired each supported ERC20 token with ETH. An exchange contract held reserves of both assets, and traders swapped against those reserves rather than a conventional order book. Token-to-token trades could pass through ETH as an intermediate step. Anyone could create an exchange for a token through the factory contract.

Prices followed a constant-product market-making rule, commonly written x*y=k. Adding one asset in a swap removed some of the other, changing the reserve ratio and the next price. Larger trades moved that ratio further. The equation is a simplified swap relationship: trading fees increase the reserve product, and liquidity deposits or withdrawals also change it.

Liquidity providers supplied both assets, normally in the pool's current ratio, and received pool tokens recording their share. A 0.3% trading fee accumulated in the reserves for those providers. The two labelled baskets represent the paired reserves of one illustrated pool, not two independent markets.

HISTROVE imagines a unicorn exchanging tokens while balancing on a wooden beam. The purple ETH coin and turquoise ERC20 coin stand for existing assets being swapped, not coins magically created by the exchange. The V1 plaque identifies the original protocol. UNI, the later governance token, arrived in September 2020; V1's liquidity-share tokens were a different thing.

## Details in the artwork

1. **THE PAIRED BASKETS** ETH and ERC20 label the two baskets. They represent one V1 exchange's reserves: Ether paired with a particular ERC20 token. The generic token symbol does not identify UNI or a specific traded asset.
2. **THE TOKEN EXCHANGE** The unicorn holds one coin above each reserve. This compresses a swap into a gesture: one asset enters the pool and some of the other leaves. The traded coins are existing assets; pool-share tokens issued to liquidity providers are separate.
3. **THE BEAM AND FULCRUM** A wooden beam rests on a triangular stone support. Balancing evokes reserves whose ratio changes through trading. It is not a fixed 1:1 exchange rate, a promise of equal quantities or a literal diagram of the constant-product formula.
4. **THE V1 PLAQUE** V1 identifies the original Uniswap protocol, launched in 2018. Its exchanges paired tokens with ETH, and token-to-token swaps could route through ETH. The plaque distinguishes this chapter from later versions.

## Source and art note

Sources: [Hayden Adams: A Short History of Uniswap](https://blog.uniswap.org/uniswap-history); [Uniswap V1: original overview](https://github.com/Uniswap/v1-docs/blob/3d71d5d7e0ffefd08596de29b7630fe9744721d2/README.md); [Uniswap V1: pool liquidity](https://github.com/Uniswap/v1-docs/blob/3d71d5d7e0ffefd08596de29b7630fe9744721d2/frontend-integration/pool.md); [Uniswap V1: exchange contract](https://github.com/Uniswap/v1-contracts/blob/master/contracts/uniswap_exchange.vy); [Uniswap Labs: Introducing UNI](https://blog.uniswap.org/uni). The unicorn, seesaw and harbour are fictional allegory, not a portrait of Hayden Adams, an official logo or a historical scene. The balancing act is not a technical pricing diagram. LIQUIDITY, PAIRED. is editorial wording, not a historical quotation.
