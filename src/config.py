import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    form_url: str
    delay_between_submissions: float = 2.0
    max_retries: int = 3
    request_timeout: int = 30

    @classmethod
    def from_environment(cls) -> "Config":

        form_url = os.getenv("FORM_URL")

        if not form_url:
            raise ValueError(
                "FORM_URL environment variable is not set."
            )

        return cls(
            form_url=form_url,
            delay_between_submissions=2.0,
            max_retries=3,
            request_timeout=30,
        )