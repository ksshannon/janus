#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22, 2019

@author: Kendra Kaiser

Read in GCAM-USA output, convert to categories used in this instance for profit signal generation
"""

import numpy as np
import sys
import pandas as pd
from scipy.stats import linregress


def main(argv):
    """Description

    :param argv: Array of 5 command line arguments passed from the __main__ function
    :param argv[0]: Name of this function (convert_GCAM-USA_prices)
    :param argv[1]: Number of crops to create profit time series for
    :param argv[2]: Number of time steps in the time series
    :param argv[3]: Name of CSV file with GCAM-USA outputs including path if CSV file is in a different directory
    :param argv[4]: Name of CSV file to which profit time series will be written, including path to output if in
    a different directory than the script
    :param argv[5]: Start year of model run
    :param argv[6]: Name of key file including path if not in directory
    :param argv[7]: Resolution of model in km
    :return: null (output written to file)
    """

    if len(argv) != 7:
        print('\nERROR: Incorrect number of command line arguments\n')
        print(
            'Usage: convert_GCAM-USA_prices.py <no. crops> <no. time steps> <Input CSV file> <Output CSV file> <Key file> <Resolution km>\n')
        print('\tconvert_gcamland_prices.py   = Name of this python script')
        print('\t<no. crops>                  = Number of crops to synthesize prices for')
        print('\t<no. time steps>             = Number of time steps to generate prices for')
        print('\t<CSV file>                   = CSV file containing crop information')
        print('\t                               (see documentation)')
        print('\t<Output CSV file>            = CSV file in which to save output prices')
        print('\t<start year                  = Year that Janus is initiated')
        print('\t<Key file>                   = Key file that contains conversions between GCAM and janus\n')
        sys.exit()

    nc = int(argv[1])
    nt = int(argv[2])
    CropFileIn = argv[3]
    CropFileOut = argv[4]
    year = argv[5]
    key_file = argv[6]
    res = argv[7]

    # Error traps
    assert nc > 0, 'convert_GCAM-USA_prices.py ERROR: Negative number of crops encountered'
    assert nt > 0, 'convert_GCAM-USA_prices.py ERROR: Negative number of time steps encountered'
    assert nc <= 28, 'convert_GCAM-USA_prices.py ERROR: Too many crops encountered'

    # function to find nearest value
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    # read input data
    gcam_dat = pd.read_csv(CropFileIn)
    key = pd.read_csv(key_file)

    # parse input data
    crop_names = gcam_dat.sector.unique()
    valid_crops = np.where(key['GCAM_USA_price_id'].notna())  # GCAM-USA LU categories with crop prices
    gcam_usa_names = key['GCAM_USA_price_id'][
        valid_crops[0]]  # crop categories from GCAM-USA to use for SRB crop prices
    srb_ids = key['local_GCAM_id_list'][valid_crops[0]]

    # TODO fix this assert, need to drop crops that aren't in the SRB
    #assert all(np.sort(gcam_usa_names.unique()) == np.sort(crop_names)), 'convert_GCAM-USA_prices.py ERROR: Crop ' \
                                                                         #'names from GCAM-USA do not match keyfile'

    # find start and end years from gcam data
    int_col = np.where(gcam_dat.columns == str(year))[0][0]
    end_yr = find_nearest(gcam_dat.columns[3:-1].astype(int), (year + nt))
    end_col = np.where(gcam_dat.columns == str(end_yr))[0][0]
    years = np.arange(year, end_yr + 1)

    # setup output array
    out = np.zeros([nt + 1, len(valid_crops[0])])
    out[0, :] = np.transpose(srb_ids)

    # Create linear regressions between each timestep
    for c in np.arange(len(valid_crops[0])):
        yrs = gcam_dat.columns[int_col: end_col+1].astype(int)
        prices_usa = gcam_dat[gcam_dat['region'] == 'USA']
        prices = prices_usa.iloc[:, int_col:(end_col+1)]
    # TODO fix the linear regressions - it should be linear between each set of points, not through the entire timeseries
        # create regression based off of GCAM data
        m, b, r_val, p_val, stderr = linregress(yrs, prices.iloc[c, :])
        # predict prices for every year
        price_pred = m * years + b
        # find corresponding SRB crop to place prices in outfile
        gcam_srb_idx = np.where(gcam_usa_names == crop_names[c])[0][0]
        out[1:, gcam_srb_idx] = np.transpose(price_pred)

    if out.shape[1] != nc:
        print('\nERROR: Mismatch in number of crops read and provided as input\n')
        print(str(nc) + ' crops were expected, ' + str(out.shape[1]) + ' were read. Check key file\n')
        sys.exit()

    # TODO: fix the warning here
    with open(CropFileOut, 'w') as fp:
        np.savetxt(fp, out, delimiter=',', fmt='%.2f')
        fp.close()


if __name__ == "__main__":
    main(sys.argv)