import os
import json
import discord
from discord import app_commands

from typing import Optional, Dict, Any, Protocol
from collections import defaultdict


DEFAULT_LOCALE = discord.Locale.brazil_portuguese

_translations: Dict[str, Dict[str, Any]] = defaultdict(dict)


class CommandTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContextTypes
    ) -> Optional[str]:
        if locale.value not in _translations.keys():
            locale = DEFAULT_LOCALE
        if not string.extras.get('id'):
            return None
        return Translator(locale)(string.extras['id'])


class TranslatorCallable(Protocol):
    def __call__(self, string: str, **kwargs: Any) -> str:
        ...


class Translator:
    def __init__(self, locale: discord.Locale) -> None:
        self._locale = locale if isinstance(
            locale, str) else locale.value

    def __call__(self, string: str, **kwargs: Any) -> str:
        if _translations.get(self._locale) is None:
            self._locale = DEFAULT_LOCALE.value

        t = _translations[self._locale]
        try:
            for k in string.split('.'):
                t = t[k]
            if isinstance(t, list):
                return ''.join(t).format(**kwargs)
            elif not isinstance(t, str):
                return str(t)
            else:
                return t.format(**kwargs)
        except KeyError:
            return string

    @staticmethod
    def load_locales(path: str = 'locales') -> None:
        _translations.clear()
        for element in os.listdir(path):
            if element.endswith('.json'):
                with open(f'{path}/{element}', 'r', encoding='utf-8') as f:
                    _translations[element[:-5]] = json.load(f)
