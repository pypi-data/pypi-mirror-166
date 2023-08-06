#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from shutil import copy
import xlwings as xw
from .error import Error
from .excel import sheet_with_name, close_wb


def create_warnings_file(template_file_path: str, folder_path: str, keywords: str, recover: bool = True):
    file_name = '{}.warnings.xlsx'.format(keywords)
    file_path = os.path.join(folder_path, file_name)

    if not recover:
        i = 0
        while os.path.exists(file_path):
            file_name = '{}.warnings.{}.xlsx'.format(keywords, i)
            file_path = os.path.join(folder_path, file_name)
            i += 1

    copy(template_file_path, file_path)
    return file_path


def write_warnings(err: Error, file_path: str, excel_app: xw.App):
    if err.has_error() or not err.has_warning():
        return

    wb = excel_app.books.open(file_path)
    try:
        sht = sheet_with_name(err, wb, 'Warnings')
        if err.has_error():
            return

        row_num = 2
        for warning in err.warnings:
            sht.range((row_num, 'A')).value = warning['file']
            sht.range((row_num, 'B')).value = warning['sheet']
            sht.range((row_num, 'C')).value = warning['row']
            sht.range((row_num, 'D')).value = warning['details']
            row_num += 1

        if not err.has_error():
            wb.save(file_path)
    finally:
        close_wb(wb)
