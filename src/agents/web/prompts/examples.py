from . import user, user_context

def example_thought(thought):
    return f"""
InternalThought: {thought}
    """.strip()

def example_answer(output):
    return f"""
Do I have enough information to answer the user's query: yes
Answer: {output}
    """.strip()

def example_search(output):
    return f"""
Do I have enough information to answer the user's query: no
WebSearch: {output}
    """.strip()

def example_access(output):
    return f"""
Do I have enough information to answer the user's query: no
WebAccess: {output}
    """.strip()

def examples():
    return [
      [
        user(
          "What is the weather in New York?"
        ),
        "\n".join([
          example_thought(
            "I dont know the current weather. I need to run a web search to find websites that can tell me."
          ),
          example_search("current weather new york"),
        ])
      ],
      [
        user(
          "What is the weather in New York?", 
          user_context([[
            "WebSearch", 
            "current weather new york", 
            "[('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city')]"
          ]])
        ),
        "\n".join([
          example_thought(
            "I dont know the current weather. I know a list of websites that can tell me from the context. I need to run a web access on one of them."
          ),
          example_access("https://www.accuweather.com/en/us/new-york/10021/current-weather/349727"),
        ])
      ],
      [
        user(
          "What is the weather in New York?", 
          """
WebAccess: https://www.accuweather.com/en/us/new-york/10021/current-weather/349727
Results: Access Denied
|||||
WebSearch: current weather new york
Results: [('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city')]
          """.strip()
        ),
        "\n".join([
          example_thought(
            "I dont know the current weather. I know a list of websites that can tell me from the context. I know the results for www.accuweather.com were Access Denied. I need to run a web access on one of them that isnt www.accuweather.com and I think is more likely to work."
          ),
          example_access("https://www.wunderground.com/weather/us/ny/new-york-city"),
        ])
      ],
      [
        user(
          "What is the weather in New York?", 
          """
WebAccess: https://www.wunderground.com/weather/us/ny/new-york-city
Results: New York City Feels like 68 F Clear Alerts
|||||
WebAccess: https://www.accuweather.com/en/us/new-york/10021/current-weather/349727
Results: Access Denied
|||||
WebSearch: current weather new york
Results: [('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city')]
          """.strip()
        ),
        example_answer("The current temperature in New York is 64 degrees Fahrenheit.")
      ],
    ]