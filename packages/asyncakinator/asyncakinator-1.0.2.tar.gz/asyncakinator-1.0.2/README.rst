========
akinator
========

**An async API wrapper for the online game, Akinator, written in Python**

.. image:: https://img.shields.io/badge/python-%E2%89%A53.5.3-yellow.svg
    :target: https://www.python.org/downloads/

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Copyright © 2019 NinjaSnail1080

Copyright © 2022 avizum

Licensed under the MIT License (see ``LICENSE.txt`` for details).

`Akinator.com <https://www.akinator.com>`_ is an online game where you think of a character, real or fiction, and by asking you questions the site will try to guess who you're thinking of. This library allows for easy access to the Akinator API and makes writing programs that use it much simpler.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

**********
Installing
**********

To install, just run the following command::

  python3 -m pip install -U asyncakinator

Requirements
============

- Python ≥3.9

- ``requests``

- ``aiohttp``


Usually, ``pip`` will handle these for you.

**************
Quick Examples
**************

Here's a quick little example of the library being used to make a simple, text-based Akinator game:

.. code-block:: python

    import akinator
    import asyncio

    aki = akinator.AsyncAkinator()

    async def main():
        q = await aki.start()

        while aki.progression <= 80:
            a = input(q + "\n\t")
            if a == "b":
                try:
                    q = await aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = await aki.answer(a)
        await aki.win()

        correct = input(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?\n{aki.first_guess['absolute_picture_path']}\n\t")
        if correct.lower() == "yes" or correct.lower() == "y":
            print("Yay\n")
        else:
            print("Oof\n")
        await aki.close()

    await asyncio.run(main())