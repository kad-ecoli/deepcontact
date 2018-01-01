#!/usr/bin/env python
#### provide two configuration dictionaries: global_setting and feature_set ####

###This is basic configuration
global_setting=dict(
        max_len         =       256, # max length for the dataset
        )

feature_set=dict(
ccmpred=dict(
        suffix          =       "ccmpred",
        length          =       1,
        parser_name     =       "ccmpred_parser_2d",
        type            =       "2d",
        skip            =       False,
        ),

# secondary structure
ss2=dict(
        suffix          =       "ss2",
        length          =       3,
        parser_name     =       "ss2_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),

# whether is on surface
solv=dict(
        suffix          =       "solv",
        length          =       1,
        parser_name     =       "solv_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),

# colstats
colstats=dict(
        suffix          =       "colstats",
        length          =       22,
        parser_name     =       "colstats_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),

#pairwise conatct features
pairstats=dict(
        suffix          =       "pairstats",
        length          =       3,
        parser_name     =       "pairstats_parser_2d",
        type            =       "2d",
        skip            =       False,
        ),

# EVFold output
evfold=dict(
        suffix          =       "evfold",
        length          =       1,
        parser_name     =       "evfold_parser_2d",
        type            =       "2d",
        skip            =       False,
        ),

# NEFF Count
neff=dict(
        suffix          =       "hhmake",
        length          =       1,
        parser_name     =       "neff_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),

# STD-DEV of CCMPRED output
ccmpred_std=dict(
        suffix          =       "ccmpred",
        length          =       1,
        parser_name     =       "ccmpred_std_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),

# STD_DEV of EVfold output
evfold_std=dict(
        suffix          =       "evfold",
        length          =       1,
        parser_name     =       "evfold_std_parser_1d",
        type            =       "1d",
        skip            =       False,
        ),
)
