import os
from babel.support import Translations
from aiogram import Bot, Dispatcher, types


class I18n:
    def __init__(self, default_locale="en", locales_dir="locales"):
        self.locales_dir = locales_dir
        self.default_locale = default_locale

    def get_translations(self, locale):
        mo_file = os.path.join(self.locales_dir, locale, "LC_MESSAGES", "messages.mo")
        if os.path.exists(mo_file):
            with open(mo_file, "rb") as f:
                return Translations(f)
        return Translations()

    def gettext(self, locale, msgid):
        translations = self.get_translations(locale)
        return translations.gettext(msgid)


i18n = I18n()
