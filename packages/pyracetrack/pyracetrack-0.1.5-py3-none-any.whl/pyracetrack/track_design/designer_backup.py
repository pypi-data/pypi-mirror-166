import pygame
import numpy as np
import datetime as dt
import os
from ..track import Track, TrackPoint, Point2D
from ..track_element import TrackElement, StraightElement, CurveElement
from typing import List, Tuple
import enum
import json
import cv2


class ElementMode(enum.Enum):
    straight_elem: str = 'straight'
    curveL_elem: str = 'curve_left'
    curveR_elem: str = 'curve_right'


class Designer():
    '''
    Class for rebuilding tracks from scratch using pygame.
    '''
    def __init__(self, bg_img: str, scale: float=1.0, fname: str=None):
        self.fg_color = (40, 40, 40)
        self.bg_color = (220, 220, 220)
        self.line_color = (20, 220, 220)
        if os.path.isfile(fname):
            with open(fname) as fp:
                data = json.load(fp)
                self.track = Track(data)
        else:
            self.track: Track = None
        self.elems: List[TrackElement] = []
        self._start_points = TrackPoint(Point2D(0.0, 0.0), 0.0)
        self.cursor_pos = None
        self.track_width: float = 20.0
        self.scale = scale
        self.bgimg_path = bg_img
        self.mode = 'select_point'
        self.element_mode = ElementMode.straight_elem
        self.last_click: Tuple[int, int] = None
        self.click_angle: float = None
        self.last_click_angle: float = None
        self.last_save = dt.datetime.now()
        #dfont = pygame.font.get_default_font()
        if fname is None:
            self.save_file = 'new_track.json'
            counter = 0
            while os.path.isfile(self.save_file):
                counter += 1
                cstr = str(counter).zfill(3)
                self.save_file = 'new_track_{}.json'.format(cstr)
        else:
            self.save_file = fname
        pygame.init()
        self.myfont = pygame.font.SysFont('Ubuntu', 16)
        self._setup_pygame()

    def _setup_pygame(self):
        self.dispshape = (1600, 900)
        self.img = pygame.image.load(self.bgimg_path)
        self.img = pygame.transform.scale(self.img, self.dispshape)
        self.disp = pygame.display.set_mode(self.dispshape)
        pygame.display.set_caption('Track Designer')

    def main_loop(self):
        self.running = True
        while self.running == True:
            # Update screen
            self.plot_background()
            self.plot_track()
            self.plot_angle_selector()
            self.handle_inputs()
            self.plot_hints()
            pygame.display.update()
            dt_now = dt.datetime.now()
            tdiff = dt_now - self.last_save
            if tdiff.total_seconds() > 5.0 and self.track is not None:
                self.quick_save()
                self.last_save = dt_now

    def quick_save(self):
        tdict = self.track.to_dict()
        with open(self.save_file, 'w') as fs:
            json.dump(tdict, fs, indent=4)

    def get_new_point(self) -> TrackPoint:
        '''
        If we have found a point and a direction we can use them to find the
        actual position.
        '''
        if self.last_click is None or self.click_angle is None:
            print('cannot add track point')
            return None
        # Make new point
        point = Point2D(self.last_click[0]*self.scale, self.last_click[1]*self.scale)
        tpoint = TrackPoint(point, self.click_angle)
        return tpoint

    def init_track(self, new_point: TrackPoint):
        tdict = {}
        tdict['start position'] = new_point.point.as_tuple()
        tdict['angle'] = new_point.orientation
        tdict['width'] = self.track_width
        self.track = Track(tdict)

    def fix_curve(self, new_straight_point: TrackPoint):
        if self.track is None:
            return
        if len(self.track.get_elements()) < 1:
            return
        lelem: CurveElement = self.track.get_elements()[-1]
        if not isinstance(lelem, CurveElement):
            return
        p0 = self.track.get_last_point().get_position().as_np()
        p1 = new_straight_point.get_position().as_np()
        pdiff = p1 - p0
        curve_start = lelem.get_start_point()
        curve_out_angle = np.arctan2(pdiff[1], pdiff[0])
        curve_end = TrackPoint(Point2D(*p0), curve_out_angle)
        direct = lelem.get_direction_flipped()
        new_curve = CurveElement.from_points_scipy(curve_start, curve_end, direct)
        self.track.remove_last_elem()
        self.track.add_elem(new_curve)

    def fix_start(self, new_straight_point: TrackPoint):
        if self.track is None:
            return
        if len(self.track.get_elements()) == 0:
            p0 = self.track.get_last_point().get_position().as_np()
            p1 = new_straight_point.get_position().as_np()
            pdiff = p1 - p0
            angle = np.arctan2(pdiff[1], pdiff[0])
            self.track.start_point.orientation = angle

    def add_element(self, new_point: TrackPoint):
        '''
        Add track element by new track point
        '''
        last_point = self.track.get_last_point()
        if self.element_mode == ElementMode.straight_elem:
            # Compute length of straight
            self.fix_curve(new_point)
            self.fix_start(new_point)
            p0 = last_point.get_position().as_np()
            p1 = new_point.get_position().as_np()
            v0 = last_point.get_direction().as_np()
            dist = abs(np.dot(p1 - p0, v0))
            new_elem = StraightElement(last_point, dist)
            self.track.add_elem(new_elem)
            # Check if second to last element is a curve that can be adjusted.
        else:
            # Compute curve element.
            direc = 'left' if self.element_mode == ElementMode.curveL_elem else 'right'
            new_elem = CurveElement.from_points_scipy(last_point, new_point, direc)
            self.track.add_elem(new_elem)

    def handle_keyboard(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    print('Removing last track element')
                    if self.track is not None:
                        self.track.remove_last_elem()
                if event.key == pygame.K_x:
                    if self.element_mode == ElementMode.straight_elem:
                        self.element_mode = ElementMode.curveL_elem
                    elif self.element_mode == ElementMode.curveL_elem:
                        self.element_mode = ElementMode.curveR_elem
                    elif self.element_mode == ElementMode.curveR_elem:
                        self.element_mode = ElementMode.straight_elem
                if event.key == pygame.K_f:
                    self.flip_curve()

    def plot_hints(self):
        infos = {}
        infos['Element mode'] = self.element_mode.value
        if self.last_click is not None:
            infos['Last click position:'] = '{:2.2f}, {:2.2f}'.format(*self.last_click)
        if self.track is not None:
            infos['Total track len:'] = '{:2.2f}'.format(self.track.get_length())
        px, py = 20, 20
        for key in infos:
            msg = '{}= {}'.format(key, infos[key])
            text_surf = self.myfont.render(msg, True, (0, 0, 0), (200, 200, 200))
            self.disp.blit(text_surf, (px, py))
            py += 18

    def to_rw_coords(self, px, py):
        '''
        Convert screen coordinates to real world coordinates.
        '''
        rw_x = px * self.scale
        rw_y = (self.disp.get_height() - py) * self.scale 
        return rw_x, rw_y

    def handle_click(self, pos: Tuple[int, int]):
        if self.mode == 'select_point':
            #self.last_click = self.to_rw_coords(pos[0], pos[1])
            self.last_click = pos
            if self.track is not None and self.element_mode == ElementMode.straight_elem:
                # Add straight element directly
                self.click_angle = 0.0
                new_point = self.get_new_point()
                self.add_element(new_point)
                self.last_click = None
                self.click_angle = None
                self.mode = 'select_point'
            else:
                self.mode = 'select_direction'
        elif self.mode == 'select_direction':
            pos1 = np.array(pos)
            pos0 = np.array(self.last_click)
            pos_diff = pos1 - pos0
            angle = np.arctan2(pos_diff[1], pos_diff[0])
            self.click_angle = angle
            self.mode = 'select_point'
            new_point = self.get_new_point()
            self.last_click = None
            self.click_angle = None
            if self.track is None:
                print('Initialised track')
                self.init_track(new_point)
            else:
                print('Adding element to track')
                self.add_element(new_point)

    def handle_inputs(self):
        # get all events
        ev = pygame.event.get()
        # proceed events
        self.handle_keyboard(ev)
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)

    def plot_background(self):
        self.disp.fill(self.bg_color)
        # Render image 
        self.disp.blit(self.img, (0, 0))

    def flip_curve(self):
        if self.track is None:
            return
        if len(self.track.get_elements()) <= 0:
            return
        lelem: CurveElement = self.track.get_elements()[-1]
        if not isinstance(lelem, CurveElement):
            if len(self.track.get_elements()) <= 1:
                return
            else:
                lelem: CurveElement = self.track.get_elements()[-2]
        if not isinstance(lelem, CurveElement):
            return
        new_adist = np.pi - lelem.angular_dist
        radius = lelem.radius
        start_curve = lelem.get_start_point()
        end_curve = lelem.get_last_point()
        if end_curve.get_orientation() > start_curve.get_orientation():
            end_curve.orientation -= 2.0*np.pi
        else:
            end_curve.orientation += 2.0*np.pi
        new_curve = CurveElement.from_points(end_curve, start_curve)
        lelem.angular_dist = new_curve.angular_dist

    def plot_angle_selector(self):
        '''
        Draw an angle selector if we are currently selecting angles.
        '''
        if self.mode == 'select_direction':
            mouse_pos = pygame.mouse.get_pos()
            last_pos = self.last_click
            diff = (mouse_pos[0] - last_pos[0], mouse_pos[1] - last_pos[1])
            pos_start = (last_pos[0] - diff[0], last_pos[1] - diff[1])
            color = (255, 10, 10)
            pygame.draw.aaline(self.disp, color, pos_start, mouse_pos, 5)

    def plot_track(self):
        if self.track is None:
            return
        track_len = self.track.get_length()
        npts = max(1, int(round(track_len / 8.0)))
        s_dists = np.linspace(0.0, track_len, npts)
        xy_old: TrackPoint = self.track.get_point(0.0)
        for sdist in s_dists[1:]:
            # Get new point
            xy_new = self.track.get_point(sdist)
            # Draw the element
            corners = []
            left0 = xy_old.get_bound(self.track_width, which='left')
            right0 = xy_old.get_bound(self.track_width, which='right')
            right1= xy_new.get_bound(self.track_width, which='right')
            left1= xy_new.get_bound(self.track_width, which='left')
            corners.append(left0.as_tuple())
            corners.append(right0.as_tuple())
            corners.append(right1.as_tuple())
            corners.append(left1.as_tuple())
            corners2 = []
            height = self.dispshape[1]
            color = (10, 255, 10)
            for c in corners:
                pos_x = int(round(c[0] / self.scale))
                pos_y = int(round(c[1] / self.scale))
                corners2.append((pos_x, pos_y))
            poly = pygame.draw.polygon(self.disp, color, corners2)
            # Update old point
            xy_old = xy_new
        tpoints = [self.track.start_point]
        for elem in self.track.get_elements():
            tpoints.append(elem.get_last_point())
        for tp in tpoints:
            self.plot_track_point(tp)

    def plot_track_point(self, tpoint: TrackPoint):
        '''
        Draw track point position and angle
        '''
        p2d = tpoint.get_position().as_tuple()
        ori = tpoint.get_direction().as_tuple()
        pstart = tpoint.get_position()
        pend = pstart + 20.0*tpoint.get_direction()
        pstart = [int(val+0.5) for val in pstart.as_tuple()]
        pend = [int(val+0.5) for val in pend.as_tuple()]
        pygame.draw.aaline(self.disp, self.fg_color, pstart, pend, blend=3)
