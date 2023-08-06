from typing import List
import requests
from .error import AuthenticationError, ArgumentValidationError, ServerError


class Options:
    def __init__(self,
                 temperature: float = 0.7,
                 max_tokens: int = 100,
                 top_p: float = 1,
                 frequency_penalty: float = 0,
                 presence_penalty: float = 0,
                 stop: [str] = ["Q:"],
                 best_of: int = 1):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.best_of = best_of


class Cerebrate:
    def __init__(self, api_key: str, url: str = 'https://app.cerebrate.ai/api/predict'):
        self._api_key = api_key
        self._url = url

    def predict(self, task: str, examples: [str], query: str, options: Options = Options()) -> List[str]:
        examples_string = '\n'.join(examples)
        prompt = f"{task}\n\nexamples:\n{examples_string}\n\n{query}"

        response = self.__send_request(prompt, options)
        return list(response)

    def raw(self, prompt: str, options: Options = Options()) -> List[str]:
        response = self.__send_request(prompt, options)

        return list(response)

    # def match(self):
    #     raise Exception("Not implemented!")

    # def recommend(self):
    #     raise Exception("Not implemented!")

    def __send_request(self, prompt: str, options: Options):
        body = {
            "data": {
                "prompt": prompt,
                "temperature": options.temperature,
                "maxTokens": options.max_tokens,
                "topP": options.top_p,
                "frequencyPenalty": options.frequency_penalty,
                "presencePenalty": options.presence_penalty,
                "stop": options.stop,
                "bestOf": options.best_of,
            }
        }

        response = requests.post(
            self._url,
            json=body,
            headers={"Authorization": self._api_key, "Content-Type": "application/json"}
        )
        if response.status_code != 200:
            if response.json()['extensions'] is not None:
                match response.json()['extensions']['code']:
                    case 'UNAUTHENTICATED':
                        raise AuthenticationError(message=response.json()['message'], code=401, status='Unauthorized')
                    case 'BAD_USER_INPUT':
                        raise ArgumentValidationError(message=response.json()['message'], code=400, status='Bad request')
                    case _:
                        raise ServerError(message=response.json()['message'], code=500, status='Internal server error')
            raise ServerError(message='Unknown error.', code=500, status='Internal server error')

        return response.json()
