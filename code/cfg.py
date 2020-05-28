# -*- coding: utf-8 -*-
""" Configurations for script of paper on
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

import datetime


def get_date():
    """ Get string with date.
        Used to make result directories.

        Returns:
        --------
        string with date.
    """

    date_time = datetime.datetime.now()
    return '{}{:02}{:02}'.format(date_time.year,
                                 date_time.month,
                                 date_time.day)


DATE = get_date()

# Define paths for input and output data.
INPUT_DIR_PATH = '../input/'
OUTPUT_DIR_PATH = '../output/{}'.format(DATE)
RESULT_DIR_PATH = '{}/result/'.format(OUTPUT_DIR_PATH)
RESULT_TXT_DIR_PATH = '{}/txt/'.format(RESULT_DIR_PATH)
LOG_DIR_PATH = '{}/log/'.format(OUTPUT_DIR_PATH)

LIST_OUTPUT_DIR_PATH = [RESULT_TXT_DIR_PATH,
                        LOG_DIR_PATH]

# Define file names of input data.
BRIDGE_TNO_EB_FILE_NAME = 'bridge_tno_primary_eb.txt'
BRIDGE_TNO_CIRCULAR_IO_FILE_NAME = 'bridge_tno_circular_io.txt'
IO_CBS_2010_FILE_NAME = 'io_cbs_2010.txt'
BRIDGE_CBS_EB_FILE_NAME = 'bridge_cbs_eb.txt'

DELTA_FILE_NAME = 'deltaberekening_delta.txt'
PROD_ID_FILE_NAME = 'deltaberekening_prod_id.txt'
SEC_FILE_NAME = 'deltaberekening_sec.txt'
CBS_REP_EMP_2010_FILE_NAME = 'cbs_rep_emp_2010.txt'

# Directory with raw text version of EXIOBASE. Used for parsing.
EB_DATA_DIR_PATH = '../../data/'
EB_DIR_PATH = EB_DATA_DIR_PATH+'mrIOT_pxp_ita_transactions_3.3_2010/'
E_FP_FILE_NAME = 'list_impact_emission.txt'
M_FP_FILE_NAME = 'list_impact_material.txt'
R_FP_FILE_NAME = 'list_impact_resource.txt'
V_FP_FILE_NAME = 'list_impact_v.txt'
JOB_FP_FILE_NAME = 'list_impact_job.txt'
VA_FP_FILE_NAME = 'list_impact_va.txt'
DICT_FP_FILE_NAME = {}
DICT_FP_FILE_NAME['job'] = JOB_FP_FILE_NAME
DICT_FP_FILE_NAME['va'] = VA_FP_FILE_NAME
# Name of processed EXIOBASE pickle.
DICT_EB_PROC_FILE_NAME = 'dict_eb_proc.pkl'

TUP_CBS_REP_CONS = (73, 'Reparatie van consumentenartikelen')
TUP_EB_REP_CONS = ('NL',
                   ('Retail  trade services, except of motor vehicles and '
                    'motorcycles; repair services of personal and household '
                    'goods'))

TUP_CBS_REP_MACH = (27, 'Reparatie en installatie van machines')
TUP_EB_REP_MACH = ('NL', 'Machinery and equipment n.e.c.')

# Files with characterization factors of footprints.
CQE_FILE_NAME = 'Q_emission.txt'
CQM_FILE_NAME = 'Q_material.txt'
CQR_FILE_NAME = 'Q_resource.txt'

# Column names of circular sectors in CBS IO.
IO_CBS_REP_MACH_NAME = 'Reparatie en installatie van machines'
IO_CBS_REP_MACH_ID = '27'
IO_CBS_REP_CONS_NAME = 'Reparatie van consumentenartikelen'
IO_CBS_REP_CONS_ID = '73'

TUP_EB_MARGIN = ('NL', ('Wholesale trade and commission trade services, '
                        'except of motor vehicles and motorcycles'))
# Boolean to save processed EXIOBASE version for future uses.
SAVE_EB = True

# Define file names of log data.
LOG_FILE_NAME = 'log.txt'

# Define log mode for first log.
log_mode = 'w'

# Define region tuples
TUP_NL = ('The Netherlands', ['NL'])

TUP_EU28_NO_NL = ('EU28 ex. the Netherlands', ['SE', 'AT', 'BE', 'BG', 'HR',
                                               'CY', 'CZ', 'DK', 'EE', 'FI',
                                               'FR', 'DE', 'GR', 'HU', 'IE',
                                               'IT', 'LV', 'LT', 'LU', 'MT',
                                               'PL', 'PT', 'RO', 'SK', 'SI',
                                               'ES', 'GB'])

TUP_WORLD_NO_EU28 = ('Rest of World ex. EU28', ['US', 'JP', 'CN', 'CA', 'KR',
                                                'BR', 'IN', 'MX', 'RU', 'AU',
                                                'CH', 'TR', 'TW', 'NO', 'ID',
                                                'ZA', 'WA', 'WL', 'WE', 'WF',
                                                'WM'])


LIST_TUP_REG = [TUP_NL, TUP_EU28_NO_NL, TUP_WORLD_NO_EU28]

TNO_EURO_KILO2MEGA_SCALAR = 1e3

TUP_CF_SCALAR_BASE = ('Global Warming ' + r'[$Pg\/CO_2\/eq.$]',
                      ('Global Warming', 'PgCO2eq.'), 1e12)
TUP_MF_SCALAR_BASE = ('Material use [Mt]',
                      ('Material use', 'Mt'), 1e6)
TUP_WF_SCALAR_BASE = ('Water consumption ' + r'[$Gm^3$]',
                      ('Water consumption', 'Gm3'), 1e3)
TUP_LF_SCALAR_BASE = ('Land use' + r'[$Gm^2$]',
                      ('Land use', 'Gm2'), 1e6)
TUP_JOB_SCALAR_BASE = ('Employment [M]',
                       ('Employment', 'M'), 1e3)
TUP_VA_SCALAR_BASE = ('Value added [T€]',
                      ('Value added', 'T€'), 1e6)

TUP_CF_SCALAR_DELTA = ('Global Warming ' + r'[$Tg\/CO_2\/eq.$]',
                       ('Global Warming', 'TgCO2eq.'), 1e9)
TUP_MF_SCALAR_DELTA = ('Material use [kt]',
                       ('Material use', 'kt'), 1e3)
TUP_WF_SCALAR_DELTA = ('Water consumption ' + r'[$Gm^3$]',
                       ('Water consumption', 'Gm3'), 1e3)
TUP_LF_SCALAR_DELTA = ('Land use' + r'[$Mm^2$]',
                       ('Land use', 'Mm2'), 1e3)
TUP_JOB_SCALAR_DELTA = ('Employment [M]',
                        ('Employment', 'M'), 1e3)
TUP_VA_SCALAR_DELTA = ('Value added [G€]',
                       ('Value added', 'G€'), 1e3)

BASE_NET_FILE_NAME_PATTERN = 'base_net'
BASE_CIRC_FILE_NAME_PATTERN = 'base_circ'
BASE_PRIM_FILE_NAME_PATTERN = 'base_prim'

DELTA_NET_FILE_NAME_PATTERN = 'delta_net'
DELTA_CIRC_FILE_NAME_PATTERN = 'delta_circ'
DELTA_PRIM_FILE_NAME_PATTERN = 'delta_prim'

LIST_MEAS_ID_SHORT_LONG_FILE_NAME = 'list_meas_id_short_long.txt'
