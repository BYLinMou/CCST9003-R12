from copy import deepcopy

import numpy as np
from manim import *
from scipy.fft import hfftn

# for presentation of the CCST9003 project

# global vars
shared_objs: list[Mobject] = [] # shared objects between scenes

# SolarAngleScene: shows how the solar position is calculated
class MyScene(ThreeDScene):
    def construct(self):
        self.next_section(name='SolarAngleScene')
        self.__solar_angle_scene()
        self.next_section(name='HeightAndShadowFieldsScene')
        self.__height_and_shadow_fields_scene()

    def __solar_angle_scene(self):
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
        x_y_plane = NumberPlane(
            x_range=[-30, 30, 2],
            y_range=[-30, 30, 2],
            background_line_style={
                "stroke_color": GREY,
            }
        )
        self.play(
            Create(axes, run_time=0.5),
            Create(x_y_plane, run_time=0.5),
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

        # connect to sun
        line_o_s = Line(observer.get_center(), sun.get_center(), color=GREEN)
        line_p_s = DashedLine(sun_projection.get_center(), sun.get_center(), color=GREY)
        self.play(Transform(active_line, line_o_s, run_time=1), Create(line_p_s, run_time=1))
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
                                  color=RED, font_size=22, background_stroke_color=RED_E, background_stroke_width=1.5)
        self.add_fixed_in_frame_mobjects(azimuth_formula)
        azimuth_formula.to_corner(UR)
        self.play(Unwrite(azimuth_label, run_time=0.5), Write(azimuth_formula, run_time=0.5))
        self.wait(0.5)

        elevation_formula = MathTex(r'\sin(', r'\theta_{az}',
                                    r')=\frac{-\cos\theta_{dec}\cdot\sin\theta_{ha}}{\cos{\theta_{el}}}',
                                    color=GREEN, font_size=22, background_stroke_color=GREEN_E, background_stroke_width=1.5)
        self.add_fixed_in_frame_mobjects(elevation_formula)
        elevation_formula.to_corner(UR)
        elevation_formula.shift(DOWN)
        self.play(Unwrite(elevation_label, run_time=0.5), Write(elevation_formula, run_time=0.5))
        self.wait(2)

        # packup shared objects
        shared_objs.extend([
            axes, x_y_plane, x_label, y_label, sun, sun_projection, sun_label, observer, active_line, line_p_s, line_o_s,
            line_o_p_copy, azimuth_formula, elevation_formula, azimuth_angle, elevation_angle
        ])

    def __height_and_shadow_fields_scene(self):
        # adjust camera to match previous scene
        self.set_camera_orientation(phi=PI/4, theta=-PI/6, zoom=0.75)

        # unpack from shared objects
        axes, x_y_plane, x_label, y_label, sun, sun_projection, sun_label, observer, active_line, line_p_s, line_o_s,\
        line_o_p_copy, azimuth_formula, elevation_formula, azimuth_angle, elevation_angle = shared_objs

        self.add(axes, x_y_plane, x_label, y_label, sun, sun_projection, observer, active_line) # non-fixed objects
        self.add_fixed_in_frame_mobjects(sun_label, azimuth_formula, elevation_formula) # fixed objects
        self.play(
            FadeOut(sun_label),
            FadeOut(azimuth_formula),
            FadeOut(elevation_formula),

            # restore colors
            FadeToColor(axes, WHITE),
            FadeToColor(x_label, WHITE),
            FadeToColor(y_label, WHITE),
            FadeToColor(sun, YELLOW),
            FadeToColor(sun_projection, YELLOW),
            FadeToColor(observer, RED),
            FadeToColor(active_line, GREEN),
        )
        self.play(
            # remove unnecessary objects
            FadeOut(azimuth_angle, run_time=0.5),
            FadeOut(elevation_angle, run_time=0.5),

            # temporarily hide objects
            FadeOut(sun, run_time=0.5),
            FadeOut(sun_projection, run_time=0.5),
            FadeOut(active_line, run_time=0.5),
            FadeOut(line_p_s, run_time=0.5),
            FadeOut(line_o_s, run_time=0.5),
            FadeOut(line_o_p_copy, run_time=0.5),
        )

        # move back to top-down view
        self.move_camera(phi=0, theta=-PI/2)
        self.play(
            Unwrite(x_label, run_time=0.5),
            Unwrite(y_label, run_time=0.5),
        )

        # generate a random height field
        def get_height(lat, lon):
            # leave the line y=-x, width of 2 as a road (height=0)
            distance = np.abs(lat + lon) / (2 ** 0.5)
            if distance <= 2:
                return 0
            return np.random.random() * 10

        def match_color(height):
            height = int(height)
            if height in range(0, 2):
                return BLUE_A
            elif height in range(2, 4):
                return BLUE_B
            elif height in range(4, 6):
                return BLUE_C
            elif height in range(6, 8):
                return BLUE_D
            elif height in range(8, 10):
                return BLUE_E

        field = [] # 2D array of (lat, lon, height)
        nums = {} # dictionary of (lat, lon) to MathTex
        # read from file
        with open('height_field.txt', 'r') as file:
            for line in file:
                row = []
                row_group = VGroup()
                for entry in line.split():
                    lat, lon, h = map(float, entry.split(';'))
                    h = h*0.5
                    row.append((lat, lon, h)) # scale down height
                    nums[(lat, lon)] = (MathTex(f'{h:.2f}', color=match_color(h * 2), stroke_width=1.5, font_size=30)
                                    .move_to(axes.c2p([lat, lon, 0])[0]))
                    row_group.add(nums[(lat, lon)])
                self.play(Write(row_group, run_time=0.05))
                field.append(row)

        self.wait(0.5)

        # explanatory text
        hf_line_1 = MathTex(r'\text{Suppose we have a scalar field }\boldsymbol{H}\text{,}')
        hf_line_2 = MathTex(r'\text{where }\boldsymbol{H}(\phi, \lambda)\text{ represents the height of a building at '
                            r'latitude }\phi\text{ and longitude }\lambda\text{.}')
        hf_group = VGroup(hf_line_1, hf_line_2).arrange_submobjects(DOWN, aligned_edge=LEFT)
        hf_box = SurroundingRectangle(
            hf_group,
            buff=MED_LARGE_BUFF,
            color=BLUE,
            stroke_width=3,
            fill_color=DARK_BLUE,
            fill_opacity=0.95,
        )
        self.play(Create(hf_box, run_time=0.5), Write(hf_group, run_time=0.5))

        self.wait(2)

        # explain creation of ray vector
        ray_line_1 = MathTex(r'\text{From the observer, construct a ray vector }\hat{r}\text{ pointing to the Sun.}')
        ray_line_2 = MathTex(r'\hat{r} = \left(\cos\theta_{el}\right)'
                             r'\left(\sin\theta_{az}\hat{\boldsymbol{i}}+\cos\theta_{az}\hat{\boldsymbol{j}}'
                             r'+\tan\theta_{el}\hat{\boldsymbol{k}}\right)')
        ray_group = VGroup(ray_line_1, ray_line_2).arrange_submobjects(DOWN)
        ray_box = SurroundingRectangle(
                ray_group,
                buff=MED_LARGE_BUFF,
                color=RED,
                stroke_width=3,
                fill_color=RED_E,
                fill_opacity=0.95)
        self.play(
            ReplacementTransform(hf_group, ray_group, run_time=0.5),
            ReplacementTransform(hf_box, ray_box, run_time=0.5),
        )

        self.wait(2)

        self.play(FadeOut(ray_box), FadeOut(ray_group))
        self.move_camera(phi=np.deg2rad(70), theta=-PI/4, zoom=0.5) # move camera far away

        buildings = VGroup()
        buildings.set_z_index(2)
        for row in field:
            for lat, lon, h in row:
                if h == 0:
                    continue
                building = Prism(dimensions=(1, 1, h), fill_color=match_color(h*2), fill_opacity=0.2)
                building.move_to(axes.c2p([lat, lon, 0])[0] + np.array([0, 0, h/2]))
                buildings.add(building)

        self.play(DrawBorderThenFill(buildings, run_time=1), FadeOut(VGroup(*nums.values()), run_time=0.5))

        # put back Sun
        sun.set_z_index(6)
        self.play(FadeIn(sun, run_time=0.5), FadeIn(sun_projection, run_time=0.5))

        # create ray vector
        # angle objects values are inaccurate, manual calculation is adopted
        azimuth = PI + np.arctan(3/6)
        elevation = np.arctan(10/((3**2 + 6**2)**0.5))
        ray_vec = Arrow3D(
            start=observer.get_center(),
            end=axes.c2p([
                np.sin(azimuth)*np.cos(elevation),
                np.cos(azimuth)*np.cos(elevation),
                np.sin(elevation)
            ])[0],
            color=RED,
        )
        self.play(Create(ray_vec, run_time=0.5))
        self.move_camera(zoom=3)
        self.play(Indicate(ray_vec, color=YELLOW, run_time=1))
        self.wait(0.5)
        self.move_camera(zoom=0.5)

        # construct a line
        line_propagation = VGroup(
            MathTex(r'\text{Construct a straight line from the observer }\\'),
                    MathTex(r'\text{in the direction of }\hat{r}'
                            r'\text{ all the way until the edge of the map.}')
        ).set_z_index(7).arrange_submobjects(DOWN)
        line_propagation_box = SurroundingRectangle(
            line_propagation,
            buff=MED_LARGE_BUFF,
            color=RED,
            stroke_width=3,
            fill_color=RED_E,
            fill_opacity=0.95
        ).set_z_index(6)
        self.add_fixed_in_frame_mobjects(line_propagation, line_propagation_box)
        self.play(
            Create(line_propagation_box, run_time=0.5),
            Write(line_propagation, run_time=0.5),
        )
        self.wait(2)

        self.play(
            Uncreate(line_propagation_box, run_time=0.5),
            Unwrite(line_propagation, run_time=0.5),
        )
        active_line.set_z_index(6).set(stroke_color=RED)
        self.play(Create(active_line, run_time=0.5))

        check_group = VGroup(
            MathTex(r'\text{Look for intersections between the line and the buildings.}'),
            MathTex(r'\text{Intersection indicates that the observer is in shadow.}')
        ).set_z_index(7).arrange_submobjects(DOWN)
        check_box = SurroundingRectangle(
            check_group,
            buff=MED_LARGE_BUFF,
            color=RED,
            stroke_width=3,
            fill_color=RED_E,
            fill_opacity=0.95
        ).set_z_index(6)
        check_group.apply_matrix(np.linalg.inv(self.camera.generate_rotation_matrix())).scale(2)
        check_box.apply_matrix(np.linalg.inv(self.camera.generate_rotation_matrix())).scale(2)

        self.play(
            Create(check_box, run_time=0.5),
            Write(check_group, run_time=0.5),
        )

        self.wait(2)

        shadow_field_group = VGroup(
            MathTex(r'\text{The field }\boldsymbol{H}\text{ is then transformed into}'),
            MathTex(r'\text{ a vector shadow field }\boldsymbol{\vec{S}}\text{.}')
        ).set_z_index(7).arrange_submobjects(DOWN)
        shadow_field_box = SurroundingRectangle(
            shadow_field_group,
            buff=MED_LARGE_BUFF,
            color=RED,
            stroke_width=3,
            fill_color=RED_E,
            fill_opacity=0.95
        ).set_z_index(6)

        shadow_field_box.apply_matrix(np.linalg.inv(self.camera.generate_rotation_matrix())).scale(2)
        shadow_field_group.apply_matrix(np.linalg.inv(self.camera.generate_rotation_matrix())).scale(2)

        self.play(
            ReplacementTransform(check_group, shadow_field_group, run_time=0.5),
            ReplacementTransform(check_box, shadow_field_box, run_time=0.5),
        )

        self.wait(2)

        # top-down view, buildings removed
        trackers = self.camera.get_value_trackers()
        camera_phi, camera_theta, camera_zoom = trackers[0], trackers[1], trackers[4]
        flat_ray_vec = Arrow(
            start=ray_vec.get_start(),
            end=ray_vec.get_end(),
            color=RED,
            max_tip_length_to_length_ratio=0.3
        )
        self.play(
            camera_phi.animate(run_time=0.5).set_value(0),
            camera_theta.animate(run_time=0.5).set_value(-PI/2),
            camera_zoom.animate(run_time=0.5).set_value(1.5),
            Uncreate(buildings, run_time=0.5),
            Uncreate(shadow_field_box, run_time=0.5),
            Unwrite(shadow_field_group, run_time=0.5),
            Uncreate(active_line, run_time=0.5),
            ReplacementTransform(ray_vec, flat_ray_vec, run_time=0.5),
        )

        self.wait(1)

        self.play(
            camera_zoom.animate(run_time=0.5).set_value(0.75),
            Uncreate(flat_ray_vec, run_time=0.5),
        )

        sf_formula = MathTex(
            r'\boldsymbol{\vec{S}}(\phi, \lambda) = \begin{cases}' 
            r'\boldsymbol{\vec{0}} & \text{if observer is in shadow}\end{cases}' '\\\\'
            r'\hat{r}\cdot\left[\begin{matrix}' 
            '1 & 0 & 0\\\\0 & 1 & 0\\\\0 & 0 & 0' r'\end{matrix}\right] & \text{otherwise}'
        ).set_z_index(7)
        sf_formula_box = SurroundingRectangle(
            sf_formula,
            buff=MED_LARGE_BUFF,
            color=GREEN,
            stroke_width=3,
            fill_color=GREEN_E,
            fill_opacity=0.95
        ).set_z_index(6)

        self.play(
            Write(sf_formula, run_time=0.5),
            Create(sf_formula_box, run_time=0.5),
        )

        self.wait(2)

        further_use_group = VGroup(
            MathTex(r'\boldsymbol{\vec{S}}\text{ can be further used to determine whether a point}'),
            MathTex(r'\text{on the map is in shadow, or the direction of sunlight at that point.}')
        ).set_z_index(7).arrange_submobjects(DOWN)
        further_use_box = SurroundingRectangle(
            further_use_group,
            buff=MED_LARGE_BUFF,
            color=GREEN,
            stroke_width=3,
            fill_color=GREEN_E,
            fill_opacity=0.95
        ).set_z_index(6)

        self.play(
            ReplacementTransform(sf_formula, further_use_group, run_time=0.5),
            ReplacementTransform(sf_formula_box, further_use_box, run_time=0.5),
        )

        self.wait(3)
