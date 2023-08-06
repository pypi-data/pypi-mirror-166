import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline


class ApproxCurveFunc():


    def __init__(self, points: np.ndarray, curvatures: np.ndarray):
        self.points = points
        self.curvatures = curvatures
        interp_poly = interp1d(self.points, self.curvatures, kind='cubic')
        self.spline = CubicSpline(self.points, self.curvatures, bc_type='natural')
        self.spline_d1 = self.spline.derivative(1) 
        self.spline_d2 = self.spline.derivative(2)
        self.spline_d3 = self.spline.derivative(3)
        
    def eval(self, x_vals):
        return self.spline(x_vals)
    
    def eval_deriv(self, x_vals):
        return self.spline_d1(x_vals)
