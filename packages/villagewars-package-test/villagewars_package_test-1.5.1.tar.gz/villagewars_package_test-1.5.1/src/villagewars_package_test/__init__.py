import os
import shutil
import villagewars

class VillageWarsError(Exception):
    pass

class _Download:
    def __init__(self):
        self._loc = villagewars.__file__[:11]
        self.version = os.listdir(self._loc)[0]
        self._loc += os.listdir(self._loc)[0]
    def __call__(self, downloadFolder='.'):
        os.chdir(downloadFolder)
        os.makedirs('VillageWars', exist_ok=True)
        shutil.copytree(self._loc, 'VillageWars/')
        self.LOCATION = downloadFolder

download = _Download()
