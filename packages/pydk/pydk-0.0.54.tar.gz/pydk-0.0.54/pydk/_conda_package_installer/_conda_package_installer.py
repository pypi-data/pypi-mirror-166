
# import packages -------------------------------------------------------------
from ._supporting_functions import _conda_list_to_pandas_df
from ._supporting_functions import _check_installation
from ._supporting_functions import _do_install_conda_pkg
from ._supporting_functions import _check_download_log
from ._supporting_functions import _remove_package


# main class ------------------------------------------------------------------
class conda_package_installer:
    def __init__(self, package_name, channel):

        self._pkg_name = package_name
        self._channel = channel
        self._conda_list_tmp_path = "._tmp.conda_list_table.txt"

    def conda_list(self):
        self._conda_list_df = _conda_list_to_pandas_df(self._conda_list_tmp_path)

    def check_installation(self):
        
        self.conda_list()
        self.installed = _check_installation(
            self._conda_list_df, pkg_name=self._pkg_name
        )
        print("Installed: {}".format(self.installed))
        
    def _do_installation(self):

        self._download_log = _do_install_conda_pkg(self._channel, self._pkg_name)
        self.installed, self._trouble_shoot_msg = _check_download_log(
            self._download_log
        ) 
        
    def install(self):
        
        self.conda_list()
        self.installed = _check_installation(
            self._conda_list_df, pkg_name=self._pkg_name
        )
        if not self.installed:
            self._do_installation()

    def remove_package(self):
        self._rm_log, self.installed = _remove_package(self._pkg_name)
