import numpy as np
import torch as th


class InterpSegment():
    """
    Smooth step function for value interpolation.
    """

    def __init__(self, x_left, x_right, val_left, val_right):
        self.xleft = x_left
        self.xright = x_right
        self.width = x_right - x_left
        self.val_l = val_left
        self.val_r = val_right
        
    def get_value(self, point: th.Tensor) -> th.Tensor:
        mask = (point>=self.xleft) * (point<self.xright)
        px = (point - self.xleft) / self.width
        px = 2.0*px - 1.0
        px = th.clip(px, min=-1.0, max=+1.0)
        lam = (3.0/16.0)*(px**5.0) - (5.0/8.0)*(px**3.0) + (15.0/16.0)*px + 0.5
        lam = 0.5*(lam + 1.0)
        out_val = lam*self.val_l + (1.0-lam)*self.val_r
        return out_val * mask
