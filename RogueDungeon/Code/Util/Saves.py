import pickle
import os

from Code.Util.SettingsGlobal import SettingsGlobal


def save(obj, name):
    path = _path(name)
    if not _folderExists(_path()):
        _createFolder(_path())
    pickle.dump(obj, open(path, "wb"))


def loadSave(name, default):
    path = _path(name)
    if _fileExists(path):
        obj = pickle.load(open(path, "rb"))
    else:
        obj = default()
    return obj


def _path(name=None):
    if name is None:
        path = SettingsGlobal.SavePath
    else:
        path = SettingsGlobal.SavePath + name + ".p"
    return path


def _folderExists(path):
    return os.path.isdir(path)


def _fileExists(path):
    return os.path.isfile(path)


def _createFolder(path):
    path = path[:-1]
    os.makedirs(path)
