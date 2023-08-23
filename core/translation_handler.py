import openai

import context
from context import BookDetails, ModelDetails

NEGATIVE_ANSWER = 'I could not translate.'

from secrets import API_SECRET_KEY, API_ENDPOINT, API_VERSION


class TranslationHandler:
    def __init__(self, book_details: BookDetails,model_details: ModelDetails):
        self.book_details = book_details
        self.model_details = model_details
        # self._system = f'Translate from {book_details.source_language} to {book_details.target_language}: '

        self._system = (
            f'Translate following text segments from {book_details.source_language} to {book_details.target_language}. '
            f'The text is part of a novel {book_details.title} and is broken into segments to fit request constraints. '
            f'Ensure that the translation maintains the flow and context across segments, and is both accurate and fluent. '
            f'Handle idioms, cultural references, and nuances in a way that is coherent '
            f'with modern {book_details.target_language} orthography and literary language style: '
        )
        print(f'system message: \n{self._system}')

        openai.api_key = API_SECRET_KEY
        openai.api_type = 'open_ai'
        openai.api_base = API_ENDPOINT
        openai.api_version = API_VERSION

    def form_request(self, request_body: str, include_history: bool = True) -> list[dict[str, str]]:
        messages: list[dict[str, str]] =  list()

        messages.extend([
            {'role': 'system', 'content': self._system},
            {'role': 'user', 'content': request_body},
        ])
        return messages

    def translate(self, chunk: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model_details.name,
            messages=self.form_request(chunk),
            temperature=0.15,
            # max_tokens=3096,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0
        )

        response_message = response['choices'][0]['message']['content']
        return response_message


if __name__ == '__main__':
    trh = TranslationHandler(context.DOOMED_CITY, context.GPT_35_TURBO)
    result = trh.translate('- Дворник должен быть метущий, - наставительно заметил Андрей, крутя кистью правой руки и прислушиваясь к своим ощущениям: ему показалось, что он немного растянул сухожилие.')
    print(result)
