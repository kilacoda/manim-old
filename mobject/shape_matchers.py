from manimlib.constants import *
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.color import Color
from manimlib.utils.config_ops import digest_config
from manimlib.mobject.geometry import Arrow
from manimlib.utils.space_ops import get_norm

class SurroundingRectangle(Rectangle):
    CONFIG = {
        "color": YELLOW,
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        kwargs["width"] = mobject.get_width() + 2 * self.buff
        kwargs["height"] = mobject.get_height() + 2 * self.buff
        Rectangle.__init__(self, **kwargs)
        self.move_to(mobject)


class BackgroundRectangle(SurroundingRectangle):
    CONFIG = {
        "color": BLACK,
        "stroke_width": 0,
        "stroke_opacity": 0,
        "fill_opacity": 0.75,
        "buff": 0
    }

    def __init__(self, mobject, **kwargs):
        SurroundingRectangle.__init__(self, mobject, **kwargs)
        self.original_fill_opacity = self.fill_opacity

    def pointwise_become_partial(self, mobject, a, b):
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style_data(self,
                       stroke_color=None,
                       stroke_width=None,
                       fill_color=None,
                       fill_opacity=None,
                       family=True
                       ):
        # Unchangable style, except for fill_opacity
        VMobject.set_style_data(
            self,
            stroke_color=BLACK,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=fill_opacity
        )
        return self

    def get_fill_color(self):
        return Color(self.color)


class Cross(VGroup):
    CONFIG = {
        "stroke_color": RED,
        "stroke_width": 6,
    }

    def __init__(self, mobject, **kwargs):
        VGroup.__init__(self,
                        Line(UP + LEFT, DOWN + RIGHT),
                        Line(UP + RIGHT, DOWN + LEFT),
                        )
        self.replace(mobject, stretch=True)
        self.set_stroke(self.stroke_color, self.stroke_width)


class Underline(Line):
    CONFIG = {
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(LEFT, RIGHT)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)


class Cancel(VGroup):
    '''``Cancel`` class created by @theoremofbeethoven

        This is to cross a mobject (text) with an arrow
        and some text(texmob) at the tip.
    '''
    CONFIG = {
        "line_kwargs": {"color": RED},
        "buff_text": None,
        "buff_line": 0.7,
    }

    def __init__(self, text, texmob=None, **kwargs):

        digest_config(self, kwargs)
        VGroup.__init__(self, **kwargs)

        pre_coord_dl = text.get_corner(DL)
        pre_coord_ur = text.get_corner(UR)
        reference_line = Line(pre_coord_dl, pre_coord_ur)
        reference_unit_vector = reference_line.get_unit_vector()
        coord_dl = text.get_corner(
            DL) - text.get_center() - reference_unit_vector*self.buff_line
        coord_ur = text.get_corner(
            UR) - text.get_center() + reference_unit_vector*self.buff_line
        if texmob == None:
            line = Line(coord_dl, coord_ur, **self.line_kwargs)
            self.add(line)
        else:
            arrow = Arrow(coord_dl, coord_ur, **self.line_kwargs)
            unit_vector = arrow.get_unit_vector()
            if self.buff_text == None:
                self.buff_text = get_norm(
                    (texmob.get_center()-texmob.get_critical_point(unit_vector))/2)*2
            texmob.move_to(arrow.get_end()+unit_vector*self.buff_text)
            self.add(arrow, texmob)
