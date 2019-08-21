import bpy
import gpu
import bgl
import blf
from mathutils import Vector
from gpu_extras.batch import batch_for_shader
from bpy_extras.io_utils import ImportHelper

# TODO: Accept keyboards inputs for value changes


NUMBER_INPUTS = {
    'ZERO': 0,
    'ONE': 1,
    'TWO': 2,
    'THREE': 3,
    'FOUR': 4,
    'FIVE': 5,
    'SIX': 6,
    'SEVEN': 7,
    'EIGHT': 8,
    'NINE': 9,
    'NUMPAD_0': 0,
    'NUMPAD_1': 1,
    'NUMPAD_2': 2,
    'NUMPAD_3': 3,
    'NUMPAD_4': 4,
    'NUMPAD_5': 5,
    'NUMPAD_6': 6,
    'NUMPAD_7': 7,
    'NUMPAD_8': 8,
    'NUMPAD_9': 9,
}

COLORS = {
    'red': (1, 0, 0, 1),
    'green': (0, 1, 0, 1),
    'blue': (0, 0, 1, 1),
}

class VIEW3D_OT_draw_image_test(bpy.types.Operator, ImportHelper):
    bl_idname = "view3d.view_image_test"
    bl_label = "view3d image display test"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def get_image_coords(self, context, image):
        # this is ugly and should be redone
        target_screen_percentage = 0.8
        area = context.area
        area_center = (area.width * 0.5, area.height * 0.5)
        target_width = area.width * target_screen_percentage
        target_height = area.height * target_screen_percentage
        current_width_ratio = target_width / image.size[0]
        current_height_ratio = target_height / image.size[1]
        scaler = min(current_width_ratio, current_height_ratio)
        render_width = image.size[0] * scaler
        render_height = image.size[1] * scaler
        origin = (area_center[0] - (render_width * 0.5),
                  area_center[1] - (render_height * 0.5))

        output = (origin,
                  (origin[0] + render_width, origin[1]),
                  (origin[0] + render_width, origin[1] + render_height),
                  (origin[0], origin[1] + render_height))
        # print(output)
        return output

    ####################

#    def draw_callback_px(self, context, image, image_coords):
    def draw_callback_px(self, context, image_coords):

        #image = bpy.data.images[1]
        area = context.area
        shader = gpu.shader.from_builtin('2D_IMAGE')

        # Draw spritesheet
        batch = batch_for_shader(
            shader, 'TRI_FAN',
            {
                "pos": (image_coords[0],
                        image_coords[1],
                        image_coords[2],
                        image_coords[3],),
                "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
            },
        )

        if self.image.gl_load():
            raise Exception()

        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.image.bindcode)

        shader.bind()
        shader.uniform_int("image", 0)
        # shader.uniform_int("image", 0)
        batch.draw(shader)

        #######################################################################
        # Draw Grid overlay
        #######################################################################

        x_cell_count = self.sheet_attributes['X Cells']
        y_cell_count = self.sheet_attributes['Y Cells']
        total = x_cell_count * y_cell_count + self.sheet_attributes['Total Offset']

        x_step = 1.0 / x_cell_count
        y_step = 1.0 / y_cell_count

        coords = []
        indices = []

        # Created normalized grid coords and line indices
        cell_index = 0
        for row in range(y_cell_count):
            for column in range(x_cell_count):
                if cell_index == total:
                    continue

                # Rectangle coords
                coords.extend((
                    Vector((x_step * column, y_step * row)),
                    Vector((x_step * (1 + column), y_step * row)),
                    Vector((x_step * (1 + column), y_step * (1 + row))),
                    Vector((x_step * column, y_step * (1 + row))),
                ))

                base_indices = ((0, 1),
                                (1, 2),
                                (2, 3),
                                (3, 0),
                                )
                index_offset = 4 * cell_index
                for a, b in base_indices:
                    indices.append((a + index_offset, b + index_offset)) 

                cell_index += 1

        x_scaler = abs(image_coords[0][0] - image_coords[1][0])
        y_scaler = abs(image_coords[0][1] - image_coords[3][1]) * -1

        coords = list(map(lambda xy: Vector((xy[0] * x_scaler, xy[1] * y_scaler)), coords))
        coords = list(map(lambda xy: xy + Vector(image_coords[3]), coords))

        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": coords}, indices=indices)

        # bgl.glEnable(bgl.GL_FRAMEBUFFER_SRGB)  glLineWidth(width):
        bgl.glLineWidth(2)

        shader.bind()
        # shader.uniform_float("color", (1, 0, 0, 1))
        shader.uniform_float("color", COLORS[list(COLORS.keys())[self.draw_color_index]])
        batch.draw(shader)

        #######################################################################

        # Draw Text
        active_color = (1, 1, 1, 1)
        inactive_color = (0.5, 0.5, 0.5, 1)

        font_id = 0

        origin_x = 2
        origin_y = 80
        y_step = -20
        blf.size(font_id, 24, 72)

        for i, (key, value) in enumerate(self.sheet_attributes.items()):
            blf.position(font_id, origin_x, origin_y + (y_step * i), 0)
            if key == self.states[self.state_index]:
                blf.color(font_id, *active_color)
            else:
                blf.color(font_id, *inactive_color)
            blf.draw(font_id, "{}: {}".format(key, value))

        blf.position(font_id, origin_x, origin_y + (y_step * len(self.sheet_attributes.items())), 0)
        blf.color(font_id, *inactive_color)
        blf.draw(font_id, "Change Color: C")

    ###########################################################################


    def invoke(self, context, event):
        # self.image = bpy.data.images[0]
        print(self.filepath)

        self.image = bpy.data.images.load(self.filepath)

        # Colormanagement must be 'disabled' or viewport gamme will be incorrect
        # Returned to default on draw handle unregister
        self.initial_image_colorspace = self.image.colorspace_settings.name
        self.image.colorspace_settings.name = 'Raw'

        self.input_state = 'Set X cells'
        self.draw_color = COLORS['red']
        self.draw_color_index = 0

        self.sheet_attributes = {
            'X Cells': 1,
            'Y Cells': 1,
            'Total Offset': 0,
        }
        self.states = tuple(self.sheet_attributes.keys())
        self.state_index = 0

        # input mapping
        self.input_mappings = {
            'increase value': ['WHEELUPMOUSE', 'PLUS'],
            'decrease value': ['WHEELDOWNMOUSE', 'MINUS'],
            'next input': ['LEFTMOUSE'],
            'previous input': ['RIGHTMOUSE'],
            'confirm': ['RET'],
            'cancel': ['ESC'],
            'color': ['C'],
        }

        #args = (self, context)
        args = (context, self.get_image_coords(context, self.image))
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in self.input_mappings['increase value'] and event.value == 'PRESS':
            self.sheet_attributes[self.states[self.state_index]] += 1
        if event.type in self.input_mappings['decrease value'] and event.value == 'PRESS':
            self.sheet_attributes[self.states[self.state_index]] -= 1
        if event.type in self.input_mappings['next input'] and event.value == 'PRESS':
            self.state_index += 1
            self.state_index = min(self.state_index, len(self.states))
        if event.type in self.input_mappings['previous input'] and event.value == 'PRESS':
            self.state_index -= 1
            self.state_index = max(self.state_index, 0)
        if event.type in self.input_mappings['color'] and event.value == 'PRESS':
            self.draw_color_index = (self.draw_color_index + 1) % len(COLORS.keys())
        if event.type in self.input_mappings['confirm'] and event.value == 'PRESS':
            return self.finish()
        if event.type in self.input_mappings['cancel']:
            return self.cancelled()

        # Cap Values
        self.sheet_attributes['X Cells'] = max(self.sheet_attributes['X Cells'], 1)
        self.sheet_attributes['Y Cells'] = max(self.sheet_attributes['Y Cells'], 1)
        self.sheet_attributes['Total Offset'] = min(self.sheet_attributes['Total Offset'], 0)
        mininmum_offset_value = (self.sheet_attributes['X Cells'] * self.sheet_attributes['Y Cells']) * -1 + 1
        self.sheet_attributes['Total Offset'] = max(self.sheet_attributes['Total Offset'], mininmum_offset_value)
        self.state_index = min(self.state_index, len(self.states) - 1)
        self.state_index = max(self.state_index, 0)

        return {"RUNNING_MODAL"}

    def finish(self):
        self.image.colorspace_settings.name = self.initial_image_colorspace
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
        print('we done, yeah')
        return {"FINISHED"}

    def cancelled(self):
        self.image.colorspace_settings.name = self.initial_image_colorspace
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
        return {"CANCELLED"}


def register():
    bpy.utils.register_class(VIEW3D_OT_draw_image_test)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_draw_image_test)


if __name__ == "__main__":
    register()
