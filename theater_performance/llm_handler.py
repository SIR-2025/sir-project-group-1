from dotenv import load_dotenv
from os import environ
from sic_framework.services.openai_gpt.gpt import (
    GPT,
    GPTConf,
    GPTRequest
)

from theater_performance.config import (
    LLM_MODEL,
    LLM_TEMP,
    LLM_MAX_TOKENS
)


class LLMHandler:
    """Handles GPT fallback responses for improvisation."""

    def __init__(self, logger=None):
        self.logger = logger

        load_dotenv(".env")
        api_key = environ.get("OPENAI_API_KEY")

        conf = GPTConf(
            openai_key=api_key,
            system_message="You are NAO the robot in a theatre show. Respond with short dry humor.",
            model=LLM_MODEL,
            temp=LLM_TEMP,
            max_tokens=LLM_MAX_TOKENS
        )

        self.gpt = GPT(conf=conf)
        self.context = []

    def generate(self, state, user_input):
        prompt = f"""
State: {state}
Context: {self.context[-2:] if self.context else 'None'}
Human: "{user_input}"
Respond as NAO:
"""

        reply = self.gpt.request(GPTRequest(input=prompt, context_messages=[]))
        text = reply.response.strip()

        if self.logger:
            self.logger.info(f"LLM reply: {text}")

        self.context.append(f"Human: {user_input}")
        self.context.append(f"NAO: {text}")
        self.context = self.context[-4:]

        return text
