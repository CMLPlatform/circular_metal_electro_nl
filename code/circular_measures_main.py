# -*- coding: utf-8 -*-
""" Main script for paper on
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
import circular_measures_read as cmr
import circular_measures_calc as cmc
import circular_measures_write as cmw

import utils as ut

def main():
#%%
    """ Preprocessing.

    """
    # Make directories for results, tests, and logs.
    ut.makedirs()

    # Read EXIOBASE.
    dict_io_eb_2010_proc = cmr.read_io_eb_2010_proc()

    # Calculate sourcing fractions for all regions
    df_bridge_eb_source_all = cmc.calc_bridge_eb_source_reg_all(
        dict_io_eb_2010_proc)

    df_bridge_eb_source_nl = cmc.calc_bridge_eb_source_reg_nl(
        dict_io_eb_2010_proc)

    # Read baseline, scenario, and delta of final demand in TNO classification.
    df_y_base_tno, df_y_scen_tno, df_y_delta_tno = cmr.read_y_tno()
    df_y_delta_tno.sum().sum()

    # Read footprints.
    dict_tup_fp = cmr.read_footprint()
    dict_impact = cmr.read_dict_impact()

    # Read bridge from TNO to CBS IO circularity sectors.
    df_b_cpa_circ_sbi = cmr.read_b_cpa_circ_sbi()

    # Read bridge from TNO to EXIOBASE.
    df_b_cpa_prim_eb = cmr.read_b_cpa_prim_eb()

    # Read bridge from CBS to EXIOBASE.
    df_bridge_sbi_eb = cmr.gen_bridge_sbi_eb(dict_io_eb_2010_proc)

    # Calculate production recipe of repair sectors.
    df_io_cbs_2010 = cmr.read_io_cbs_2010()

    dict_cbs_emp_2010 = cmr.read_cbs_emp_2010()

    (df_io_cbs_2010_circular_a,
     df_io_cbs_2010_circular_import_coeff,
     df_io_cbs_2010_circular_margin_coeff,
     df_io_cbs_2010_circular_va_coeff,
     df_cbs_emp_2010_coeff) = (
         cmc.calc_circular_prod_recipe(df_io_cbs_2010, dict_cbs_emp_2010))

    """ Bridge primary sale baseline from TNO to EXIOBASE.

    """
    # Get baseline of primary sales.
    df_y_base_tno_primary = cmr.get_y_tno_primary(df_y_base_tno)

    # Bridge base demand from TNO to sourced EXIOBASE classification.
    df_y_base_eb_primary = cmc.calc_y_eb(df_b_cpa_prim_eb,
                                         df_y_base_tno_primary)

    df_y_base_eb_primary_source = cmc.calc_y_eb_source(df_bridge_eb_source_all,
                                                       df_y_base_eb_primary)

    """ Bridge circularity baseline from TNO via CBS to EXIOBASE.

    """
    # Get baseline of circularity sectors.
    df_y_base_tno_circular = cmr.get_y_tno_circular(df_y_base_tno)
    df_y_base_tno_circular.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_base_tno_circular.txt',
        sep='\t')

    # Bridge baseline in circularity sectors from TNO to CBS IO.
    df_y_base_cbs_circular = df_b_cpa_circ_sbi.dot(
        df_y_base_tno_circular)

    df_y_base_cbs_circular_a = df_io_cbs_2010_circular_a.dot(
        df_y_base_cbs_circular)

    # Bridge circularity demand from CBS to EXIOBASE.
    df_y_base_eb_circular_a = df_bridge_sbi_eb.dot(df_y_base_cbs_circular_a)

    df_y_base_eb_circular_a_source_nl = cmc.calc_y_eb_source(
        df_bridge_eb_source_nl,
        df_y_base_eb_circular_a)

    # Calculate baseline of import of consumer repairs.
    y_base_cbs_circular_import_cons = cmc.calc_y_base_cbs_circular_import(
        df_io_cbs_2010_circular_import_coeff,
        df_y_base_cbs_circular,
        cfg.TUP_CBS_REP_CONS)

    df_eb_ca_nl_rep_cons_reg_import = cmc.calc_eb_ca_import(
        dict_io_eb_2010_proc,
        cfg.TUP_EB_REP_CONS)

    df_y_base_eb_circular_import_cons = pd.DataFrame(
        df_eb_ca_nl_rep_cons_reg_import*y_base_cbs_circular_import_cons)
    df_y_base_eb_circular_import_cons.columns = (
        df_y_base_eb_primary_source.columns)

    # Calculate baseline of import of machinery repairs.
    y_base_cbs_circular_import_mach = cmc.calc_y_base_cbs_circular_import(
        df_io_cbs_2010_circular_import_coeff,
        df_y_base_cbs_circular,
        cfg.TUP_CBS_REP_MACH)

    df_eb_ca_nl_rep_mach_reg_import = cmc.calc_eb_ca_import(
        dict_io_eb_2010_proc,
        cfg.TUP_EB_REP_MACH)

    df_y_base_eb_circular_import_mach = pd.DataFrame(
        df_eb_ca_nl_rep_mach_reg_import*y_base_cbs_circular_import_mach)
    df_y_base_eb_circular_import_mach.columns = (
        df_y_base_eb_primary_source.columns)

    # Calculate baseline of margin of consumer repairs
    y_base_cbs_circular_margin_cons = cmc.calc_y_base_cbs_circular_margin(
        df_io_cbs_2010_circular_margin_coeff,
        df_y_base_cbs_circular,
        cfg.TUP_CBS_REP_CONS)

    # Calculate direct value added of consumer repairs
    df_base_cbs_va = df_io_cbs_2010_circular_va_coeff.dot(
        df_y_base_cbs_circular)

    # Calculate direct employment of baseline.
    df_base_cbs_emp = df_cbs_emp_2010_coeff.dot(df_y_base_cbs_circular)

    df_y_base_eb_circular_margin_cons = cmc.calc_base_eb_margin(
        df_y_base_eb_primary_source, y_base_cbs_circular_margin_cons)

    # Calculate baseline of margin of machinery repairs
    y_base_cbs_circular_margin_mach = cmc.calc_y_base_cbs_circular_margin(
        df_io_cbs_2010_circular_margin_coeff,
        df_y_base_cbs_circular,
        cfg.TUP_CBS_REP_MACH)

    df_y_base_eb_circular_margin_mach = cmc.calc_base_eb_margin(
        df_y_base_eb_primary_source, y_base_cbs_circular_margin_mach)

    df_y_base_eb_source_primary = (df_y_base_eb_primary_source)
    df_y_base_eb_source_primary.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_base_eb_source_primary.txt',
        sep='\t')

    """ Calculate baseline of footprints from primary sales and circularity.

    """
    (dict_ef_eb_base_prim,
     dict_vf_eb_base_emp_prim,
     dict_vf_eb_base_va_prim) = cmc.calc_base(dict_io_eb_2010_proc,
                                              df_y_base_eb_source_primary,
                                              dict_tup_fp,
                                              dict_impact)

###
    df_y_cntr = dict_io_eb_2010_proc['tY'].sum(axis = 1, level=0)
    df_y_nl = pd.DataFrame(df_y_cntr['NL'])

    df_y_nl.to_csv(cfg.RESULT_TXT_DIR_PATH+'df_y_nl.txt', sep='\t')
    (dict_ef_eb_base_nl,
     dict_vf_eb_base_emp_nl,
     dict_vf_eb_base_va_nl) = cmc.calc_base(dict_io_eb_2010_proc,
                                              df_y_nl,
                                              dict_tup_fp,
                                              dict_impact)

    s_mega2giga = 1e3
    df_y_nl_cntr  = df_y_nl.sum(level=0)
    d_y_nl_cntr = df_y_nl_cntr.to_dict()
    d_y_nl_source_reg = {}
    for t_reg in cfg.LIST_TUP_REG:
         reg, l_cntr = t_reg
         if reg not in d_y_nl_source_reg:
             d_y_nl_source_reg[reg] = 0
             for cntr in l_cntr:
                 val = df_y_nl_cntr['NL'][cntr]/s_mega2giga
                 d_y_nl_source_reg[reg] += val


    with open(cfg.RESULT_TXT_DIR_PATH+'y_nl.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Region', 'Final Demand [G€]']
        csv_file.writerow(row_write)
        for reg in d_y_nl_source_reg:
            val = d_y_nl_source_reg[reg]
            row_write = [reg, val]
            csv_file.writerow(row_write)

    d_fp_tup_ef_scalar = {'Carbon': cfg.TUP_CF_SCALAR_DELTA,
              'Material use': cfg.TUP_MF_SCALAR_DELTA,
              'Water consumption': cfg.TUP_WF_SCALAR_DELTA,
              'Land use': cfg.TUP_LF_SCALAR_DELTA}
    d_fp_nl = {}
    for nl in dict_ef_eb_base_nl:
        for fp_cat in dict_ef_eb_base_nl[nl]:
            t_fp = d_fp_tup_ef_scalar[fp_cat]
            fp_plt, fp_txt, fp_scalar = t_fp
            df = dict_ef_eb_base_nl[nl][fp_cat]
            d_df = df.to_dict()
            for reg in d_df:
                if reg not in d_fp_nl:
                    d_fp_nl[reg] = {}
                for t_imp_cat in d_df[reg]:
                    val = d_df[reg][t_imp_cat]/fp_scalar
                    d_fp_nl[reg][fp_txt] = val
                    print(fp_cat, reg, t_imp_cat, fp_txt, val)

    emp_plt, emp_txt, emp_scalar = cfg.TUP_JOB_SCALAR_BASE
    for nl in dict_vf_eb_base_emp_nl:
        df = dict_vf_eb_base_emp_nl[nl]
        d_df = df.to_dict()
        for reg in d_df:
            if reg not in d_fp_nl:
                d_fp_nl[reg] = {}
            d_fp_nl[reg][emp_txt] = 0

            for t_imp_cat in d_df[reg]:
                val = d_df[reg][t_imp_cat]/emp_scalar
                d_fp_nl[reg][emp_txt] += val
                print(fp_cat, reg, t_imp_cat, emp_txt, val)

    va_plt, va_txt, va_scalar = cfg.TUP_VA_SCALAR_BASE
    for nl in dict_vf_eb_base_va_nl:
        df = dict_vf_eb_base_va_nl[nl]
        d_df = df.to_dict()
        for reg in d_df:
            if reg not in d_fp_nl:
                d_fp_nl[reg] = {}
            d_fp_nl[reg][va_txt] = 0
            for t_imp_cat in d_df[reg]:
                val = d_df[reg][t_imp_cat]/va_scalar
                d_fp_nl[reg][va_txt] += val
                print(fp_cat, reg, t_imp_cat, va_txt, val)

    with open(cfg.RESULT_TXT_DIR_PATH+'fp_nl.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Region', 'Footprint ID', 'Footprint', 'Unit', 'Value']
        csv_file.writerow(row_write)
        for reg in d_fp_nl:
            for t_fp_id, t_fp in enumerate(d_fp_nl[reg]):
                fp, unit = t_fp
                val = d_fp_nl[reg][t_fp]
                row_write = [reg, t_fp_id, fp, unit, val]
                csv_file.writerow(row_write)

###


    df_y_base_eb_source_circular = (df_y_base_eb_circular_a_source_nl +
                                    df_y_base_eb_circular_import_cons +
                                    df_y_base_eb_circular_import_mach +
                                    df_y_base_eb_circular_margin_cons +
                                    df_y_base_eb_circular_margin_mach)

###
    s_mega2giga = 1e3
    df_y_base_eb_source_prim_cntr  = df_y_base_eb_source_primary.sum(level=0)
    d_y_base_eb_source_prim_cntr = df_y_base_eb_source_prim_cntr.to_dict()
    d_y_base_eb_source_reg = {}
    d_y_base_eb_source_reg['Prim'] = {}
    for t_reg in cfg.LIST_TUP_REG:
        reg, l_cntr = t_reg
        if reg not in d_y_base_eb_source_reg['Prim']:
            d_y_base_eb_source_reg['Prim'][reg] = 0
            for cntr in l_cntr:
                val = d_y_base_eb_source_prim_cntr[0][cntr]/s_mega2giga
                d_y_base_eb_source_reg['Prim'][reg] += val


    d_y_base_eb_source_reg['Circ'] = {}
    d_y_base_eb_source_reg['Circ']['NL'] = (
        df_y_base_tno_circular.sum().sum()/s_mega2giga)

    with open(cfg.RESULT_TXT_DIR_PATH+'y_base.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Activity', 'Region', 'Final Demand [G€]']
        csv_file.writerow(row_write)
        for act in d_y_base_eb_source_reg:
            for reg in d_y_base_eb_source_reg[act]:
                val = d_y_base_eb_source_reg[act][reg]
                row_write = [act, reg, val]
                csv_file.writerow(row_write)
###
    (dict_ef_eb_base_circ,
     dict_vf_eb_base_emp_circ,
     dict_vf_eb_base_va_circ) = cmc.calc_base(dict_io_eb_2010_proc,
                                              df_y_base_eb_source_circular,
                                              dict_tup_fp,
                                              dict_impact)

    df_y_base_eb_source_net = (df_y_base_eb_primary_source +
                               df_y_base_eb_circular_a_source_nl +
                               df_y_base_eb_circular_import_cons +
                               df_y_base_eb_circular_import_mach +
                               df_y_base_eb_circular_margin_cons +
                               df_y_base_eb_circular_margin_mach)

    df_y_base_eb_source_net.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_base_eb_source_net.txt',
        sep='\t')

    dict_ef_eb_base_net = cmc.calc_ef_net(dict_ef_eb_base_prim,
                                          dict_ef_eb_base_circ)
    dict_vf_eb_base_emp_net = cmc.calc_vf_net(dict_vf_eb_base_emp_prim,
                                              dict_vf_eb_base_emp_circ)
    dict_vf_eb_base_va_net = cmc.calc_vf_net(dict_vf_eb_base_va_prim,
                                             dict_vf_eb_base_va_circ)

    """ Bridge primary sale delta from TNO to EXIOBASE.

    """
    # Get delta of primary sales.
    df_y_delta_tno_primary = cmr.get_y_tno_primary(df_y_delta_tno)

    # Bridge base demand from TNO to sourced EXIOBASE classification.
    df_y_delta_eb_primary = cmc.calc_y_eb(df_b_cpa_prim_eb,
                                          df_y_delta_tno_primary)


    df_y_delta_eb_primary_source = cmc.calc_y_eb_source(
        df_bridge_eb_source_all,
        df_y_delta_eb_primary)

    """ Bridge circularity delta from TNO via CBS to EXIOBASE.

    """
    # Get delta of circularity sectors.
    df_y_delta_tno_circular = cmr.get_y_tno_circular(df_y_delta_tno)
    df_y_delta_tno_circular.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_delta_tno_circular.txt',
        sep='\t')

    # Bridge shifts in circularity sectors from TNO to CBS IO.
    df_y_delta_cbs_circular = df_b_cpa_circ_sbi.dot(
        df_y_delta_tno_circular)

    # Calculate production recipe of repair sectors.
    df_y_delta_cbs_circular_a = df_io_cbs_2010_circular_a.dot(
        df_y_delta_cbs_circular)

    # Calculate delta of circularity import of consumer repairs.
    dict_y_delta_cbs_circular_import_cons = (
        cmc.calc_y_delta_cbs_circular_import(
            df_io_cbs_2010_circular_import_coeff,
            df_y_delta_cbs_circular,
            cfg.TUP_CBS_REP_CONS))

    df_y_delta_eb_circular_import_cons = cmc.calc_y_delta_eb_circular_import(
        df_eb_ca_nl_rep_cons_reg_import,
        dict_y_delta_cbs_circular_import_cons)

    # Calculate delta of circularity import of machinery repairs.
    dict_y_delta_cbs_circular_import_mach = (
        cmc.calc_y_delta_cbs_circular_import(
            df_io_cbs_2010_circular_import_coeff,
            df_y_delta_cbs_circular,
            cfg.TUP_CBS_REP_MACH))

    df_y_delta_eb_circular_import_mach = cmc.calc_y_delta_eb_circular_import(
        df_eb_ca_nl_rep_cons_reg_import,
        dict_y_delta_cbs_circular_import_mach)

    # Calculate delta of circularity margin of consumer repairs.
    dict_y_delta_cbs_circular_margin_cons = (
        cmc.calc_y_delta_cbs_circular_margin(
            df_io_cbs_2010_circular_margin_coeff,
            df_y_delta_cbs_circular,
            cfg.TUP_CBS_REP_CONS))

    df_y_delta_eb_circular_margin_cons = cmc.calc_delta_eb_margin(
        df_y_base_eb_primary_source,
        dict_y_delta_cbs_circular_margin_cons)

    # Calculate delta of circularity margin of machinery repairs.
    dict_y_delta_cbs_circular_margin_mach = (
        cmc.calc_y_delta_cbs_circular_margin(
            df_io_cbs_2010_circular_margin_coeff,
            df_y_delta_cbs_circular,
            cfg.TUP_CBS_REP_MACH))

    df_y_delta_eb_circular_margin_mach = cmc.calc_delta_eb_margin(
        df_y_base_eb_primary_source,
        dict_y_delta_cbs_circular_margin_mach)

    # Calculate direct value added of delta.
    df_delta_cbs_va = df_io_cbs_2010_circular_va_coeff.dot(
        df_y_delta_cbs_circular)

    # Calculate direct employment of delta.
    df_delta_cbs_emp = df_cbs_emp_2010_coeff.dot(df_y_delta_cbs_circular)

    # Bridge circularity demand from CBS to EXIOBASE.
    # df_y_delta_eb_circular_a = df_bridge_cbs_eb.dot(df_y_delta_cbs_circular_a)
    df_y_delta_eb_circular_a = df_bridge_sbi_eb.dot(df_y_delta_cbs_circular_a)
    df_y_delta_eb_circular_a_source_nl = cmc.calc_y_eb_source(
        df_bridge_eb_source_nl,
        df_y_delta_eb_circular_a)

    df_y_delta_eb_source_primary = (df_y_delta_eb_primary_source)
    df_y_delta_eb_source_primary.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_delta_eb_source_primary.txt',
        sep='\t')

###
    # df_y_base_eb_source_prim_cntr  = df_y_base_eb_source_primary.sum(level=0)
    # d_y_base_eb_source_prim_cntr = df_y_base_eb_source_prim_cntr.to_dict()

    # d_y_base_eb_source_reg = {}
    # d_y_base_eb_source_reg['Prim'] = {}
    # for t_reg in cfg.LIST_TUP_REG:
    #     reg, l_cntr = t_reg
    #     if reg not in d_y_base_eb_source_reg['Prim']:
    #         d_y_base_eb_source_reg['Prim'][reg] = 0
    #         for cntr in l_cntr:
    #             val = d_y_base_eb_source_prim_cntr[0][cntr]/s_mega2giga
    #             d_y_base_eb_source_reg['Prim'][reg] += val
    #             print(reg, cntr, val)

    s_mega2giga = 1e3

    df_y_delta_eb_source_primary_cntr = (
        df_y_delta_eb_source_primary.sum(axis=1).sum(level=0))
    d_y_delta_eb_source_primary_cntr = (
        df_y_delta_eb_source_primary_cntr.to_dict())

    d_y_delta_eb_source_reg = {}
    d_y_delta_eb_source_reg['Prim'] = {}
    for t_reg in cfg.LIST_TUP_REG:
        reg, l_cntr = t_reg
        if reg not in d_y_delta_eb_source_reg['Prim']:
            d_y_delta_eb_source_reg['Prim'][reg] = 0
            for cntr in l_cntr:
                val = d_y_delta_eb_source_primary_cntr[cntr]/s_mega2giga
                d_y_delta_eb_source_reg['Prim'][reg] += val

    d_y_delta_eb_source_reg['Circ'] = {}
    d_y_delta_eb_source_reg['Circ']['NL'] = (
        df_y_delta_tno_circular.sum().sum()/s_mega2giga)

    with open(cfg.RESULT_TXT_DIR_PATH+'y_delta.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Activity', 'Region', 'Final Demand [G€]']
        csv_file.writerow(row_write)
        for act in d_y_delta_eb_source_reg:
            for reg in d_y_delta_eb_source_reg[act]:
                val = d_y_delta_eb_source_reg[act][reg]
                row_write = [act, reg, val]
                csv_file.writerow(row_write)


###
    (dict_ef_eb_delta_prim,
     dict_vf_eb_delta_emp_prim,
     dict_vf_eb_delta_va_prim) = cmc.calc_delta(dict_io_eb_2010_proc,
                                                df_y_delta_eb_source_primary,
                                                dict_tup_fp,
                                                dict_impact)

    df_y_delta_eb_source_circular = (df_y_delta_eb_circular_a_source_nl +
                                     df_y_delta_eb_circular_import_cons +
                                     df_y_delta_eb_circular_import_mach +
                                     df_y_delta_eb_circular_margin_cons +
                                     df_y_delta_eb_circular_margin_mach)

    (dict_ef_eb_delta_circ,
     dict_vf_eb_delta_emp_circ,
     dict_vf_eb_delta_va_circ) = cmc.calc_delta(
         dict_io_eb_2010_proc,
         df_y_delta_eb_source_circular,
         dict_tup_fp,
         dict_impact)

    df_y_delta_eb_source_net = (df_y_delta_eb_primary_source +
                                df_y_delta_eb_circular_a_source_nl +
                                df_y_delta_eb_circular_import_cons +
                                df_y_delta_eb_circular_import_mach +
                                df_y_delta_eb_circular_margin_cons +
                                df_y_delta_eb_circular_margin_mach)

    df_y_delta_eb_source_net.to_csv(
        cfg.RESULT_TXT_DIR_PATH+'y_delta_eb_source_net.txt',
        sep='\t')

    dict_ef_eb_delta_net = cmc.calc_ef_net(dict_ef_eb_delta_prim,
                                           dict_ef_eb_delta_circ)
    dict_vf_eb_delta_emp_net = cmc.calc_vf_net(dict_vf_eb_delta_emp_prim,
                                               dict_vf_eb_delta_emp_circ)
    dict_vf_eb_delta_va_net = cmc.calc_vf_net(dict_vf_eb_delta_va_prim,
                                              dict_vf_eb_delta_va_circ)

    dict_meas_id_short_long = {}
    with open(cfg.INPUT_DIR_PATH+cfg.LIST_MEAS_ID_SHORT_LONG_FILE_NAME,
              'r') as (read_file):
        csv_file = csv.reader(read_file, delimiter='\t')
        for row_id, row in enumerate(csv_file):
            if row_id:
                meas_id, meas_short, meas_long = row
                dict_meas_id_short_long[meas_id] = {}
                dict_meas_id_short_long[meas_id]['short'] = meas_short
                dict_meas_id_short_long[meas_id]['long'] = meas_long

    cmw.write_y_tno(df_y_base_tno, dict_meas_id_short_long, 'base',
                    'all')
    cmw.write_y_tno(df_y_base_tno_primary, dict_meas_id_short_long, 'base',
                    'primary')
    cmw.write_y_tno(df_y_base_tno_circular, dict_meas_id_short_long, 'base',
                    'circular')
    cmw.write_y_tno(df_y_delta_tno_primary, dict_meas_id_short_long, 'delta',
                    'primary')
    cmw.write_y_tno(df_y_delta_tno_circular, dict_meas_id_short_long, 'delta',
                    'circular')
    cmw.write_y_tno(df_y_delta_tno, dict_meas_id_short_long, 'delta',
                    'all')

    '''Write results.'''
    df_base_plt_prim, df_base_txt_prim = cmw.write_base(
        dict_ef_eb_base_prim,
        dict_vf_eb_base_emp_prim,
        dict_vf_eb_base_va_prim)

    df_base_plt_circ, df_base_txt_circ = cmw.write_base(
        dict_ef_eb_base_circ,
        dict_vf_eb_base_emp_circ,
        dict_vf_eb_base_va_circ)

    df_base_txt_circ_inc_direct = cmw.add_direct(df_base_txt_circ,
                                                 df_base_cbs_emp,
                                                 df_base_cbs_va)

###
    d_delta_emp = {}
    d_delta_emp['Circ'] = {}
    d_delta_emp['Prim'] = {}
    act = 'Circ'
    d_emp_act = dict_vf_eb_delta_emp_circ
    for meas_id in d_emp_act:
        df = d_emp_act[meas_id]
        d_df = df.to_dict()
        for reg in d_df:
            if reg not in d_delta_emp[act]:
                d_delta_emp[act][reg] = {}
            for t_emp in d_df[reg]:
                if t_emp not in d_delta_emp[act][reg]:
                    d_delta_emp[act][reg][t_emp] = 0
                val = d_df[reg][t_emp]
                d_delta_emp[act][reg][t_emp] += val

    act = 'Prim'
    d_emp_act = dict_vf_eb_delta_emp_prim
    for meas_id in d_emp_act:
        df = d_emp_act[meas_id]
        d_df = df.to_dict()
        for reg in d_df:
            if reg not in d_delta_emp[act]:
                d_delta_emp[act][reg] = {}
            for t_emp in d_df[reg]:
                if t_emp not in d_delta_emp[act][reg]:
                    d_delta_emp[act][reg][t_emp] = 0
                val = d_df[reg][t_emp]
                d_delta_emp[act][reg][t_emp] += val

    with open(cfg.RESULT_TXT_DIR_PATH+'d_delta_emp.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Activity', 'Region', 'Employment type', 'Unit', 'Value']
        csv_file.writerow(row_write)
        for act in d_delta_emp:
            for reg in d_delta_emp[act]:
                for t_emp in d_delta_emp[act][reg]:
                    emp, unit = t_emp
                    val = d_delta_emp[act][reg][t_emp]
                    row_write = [act, reg, emp, unit, val]
                    csv_file.writerow(row_write)

###

    d_cat_base = cmw.cat_base(df_base_txt_prim, df_base_txt_circ_inc_direct)
    cmw.write_cat_base(d_cat_base)

    d_cat_delta = cmw.cat_delta(dict_ef_eb_delta_prim,
                                dict_vf_eb_delta_emp_prim,
                                dict_vf_eb_delta_va_prim,
                                dict_ef_eb_delta_circ,
                                dict_vf_eb_delta_emp_circ,
                                dict_vf_eb_delta_va_circ,
                                df_delta_cbs_emp,
                                df_delta_cbs_va)

    cmw.write_cat_delta(d_cat_delta)
#%%
if __name__ == '__main__':
    main()
