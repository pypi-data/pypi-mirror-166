import numpy as np


def project_points(p0, p1, p2):
    '''
    Project point p0 onto line through p1, p2
    Each point has to be given as a row in p0, p1, p3
    such that
        for p in [p0, p1, p2]: 
            assert p.shape == (N, 2)
    holds
    '''
    a_vec = p0 - p1
    b_vec = p2 - p1
    b_norm = np.linalg.norm(b_vec, axis=1)
    b_norm = np.maximum(b_norm, 1e-8)
    dot_prod = np.sum(a_vec * b_vec, axis=1)
    dot_prod_rep = np.tile(dot_prod, (2, 1)).T
    b_norm_rep = np.tile(b_norm, (2, 1)).T
    proj_vec = (dot_prod_rep * b_vec) / (b_norm_rep**2.0)
    out_point = proj_vec + p1
    return out_point 


def get_triangle_areas(p0, p1, p2):
    p_p0_base = project_points(p0, p1, p2)
    len_base = np.linalg.norm(p2 - p1, axis=1)
    len_height = np.linalg.norm(p_p0_base - p0, axis=1)
    return 0.5 * np.abs(len_base * len_height)


def get_square_areas(p0, p1, p2, p3):
    area0 = get_triangle_areas(p0, p1, p2)
    area1 = get_triangle_areas(p1, p2, p3)
    return area0 + area1


def get_point_in_triangle(p0, t0, t1, t2, tol=1e-10):
    area0 = get_triangle_areas(p0, t1, t2)
    area1 = get_triangle_areas(p0, t2, t0)
    area2 = get_triangle_areas(p0, t0, t1)
    area_tri = get_triangle_areas(t0, t1, t2)
    area_diff = area_tri - (area0 + area1 + area2)
    return np.abs(area_diff) < tol


def get_point_in_square(p0, s0, s1, s2, s3, tol=1e-10):
    in_t0 = get_point_in_triangle(p0, s0, s1, s3, tol=tol)
    in_t1 = get_point_in_triangle(p0, s1, s2, s3, tol=tol)
    return np.logical_or(in_t0, in_t1)
