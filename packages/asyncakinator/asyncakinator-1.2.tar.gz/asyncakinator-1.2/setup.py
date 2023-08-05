# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncakinator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'asyncakinator',
    'version': '1.2',
    'description': 'An async API wrapper for Akinator, written in Python.',
    'long_description': 'asyncakinator\n=============\n\n\n.. image:: https://discord.com/api/guilds/751490725555994716/embed.png\n   :target: https://discord.gg/muTVFgDvKf\n   :alt: Support Server Invite\n\nAn async API wrapper for the online game, Akinator, written in Python.\n\n`Akinator <https://en.akinator.com/>`_ is a web-based game which tries to determine what character you are thinking of by asking a series of questions.\n\nInstalling\n----------\n\nTo install, just run the following command::\n\n  python3 -m pip install -U asyncakinator\n\nRequirements\n~~~~~~~~~~~~\n- Python ≥3.9\n\n- ``requests``\n\n- ``aiohttp``\n\n\nUsually, ``pip`` will handle these for you.\n\nQuick Examples\n--------------\n\nHere\'s a quick little example of the library being used to make a simple, text-based Akinator game:\n\n.. code-block:: python\n\n    import akinator\n    import asyncio\n\n    aki = akinator.Akinator(\n        language=akinator.Language.ENGLISH,\n        theme=akinator.Theme.ANIMALS,\n    )\n\n    async def main():\n        question = await aki.start()\n\n        while aki.progression <= 80:\n            a = input(f"{question}\\n\\t")\n            if a == "b":\n                try:\n                    question = await aki.back()\n                except akinator.CantGoBackAnyFurther:\n                    continue\n            else:\n                try:\n                    question = await aki.answer(akinator.Answer.from_str(a))\n                except akinator.InvalidAnswer:\n                    print("Invalid answer. Please try again.\\n")\n                    continue\n        await aki.win()\n\n        correct = input(\n            f"You are thinking of {aki.first_guess.name} ({aki.first_guess.description}). "\n            f"Am I correct?\\n{aki.first_guess.absolute_picture_path}\\n\\t"\n        )\n        if akinator.Answer.from_str(correct) == akinator.Answer.YES:\n            print("Nice.")\n        else:\n            print("Maybe next time.")\n        await aki.close()\n\n    asyncio.run(main())\n\nDocumentation\n-------------\nDocumention can be found `here. <https://asyncakinator.readthedocs.io/en/latest/>`_',
    'author': 'avizum',
    'author_email': 'juliusrt@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/avizum/akinator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
