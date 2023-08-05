"""
MIT License

Copyright (c) 2019 NinjaSnail1080
Copyright (c) 2022 avizum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

import aiohttp

from .exceptions import CantGoBackAnyFurther
from .utils import (
    MISSING,
    Guess,
    answer_to_id,
    format_guess,
    get_lang_and_theme,
    raise_connection_error
)

# * URLs for the API requests
NEW_SESSION_URL = "https://{}/new_session?callback=jQuery331023608747682107778_{}&urlApiWs={}&partner=1&childMod={}&player=website-desktop&uid_ext_session={}&frontaddr={}&constraint=ETAT<>'AV'&soft_constraint={}&question_filter={}"
ANSWER_URL = "https://{}/answer_api?callback=jQuery331023608747682107778_{}&urlApiWs={}&childMod={}&session={}&signature={}&step={}&answer={}&frontaddr={}&question_filter={}"
BACK_URL = "{}/cancel_answer?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}&answer=-1&question_filter={}"
WIN_URL = "{}/list?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}"

# * HTTP headers to use for the requests
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.92 Chrome/81.0.4044.92 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


class Akinator:
    """
    A class that represents an async Akinator game.

    .. note::

        Some attributes will be missing before a game has started.
        Use :func:`Akinator.start` a game before accessing these attributes.

    Parameters
    ----------
    language: :class:`str`
        The language to use when starting the game. "en" if not provided, or you can use the following:

        - ``en``: English (default)
        - ``en_animals``: English server for guessing animals
        - ``en_objects``: English server for guessing objects
        - ``ar``: Arabic
        - ``cn``: Chinese
        - ``de``: German
        - ``de_animals``: German server for guessing animals
        - ``es``: Spanish
        - ``es_animals``: Spanish server for guessing animals
        - ``fr``: French
        - ``fr_animals``: French server for guessing animals
        - ``fr_objects``: French server for guessing objects
        - ``il``: Hebrew
        - ``it``: Italian
        - ``it_animals``: Italian server for guessing animals
        - ``jp``: Japanese
        - ``jp_animals``: Japanese server for guessing animals
        - ``kr``: Korean
        - ``nl``: Dutch
        - ``pl``: Polish
        - ``pt``: Portuguese
        - ``ru``: Russian
        - ``tr``: Turkish
        - ``id``: Indonesian

    child_mode: :class:`bool`
        Whether to use child mode or not. Defaults to False.

    Attributes
    ----------
    question: :class:`str`
        The question that Akinator is asking.
    progression: :class:`float`
        How far in the game you are.
    step: :class:`int`
        The question you are on, starting from 0.
    first_guess: :class:`Guess`
        A dictionary containing the first guess information.
    guesses: list[:class:`Guess`]
        A list of :class:`Guess` dictionary of guesses from greatest to least probability.

    Raises
    ------
    :exc:`TypeError`
        The session is not an class`aiohttp.ClientSession`.
    """

    def __init__(
        self,
        language: str = "en",
        child_mode: bool = False,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        if session is not None and not isinstance(session, aiohttp.ClientSession):
            raise TypeError("session must be a aiohttp.ClientSession")

        self.language: str = language
        self.child_mode: bool = child_mode
        self._session: aiohttp.ClientSession = MISSING

        self.question: str = MISSING
        self.progression: float = 0.0
        self.step: int = 0

        self.first_guess: Guess = MISSING
        self.guesses: list[Guess] = MISSING

        self.uri: str = MISSING
        self.server: str = MISSING
        self.signature: int = MISSING
        self.uid: str = MISSING
        self.frontaddr: str = MISSING
        self.question_filter: str = MISSING
        self.timestamp: float = 0.0
        self.session: int = 0

    async def _create_session(self) -> None:
        self._session = aiohttp.ClientSession()

    def _update(self, resp: Any, start: bool = False) -> None:
        """Update class variables"""

        if start:
            self.session = int(resp["parameters"]["identification"]["session"])
            self.signature = int(resp["parameters"]["identification"]["signature"])
            self.question = str(resp["parameters"]["step_information"]["question"])
            self.progression = float(resp["parameters"]["step_information"]["progression"])
            self.step = int(resp["parameters"]["step_information"]["step"])
        else:
            self.question = str(resp["parameters"]["question"])
            self.progression = float(resp["parameters"]["progression"])
            self.step = int(resp["parameters"]["step"])

    def _parse_response(self, response: Any) -> Any:
        """Parse the JSON response and turn it into a Python object"""

        return json.loads(",".join(response.split("(")[1::])[:-1])

    async def _get_session_info(self) -> None:
        """Get uid and frontaddr from akinator.com/game"""

        info_regex = re.compile("var uid_ext_session = '(.*)'\\;\\n.*var frontaddr = '(.*)'\\;")

        async with self._session.get("https://en.akinator.com/game") as w:
            match = info_regex.search(await w.text())
            if not match:
                return

        self.uid, self.frontaddr = match.groups()[0], match.groups()[1]

    async def _auto_get_region(self, lang: str, theme: str) -> dict[str, str]:
        """Automatically get the uri and server from akinator.com for the specified language and theme"""

        server_regex = re.compile(
            '[{"translated_theme_name":"[\s\S]*","urlWs":"https:\\\/\\\/srv[0-9]+\.akinator\.com:[0-9]+\\\/ws","subject_id":"[0-9]+"}]'
        )

        uri = f"{lang}.akinator.com"
        bad_list = ["https://srv12.akinator.com:9398/ws"]
        while True:
            async with self._session.get(f"https://{uri}") as w:
                match = server_regex.search(await w.text())
                if match is None:
                    return {"url": MISSING, "server": MISSING}
            parsed = json.loads(match.group().split("'arrUrlThemesToPlay', ")[-1])
            server = MISSING
            if theme == "a":
                server = next((i for i in parsed if i["subject_id"] == "14"), MISSING)["urlWs"]
            elif theme == "c":
                server = next((i for i in parsed if i["subject_id"] == "1"), MISSING)["urlWs"]
            elif theme == "o":
                server = next((i for i in parsed if i["subject_id"] == "2"), MISSING)["urlWs"]
            if server not in bad_list:
                return {"uri": uri, "server": server}

    async def start(
        self,
        language: str | None = None,
        child_mode: bool | None = None,
    ) -> str:
        """
        Starts a new game. This should be called before any other method.


        Parameters
        ----------
        language: :class:`str` | :class:`None`
            The language to use when starting the game.
        child_mode: :class:`bool`
            Whether or not to use child mode. If True, the game will be more "child-friendly".

        Raises
        ------
        :exc:`TypeError`
            The `session` parameter was not a :class:`aiohttp.ClientSession`.

        Returns
        -------
        :class:`str`
            The first question that Akinator is asking.
        """
        if self._session is MISSING:
            await self._create_session()

        if language is not None:
            self.language = language
        if child_mode is not None:
            self.child_mode = child_mode

        self.timestamp = time.time()

        region_info = await self._auto_get_region(
            get_lang_and_theme(self.language)["lang"],
            get_lang_and_theme(self.language)["theme"]
        )
        self.uri, self.server = region_info["uri"], region_info["server"]

        soft_constraint = "ETAT%3D%27EN%27" if self.child_mode else ""
        self.question_filter = "cat%3D1" if self.child_mode else ""
        await self._get_session_info()

        async with self._session.get(
            NEW_SESSION_URL.format(
                self.uri,
                self.timestamp,
                self.server,
                str(self.child_mode).lower(),
                self.uid,
                self.frontaddr,
                soft_constraint,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp, True)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def answer(self, answer: str) -> str:
        """
        Answers the current question accessed with :attr:`Akinator.question`, and returns the next question.

        Parameter
        ---------
        answer: :class:`str`
            The answer to the current question. It can be one of the following:
                - Yes: "y", "yes" "0"
                - No: "n", "no", "1"
                - I don't know: "i", "idk", "i dont know", "i don't know", "2"
                - Probably: "p", "probably", "3"
                - Probably not: "pn", "probably not", "4"

        Raises
        ------
        :exc:`InvalidAnswerError`
            The answer was not one of the valid answers.

        Returns
        -------
        :class:`str`
            The next question that Akinator asks.
        """
        ans = answer_to_id(answer)

        async with self._session.get(
            ANSWER_URL.format(
                self.uri,
                self.timestamp,
                self.server,
                str(self.child_mode).lower(),
                self.session,
                self.signature,
                self.step,
                ans,
                self.frontaddr,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def back(self) -> str:
        """
        Go back to the previous question.

        Raises
        ------
        :exc:`CantGoBackAnyFurther`
            The Akinator game is on the first question, so it can't go back anymore.

        Returns
        -------
        :class:`str`
            The previous question that Akinator asked.
        """
        if self.step == 0:
            raise CantGoBackAnyFurther("You were on the first question and couldn't go back any further")

        async with self._session.get(
            BACK_URL.format(
                self.server,
                self.timestamp,
                str(self.child_mode).lower(),
                self.session,
                self.signature,
                self.step,
                self.question_filter,
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def win(self) -> Guess:
        """
        Get Akinator's current guesses based on the responses to the questions thus far.

        This function will set:

        :attr:`Akinator.first_guess`
            The first guess that is returned
        :attr:`Akinator.guesses`
            A list of guesses from greatest to lowest probablity

        .. note::

            It is recommended that you call this function when `Akinator.progression` is above 85.0,
            because by then, Akinator will most likely narrowed the guesses down to one.
        """
        async with self._session.get(
            WIN_URL.format(
                self.server, self.timestamp, str(self.child_mode).lower(), self.session, self.signature, self.step
            ),
            headers=HEADERS,
        ) as w:
            resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self.first_guess = format_guess(resp["parameters"]["elements"][0]["element"])
            self.guesses = [format_guess(g["element"]) for g in resp["parameters"]["elements"]]
            return self.first_guess
        else:
            return raise_connection_error(resp["completion"])

    async def close(self) -> None:
        """
        Closes the aiohttp ClientSession.

        .. caution::

            If you specified your own ClientSession, this may interrupt what you are doing with the session.
        """
        if self._session is not MISSING and self._session.closed is False:
            await self._session.close()

        self._session = MISSING
