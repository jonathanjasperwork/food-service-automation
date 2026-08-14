import json
import time
from datetime import datetime, timezone

import requests

from .config import Config


class MicrosoftFormsClient:

    RETRY_STATUS_CODES = {
        429,
        500,
        502,
        503,
        504,
    }

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()

    def submit(
        self,
        answers: list[dict],
    ) -> bool:

        now = datetime.now(
            timezone.utc
        ).isoformat(
            timespec="milliseconds"
        ).replace("+00:00", "Z")

        payload = {
            "answers": json.dumps(answers),
            "startDate": now,
            "submitDate": now,
        }

        for attempt in range(
            self.config.max_retries + 1
        ):

            try:

                response = self.session.post(
                    self.config.form_url,
                    json=payload,
                    timeout=self.config.request_timeout,
                )

                if response.status_code == 201:
                    return True

                if (
                    response.status_code
                    in self.RETRY_STATUS_CODES
                ):

                    if attempt < self.config.max_retries:

                        wait_time = 2 ** attempt

                        print(
                            f"Temporary error "
                            f"{response.status_code}. "
                            f"Retrying in {wait_time}s..."
                        )

                        time.sleep(wait_time)
                        continue

                    print(
                        "Maximum retries reached."
                    )

                    return False

                print(
                    f"Request failed: "
                    f"{response.status_code}"
                )

                print(response.text)

                return False

            except requests.RequestException as error:

                if attempt < self.config.max_retries:

                    wait_time = 2 ** attempt

                    print(
                        f"Network error: {error}"
                    )

                    print(
                        f"Retrying in {wait_time}s..."
                    )

                    time.sleep(wait_time)

                else:

                    print(
                        f"Request failed after "
                        f"{self.config.max_retries + 1} attempts: "
                        f"{error}"
                    )

                    return False

        return False