#!/usr/bin/env python3
"""
============================================================
NOVA-X Rate Limit Manager v1.0
============================================================

Centralized retry logic for API calls.

Features
--------
• Exponential backoff
• Configurable retries
• Configurable token budget
• Friendly status messages

Douglas Davis & OpenAI
============================================================
"""

import time


class RateLimitManager:

    def __init__(
        self,
        max_input_tokens=2000,
        max_output_tokens=512,
        max_retries=5,
        base_delay=2,
    ):

        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.max_retries = max_retries
        self.base_delay = base_delay

    def token_settings(self):

        return {
            "max_input_tokens": self.max_input_tokens,
            "max_output_tokens": self.max_output_tokens,
        }

    def execute(self, api_function, *args, **kwargs):

        delay = self.base_delay

        for attempt in range(1, self.max_retries + 1):

            try:

                print(f"[RateLimit] Attempt {attempt}")

                return api_function(*args, **kwargs)

            except Exception as e:

                message = str(e).lower()

                if "429" in message or "rate limit" in message:

                    print(
                        f"[RateLimit] Rate limited. "
                        f"Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)

                    delay *= 2

                    continue

                raise

        raise RuntimeError(
            "Maximum retry attempts exceeded."
        )


############################################################
# Demo
############################################################

if __name__ == "__main__":

    manager = RateLimitManager()

    print()

    print("=" * 60)
    print("TOKEN SETTINGS")
    print("=" * 60)

    print(manager.token_settings())

    print()

    counter = {"count": 0}

    def fake_api():

        counter["count"] += 1

        if counter["count"] < 3:

            raise Exception("429 Rate Limit")

        return "API call succeeded!"

    result = manager.execute(fake_api)

    print()

    print("Result:", result)

