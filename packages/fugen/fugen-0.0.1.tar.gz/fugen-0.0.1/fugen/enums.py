"""Implements enums for methods.
Enums from this module are used in method in whole package.
"""
from enum import IntEnum
from datetime import date


class Data(IntEnum):
    CURRENT_YEAR = date.today().year


class CompanyType:
    FOREIGN_COMPANY = 'FC'
    UNDIVIDUAL_ENTERPRENEUR = 'IP'
    RUSSIAN_COMPANY = 'UL'


class CodeRange:
    COMPANY_INN_CODE_RANGE = (0, 100000)
    COMPANY_KPP_CODE_RANGE = (0, 1000)
    COMPANY_OGRN_RANGE = (0, 100000)
    ENTERPRENEUR_INN_CODE_RANGE = (0, 1000000)
    ENTERPRENEUR_OGRN_RANGE = (0, 10000000)


class ControlCoeffitients:
    COMPANY_INN_CONTROL_COEFFS = (2, 4, 10, 3, 5, 9, 4, 6, 8)
    ENTERPRENEUR_INN_CONTROL_COEFFS = ((7, 2, 4, 10, 3, 5, 9, 4, 6, 8), (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8))


class CodeInfo:
    COMPANY_OGRN_SIGN = ('1', '5')
    ENTERPRENEUR_OGRN_SIGN = ('3')
    FOREIGN_COMPANY_INN_SIGN = '9909'
    SPPUNO = ('01', '02', '03', '04', '05', '06', '07', '08', '27', '28', '29', '31', '32', '43', '44', '45', '50')


class FilePath:
    IFNS_JSON_PATH = 'ifns_branches.json'
    OKVED_JSON_PATH = 'okved_codes.json'
