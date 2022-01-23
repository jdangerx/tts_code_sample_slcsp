#! /usr/bin/env python

from unittest import TestCase, main

from slcsp import slcsps, Plan, rates_for_areas


class TestSlcsp(TestCase):
    def test_rates_for_areas(self):
        plans = [
            Plan("AZ", 1, 1.01),
            Plan("AZ", 1, 2.01),
            Plan("AZ", 1, 3.01),
            Plan("CA", 1, 10.01),
        ]
        expected = {
            ("AZ", 1): 2.01,
            ("CA", 1): None,
        }
        calculated = rates_for_areas(plans)
        self.assertEqual(calculated, expected)

    def test_slcsps(self):
        zips_of_interest = [
            "zipcode,rate",
            "00001,",
            "00002,",
            "00003,",
            "00004,",
            "00005,",
        ]

        all_zips = [
            "zipcode,state,county_code,name,rate_area",
            "00001,AZ,01001,Alameda,1",
            "00001,UT,01001,Santa Clara,1",
            "00002,AZ,01001,Alameda,2",
            "00003,AZ,01001,San Mateo,3",
            "00004,AZ,01001,Santa Cruz,4",
            "00004,AZ,01001,Santa Cruz,5",
            "00005,AZ,01001,Santa Cruz,5",
        ]

        plans = [
            "plan_id,state,metal_level,rate,rate_area",
            "00000AZ0000011,AZ,Silver,1.01,1",
            "00000AZ0000012,AZ,Silver,2.01,1",
            "00000AZ0000013,AZ,Silver,3.01,1",
            "00000UT0000011,UT,Silver,1.11,1",
            "00000UT0000012,UT,Silver,2.11,1",
            "00000UT0000013,UT,Silver,3.11,1",
            "00000AZ0000022,AZ,Silver,2.02,2",
            "00000AZ0000021,AZ,Silver,1.02,2",
            "00000AZ0000022,AZ,Gold,2.00,2",
            "00000AZ0000023,AZ,Silver,3.02,2",
            "00000AZ0000031,AZ,Silver,1.03,3",
            "00000AZ0000032,AZ,Gold,2.03,3",
            "00000AZ0000033,AZ,Gold,3.03,3",
            "00000AZ0000041,AZ,Silver,1.04,4",
            "00000AZ0000042,AZ,Silver,2.04,4",
            "00000AZ0000043,AZ,Silver,3.04,4",
        ]

        # 00001 has two rate areas in different states
        # 00002 is happy path
        # 00003 has only 1 Silver plan
        # 00004 has 2 rate areas in the same state
        # 00005 has no plans at all

        expected = [
            {"zipcode": "00001", "rate": ""},
            {"zipcode": "00002", "rate": "2.02"},
            {"zipcode": "00003", "rate": ""},
            {"zipcode": "00004", "rate": ""},
            {"zipcode": "00005", "rate": ""},
        ]

        calculated = slcsps(
            zips_of_interest=zips_of_interest, plans=plans, all_zips=all_zips
        )

        self.assertEqual(calculated, expected)


if __name__ == "__main__":
    main()
