# 🧰 GPT Toolbox

A system that augments GPT with general purpose tools. Currently implemented via gpt4 plugin that must be running on localhost.

## Setup:

1. You need the following from OpenAI:

    - **API key**: https://platform.openai.com/signup

    - **GPT4 plugin developer access**: Be subscribed to "Plus" and join the waitlist for plugin dev https://openai.com/waitlist/plugins

      - It seems some people get in much sooner than others. I speculate that using the 3.5 API might get you "noticed". Try other projects and check out the `agents` module

2. Init the project: `make init`

3. Edit the env file `.env`, put required API keys where specified

| Name | Type | Description |
| ---- | ---- | ----------- |
| OPENAI_API_KEY | string | OpenAI API key |
| LOG_LEVEL | string | Log level (VERBOSE, NORMAL, ERROR, NONE) |
| WANDB_ENABLED | boolean | Enable Weights & Biases logging |



## Plugin

1. Start the server on **localhost:3333**:

```
make start
```

## Credits:

* OpenAI cookbook (https://github.com/openai/openai-cookbook/tree/main/examples)

* Before this was a plugin, this project started as a different way of doing "agents" (w/o the AgentExecutor) from **Langchain** (https://github.com/hwchase17/langchain)

* The executive agent is an implementation of the planning step of the system described in **HuggingGPT** (https://arxiv.org/pdf/2303.17580.pdf) and its prompt was forked from **JARVIS** (https://github.com/microsoft/JARVIS)

* Project named by gpt3.5, logo by midjourney

## Logo:

![toolbox](./src/plugin/.well-known/logo.png)
