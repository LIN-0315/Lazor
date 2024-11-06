'''
EN.640.635 Software Carpentry at JHU
Lazer Group Project
Group： Weiting Yu, Yilin Li

Lazor Game Solver - Test Suite for .bff File Parser
This script contains test cases to verify the functionality of the Lazor game .bff file parser.
It validates the parsing of grid settings, block types, laser paths, and target points.

'''
import unittest
from Lazor_parse import load_files

results = {
            "mad_1.bff": {
                "grid": [
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"]
                ],
                "blocks": {
                    "A": 2,
                    "C": 1
                },
                "lasers": [
                    (2, 7, 1, -1)
                ],
                "points": [
                    (3, 0),
                    (4, 3),
                    (2, 5),
                    (4, 7)
                ]
            },
            "dark_1.bff": {
                "grid": [
                    ["x", "o", "o"],
                    ["o", "o", "o"],
                    ["o", "o", "x"]
                ],
                "blocks": {
                    "B":3
                },
                "lasers": [
                    (3, 0, -1, 1),
                    (1,6,1,-1),
                    (3,6,-1,-1),
                    (4,3,1,-1)
                ],
                "points": [
                    (0, 3),
                    (6, 1),
                ]
            },
            "mad_4.bff": {
                "grid": [
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"],
                    ["o", "o", "o", "o"]
                ],
                "blocks": {
                    "A": 5

                },
                "lasers": [
                    (7,2,-1,1)
                ],
                "points": [
                    (3,4),
                    (7,4),
                    (5,8)
                ]
            },

            "mad_7.bff": {
                "grid": [
                    ["o", "o", "o", "o", "o"],
                    ["o", "o", "o", "o", "o"],
                    ["o", "o", "o", "o", "x"],
                    ["o", "o", "o", "o", "o"],
                    ["o", "o", "o", "o", "o"]
                ],
                "blocks": {
                    "A": 6

                },
                "lasers": [
                    (2,1,1,1),
                    (9,4,-1,1)
                ],
                "points": [
                    (6,3),
                    (6,5),
                    (6,7),
                    (2,9),
                    (9,6)
                ]
            },

            "numbered_6.bff": {
                "grid": [
                    ["o", "o", "o"],
                    ["o", "x", "x"],
                    ["o", "o", "o"],
                    ["o", "x", "o"],
                    ["o", "o", "o"]
                ],
                "blocks": {
                    "A": 3,
                    "B": 3
                },
                "lasers": [
                    (4,9,-1,-1),
                    (6,9,-1,-1)
                ],
                "points": [
                    (2,5),
                    (5,0)
                ]
            },

            "showstopper_4.bff": {
                "grid": [
                    ["B", "o", "o"],
                    ["o", "o", "o"],
                    ["o", "o", "o"],
                ],
                "blocks": {
                    "A": 3,
                    "B": 3
                },
                "lasers": [
                    (3,6,-1,-1)
                ],
                "points": [
                    (2,3)
                ]
            },

            "tiny_5.bff": {
                "grid": [
                    ["o", "B", "o"],
                    ["o", "o", "o"],
                    ["o", "o", "o"],
                ],
                "blocks": {
                    "A": 3,
                    "C": 1
                },
                "lasers": [
                    (4,5,-1,-1)
                ],
                "points": [
                    (1, 2),
                    (6, 3)
                ]
            },

            "yarn_5.bff": {
                "grid": [
                    ["o", "B", "x", "o", "o"],
                    ["o", "o", "o", "o", "o"],
                    ["o", "x", "o", "o", "o"],
                    ["o", "x", "o", "o", "x"],
                    ["o", "o", "x", "x", "o"],
                    ["B", "o", "x", "o", "o"]
                ],
                "blocks": {
                    "A": 8

                },
                "lasers": [
                    (4, 1, 1, 1)
                ],
                "points": [
                    (6, 9),
                    (9, 2)
                ]
            },

        }


class TestBFFParser(unittest.TestCase):
    '''
    Test function test_parse_bff.
    '''
    def test_parse_bff(self):
        bff_files = [
            "mad_1.bff",
            "dark_1.bff",
            "mad_4.bff",
            "mad_7.bff",
            "numbered_6.bff",
            "showstopper_4.bff",
            "tiny_5.bff",
            "yarn_5.bff"
        ]

        parsed_files = load_files(bff_files)

        for filename, data in results.items():
            with self.subTest(filename=filename):
                parsed_data = parsed_files.get(filename, {})
    # Verify the parsed data against expected values
                self.assertEqual(parsed_data.get("grid"), data["grid"], f"Grid mismatch {filename}")
    # Verify the parsed data against expected values
                self.assertEqual(parsed_data.get("blocks"), data["blocks"], f"Blocks mismatch {filename}")
    # Verify the parsed data against expected values
                self.assertEqual(parsed_data.get("lasers"), data["lasers"], f"Lasers mismatch {filename}")
    # Verify the parsed data against expected values
                self.assertEqual(parsed_data.get("points"), data["points"], f"Points mismatch {filename}")


if __name__ == "__main__":
    unittest.main()
