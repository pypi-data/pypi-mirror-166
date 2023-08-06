from datetime import date
import warnings
from fugen.generators.ifns import IfnsGenerator
from fugen.enums import CompanyType, CodeRange, CodeInfo, ControlCoeffitients, Data
from fugen.random_module import random as random_module
import random


class CompanyGenerator:
    """Class for company generation"""
    current_year = date.today().year

    def __init__(self):
        """Initialize attributes"""
        self.ifns_generator = IfnsGenerator()

    def generate_inn(self, company_type='UL', ifns_instance=None):
        """Generates Russian INN code according to russian laws.

        :param company_type - the type of company for which INN is generated
            possible values: 'IP' - 'individual person', 'UL' - 'legal entity', 'FC' - 'foreign company'
            When set to `None` then `UL` is used
        :param ifns_instance - fns branch, instance of IfnsBranch class
        :return string that represents INN code
        """
        if company_type == CompanyType.UNDIVIDUAL_ENTERPRENEUR:
            if not ifns_instance:
                ifns_instance = random.choice(self.ifns_generator.ifns_branches)  # 1-4 символы
            if len(ifns_instance.used_inn_ip_nums) != 1000000:
                if len(ifns_instance.used_inn_ip_nums) < 800000:
                    XXXXXX = random.randint(0, 999999)
                    while XXXXXX in ifns_instance.used_inn_ip_nums:
                        XXXXXX = random.randint(0, 999999)
                else:
                    XXXXXX = random.choice(list(CodeRange.ENTERPRENEUR_INN_CODE_RANGE - ifns_instance.used_inn_ip_nums))
                ifns_instance.used_inn_ip_nums.add(XXXXXX)
                NNNN = ifns_instance.id
                inn_num = NNNN + f'{XXXXXX:06}'
                inn_num += str(sum([int(inn_num[i]) * ControlCoeffitients.ENTERPRENEUR_INN_CONTROL_COEFFS[0][i] for i in range(len(inn_num))]) % 11)[-1]
                inn_ctrl_num = sum([int(inn_num[i]) * ControlCoeffitients.ENTERPRENEUR_INN_CONTROL_COEFFS[1][i] for i in range(len(inn_num))]) % 11
                return inn_num + str(inn_ctrl_num)[-1]
            else:
                raise Exception('There is no INN for IP left in this ifns branch, only 1000000 IP codes is possible for 1 branch')
        elif company_type == CompanyType.FOREIGN_COMPANY:
            if len(self.ifns_generator.used_inn_fc_nums) != 100000:
                if len(self.ifns_generator.used_inn_fc_nums) < 80000:
                    XXXXX = random.randint(0, 99999)
                    while XXXXX in self.ifns_generator.used_inn_fc_nums:
                        XXXXX = random.randint(0, 99999)
                else:
                    XXXXX = random.choice(list(CodeRange.COMPANY_INN_CODE_RANGE - self.ifns_generator.used_inn_fc_nums))
                NNNN = CodeInfo.FOREIGN_COMPANY_INN_SIGN
                self.ifns_generator.used_inn_fc_nums.add(XXXXX)
                inn_num = NNNN + f'{XXXXX:05}'
                inn_ctrl_num = sum([int(inn_num[i]) * ControlCoeffitients.COMPANY_INN_CONTROL_COEFFS[i] for i in range(len(inn_num))]) % 11 % 10
                return inn_num + str(inn_ctrl_num)[-1]
            else:
                raise Exception(
                    'There is no INN for FC left, only 100000 foreign companies is possible')
        elif company_type == CompanyType.RUSSIAN_COMPANY:
            if not ifns_instance:
                ifns_instance = random.choice(self.ifns_generator.ifns_branches)  # 1-4 символы
            if len(ifns_instance.used_inn_ul_nums) != 100000:
                if len(ifns_instance.used_inn_ul_nums) < 80000:
                    XXXXX = random.randint(0, 99999)
                    while XXXXX in ifns_instance.used_inn_ul_nums:
                        XXXXX = random.randint(0, 99999)
                else:
                    XXXXX = random.choice(list(CodeRange.ENTERPRENEUR_INN_CODE_RANGE - ifns_instance.used_egrn_nums))
                ifns_instance.used_inn_ul_nums.add(XXXXX)
                NNNN = ifns_instance.id
                inn_num = NNNN + f'{XXXXX:05}'
                inn_ctrl_num = sum([int(inn_num[i]) * ControlCoeffitients.COMPANY_INN_CONTROL_COEFFS[i] for i in range(len(inn_num))]) % 11 % 10
                return inn_num + str(inn_ctrl_num)[-1]
            else:
                raise Exception('There is no INN for legal entities left in this ifns branch, only 100000 legal entities is possible for 1 branch')
        else:
            print(company_type, CompanyType.RUSSIAN_COMPANY)
            raise Exception("company_type should be in: 'UL', 'IP', 'FC'")

    def generate_kpp(self, ifns_instance=None, kpp_reg_purpose=None):
        """Generates Russian KPP code according to russian laws.

        :param ifns_instance - fns branch, instance of IfnsBranch class
        :param kpp_reg_purpose - company registration purpose
        :return string that represents KPP code
        """
        if not ifns_instance:
            ifns_instance = random.choice(self.ifns_generator.ifns_branches)
        if kpp_reg_purpose not in CodeInfo.SPPUNO:
            if kpp_reg_purpose:
                warnings.warn('Передан не существующий код причины регистрации, будет использован код по умолчанию')
            kpp_reg_purpose = random.choice(CodeInfo.SPPUNO)
        kpp_random_num = random.choice(CodeRange.COMPANY_KPP_CODE_RANGE)
        return ifns_instance.id + kpp_reg_purpose + f'{kpp_random_num:03}'

    def generate_ogrn(self, company_type='UL', ifns_instance=None, reg_year=None):
        """Generates Russian OGRN code according to russian laws.

        :param company_type - the type of company for which INN is generated
        :param possible values: 'IP' - 'individual person', 'UL' - 'legal entity', 'FC' - 'foreign company'
        :param ifns_instance - fns branch, instance of IfnsBranch class
        :param reg_year - integer year of company registration date,
        for all companies older than 2002 ogrn is evaluated as for 2002
        :return string that represents OGRN code
        """
        if not ifns_instance:
            ifns_instance = random.choice(self.ifns_generator.ifns_branches)
        if company_type in ('UL', 'FC'):
            C = random.choice(CodeInfo.COMPANY_OGRN_SIGN)
            if not reg_year:
                GG = f'{random.randint(2002, Data.CURRENT_YEAR) % 100:02}'
            else:
                GG = f'{max(2002, reg_year) % 100:02}'
            KK = ifns_instance.id[:2]
            HH = ifns_instance.id[:-2]
            if len(ifns_instance.used_ogrn_ul_nums[GG]) < 70000:
                XXXXX = random.randint(0, 99999)
                while XXXXX in ifns_instance.used_ogrn_ul_nums[GG]:
                    XXXXX = random.randint(0, 99999)
            else:
                XXXXX = random.choice(list(CodeRange.COMPANY_OGRN_RANGE - ifns_instance.used_ogrn_ul_nums[GG]))
            ifns_instance.used_ogrn_ul_nums[GG].add(f'{XXXXX:05}')
            ogrn_num = C + GG + KK + HH + f'{XXXXX:05}'
            ogrn_ctrl_num = int(ogrn_num) % 11 % 10
            return ogrn_num + str(ogrn_ctrl_num)
        elif company_type == 'IP':
            C = random.choice(CodeInfo.COMPANY_OGRN_SIGN)
            if not reg_year:
                GG = f'{random.randint(2002, Data.CURRENT_YEAR) % 100:02}'
            else:
                GG = f'{max(2002, reg_year) % 100:02}'
            KK = ifns_instance.id[:2]
            HH = ifns_instance.id[:-2]
            if len(ifns_instance.used_ogrn_ip_nums[GG]) < 7000000:
                XXXXXXX = random.randint(0, 9999999)
                while XXXXXXX in ifns_instance.used_ogrn_ip_nums[GG]:
                    XXXXXXX = random.randint(0, 9999999)
            else:
                XXXXXXX = random.choice(list(CodeRange.ENTERPRENEUR_OGRN_RANGE - ifns_instance.used_ogrn_ip_nums[GG]))
            ogrn_num = C + GG + KK + HH + f'{XXXXXXX:07}'
            ogrn_ctrl_num = int(ogrn_num) % 13 % 10
            return ogrn_num + str(ogrn_ctrl_num)
        else:
            raise Exception("company_type should be in: 'UL', 'IP', 'FC'")

    def generate_company(self, inn_code=None, kpp_code=None, ogrn_code=None, company_type=None, reg_date=None, ifns_branch=None, ct_weights=(0.4, 0.4, 0.2)):
        """Generates related data for company
        :param inn_code - company INN code
        :param kpp_code - company KPP code
        :param ogrn_code - company OGRN code
        :param company_type - can be 'UL' - 'legal entity', 'IP' - 'individual person', 'FC' - 'foreign company'
        :param reg_date - company registration date
        :param ifns_branch - company ifns branch
        :param ct_weights - weight distribution for company types:
             'UL' - 'legal entity', 'IP' - 'individual person', 'FC' - 'foreign company' accordingly
        :return Returns instance of Company class
        """
        args = dict()

        if company_type:
            args['company_type'] = company_type
        else:
            args['company_type'] = random.choices((CompanyType.RUSSIAN_COMPANY,
                                                   CompanyType.FOREIGN_COMPANY,
                                                   CompanyType.UNDIVIDUAL_ENTERPRENEUR),
                                                  ct_weights)[0]

        if ifns_branch:
            args['ifns_branch'] = ifns_branch
        else:
            args['ifns_branch'] = random.choice(self.ifns_generator.ifns_branches)
        args['region_code'] = args['ifns_branch'].id[:2]

        if reg_date:
            args['reg_date'] = reg_date
        else:
            args['reg_date'] = random_module.generate_date(date(1991, 12, 25), date.today())

        if inn_code:
            args['inn_code'] = inn_code
        else:
            args['inn_code'] = self.generate_inn(company_type=args['company_type'],
                                                 ifns_instance=args['ifns_branch'])

        if args['company_type'] != 'IP' and kpp_code:
            args['kpp_code'] = kpp_code
        else:
            args['kpp_code'] = self.generate_kpp(ifns_instance=args['ifns_branch'])

        if ogrn_code:
            args['ogrn_code'] = ogrn_code
        else:
            args['ogrn_code'] = self.generate_ogrn(company_type=args['company_type'],
                                                   ifns_instance=args['ifns_branch'],
                                                   reg_year=args['reg_date'].year)
        return Company(args)


class Company:

    def __init__(self, arguments):
        self.__dict__ = arguments

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        str_dict = self.__dict__.copy()
        str_dict['ifns_branch'] = str_dict['ifns_branch'].id
        return str(str_dict)
