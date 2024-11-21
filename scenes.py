import numpy as np
from manim import *
from pydub.generators import Pulse


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
        x_label = axes.get_x_axis_label(Text('East', color=WHITE).scale(0.6), buff=-0.75)
        y_label = axes.get_y_axis_label(Text('North', color=WHITE).scale(0.6), buff=-0.25)
        self.play(
            Create(axes, run_time=0.5),
            # Create(x_y_plane, run_time=0.5),
            Write(x_label, run_time=0.5),
            Write(y_label), run_time=0.5)
        self.wait(0.5)

        # move camera and animate
        self.move_camera(phi=PI/4, theta=-PI/6)
        self.wait(0.5)

        # create a sun
        sun = Dot(radius=0.05, color=YELLOW, point=axes.coords_to_point([-3, -6, 10])[0])
        sun_projection = Dot(radius=0.05, color=YELLOW, point=axes.coords_to_point([-3, -6, 0])[0])
        sun_label = Text('Sun', color=YELLOW).scale(0.5).next_to(sun, np.array((-1, -1, 0)), buff=0.5)
        self.camera.add_fixed_orientation_mobjects(sun)
        self.remove(sun)
        self.camera.add_fixed_in_frame_mobjects(sun_label)
        self.remove(sun_label)
        sun_label.to_corner(UL).shift(0.5 * DOWN + 3 * RIGHT)

        # create observer at origin
        observer = Dot(radius=0.05, color=RED, point=axes.coords_to_point([0, 0, 0])[0])

        self.play(
            Create(sun, run_time=0.5),
            Create(sun_projection, run_time=0.5),
            Write(sun_label, run_time=0.5),
            Create(observer, run_time=0.5)
        )
        self.wait(0.5)

        len_center_to_projection = (3 ** 2 + 6 ** 2) ** 0.5
        # create a line from observer to sun's projection
        active_line = Line(observer.get_center(), axes.coords_to_point(0, len_center_to_projection, 0), color=RED)
        # rotate 0.1 deg to avoid parallelism
        active_line.rotate(-np.deg2rad(0.1), about_point=observer.get_center())
        azimuth_angle = Angle(Line(ORIGIN, UP), active_line, radius=0.5, color=RED, other_angle=True)
        azimuth_label = (MathTex(r'\text{Azimuth }', r'\theta_{az}', color=RED, stroke_width=1.5)
                         .scale(0.5)
                         .next_to(azimuth_angle, DR))
        self.camera.add_fixed_in_frame_mobjects(azimuth_label)
        azimuth_label.shift(0.3 * DOWN + 0.3 * RIGHT)
        self.add(azimuth_angle)
        self.play(Create(active_line, run_time=0.5))

        # rotate active_line up to sun_projection
        azimuth_angle.add_updater(
            lambda m: m.become(Angle(Line(ORIGIN, UP), active_line, radius=0.5, color=RED, other_angle=True))
        )
        self.play(
            Rotate(
                active_line,
                angle=-PI - np.arctan(3/6) + np.deg2rad(0.1),
                about_point=observer.get_center(),
                run_time=1,
            )
        )

        # creates a copy of active_line
        line_o_p_copy = DashedLine(observer.get_center(), axes.coords_to_point(-3, -6, 0), color=GREY)
        self.add(line_o_p_copy)
        self.play(Write(azimuth_label, run_time=0.5))

        # remove updater
        azimuth_angle.clear_updaters()

        active_line.become(Line(
            observer.get_center(),
            axes.c2p(-3, -6, 0.01),
            color=RED
        ))

        # get projection of end point of temp_line on xy-plane
        temp_projection = axes.p2c(
            active_line
                .copy()
                .rotate(-PI/2, about_point=ORIGIN, axis=np.array((-3, -6, 0)))
                .get_end()
        )
        temp_projection[2] = 0
        temp_projection = Dot(radius=0.05, color=GREEN, point=axes.c2p(temp_projection)[0], fill_opacity=1)

        elevation_angle = Angle.from_three_points(
            sun_projection.get_center(),
            observer.get_center(),
            temp_projection.get_center(),
            radius=0.5,
            color=GREEN,
        ).rotate(PI/2, about_point=ORIGIN, axis=np.array((-3, -6, 0)))
        elevation_label = (MathTex(r'\text{Elevation }', r'\theta_{el}', color=GREEN, stroke_width=1.5)
                           .scale(0.5)
                           .next_to(elevation_angle, axes.c2p(-3, -6, 5)[0], buff=0.5, aligned_edge=RIGHT))
        self.camera.add_fixed_in_frame_mobjects(elevation_label)
        elevation_label.shift(1.5 * UP + 0.5 * RIGHT)
        self.add(elevation_angle)

        def update_elevation_angle(m):
            copy = active_line.copy()
            copy.set_stroke(opacity=0)
            copy.rotate(-PI/2, about_point=ORIGIN, axis=np.array((-3, -6, 0)))
            tp = axes.p2c(copy.get_end())
            tp[2] = 0
            tp = Dot(radius=0.05, color=GREEN, point=axes.c2p(tp)[0], fill_opacity=0)
            m.become(Angle.from_three_points(
                sun_projection.get_center(),
                observer.get_center(),
                tp.get_center(),
                radius=0.5,
                color=GREEN,
            ).rotate(PI/2, about_point=ORIGIN, axis=np.array((-3, -6, 0))))

        elevation_angle.add_updater(lambda m: update_elevation_angle(m))

        # rotation
        line_o_s = Line(observer.get_center(), sun.get_center(), color=GREEN)
        self.play(Transform(active_line, line_o_s, run_time=1))
        self.play(Write(elevation_label, run_time=0.5))
        self.wait(1)

        # fade everything except the labels
        self.play(
            FadeToColor(axes, GREY, run_time=0.5),
            FadeToColor(x_label, GREY, run_time=0.5),
            FadeToColor(y_label, GREY, run_time=0.5),
            FadeToColor(sun, GREY, run_time=0.5),
            FadeToColor(sun_label, GREY, run_time=0.5),
            FadeToColor(sun_projection, GREY, run_time=0.5),
            FadeToColor(observer, GREY, run_time=0.5),
            FadeToColor(active_line, GREY, run_time=0.5),
            FadeToColor(line_o_p_copy, GREY, run_time=0.5),
        )
        self.wait(1)

        # transform labels into formulae
        azimuth_formula = MathTex(r'''\cos\left(\frac{1}{2}-\theta_{az}\right)
                                  =\sin(\phi)\cdot\sin(\theta_{dec})
                                  +\cos(\phi)\cdot\cos(\theta_{dec})\cdot\cos(\theta_{ha})''',
                                  color=RED, font_size=26)
        self.add_fixed_in_frame_mobjects(azimuth_formula)
        azimuth_formula.to_corner(UR)
        self.play(Unwrite(azimuth_label, run_time=0.5), Write(azimuth_formula, run_time=0.5))
        self.wait(0.5)

        elevation_formula = MathTex(r'\sin(', r'\theta_{az}',
                                    r')=\frac{-\cos\theta_{dec}\cdot\sin\theta_{ha}}{\cos{\theta_{el}}}',
                                    color=GREEN, font_size=26)
        self.add_fixed_in_frame_mobjects(elevation_formula)
        elevation_formula.to_corner(UR)
        elevation_formula.shift(DOWN)
        self.play(Unwrite(elevation_label, run_time=0.5), Write(elevation_formula, run_time=0.5))
        self.wait(2)
