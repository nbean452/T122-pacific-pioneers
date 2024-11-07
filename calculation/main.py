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
CARGO_COMPARTMENT_WIDTH = 1.82
CARGO_HEIGHT = 1.823
CARGO_LENGTH = 14.75

# Adjusted section volumes (this issue will be explained more during pitching)
ADJUSTMENT_RATIO = 0.29
ADJUSTED_FRONT_SECTION_VOLUME = (
    FRONT_SECTION_RATIO + ADJUSTMENT_RATIO
) * AVAILABLE_CARGO_VOLUME
ADJUSTED_REAR_SECTION_VOLUME = (
    REAR_SECTION_RATIO - ADJUSTMENT_RATIO
) * AVAILABLE_CARGO_VOLUME

SECTION_VOLUMES = [
    FRONT_SECTION_VOLUME,
    REAR_SECTION_VOLUME,
]
NO_OF_BAGGAGE_SECTIONS = 2


def distribute_baggages(baggages, subsections, max_volume, index=0) -> int:
    """
    Distribute baggages into sub-sections based on their volume and sub-section limits.
    Returns an index that can be used to continue from the last operation
    """

    for baggage in baggages:
        baggage_volume = (
            baggage["Width"] * baggage["Length"] * baggage["Height"]
        ) / 1_000_000  # Convert from cm^3 to m^3

        for subsection in subsections:
            subsection_volume = sum(
                (b["Width"] * b["Length"] * b["Height"]) / 1_000_000 for b in subsection
            )

            if subsection_volume + baggage_volume <= max_volume / len(subsections):
                subsection.append(baggage)
                index += 1
                break

    return index


def main():

    csv_path = "./data.csv"

    df = pd.read_csv(csv_path)

    baggages: list[dict] = df.to_dict("records")

    # init variables to filter baggages for transfer and non-transfer
    transfer_baggages = []
    non_transfer_baggages = []

    # sort the list based on weight and if the baggage is fragile
    all_sorted_baggages = sorted(
        baggages,
        key=lambda x: (x["Weight"], x["Fragility"] == "NF"),
    )

    # Separate transfer and non-transfer baggages
    for baggage in all_sorted_baggages:
        if baggage["Transfer Status"] == "T":
            transfer_baggages.append(baggage)
        else:
            non_transfer_baggages.append(baggage)

    # get average baggage length
    baggage_lengths = [baggage["Length"] for baggage in all_sorted_baggages]
    average_baggage_length = mean(baggage_lengths) / 100

    # get the number of sub-sections in the front cargo section
    no_of_front_sub_sections = math.ceil(
        CARGO_LENGTH * FRONT_SECTION_RATIO / average_baggage_length
    )

    front_sub_sections = [[] for _ in range(no_of_front_sub_sections)]

    # same thing but with rear cargo section (AFT + BULK CARGO)
    no_of_rear_sub_sections = math.ceil(
        CARGO_LENGTH * REAR_SECTION_RATIO / average_baggage_length
    )
    rear_sub_sections = [[] for _ in range(no_of_rear_sub_sections)]

    # Distribute non-transfer baggages into front section
    last_index = distribute_baggages(
        # non_transfer_baggages[: len(non_transfer_baggages) // 2],  # Heaviest to front
        non_transfer_baggages,  # Heaviest to front
        front_sub_sections,
        ADJUSTED_FRONT_SECTION_VOLUME,
    )

    # Distribute non-transfer and transfer baggages into rear section
    sorted_transfer_baggages = sorted(
        transfer_baggages,
        key=lambda x: (x["Weight"], x["Fragility"] == "F"),
    )

    # baggages for transfers are always put last,
    # so that when the baggages are placed,
    # they are placed near the cargo door, for easy access
    rear_section_baggages = (
        non_transfer_baggages[last_index:] + sorted_transfer_baggages
    )

    # distribute baggage starting from the last index, if there's no more baggages,
    # then this function won't do anything
    distribute_baggages(
        rear_section_baggages,
        rear_sub_sections,
        ADJUSTED_REAR_SECTION_VOLUME,
    )

    print("=" * 20)
    print(f"Number of baggages for transfer: {len(transfer_baggages)}")

    print("=" * 20)
    print("Front Section (FWD)")
    print("=" * 20)

    sum_of_baggages = 0
    for last_index, front_sub_section in enumerate(front_sub_sections):
        print(f"sub-section {last_index+1}: {len(front_sub_section)} baggage")
        sum_of_baggages += len(front_sub_section)

    print("=" * 20)
    print("Rear Section (AFT + Cargo)")
    print("=" * 20)
    for last_index, rear_sub_section in enumerate(rear_sub_sections):
        print(f"sub-section {last_index+1}: {len(rear_sub_section)} baggage")
        sum_of_baggages += len(rear_sub_section)

    print("=" * 20)
    print(f"Loaded Baggages: {sum_of_baggages} baggages")


if __name__ == "__main__":
    main()
