from .config import Config
from .forms_client import MicrosoftFormsClient
from .food_service import MonthlyFoodService


def main() -> None:

    config = Config.from_environment()

    client = MicrosoftFormsClient(
        config
    )

    food_service = MonthlyFoodService(
        client,
        config,
    )

    food_service.run()


if __name__ == "__main__":
    main()