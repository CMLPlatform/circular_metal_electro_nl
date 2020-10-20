# -*- coding: utf-8 -*-
""" Calculation module for script of paper on
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

import numpy as np
import pandas as pd

import cfg
import utils as ut

# Calculate total demand of machinery, and electrical machinery in EXIOBASE.


def calc_y_base_cbs_circular_import(df_io_cbs_2010_circular_import_coeff,
                                    df_y_base_cbs_circular,
                                    tup_cbs_rep):
    """ Calculate imports for baseline of
        circularity activities in CBS classification.
    """
    df_y_base_cbs_circular_diag = (
        pd.DataFrame(np.diag(df_y_base_cbs_circular[0]),
                     index=df_y_base_cbs_circular.index,
                     columns=df_y_base_cbs_circular.index))
    df_y_base_cbs_circular_import = df_io_cbs_2010_circular_import_coeff.dot(
        df_y_base_cbs_circular_diag)
    df_y_base_cbs_circular_import_sum = df_y_base_cbs_circular_import.sum()
    df_y_base_cbs_circular_import_cons = df_y_base_cbs_circular_import_sum[(
        tup_cbs_rep)]
    return df_y_base_cbs_circular_import_cons


def calc_y_base_cbs_circular_margin(df_io_cbs_2010_circular_margin_coeff,
                                    df_y_base_cbs_circular,
                                    tup_cbs_rep):
    """ Calculate margins for baseline of
        circularity activities in CBS classification.
    """
    df_y_base_cbs_circular_diag = (
        pd.DataFrame(np.diag(df_y_base_cbs_circular[0]),
                     index=df_y_base_cbs_circular.index,
                     columns=df_y_base_cbs_circular.index))
    df_y_base_cbs_circular_margin = df_io_cbs_2010_circular_margin_coeff.dot(
        df_y_base_cbs_circular_diag)
    df_y_base_cbs_circular_margin_sum = df_y_base_cbs_circular_margin.sum()
    df_y_base_cbs_circular_margin_cons = df_y_base_cbs_circular_margin_sum[(
        tup_cbs_rep)]
    return df_y_base_cbs_circular_margin_cons


def calc_y_delta_eb_circular_import(df_eb_ca_nl_rep_cons_reg_import,
                                    dict_y_delta_cbs_circular_import_cons):
    """ Calculate imports for changes in
        circularity activities in EB classification.
    """
    df_y_delta_eb_circular_import_cons = pd.DataFrame()
    for col in dict_y_delta_cbs_circular_import_cons:
        df_y_delta_cbs_circular_col_import_cons = (
            dict_y_delta_cbs_circular_import_cons[col])
        df_y_delta_eb_circular_col_import_cons = pd.DataFrame(
            df_eb_ca_nl_rep_cons_reg_import *
            df_y_delta_cbs_circular_col_import_cons)
        df_y_delta_eb_circular_col_import_cons.columns = [col]
        if df_y_delta_eb_circular_import_cons.empty:
            df_y_delta_eb_circular_import_cons = (
                df_y_delta_eb_circular_col_import_cons)
        else:
            df_y_delta_eb_circular_import_cons[col] = (
                df_y_delta_eb_circular_col_import_cons)
    return df_y_delta_eb_circular_import_cons


def calc_y_delta_cbs_circular_import(df_io_cbs_2010_circular_import_coeff,
                                     df_y_delta_cbs_circular,
                                     tup_cbs_rep):
    """ Calculate imports for changes in
        circularity activities in CBS classification.
    """
    dict_y_delta_cbs_circular_import_cons = {}
    for col in df_y_delta_cbs_circular:
        df_y_delta_cbs_circular_col_diag = (
            pd.DataFrame(np.diag(df_y_delta_cbs_circular[col]),
                         index=df_y_delta_cbs_circular.index,
                         columns=df_y_delta_cbs_circular.index))
        df_y_delta_cbs_circular_col_import = (
            df_io_cbs_2010_circular_import_coeff.dot(
                df_y_delta_cbs_circular_col_diag))
        df_y_delta_cbs_circular_col_import_sum = (
            df_y_delta_cbs_circular_col_import.sum())
        df_y_delta_cbs_circular_col_import_cons = (
            df_y_delta_cbs_circular_col_import_sum[tup_cbs_rep])
        dict_y_delta_cbs_circular_import_cons[col] = (
            df_y_delta_cbs_circular_col_import_cons)
    return dict_y_delta_cbs_circular_import_cons


def calc_y_delta_cbs_circular_margin(df_io_cbs_2010_circular_margin_coeff,
                                     df_y_delta_cbs_circular,
                                     tup_cbs_rep):
    """ Calculate margins for changes in
        circularity activities in CBS classification.
    """

    dict_y_delta_cbs_circular_margin_cons = {}
    for col in df_y_delta_cbs_circular:
        df_y_delta_cbs_circular_col_diag = (
            pd.DataFrame(np.diag(df_y_delta_cbs_circular[col]),
                         index=df_y_delta_cbs_circular.index,
                         columns=df_y_delta_cbs_circular.index))
        df_y_delta_cbs_circular_col_margin = (
            df_io_cbs_2010_circular_margin_coeff.dot(
                df_y_delta_cbs_circular_col_diag))
        df_y_delta_cbs_circular_col_margin_sum = (
            df_y_delta_cbs_circular_col_margin.sum())
        df_y_delta_cbs_circular_col_margin_cons = (
            df_y_delta_cbs_circular_col_margin_sum[tup_cbs_rep])
        dict_y_delta_cbs_circular_margin_cons[col] = (
            df_y_delta_cbs_circular_col_margin_cons)
    return dict_y_delta_cbs_circular_margin_cons


def calc_delta_eb_margin(df_y_base_eb_primary_source,
                         dict_y_delta_cbs_circular_margin):
    """ Calculate imports for changes in
        circularity activities in EB classification.
    """

    df_margin = pd.DataFrame()
    for meas_id in dict_y_delta_cbs_circular_margin:
        margin = dict_y_delta_cbs_circular_margin[meas_id]
        df_y_delta_eb_circular_margin_col = df_y_base_eb_primary_source.copy()
        df_y_delta_eb_circular_margin_col[:] = 0
        df_y_delta_eb_circular_margin_col.loc[cfg.TUP_EB_MARGIN] = (
            margin)
        df_y_delta_eb_circular_margin_col.columns = [meas_id]
        if df_margin.empty:
            df_margin = df_y_delta_eb_circular_margin_col
        else:
            df_margin[meas_id] = df_y_delta_eb_circular_margin_col
    return df_margin


def calc_base_eb_margin(df_y_base_eb_primary_source,
                        df_y_base_cbs_circular_margin):
    """ Calculate margins for baseline of
        circularity activities in EB classification.
    """

    df_y_base_eb_circular_margin_cons = df_y_base_eb_primary_source.copy()
    df_y_base_eb_circular_margin_cons[:] = 0
    df_y_base_eb_circular_margin_cons.loc[cfg.TUP_EB_MARGIN] = (
        df_y_base_cbs_circular_margin)
    return df_y_base_eb_circular_margin_cons


def calc_eb_ca_import(dict_io_eb_2010_proc, tup_cntr_prod):
    """ Calculate production recipe of imports for
        circularity activities in EB classification.
    """

    df_ca = dict_io_eb_2010_proc['cA']
    df_ca_nl_rep_cons_reg_all = df_ca[tup_cntr_prod]
    df_ca_nl_rep_cons_reg_import = df_ca_nl_rep_cons_reg_all.copy()
    df_ca_nl_rep_cons_reg_import.loc['NL'] = 0
    df_ca_nl_rep_cons_reg_import_sum = df_ca_nl_rep_cons_reg_import.sum()
    df_ca_nl_rep_cons_reg_import_scalar = 1/df_ca_nl_rep_cons_reg_import_sum

    df_ca_nl_rep_cons_reg_import_scaled = (df_ca_nl_rep_cons_reg_import *
                                           df_ca_nl_rep_cons_reg_import_scalar)
    df_ca_nl_rep_cons_reg_import_scaled.index = (
        df_ca_nl_rep_cons_reg_import.index.droplevel(2))

    return df_ca_nl_rep_cons_reg_import_scaled


def calc_bridge_eb_source_reg_all(dict_io_eb_2010):
    """ Calculate sourcing in EB classification.
    """

    df_eb_y = dict_io_eb_2010['tY']

    # Sum final demand to country level.
    df_eb_y_cntr = df_eb_y.sum(axis=1, level=0)

    # Get final demand from NL.
    df_eb_y_cntr_nl = df_eb_y_cntr['NL']

    # Get total use per product.
    df_eb_y_cntr_nl_prod = df_eb_y_cntr_nl.sum(level=1)

    # Get fraction of sourcing countries
    df_eb_y_cntr_nl_frac_div = (
        df_eb_y_cntr_nl.div(
            df_eb_y_cntr_nl_prod,
            axis=0,
            level=1))

    # Replace NaNs with 0s, arising from division by 0 if product sum is 0.
    df_eb_y_cntr_nl_frac_div[(
        np.isnan(df_eb_y_cntr_nl_frac_div))] = 0

    return df_eb_y_cntr_nl_frac_div


def calc_bridge_eb_source_reg_nl(dict_io_eb_2010):
    """ Calculate sourcing from NL in EB classification.

    """

    df_eb_y = dict_io_eb_2010['tY']

    # Sum final demand to country level.
    df_eb_y_cntr = df_eb_y.sum(axis=1, level=0)

    # Get final demand from NL.
    df_eb_y_cntr_nl = df_eb_y_cntr['NL']
    df_eb_y_cntr_nl[:] = 0

    df_eb_y_cntr_nl.loc['NL'] = 1

    return df_eb_y_cntr_nl


def calc_y_eb(df_bridge_eb_cpa3, df_y_cpa3):
    """ Calculate final demand in EB classification.

    """

    df_y_eb = df_bridge_eb_cpa3.dot(df_y_cpa3)
    return df_y_eb


def calc_y_eb_source(df_bridge_eb_source, df_y_eb):
    """ Calculate sourcing of final demand.

    """

    df_y_eb_source = pd.DataFrame()
    for col in df_y_eb.columns:
        df_y_eb_source[col] = (
            df_bridge_eb_source.mul(
                df_y_eb[col],
                axis=0,
                level=1))
    return df_y_eb_source


def calc_x_eb(dict_io_eb_2010, df_y_eb_source):
    """ Calculate total demand changes matrix in EXIOBASE classification.

    """
    ut.log(('Calculate total demand changes matrix in EXIOBASE '
            'classification.'))

    df_x_eb = dict_io_eb_2010['cL'].dot(df_y_eb_source)

    return df_x_eb


def get_dict_x_eb_source_diag_reg(df_x_delta_eb_source):
    """ Diagonalize final demand of regions in EB classification.

    """

    dict_x_eb_source_diag_reg = {}
    for col in df_x_delta_eb_source.columns:
        df_x_delta_eb_source_col = df_x_delta_eb_source[col]
        ar_x_delta_eb_source_col_diag = np.diag(df_x_delta_eb_source_col)
        df_x_delta_eb_source_col_diag = pd.DataFrame(
            ar_x_delta_eb_source_col_diag,
            index=df_x_delta_eb_source_col.index,
            columns=df_x_delta_eb_source_col.index)
        df_x_delta_eb_source_col_diag_cntr = (
            df_x_delta_eb_source_col_diag.sum(axis=1, level=0))
        df_x_delta_eb_source_col_diag_reg = pd.DataFrame()
        for tup_reg in cfg.LIST_TUP_REG:
            (reg, list_cntr) = tup_reg
            df_x_delta_eb_source_col_diag_reg[reg] = (
                df_x_delta_eb_source_col_diag_cntr[list_cntr].sum(
                    axis=1))

        dict_x_eb_source_diag_reg[col] = df_x_delta_eb_source_col_diag_reg

    return dict_x_eb_source_diag_reg


def calc_ef_eb(dict_io_eb_2010, dict_x_eb_diag, dict_tup_fp):
    """ Calculate environmental footprints of total demand changes matrix
        in EXIOBASE classification.

    """
    ut.log(('Calculate environmental footprints of total demand changes '
            'matrix in EXIOBASE classification.'))

    dict_ef_eb = {}

    for meas_id in dict_x_eb_diag:
        df_x_eb_diag = dict_x_eb_diag[meas_id]

        list_tup_fpm_qm_rm = [('e', 'cQe', 'cRe'),
                              ('m', 'cQm', 'cRm'),
                              ('r', 'cQr', 'cRr')]
        dict_ef_eb[meas_id] = {}
        for tup_fpm_qm_rm in list_tup_fpm_qm_rm:
            fpm, qm, rm = tup_fpm_qm_rm
            for fp in dict_tup_fp[fpm]:
                q = dict_tup_fp[fpm][fp]
                df_cq = dict_io_eb_2010[qm].loc[[q]]
                df_cr = dict_io_eb_2010[rm]
                df_fp = df_cq.dot(df_cr.dot(df_x_eb_diag))
                dict_ef_eb[meas_id][fp] = df_fp

    return dict_ef_eb


def calc_circular_prod_recipe(df_io_cbs_2010, dict_cbs_emp):
    """ Calculate production recipe of imports in CBS classification.

    """

    list_io_cbs_2010_circular_col = [(cfg.IO_CBS_REP_MACH_NAME,
                                      cfg.IO_CBS_REP_MACH_ID),
                                     (cfg.IO_CBS_REP_CONS_NAME,
                                      cfg.IO_CBS_REP_CONS_ID)]

    list_io_cbs_2010_circular_row = [(int(cfg.IO_CBS_REP_MACH_ID),
                                      cfg.IO_CBS_REP_MACH_NAME),
                                     (int(cfg.IO_CBS_REP_CONS_ID),
                                      cfg.IO_CBS_REP_CONS_NAME)]

    df_io_cbs_2010_circular_col = df_io_cbs_2010[list_io_cbs_2010_circular_col]
    df_io_cbs_2010_circular_col.columns = list_io_cbs_2010_circular_row

    df_io_cbs_2010_circular_z = df_io_cbs_2010_circular_col.iloc[0:76]
    df_io_cbs_2010_circular_sum = df_io_cbs_2010_circular_col.iloc[-1]
    df_io_cbs_2010_circular_a = (
        df_io_cbs_2010_circular_z/df_io_cbs_2010_circular_sum)
    df_io_cbs_2010_circular_import_coeff = (
        df_io_cbs_2010_circular_col.iloc[77:79]/df_io_cbs_2010_circular_sum)
    df_io_cbs_2010_circular_margin_coeff = pd.DataFrame(
        df_io_cbs_2010_circular_col.iloc[85]).T/df_io_cbs_2010_circular_sum

    df_io_cbs_2010_circular_va_coeff = pd.DataFrame(
        df_io_cbs_2010_circular_col.iloc[92]).T/df_io_cbs_2010_circular_sum

    dict_io_cbs_2010_circular_sum = df_io_cbs_2010_circular_sum.to_dict()
    dict_emp_frac = {}
    dict_emp_frac['Employment [k]'] = {}
    for tup_prod_id_name in dict_io_cbs_2010_circular_sum:
        prod_id, prod_name = tup_prod_id_name
        val_sum = dict_io_cbs_2010_circular_sum[tup_prod_id_name]
        val_emp = dict_cbs_emp[prod_name]
        val_emp_frac = val_emp/val_sum
        dict_emp_frac['Employment [k]'][tup_prod_id_name] = val_emp_frac
    df_emp_frac = pd.DataFrame.from_dict(dict_emp_frac).T

    return (df_io_cbs_2010_circular_a,
            df_io_cbs_2010_circular_import_coeff,
            df_io_cbs_2010_circular_margin_coeff,
            df_io_cbs_2010_circular_va_coeff,
            df_emp_frac
            )


def calc_vf_eb_emp(dict_io_eb_2010, dict_x_eb_diag, dict_impact):
    """ Calculate employment footprint of total demand changes matrix in
        EXIOBASE classification.

    """
    ut.log(('Calculate employment footprint of total demand changes matrix in '
            'EXIOBASE classification.'))
    dict_vf_eb_emp = {}

    for meas_id in dict_x_eb_diag:
        df_x_eb_diag = dict_x_eb_diag[meas_id]

        df_vf_eb = dict_io_eb_2010['cV'].dot(df_x_eb_diag)

        df_vf_eb_emp = df_vf_eb.loc[dict_impact['job']]
        dict_vf_eb_emp[meas_id] = df_vf_eb_emp
    return dict_vf_eb_emp


def calc_vf_eb_va(dict_io_eb_2010, dict_x_eb_diag, dict_impact):
    """ Calculate va footprint of total demand changes matrix in
        EXIOBASE classification.

    """
    ut.log(('Calculate va footprint of total demand changes matrix in '
            'EXIOBASE classification.'))
    dict_vf_eb_va = {}

    for meas_id in dict_x_eb_diag:
        df_x_eb_diag = dict_x_eb_diag[meas_id]
        df_vf_eb = dict_io_eb_2010['cV'].dot(
            df_x_eb_diag)

        df_vf_eb_va = df_vf_eb.loc[dict_impact['va']]
        dict_vf_eb_va[meas_id] = df_vf_eb_va
    return dict_vf_eb_va


def calc_base(dict_io_eb_2010_proc,
              df_y_base_eb_source,
              dict_tup_fp,
              dict_impact):
    """ Calculate baseline.

    """

    # Calculate total demand.
    df_x_base_eb_source = calc_x_eb(dict_io_eb_2010_proc,
                                    df_y_base_eb_source)

    # Diagonalize total demand and aggregate over regions.
    dict_x_base_eb_source_diag_reg = get_dict_x_eb_source_diag_reg(
        df_x_base_eb_source)

    # Calculate baseline environmental footprints.
    dict_ef_eb_base = calc_ef_eb(dict_io_eb_2010_proc,
                                 dict_x_base_eb_source_diag_reg,
                                 dict_tup_fp)

    # Calculate baseline employment.
    dict_vf_eb_base_emp = calc_vf_eb_emp(dict_io_eb_2010_proc,
                                         dict_x_base_eb_source_diag_reg,
                                         dict_impact)

    # Calculate baseline va
    dict_vf_eb_base_va = calc_vf_eb_va(dict_io_eb_2010_proc,
                                       dict_x_base_eb_source_diag_reg,
                                       dict_impact)

    return dict_ef_eb_base, dict_vf_eb_base_emp, dict_vf_eb_base_va


def calc_delta(dict_io_eb_2010_proc,
               df_y_delta_eb_source,
               dict_tup_fp,
               dict_impact):
    """ Calculate delta.

    """

    # Calculate delta total demand.
    df_x_delta_eb_source = calc_x_eb(dict_io_eb_2010_proc,
                                     df_y_delta_eb_source)

    # Diagonalize total demand and aggregate over regions.
    dict_x_delta_eb_source_diag_reg = get_dict_x_eb_source_diag_reg(
        df_x_delta_eb_source)

    # Calculate delta environmental footprints.
    dict_ef_eb_delta = calc_ef_eb(dict_io_eb_2010_proc,
                                  dict_x_delta_eb_source_diag_reg,
                                  dict_tup_fp)

    # Calculate delta employment.
    dict_vf_eb_delta_emp = calc_vf_eb_emp(dict_io_eb_2010_proc,
                                          dict_x_delta_eb_source_diag_reg,
                                          dict_impact)

    # Calculate delta va
    dict_vf_eb_delta_va = calc_vf_eb_va(dict_io_eb_2010_proc,
                                        dict_x_delta_eb_source_diag_reg,
                                        dict_impact)

    return dict_ef_eb_delta, dict_vf_eb_delta_emp, dict_vf_eb_delta_va


def calc_ef_net(dict_fp_eb_prim, dict_fp_eb_circ):
    """ Calculate net changes in EF.

    """

    dict_fp_eb_net = {}
    for meas_id in dict_fp_eb_prim:
        dict_fp_eb_net[meas_id] = {}
        for fp in dict_fp_eb_prim[meas_id]:
            df_fp_prim = dict_fp_eb_prim[meas_id][fp]
            df_fp_circ = dict_fp_eb_circ[meas_id][fp]
            df_fp_net = df_fp_prim+df_fp_circ
            dict_fp_eb_net[meas_id][fp] = df_fp_net
    return dict_fp_eb_net


def calc_vf_net(dict_fp_eb_prim, dict_fp_eb_circ):
    """ Calculate net changes in VF.

    """

    dict_fp_eb_net = {}
    for meas_id in dict_fp_eb_prim:
        dict_fp_eb_net[meas_id] = {}
        df_fp_prim = dict_fp_eb_prim[meas_id]
        df_fp_circ = dict_fp_eb_circ[meas_id]
        df_fp_net = df_fp_prim+df_fp_circ
        dict_fp_eb_net[meas_id] = df_fp_net
    return dict_fp_eb_net


def calc_fp_nl(dict_io_eb_2010_proc, df_y_nl, dict_tup_fp, dict_impact):
    (dict_ef_eb_base_nl,
     dict_vf_eb_base_emp_nl,
     dict_vf_eb_base_va_nl) = cmc.calc_base(dict_io_eb_2010_proc,
                                              df_y_nl,
                                              dict_tup_fp,
                                              dict_impact)
