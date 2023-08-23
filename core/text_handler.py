import logging
from os import path, linesep

from context import BookDetails, ModelDetails, SOURCE_DIR
from core.utils import num_tokens

logger = logging.getLogger('text_handler')


class TextHandler:
    def __init__(self, book_details: BookDetails, model_details: ModelDetails):
        self.book_details = book_details
        self.model_details = model_details

    def _process_line(self, line: str, chunks: list[str]) -> list[str]:
        chunk = f'{chunks[-1] if chunks else ""}{line}'
        if num_tokens(chunk, self.model_details.name) <= self.model_details.max_gpt_tokens:
            if chunks:
                chunks[-1] = chunk
            else:
                chunks.append(chunk)
        else:
            is_new_line: bool = True
            sentences = line.split(sep='. ')
            for sentence in sentences:
                chunk = f'{chunks[-1] if chunks else ""}{linesep if is_new_line else " "}{sentence}.'
                if num_tokens(chunk, self.model_details.name) <= self.model_details.max_gpt_tokens:
                    if chunks:
                        chunks[-1] = chunk
                    else:
                        chunks.append(chunk)
                else:
                    chunks.append(f'{sentence}.')

        return chunks

    def chunks(self) -> list[str]:
        chunks: list[str] = list()

        fqfp = path.join(SOURCE_DIR, self.book_details.source_filename)
        with open(fqfp, 'r') as source_file:
            while True:
                line = source_file.readline()
                if not line:
                    break

                chunks = self._process_line(line, chunks)
        return chunks


if __name__ == '__main__':
    from context import DOOMED_CITY, GPT_35_TURBO
    handler = TextHandler(DOOMED_CITY, GPT_35_TURBO)
    chunks = handler.chunks()
    print(f'total chunks = {len(chunks)}, head = {chunks[:2]}, tail = {chunks[-2:]}')
