import json
import engine as en
import os
import pygame as pg


class Animation:
    _animations = {}

    def __init__(self, fps=10):
        self.time_since_last_update = 0
        self.fps = fps
        self.ms_per_frame = 1000. / fps
        self.animation_rects = None
        self.num_frames = 0
        self.current_frame = 0

    def load_animation_file(self, filename, scale):
        res_dir = en.get_resources_directory()
        os_filename = os.path.join(res_dir, filename)

        if os_filename in Animation._animations.keys():
            self.animation_rects = Animation._animations[os_filename]
            self.num_frames = len(self.animation_rects)
            return Animation._animations[os_filename]

        with open(os_filename) as f:
            animation_data = json.load(f)

        frames = animation_data['frames']

        animation_rects = []
        for frame in frames:
            rect_dict = frame['frame']
            animation_rects.append(
                pg.Rect(rect_dict['x'] * scale,
                 rect_dict['y'] * scale,
                 rect_dict['w'] * scale,
                 rect_dict['h'] * scale))

        self.animation_rects = animation_rects
        self.num_frames = len(animation_rects)
        Animation._animations[os_filename] = self.animation_rects
        en.graphical_logger.log("Loaded Animation" + os_filename)
        return animation_rects

    def get_new_frame_rect(self, dt):
        self.time_since_last_update += dt
        self.time_since_last_update %= (self.ms_per_frame * self.num_frames)
        self.current_frame = int(self.time_since_last_update / self.ms_per_frame)
        return self.animation_rects[self.current_frame].copy()
