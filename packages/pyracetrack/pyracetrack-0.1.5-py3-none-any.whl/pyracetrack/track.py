from .interp_segment import InterpSegment
from .lines import Lines
from .track_element import CurveElement, StraightElement, TrackElement, TrackPoint, Point2D
from .trajectory import Trajectory
from .geom_utils import *
from matplotlib.patches import Polygon
from sympy import geometry
from tikzplot.plotter import Plotter
from tqdm import tqdm
from typing import List, Callable, Optional
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import torch as th


class Track():
    '''
    Track discretisation, able to generate finer discretisations of meshes.
    '''
    def __init__(self, track_dict: dict, verbose: int=0, hb_length: float=8.0):
        '''
        Initialize the track using an initial discretisation given in
        the json format
        '''
        if 'start position' in track_dict:
            start_pos = Point2D(*track_dict['start position'])
        else:
            start_pos = Point2D(0.0, 0.0)
        if 'angle' in track_dict:
            start_angle = track_dict['angle'] * (np.pi / 180.0)
        else:
            start_angle = 0.0
        if 'width' in track_dict:
            self.width: float = float(track_dict['width'])
        else:
            self.width = 10.0
        self.debug_mode: bool = False
        self.start_point = TrackPoint(start_pos, start_angle)
        self.track_elems: List[TrackElement] = []
        self.elem_lens: np.ndarray = None
        self.eps = 1.0
        self.interp_orientations: List[InterpSegment] = []
        self.interp_curvatures: List[InterpSegment] = []
        self.num_elements: int = 0
        self.length: float = 0.0
        self.verbose: int = verbose
        self.lines = None
        if 'elements' in track_dict:
            for elem in track_dict['elements']:
                if elem['type'] == 'straight':
                    length = float(elem['length'])
                    self.add_straight(length)
                elif elem['type'] == 'curve':
                    radius = float(elem['radius'])
                    angle_dist = math.radians(float(elem['angle distance']))
                    self.add_curve(radius, angle_dist)
                else:
                    print('Undefined element type: ', elem['type'])
                    break
        self.length = self.get_length()
        self.make_orientation_curvature()
        self.hb_length: float = hb_length
        if len(self.get_elements()) > 0:
            self.make_hitboxs()
        if self.verbose > 0:
            print('Track has a total length of {}'.format(self.length))

    def get_hitbox_idx(self, pos_x, pos_y) -> int:
        squares = self.hitboxs
        num_hitboxes = self.hitboxs.shape[0]
        points = np.zeros((num_hitboxes, 2))
        points[:, 0], points[:, 1] = pos_x, pos_y
        in_squares = get_point_in_square(points, squares[:, 0, :], squares[:, 1, :], squares[:, 2, :], squares[:, 3, :])
        if np.any(in_squares):
            return np.argmax(in_squares)
        # Check the closes hitbox
        mid_points = np.zeros((num_hitboxes, 2))
        mid_points[:, 0] = np.mean(self.hitboxs[:, :, 0], axis=1)
        mid_points[:, 1] = np.mean(self.hitboxs[:, :, 1], axis=1)
        dists = np.sqrt(np.sum((points - mid_points)**2.0, axis=1))
        return np.argmin(dists)

    def get_nudist(self, pos_x, pos_y):
        '''
        Compute the nu_distance of a single point 
        '''
        idx = self.get_hitbox_idx(pos_x, pos_y)
        # Check if point is on track
        if idx is None:
            return None
        p0p1 = self.hitboxs[idx, [0, 3], :]
        p2p3 = self.hitboxs[idx, [1, 2], :]
        pleft = np.mean(p0p1, axis=0)[None, :]
        pright = np.mean(p2p3, axis=0)[None, :]
        point = np.array([[pos_x, pos_y]])
        # find the orthogonal distance
        proj_point = project_points(point, pleft, pright)
        conn_dir = pright - pleft
        ortho_dir = np.array([-conn_dir[0, 1], conn_dir[0, 0]])
        ortho_dir = ortho_dir / np.linalg.norm(ortho_dir)
        point_diff = (point - proj_point)[0, :]
        nu_dist = np.dot(ortho_dir, point_diff)
        return nu_dist

    def get_sdist(self, pos_x, pos_y):
        '''
        Compute the s_distance of a single point 
        '''
        # Check if points are in square
        idx = self.get_hitbox_idx(pos_x, pos_y)
        if idx is None:
            return None
        p0p1 = self.hitboxs[idx, [0, 3], :]
        p2p3 = self.hitboxs[idx, [1, 2], :]
        pleft = np.mean(p0p1, axis=0)[None, :]
        pright = np.mean(p2p3, axis=0)[None, :]
        point = np.array([[pos_x, pos_y]])
        proj_point = project_points(point, pleft, pright)
        len_base = np.linalg.norm(pright - pleft)
        len_proj = np.linalg.norm(proj_point - pleft)
        rel_len = len_proj / len_base
        s0 = self.hitboxs_sdists[idx, 0]
        len_s = self.hitboxs_sdists[idx, 1] - s0
        my_sdist = s0 + rel_len * len_s
        if np.isnan(my_sdist):
            my_sdist = None
        return my_sdist

    def get_xi_angle(self, pos_x, pos_y, yaw):
        s_dist = self.get_sdist(pos_x, pos_y)
        if s_dist is None:
            return None
        tangle = self.get_point(s_dist).get_orientation()
        rel_angle = yaw - tangle
        return rel_angle

    def make_hitboxs(self):
        last_dist = 0.0
        hb_sdists = []
        for elem in self.get_elements():
            if isinstance(elem, StraightElement):
                npts = 4
            else:
                npts = int(elem.get_length() / self.hb_length + 0.5)
                npts = max(4, npts)
            elen = elem.get_length()
            new_s = np.linspace(last_dist, last_dist+elen, npts)
            last_dist += elem.get_length()
            hb_sdists.extend(list(new_s))
        hb_sdists = list(set(hb_sdists))
        hb_sdists.sort()
        sdist_list = np.array(hb_sdists)
        num = len(sdist_list) - 1
        self.hitboxs = np.zeros((num, 4, 2))
        self.hitboxs_sdists = np.zeros((num, 2))
        self.hb_sdists = np.array(hb_sdists)
        self.hitboxs_a = np.zeros(num)
        track_len = self.get_length()
        wid = self.get_width()
        self.hitboxs_sdists[:, 0] = sdist_list[0:-1]
        self.hitboxs_sdists[:, 1] = sdist_list[1:]
        for idx, (s0, s1) in enumerate(zip(sdist_list[0:-1], sdist_list[1:])):
            p0 = self.get_point(s0).get_bound(wid, 'left')
            p1 = self.get_point(s1).get_bound(wid, 'left')
            p2 = self.get_point(s1).get_bound(wid, 'right')
            p3 = self.get_point(s0).get_bound(wid, 'right')
            dat = np.array([p0.as_np(), p1.as_np(), p2.as_np(), p3.as_np()])
            self.hitboxs[idx, :, :] = dat
        for idx in range(num):
            A = self.hitboxs[idx, 0, :]
            B = self.hitboxs[idx, 1, :]
            C = self.hitboxs[idx, 2, :]
            D = self.hitboxs[idx, 3, :]
            area = 0.5*np.cross(C - A, D - B)
            self.hitboxs_a[idx] = area
            
    def on_track(self, pos):
        '''
        Check if a list of positions is on the track
            pos.shape = (2, )
        '''
        num_hbox = self.hitboxs.shape[0]
        tareas = np.zeros((num_hbox, 4), dtype=np.float64)
        checks = np.zeros((num_hbox, 4), dtype=np.bool8)
        for k in range(4):
            pA = self.hitboxs[:, k, :]
            pB = self.hitboxs[:, (k+1)%4, :]
            pP = np.tile(pos, (num_hbox, 1))
            # Make triangle areas
            xarr = np.array([pA[:, 0], pB[:, 0], pP[:, 0]]).T
            yarr = np.array([pA[:, 1], pB[:, 1], pP[:, 1]]).T
            tareas[:, k] += xarr[:, 0] * (yarr[:, 1] - yarr[:, 2])
            tareas[:, k] += xarr[:, 1] * (yarr[:, 2] - yarr[:, 0])
            tareas[:, k] += xarr[:, 2] * (yarr[:, 0] - yarr[:, 1])
            tareas[:, k] = 0.5*np.abs(tareas[:, k])
        qareas = np.sum(tareas, axis=1)
        area_diffs = abs(self.hitboxs_a - qareas)
        on_ele = np.min(area_diffs) < 1e-6
        return on_ele

    def get_elements(self) -> List[TrackElement]:
        return self.track_elems

    def get_elem_lens(self) -> np.ndarray:
        nele = len(self.get_elements())
        elens = np.zeros((nele, 2))
        clen: float = 0.0
        for eidx, ele in enumerate(self.get_elements()):
            my_len = ele.get_length()
            elens[eidx, :] = [clen, clen+my_len]
            clen += my_len
        return elens

    def set_start(self, px, py, angle, width):
        pstart = Point2D(px, py)
        self.start_point = TrackPoint(pstart, angle)
        self.width = width

    def get_width(self) -> float:
        return self.width

    def get_last_point(self) -> TrackPoint:
        if len(self.track_elems) == 0:
            return self.start_point
        last_elem = self.track_elems[-1]
        elem_len = last_elem.get_length()
        fin_point = last_elem.get_point(elem_len)
        # print('last point in track:', fin_point.get_position().as_tuple())
        return fin_point

    def get_position(self, s_dist: float, nu_dist: float) -> 'Point2D':
        point = self.get_point(s_dist)
        return point.get_position() + nu_dist * point.get_ortho_direction()

    def remove_last_elem(self):
        if len(self.track_elems) == 0:
            return
        elem = self.track_elems.pop()
        elem.set_prev_elem(None)
        if len(self.get_elements())>0:
            self.track_elems[-1].set_next_elem(None)
        self.length = self.length - elem.get_length()

    def get_elements(self) -> List[TrackElement]:
        return self.track_elems

    def get_num_elements(self) -> int:
        return self.num_elements

    def update_element_lengths(self):
        # Recompute the element lengths
        if self.get_num_elements() < 1:
            return
        elens = np.zeros(self.get_num_elements(), dtype=np.float64)
        for idx, elem in enumerate(self.get_elements()):
            elens[idx] = elem.get_length()
        self.elem_lens = elens
        self.length = np.sum(self.elem_lens)

    def add_elem(self, elem: TrackElement):
        if len(self.track_elems) > 0:
            last_elem = self.track_elems[-1]
            last_elem.set_next_elem(elem)
        self.track_elems.append(elem)
        self.num_elements = len(self.track_elems)
        self.length = self.length + elem.get_length()
        if self.verbose > 1:
            elen = elem.get_length()
            print('added a track element of length: {}'.format(elen))
        self.update_element_lengths()

    def add_straight(self, length: float):
        new_elem = StraightElement(self.get_last_point(), length)
        self.add_elem(new_elem)

    def add_curve(self, radius: float, angle_dist: float):
        new_elem = CurveElement(self.get_last_point(), radius, angle_dist)
        self.add_elem(new_elem)

    def get_length(self) -> float:
        """
        returns total track length
        """
        # Compile lengths for elements
        return self.length

    def to_dict(self):
        out_dict = {}
        out_dict['start position'] = list(self.start_point.get_position().as_tuple())
        out_dict['angle'] = self.start_point.get_orientation(mode='degree')
        out_dict['width'] = self.width
        out_dict['elements'] = []
        # Add bounds
        for elem in self.track_elems:
            out_dict['elements'].append(elem.to_dict())
        return out_dict

    def get_point(self, dist) -> TrackPoint:
        '''
        returns the track point at a given distance
        '''
        tol = 1e-4
        if dist < 0-tol or dist > self.get_length() - tol:
            msg = 'Warning: tried evaluating track point at distance {}'
            print(msg.format(dist))
            dist = max(1e-5, dist)
            dist = min(self.get_length()-tol, dist)
        dist_left = dist
        #zero_padded_elens = np.zeros(1+self.get_num_elements(), dtype=np.float64)
        #zero_padded_elens[1:] = self.elem_lens
        #summed_lens = np.cumsum(zero_padded_elens)
        #first_match = np.where(summed_lens > dist-eps)[0][0] - 1
        #pos_in_elem: float = dist - zero_padded_elens[first_match]
        #elem = self.get_elements()[first_match]
        #return elem.get_point(pos_in_elem)
        for idx, elem in enumerate(self.track_elems):
            if elem.length <= dist_left:
                # discard this track element
                dist_left = dist_left - elem.length
            else:
                # found the correct element
                return elem.get_point(dist_left)
        # Not found -> get extracted point from last element
        if len(self.track_elems) > 0:
            return self.track_elems[-1].get_point(dist_left)
        # Have not found a correct track element.
        return self.start_point

    def get_element(self, dist) -> TrackElement:
        idx = self.get_elem_id(dist)
        return self.get_elements()[idx]

    def get_elem_id(self, dist) -> int:
        """
        Find the ID of a corresponding track element.
        """
        # compute end lengths
        if dist < 0 or dist > self.get_length():
            #print('Warning: element position ill-defined {}'.format(dist))
            pass
        if dist < 0:
            return 0
        if dist > self.get_length():
            return len(self.get_elements()) - 1
        # Compute the correct element in between
        elem_lens = [e.get_length() for e in self.get_elements()]
        elem_lens_csum = np.cumsum(elem_lens)
        tot_len = 0.0
        for eid, elem in enumerate(self.get_elements()):
            tot_len += elem.get_length()
            if dist <= tot_len:
                return eid
        return len(self.get_elements())-1

    def get_partial_length(self, elem_id) -> float:
        """
        Compute the length of elements before the current index
        """
        elens = np.zeros(self.num_elements+1) 
        elens[1:] = self.elem_lens
        cum_sum_elens = elens.cumsum()
        return cum_sum_elens[elem_id]

    def get_curvature(self, dist) -> Optional[float]:
        if dist < 0.0:
            return self.get_curvature(0.0)
        elif dist > self.get_length():
            return self.get_curvature(self.get_length())
        # Get summed lengths
        elem_lens = [e.get_length() for e in self.get_elements()] 
        elem_lens_csum = np.cumsum(elem_lens)
        eid = self.get_elem_id(dist)
        elem = self.get_elements()[eid]
        dist_in_elem = dist - (elem_lens_csum[eid] - elem_lens[eid])
        eps: float = 1.0
        cur_curvature: float = elem.get_curvature(dist_in_elem)
        # Values for interpolation
        if dist_in_elem < eps:
            # Interpolate with element before, if possible
            cur_curvature: float = elem.get_curvature(eps)
            prev_curvature: float = cur_curvature
            if eid > 0:
                prev_elem = self.get_elements()[eid-1]
                prev_curvature = prev_elem.get_curvature(prev_elem.get_length()-eps)
            interp = (dist_in_elem + eps) / (2.0*eps)
            if interp < 0.0 or interp > 1.0:
                print('interpolation error at start of elem')
                print('eid:', eid)
                print('interp:', interp)
                print('\n')
            return smooth_step(prev_curvature, cur_curvature, interp)
        if dist_in_elem > elem_lens[eid] - eps:
            cur_curvature: float = elem.get_curvature(elem.get_length()-eps)
            interp = (dist_in_elem - elem_lens[eid] + eps) / (2.0*eps)
            if interp < 0.0 or interp > 1.0:
                print('interpolation error at end of elem: {:2.2f}'.format(interp))
            next_curvature: float = cur_curvature
            if eid < len(self.get_elements())-1:
                next_elem = self.get_elements()[eid+1]
                next_curvature = next_elem.get_curvature(eps)
            return smooth_step(cur_curvature, next_curvature, interp)
        return cur_curvature

    def visualize(self, res=200, render=False, draw_center=False):
        ax = plt.gca()
        length_space = np.linspace(0.0, self.get_length(), res)
        points: List[TrackPoint] = [self.get_point(l) for l in length_space]
        xbounds = np.array([10**100, -10**100])
        ybounds = np.copy(xbounds)
        for p0, p1 in zip(points[0:-1], points[1:]):
            # Compute corners
            corners = np.zeros((4, 2))
            corners[0, :] = p0.get_bound(self.width, which='left').coords()
            corners[1, :] = p1.get_bound(self.width, which='left').coords()
            corners[2, :] = p1.get_bound(self.width, which='right').coords()
            corners[3, :] = p0.get_bound(self.width, which='right').coords()
            xbounds[0] = min(xbounds[0], min(corners[:, 0]))
            ybounds[0] = min(ybounds[0], min(corners[:, 1]))
            xbounds[1] = max(xbounds[1], max(corners[:, 0]))
            ybounds[1] = max(ybounds[1], max(corners[:, 1]))
            poly = Polygon(corners, closed=True, alpha=0.5, color='red')
            ax.add_patch(poly)
        # Draw center line:
        plt.xlim(*xbounds)
        plt.ylim(*ybounds)
        if draw_center:
            cline = np.zeros((res, 2))
            for idx, dist in enumerate(length_space):
                track_point: TrackPoint = self.get_point(dist)
                cline[idx, :] = track_point.point.coords()
            plt.plot(cline[:, 0], cline[:, 1])
        if render:
            plt.savefig('track_figure.png', dpi=600, bbox_inches='tight')
            plt.show()

    def visualize_trajectory(self, traj: Trajectory):
        self.visualize()
        traj.visualize()

    def vis_track_bound(self, plotter, sdists, scale: float):
        width = self.get_width()
        points_l = [self.get_point(s).get_bound(width, 'left') for s in sdists]
        points_r = [self.get_point(s).get_bound(width, 'right') for s in sdists]
        points = list(zip(points_l[0:-1], points_l[1:])) + [(False, False)] + list(zip(points_r[0:-1], points_r[1:]))
        pstart = self.get_position(0.0, 0.0).as_np()
        rw = True
        for p0, p1 in zip(sdists[0:-1], sdists[1:]):
            if rw:
                rw = False
                color = (0.8, 0.1, 0.1)
            else:
                rw = True
                color = (0.8, 0.8, 0.8)
            # Draw connection line
            my_sdists = np.linspace(p0-0.01, p1+0.01, 8)
            points_l = [self.get_point(s).get_bound(width, 'left') for s in my_sdists]
            points_r = [self.get_point(s).get_bound(width, 'right') for s in my_sdists]
            pmtx_l = (np.array([p.as_np() for p in points_l]) - pstart) * scale
            pmtx_r = (np.array([p.as_np() for p in points_r]) - pstart) * scale
            lwidth = scale * 40.0
            plotter.plot_poly(pmtx_l[:, 0], pmtx_l[:, 1], color=color, closed=False, linewidth=lwidth)
            plotter.plot_poly(pmtx_r[:, 0], pmtx_r[:, 1], color=color, closed=False, linewidth=lwidth)

    def visualize_tikz(self, s_dists, track_name: str, scale: float=0.1, traj: Trajectory=None, plot_nodes=True, save_fig=True, mark=True):
        # Draw the track 
        #num = int(round(track.get_length() / res))
        num = len(s_dists)
        plotter = Plotter()
        points = [self.get_point(s) for s in s_dists]
        positions = np.zeros((2*num, 2))
        twidth = self.get_width()
        x0, y0 = self.get_position(0.0, 0.0).as_tuple()
        # Plot the nodes
        for idx, p in tqdm(list(enumerate(points))):
            positions[idx, :] = p.get_bound(twidth, 'left').as_np()
            positions[-idx-1, :] = p.get_bound(twidth, 'right').as_np()
        # Plot the asphalt
        positions_asph = np.zeros((2*num*6, 2))
        points_asph = [self.get_point(s) for s in np.linspace(s_dists[0], s_dists[-1], num=num*6)]
        for idx, p in tqdm(list(enumerate(points_asph))):
            positions_asph[idx, :] = p.get_bound(twidth, 'left').as_np()
            positions_asph[-idx-1, :] = p.get_bound(twidth, 'right').as_np()
        xarr = (positions_asph[:, 0] - x0) * scale
        yarr = (positions_asph[:, 1] - y0) * scale
        plotter.plot_poly(xarr, yarr, closed=True, color=(0.2667, 0.2667, 0.2667), opacity=0.9)
        # Mark the first and last element
        if mark:
            plotter.plot_poly(xarr[[0, 1, -2, -1]], yarr[[0, 1, -2, -1]],
                    closed=True, color=(0.05, 0.05, 0.5), opacity=0.9)
            plotter.plot_poly(xarr[[num-2, num-1, num, num+1]], yarr[[num-2, num-1, num, num+1]],
                    closed=True, color=(0.5, 0.05, 0.05), opacity=0.9)
        # Plot the nodes
        if plot_nodes:
            for idx, p in tqdm(list(enumerate(points))):
                p0 = p.get_bound(twidth, which='left').as_np()
                p1 = p.get_bound(twidth, which='right').as_np()
                xarr = scale*(np.array([p0[0], p1[0]]) - x0)
                yarr = scale*(np.array([p0[1], p1[1]]) - y0)
                # plot the track nodes
                plotter.plot_poly(xarr, yarr, closed=False, color=(0.1, 0.1, 0.1), opacity=0.8, linewidth=2.0)
        #mids = np.array([self.get_position(s, 0.0).as_np() for s in s_dists])
        #plotter.scatter(mids[:, 0], mids[:, 1], color=(0.667, 0.667, 0.667))
        # Plot the trajectory
        if traj is not None:
            xarr = (traj.xpos - x0) * scale
            yarr = (traj.ypos - y0) * scale
            plotter.plot_poly(xarr, yarr, closed=False, color=(0.5, 0.5, 1.0), opacity=0.9, linewidth=3.0)
        num = int(round(self.get_length() / 5.0))
        sdists2 = np.linspace(min(s_dists), max(s_dists), num=num)
        self.vis_track_bound(plotter, sdists2, scale)
        if save_fig:
            plot_name = 'vis_{}'.format(track_name)
            plotter.save(plot_name)
        return plotter

    def generate_line_disc(self, res):
        '''
        Generates line discretisation of this track.
        '''
        dists = np.linspace(0.0, self.get_length(), num=res+1)[1:]
        last_point = self.get_point(0.0)
        points_0 = np.zeros((2*res, 2))
        points_1 = np.zeros((2*res, 2))
        for k, dist in enumerate(dists):
            new_point = self.get_point(dist)
            last_left = last_point.get_bound(self.width, which='left')
            last_right = last_point.get_bound(self.width, which='right')
            new_left = new_point.get_bound(self.width, which='left')
            new_right = new_point.get_bound(self.width, which='right')
            # Make line segment
            points_0[k, :] = last_left.as_tuple()
            points_1[k, :] = new_left.as_tuple()
            points_0[k+res, :] = last_right.as_tuple()
            points_1[k+res, :] = new_right.as_tuple()
            last_point = new_point
        lines = Lines(points_0, points_1)
        # print('created discretized track using {} line segments'.format(2*res))
        self.lines = lines

    def get_ray_dists(self, point, angles):
        '''
        Computes how far the rays reach into this track from a central
        point located at 'point'.
        '''
        if self.lines is None:
            self.generate_line_disc(50)
        ray_dists = np.zeros(len(angles))
        for k, angle in enumerate(angles):
            vec = np.array([np.cos(angle), np.sin(angle)])
            cross_points, valid = self.lines.ray_intersectin(point, vec)
            point_diffs = cross_points
            point_diffs[:, 0] = cross_points[:, 0] - point[0]
            point_diffs[:, 1] = cross_points[:, 1] - point[1]
            dists = np.linalg.norm(point_diffs, axis=1)
            if not np.any(valid):
                ray_dists[k] = 1000.0
            else:
                ray_dists[k] = np.min(dists[valid])
        return ray_dists

    def make_clone(self) -> 'Track':
        my_dict = self.to_dict()
        return Track(my_dict)

    def make_orientation_curvature(self):
        """
        Precompute the track orientation as a list of interpolation segments
        """
        self.interp_orientations: List[InterpSegment] = []
        self.interp_curvatures: List[InterpSegment] = []
        dist = 0.0
        for idx, elem in enumerate(self.track_elems):
            oleft = elem.get_first_point().get_orientation()
            oright = elem.get_last_point().get_orientation()
            cleft = elem.get_curvature(0.0)
            cright = elem.get_curvature(elem.get_length())
            if elem.has_next_elem():
                # has previous and next element
                distl = dist + self.eps if elem.has_prev_elem() else dist
                distr = dist + elem.get_length() - self.eps
                self.interp_orientations.append(InterpSegment(distl, distr, oleft, oright))
                self.interp_curvatures.append(InterpSegment(distl, distr, cleft, cright))
                # add interpolation segment
                distl = dist + elem.get_length() - self.eps
                distr = dist + elem.get_length() + self.eps
                oleft_next = elem.get_next_elem().get_first_point().get_orientation()
                cleft_next = elem.get_next_elem().get_curvature(0.0)
                new_seg = InterpSegment(distl, distr, oright, oleft_next)
                self.interp_orientations.append(InterpSegment(distl, distr, oright, oleft_next))
                self.interp_curvatures.append(InterpSegment(distl, distr, cright, cleft_next))
            else:
                # Does not have next element
                distl = dist + self.eps if elem.has_prev_elem() else dist
                distr = dist + elem.get_length()
                # new_seg = InterpSegment(distl, distr, oleft, oright)
                self.interp_orientations.append(InterpSegment(distl, distr, oleft, oright))
                self.interp_curvatures.append(InterpSegment(distl, distr, cleft, cright))
                # Extend by an element to make the mask work correctly
                self.interp_orientations.append(InterpSegment(distr, distr+1.0, oright, oright))
                self.interp_curvatures.append(InterpSegment(distr, distr+1.0, cright, cright))
            dist += elem.get_length()

    def get_orientations_th(self, s_dist_th: th.Tensor):
        """
        Get the track curvatures at the given track points.
        This is required to get potential derivatives for track orientation
        using the torch automatic differentiation framework.
        """
        out = 0.0*s_dist_th
        for seg in self.interp_orientations:
            out += seg.get_value(s_dist_th)
        return out

    def get_curvatures_th(self, s_dist_th: th.Tensor):
        """
        Get the track curvatures at the given track points.
        This is required to get potential derivatives for track orientation
        using the torch automatic differentiation framework.
        """
        out = 0.0*s_dist_th
        for seg in self.interp_curvatures:
            out += seg.get_value(s_dist_th)
        return out

    def scale(self, scale_fac: float) -> 'Track':
        '''
        Get a scaled version of this track.
        '''
        tdict = {} 
        tdict['start position'] = self.start_point.get_position().as_tuple()
        tdict['angle'] = self.start_point.get_orientation(mode='degree')
        tdict['width'] = self.get_width()
        tdict['elements'] = []
        for elem in self.get_elements():
            edict = {}
            if isinstance(elem, StraightElement):
                # Scale the straight elem
                edict['type'] = 'straight'
                edict['length'] = elem.get_length() * scale_fac
            elif isinstance(elem, CurveElement):
                edict['type'] = 'curve'
                edict['radius'] =  elem.radius * scale_fac
                edict['angle distance'] = np.rad2deg(elem.angular_dist)
            else:
                raise ValueError('Unknown element type')
            tdict['elements'].append(edict)
        new_track = Track(tdict)
        return new_track

    @staticmethod
    def load(fname: str) -> 'Track':
        with open(fname, 'r') as fs:
            data = json.load(fs)
        track = Track(data)
        tlen = track.get_length()
        print('Loaded track of length {} from {}'.format(tlen, fname))
        return track

    def save(self, fname: str):
        data = self.to_dict()
        with open(fname, 'w') as fs:
            json.dump(data, fs, indent=4)
        print('Saved track of length {} to {}'.format(self.get_length(), fname))
        

def smooth_step(val_left: float, val_right: float, pos_x: float):
    if pos_x < 0.0:
        return val_left
    elif pos_x > 1.0:
        return val_right
    lam = 6.0*(pos_x**5) - 15.0*(pos_x**4) + 10.0*(pos_x**3)
    return lam*val_right + (1.0-lam)*val_left
