import numpy as np

class Lines():
    '''
    Organise line segments into a class to accelerate
    computation of intersections.
    '''

    def __init__(self, points_0, points_1):
        self.points_0 = points_0
        self.points_1 = points_1
        self.dx = points_1[:, 0] - points_0[:, 0]
        self.dy = points_1[:, 1] - points_0[:, 1]
        self.num_lines: int = len(points_0)
        # Compute line equations.
        self.normals = np.zeros((self.num_lines, 2))
        self.normals[:, 0] = -self.dy
        self.normals[:, 1] = +self.dx
        normal_lens = np.linalg.norm(self.normals, axis=1)
        self.normals[:, 0] = self.normals[:, 0] / normal_lens
        self.normals[:, 1] = self.normals[:, 1] / normal_lens
        # compute tangents and tangent lengths
        self.tangents = np.zeros((self.num_lines, 2))
        self.tangents[:, 0] = +self.dx
        self.tangents[:, 1] = +self.dy
        self.line_lens = np.linalg.norm(self.tangents, axis=1)
        self.tangents[:, 0] = self.tangents[:, 0] / self.line_lens
        self.tangents[:, 1] = self.tangents[:, 1] / self.line_lens
        # Compute offsets in line equation
        self.rhs = np.sum(self.points_0 * self.normals, axis=1)

    def contains(self, points, check_eqs=True, check_bounds=True, eqtol=1e-10):
        '''
        Provide a list of n points. The k-th line check whether
        it contains the k-th point.
        '''
        before_fin = np.ones(self.num_lines)
        after_start = np.ones(self.num_lines)
        sateq = np.ones(self.num_lines)
        directions = np.zeros((self.num_lines, 2))
        directions[:, 0] = points[:, 0] - self.points_0[:, 0]
        directions[:, 1] = points[:, 1] - self.points_0[:, 1]
        if check_bounds:
            # Check that point satisfies line segment bounds
            dir_lens = np.sum(directions * self.tangents, axis=1)
            before_fin = (dir_lens <= self.line_lens).astype(float)
            after_start = (dir_lens >= 0.0).astype(float)
        if check_eqs:
            # Check the point satisfies line equation
            defects = np.sum(points * self.normals, axis=1) - self.rhs
            defects = np.abs(defects)
            sateq = (defects < eqtol).astype(float)
        in_line = sateq * before_fin * after_start
        in_line = in_line.astype(bool)
        return in_line

    def ray_intersectin(self, point, vec):
        '''
        Given a ray defined by a point and a direction vector,
        we compute all the intersection points with all lines
        in this line set.
        A second check is performed to see if points are located within the
        corresponding line.
        '''
        vec_normal = np.array([-vec[0], vec[1]])
        vec_normal = vec_normal / np.linalg.norm(vec_normal)
        _vec_normal = np.array([vec_normal[1], -vec_normal[0]])
        _lines_normal = np.zeros((self.num_lines, 2))
        _lines_normal[:, 0] = -self.normals[:, 1]
        _lines_normal[:, 1] = +self.normals[:, 0]
        # Compute matrix determinants
        inter_points = np.zeros((self.num_lines, 2))
        rhs_ray = vec_normal.dot(point)
        dets = np.sum(self.normals * _vec_normal, 1)
        # Compute unscaled solutions
        us_sol = np.zeros((self.num_lines, 2))
        us_sol += rhs_ray * _lines_normal
        us_sol[:, 0] += _vec_normal[0] * self.rhs
        us_sol[:, 1] += _vec_normal[1] * self.rhs
        inter_points = np.zeros((self.num_lines, 2))
        inter_points[:, 0] = us_sol[:, 0] / dets
        inter_points[:, 1] = us_sol[:, 1] / dets
        in_line = self.contains(inter_points, check_eqs=False).astype(float)
        #valid_intersect = (np.abs(dets) > 1e-9).astype(float)
        # check if intersection is in front of ray:
        ray_diff = np.zeros((self.num_lines, 2))
        ray_diff[:, 0] = inter_points[:, 0] - point[0]
        ray_diff[:, 1] = inter_points[:, 1] - point[1]
        vec_rep = np.tile(vec, (self.num_lines, 1))
        forward = (np.sum(ray_diff * vec_rep, axis=1) >= 0.0)
        return inter_points, (forward * in_line).astype(bool)

if __name__ == '__main__':
    # Little benchmark:
    import time
    from tqdm import tqdm
    runs = 10
    num = 10**6
    num_rays = 16
    time0 = time.time()
    points_0 = np.random.randn(num, 2)
    points_1 = np.random.randn(num, 2)
    lines = Lines(points_0, points_1)
    for j in tqdm(range(runs)):
        for k in range(num_rays):
            p0, vec = np.random.randn(2), np.random.randn(2)
            inter_points, inline = lines.ray_intersectin(p0, vec)
    time1 = time.time()
    print('Checking 16 rays and 1000 line track takes (ms)')
    print((time1 - time0)/runs * 1000.0)

