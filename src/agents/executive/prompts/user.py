def user(user_prompt, chat_log=''):
  return f"""
The chat log [ {chat_log} ] may contain the resources I mentioned.

Now I input {{ {user_prompt} }}. 

Pay attention to the input and output types of tasks and the dependencies between tasks.

Remember Most important instruction: Only output the formatted json task list. Do not output any other text
""".strip()
