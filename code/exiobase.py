# -*- coding: utf-8 -*-
""" Parsing and processing scripts for EXIOBASE v3.



    Copyright (c) 2019 Bertram F. de Boer

    Bertram F. de Boer
    Faculty of Science
    Institute of Environmental Sciences (CML)
    Department of Industrial Ecology
    Einsteinweg 2
    2333 CC Leiden
    The Netherlands

    +31 (0)71 527 1478
    b.f.de.boer@cml.leidenuniv.nl

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""
import csv
import os

import numpy as np
import pandas as pd

import cfg
import utils as ut


def get_cf(file_path, df_cq):
    """ Extract characterization factors of footprints from DataFrame

        Parameters:
        -----------
        file_path: string with path to file containing names of footprints
        df_cQ: DataFrame with characterization factors

    """
    list_imp = []
    with open(file_path) as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row in csv_file:
            list_imp.append(tuple(row))
    return df_cq.loc[list_imp]


def get_dict_cf(dict_eb):
    """ Generate dictionary with characterization factors for footprints

        Parameters:
        dict_eb: dictionary with processed version of EXIOBASE.

        Returns:
        dict_cf: dictionary with DataFrames of characterization factors.

    """
    dict_cf = {}
    dict_cf['e'] = get_cf(cfg.INPUT_DIR_PATH+cfg.E_FP_FILE_NAME,
                          dict_eb['cQe'])
    dict_cf['m'] = get_cf(cfg.INPUT_DIR_PATH+cfg.M_FP_FILE_NAME,
                          dict_eb['cQm'])
    dict_cf['r'] = get_cf(cfg.INPUT_DIR_PATH+cfg.R_FP_FILE_NAME,
                          dict_eb['cQr'])
    dict_cf['v'] = get_cf(cfg.INPUT_DIR_PATH+cfg.V_FP_FILE_NAME,
                          dict_eb['cV'])
    return dict_cf


def get_dict_eb_parse_meta():
    """ Get dictionary with meta data for parsing of EXIOBASE.

    """

    dict_eb_parse_meta = {}
    dict_eb_parse_meta['table'] = {}
    dict_eb_parse_meta['table']['tZ'] = {}
    dict_eb_parse_meta['table']['tY'] = {}
    dict_eb_parse_meta['table']['tRe'] = {}
    dict_eb_parse_meta['table']['tRm'] = {}
    dict_eb_parse_meta['table']['tRr'] = {}
    dict_eb_parse_meta['table']['tHe'] = {}
    dict_eb_parse_meta['table']['tHm'] = {}
    dict_eb_parse_meta['table']['tHr'] = {}
    dict_eb_parse_meta['table']['tV'] = {}

    dict_eb_parse_meta['table']['tZ']['file_name_pattern'] = 'mrIot'
    dict_eb_parse_meta['table']['tY']['file_name_pattern'] = 'mrFinalDemand'
    dict_eb_parse_meta['table']['tRe']['file_name_pattern'] = 'mrEmission'
    dict_eb_parse_meta['table']['tRm']['file_name_pattern'] = 'mrMaterial'
    dict_eb_parse_meta['table']['tRr']['file_name_pattern'] = 'mrResource'
    dict_eb_parse_meta['table']['tHe']['file_name_pattern'] = 'mrFDEmission'
    dict_eb_parse_meta['table']['tHm']['file_name_pattern'] = 'mrFDMaterial'
    dict_eb_parse_meta['table']['tHr']['file_name_pattern'] = 'mrFDResource'
    dict_eb_parse_meta['table']['tV']['file_name_pattern'] = 'mrFactorInput'

    dict_eb_parse_meta['table']['tZ']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tY']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tRe']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tRm']['index_col'] = [0, 1]
    dict_eb_parse_meta['table']['tRr']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tHe']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tHm']['index_col'] = [0, 1]
    dict_eb_parse_meta['table']['tHr']['index_col'] = [0, 1, 2]
    dict_eb_parse_meta['table']['tV']['index_col'] = [0, 1]

    dict_eb_parse_meta['table']['tZ']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tY']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tRe']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tRm']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tRr']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tHe']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tHm']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tHr']['header'] = [0, 1]
    dict_eb_parse_meta['table']['tV']['header'] = [0, 1]

    return dict_eb_parse_meta


def fill_unit(df_source, df_target):
    ''' Fill units in stressor data.

    '''
    list_df_source_column_values = list(df_source.columns.values)
    list_df_target_index_values = list(df_target.index.values)
    list_df_target_index_values_new = []
    for index_id, index in enumerate(list_df_target_index_values):
        unit = index[-1]
        if pd.isnull(unit):
            unit = list_df_source_column_values[index_id][-1]
        list_index = list(index)
        list_index[-1] = unit
        tuple_index = tuple(list_index)
        list_df_target_index_values_new.append(tuple_index)
    df_target.index = list_df_target_index_values_new
    return df_target


def parse():
    """ Parse EXIOBASE.

    """

    ut.log('Parsing EXIOBASE')
    dict_eb_parse_meta = get_dict_eb_parse_meta()
    dict_eb_raw = {}

    # Get file names of exiobase.
    list_eb_file_name = os.listdir(cfg.EB_DIR_PATH)

    # Pattern match file names to fill dictionary with raw exiobase data.
    for eb_file_name in list_eb_file_name:
        for table in dict_eb_parse_meta['table']:
            if dict_eb_parse_meta['table'][table]['file_name_pattern'] in (
                    eb_file_name):
                eb_file_path = cfg.EB_DIR_PATH+eb_file_name
                dict_eb_raw[table] = pd.read_csv(
                    eb_file_path,
                    sep='\t',
                    header=dict_eb_parse_meta['table'][table]['header'],
                    index_col=dict_eb_parse_meta['table'][table]['index_col'],
                    low_memory=False)

    # Define file paths for characteristion factors.
    cqe_file_path = cfg.EB_DATA_DIR_PATH+cfg.CQE_FILE_NAME
    cqm_file_path = cfg.EB_DATA_DIR_PATH+cfg.CQM_FILE_NAME
    cqr_file_path = cfg.EB_DATA_DIR_PATH+cfg.CQR_FILE_NAME

    # Read characterisation factors into pandas.
    df_cqe = pd.read_csv(cqe_file_path,
                         sep='\t',
                         header=[0, 1, 2],
                         index_col=[0, 1, 2, 3],
                         low_memory=False)
    df_cqm = pd.read_csv(cqm_file_path,
                         sep='\t',
                         header=[0, 1],
                         index_col=[0, 1],
                         low_memory=False)
    df_cqr = pd.read_csv(cqr_file_path,
                         sep='\t',
                         header=[0, 1, 2],
                         index_col=[0, 1],
                         low_memory=False)
    dict_eb_raw['cQe'] = df_cqe
    dict_eb_raw['cQm'] = df_cqm
    dict_eb_raw['cQr'] = df_cqr

    return dict_eb_raw


def process(dict_eb_raw):
    """ Process EB.

    """

    ut.log('Processing EXIOBASE.')
    dict_eb_proc = {}

    # Construct Total Production Vector x from sum of Z and Y.
    df_tx = dict_eb_raw['tZ'].sum(axis=1) + dict_eb_raw['tY'].sum(axis=1)

    # Construct 1/x array for future calculations.
    array_tx = df_tx.values
    array_tx[array_tx == 0] = np.nan
    array_tx_inv = (1/array_tx)

    # Replace nan with zero, due to div by zero.
    array_tx_inv[np.isnan(array_tx_inv)] = 0

    # Construct Technical Coefficient Matrix.
    df_ca = dict_eb_raw['tZ']*array_tx_inv

    # Construct Leontief Inverse.
    array_ci = np.eye(df_ca.shape[0])
    array_cl = np.linalg.inv(array_ci-df_ca)
    df_cl = pd.DataFrame(array_cl,
                         index=df_ca.index,
                         columns=df_ca.columns)
    df_cl.index = df_cl.index.droplevel(2)
    df_cre = dict_eb_raw['tRe']*array_tx_inv
    df_crm = fill_unit(dict_eb_raw['cQe'], df_cre)
    df_crm = dict_eb_raw['tRm']*array_tx_inv
    df_crm = fill_unit(dict_eb_raw['cQm'], df_crm)
    df_crr = dict_eb_raw['tRr']*array_tx_inv
    df_crr = fill_unit(dict_eb_raw['cQr'], df_crr)
    df_cv = dict_eb_raw['tV']*array_tx_inv
    df_ty = dict_eb_raw['tY']
    df_ty.index = df_ty.index.droplevel(2)

    dict_eb_proc['cQe'] = dict_eb_raw['cQe']
    dict_eb_proc['cQm'] = dict_eb_raw['cQm']
    dict_eb_proc['cQr'] = dict_eb_raw['cQr']
    dict_eb_proc['cRe'] = df_cre
    dict_eb_proc['cRm'] = df_crm
    dict_eb_proc['cRr'] = df_crr
    dict_eb_proc['cL'] = df_cl
    dict_eb_proc['tY'] = df_ty
    dict_eb_proc['tHe'] = dict_eb_raw['tHe']
    dict_eb_proc['tHm'] = dict_eb_raw['tHm']
    dict_eb_proc['tHr'] = dict_eb_raw['tHr']
    dict_eb_proc['cV'] = df_cv
    dict_eb_proc['cA'] = df_ca
    return dict_eb_proc


if __name__ == "__main__":

    DICT_EB_RAW = parse()
    DICT_EB_PROC = process(DICT_EB_RAW)
