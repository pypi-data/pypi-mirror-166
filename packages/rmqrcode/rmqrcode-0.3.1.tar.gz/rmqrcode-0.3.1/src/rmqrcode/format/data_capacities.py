from .error_correction_level import ErrorCorrectionLevel

# ISO/IEC 23941:2022 Table 6
DataCapacities = {
    "R7x43": {
        "height": 7,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 48,
            ErrorCorrectionLevel.H: 24,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 5,
                ErrorCorrectionLevel.H: 2,
            },
        },
    },
    "R7x59": {
        "height": 7,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 96,
            ErrorCorrectionLevel.H: 56,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 11,
                ErrorCorrectionLevel.H: 6,
            },
        },
    },
    "R7x77": {
        "height": 7,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 160,
            ErrorCorrectionLevel.H: 80,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 19,
                ErrorCorrectionLevel.H: 9,
            },
        },
    },
    "R7x99": {
        "height": 7,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 224,
            ErrorCorrectionLevel.H: 112,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 27,
                ErrorCorrectionLevel.H: 13,
            },
        },
    },
    "R7x139": {
        "height": 7,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 352,
            ErrorCorrectionLevel.H: 192,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 42,
                ErrorCorrectionLevel.H: 22,
            },
        },
    },
    "R9x43": {
        "height": 9,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 96,
            ErrorCorrectionLevel.H: 56,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 11,
                ErrorCorrectionLevel.H: 6,
            },
        },
    },
    "R9x59": {
        "height": 9,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 168,
            ErrorCorrectionLevel.H: 88,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 20,
                ErrorCorrectionLevel.H: 10,
            },
        },
    },
    "R9x77": {
        "height": 9,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 248,
            ErrorCorrectionLevel.H: 136,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 30,
                ErrorCorrectionLevel.H: 16,
            },
        },
    },
    "R9x99": {
        "height": 9,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 336,
            ErrorCorrectionLevel.H: 176,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 40,
                ErrorCorrectionLevel.H: 20,
            },
        },
    },
    "R9x139": {
        "height": 9,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 504,
            ErrorCorrectionLevel.H: 264,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 61,
                ErrorCorrectionLevel.H: 31,
            },
        },
    },
    "R11x27": {
        "height": 11,
        "width": 27,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 56,
            ErrorCorrectionLevel.H: 40,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 6,
                ErrorCorrectionLevel.H: 4,
            },
        },
    },
    "R11x43": {
        "height": 11,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 152,
            ErrorCorrectionLevel.H: 88,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 18,
                ErrorCorrectionLevel.H: 10,
            },
        },
    },
    "R11x59": {
        "height": 11,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 248,
            ErrorCorrectionLevel.H: 120,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 30,
                ErrorCorrectionLevel.H: 14,
            },
        },
    },
    "R11x77": {
        "height": 11,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 344,
            ErrorCorrectionLevel.H: 184,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 41,
                ErrorCorrectionLevel.H: 21,
            },
        },
    },
    "R11x99": {
        "height": 11,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 456,
            ErrorCorrectionLevel.H: 232,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 55,
                ErrorCorrectionLevel.H: 27,
            },
        },
    },
    "R11x139": {
        "height": 11,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 672,
            ErrorCorrectionLevel.H: 336,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 82,
                ErrorCorrectionLevel.H: 40,
            },
        },
    },
    "R13x27": {
        "height": 13,
        "width": 27,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 96,
            ErrorCorrectionLevel.H: 56,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 11,
                ErrorCorrectionLevel.H: 6,
            },
        },
    },
    "R13x43": {
        "height": 13,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 216,
            ErrorCorrectionLevel.H: 104,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 26,
                ErrorCorrectionLevel.H: 12,
            },
        },
    },
    "R13x59": {
        "height": 13,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 304,
            ErrorCorrectionLevel.H: 160,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 36,
                ErrorCorrectionLevel.H: 18,
            },
        },
    },
    "R13x77": {
        "height": 13,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 424,
            ErrorCorrectionLevel.H: 232,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 51,
                ErrorCorrectionLevel.H: 27,
            },
        },
    },
    "R13x99": {
        "height": 13,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 584,
            ErrorCorrectionLevel.H: 280,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 71,
                ErrorCorrectionLevel.H: 33,
            },
        },
    },
    "R13x139": {
        "height": 13,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 848,
            ErrorCorrectionLevel.H: 432,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 104,
                ErrorCorrectionLevel.H: 52,
            },
        },
    },
    "R15x43": {
        "height": 15,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 264,
            ErrorCorrectionLevel.H: 120,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 31,
                ErrorCorrectionLevel.H: 13,
            },
        },
    },
    "R15x59": {
        "height": 15,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 384,
            ErrorCorrectionLevel.H: 208,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 46,
                ErrorCorrectionLevel.H: 24,
            },
        },
    },
    "R15x77": {
        "height": 15,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 536,
            ErrorCorrectionLevel.H: 248,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 65,
                ErrorCorrectionLevel.H: 29,
            },
        },
    },
    "R15x99": {
        "height": 15,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 704,
            ErrorCorrectionLevel.H: 384,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 86,
                ErrorCorrectionLevel.H: 46,
            },
        },
    },
    "R15x139": {
        "height": 15,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 1016,
            ErrorCorrectionLevel.H: 552,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 125,
                ErrorCorrectionLevel.H: 67,
            },
        },
    },
    "R17x43": {
        "height": 17,
        "width": 43,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 312,
            ErrorCorrectionLevel.H: 168,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 37,
                ErrorCorrectionLevel.H: 19,
            },
        },
    },
    "R17x59": {
        "height": 17,
        "width": 59,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 448,
            ErrorCorrectionLevel.H: 224,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 54,
                ErrorCorrectionLevel.H: 26,
            },
        },
    },
    "R17x77": {
        "height": 17,
        "width": 77,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 624,
            ErrorCorrectionLevel.H: 304,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 76,
                ErrorCorrectionLevel.H: 36,
            },
        },
    },
    "R17x99": {
        "height": 17,
        "width": 99,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 800,
            ErrorCorrectionLevel.H: 448,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 98,
                ErrorCorrectionLevel.H: 54,
            },
        },
    },
    "R17x139": {
        "height": 17,
        "width": 139,
        "number_of_data_bits": {
            ErrorCorrectionLevel.M: 1216,
            ErrorCorrectionLevel.H: 608,
        },
        "capacity": {
            "Byte": {
                ErrorCorrectionLevel.M: 150,
                ErrorCorrectionLevel.H: 74,
            },
        },
    },
}
