# -*- coding: utf-8 -*-
""" Read module for script of paper on
    Global environmental and socio-economic impacts of a transition to a
    circular economy in metal and electrical products: a Dutch case-study

    Copyright (c) 2020 Bertram F. de Boer

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
import numpy as np

import os
import pickle

import pandas as pd

import cfg
import exiobase as eb
import utils as ut


def read_cbs_emp_2010():
    """ Read direct employment effects.

    """
    dict_cbs_emp = {}
    with open(cfg.INPUT_DIR_PATH+cfg.CBS_REP_EMP_2010_FILE_NAME,
              'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row_id, row in enumerate(csv_file):
            if row_id:
                total_s, total_e, str_prod_id_name, yr, str_val = row
                list_prod_id_name = str_prod_id_name.split()
                prod_name = ' '.join(list_prod_id_name[1:])
                dict_cbs_emp[prod_name] = float(str_val)
    return dict_cbs_emp


def read_y_tno():
    """ Read final demand baseline, scenario, and changes matrix
        in TNO classification.
    """
    ut.log(('Reading final demand baseline, scenario, and changes matrix '
            'in TNO classification.'))
    # Read list with sector IDs and names to dict.
    dict_sec = {}
    with open(cfg.INPUT_DIR_PATH+cfg.SEC_FILE_NAME, 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row in csv_file:
            sec_id, sec_nl, sec_en = row
            dict_sec[sec_nl] = (sec_id, sec_en)

    # Read list with product position, ID, and name to dict.
    dict_prod = {}
    with open(cfg.INPUT_DIR_PATH+cfg.PROD_ID_FILE_NAME, 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row in csv_file:
            str_prod_pos, str_prod_id, prod_nl, prod_en = row
            prod_id = int(str_prod_id)
            prod_pos = int(str_prod_pos)
            dict_prod[prod_id] = (prod_nl, prod_en, prod_pos)

    # Read raw delta sheet from deltaberekening.xlsx.
    # Note that one empty row was added between measure 1a and 1b, and
    # one empty row was removed between measure 1b and 2a.
    dict_row_count = {}
    dict_meas_row_count = {}
    list_csv_file = []
    with open(cfg.INPUT_DIR_PATH+cfg.DELTA_FILE_NAME, 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row_id, row in enumerate(csv_file):
            list_csv_file.append(row)
            # Skip first 2 header rows.
            if row_id > 1:
                bool_empty_row = True
                for col in row:
                    if col:
                        bool_empty_row = False
                if not bool_empty_row:
                    (str_meas_id,
                     str_prod_id_sec,
                     str_unit,
                     str_me_lo_base,
                     str_me_hi_base,
                     str_mon,
                     str_foo_1,
                     str_unit_delta,
                     str_mon_delta,
                     str_foo_2,
                     str_unit_scen,
                     str_mon_lo_scen,
                     str_mon_hi_scen,
                     str_foo_3,
                     str_mon_scen,
                     str_mon_delta,
                     str_mon_delta_corr,
                     str_foo_4) = row
                    # If cell is not empty: measure ID.
                    if str_meas_id:
                        # Ignore split by sector.
                        # E.g. 1a, 1b both go to measure ID 1.
                        if not str_meas_id.isdigit():
                            meas_id = int(str_meas_id[:-1])
                        else:
                            meas_id = int(str_meas_id)
                        # For each measure, count rows and log row IDs
                        dict_row_count[meas_id] = 1
                        start = row_id
                    else:
                        dict_row_count[meas_id] += 1
                        stop = row_id
                    # If cell is not empty: product IDs or sector.
                    if str_prod_id_sec:
                        list_prod_id_sec_split = str_prod_id_sec.split()
                        list_sec = []
                        sec_nl = ''
                        # If all elements are letters: sector.
                        for prod_id_sec_split in list_prod_id_sec_split:
                            if prod_id_sec_split.isalpha():
                                list_sec.append(prod_id_sec_split)
                            sec_nl = ' '.join(list_sec)

                # If row is empty: all values of measures are parsed
                else:
                    # Some measures only contain 1 row with values as opposed
                    # to 17 rows with data. These measures have an off-by-one
                    # product count. Adjust count.
                    if dict_row_count[meas_id] == 2:
                        dict_row_count[meas_id] = 1
                        stop = stop-1
                    # Fill dictionary with start and stop row numbers of
                    # measures.
                    if meas_id not in dict_meas_row_count:
                        dict_meas_row_count[meas_id] = {}
                    if sec_nl not in dict_meas_row_count[meas_id]:
                        dict_meas_row_count[meas_id][sec_nl] = {}
                    dict_meas_row_count[meas_id][sec_nl]['start'] = start
                    dict_meas_row_count[meas_id][sec_nl]['stop'] = stop

    # Fill dictionary with rows per measure and circularity sector.
    dict_meas_id_sec_row = {}
    for meas_id in dict_meas_row_count:
        dict_meas_id_sec_row[meas_id] = {}
        for sec_nl in dict_meas_row_count[meas_id]:
            start = dict_meas_row_count[meas_id][sec_nl]['start']
            stop = dict_meas_row_count[meas_id][sec_nl]['stop']
            dict_meas_id_sec_row[meas_id][sec_nl] = list_csv_file[start:stop+1]

    dict_base_df_dict_meas_prod_sec = {}
    dict_scen_df_dict_meas_prod_sec = {}
    dict_delta_df_dict_meas_prod_sec = {}

    # For each measure, for each circularity sector, read rows.
    for meas_id in dict_meas_id_sec_row:
        dict_base_df_dict_meas_prod_sec[meas_id] = {}
        dict_scen_df_dict_meas_prod_sec[meas_id] = {}
        dict_delta_df_dict_meas_prod_sec[meas_id] = {}
        for sec_nl in dict_meas_id_sec_row[meas_id]:
            prod_iter = 0
            for row_id, row in enumerate(
                    dict_meas_id_sec_row[meas_id][sec_nl]):
                (str_meas_id,
                 str_prod_id_sec,
                 str_base_unit,
                 str_base_mon_lo,
                 str_base_mon_hi,
                 str_base_mon,
                 str_foo_1,
                 str_delta_unit,
                 str_delta_mon_unit,
                 str_foo_2,
                 str_scen_unit,
                 str_scen_mon_lo,
                 str_scen_mon_hi,
                 str_foo_3,
                 str_scen_mon,
                 str_delta_mon,
                 str_delta_mon_corr,
                 str_foo_4) = row
                # First row contains product IDs.
                if row_id == 0:
                    # Expand product ID list (e.g. from 4, 5-7 to 4,5,6,7).
                    prod_id_split = str_prod_id_sec.replace(',', ' ')
                    list_prod_id_split = prod_id_split.split()
                    list_prod_id = []
                    for prod_id_split in list_prod_id_split:
                        if '-' in prod_id_split:
                            range_start, range_end = prod_id_split.split('-')
                            list_prod_id_range = list(range(int(range_start),
                                                            int(range_end)+1))
                            for prod_id_range in list_prod_id_range:
                                # Skip product ID 2, metal scrap not used.
                                if prod_id_range != 2:
                                    list_prod_id.append(prod_id_range)
                        else:
                            list_prod_id.append(int(prod_id_split))

                    # Generate list with corresponding product positions.
                    list_prod_pos = []
                    for prod_id in list_prod_id:
                        prod_nl, prod_en, prod_pos = dict_prod[prod_id]
                        list_prod_pos.append(prod_pos)

                    # Sort list with product IDs according to product position.
                    list_prod_pos_id = zip(list_prod_pos, list_prod_id)
                    list_prod_pos_id_sort = sorted(list_prod_pos_id)
                    list_prod_id_sort = []
                    for tup_prod_pos_id in list_prod_pos_id_sort:
                        prod_pos, prod_id = tup_prod_pos_id
                        list_prod_id_sort.append(prod_id)

                # If row contains data, extract monetary baseline and scenario,
                # and fill dictionary with these values per measure, product,
                # and sector.
                if str_base_mon:
                    base_mon = (
                        float(str_base_mon)/cfg.TNO_EURO_KILO2MEGA_SCALAR)
                    scen_mon = (
                        float(str_scen_mon)/cfg.TNO_EURO_KILO2MEGA_SCALAR)
                    delta_mon = (
                        float(str_delta_mon)/cfg.TNO_EURO_KILO2MEGA_SCALAR)
                    prod_id = list_prod_id_sort[prod_iter]
                    prod_nl, prod_en, prod_pos = dict_prod[prod_id]
                    sec_id, sec_en = dict_sec[sec_nl]
                    prod_iter += 1
                    dict_base_df_dict_meas_prod_sec[meas_id][prod_en,
                                                             sec_en] = (
                                                                 base_mon)
                    dict_scen_df_dict_meas_prod_sec[meas_id][prod_en,
                                                             sec_en] = (
                                                                 scen_mon)
                    dict_delta_df_dict_meas_prod_sec[meas_id][prod_en,
                                                              sec_en] = (
                                                                  delta_mon)

    dict_base = {}
    dict_base[0] = {}
    for meas_id in dict_base_df_dict_meas_prod_sec:
        for tup_prod_sec in dict_base_df_dict_meas_prod_sec[meas_id]:
            val = dict_base_df_dict_meas_prod_sec[meas_id][tup_prod_sec]
            if tup_prod_sec not in dict_base[0]:
                dict_base[0][tup_prod_sec] = val

    df_base = pd.DataFrame.from_dict(dict_base)

    df_scen = pd.DataFrame.from_dict(dict_scen_df_dict_meas_prod_sec)
    df_scen = df_scen.fillna(0)

    df_delta = pd.DataFrame.from_dict(dict_delta_df_dict_meas_prod_sec)
    df_delta = df_delta.fillna(0)

    return df_base, df_scen, df_delta


def get_y_tno_primary(df_y_tno):
    """ Get final demand for primary products in TNO classification.

    """
    dict_y_tno = df_y_tno.to_dict()

    dict_y_tno_primary = {}
    for meas_id in dict_y_tno:
        dict_y_tno_primary[meas_id] = {}
        for tup_prod_sec in dict_y_tno[meas_id]:
            prod, sec = tup_prod_sec
            if sec == 'Primary':
                val = dict_y_tno[meas_id][tup_prod_sec]
                dict_y_tno_primary[meas_id][tup_prod_sec] = val
    df_y_tno_primary = pd.DataFrame.from_dict(dict_y_tno_primary)
    return df_y_tno_primary


def get_y_tno_circular(df_y_tno):
    """ Get final demand for circularity activities in TNO classification.

    """
    dict_y_tno = df_y_tno.to_dict()

    dict_y_tno_circular = {}
    for meas_id in dict_y_tno:
        dict_y_tno_circular[meas_id] = {}
        for tup_prod_sec in dict_y_tno[meas_id]:
            prod, sec = tup_prod_sec
            if sec != 'Primary':
                val = dict_y_tno[meas_id][tup_prod_sec]
                dict_y_tno_circular[meas_id][tup_prod_sec] = val
    df_y_tno_primary = pd.DataFrame.from_dict(dict_y_tno_circular)
    return df_y_tno_primary


def read_io_eb_2010_proc():
    """ Read Input-Output tables from EXIOBASE 2010.'

    """
    ut.log('Reading Input-Output tables from EXIOBASE 2010.')
    # If EXIOBASE has already been parsed, read the pickle.
    if cfg.DICT_EB_PROC_FILE_NAME in os.listdir(cfg.INPUT_DIR_PATH):
        dict_io_eb_2010 = pickle.load(
            open(cfg.INPUT_DIR_PATH+cfg.DICT_EB_PROC_FILE_NAME,
                 'rb'))
    # Else, parse and process EXIOBASE and optionally save for future runs
    else:
        dict_io_eb_2010 = eb.process(eb.parse())
        if cfg.SAVE_EB:
            pickle.dump(dict_io_eb_2010,
                        open(cfg.INPUT_DIR_PATH+cfg.DICT_EB_PROC_FILE_NAME,
                             'wb'))
    return dict_io_eb_2010


def read_footprint():
    """ Read environmental impact categories.'

    """
    ut.log('Reading environmental impact categories.')
    dict_tup_fp = {}
    dict_tup_fp['e'] = {}
    dict_tup_fp['m'] = {}
    dict_tup_fp['r'] = {}

    list_fp_q_file_name = [('e', cfg.E_FP_FILE_NAME),
                           ('m', cfg.M_FP_FILE_NAME),
                           ('r', cfg.R_FP_FILE_NAME)]
    for fp_q_file_name in list_fp_q_file_name:
        fp_q, file_name = fp_q_file_name
        with open(cfg.INPUT_DIR_PATH+file_name) as read_file:
            csv_file = csv.reader(read_file, delimiter='\t')
            for row in csv_file:
                fp = row[0]
                q = tuple(row[1:])
                dict_tup_fp[fp_q][fp] = q
    return dict_tup_fp


def read_dict_impact():
    """ Read socio-economic impact categories.'

    """
    ut.log('Reading socio-economic impact categories.')
    dict_impact = {}
    list_fp_type = ['job', 'va']
    for fp_type in list_fp_type:
        dict_impact[fp_type] = []
        fp_file_name = cfg.DICT_FP_FILE_NAME[fp_type]
        with open(cfg.INPUT_DIR_PATH+fp_file_name) as read_file:
            csv_file = csv.reader(read_file, delimiter='\t')
            for row in csv_file:
                dict_impact[fp_type].append(tuple(row))
    return dict_impact


# def read_bridge_cbs_eb():
#     """ Read bridge matrix from CBS to EB classification.

#     """

#     df_bridge_cbs_eb = pd.read_csv(
#         cfg.INPUT_DIR_PATH+cfg.BRIDGE_CBS_EB_FILE_NAME,
#         index_col=0,
#         header=[0, 1],
#         sep='\t')
#     list_df_bridge_cbs_eb_col = list(df_bridge_cbs_eb.columns)
#     list_df_bridge_cbs_eb_col_int = []
#     for tup_cbs_prod in list_df_bridge_cbs_eb_col:
#         str_cbs_prod_id, cbs_prod_name = tup_cbs_prod
#         cbs_prod_id = int(str_cbs_prod_id)
#         tup_cbs_prod_int = (cbs_prod_id, cbs_prod_name)
#         list_df_bridge_cbs_eb_col_int.append(tup_cbs_prod_int)
#     df_bridge_cbs_eb.columns = list_df_bridge_cbs_eb_col_int


#     return df_bridge_cbs_eb

def gen_bridge_sbi_eb(dict_io_eb_2010):
    """ Generate bridge matrix from SBI to EB classification.

    """

    df_b_sbi_eb = pd.read_csv(
        cfg.INPUT_DIR_PATH+cfg.B_SBI_EB_FILE_NAME,
        sep = '\t',
        index_col = [0],
        header = [0,1])
    df_eb_y = dict_io_eb_2010['tY']

    # Sum final demand to country level.
    df_eb_y_cntr = df_eb_y.sum(axis=1, level=0)
    df_eb_y_nl = df_eb_y_cntr['NL']
    df_eb_y_nl_nl = df_eb_y_nl['NL']
    df_eb_y_nl_nl_diag = pd.DataFrame(np.diag(df_eb_y_nl_nl),
                                      index = df_eb_y_nl_nl.index,
                                      columns = df_eb_y_nl_nl.index)
    df_b_sbi_eb_nl = df_eb_y_nl_nl_diag.dot(df_b_sbi_eb)
    df_b_sbi_eb_nl_sum = df_b_sbi_eb_nl.sum()
    df_b_sbi_eb_nl_norm = df_b_sbi_eb_nl/df_b_sbi_eb_nl_sum

    l_df_b_sbi_eb_nl_norm_col = list(df_b_sbi_eb_nl_norm.columns)
    l_df_b_sbi_eb_nl_norm_col_int = []
    for tup_sbi_prod in l_df_b_sbi_eb_nl_norm_col:
        str_sbi_prod_id, sbi_prod_name = tup_sbi_prod
        sbi_prod_id = int(str_sbi_prod_id)
        tup_sbi_prod_int = (sbi_prod_id, sbi_prod_name)
        l_df_b_sbi_eb_nl_norm_col_int.append(tup_sbi_prod_int)
    df_b_sbi_eb_nl_norm.columns = l_df_b_sbi_eb_nl_norm_col_int

    return df_b_sbi_eb_nl_norm



def read_io_cbs_2010():
    """ Read CBS 2010 IO table.

    """

    df_io_cbs_2010 = pd.read_csv(cfg.INPUT_DIR_PATH+cfg.IO_CBS_2010_FILE_NAME,
                                 header=[1, 2],
                                 index_col=[0, 1],
                                 sep='\t')

    return df_io_cbs_2010


# def read_bridge_tno_circular_io():
#     """ Read bridge matrix from TNO to CBS circularity activities.

#     """
#     df_bridge_tno_circular_io = pd.read_csv(
#         cfg.INPUT_DIR_PATH+cfg.BRIDGE_TNO_CIRCULAR_IO_FILE_NAME,
#         header=[0, 1],
#         index_col=[0, 1],
#         sep='\t')
#     return df_bridge_tno_circular_io

def read_b_cpa_circ_sbi():
    """ Read bridge matrix from TNO to CBS circularity activities.

    """
    df_b_cpa_circ_sbi = pd.read_csv(
        cfg.INPUT_DIR_PATH+cfg.B_CPA_CIRC_SBI_FILE_NAME,
        header=[0, 1],
        index_col=[0, 1],
        sep='\t')
    return df_b_cpa_circ_sbi


# def read_bridge_tno_primary_eb():
#     """ Read bridge matrix from TNO classification to EXIOBASE.

#     """
#     ut.log('Reading bridge matrix from TNO classification to EXIOBASE.')

#     df_bridge_tno_eb = pd.read_csv(
#         cfg.INPUT_DIR_PATH+cfg.BRIDGE_TNO_EB_FILE_NAME,
#         header=[0, 1],
#         index_col=0,
#         sep='\t')
#     return df_bridge_tno_eb

def read_b_cpa_prim_eb():
    """ Read bridge matrix from TNO classification to EXIOBASE.

    """
    ut.log('Reading bridge matrix from TNO classification to EXIOBASE.')

    df_b_cpa_prim_eb = pd.read_csv(
        cfg.INPUT_DIR_PATH+cfg.B_CPA_PRIM_EB_FILE_NAME,
        header=[0, 1],
        index_col=0,
        sep='\t')
    return df_b_cpa_prim_eb
