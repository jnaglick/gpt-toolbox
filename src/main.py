from agents import WebInformedAgent
from utils import wandb_autolog
from llm import ChatSession

from plugin import start_server

start_server()

# questions that dont require web access
noop_benchmarks = [
    "Name the capital city of France.",
    "What is the largest planet in our solar system?",
    "Who is the author of the Harry Potter book series?",
    "What is the smallest country in the world by land area?",
    "What is the name of the world's largest ocean?",
    "Who was the first person to step on the moon?",
    "What is the name of the largest desert in the world?",
    "Who painted the Mona Lisa?",
    "What is the currency used in Japan?",
    "What is the highest mountain in Africa?"
]

# questions that require web access for current gpt3.5
after_sept_2021 = [
    ["Who won the Academy Award for Best Picture in 2023?", "Everything Everywhere All at Once"],
    ["Who lost the MLB world series in 2022?", "The Philadelphia Phillies"],
    ["What was amazons closing stock price for 2022?", "84.00"],
    # "Which book won the Pulitzer Prize for Fiction in 2023?",
    ["Who won the Nobel Prize in Physics in 2022?", "Alain Aspect, John F. Clauser, and Anton Zeilinger"],
    ["What was the highest-grossing movie of 2022?", "Top Gun Maverick"],
    "Which scientific breakthrough won the Breakthrough of the Year award in 2022?",
    "Who won the 2023 Grammy Award for Album of the Year?",
     # "What was the most influential technology trend in 2022?",
    "Which country hosted the 2022 Winter Olympics?",
]

check = [
    ["When does your training data end?"] # sept 2021
]

""" with ChatSession() as session:
    with wandb_autolog():
        web_agent = WebInformedAgent("Main", session)

        prediction = web_agent.prediction("Who won the Academy Award for Best Actor in 2023 and who lost the MLB world series in 2022?")

        print(prediction) """
 