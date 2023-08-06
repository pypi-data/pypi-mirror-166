import pygame
import numpy as np
import datetime as dt
import scipy.optimize as opt
import os
from ..track import Track, TrackPoint, Point2D
from ..track_element import TrackElement, StraightElement, CurveElement
from typing import List, Tuple
import enum
import json
import cv2


class ElementMode(enum.Enum):
    straight_elem: str = 'straight'
    select_start: str = 'select_start'
    select_direction: str = 'select_direction'
    add_element: str = 'add_element'
    edit_element: str = 'edit_element'
    normal_mode: str = 'normal'
    curve_elem: str = 'curve'
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
        if fname is None:
            self.track: Track = None
        elif os.path.isfile(fname):
            with open(fname) as fp:
                data = json.load(fp)
                self.track = Track(data)
        self.elems: List[TrackElement] = []
        self.new_elem: TrackElement = None
        self.cursor_pos = None
        self.track_width: float = 20.0
        self.scale = scale
        self.bgimg_path = bg_img
        self.mode = ElementMode.select_start
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
        self.img = pygame.image.load(self.bgimg_path)
        img_size = self.img.get_size()
        self.dispshape = img_size
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
        point = Point2D(*self.last_click)
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
        if len(self.track.get_elements()) !=0:
            return
        p0 = self.track.get_last_point().get_position().as_np()
        p1 = new_straight_point.get_position().as_np()
        pdiff = p1 - p0
        angle = np.arctan2(pdiff[1], pdiff[0])
        self.track.start_point.orientation = angle

    def make_new_elem(self, mouse_pos: Tuple[int, int], elem: TrackElement):
        rw_pos = self.to_rw_coords(*mouse_pos)
        start_point = elem.get_start_point()
        if isinstance(elem, CurveElement):
            # Compute radius and angle
            dir0 = start_point.get_ortho_direction().as_np()
            dir2 = start_point.get_direction().as_np()
            dir1 = np.array(rw_pos) - start_point.get_position().as_np()
            dir1_norm = np.linalg.norm(dir1)
            dir1 = dir1 / dir1_norm
            dotp0 = np.dot(dir0, dir1)
            dotp2 = np.dot(dir2, dir1)
            angle_dir = np.sign(dotp0)
            angle_size = np.arccos(dotp2)
            angle_diff = angle_dir * angle_size
            radius = dir1_norm / angle_size
            radius = min(max(radius, 0.01), 1000.0)
            # Make new curve
            elem.radius = radius
            elem.angular_dist = angle_diff
        elif isinstance(elem, StraightElement):
            # Compute straight distance
            diff = np.array(rw_pos) - np.array(self.last_click)
            direction = start_point.get_direction().as_np()
            dist = np.dot(diff, direction)
            elem.length = dist
        elem.update()

    def add_straight_curve(self, new_point: TrackPoint):
        '''
        Add straight and a curve by solving a 2x2 linear system.
        '''
        cur_point = self.track.get_last_point()
        w0 = cur_point.get_ortho_direction(offset='left')
        w1 = new_point.get_ortho_direction(offset='left')
        v0 = cur_point.get_direction().as_np()
        v1 = new_point.get_direction().as_np()
        if self.element_mode == ElementMode.curveR_elem:
            ang_dist = -np.arccos(np.dot(v0, v1))
        else:
            ang_dist = np.arccos(np.dot(v0, v1))
        print('Adding curve with angular distance: {:2.2f}'.format(ang_dist))
        q0 = cur_point.get_direction().as_np()
        q1 = (w1 - w0).as_np()
        mtx = np.zeros((2, 2), dtype=np.float64)
        mtx[:, 0] = q0
        mtx[:, 1] = q1
        p0 = cur_point.get_position().as_np()
        p1 = new_point.get_position().as_np()
        rhs = new_point.get_position().as_np() - cur_point.get_position().as_np()
        sol = np.linalg.solve(mtx, rhs)
        def pos_out(x):
            return p0 + x[0]*q0 + x[1]*q1
        def pos_err(x):
            diff = p1 - pos_out(x)
            return diff.dot(diff)
        res = opt.minimize(pos_err, [1.0, 1.0], bounds=[[10**-3, 10**3.0], [10**-3, 10**3.0]])
        sol = res.x
        s_len, c_rad = sol[0], sol[1]
        print('New length: {:2.2f}, new radius: {:2.2f}'.format(s_len, c_rad))
        new_straight = StraightElement(cur_point, s_len)
        new_straight_end = new_straight.get_last_point()
        new_curve = CurveElement(new_straight_end, c_rad, ang_dist)
        self.track.add_elem(new_straight)
        self.track.add_elem(new_curve)

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

    def handle_keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                print('Removing last track element')
                if self.track is not None:
                    self.track.remove_last_elem()
            if event.key == pygame.K_x and self.mode == ElementMode.add_element:
                if self.element_mode == ElementMode.straight_elem:
                    self.element_mode = ElementMode.curve_elem
                    last_point = self.track.get_last_point()
                    self.new_elem = CurveElement(last_point, 1.0, 0.01)
                elif self.element_mode == ElementMode.curve_elem:
                    self.element_mode = ElementMode.straight_elem
                    last_point = self.track.get_last_point()
                    self.new_elem = StraightElement(last_point, 1.0)
            if event.key == pygame.K_a:
                self.mode = ElementMode.add_element
                if self.element_mode == ElementMode.straight_elem:
                    last_point = self.track.get_last_point()
                    self.new_elem = StraightElement(last_point, 1.0)
                elif self.element_mode == ElementMode.curve_elem:
                    last_point = self.track.get_last_point()
                    self.new_elem = CurveElement(last_point, 1.0, 0.01)
            elif event.key == pygame.K_ESCAPE:
                self.mode = ElementMode.normal_mode
                self.new_elem = None

    def plot_hints(self):
        infos = {}
        infos['Mode'] = self.mode.value
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

    def to_rw_coords(self, px, py) -> Tuple[float, float]:
        '''
        Convert screen coordinates to real world coordinates.
        '''
        rw_x = px * self.scale
        rw_y = (self.disp.get_height() - py) * self.scale 
        return (rw_x, rw_y)

    def to_scr_coords(self, rw_x, rw_y):
        px = int(round(rw_x / self.scale))
        py = self.disp.get_height() - rw_y / self.scale
        py = int(round(py))
        return (px, py)

    def handle_click(self, pos: Tuple[int, int]):
        if self.mode == ElementMode.select_start:
            self.last_click = self.to_rw_coords(*pos)
            self.click_angle = None
            self.mode = ElementMode.select_direction
        elif self.mode == ElementMode.select_direction:
            pos0 = np.array(self.last_click)
            pos1 = np.array(self.to_rw_coords(*pos))
            pos_diff = pos1 - pos0
            angle = np.arctan2(pos_diff[1], pos_diff[0])
            self.click_angle = angle
            new_point = self.get_new_point()
            if self.track is None:
                print('Initialised track')
                self.init_track(new_point)
            self.mode = ElementMode.normal_mode
        elif self.mode == ElementMode.normal_mode and self.track is not None:
            # Check if click is on element
            rw_pos = self.to_rw_coords(*pos)
            for eidx, elem in enumerate(self.track.get_elements()):
                if elem.on_elem(rw_pos, self.track.get_width()):
                    self.mode = ElementMode.edit_element
                    self.new_elem = self.track.get_elements()[eidx]
                    estart = self.track.get_elem_lens()[eidx, 0]
                    self.last_click = self.new_elem.get_start_point().get_position().as_tuple()
        elif self.mode == ElementMode.edit_element and self.track is not None:
            self.last_click = self.track.get_last_point().get_position().as_tuple()
            self.mode = ElementMode.normal_mode
            self.new_elem = None
        elif self.mode == ElementMode.add_element and self.new_elem is not None:
            self.track.add_elem(self.new_elem)
            self.last_click = self.new_elem.get_last_point().get_position().as_tuple()
            self.mode = ElementMode.normal_mode
            self.new_elem = None

    def handle_inputs(self):
        # get all events
        ev = pygame.event.get()
        # proceed events
        for event in ev:
            self.handle_keyboard(event)
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)
        if self.track is None:
            return
        mouse_pos = pygame.mouse.get_pos()
        if self.mode == ElementMode.edit_element:
            elem = self.new_elem
            rw_pos = self.to_rw_coords(*mouse_pos)
            self.make_new_elem(mouse_pos, elem)
        elif self.mode == ElementMode.add_element:
            elem = self.new_elem
            self.make_new_elem(mouse_pos, elem)

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
        if self.mode == ElementMode.select_direction:
            mouse_pos = pygame.mouse.get_pos()
            last_pos = self.to_scr_coords(*self.last_click)
            diff = (mouse_pos[0] - last_pos[0], mouse_pos[1] - last_pos[1])
            pos_start = (last_pos[0] - diff[0], last_pos[1] - diff[1])
            color = (255, 10, 10)
            pygame.draw.aaline(self.disp, color, pos_start, mouse_pos, 5)

    def draw_element(self, elem: TrackElement, npts: int, color=(10, 255, 10)):
        s_dists = np.linspace(0.0, elem.get_length(), npts)
        xy_old: TrackPoint = elem.get_start_point()
        for sdist in s_dists[1:]:
            xy_new = elem.get_point(sdist)
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
            for corner_pos in corners:
                pos_x, pos_y = self.to_scr_coords(*corner_pos)
                corners2.append((pos_x, pos_y))
            poly = pygame.draw.polygon(self.disp, color, corners2)
            # Update old point
            xy_old = xy_new

    def plot_track(self):
        if self.track is None:
            return
        track_len = self.track.get_length()
        npts = max(1, int(round(track_len / 8.0)))
        s_dists = np.linspace(0.0, track_len, npts)
        xy_old: TrackPoint = self.track.get_point(0.0)
        for elem in self.track.get_elements():
            npts = 16
            if isinstance(elem, StraightElement):
                npts = 3
            self.draw_element(elem, npts, (10, 255, 10))
        if self.new_elem is not None:
            # Draw new element
            npts: int = 16
            self.draw_element(self.new_elem, 16, (255, 10, 10))

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
