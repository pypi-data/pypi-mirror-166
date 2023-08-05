asyncakinator
=============


.. image:: https://discord.com/api/guilds/751490725555994716/embed.png
   :target: https://discord.gg/muTVFgDvKf
   :alt: Support Server Invite

An async API wrapper for the online game, Akinator, written in Python.

`Akinator <https://en.akinator.com/>`_ is a web-based game which tries to determine what character you are thinking of by asking a series of questions.

Installing
----------

To install, just run the following command::

  python3 -m pip install -U asyncakinator

Requirements
~~~~~~~~~~~~
- Python ≥3.9

- ``requests``

- ``aiohttp``


Usually, ``pip`` will handle these for you.

Quick Examples
--------------

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

Documentation
-------------
Documention can be found `here. <https://asyncakinator.readthedocs.io/en/latest/>`_