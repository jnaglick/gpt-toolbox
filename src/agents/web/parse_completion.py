import re

from .prompts.special_tokens import *

def completion_pattern():
    actions = '|'.join([
        f"{SECTION_ANSWER}:(?P<{SECTION_ANSWER}>[^\n]+)", 
        f"{SECTION_WEB_SEARCH}:(?P<{SECTION_WEB_SEARCH}>[^\n]+)"
    ])

    return re.compile(
        rf"{SECTION_PREVIOUS_ACTIONS}:(?P<{SECTION_PREVIOUS_ACTIONS}>[^\n]*)\n"
        rf"{SECTION_INTERNAL_THOUGHT}:(?P<{SECTION_INTERNAL_THOUGHT}>[^\n]+)\n"
        rf"{SECTION_ENOUGH_INFO}:(?P<{SECTION_ENOUGH_INFO}>yes|no)\n"
        rf"(?P<action_line>{actions})\n?"
    )

COMPETION_PATTERN = completion_pattern()

def parse_completion(completion):
    match = COMPETION_PATTERN.match(completion)

    if match:
        return match.groupdict()
    else:
        return None
