import os
import shutil
import villagewars

class VillageWarsError(Exception):
    pass

class download:
    def __init__(self):
        self._loc = villagewars.__file__[:11]
        self.version = os.listdir(self._loc)[0]
        self._loc += os.listdir(self._loc)[0]
    def __call__(self, downloadFolder='.'):
        shutil.copytree(self._loc, downloadFolder)
        self.LOCATION = downloadFolder
