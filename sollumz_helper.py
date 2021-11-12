import traceback
import time
from abc import abstractmethod
from .sollumz_properties import DrawableType


class SOLLUMZ_OT_base:
    bl_options = {"UNDO"}
    bl_action = "do"
    bl_showtime = False

    def __init__(self):
        self.messages = []

    @abstractmethod
    def run(self, context):
        pass

    def execute(self, context):
        start = time.time()
        try:
            result = self.run(context)
            reset_sollumz_view(context.scene)
        except:
            result = False
            self.error(
                f"Error occured running operator : {self.bl_idname} \n {traceback.format_exc()}")
        end = time.time()

        if self.bl_showtime and result == True:
            self.message(
                f"{self.bl_label} took {round(end - start, 3)} seconds to {self.bl_action}.")

        if len(self.messages) > 0:
            self.message('\n'.join(self.messages))

        if result:
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def message(self, msg):
        self.report({"INFO"}, msg)

    def warning(self, msg):
        self.report({"WARNING"}, msg)

    def error(self, msg):
        self.report({"ERROR"}, msg)


def reset_sollumz_view(scene):
    scene.hide_collision = not scene.hide_collision
    scene.hide_high_lods = not scene.hide_high_lods
    scene.hide_medium_lods = not scene.hide_medium_lods
    scene.hide_low_lods = not scene.hide_low_lods
    scene.hide_very_low_lods = not scene.hide_very_low_lods

    scene.hide_collision = not scene.hide_collision
    scene.hide_high_lods = not scene.hide_high_lods
    scene.hide_medium_lods = not scene.hide_medium_lods
    scene.hide_low_lods = not scene.hide_low_lods
    scene.hide_very_low_lods = not scene.hide_very_low_lods


def is_sollum_object_in_objects(objs):
    for obj in objs:
        if obj.sollum_type != DrawableType.NONE:
            return True
    return False


def is_sollum_type(obj, type):
    return obj.sollum_type in type._value2member_map_
