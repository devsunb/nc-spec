FROM python:3
LABEL maintainer="leejs@satreci.com"

RUN apt-get update && apt-get install -y libhdf4-dev
RUN pip install requests bs4
RUN pip install numpy netcdf4 h5py scipy
RUN pip install python-dateutil
RUN pip install pyyaml
RUN pip install mymodule
RUN pip install xarray
RUN pip install pyhdf

WORKDIR /

COPY gopt-*-py3-none-any.whl /
COPY run.py /
RUN pip install gopt-*-py3-none-any.whl && rm -rf gopt-*-py3-none-any.whl

ENTRYPOINT ["python", "/run.py"]
