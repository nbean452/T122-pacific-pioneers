import json
import math
from statistics import mean

import pandas as pd

# unit in m^3
FRONT_SECTION_VOLUME = 13.28
REAR_SECTION_VOLUME = 24.14

AVAILABLE_CARGO_VOLUME = FRONT_SECTION_VOLUME + REAR_SECTION_VOLUME

FRONT_SECTION_RATIO = FRONT_SECTION_VOLUME / AVAILABLE_CARGO_VOLUME
REAR_SECTION_RATIO = REAR_SECTION_VOLUME / AVAILABLE_CARGO_VOLUME

# unit in m
# BULK_COMPARTMENT_WIDTH = 0.81
CARGO_COMPARTMENT_WIDTH = 1.82

# BULK_HEIGHT = 0.95
CARGO_HEIGHT = 1.823
CARGO_LENGTH = 14.75

ADJUSTMENT_RATIO = 0.29

# adjust the ratio a bit for easier calculation
ADJUSTED_FRONT_SECTION_VOLUME = (
    FRONT_SECTION_RATIO + ADJUSTMENT_RATIO
) * AVAILABLE_CARGO_VOLUME
ADJUSTED_REAR_SECTION_VOLUME = (
    REAR_SECTION_RATIO - ADJUSTMENT_RATIO
) * AVAILABLE_CARGO_VOLUME

print(ADJUSTED_FRONT_SECTION_VOLUME + ADJUSTED_REAR_SECTION_VOLUME)

SECTION_VOLUMES = [
    FRONT_SECTION_VOLUME,
    REAR_SECTION_VOLUME,
]
NO_OF_BAGGAGE_SECTIONS = 2

# order of baggages
# 1. Heavy first section
# 2. Light first section (Medium)
# 3. Light second section (Lightest)
# 4. Heavy second section (Medium)
# 5. Transfer bags


def main():

    csv_path = "./data.csv"

    df = pd.read_csv(csv_path)

    baggages: list[dict] = df.to_dict("records")

    transfer_baggages = []
    non_transfer_baggages = []

    cumulative_volumes = []

    all_sorted_baggages = sorted(
        baggages,
        key=lambda x: (x["Weight"], x["Fragility"] == "NF"),
    )

    # iterate over all baggages
    for baggage in all_sorted_baggages:
        if baggage["Transfer Status"] == "T":
            transfer_baggages.append(baggage)
        else:
            non_transfer_baggages.append(baggage)

    print(f"length of non-transfer baggages: {len(non_transfer_baggages)}")

    section_index = 0
    baggage_sections = [[] for _ in range(NO_OF_BAGGAGE_SECTIONS)]

    baggage_lengths = [baggage["Length"] for baggage in all_sorted_baggages]
    average_baggage_length = mean(baggage_lengths)

    # cumulative_volume = 0
    # for baggage_index in range(len(non_transfer_baggages)):
    #     baggage = non_transfer_baggages[baggage_index]
    #
    #     baggage_volume = (
    #         baggage["Width"] * baggage["Length"] * baggage["Height"]
    #     ) / math.pow(100, 3)
    #     current_volume = cumulative_volume + baggage_volume
    #
    #     if current_volume > SECTION_VOLUMES[section_index]:
    #         cumulative_volumes.append(cumulative_volume)
    #
    #         section_index += 1
    #         cumulative_volume = 0
    #         current_volume = baggage_volume
    #
    #     baggage_section_copy = baggage_sections[section_index].copy()
    #     baggage_section_copy.append(baggage)
    #
    #     baggage_sections[section_index] = baggage_section_copy
    #     cumulative_volume = current_volume
    #
    # cumulative_volumes.append(cumulative_volume)

    front_section_baggages, rear_section_baggages = baggage_sections

    no_of_front_sub_sections = math.ceil(CARGO_LENGTH / average_baggage_length)
    front_sub_sections = [[] for _ in range(no_of_front_sub_sections)]

    print(len(front_sub_sections))

    sorted_transfer_baggages = sorted(
        transfer_baggages,
        key=lambda x: (x["Weight"], x["Fragility"] == "F"),
    )

    rear_section_baggages += sorted_transfer_baggages

    print(
        json.dumps(
            rear_section_baggages,
            indent=2,
        )
    )

    # with open("./output-new.json", "w") as file:
    #     json.dump(
    #         {
    #             "front_section": {
    #                 "volume_available": SECTION_VOLUMES[0],
    #                 "volume_used": cumulative_volumes[0],
    #                 "items": front_section_baggages,
    #             },
    #             "rear_section": {
    #                 "volume_available": SECTION_VOLUMES[1],
    #                 "volume_used": cumulative_volumes[1],
    #                 "items": rear_section_baggages,
    #             },
    #         },
    #         file,
    #         indent=2,
    #     )


if __name__ == "__main__":
    main()
