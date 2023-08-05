# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['babbagecoin',
 'babbagecoin.client',
 'babbagecoin.common',
 'babbagecoin.master',
 'babbagecoin.miner']

package_data = \
{'': ['*'], 'babbagecoin': ['webclient/*', 'webclient/assets/*']}

install_requires = \
['Flask>=2.0.3,<3.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0',
 'sentry-sdk[flask]>=1.5.8,<2.0.0']

setup_kwargs = {
    'name': 'babbagecoin',
    'version': '0.5.0',
    'description': 'Second edition of Project Babbage, create a blockchain from scratch.',
    'long_description': "# Babbagecoin\n\n### An understandable proof of work blockchain.\n\n**Visit our [web page](https://projectbabbage.github.io/babbagecoin/) for a nice general overview of the project !**\n\n## Quickly run a node !\n\n\n```bash\npip install --user babbagecoin\n```\n\n```bash\npython -m babbagecoin master\n# then in another terminal:\npython -m babbagecoin miner\n```\n\n# For development\n\n## Requirements\n\nInstall `docker` and `docker-compose`, `python3` (>=3.9) and `poetry`.\n\nRun `poetry install` then `poetry shell`\n\n## Launch\n\nRun the node (master + miner):\n\n`make`\n\nStop the node properly:\n\n`make stop` --> to stop all containers if you didn't stopped them properly (if you did two Ctrl+C in a row)\n\nOr you can run separately the master or miner:\n\n`make (master | miner)`\n\nThere are also VSCode actions for debugging each one of them (even the tests, run in terminal with `make test`)\n\n## Interact with the blockchain\n\n!! Important\n\nConfigure your blockchain by creating a `.env` file on the same model as what's in `.env.example`.\n\nThe wallet will generate a private key for you, save it to private.key.<CURRENT_USER>, and reuse it afterward. A public key is derived from this private key. The hash of the public key is your address, for example e93417c7 (the first 8 characters).\nThe wallet is managing only one private key at the time.\n\n### Transactions\n\nUse the `bbc.sh` script (`chmod +x` it first):\n\n`./bbc.sh tx MARTIAL 10 0.3` --> sending 10BBC with 0.5BBC fees to MARTIAL\n\n_`make tx` is a shortcut for the above command_\n\n### Balance\n\n`./bbc.sh balance` to get your wallet balance\n\n_`make balance` is a shortcut for the above command_\n\n",
    'author': 'Quentin Garchery',
    'author_email': 'garchery.quentin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ProjectBabbage/babbagecoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
