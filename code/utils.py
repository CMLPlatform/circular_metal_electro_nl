# -*- coding: utf-8 -*-
""" Utilities for script of paper on
    Global environmental and socio-economic impacts of a transition to a
    circular economy in metal and electrical products: a Dutch case-study

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

import cfg


def log(str_log):
    """ Log console output to file.

    """
    print('\n{}'.format(str_log))
    with open(cfg.LOG_DIR_PATH+cfg.LOG_FILE_NAME, cfg.log_mode) as write_file:
        csv_file = csv.writer(write_file,
                              delimiter='\t',
                              lineterminator='\n')
        csv_file.writerow([str_log])


def makedirs():
    """ Make directories for results, tests, and logs.

    """
    list_log_makedirs = []
    list_log_makedirs.append('Making output directories in:')
    list_log_makedirs.append('    {}'.format(cfg.OUTPUT_DIR_PATH))
    for output_dir_path in cfg.LIST_OUTPUT_DIR_PATH:
        try:
            os.makedirs(output_dir_path)
        except FileExistsError:
            list_log_makedirs.append(
                '    Output directory already exists:')
            list_log_makedirs.append(
                '    {}'.format(output_dir_path))
            list_log_makedirs.append(
                '    This run will overwrite previous output.')
    for log_makedirs in list_log_makedirs:
        log(log_makedirs)
        cfg.log_mode = 'a'
