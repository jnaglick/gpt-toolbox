from . import user
from .special_tokens import *

def example_previous(previous):
    return f"""
{SECTION_PREVIOUS_ACTIONS}: {previous}
    """.strip()

def example_thought(thought):
    return f"""
{SECTION_INTERNAL_THOUGHT}: {thought}
    """.strip()

def example_answer(output):
    return f"""
{SECTION_ENOUGH_INFO}: yes
{SECTION_ANSWER}: {output}
    """.strip()

def example_search(output):
    return f"""
{SECTION_ENOUGH_INFO}: no
{SECTION_WEB_SEARCH}: {output}
    """.strip()

def examples():
    return [
      [
        user(
          "Who was the 23rd president of the United States?"
        ),
        example_answer(
          "Benjamin Harrison."
        )
      ],
      [
        user(
          "Where is the island of Java?"
        ),
        example_answer(
          "Java is located in Southeast Asia and is part of Indonesia."
        )
      ],
      [
        user(
          "What is the weather in New York?"
        ),
        "\n".join([
          example_thought(
            "Answering this question requires live information, so I will need to search the web."
          ),
          example_search("current weather new york"),
        ])
      ],
      [
        user(
          "What is the weather in New York?", 
          [[
            "WebSearch", 
            "current weather new york", 
            "[('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727', 'Access Denied'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727', 'New York City Feels like 68 F Clear Alerts'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city', 'MORE INFO')]"
          ]]
        ),
        "\n".join([
          example_previous(
            "WebSearch: current weather new york"
          ),
          example_thought(
            "The second result tells me the answer."
          ),
          example_answer("The current temperature in New York is 64 degrees Fahrenheit.")   
        ])
      ],
      [
        user(
          "What is the weather in New York and Who won the Academy Award for Best Picture in 2023?"
        ),
        "\n".join([
          example_thought(
            "Answering this question requires multiple searches, so I'll just pick one."
          ),
          example_search("current weather new york"),
        ])
      ],
      [
        user(
          "What is the weather in New York and Who won the Academy Award for Best Picture in 2023?",
          [[
            "WebSearch", 
            "current weather new york", 
            "[('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727', 'Access Denied'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727', 'New York City Feels like 68 F Clear Alerts'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city', 'MORE INFO')]"
          ]]
        ),
        "\n".join([
          example_previous(
            "WebSearch: current weather new york"
          ),
          example_thought(
            "The second result tells me the answer to the first part of the question, but I need to do another search for the second part of the question."
          ),
          example_search("academy award best picture 2023"),
        ])
      ],
            [
        user(
          "What is the weather in New York and Who won the Academy Award for Best Picture in 2023?",
          [[
            "WebSearch", 
            "current weather new york", 
            "[('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727', 'Access Denied'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727', 'New York City Feels like 68 F Clear Alerts'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city', 'MORE INFO')]"
          ],[
            "WebSearch", 
            "academy award best picture 2023", 
            "[('ACADEMY AWARDS 2023', 'https://www.oscars.org/oscars/ceremonies/2023', 'The Academy Award for Best Picture in 2023 was won by Everything Everywhere All at Once')]"
          ]]
        ),
        "\n".join([
          example_previous(
            "WebSearch: current weather new york, WebSearch: academy award best picture 2023"
          ),
          example_thought(
            "I have enough information to answer the question from the context"
          ),
          example_answer("The current temperature in New York is 64 degrees Fahrenheit. The Academy Award for Best Picture in 2023 was won by Everything Everywhere All at Once.")
        ])
      ],
    ]