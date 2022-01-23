#! /usr/bin/env python
"""Output the second-lowest-cost Silver plan for each ZIP code to stdout in CSV
format.
"""

import csv
import os
import sys
from argparse import ArgumentParser
from collections import defaultdict
from typing import Dict, Iterable, List, NamedTuple, Optional, Set, Tuple


class Plan(NamedTuple):
    """Relevant attributes of a plan.

    For the purposes of this calculation we don't care about the plan ID, and
    we filter out all non-silver plans at ingestion time.
    """

    state: str
    rate_area: int
    rate: float


def _second_lowest(rates: List[float]) -> Optional[float]:
    if len(rates) < 2:
        return None
    return sorted(rates)[1]


def rates_for_areas(
    silver_plans: Iterable[Plan],
) -> Dict[Tuple[str, int], Optional[float]]:
    """For each state/rate area pair, find the second lowest cost silver plan, if it exists."""
    all_rates_for_areas = defaultdict(list)
    for plan in silver_plans:
        all_rates_for_areas[(plan.state, plan.rate_area)].append(plan.rate)

    return {
        state_area: _second_lowest(rates)
        for state_area, rates in all_rates_for_areas.items()
    }


def get_silver_plans(plans: Iterable[str]) -> Iterable[Plan]:
    return (
        Plan(row["state"], int(row["rate_area"]), float(row["rate"]))
        for row in csv.DictReader(plans)
        if row["metal_level"] == "Silver"
    )


def _only_if_unique(xs: Set):
    if len(xs) == 1:
        return xs.pop()
    return None


def rate_areas_for_zips(
    all_zips: Iterable[str],
) -> Dict[str, Optional[Tuple[str, int]]]:
    all_areas_for_zips = defaultdict(set)
    """Determine the unique rate area in a ZIP code.

    If there are none, or multiple, return None.
    """
    for r in csv.DictReader(all_zips):
        all_areas_for_zips[r["zipcode"]].add((r["state"], int(r["rate_area"])))

    return {
        zipcode: _only_if_unique(areas) for zipcode, areas in all_areas_for_zips.items()
    }


def get_rate_for_zip(
    zipcode: str,
    areas: Dict[str, Optional[Tuple[str, int]]],
    rates: Dict[Tuple[str, int], Optional[float]],
) -> Optional[str]:
    """Return the formatted rate of the second-lowest-cost Silver plan for a
    ZIP code.

    Formats to 2 decimal places and returns the empty string if there is none.
    """
    if state_area := areas.get(zipcode):
        if rate := rates.get(state_area):
            return f"{rate:.2f}"
    return ""


def slcsps(
    zips_of_interest: Iterable[str], all_plans: Iterable[str], all_zips: Iterable[str]
) -> List[Dict[str, Optional[str]]]:
    """Find the second-lowest-cost silver plan in the ZIPs of interest."""
    silver_plans = get_silver_plans(all_plans)
    rates = rates_for_areas(silver_plans)
    areas = rate_areas_for_zips(all_zips)
    return [
        {"zipcode": r["zipcode"], "rate": get_rate_for_zip(r["zipcode"], areas, rates)}
        for r in csv.DictReader(zips_of_interest)
    ]


def main(slcsp, plans, zips):
    with open(slcsp) as f:
        zips_of_interest = f.readlines()

    with open(plans) as f:
        all_plans = f.readlines()

    with open(zips) as f:
        all_zips = f.readlines()

    writer = csv.DictWriter(
        sys.stdout, fieldnames=["zipcode", "rate"], lineterminator=os.linesep
    )
    writer.writeheader()
    for r in slcsps(zips_of_interest, all_plans, all_zips):
        writer.writerow(r)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "slcsp", help="File containing ZIP codes to calculate SLCSP for."
    )
    parser.add_argument("plans", help="File containing plan information.")
    parser.add_argument("zips", help="File containing a ZIP code to rate area mapping.")
    return parser.parse_args()


if __name__ == "__main__":
    main(**vars(parse_args()))
