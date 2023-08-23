from os import path

import openai
import requests
from tqdm import tqdm

import context
from context import BookDetails, ModelDetails, TRANSLATED_DIR
from core import text_handler, translation_handler
from secrets import API_SECRET_KEY, API_ENDPOINT, API_VERSION


def openai_connection_init(show_output: bool = False) -> bool:
    openai.api_key = API_SECRET_KEY
    openai.api_type = 'open_ai'
    openai.api_base = API_ENDPOINT

    url = f'{openai.api_base}/engines'
    r = requests.get(url, headers={'Authorization': f'Bearer {API_SECRET_KEY}'})
    if show_output:
        print(f'URL={url}')
        print(r.text)
    return 200 <= r.status_code <= 400


class Translator:
    def __init__(self, book_details: BookDetails, model_details: ModelDetails):
        self.book_details = book_details
        self.model_details = model_details
        self.teh = text_handler.TextHandler(book_details, model_details)
        self.trh = translation_handler.TranslationHandler(book_details, model_details)

    def run(self):
        translated_text: list[str] = list()
        for chunk in tqdm(self.teh.chunks()):
            translated_chunk = self.trh.translate(chunk)
            translated_text.append(translated_chunk)

        fqfn = path.join(TRANSLATED_DIR, self.book_details.target_filename)
        with open(fqfn, 'w+') as translated_file:
            translated_file.writelines(translated_text)


if __name__ == '__main__':
    openai_connection_init(show_output=True)
    translator = Translator(context.DOOMED_CITY, context.GPT_35_TURBO_16K)
    translator.run()
