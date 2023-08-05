from manim import *
import numpy as np
import os

__dir = os.path.dirname(__file__)
svg_path = os.path.join(__dir, 'src', 'gene.svg')

class GVer(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        svg = SVGMobject(svg_path).rotate(PI/2)
        self.blue, eyes, self.red = svg.submobjects
        self.add(self.blue, self.red)

        eye_in = Circle(radius=.15).set_stroke().set_opacity(1)
        eye_out = Circle(radius=.3).set_stroke().set_opacity(1)
        eye_in.set_color(GRAY_D)
        eye_out.set_color(WHITE)
        eye = VGroup(eye_out, eye_in)

        e_ = Line(LEFT*.3, RIGHT*.3, stroke_width=6, path_arc=1)
        e_l = e_.copy().shift(LEFT*.65)
        e_r = e_.copy().shift(RIGHT*.65)
        self.add(e_l, e_r)

        self.left_eye = eye.copy().shift(LEFT*.65)
        self.right_eye = eye.copy().shift(RIGHT*.65)
        self.add(self.left_eye, self.right_eye)

    def close_eye(self, left=None, right=None):
        if not left and not right:
            left = right = True
        if left:
            self.left_eye.set_opacity(0)
        if right:
            self.right_eye.set_opacity(0)
        return self

    def open_eye(self, left=None, right=None):
        if not left and not right:
            left = right = True
        if left:
            self.left_eye.set_opacity(1)
        if right:
            self.right_eye.set_opacity(1)
        return self
    
    def wink(self, cls, times=2, lag=.3):
        for i in range(times):
            cls.wait(lag)
            cls.play(self.animate(run_time=.07).close_eye())
            cls.play(self.animate(run_time=.07).open_eye())

    def watch(self, mob):
        # left eye
        left_center = self.left_eye[0].get_center()
        l = mob.get_center() - left_center
        l_n = np.linalg.norm(l)
        l_ = l / l_n * .15
        self.left_eye[1].move_to(left_center + l_)

        # right eye
        right_center = self.right_eye[0].get_center()
        r = mob.get_center() - right_center
        r_n = np.linalg.norm(r)
        r_ = r / r_n * .15
        self.right_eye[1].move_to(right_center + r_)
        return self

    def stop_watch(self):
        self.left_eye[1].move_to(self.left_eye[0])
        self.right_eye[1].move_to(self.right_eye[0])
        return self