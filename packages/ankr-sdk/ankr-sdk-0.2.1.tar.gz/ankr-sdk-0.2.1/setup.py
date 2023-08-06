# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ankr']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0',
 'pyhumps>=3.7.2,<4.0.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'web3>=5.29.2,<6.0.0']

setup_kwargs = {
    'name': 'ankr-sdk',
    'version': '0.2.1',
    'description': "Compact Python library for interacting with Ankr's Advanced APIs.",
    'long_description': '# ⚓️ Ankr Python SDK\n\nCompact Python library for interacting with Ankr\'s [Advanced APIs](https://www.ankr.com/advanced-api/).\n\n## Get started in 2 minutes\n\n#### 1. Install the package from PyPi\n\n```bash\npip install ankr-sdk\n```\n\n#### 2. Initialize the SDK\n\n```python3\nfrom ankr import AnkrWeb3\n\nankr_w3 = AnkrWeb3()\n\n# Or, if you have an Ankr Protocol premium plan\nankr_w3 = AnkrWeb3("YOUR-TOKEN")\n```\n\n#### 3. Use the sdk and call one of the supported methods\n\n#### Node\'s API\n```python3\neth_block = ankr_w3.eth.get_block("latest")\nbsc_block = ankr_w3.bsc.get_block("latest")\npolygon_block = ankr_w3.polygon.get_block("latest")\n```\n\n#### Ankr NFT API \n\n```python3\nfrom ankr.types import Blockchain\n\nnfts = ankr_w3.nft.get_nfts(\n    blockchain=[Blockchain.ETH, Blockchain.BSC],\n    wallet_address="0x0E11A192d574b342C51be9e306694C41547185DD",\n    filter=[\n        {"0x700b4b9f39bb1faf5d0d16a20488f2733550bff4": []},\n        {"0xd8682bfa6918b0174f287b888e765b9a1b4dc9c3": ["8937"]},\n    ],\n)\n```\n\n#### Ankr Token API\n```python3\nassets = ankr_w3.token.get_account_balance(\n    wallet_address="0x77A859A53D4de24bBC0CC80dD93Fbe391Df45527"\n)\n```\n\n#### Ankr Query API\n```python3\nlogs = ankr_w3.query.get_logs(\n    blockchain="eth",\n    from_block="0xdaf6b1",\n    to_block=14350010,\n    address=["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"],\n    topics=[\n        [],\n        ["0x000000000000000000000000def1c0ded9bec7f1a1670819833240f027b25eff"],\n    ],\n    decode_logs=True,\n)\n```\n\n## Ankr Advanced APIs supported chains\n\n`ankr-sdk` supports the following chains at this time:\n\n- ETH: `"eth"`\n- BSC: `"bsc"`\n- Polygon: `"polygon"`\n- Fantom: `"fantom"`\n- Arbitrum: `"arbitrum"`\n- Avalanche: `"avalanche"`\n- Syscoin NEVM: `"syscoin"`\n\n## Available methods\n\n`ankr-sdk` supports the following methods:\n\n- [`nft.get_nfts`](#get_nfts)\n- [`nft.get_nft_metadata`](#get_nft_metadata)\n- `nft.get_nft_holders`\n- [`token.get_token_holders`](#get_token_holders)\n- [`token.get_token_holders_count_history`](#get_token_holders_count_history)\n- [`token.get_token_holders_count`](#get_token_holders_count)\n- `token.get_token_price`\n- [`token.get_account_balance`](#get_account_balance)\n- [`query.get_logs`](#get_logs)\n- [`query.get_blocks`](#get_blocks)\n- [`query.get_transaction`](#get_transaction)\n\n#### `get_nfts`\n\nGet data about all the NFTs (collectibles) owned by a wallet.\n\n````python3\nnfts = ankr_w3.nft.get_nfts(\n    blockchain="eth",\n    wallet_address="0x0E11A192d574b342C51be9e306694C41547185DD",\n    filter=[\n        {"0x700b4b9f39bb1faf5d0d16a20488f2733550bff4": []},\n        {"0xd8682bfa6918b0174f287b888e765b9a1b4dc9c3": ["8937"]},\n    ],\n)\n````\n\n#### `get_nft_metadata`\n\nGet metadata of NFT.\n\n````python3\nnfts = ankr_w3.nft.get_nft_metadata(\n    blockchain="eth",\n    contract_address="0x4100670ee2f8aef6c47a4ed13c7f246e621228ec",\n    token_id="4",\n)\n````\n\n#### `get_token_holders`\n\nGet holders of a token.\n\n````python3\nholders = ankr_w3.token.get_token_holders(\n    blockchain="bsc",\n    contract_address="0xf307910A4c7bbc79691fD374889b36d8531B08e3",\n    limit=10,\n)\n````\n\n#### `get_token_holders_count_history`\n\nGet token holders count daily history.\n\n````python3\ndaily_holders_history = ankr_w3.token.get_token_holders_count_history(\n    blockchain="bsc",\n    contract_address="0xf307910A4c7bbc79691fD374889b36d8531B08e3",\n    limit=10,  # last 10 days history\n)\n````\n\n#### `get_token_holders_count`\n\nGet token holders count at the latest block.\n\n````python3\nholders_count = ankr_w3.token.get_token_holders_count(\n    blockchain="bsc",\n    contract_address="0xf307910A4c7bbc79691fD374889b36d8531B08e3",\n)\n````\n\n#### `get_account_balance`\n\nGet account assets.\n\n````python3\nassets = ankr_w3.token.get_account_balance(\n    wallet_address="0x77A859A53D4de24bBC0CC80dD93Fbe391Df45527",\n    blockchain=["eth", "bsc"],\n)\n````\n\n#### `get_logs`\n\nGet logs matching the filter.\n\n```python3\nlogs = ankr_w3.query.get_logs(\n    blockchain="eth",\n    from_block="0xdaf6b1",\n    to_block=14350010,\n    address=["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"],\n    topics=[\n        [],\n        ["0x000000000000000000000000def1c0ded9bec7f1a1670819833240f027b25eff"],\n    ],\n    decode_logs=True,\n)\n```\n\n#### `get_blocks`\n\nQuery data about blocks within a specified range.\n\n```python3\nblocks = ankr_w3.query.get_blocks(\n    blockchain="eth",\n    from_block=14500001,\n    to_block=14500001,\n    desc_order=True,\n    include_logs=True,\n    include_txs=True,\n    decode_logs=True,\n)\n```\n\n#### `get_transaction`\n\nGet Transaction by hash.\n\n````python3\ntx = ankr_w3.query.get_transaction(\n    transaction_hash="0x82c13aaac6f0b6471afb94a3a64ae89d45baa3608ad397621dbb0d847f51196f",\n    include_logs=True,\n    decode_logs=True,\n    decode_tx_data=True,\n)\n````\n\n\n### About API keys\n\nFor now, Ankr is offering _free_ access to these APIs with no request limits i.e. you don\'t need an API key at this\ntime.\n\nLater on, these APIs will become a part of Ankr Protocol\'s [Premium Plan](https://www.ankr.com/protocol/plan/).\n',
    'author': 'Roman Fasakhov',
    'author_email': 'romanfasakhov@ankr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ankr.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
