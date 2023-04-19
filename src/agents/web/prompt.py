def system(): return """
A. Introduction
You are an assistant that can can ask the user to search the web or access a webpage to help you answer their question.
The user's input will contain the question and additional context.
If you have all the information needed to answer the question, do so. If you dont, ask for a single web search or web access.
The context will often help you answer the question. The context will be a list of previous web searches and web accesses, if any. 
Don't ask for the same WebSearch or WebAccess that appears in the context.

B. User Input Format:
CONTEXT:
WebSearch: <previous search term>
Results: <result of previous search>
|||||
WebAccess: <previous url>
Results: <result of previous access>
(WebSearch,Result or WebAccess,Result can appear 0 or more times, separated by |||||)
QUESTION: <user question here>

C. Your Output Format:
InternalThought: <your thoughts, if any>
InternalAnswer: <your answers, if any>
(InternalThought,InternalAnswer can appear 0 or more times)
Do I have enough information to answer the user's query: (yes/no)
(Finally, one of the following:)
Answer: <your final answer>
WebSearch: <search term>
WebAccess: <url>

D. Most important instructions:
1. Answer: <your final answer> should be the complete, final answer to the users question. Do not reference *ANY* CONTEXT in your answer!
2. After resolving your InternalThought+InternalAnswer's, always ask yourself "Do I have enough information..." once and only once.
3. Remember to not repeat a WebSearch or WebAccess that appears in the context! Example: If "WebAccess: <url>" appears in the context, you should not output "WebAccess: <url>"!
4. After asking yourself "Do I have enough information...", output only a single line containing one of: Answer, WebSearch, WebAccess.
""".strip()

def user(question, context=""):
    return f""" 
CONTEXT:
{context}
QUESTION: {question}
    """.strip()

def user_context(context_items):
    return "|||||".join([
        f"{action}: {action_input}\nResults: {result}"
        for (action, action_input, result) in context_items
    ])

def example_internal(thought, answer):
    return f"""
InternalThought: {thought}
InternalAnswer: {answer}
    """.strip()

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
          """
WebSearch: current weather new york
Results: [('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New york, NY Weather Forecast and Conditions - The Weather Channel', 'https://weather.com/weather/today/l/New+York+NY+USNY0996:1:US'), ('Local Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/ny/new-york-weather'), ('Weather for New York, New York, USA - TimeAndDate', 'https://www.timeanddate.com/weather/usa/new-york'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city'), ('New York City, NY 10-Day Weather Forecast - The Weather Channel ...', 'https://weather.com/weather/tenday/l/96f2f84af9a5f5d452eb0574d4e4d8a840c71b05e22264ebdc0056433a642c84'), ('New York, New York 7 Day Weather Forecast - The Weather Network', 'https://www.theweathernetwork.com/us/weather/new-york/new-york'), ('New York, New York | Current Weather Forecasts, Live Radar Maps & News ...', 'https://www.weatherbug.com/weather-forecast/now/new-york-ny-10001'), ('NY Current Conditions - sfgate.com', 'https://www.sfgate.com/weather/article/ny-current-conditions-17896774.php'), ('NY Current Conditions', 'https://www.sfchronicle.com/weather/article/ny-current-conditions-17903155.php'), ('New York, New York, USA 14 day weather forecast - TimeAndDate', 'https://www.timeanddate.com/weather/usa/new-york/ext'), ('National Weather Service', 'https://forecast.weather.gov/MapClick.php?lat=40.71455000000003&lon=-74.00713999999994'), ('NWS Forecast Office New York, NY - National Weather Service', 'https://www.weather.gov/okx/'), ('New York - BBC Weather', 'https://www.bbc.com/weather/5128581'), ('National Weather Service', 'https://forecast.weather.gov/MapClick.php?zoneid=NYZ072'), ('New York - BBC Weather', 'https://www.bbc.com/weather/2641508'), ('New York (United States of America) weather - Met Office', 'https://www.metoffice.gov.uk/weather/forecast/dr5reg58f')]
          """.strip()
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
Results: [('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New york, NY Weather Forecast and Conditions - The Weather Channel', 'https://weather.com/weather/today/l/New+York+NY+USNY0996:1:US'), ('Local Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/ny/new-york-weather'), ('Weather for New York, New York, USA - TimeAndDate', 'https://www.timeanddate.com/weather/usa/new-york'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city')]
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
Results: [('New York, NY Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/current-weather/349727'), ('New York, NY Weather Forecast | AccuWeather', 'https://www.accuweather.com/en/us/new-york/10021/weather-forecast/349727'), ('New york, NY Weather Forecast and Conditions - The Weather Channel', 'https://weather.com/weather/today/l/New+York+NY+USNY0996:1:US'), ('Local Current Weather | AccuWeather', 'https://www.accuweather.com/en/us/ny/new-york-weather'), ('Weather for New York, New York, USA - TimeAndDate', 'https://www.timeanddate.com/weather/usa/new-york'), ('New York City, NY Weather Conditions | Weather Underground', 'https://www.wunderground.com/weather/us/ny/new-york-city')]
          """.strip()
        ),
        example_answer("The current temperature in New York is 64 degrees Fahrenheit.")
      ],
    ]

def refine_search(query, results): return f"""
  Given this query: {query}
  Give me a very brief summary of the relevant information from this result: : {results}
""".strip()