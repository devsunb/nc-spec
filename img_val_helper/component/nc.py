import h5py
import numpy as np
from netCDF4 import Dataset

from img_val_helper.component.string import split_path, join_path


class NCReader:
    def __init__(self, path):
        self.nc = Dataset(path, 'r')
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_nc(self, path):
        if isinstance(path, list):
            path = join_path(path)
        if path == '' or path == '/':
            return self.nc
        return self.nc[path]

    def get_attr(self, path):
        try:
            path_list = split_path(path)
            key = path_list[-1]
            nc = self.get_nc(path_list[:-1])
            return nc.getncattr(key)
        except AttributeError:
            return

    def get_attr_keys(self, path):
        nc = self.get_nc(path)
        return nc.ncattrs()

    def get_group_keys(self, path):
        nc = self.get_nc(path)
        return list(nc.groups)

    def get_dimension(self, path):
        path_list = split_path(path)
        nc = self.get_nc(path_list[:-1])
        return nc.dimensions[path_list[-1]]

    def get_dimension_keys(self, path):
        nc = self.get_nc(path)
        return list(nc.dimensions)

    def get_variable(self, path):
        path_list = split_path(path)
        nc = self.get_nc(path_list[:-1])
        return nc.variables[path_list[-1]][:]

    def get_variable_keys(self, path):
        nc = self.get_nc(path)
        return list(nc.variables)

    def get_compound(self, path):
        self.nc.close()
        with h5py.File(self.path, 'r') as hdf:
            data = np.array(hdf[path])
        self.__init__(self.path)
        dtype = np.dtype(data.dtype)
        dim = data.shape[0]
        return NCCompound(data, dtype, dim)

    def get(self, conf_list):
        result = []
        for conf in conf_list:
            t = conf['type']
            p = conf['path']
            if t == 'attribute':
                result.append(self.get_attr(p))
            elif t == 'compound':
                result.append(self.get_compound(p))
            elif t == 'variable':
                result.append(self.get_variable(p))

    def exists(self, path, item_type='all'):
        path_list = split_path(path)
        name = path_list[-1]
        attr_exist = name in self.get_attr_keys(path_list[:-1])
        dim_exist = name in self.get_dimension_keys(path_list[:-1])
        var_exist = name in self.get_variable_keys(path_list[:-1])
        grp_exist = name in self.get_group_keys(path_list[:-1])
        if item_type == 'all':
            return attr_exist or dim_exist or var_exist or grp_exist
        elif item_type == 'attr':
            return attr_exist
        elif item_type == 'dim':
            return dim_exist
        elif item_type == 'var':
            return var_exist
        elif item_type == 'group':
            return grp_exist

    def close(self):
        return self.nc.close()


class NCWriter(NCReader):
    def __init__(self, path, add=False):
        if not add:
            Dataset(path, 'w').close()
        super().__init__(path)
        self.nc.close()
        self.nc = Dataset(path, 'a')

    def get_nc(self, path):
        if isinstance(path, str):
            path = split_path(path)
        if not path:
            return self.nc
        nc = self.nc
        for p in path:
            if self.exists(nc.path + '/' + p):
                nc = nc[p]
            else:
                nc = nc.createGroup(p)
        return nc

    def set_attr(self, path, attr):
        path_list = split_path(path)
        name = path_list[-1]
        nc = self.get_nc(path_list[:-1])
        nc.setncattr(name, attr)

    def create_group(self, path):
        path_list = split_path(path)
        name = path_list[-1]
        nc = self.get_nc(path_list[:-1])
        nc.createGroup(name)

    def create_dimension(self, path, size, exist_ok=True):
        path_list = split_path(path)
        name = path_list[-1]
        nc = self.get_nc(path_list[:-1])
        if exist_ok and name in self.get_dimension_keys(join_path(path_list[:-1])):
            return
        nc.createDimension(name, size)

    def create_variable(self, path, data, dtype=None, fill_value=None, dims=('number_of_lines', 'pixels_per_line')):
        if not dtype:
            if hasattr(data, 'dtype'):
                dtype = data.dtype
            else:
                dtype = type(data)
                dims = ()
        if not fill_value and hasattr(data, 'fill_value'):
            fill_value = data.fill_value
        path_list = split_path(path)
        name = path_list[-1]
        nc = self.get_nc(path_list[:-1])
        created_var = nc.createVariable(
            name, dtype, dimensions=dims, fill_value=fill_value)
        if dtype is str:
            created_var[0] = data
        else:
            created_var[:] = data[:]

    def create_compound(self, path, compound):
        path_list = split_path(path)
        name = path_list[-1]
        nc = self.get_nc(path_list[:-1])
        compound_type = nc.createCompoundType(compound.dtype, 'compound')
        nc.createDimension('compound_dim', compound.dimension)
        nc.createVariable(name, compound_type, 'compound_dim')[
            :] = compound.data[:]

    def set(self, conf_list):
        for conf in conf_list:
            t = conf['type']
            p = conf['path']
            v = conf['value']
            if t == 'attribute':
                self.set_attr(p, v)
            elif t == 'compound':
                self.create_compound(p, v)
            elif t == 'dimension':
                self.create_dimension(p, v)
            elif t == 'variable':
                dims = conf['dims']
                self.create_variable(p, v, dims=dims)

    def close(self):
        return self.nc.close()


class NCCompound:
    def __init__(self, data, dtype, dimension):
        self.data = data
        self.dtype = dtype
        self.dimension = dimension
