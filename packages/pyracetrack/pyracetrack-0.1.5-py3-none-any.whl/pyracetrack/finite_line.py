import numpy as np
import numba
from typing import List, Tuple
import torch as th

coord2d = Tuple[float, float]

@numba.jit(nopython=True)
def get_intersect(a1, a2, b1, b2):
    """ 
    Returns the point of intersection of the lines passing through a2, a1 and b2, b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack((a1, a2, b1, b2))        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    valid = (z > 1e-6)
    fac = max(z, 1e-6)
    point = np.array([x/fac, y/fac])
    return point, valid

@numba.jit(nopython=True)
def magnitude(vector):
   return np.sqrt(np.dot(np.array(vector),np.array(vector)))

@numba.jit(nopython=True)
def norm(vector):
   return np.array(vector)/magnitude(np.array(vector))

@numba.jit(nopython=True)
def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

@numba.jit(nopython=True)
def lineRayIntersectionPoint(rayOrigin, rayDirection, point1, point2):
    # Ray-Line Segment Intersection Test in 2D
    # http://bit.ly/1CoxdrG
    v1 = rayOrigin - point1
    v2 = point2 - point1
    v3 = np.array([-rayDirection[1], rayDirection[0]])
    dnum = np.dot(v2, v3)
    if abs(dnum) < 1e-10:
        return rayOrigin, False
    t1 = cross(v2, v1) / dnum
    t2 = np.dot(v1, v3) / dnum
    if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
        return rayOrigin + t1 * rayDirection, True
    else:
        return rayOrigin, False

def line_ray_intersection_torch(ray_origin: th.Tensor, ray_direction: th.Tensor, point1: th.Tensor, point2: th.Tensor):
    '''
    Compute multiple ray, line intersection.
    '''
    device = ray_origin.device
    num = ray_origin.shape[0]
    # Prepare the results
    ipoint = th.clone(ray_origin)
    valids = th.zeros(num, dtype=th.bool, device=device)
    # Computations
    v1 = ray_origin - point1
    v2 = point2 - point1
    v3 = th.stack([-ray_direction[:, 1], ray_direction[:, 0]]).T
    #v3[:, 0] = -1.0*ray_direction[:, 1]
    #v3[:, 1] = +1.0*ray_direction[:, 0]
    dnum = th.sum(v2*v3, dim=1)
    mask = (th.abs(dnum)  >= 1e-10)
    # Select the entries with possible intersection
    v1i = v1[mask]
    v2i = v2[mask]
    v3i = v3[mask]
    dnumi = dnum[mask]
    t1 = (v2i[:, 0]*v1i[:, 1] - v2i[:, 1]*v1i[:, 0]) / dnumi
    t2 = th.sum(v1i*v3i, dim=1) / dnumi
    mask2 = t1 >= 0.0
    mask2 = th.logical_and(t2 >= 0.0, mask2)
    mask2 = th.logical_and(t2 <= 1.0, mask2)
    mask2_ = th.zeros(th.sum(mask), dtype=th.bool, device=device)
    mask2_[mask2] = True
    mask2__ = th.zeros(num, dtype=th.bool, device=device)
    mask2__[mask] = mask2_
    origin_mask = ray_origin[mask][mask2]
    direct_mask = ray_direction[mask][mask2]
    ipoint[mask2__, :] = origin_mask + t1[mask2].tile((2, 1)).T * direct_mask
    valids[mask2__] = True
    return ipoint, valids

@numba.jit(nopython=True, parallel=False)
def get_ray_intersections(ray_start, ray_end, starts, ends):
    num_lines = starts.shape[0]
    ipoints = np.zeros((num_lines, 2))
    valids = np.zeros(num_lines, dtype='bool')
    for i in range(num_lines):
        ipoints[i, :], valids[i] = lineRayIntersectionPoint(ray_start, ray_end, starts[i, :], ends[i, :])
    return ipoints, valids

@numba.jit(nopython=True)
def get_intersects(a1, a2, starts, ends):
    num_lines = starts.shape[0]
    ipoints = np.zeros((num_lines, 2))
    valids = np.zeros(num_lines, dtype='bool')
    for i in range(num_lines):
        b1 = starts[i, :]
        b2 = ends[i, :]
        line_len = np.linalg.norm(b2 - b1)
        line_vec = (b2 - b1) / line_len
        point, valid = get_intersect(a1, a2, b1, b2)
        ipoints[i, :] = point
        if valid:
            ray_dist = np.dot(point - a1, a2 - a1)
            valid_ray = ray_dist >= -1e-6
            after_line_start = np.dot(point - b1, line_vec) >= 0.0
            before_line_end = np.dot(point - b1, line_vec) <= 1.0
            valid_line = after_line_start and before_line_end
            valids[i] = (valid and valid_ray and valid_line)
    return ipoints, valids

@numba.jit(nopython=True)
def get_intersection_params(start0, dir0, start1, dir1):
    '''
    Return intersection matrix determinant, and if possible the direction
    coefficients for dir0, dir1. 
    It turns out I also want to get a fourth parameter, which is 1.0 if
    intersection is valid and 0.0 otherwise
    '''
    dir0_ = np.array([-dir0[1], dir0[1]])
    y_vec = start1 - start0
    det_m = np.dot(dir0_, dir1)
    a, b = dir0[0], dir1[0]
    c, d = dir0[1], dir1[1]
    mtx_m = np.array([[a, b], [c, d]])
    valid_isect = 0.0
    if det_m > 1e-6:
        inv_mtx = invert_2x2(mtx_m)
        alpha, beta = inv_mtx.dot(y_vec)
        if alpha >= 0.0 and beta >= 0.0 and beta <= 1.0:
            valid_isect = 1.0
        else:
            valid_isect = 0.0
    else:
        alpha = 0.0
        beta = 0.0
        # Check if lines are identical
        defect = np.dot(dir0_, start1 - start0)
        if defect < 1e-6:
            valid_isect = 1.0
        else:
            valid_isect = 0.0
    return det_m, alpha, beta, valid_isect

@numba.jit(nopython=True)
def invert_2x2(mtx):
    a, b = mtx[0, :]
    c, d = mtx[1, :]
    det = a*b - c*b
    if np.abs(det) > 1e-10:
        inv_mtx = (1.0 / det) * np.array([[d, -b], [-c, a]])
    else:
        nan = np.nan
        inv_mtx = np.array([[nan, nan], [nan, nan]])
    return inv_mtx

@numba.jit(nopython=True, parallel=False)
def old_get_intersections(eq_mtx, line_eq):
    '''
    Computes all intersection points given the equation matrix in eq_mtx.
    '''
    num_eqs = eq_mtx.shape[0]
    outs = np.zeros((num_eqs, 2))
    for k in range(num_eqs):
        mtx = np.zeros((2, 2))
        mtx[0, :] = eq_mtx[k, 0:2]
        mtx[1, :] = line_eq[0:2]
        rhs = np.array([eq_mtx[k, 2], line_eq[2]])
        mtx_inv = invert_2x2(mtx)
        sol = np.dot(mtx_inv, rhs)
        outs[k, :] = sol
    return outs

@numba.jit(nopython=True, parallel=False)
def old_points_on_lines(points, start_points, end_points):
    num_points = points.shape[0]
    res = np.zeros(num_points, dtype='bool')
    for k in range(num_points):
        point = points[k, :]
        start = start_points[k, :]
        end = end_points[k, :]
        length = np.linalg.norm(end - start)
        direction = (end - start) / length
        ortho_vec = np.array([direction[1], -direction[0]])
        start_dist = np.dot(point - start, direction)
        # Check if on infinite line:
        defect = np.abs(np.dot(point - start, ortho_vec))
        defect_low = 1.0 if defect < 1e-12 else 0.0
        after_start = 1.0 if start_dist >= 0.0 else 0.0
        before_end = 1.0 if start_dist <= length else 0.0
        res[k] = defect_low * after_start * before_end
    return res

class FiniteLine():

    def __init__(self, start, end):
        '''
        Instance of a finite directed line.
        '''
        self.start = np.array(start)
        self.end = np.array(end)
        self.length = np.linalg.norm(self.end - self.start)
        self.direction = (self.end - self.start) / self.length
        self.ortho_direction = np.zeros(2)
        self.ortho_direction[0] = +self.direction[1]
        self.ortho_direction[1] = -self.direction[0]
        # Setup the line equation
        self.alpha: float = 0.0
        self.beta: float = 0.0
        self.c: float = 0.0
        self.eq_facs = np.zeros(3)
        # self.init_line_eq()
        # Setup directional vector
    
    def init_line_eq(self):
        dist_x = abs(self.start[0] - self.end[0])
        dist_y = abs(self.start[1] - self.end[1])
        if dist_x + dist_y <= 1e-14:
            raise ValueError('illegal line with identical points')
        # Construct linear system:
        mtx = np.zeros((2, 2))
        mtx[0, :] = [self.start[0], self.start[1]]
        mtx[1, :] = [self.end[0], self.end[1]]
        rhs = np.ones(2) 
        sol_ = np.linalg.solve(mtx, rhs)
        sol = np.ones(3)
        sol[0:2] = sol_
        self.eq_facs = np.copy(sol)
        self.alpha, self.beta, self.c = sol

    def contains_point(self, point: coord2d) -> bool:
        '''
        Check whether this line contains a point using start, direction and length.
        '''
        start_offset = point - self.start
        parallel_dist = np.dot(self.direction, start_offset)
        ortho_dist = np.dot(self.ortho_direction, start_offset)
        on_ray = np.abs(ortho_dist) < 1e-6
        match_dist = (parallel_dist >= 0.0) and (parallel_dist <= self.length)
        return on_ray and match_dist

    def satisfies_eq(self, point: coord2d):
        defect = self.alpha * coord2d[0] + self.beta * coord2d[1] - c
        return abs(defect) < 1e-12
    
    def intersection(self, other: 'FiniteLine'):
        '''
        Compute the intersection with another line
        '''
        a1, a2 = self.start, self.end
        b1, b2 = other.start, other.end
        return get_intersect(a1, a2, b1, b2)

class FiniteLineGroup():

    def __init__(self):
        self.line_group: List[FiniteLine] = []
        self.equations = None
        self.start_points = None
        self.end_points = None
        self.num_lines: int = 0

    def recompute_eqs(self):
        num_lines = len(self.line_group)
        self.equations = np.zeros((num_lines, 3))
        self.start_points = np.zeros((num_lines, 2))
        self.end_points = np.zeros((num_lines, 2))
        for idx, line in enumerate(self.line_group):
            self.equations[idx, :] = line.eq_facs
            self.start_points[idx, :] = line.start
            self.end_points[idx, :] = line.end

    def add_line(self, line: FiniteLine, recompute=True):
        self.line_group.append(line)
        self.num_lines += 1
        # Do the computation to compress the line equations here
        if recompute:
            self.recompute_eqs()

    def get_intersections(self, line: FiniteLine):
        # Compute all intersections of line and this group.
        start0 = line.start
        dir0 = line.direction
        end0 = line.end
        starts = self.start_points
        ends = self.end_points
        points = np.zeros((self.num_lines, 2))
        do_intersect = np.zeros(self.num_lines)
        points, do_intersect = get_intersects(start0, end0, starts, ends)
        return points, do_intersect

    def get_ray_intersections(self, ray_start, ray_direction):
        # Compute all intersections of line and this group.
        starts = self.start_points
        ends = self.end_points
        points = np.zeros((self.num_lines, 2))
        do_intersect = np.zeros(self.num_lines)
        points, do_intersect = get_ray_intersections(ray_start, ray_direction, starts, ends)
        return points, do_intersect

    def get_multi_ray_intersections(self, ray_starts: th.Tensor, ray_directions: th.Tensor):
        '''
        Get the intersections of multiple rays with the current finite
        line-group.
            1) ray_start is a 2d vector
            2) ray_direction is a 2d vector
        '''
        # Compute the intersections of multiple rays with this line_group
        device = str(ray_starts.device)
        num_rays = ray_starts.shape[0]
        num_lines = self.num_lines
        starts_th = th.tensor(self.start_points, device=device)
        ends_th = th.tensor(self.end_points, device=device)
        # something seems broken in the parallel computation, also memory usage is high,
        # so we use sequential computations here
        ray_starts_list = []
        ray_dirs_list = []
        starts_list = []
        ends_list = []
        for k in range(num_rays):
            ray_starts_list.append(th.tile(ray_starts[k, :], (self.num_lines, 1)))
            ray_dirs_list.append(th.tile(ray_directions[k, :], (self.num_lines, 1)))
            starts_list.append(starts_th)
            ends_list.append(ends_th)
        #rs_tot = ray_starts.repeat((self.num_lines, 1))
        #rd_tot = ray_directions.repeat((self.num_lines, 1))
        rs_tot = th.concat(ray_starts_list, dim=0)
        rd_tot = th.concat(ray_dirs_list, dim=0)
        #ls_tot_test = th.tile(starts_th, (num_rays, 1))
        #le_tot_test = th.tile(ends_th, (num_rays, 1))
        ls_tot = th.concat(starts_list, dim=0)
        le_tot = th.concat(ends_list, dim=0)
        points_mtx, valids_mtx = line_ray_intersection_torch(rs_tot, rd_tot, ls_tot, le_tot)
        points_mtx = points_mtx.reshape((num_rays, num_lines, 2))
        valids_mtx = valids_mtx.reshape((num_rays, num_lines))
        return points_mtx, valids_mtx
        
    #def get_intersections(self, line: FiniteLine):
    #    # Compute all intersections of line and this group.
    #    line_eq = line.eq_facs
    #    eq_mtx = self.equations
    #    points = get_intersections(eq_mtx, line_eq)
    #    do_intersect = points_on_lines(points, self.start_points, self.end_points)
    #    return points, do_intersect
