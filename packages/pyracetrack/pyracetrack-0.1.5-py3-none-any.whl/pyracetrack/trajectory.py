import numpy as np
import matplotlib.pyplot as plt


class Trajectory():

    def __init__(self, sdist, xpos, ypos, angle=None, velocity=None):
        self.sdist = sdist
        self.xpos = xpos
        self.ypos = ypos
        self.angle = angle
        self.velocity = velocity
        self.has_angle = (self.angle is not None)
        self.has_velocity = (self.velocity is not None)

    def visualize(self):
        ax = plt.gca()
        # Plot the center line
        plt.plot(self.xpos, self.ypos, linewidth=1.5)
