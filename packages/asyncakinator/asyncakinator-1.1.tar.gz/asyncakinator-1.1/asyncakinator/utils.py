"""
MIT License

Copyright (c) 2019 NinjaSnail1080

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

from typing import Any, TypedDict


from .exceptions import (
    InvalidAnswerError,
    InvalidLanguageError,
    AkinatorConnectionFailure,
    AkinatorTimedOut,
    AkinatorNoQuestions,
    AkinatorServerDown,
    AkinatorTechnicalError,
)


class Guess(TypedDict):
    id: int
    name: str
    id_base: int
    proba: float
    description: str
    valide_contrainte: int
    ranking: int
    pseudo: str
    picture_path: str
    corrupt: int
    relative: int
    award_id: int
    flag_photo: int
    absolute_picture_path: str


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


def format_guess(guess: dict[str, str]) -> Guess:
    return {
        "id": int(guess["id"]),
        "name": guess["name"],
        "id_base": int(guess["id_base"]),
        "proba": float(guess["proba"]),
        "description": guess["description"],
        "valide_contrainte": int(guess["valide_contrainte"]),
        "ranking": int(guess["ranking"]),
        "pseudo": guess["pseudo"],
        "picture_path": guess["picture_path"],
        "corrupt": int(guess["corrupt"]),
        "relative": int(guess["relative"]),
        "award_id": int(guess["award_id"]),
        "flag_photo": int(guess["flag_photo"]),
        "absolute_picture_path": guess["absolute_picture_path"],
    }

def answer_to_id(answer: str | int) -> str:
    """Convert an input answer string into an Answer ID for Akinator"""

    ans = str(answer).lower()
    if ans in {"yes", "y", "0"}:
        return "0"
    elif ans in {"no", "n", "1"}:
        return "1"
    elif ans in {"i", "idk", "i dont know", "i don't know", "2"}:
        return "2"
    elif ans in {"probably", "p", "3"}:
        return "3"
    elif ans in {"probably not", "pn", "4"}:
        return "4"
    else:
        raise InvalidAnswerError(f"{answer} is an invalid answer.")


def get_lang_and_theme(lang=None):
    """Returns the language code and theme based on what is input"""

    if lang is None:
        return {"lang": "en", "theme": "c"}

    lang = str(lang).lower()
    if lang == "en" or lang == "english":
        return {"lang": "en", "theme": "c"}
    elif lang == "en_animals" or lang == "english_animals":
        return {"lang": "en", "theme": "a"}
    elif lang == "en_objects" or lang == "english_objects":
        return {"lang": "en", "theme": "o"}
    elif lang == "ar" or lang == "arabic":
        return {"lang": "ar", "theme": "c"}
    elif lang == "cn" or lang == "chinese":
        return {"lang": "cn", "theme": "c"}
    elif lang == "de" or lang == "german":
        return {"lang": "de", "theme": "c"}
    elif lang == "de_animals" or lang == "german_animals":
        return {"lang": "de", "theme": "a"}
    elif lang == "es" or lang == "spanish":
        return {"lang": "es", "theme": "c"}
    elif lang == "es_animals" or lang == "spanish_animals":
        return {"lang": "es", "theme": "a"}
    elif lang == "fr" or lang == "french":
        return {"lang": "fr", "theme": "c"}
    elif lang == "fr_animals" or lang == "french_animals":
        return {"lang": "fr", "theme": "a"}
    elif lang == "fr_objects" or lang == "french_objects":
        return {"lang": "fr", "theme": "o"}
    elif lang == "il" or lang == "hebrew":
        return {"lang": "il", "theme": "c"}
    elif lang == "it" or lang == "italian":
        return {"lang": "it", "theme": "c"}
    elif lang == "it_animals" or lang == "italian_animals":
        return {"lang": "it", "theme": "a"}
    elif lang == "jp" or lang == "japanese":
        return {"lang": "jp", "theme": "c"}
    elif lang == "jp_animals" or lang == "japanese_animals":
        return {"lang": "jp", "theme": "a"}
    elif lang == "kr" or lang == "korean":
        return {"lang": "kr", "theme": "c"}
    elif lang == "nl" or lang == "dutch":
        return {"lang": "nl", "theme": "c"}
    elif lang == "pl" or lang == "polish":
        return {"lang": "pl", "theme": "c"}
    elif lang == "pt" or lang == "portuguese":
        return {"lang": "pt", "theme": "c"}
    elif lang == "ru" or lang == "russian":
        return {"lang": "ru", "theme": "c"}
    elif lang == "tr" or lang == "turkish":
        return {"lang": "tr", "theme": "c"}
    elif lang == "id" or lang == "indonesian":
        return {"lang": "id", "theme": "c"}
    else:
        raise InvalidLanguageError('You put "{}", which is an invalid language.'.format(lang))


def raise_connection_error(response):
    """Raise the proper error if the API failed to connect"""
    if response == "KO - SERVER DOWN":
        raise AkinatorServerDown("Akinator's servers are down in this region. Try again later or use a different language")

    elif response == "KO - TECHNICAL ERROR":
        raise AkinatorTechnicalError("Akinator's servers have had a technical error. Try again later or use a different language")

    elif response == "KO - TIMEOUT":
        raise AkinatorTimedOut("Your Akinator session has timed out")
    elif response in ["KO - ELEM LIST IS EMPTY", "WARN - NO QUESTION"]:
        raise AkinatorNoQuestions('"Akinator.step" reached 79. No more questions')
    else:
        raise AkinatorConnectionFailure(f"An unknown error has occured. Server response: {response}")
