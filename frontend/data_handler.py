import random
import faker
from datetime import datetime, timedelta

class DataHandler:
    @staticmethod
    def get_data(tool_name):
        """Simulates fetching CSV data with a large set of randomly generated data."""
        fake = faker.Faker()

        # Generate random dates within the last 2 years
        def random_date():
            start_date = datetime.now() - timedelta(days=730)  # 2 years ago
            random_days = random.randint(0, 730)
            return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

        # Generate large dummy data for each tool
        fake_data = {
            "Tool A": [
                [fake.name(), random.randint(20, 60), fake.job(), random_date()] for _ in range(50)
            ],
            "Tool B": [
                [fake.city(), random.randint(1000000, 20000000), fake.country(), random_date()] for _ in range(50)
            ],
            "Tool C": [
                [fake.bs(), random.choice(["Low", "Medium", "High"]), random.randint(1980, 2025), random_date()] for _ in range(50)
            ],
        }

        return fake_data.get(tool_name, [["No Data", "", "", ""]])  # Default if no data
