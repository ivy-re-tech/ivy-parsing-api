import json
from unittest import TestCase

from address import multiparse


class MultiParseTests(TestCase):
    def test_vanilla_cases(self):
        """test some random vanilla cases"""
        case = "123 Main St"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "123")
        self.assertEqual(output["street_name"], "Main")
        self.assertEqual(output["street_name_post_type"], "St")

        case = "123 Main St Unit 12"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "123")
        self.assertEqual(output["street_name"], "Main")
        self.assertEqual(output["street_name_post_type"], "St")
        self.assertEqual(output["occupancy_type"], "Unit")
        self.assertEqual(output["occupancy_identifier"], "12")

        case = "123 NE Main St"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "123")
        self.assertEqual(output["street_name_pre_directional"], "NE")
        self.assertEqual(output["street_name"], "Main")
        self.assertEqual(output["street_name_post_type"], "St")

        case = "123 Main St NE"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "123")
        self.assertEqual(output["street_name"], "Main")
        self.assertEqual(output["street_name_post_directional"], "NE")
        self.assertEqual(output["street_name_post_type"], "St")

    def test_weird_queens_address(self):
        """test an address with a dash in it"""
        case = "99-47 Davenport Court"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "99-47")
        self.assertEqual(output["street_name"], "Davenport")
        self.assertEqual(output["street_name_post_type"], "Court")

    def test_full_address(self):
        """test a full address"""
        case = "4302 72nd Ave W, University Place, WA 98466"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Street Address")
        self.assertEqual(output["address_number"], "4302")
        self.assertEqual(output["street_name"], "72nd")
        self.assertEqual(output["street_name_post_type"], "Ave")
        self.assertEqual(output["street_name_post_directional"], "W")
        self.assertIsNone(output["address_number_suffix"])
        self.assertIsNone(output["street_name_pre_modifier"])
        self.assertIsNone(output["street_name_pre_directional"])
        self.assertIsNone(output["street_name_pre_type"])

    def test_po_box(self):
        """test that a PO Box returns proper info"""
        case = "po box 23984, phoenix az"
        output = multiparse(case)
        self.assertEqual(output["input_type"], "Po Box")
        self.assertEqual(output["usps_box_type"], "Po Box")
        self.assertEqual(output["usps_box_id"], "23984")
        self.assertEqual(output["place_name"], "Phoenix")
        self.assertEqual(output["state_name"], "AZ")

    def test_full_obj(self):
        """check that a full returned object matches our expectations"""
        case = "123 E Main Vine St NE Apt C Gig Harbor WA 98406"
        output = multiparse(case)
        with open("full_object.json") as f:
            sample = json.load(f)
        self.assertEqual(output, sample)
