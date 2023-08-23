from dataclasses import dataclass
from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))
SOURCE_DIR = path.abspath(path.join(PROJECT_ROOT, 'text_source'))
TRANSLATED_DIR = path.abspath(path.join(PROJECT_ROOT, 'text_translated'))


@dataclass(kw_only=True)
class BookDetails:
    title: str
    language: str
    authors: list[str]
    publication_year: int
    source_language: str
    target_language: str
    source_filename: str
    target_filename: str


@dataclass
class ModelDetails:
    name: str
    max_gpt_tokens: int


# https://platform.openai.com/docs/models
GPT_35_TURBO = ModelDetails('gpt-3.5-turbo', int(4096 / 2.2))
GPT_35_TURBO_16K = ModelDetails('gpt-3.5-turbo-16k', int(16384 / 2.25))
GPT_4_8K = ModelDetails('gpt-4', int(8192 / 2.2))
GPT_4_32K = ModelDetails('gpt-4-32k', int(32768 / 2.2) )


DOOMED_CITY = BookDetails(
    title='Град обреченный',
    language='russian',
    authors=['Аркадій Натанович Стругацький', 'Борис Натанович Стругацький'],
    publication_year=1972,
    source_language='Russian',
    target_language='Ukrainian',
    # source_filename='grad-obrechenniy.txt',
    source_filename='grad-obrechenniy-snippet.txt',
    target_filename='grad-pryrechenyy.txt',
)
