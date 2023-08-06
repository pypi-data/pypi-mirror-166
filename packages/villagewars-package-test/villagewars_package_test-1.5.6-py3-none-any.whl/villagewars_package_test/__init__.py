import os
import shutil
import villagewars_package_test as villagewars
class VillageWarsError(Exception):
    pass

class _Download:
    def __init__(self):
        self._loc = villagewars.__file__[:-11]
        print(self._loc)
        listdir = os.listdir(self._loc)
        self.version = [i for i in listdir if i not in ('__init__.py', '__pycache__')][0]
        self._loc += self.version
    def __call__(self, downloadFolder='.'):
        try:
            os.chdir(downloadFolder)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                exc)
        shutil.copytree(self._loc, 'VillageWars/')
        self.LOCATION = downloadFolder

download = _Download()
