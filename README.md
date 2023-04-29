# 🧰 GPT Toolbox

A GPT-based system that generates and executes high-level plans, using specialized "agents" that augment LLMs with better reasoning and external information sources

## Setup:

0. Sign up / get your OpenAI API key: https://platform.openai.com/signup

0. Create the env file: `cp .env.example .env`, put your API key where specified

0. Install deps: `pip3 install -r requirements.txt`

0. Run: `python3 src/main.py`

## Credits:

*  **"Techniques to improve reliability"** (https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md) from the openai-cookbook and many of its citations, especially **CoT prompting** (https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)

* The concept of "agents" that iteratively prompt an llm was taken from **Langchain** (https://github.com/hwchase17/langchain)

* The executive agent is an implementation of the system described in **HuggingGPT** (https://arxiv.org/pdf/2303.17580.pdf) and its planning step prompt was forked from **JARVIS** (https://github.com/microsoft/JARVIS)

* General inspiration from Andrew Mayne (https://andrewmayneblog.wordpress.com/)

* Project named by gpt3.5
