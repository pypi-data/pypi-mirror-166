from fugen.enums import FilePath
import importlib.resources
import json
import csv


class OkvedCode(object):
    """This is a class for okved code"""

    def __init__(self, arguments):
        """Initialize attributes
        :param arguments: key-value data about okved code
        """
        self.__dict__ = arguments

    def __str__(self):
        return f'id: {self.ID}, name: {self.Name}'

    def __repr__(self):
        return str(self.__dict__)


class OkvedGenerator(object):
    """Class for Okved Branches generator"""

    def __init__(self, file_path=FilePath.OKVED_JSON_PATH):
        """Initialize attributes
        :param file_path: path to json with okved codes data
            When set to `None` then default json path is used
        """
        self.okved_codes = []
        with importlib.resources.open_text("fugen.data", file_path, encoding="ISO-8859-1") as okved_data_json:
            okved_data = json.load(okved_data_json)
            self.header = okved_data['header']
            for okved_code_json in okved_data['data']:
                self.okved_codes.append(OkvedCode(okved_code_json))

    def to_csv(self, file_path, header=None, encoding='windows-1251'):
        """Write okved codes information to csv file
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
            for okved_code in self.okved_codes:
                csv_writer.writerow([okved_code.__dict__.get(key) for key in header])

    def to_list(self, header=None):
        """Returns list of okved codes and their attributes
        :param header: fields that will be presented in list
            When set to `None` then header from json is used
        :returns list of lists, each of them contains information about okved code
        """
        if not header:
            header = self.header
        return [[okved_code.__dict__.get(key) for key in header] for okved_code in self.okved_codes]

    def to_json(self, file_path, header=None, encoding='windows-1251', ensure_ascii=False):
        """Write okved code information to json file
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
            for okved_code in self.okved_codes:
                data.append(dict([(key, okved_code.__dict__.get(key)) for key in header]))
            json.dump({'data': data}, file, ensure_ascii=ensure_ascii)
