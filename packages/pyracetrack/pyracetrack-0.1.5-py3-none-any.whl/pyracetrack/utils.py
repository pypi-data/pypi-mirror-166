from .track import Track
from enum import Enum
from typing import Optional, List, Dict, Tuple
import json
import os


class TrackNames(Enum):
    s_track = 's_track'
    s_track2 = 's_track2'
    z_track2 = 'z_track'


def clear_folder(folder):
    counter = 0
    if not os.path.isdir(folder):
        print('{} is not a folder'.format(folder))
        return counter
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
            counter += 1
        elif os.path.isdir(fpath):
            counter += clear_folder(fpath)
    return counter

def list_tracks() -> List[str]:
    track_dir = get_track_folder()
    fnames = os.listdir(track_dir)
    fnames = filter(lambda fn: '.json' in fn, fnames)
    fnames = filter(lambda fn: os.path.isfile(os.path.join(track_dir, fn)), fnames)
    fnames = [fn.split('.')[0] for fn in fnames]
    return fnames

def load_track(selection: str=None) -> Track:
    if selection is None:
        selection = 'z_track' 
    fname = selection
    if not fname.endswith('.json'):
        fname = '{}.json'.format(fname)
    track_dir = get_track_folder()
    track_file = os.path.join(track_dir, fname)
    track_dict = {}
    with open(track_file, 'r') as fs:
        track_dict = json.load(fs)
    return Track(track_dict)


def load_model(model_folder: str, model_idx: int=-1) -> str:
    '''
    Load a pre trained model from disk
    '''
    fnames = os.listdir(model_folder)
    fnames.sort()
    fnames = [os.path.join(model_folder, fn) for fn in fnames]
    fnames = filter(lambda fn: '.zip' in fn, fnames)
    fnames = filter(os.path.isfile, fnames)
    fnames = list(fnames)
    return fnames[model_idx]


def get_model_file(fname='model_name'):
    '''
    Load a model from the pre-trained models directory.
    The .zip extensions is added automatically if necessary.
    '''
    models_dir = os.path.join('../../Data/pretrained_models')
    model_file = os.path.join(models_dir, fname)
    return model_file


def get_model_info(run_name: str, info: str):
    config_file = get_config_path(run_name)
    with open(config_file, 'r') as fp:
        data = json.load(fp)
        return data[info]


def get_local():
    local_dir = os.path.join('../../Local')
    return local_dir


def get_track_folder():
    track_dir = os.path.join(get_data_folder(), 'tracks')
    return track_dir

def get_data_folder():
    data_dir = os.path.join('../../Data')
    if os.path.isdir(data_dir):
        return data_dir
    data_dir = os.path.join('../Data')
    return os.path.join(data_dir)


def get_config_path(run_name):
    return os.path.join(get_local(), run_name, 'config.json')


def get_trained_model(run_name: str, model_idx: Optional[int]=-1):
    models_dir = os.path.join(get_local(), run_name, 'models')
    found_models = os.listdir(models_dir)
    found_models = map(lambda fn: os.path.join(models_dir, fn), found_models)
    found_models = filter(lambda fn: '.zip' in fn, found_models)
    found_models = list(found_models)
    found_models.sort()
    if model_idx is None:
        return found_models
    return found_models[model_idx]
