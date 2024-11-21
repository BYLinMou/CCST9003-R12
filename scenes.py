from manim import *

# for presentation of the CCST9003 project

# SolarAngleScene: shows how the solar position is calculated
class SolarAngleScene(ThreeDScene):
    def construct(self):
        # look down at the x-y plane
        self.set_camera_orientation(phi=0, theta=-PI/2, zoom=0.75)

        # constructs a 3D coordinate system
        axes = ThreeDAxes(
            x_range=[-16, 16, 2],
            y_range=[-10, 10, 2],
            z_range=[0, 10],
            x_length=16,
            y_length=10,
        )
        x_label = axes.get_x_axis_label(Text('East', color=BLUE))
        y_label = axes.get_y_axis_label(Text('North', color=BLUE), buff=-0.5)
        self.play(Create(axes))
        self.play([Write(x_label), Write(y_label)])
        self.wait(5)