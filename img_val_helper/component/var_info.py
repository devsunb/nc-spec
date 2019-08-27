import re

import numpy as np

from img_val_helper.component.plot import save_plot_img


class VarInfo:
    def __init__(self, var_name, var):
        self.r = re.compile('.*(\\d+).*')
        self.wav_band_dict = {380: 1, 412: 2, 443: 3, 490: 4, 510: 5,
                              555: 6, 620: 7, 660: 8, 680: 9, 709: 10, 745: 11, 865: 12}
        self.var_name = var_name
        self.var = var
        self.dtype = var.dtype
        self.shape = var.shape
        self.fill_value = var._FillValue if hasattr(var, '_FillValue') else None
        self.band = self._get_band()
        self.avg, self.min, self.max, self.nan_ratio = self._get_statistics()
        self.img_path = save_plot_img(var[:], var_name)

    def _get_band(self):
        match = self.r.match(self.var_name)
        if not match:
            return 0
        band = int(match.groups()[0])
        if band > 12:
            band = self.wav_band_dict[band]
        return band

    def _get_statistics(self):
        data = np.ma.masked_invalid(self.var[:])
        data.set_fill_value(self.fill_value)
        data[data == self.fill_value] = np.ma.masked
        data_avg = np.mean(data)
        data_min = np.ma.min(data)
        data_max = np.ma.max(data)
        data_nan_ratio = np.sum(~data.mask) / data.size
        return data_avg, data_min, data_max, data_nan_ratio
