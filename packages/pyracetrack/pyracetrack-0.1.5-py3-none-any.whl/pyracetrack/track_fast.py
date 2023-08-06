from .track import Track
import numpy as np


class FastTrack(Track):

    def __init__(self, track_dict: dict):
        '''
        As long as the track is only composed of constant
        curvature elements, we can accelerate computations
        with this class.
        '''
        super().__init__(track_dict)
        num_elems = len(self.track_elems)
        self.num_elems = num_elems
        self.curves = np.zeros((num_elems, 3), dtype='float')
        # precompute curvatures
        dist = 0.0
        for idx, elem in enumerate(self.track_elems):
            elem_len = elem.get_length()
            elem_start = dist
            elem_end = dist + elem_len
            crve = elem.get_curvature(0.5*elem_len)
            self.curves[idx, :] = [crve, elem_start, elem_end]
            dist += elem_len

    def get_curvature(self, dist: np.ndarray):
        '''
        Vectorised computation of curvature
        '''
        result = np.zeros_like(dist)
        curvatures = self.curves[:, 0]
        start_dists = self.curves[:, 1]
        end_dists = self.curves[:, 2]
        for elem_idx in range(self.num_elems):
            starts_after = np.array(dist >= start_dists[elem_idx], dtype='float')
            end_before = np.array(dist < end_dists[elem_idx], dtype='float')
            result += curvatures[elem_idx]*starts_after*end_before
        return result
