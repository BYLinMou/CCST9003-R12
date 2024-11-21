import numpy as np
from manim import *

# for presentation of the CCST9003 project

# SolarAngleScene: shows how the solar position is calculated
class SolarAngleScene(ThreeDScene):
    def construct(self):
        # look down at the x-y plane
        self.set_camera_orientation(phi=0, theta=-PI/2, zoom=0.75)

        # constructs a 3D coordinate system
        axes = ThreeDAxes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            z_range=[0, 10],
            x_length=10,
            y_length=10,
        )
        x_label = axes.get_x_axis_label(Text('East', color=BLUE).scale(0.5))
        y_label = axes.get_y_axis_label(Text('North', color=BLUE).scale(0.5))
        self.play(Create(axes))
        self.play([Write(x_label), Write(y_label)])
        self.wait(0.5)

        # move camera and animate
        self.move_camera(phi=PI/6, theta=-PI/6)
        # self.play(Transform(self.camera))
        self.wait(0.5)

        # create a sun
        sun = Dot(radius=0.05, color=YELLOW, point=axes.coords_to_point([-3, -6, 10])[0])
        sun_projection = Dot(radius=0.05, color=YELLOW, point=axes.coords_to_point([-3, -6, 0])[0])
        sun_label = Text('Sun', color=YELLOW).scale(0.5).next_to(sun, np.array((0, 0, 1)), buff=0.5)
        self.camera.add_fixed_orientation_mobjects(sun, sun_label)

        # create observer at origin
        observer = Dot(radius=0.05, color=RED, point=axes.coords_to_point([0, 0, 0])[0])

        self.play(Create(sun), Create(sun_projection), Write(sun_label), Create(observer))
        self.wait(0.5)

        len_center_to_projection = (3 ** 2 + 6 ** 2) ** 0.5
        # create a line from observer to sun's projection
        line_o_p = Line(observer.get_center(), axes.coords_to_point(0, len_center_to_projection, 0), color=RED)
        # rotate 0.1 deg to avoid parallelism
        line_o_p.rotate(-np.deg2rad(0.1), about_point=observer.get_center())
        azimuth_angle = Angle(Line(ORIGIN, UP), line_o_p, radius=0.5, color=RED, other_angle=True)
        azimuth_label = (MathTex(r'\text{Azimuth }\theta_{\text{az}}', color=RED)
                         .scale(0.5)
                         .next_to(azimuth_angle))
        self.camera.add_fixed_orientation_mobjects(azimuth_label)
        self.add(azimuth_angle)
        self.play(Create(line_o_p))

        # rotate line_o_p up to sun_projection
        azimuth_angle.add_updater(
            lambda m: m.become(Angle(Line(ORIGIN, UP), line_o_p, radius=0.5, color=RED, other_angle=True))
        )
        self.play(
            Rotate(
                line_o_p,
                angle=-PI - np.arctan(3/6) + np.deg2rad(0.1),
                about_point=observer.get_center(),
                run_time=2,
            )
        )
        self.play(Write(azimuth_label))

        self.wait(2)
