from __future__ import division
from animations.animation import Animation

__author__ = 'guydmann'


class HueRotation(Animation):
    color_multiplier = None

    def set_color_multiplier(self, new_color_multiplier):
        self.color_multiplier = new_color_multiplier
