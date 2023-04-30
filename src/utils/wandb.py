from contextlib import contextmanager

from wandb.integration.openai import autolog

from .env import env

@contextmanager
def wandb_autolog():
    if not env["WANDB_ENABLED"]:
        yield
        return

    autolog({"project": "gpt-toolbox"})
    yield
    autolog.disable()