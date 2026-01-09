import json
from typing import List

from openai import OpenAI

from dto.response_types import AskMapAIResponse
from models.location import Location


def get_answer_deepseek(client: OpenAI, isDeepThinking: bool, prompt: str) -> AskMapAIResponse:
    response = client.chat.completions.create(
        model= "deepseek-reasoner" if isDeepThinking else "deepseek-chat",
        messages=[
            {"role": "system", "content":
             "You are an AI assitant from and built by AskMapAI that answers questions "
            "about locations, cities, places, countries, etc. The questions asked will be "
            "related to specific locations, answer them in order in the following format "
            "with no other extra text, no space, no return to line: [{'orderNum': 1, "
            "'lat': latitude_of_the_location_in_float, 'lng': longitude_of_the_location_in_float, 'name': 'Name of the place', "
            "'info': 'information about the place related to the question itself'},"
            "{...the rest of locations}]. if it is not related, give normal answer."},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    locations:List[Location] = []
    answer:str = ""
    content = response.choices[0].message.content

    if '[{' in content:
        data = json.loads(content.replace("'", '"'))
        locations = [ Location(**item) for item in data]
    else:
        answer = content

    return (locations, answer)