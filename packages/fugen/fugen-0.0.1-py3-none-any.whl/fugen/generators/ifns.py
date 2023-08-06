import csv

import importlib.resources
import json
from fugen.enums import FilePath, Data


class IfnsBranch(object):
    """This is a class for ifns branch"""

    def __init__(self, arguments, start_year=1991, end_year=Data.CURRENT_YEAR):
        """Initialize attributes
        :param arguments: key-value data about ifns branch
        :param start_year: year from which companies can be registered in this branch
            When set to `None` then year 1991 is used
        :param end_year: year to which companies can be registered in this branch
            When set to `None` then current year is used
        """
        self.__dict__ = arguments
        self.start_year = start_year
        self.end_year = end_year
        self.used_inn_ul_nums = set()
        self.used_inn_ip_nums = set()
        self.used_ogrn_ul_nums = {}
        for i in range(self.start_year, end_year + 1):
            self.used_ogrn_ul_nums[f'{i%100:02}'] = set()
        self.used_ogrn_ip_nums = {}
        for i in range(self.start_year, end_year + 1):
            self.used_ogrn_ip_nums[f'{i%100:02}'] = set()

    def clear(self):
        """Clears all mutable attributes"""
        self.used_inn_ul_nums = set()
        self.used_inn_ip_nums = set()
        self.used_ogrn_ul_nums = {}
        for i in range(self.start_year, self.end_year + 1):
            self.used_ogrn_ul_nums[f'{i%100:02}'] = set()
        self.used_ogrn_ip_nums = {}
        for i in range(self.start_year, self.end_year + 1):
            self.used_ogrn_ip_nums[f'{i%100:02}'] = set()

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'

    def __repr__(self):
        return str(self.__dict__)


class IfnsGenerator(object):
    """Class for IFNS Branches generator"""

    def __init__(self, file_path=FilePath.IFNS_JSON_PATH):
        """Initialize attributes
        :param file_path: path to json with ifns branches data
            When set to `None` then default json path is used
        """
        self.ifns_branches = []
        self.used_inn_fc_nums = set()
        with importlib.resources.open_text("fugen.data", file_path, encoding="ISO-8859-1") as ifns_data_json:
            ifns_data = json.load(ifns_data_json)
            self.header = ifns_data['header']
            for ifns_branches_json in ifns_data['data']:
                self.ifns_branches.append(IfnsBranch(ifns_branches_json))

    def clear(self):
        """Clears all mutable attributes in all ifns instances"""
        for instance in self.ifns_branches:
            instance.clear()

    def to_csv(self, file_path, header=None, encoding='windows-1251'):
        """Write ifns branch information to csv file
        :param file_path: path to csv file
        :param header: fields that will be presented in csv
            When set to `None` then header from json is used
        :param encoding: encoding
            When set to `None` then `windows-1251` is used
        """
        if not header:
            header = self.header
        with open(file_path, 'w', encoding=encoding, newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            csv_writer.writerow(header)
            for ifns_branch in self.ifns_branches:
                csv_writer.writerow([ifns_branch.__dict__.get(key) for key in header])

    def to_list(self, header=None):
        """Returns list of ifns branches and their attributes
        :param header: fields that will be presented in list
            When set to `None` then header from json is used
        :returns list of lists, each of them contains information about ifns branch
        """
        if not header:
            header = self.header
        return [[ifns_branch.__dict__.get(key) for key in header] for ifns_branch in self.ifns_branches]

    def to_json(self, file_path, header=None, encoding='windows-1251', ensure_ascii=False):
        """Write ifns branch information to json file
        :param file_path: path to json file
        :param header: fields that will be presented in json
            When set to `None` then header from json is used
        :param encoding: json.dumps `encoding` attribute
            When set to `None` then `windows-1251` is used
        :param ensure_ascii: json.dumps `ensure_ascii` attribute
        """
        data = []
        if not header:
            header = self.header
        with open(file_path, 'w', encoding=encoding) as file:
            for ifns_branch in self.ifns_branches:
                data.append(dict([(key, ifns_branch.__dict__.get(key)) for key in header]))
            json.dump({'data': data}, file, ensure_ascii=ensure_ascii)
