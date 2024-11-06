import random

import pandas as pd

# Base dictionary with sample data
base_data = {
    "Weight": 28.0952381,
    "Transfer Status": "NT",
    "Fragility": "NF",
    "Length": 68.0,
    "Height": 10.812,
    "Width": 7.48,
}


# Function to generate mock data
def generate_mock_data(num_samples=100):
    mock_data = []

    for _ in range(num_samples):
        mock_data.append(
            {
                "Weight": round(random.uniform(28, 32), 1),  # Around 30 kg
                "Transfer Status": (
                    "NT" if random.random() < 0.9 else "T"
                ),  # 90% NT, 10% T
                "Fragility": random.choice(["NF", "F"]),  # NF or F
                "Length": round(random.uniform(65, 75), 1),  # Around 70 cm
                "Height": round(random.uniform(30, 40), 1),  # Around 35 cm
                "Width": round(random.uniform(35, 45), 1),  # Around 40 cm
            }
        )

    return pd.DataFrame(mock_data)


# Generate 500 mock samples
mock_data_df = generate_mock_data(200)

# Save to CSV file
output_path = "data.csv"
mock_data_df.to_csv(output_path, index=False)

print(f"Generated mock data saved to {output_path}!")
