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

    aki = akinator.Akinator(
        language=akinator.Language.ENGLISH,
        theme=akinator.Theme.ANIMALS,
    )

    async def main():
        question = await aki.start()

        while aki.progression <= 80:
            a = input(f"{question}\n\t")
            if a == "b":
                try:
                    question = await aki.back()
                except akinator.CantGoBackAnyFurther:
                    continue
            else:
                try:
                    question = await aki.answer(akinator.Answer.from_str(a))
                except akinator.InvalidAnswer:
                    print("Invalid answer. Please try again.\n")
                    continue
        await aki.win()

        correct = input(
            f"You are thinking of {aki.first_guess.name} ({aki.first_guess.description}). "
            f"Am I correct?\n{aki.first_guess.absolute_picture_path}\n\t"
        )
        if akinator.Answer.from_str(correct) == akinator.Answer.YES:
            print("Nice.")
        else:
            print("Maybe next time.")
        await aki.close()

    asyncio.run(main())

Documentation
-------------
Documention can be found `here. <https://asyncakinator.readthedocs.io/en/latest/>`_