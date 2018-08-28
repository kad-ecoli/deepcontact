#!/usr/bin/env python
#### provide two configuration dictionaries: global_setting and feature_set ####

###This is basic configuration
global_setting=dict(
        max_len         =       256,               # max length for the dataset
        )

feature_set=dict(
ccmpred=dict(
        suffix          =       "ccmpred",
        length          =       1,
        parser_name     =       "ccmpred_parser_2d",
        type            =       "2d",
        skip            =       False,
        )
)
