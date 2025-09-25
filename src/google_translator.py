import logging

from googletrans import Translator

logger = logging.getLogger(__name__)

class GoogleTranslator:

    def __init__(self):
        self.translator = Translator()

    async def english_to_russian(self, text):
        return await self.translate(src='en', dest='ru', text=text)

    async def russian_to_english(self, text):
        return await self.translate(src='ru', dest='en', text=text)

    async def translate(self, src, dest, text):
        try:
            translated_obj = await  self.translator.translate(text, src=src, dest=dest)
            return translated_obj.text
        except Exception as e:
            logger.error(f'Error translate {src} > {dest}, error: {e}; text: {text}')
        return text
