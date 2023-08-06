import typing
from typing import Tuple
import scipy.optimize as opt
import math
import numpy as np
from . import geom_utils
from abc import ABC, abstractmethod


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return np.array([x, y])


class Point2D():

    def __init__(self, pos_x: float, pos_y: float):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __add__(self, other: 'Point2D') -> 'Point2D':
        new_x = self.pos_x + other.pos_x
        new_y = self.pos_y + other.pos_y
        new_point = Point2D(new_x, new_y)
        return new_point

    def __sub__(self, other:'Point2D') -> 'Point2D':
        return self + (other * -1.0)

    def __mul__(self, fac: float) -> 'Point2D':
        return Point2D(self.pos_x*fac, self.pos_y*fac)

    def __rmul__(self, fac: float) -> 'Point2D':
        return Point2D(self.pos_x*fac, self.pos_y*fac)

    def coords(self) -> Tuple[float, float]:
        return (self.pos_x, self.pos_y)

    def __str__(self):
        return '(x={x:2.3f}, y={y:2.3f})'.format(x=self.pos_x, y=self.pos_y)

    def as_tuple(self) -> Tuple[float, float]:
        return (self.pos_x, self.pos_y)

    def as_np(self):
        return np.array([self.pos_x, self.pos_y])

    def get_x(self) -> float:
        return self.pos_x

    def get_y(self) -> float:
        return self.pos_y

class TrackPoint():

    def __init__(self, point: 'Point2D', orientation: float):
        """
        point: Point2D
        orientation: Orientation in radians
        """
        self.point: 'Point2D' = point
        self.orientation: float = orientation
        self.curvature: float = float('nan')

    def set_curvature(self, val: float):
        self.curvature = val

    def get_curvature(self) -> float:
        return self.curvature

    def get_orientation(self, mode='rad'):
        output = None
        if mode == 'rad':
            output = self.orientation
        else:
            output = math.degrees(self.orientation)
        return output

    def get_position(self) -> 'Point2D':
        return self.point

    def get_direction(self) -> 'Point2D':
        """
        return a unit vector oriented with this TrackPoint.
        """
        angle = self.orientation
        return Point2D(math.cos(angle), math.sin(angle))

    def get_ortho_direction(self, offset='left') -> 'Point2D':
        '''
        return a unit vector aligned orthogonal with this
        track point (pointing towards the boundary)
        '''
        if offset == 'left':
            angle = self.orientation + math.pi*0.5
        else:
            angle = self.orientation - math.pi*0.5
        return Point2D(math.cos(angle), math.sin(angle))

    def get_bound(self, width: float, which='left') -> Point2D:
        if which == 'left':
            return self.get_position() - 0.5*width*self.get_ortho_direction()
        else:
            return self.get_position() + 0.5*width*self.get_ortho_direction()

    def __str__(self) -> str:
        out_str = '({:2.2f}, {:2.2f}) orientation {:2.2f}'
        px, py = self.get_position().as_tuple()
        angle = self.get_orientation('deg')
        return out_str.format(px, py, angle)

class TrackElement(ABC):

    def __init__(self, start: TrackPoint):
        self.start: TrackPoint = start
        self.prev_elem: 'TrackElement' = None
        self.next_elem: 'TrackElement' = None

    def get_prev_elem(self) -> 'TrackElement':
        return self.prev_elem

    def get_next_elem(self) -> 'TrackElement':
        return self.next_elem

    def set_prev_elem(self, elem):
        self.prev_elem = elem

    def set_next_elem(self, elem):
        self.next_elem = elem

    def has_prev_elem(self) -> bool:
        return (self.get_prev_elem() is not None)

    def has_next_elem(self) -> bool:
        return (self.get_next_elem() is not None)

    def get_start_point(self) -> TrackPoint:
        return self.start

    def update(self):
        self.recompute()
        new_end = self.get_last_point()
        if self.next_elem is not None:
            self.next_elem.start = new_end
            self.next_elem.update()

    @abstractmethod
    def recompute(self):
        pass

    @abstractmethod
    def get_angle(self, dist: float) -> float:
        pass

    @abstractmethod
    def get_pos(self, dist: float) -> 'Point2D':
        pass

    @abstractmethod
    def get_curvature(self, dist: float) -> float:
        pass

    @abstractmethod
    def get_length(self) -> float:
        return -1.0

    @abstractmethod
    def to_dict(self):
        return {}

    def get_num_hitboxes(self) -> int:
        return 16

    def on_elem(self, pos: Tuple[float, float], width: float):
        '''
        Check if position is on the current element.
        '''
        num_hbox = self.get_num_hitboxes()
        hit_boxs = np.zeros((num_hbox, 4, 2))
        sdists = np.linspace(0.0, self.get_length(), num_hbox+1)
        for hidx in range(num_hbox):
            p0, p1 = sdists[hidx:hidx+2]
            hit_boxs[hidx, 0, :] = self.get_point(p0).get_bound(width, 'left').as_np()
            hit_boxs[hidx, 1, :] = self.get_point(p0).get_bound(width, 'right').as_np()
            hit_boxs[hidx, 2, :] = self.get_point(p1).get_bound(width, 'right').as_np()
            hit_boxs[hidx, 3, :] = self.get_point(p1).get_bound(width, 'left').as_np()
        c0, c1, c2, c3 = hit_boxs[:, 0, :], hit_boxs[:, 1, :], hit_boxs[:, 2, :], hit_boxs[:, 3, :]
        pos_mtx = np.zeros((num_hbox, 2))
        pos_mtx[:, 0], pos_mtx[:, 1] = pos[0], pos[1]
        in_hbox = geom_utils.get_point_in_square(pos_mtx, c0, c1, c2, c3, tol=1e-6)
        if np.any(in_hbox):
            return True
        else:
            return False

    def get_last_point(self) -> TrackPoint:
        return self.get_point(self.get_length())

    def get_first_point(self) -> TrackPoint:
        return self.get_point(0.0)

    def get_point(self, dist: float) -> TrackPoint:
        new_pos = self.get_pos(dist)
        new_ori = self.get_angle(dist)
        new_curve = self.get_curvature(dist)
        new_point = TrackPoint(new_pos, new_ori)
        new_point.set_curvature(new_curve)
        return new_point

class StraightElement(TrackElement):
    def __init__(self, start: TrackPoint, length):
        super().__init__(start)
        self.length = length

    def get_angle(self, dist: float) -> float:
        return self.start.get_orientation()

    def get_pos(self, dist) -> 'Point2D':
        start = self.start.get_position()
        direction = self.start.get_direction()
        return start + direction*dist

    def recompute(self):
        pass

    def get_curvature(self, dist: float) -> float:
        return 0.0

    def get_length(self) -> float:
        return self.length

    def to_dict(self):
        out_dict = {}
        out_dict['type'] = 'straight'
        out_dict['length'] = self.length
        return out_dict

class CurveElement(TrackElement):

    def __init__(self, start: TrackPoint, radius: float, angular_dist: float):
        super().__init__(start)
        #print('Curve start:', str(start.point))
        self.radius = radius
        self.angular_dist = angular_dist
        self.recompute()

    def recompute(self):
        # Compute center position
        if self.angular_dist >= 0:
            self.ortho_angle = self.start.get_orientation() - math.pi*0.5
        else:
            self.ortho_angle = self.start.get_orientation() + math.pi*0.5
        # Contains outside normal vector to center
        self.ortho_vec = Point2D(math.cos(self.ortho_angle), math.sin(self.ortho_angle))
        #print('ortho vec', self.radius*self.ortho_vec)
        self.center = self.start.get_position() - (self.ortho_vec * self.radius)
        #print('Center pos: {}'.format(str(self.center)))
        self.length = abs(self.angular_dist * self.radius)

    def get_length(self) -> float:
        return self.length

    def get_angle(self, dist: float) -> float:
        percent = dist / self.length
        return self.start.get_orientation() + percent*self.angular_dist

    def get_curvature(self, dist: float) -> float:
        '''
        Need: C = 1 / R
        length = abs(angular_dist * self.radius)
        -> angular_dist / length = angular_dist / abs(angular_dist*self.radius)
            = sign(angular_dist) / self.radius
        '''
        return self.angular_dist / self.length

    def get_pos(self, dist) -> Point2D:
        angle = self.get_angle(dist)
        if self.angular_dist > 0:
            ortho_angle = angle - math.pi*0.5
        else:
            ortho_angle = angle + math.pi*0.5
        ortho_vec = Point2D(math.cos(ortho_angle), math.sin(ortho_angle))
        point = self.center + self.radius * ortho_vec
        return point

    def to_dict(self):
        out_dict = {}
        out_dict['type'] = 'curve'
        out_dict['radius'] = str(float(self.radius))
        out_dict['angle distance'] = math.degrees(self.angular_dist)
        return out_dict

    def get_direction(self) -> str:
        '''
        returns whether this is a left or right curve
        '''
        return 'left' if self.angular_dist > 0 else 'right'

    def get_direction_flipped(self) -> str:
        '''
        returns whether this is a left or right curve
        '''
        return 'right' if self.angular_dist >= 0 else 'left'

    @staticmethod
    def from_points(start: TrackPoint, last_point: TrackPoint, direction='left') -> 'CurveElement':
        '''
        Reconstruct curve from given points.
        '''
        beta = last_point.get_orientation() - start.get_orientation()
        shift = 0.0
        if direction == 'right' and beta < 0:
            beta += 2.0 * np.pi
            shift = -0.5*np.pi
        if direction == 'left' and beta > 0:
            beta -= 2.0 * np.pi
            shift = +0.5*np.pi
        gamma0 = start.get_orientation() + shift
        gamma1 = last_point.get_orientation() + shift
        print('{} curve with angular distance: {:2.2f}'.format(direction, beta * (180.0 / np.pi)))
        line1 = np.zeros((2, 2))
        line2 = np.zeros((2, 2))
        line1[0, :] = start.get_position().as_np() + 1.0 * np.array([np.cos(gamma0), np.sin(gamma0)])
        line1[1, :] = start.get_position().as_np()
        line2[0, :] = last_point.get_position().as_np() + 1.0 * np.array([np.cos(gamma1), np.sin(gamma1)])
        line2[1, :] = last_point.get_position().as_np()
        isect = line_intersection(line1, line2)
        print('Found intersection at: ', isect)
        radius = np.linalg.norm(start.get_position().as_np() - isect)
        # Make curve
        print('Radius: {:2.2f}'.format(radius))
        return CurveElement(start, radius, beta)

    @staticmethod
    def from_points_scipy(start_point: TrackPoint, end_point: TrackPoint, direction='left') -> 'CurveElement':
        '''
        Reconstruct curve from given points.
        '''
        print('Making curve from {} to {}'.format(str(start_point), str(end_point)))
        obj_out = np.zeros(4)
        angle = end_point.get_orientation()
        obj_out[0:2] = end_point.get_position().as_np()
        obj_out[2:4] = [100.0*np.cos(angle), 100.0*np.sin(angle)]
        def obj(x_vec):
            radius, ang_diff = x_vec[0:2]
            new_curve = CurveElement(start_point, radius, ang_diff)
            end_pos = new_curve.get_last_point()
            out_vec = np.zeros(4)
            angle = end_pos.get_orientation()
            out_vec[0:2] = end_pos.get_position().as_np()
            out_vec[2:4] = [100.0*np.cos(angle), 100.0*np.sin(angle)]
            cost = np.linalg.norm(out_vec - obj_out)
            return cost
        bounds = []
        bounds.append([0.0, 10.0**6.0])
        x0 = np.array([1.0, 1.0])
        if direction == 'right':
            bounds.append([1e-6, +np.pi])
            x0[1] = +1.0
        else:
            bounds.append([-np.pi, -1e-6])
            x0[1] = -1.0
        res = opt.minimize(obj, x0, bounds=bounds)
        rad, adist = res.x
        return CurveElement(start_point, rad, adist)
