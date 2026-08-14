import time
from calendar import monthrange
from datetime import date

from dateutil.relativedelta import relativedelta

from .config import Config
from .forms_client import MicrosoftFormsClient


class MonthlyFoodService:

    def __init__(
        self,
        client: MicrosoftFormsClient,
        config: Config,
    ):
        self.client = client
        self.config = config

    @staticmethod
    def get_next_month() -> tuple[int, int]:

        today = date.today()
        next_month = today + relativedelta(
            months=1
        )

        return (
            next_month.year,
            next_month.month,
        )

    @staticmethod
    def build_answers(
        form_date: str,
    ) -> list[dict]:

        return [
            {
                "questionId": (
                    "r5ffcad8cf9794bccaab734ff955103ac"
                ),
                "answer1": "Vendor / Outsource ",
            },
            {
                "questionId": (
                    "r3a7ed5d90c384768ab477b6aa0e3bc70"
                ),
                "answer1": "TA-00-0000",
            },
            {
                "questionId": (
                    "ree13016a8bed435b8a7308f7ee573579"
                ),
                "answer1": "Jonathan Jasper",
            },
            {
                "questionId": (
                    "r2102ed713fe24240b0c549114099ae3e"
                ),
                "answer1": "ICT",
            },
            {
                "questionId": (
                    "r7353b393f567467999edd15d4d800a35"
                ),
                "answer1": form_date,
            },
        ]

    def run(self) -> None:

        year, month = self.get_next_month()

        days = monthrange(
            year,
            month,
        )[1]

        print("=" * 60)
        print("MONTHLY FOOD SERVICE")
        print("=" * 60)
        print(
            f"Target month: "
            f"{year}-{month:02d}"
        )
        print(f"Days: {days}")
        print("=" * 60)

        successful = []
        failed = []

        for day in range(1, days + 1):

            form_date = date(
                year,
                month,
                day,
            ).isoformat()

            print(
                f"[{day:02d}/{days:02d}] "
                f"{form_date}"
            )

            answers = self.build_answers(
                form_date
            )

            success = self.client.submit(
                answers
            )

            if success:
                print("    ✓ Submitted")
                successful.append(form_date)

            else:
                print("    ✗ Failed")
                failed.append(form_date)

            if day < days:
                time.sleep(
                    self.config
                    .delay_between_submissions
                )

        self.print_summary(
            year,
            month,
            successful,
            failed,
        )

    @staticmethod
    def print_summary(
        year: int,
        month: int,
        successful: list[str],
        failed: list[str],
    ) -> None:

        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)

        print(
            f"Month: "
            f"{year}-{month:02d}"
        )

        print(
            f"Successful: "
            f"{len(successful)}"
        )

        print(
            f"Failed: "
            f"{len(failed)}"
        )

        if failed:

            print()
            print("Failed dates:")

            for form_date in failed:
                print(f"  - {form_date}")

        else:

            print()
            print(
                "✓ All submissions completed."
            )