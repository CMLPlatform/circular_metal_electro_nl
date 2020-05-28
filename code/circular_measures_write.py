# -*- coding: utf-8 -*-
""" Write module for script of paper on
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
import pandas as pd

import cfg


def arrange_ef_result(dict_ef_eb_delta):
    """ Arrange EF results.

    """
    dict_ef_eb_delta_prep = {}
    for meas_id in dict_ef_eb_delta:
        for fp_cat in dict_ef_eb_delta[meas_id]:
            df_fp = dict_ef_eb_delta[meas_id][fp_cat]
            dict_fp = df_fp.to_dict()
            for reg in dict_fp:
                for fp in dict_fp[reg]:
                    val = dict_fp[reg][fp]
                    if reg not in dict_ef_eb_delta_prep:
                        dict_ef_eb_delta_prep[reg] = {}
                    if fp_cat not in dict_ef_eb_delta_prep[reg]:
                        dict_ef_eb_delta_prep[reg][fp_cat] = {}
                    if meas_id not in dict_ef_eb_delta_prep[reg][fp_cat]:
                        dict_ef_eb_delta_prep[reg][fp_cat][meas_id] = {}
                    dict_ef_eb_delta_prep[reg][fp_cat][meas_id][fp] = val

    dict_ef_eb_delta_prep_df = {}
    for reg in dict_ef_eb_delta_prep:
        dict_ef_eb_delta_prep_df[reg] = {}
        for fp_cat in dict_ef_eb_delta_prep[reg]:
            df_fp = pd.DataFrame(dict_ef_eb_delta_prep[reg][fp_cat])
            dict_ef_eb_delta_prep_df[reg][fp_cat] = df_fp
    return dict_ef_eb_delta_prep_df


def arrange_vf_result(dict_vf_eb_delta):
    """ Arrange VF results.

    """
    dict_vf_eb_delta_prep = {}
    dict_df_meas_id_fp = {}
    for meas_id in dict_vf_eb_delta:
        dict_df_meas_id_fp[meas_id] = {}
        df_fp = dict_vf_eb_delta[meas_id]
        dict_fp = df_fp.to_dict()
        for reg in dict_fp:
            for fp in dict_fp[reg]:
                val = dict_fp[reg][fp]
                if reg not in dict_vf_eb_delta_prep:
                    dict_vf_eb_delta_prep[reg] = {}
                if meas_id not in dict_vf_eb_delta_prep[reg]:
                    dict_vf_eb_delta_prep[reg][meas_id] = {}
                dict_vf_eb_delta_prep[reg][meas_id][fp] = val

    dict_vf_eb_delta_prep_df = {}
    for reg in dict_vf_eb_delta_prep:
        dict_vf_eb_delta_prep_df[reg] = {}
        df_fp = pd.DataFrame(dict_vf_eb_delta_prep[reg])
        dict_vf_eb_delta_prep_df[reg] = df_fp
    return dict_vf_eb_delta_prep_df


def prepare_base_results(dict_ef_eb_base,
                         dict_vf_eb_base_emp,
                         dict_vf_eb_base_va):
    """ Prepare baseline results.

    """

    df_base_plt = pd.DataFrame()
    for tup_reg in cfg.LIST_TUP_REG:
        (reg, list_cntr) = tup_reg

        cf_total = dict_ef_eb_base[reg]['Carbon'].sum()
        mf_total = dict_ef_eb_base[reg]['Material use'].sum()
        wf_total = dict_ef_eb_base[reg]['Water consumption'].sum()
        lf_total = dict_ef_eb_base[reg]['Land use'].sum()
        emp_total = dict_vf_eb_base_emp[reg].sum()
        va_total = dict_vf_eb_base_va[reg].sum()

        cf_col_name_plt, cf_col_name_txt, cf_scalar = cfg.TUP_CF_SCALAR_BASE
        mf_col_name_plt, mf_col_name_txt, mf_scalar = cfg.TUP_MF_SCALAR_BASE
        wf_col_name_plt, wf_col_name_txt, wf_scalar = cfg.TUP_WF_SCALAR_BASE
        lf_col_name_plt, lf_col_name_txt, lf_scalar = cfg.TUP_LF_SCALAR_BASE
        job_col_name_plt, job_col_name_txt, job_scalar = (
            cfg.TUP_JOB_SCALAR_BASE)
        va_col_name_plt, va_col_name_txt, va_scalar = (
            cfg.TUP_VA_SCALAR_BASE)

        cf_total = cf_total/cf_scalar
        mf_total = mf_total/mf_scalar
        wf_total = wf_total/wf_scalar
        lf_total = lf_total/lf_scalar
        emp_total = emp_total/job_scalar
        va_total = va_total/va_scalar

        df_plt = pd.concat([cf_total,
                            mf_total,
                            wf_total,
                            lf_total,
                            emp_total,
                            va_total], axis=1)
        df_plt.columns = [cf_col_name_plt,
                          mf_col_name_plt,
                          wf_col_name_plt,
                          lf_col_name_plt,
                          job_col_name_plt,
                          va_col_name_plt]
        df_plt.index = [reg]
        df_base_plt = df_base_plt.append(df_plt)

    df_base_txt = df_base_plt.copy()
    df_base_txt.columns = [cf_col_name_txt,
                           mf_col_name_txt,
                           wf_col_name_txt,
                           lf_col_name_txt,
                           job_col_name_txt,
                           va_col_name_txt]
    return df_base_plt, df_base_txt


def prepare_delta_result(dict_ef_eb_delta,
                         dict_vf_eb_delta_emp,
                         dict_vf_eb_delta_va):
    """ Prepare delta results.

    """

    list_df_result_plt = []
    list_df_result_txt = []

    list_fp_tup_ef_scalar = [('Carbon', cfg.TUP_CF_SCALAR_DELTA),
                             ('Material use', cfg.TUP_MF_SCALAR_DELTA),
                             ('Water consumption', cfg.TUP_WF_SCALAR_DELTA),
                             ('Land use', cfg.TUP_LF_SCALAR_DELTA)]

    for fp_tup_ef_scalar in list_fp_tup_ef_scalar:
        df_result_ef_plt = pd.DataFrame()
        df_result_ef_txt = pd.DataFrame()
        fp_cat, tup_ef_scalar = fp_tup_ef_scalar
        fp_plt, fp_txt, fp_scalar = tup_ef_scalar
        for tup_reg in cfg.LIST_TUP_REG:
            (reg, list_cntr) = tup_reg
            if df_result_ef_plt.empty:
                df_result_ef_plt = dict_ef_eb_delta[reg][fp_cat].copy()
                df_result_ef_plt = df_result_ef_plt.T/fp_scalar
                df_result_ef_plt.columns = [(reg, fp_plt)]
                df_result_ef_txt = df_result_ef_plt.copy()
                df_result_ef_txt.columns = [(reg, fp_txt)]
            else:
                df_result_ef_plt[(reg, fp_plt)] = (
                    dict_ef_eb_delta[reg][fp_cat].T/fp_scalar)
                df_result_ef_txt[(reg, fp_txt)] = (
                    dict_ef_eb_delta[reg][fp_cat].T/fp_scalar)

        list_df_result_plt.append(df_result_ef_plt)
        list_df_result_txt.append(df_result_ef_txt)

    dict_vf_eb_sum = {}
    for reg in dict_vf_eb_delta_emp:
        df = pd.DataFrame(dict_vf_eb_delta_emp[reg].sum(axis=0).T)
        df.columns = [(reg, 'Employment [k]')]
        dict_vf_eb_sum[reg] = df

    df_result_vf_plt = pd.DataFrame()
    df_result_vf_txt = pd.DataFrame()
    fp_plt, fp_txt, fp_scalar = cfg.TUP_JOB_SCALAR_DELTA
    for tup_reg in cfg.LIST_TUP_REG:
        (reg, list_cntr) = tup_reg
        if df_result_vf_plt.empty:
            df_result_vf_plt = dict_vf_eb_sum[reg].copy()/fp_scalar
            df_result_vf_plt.columns = [(reg, fp_plt)]
            df_result_vf_txt = df_result_vf_plt.copy()
            df_result_vf_txt.columns = [(reg, fp_txt)]
        else:
            df_result_vf_plt[reg, fp_plt] = dict_vf_eb_sum[reg]/fp_scalar
            df_result_vf_txt[reg, fp_txt] = dict_vf_eb_sum[reg]/fp_scalar

    list_df_result_plt.append(df_result_vf_plt)
    list_df_result_txt.append(df_result_vf_txt)

    dict_vf_eb_va_sum = {}
    for reg in dict_vf_eb_delta_va:
        df = pd.DataFrame(dict_vf_eb_delta_va[reg].sum(axis=0).T)
        df.columns = [(reg, 'Value added [M€]')]
        dict_vf_eb_va_sum[reg] = df

    df_result_vf_va_plt = pd.DataFrame()
    df_result_vf_va_txt = pd.DataFrame()
    fp_plt, fp_txt, fp_scalar = cfg.TUP_VA_SCALAR_DELTA

    for tup_reg in cfg.LIST_TUP_REG:
        (reg, list_cntr) = tup_reg
        if df_result_vf_va_plt.empty:
            df_result_vf_va_plt = dict_vf_eb_va_sum[reg].copy()/fp_scalar
            df_result_vf_va_plt.columns = [(reg, fp_plt)]
            df_result_vf_va_txt = df_result_vf_va_plt.copy()
            df_result_vf_va_txt.columns = [(reg, fp_txt)]
        else:
            df_result_vf_va_plt[reg, fp_plt] = (
                dict_vf_eb_va_sum[reg]/fp_scalar)
            df_result_vf_va_txt[reg, fp_txt] = (
                dict_vf_eb_va_sum[reg]/fp_scalar)

    list_df_result_plt.append(df_result_vf_va_plt)
    list_df_result_txt.append(df_result_vf_va_txt)

    return list_df_result_plt, list_df_result_txt


def store_base(df_base_txt, file_name_pattern):
    """ Store base results.

    """

    dict_base_txt = df_base_txt.to_dict()

    file_name = '{}.txt'.format(file_name_pattern)

    dict_base_sum = {}
    for tup_fp in dict_base_txt:
        dict_base_sum[tup_fp] = 0
        for reg in dict_base_txt[tup_fp]:
            val = dict_base_txt[tup_fp][reg]
            dict_base_sum[tup_fp] += val

    with open(cfg.RESULT_TXT_DIR_PATH+file_name, 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Impact category',
                     'Unit',
                     'Region',
                     'Value abs']
        csv_file.writerow(row_write)
        for tup_imp_cat_unit in dict_base_txt:
            imp_cat, unit = tup_imp_cat_unit
            for reg in dict_base_txt[tup_imp_cat_unit]:
                val_abs = dict_base_txt[tup_imp_cat_unit][reg]
                row_write = [imp_cat, unit, reg, val_abs]
                csv_file.writerow(row_write)


def store_delta(list_df_delta_txt, file_name_pattern):
    """ Store delta results.

    """

    delta_file_name = '{}.txt'.format(file_name_pattern)
    with open(cfg.RESULT_TXT_DIR_PATH+delta_file_name, 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Measure ID',
                     'Impact category',
                     'Unit',
                     'Region',
                     'Value']
        csv_file.writerow(row_write)
        for df_delta_txt in list_df_delta_txt:
            dict_delta_txt = df_delta_txt.to_dict()
            for tup_reg_fp in dict_delta_txt:
                reg, tup_fp = tup_reg_fp
                fp, fp_unit = tup_fp
                for meas_id in dict_delta_txt[tup_reg_fp]:
                    val = dict_delta_txt[tup_reg_fp][meas_id]
                    row_write = [meas_id, fp, fp_unit, reg, val]
                    csv_file.writerow(row_write)


def write_base(dict_ef_eb_base,
               dict_vf_eb_base_emp,
               dict_vf_eb_base_va,
               file_name_pattern):
    """ Write base results.

    """

    dict_ef_eb_base_prep = arrange_ef_result(dict_ef_eb_base)
    dict_vf_eb_base_emp_prep = arrange_vf_result(dict_vf_eb_base_emp)
    dict_vf_eb_base_va_prep = arrange_vf_result(dict_vf_eb_base_va)

    df_base_plt, df_base_txt = prepare_base_results(dict_ef_eb_base_prep,
                                                    dict_vf_eb_base_emp_prep,
                                                    dict_vf_eb_base_va_prep)
    store_base(df_base_txt, file_name_pattern)

    return df_base_plt, df_base_txt


def write_delta(dict_ef_eb_delta,
                dict_vf_eb_delta_emp,
                dict_vf_eb_delta_va,
                df_base_txt,
                file_name_pattern):
    """ Write delta results.

    """

    dict_ef_eb_delta_prep = arrange_ef_result(dict_ef_eb_delta)
    dict_vf_eb_delta_emp_prep = arrange_vf_result(dict_vf_eb_delta_emp)
    dict_vf_eb_delta_va_prep = arrange_vf_result(dict_vf_eb_delta_va)

    list_df_delta_plt, list_df_delta_txt = (
        prepare_delta_result(dict_ef_eb_delta_prep,
                             dict_vf_eb_delta_emp_prep,
                             dict_vf_eb_delta_va_prep))

    store_delta(list_df_delta_txt, file_name_pattern)


def write_y_tno(df, dict_meas_id_short_long, time, sector):
    """ Write final demand in TNO classification.

    """
    if time == 'base':
        with open(
                cfg.RESULT_TXT_DIR_PATH+'y_{}_tno_{}.txt'.format(time, sector),
                'w') as write_file:
            csv_file = csv.writer(write_file,
                                  delimiter='\t',
                                  lineterminator='\n')
            csv_file.writerow(['Measure ID', 'Product', 'Sector', 'Value'])
            dict_df = df.to_dict()
            for meas_id in dict_df:
                for tup_prod_sect in dict_df[meas_id]:
                    prod, sect = tup_prod_sect
                    val = dict_df[meas_id][tup_prod_sect]
                    row_write = [meas_id, prod, sect, val]
                    csv_file.writerow(row_write)
    else:
        with open(
                cfg.RESULT_TXT_DIR_PATH+'y_{}_tno_{}.txt'.format(time, sector),
                'w') as write_file:
            csv_file = csv.writer(write_file,
                                  delimiter='\t',
                                  lineterminator='\n')
            csv_file.writerow(['Measure ID',
                               'Measure short',
                               'Measure long',
                               'Product',
                               'Sector',
                               'Value'])
            dict_df = df.to_dict()
            for meas_id in dict_df:
                meas_short = dict_meas_id_short_long[str(meas_id)]['short']
                meas_long = dict_meas_id_short_long[str(meas_id)]['long']
                for tup_prod_sect in dict_df[meas_id]:
                    prod, sect = tup_prod_sect
                    val = dict_df[meas_id][tup_prod_sect]
                    row_write = [meas_id,
                                 meas_short,
                                 meas_long,
                                 prod,
                                 sect,
                                 val]
                    csv_file.writerow(row_write)


def write_emp_direct(df_emp, time):
    """ Write direct employment effects.

    """
    with open(
            cfg.RESULT_TXT_DIR_PATH+'emp_direct_{}.txt'.format(time),
            'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        csv_file.writerow(['Measure ID', 'Direct employment [M]'])
        dict_emp = df_emp.to_dict()
        for meas_id in dict_emp:
            for emp in dict_emp[meas_id]:
                val = dict_emp[meas_id][emp]
                row_write = [meas_id, val]
                csv_file.writerow(row_write)


def write_va_direct(df_va, time):
    """ Write direct value added effects.

    """
    with open(cfg.RESULT_TXT_DIR_PATH+'va_direct_{}.txt'.format(time),
              'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        csv_file.writerow(['Measure ID', 'Direct value added [M€]'])
        dict_va = df_va.to_dict()
        for meas_id in dict_va:
            for va in dict_va[meas_id]:
                val = dict_va[meas_id][va]
                row_write = [meas_id, val]
                csv_file.writerow(row_write)
