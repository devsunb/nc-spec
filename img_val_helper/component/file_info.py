import re


class FileInfo:
    def __init__(self, file_name, var_list):
        self.r = re.compile(
            '.*GK2B_GOCI2_L2_(\\d{14})_LA_S(\\d{2})_G\\d{2}_(\\w+).nc')
        self.name_algo_dict = {
            'AC': 'ac-kosc', 'GEO': 'ac-kosc', 'CDOM': 'cdom-kosc', 'CHL': 'chl-kosc', 'IOP': 'iop-kosc', 'KD': 'kd-kosc', 'TSS': 'tss-kosc', 'UW': 'uw-kosc', 'ZSD': 'zsd-kosc', 'CF': 'cf-kapark', 'FA': 'fa-yjpark', 'MF': 'mf-dhkim', 'PP': 'pp-jhnoh', 'RI': 'ri-arl', 'SI': 'si-swhong', 'AEROSOL': 'aerosol-jkim', 'VI': 'vi-kshan', 'LSAB': 'lsab-kshan', 'LSAN': 'lsan-kshan', 'FVBAR': 'fvbar-kshan', 'ACR': 'acr-indi', 'LSSS': 'lsss-yhjo', 'SRL': 'srl-indi', 'FGI': 'fgi-shlee', 'SSC': 'ssc-kapark', 'LC': 'lc-jskim'
        }
        self.file_name = file_name
        self.scene_time, self.slot, self.algo_name, self.output_name = self._regex_file_name(
            file_name)
        self.var_list = var_list

    def _regex_file_name(self, file_name):
        groups = self.r.match(file_name).groups()
        scene_time = groups[0]
        slot = groups[1]
        output_name = groups[2]
        algo_name = self.name_algo_dict[groups[2]]
        return scene_time, slot, algo_name, output_name
