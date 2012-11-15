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
from chatbot.contrib import *

bot = Bot(
	nickname = 'bestbot',
	hostname = 'chat.freenode.net',
	port = 6665,
	server_password = 'my_bots_password',
	channels = ('#freenode', '#python'),
	features = (
		PyPIFeature(),
		WikipediaFeature(),
		DictionaryFeature(),
		DiceFeature(),
		ChoiceFeature(),
		SlapbackFeature(),
	)
)

bot.run()
```

Then run the script:

```bash
python simple_bot.py
```

The Flexible `Match` Feature
----------------------------

**Chatbot** comes with a built in `Match` feature, which is both simple and
powerful. You can build an entire bot from `Match` features alone. Here is an
example of a simple bot that will slap people on command.

```python
from chatbot.bots import Bot
from chatbot.contrib.simple import Match
from chatbot.chat import ChatResponse

SLAP_OPTIONS = (
	ChatResponse('slaps \g<target> around a bit with a baseball bat', action=True),
	ChatResponse('slaps \g<target> around a bit with a large trout', action=True),
	ChatResponse('slaps \g<target> around a bit with a piano', action=True),
	ChatResponse('slaps \g<target> around a bit with a french fry', action=True),
)

bot = Bot(
	nickname = 'bestbot',
	hostname = 'chat.freenode.net',
	port = 6665,
	server_password = 'my_bots_password',
	channels = ('#freenode', '#python'),
	features = (
		Match(r'slap (?P<target>[^\s]+) (?P<object>.+)', ChatResponse('slaps \g<target> around a bit \g<object>', action=True), addressing_required=True, allow_continuation=False),
		Match(r'slap (?P<target>.+)', SLAP_OPTIONS, addressing_required=True, allow_continuation=False),
	)
)

bot.run()
```

In this case, the bot handles two possible matches. The first pattern matches sentences such as `bestbot: slap melinath with a frying pan` by responding with an action, `slaps melinath around a bit with a frying pan`. The second pattern matches commands to slap that do not specify the method of slapping (e.g., `slap melinath`), by choosing an option randomly from `SLAP_OPTIONS` (e.g., `slaps melinath around a bit with a french fry`).

Using a Database
----------------

Some of Chatbot's features require a database. To use a database, pass in a database keyword argument when instantiating your bot:

```python
bot = Bot(
	nickname = 'bestbot',
	hostname = 'chat.freenode.net',
	port = 6665,
	database = 'sqlite:///:memory:',
	# ...
)
```