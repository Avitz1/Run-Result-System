import random
import faker

class DataHandler:
    @staticmethod
    def get_data(tool_name):
        """Simulates fetching CSV data with a large set of randomly generated data."""
        fake = faker.Faker()

        # Generate large dummy data for each tool
        fake_data = {
            "Tool A": [
                [fake.name(), random.randint(20, 60), fake.job()] for _ in range(50)  # 50 random entries for Tool A
            ],
            "Tool B": [
                [fake.city(), random.randint(1000000, 20000000), fake.country()] for _ in range(50)  # 50 random city data
            ],
            "Tool C": [
                [fake.bs(), random.choice(["Low", "Medium", "High"]), random.randint(1980, 2025)] for _ in range(50)  # 50 random programming languages
            ],
        }

        return fake_data.get(tool_name, [["No Data", "", ""]])  # Default if no data
