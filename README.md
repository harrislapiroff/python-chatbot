Python Chatbot
==============

A simple, extensible bot for your IRC channels.

Installation
------------

With Pip:

```bash
pip install git+https://github.com/lapilofu/python-chatbot.git@master#egg=chatbot
```

Usage
-----

To run a bot, you must write a short python script. For example `simple_bot.py`:

```python
from chatbot.bots import Bot

bot = Bot({
	'nickname': 'bestbot',
	'hostname': 'chat.freenode.net',
	'port': 6665,
	'server_password': 'my_bots_password',
	'channels': ('#freenode', '#python'),
	'features': ('chatbot.contrib.pypi.PyPIFeature',)
})

bot.run()
```

Then run the script:

```bash
python simple_bot.py
```