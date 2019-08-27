import logging
import os

from img_val_helper.component.excel import Excel
from img_val_helper.component.file_info import FileInfo
from img_val_helper.component.nc import NCReader
from img_val_helper.component.var_info import VarInfo

logger = logging.getLogger('img_val_helper')


# Image validation helper
class Helper:
    def __init__(self, input_path, output_path):
        logger.debug('Helper __init__')
        print(input_path, output_path)
        self.output_excel = Excel(output_path)
        self.input_nr = NCReader(input_path)
        self.input_vars = self._get_variables('/geophysical_data')
        file_info = FileInfo(input_path, list(self.input_vars))
        self.output_excel.set_file_info(file_info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.output_excel.close()
        self.input_nr.close()

    def run(self):
        logger.debug('Helper run')
        for k in self.input_vars:
            self._run_var(k, self.input_vars[k])

    def _run_var(self, var_name, var):
        var_info = VarInfo(var_name, var)
        self.output_excel.set_var_info(var_info)
        # self.output_excel.set_var_data(var_info.var_name, var[:])

    def _get_variables(self, path):
        variables = self.input_nr.get_nc(path).variables
        group_keys = self.input_nr.get_group_keys(path)
        if group_keys:
            for group_key in group_keys:
                variables.update(self._get_variables(os.path.join(path, group_key)))
        return variables
