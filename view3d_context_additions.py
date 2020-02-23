import bpy
from bpy.types import Menu

"""
New Context Menus
Camera Context
    Set selected camera as active scene camera

TODO:

"""

import bpy
import bpy_extras

# Define Operators
##############################################

class OBJECT_OT_add_target(bpy.types.Operator):
    bl_idname = "object.add_target_for_selected"
    bl_label = "add target for selected"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        track_to = bpy.context.active_object.constraints.new('TRACK_TO')
        obj_target = bpy_extras.object_utils.object_data_add(context, obdata=None, operator=None, name=obj.name + '_target')
        track_to.target = obj_target
        track_to.track_axis = 'TRACK_NEGATIVE_Z'
        track_to.up_axis = 'UP_Y'
        return {'FINISHED'}


# Define Menus
##############################################

# It would be prefereble for this sort of operator, mass property
# setting, to be acheivable with the existing wm.context_set** ops
# Rewrite them for personal use then maybe draft a patch for bf?

# Light Types Menu
class VIEW3D_MT_change_light_type(Menu):
    bl_label = "Change Light Type"

    def draw(self, context):
        layout = self.layout
        # TODO: replace light operator with this shit. Bpy's wm.context_set_X should support iterables like wm.context_modal_mouse
        op_btn = layout.operator("wm.context_set_enum", text='Point')
        op_btn.data_path = "active_object.data.type"
        op_btn.value = 'POINT'
        op_btn = layout.operator("wm.context_set_enum", text='Sun')
        op_btn.data_path = "active_object.data.type"
        op_btn.value = 'SUN'
        op_btn = layout.operator("wm.context_set_enum", text='Spot')
        op_btn.data_path = "active_object.data.type"
        op_btn.value = 'SPOT'
        op_btn = layout.operator("wm.context_set_enum", text='Area')
        op_btn.data_path = "active_object.data.type"
        op_btn.value = 'AREA'


def VIEW3D_MT_context_menus(self, context):
    obj = context.object
    layout = self.layout
    layout.separator()
    
    if obj.type == 'CAMERA':
        # Set Camera As Active
        op_btn = layout.operator("wm.context_set_id", text="Set Camera as Active")
        op_btn.data_path = "scene.camera"
        op_btn.value = obj.name
    
    if obj.type == 'LIGHT':
        layout.menu("VIEW3D_MT_change_light_type")

    if obj.type in ['CAMERA', 'LIGHT']:
        op_btn = layout.operator(OBJECT_OT_add_target.bl_idname, text="Add Target for Active")

    layout.separator()

classes = (
    OBJECT_OT_add_target,
    VIEW3D_MT_change_light_type,
)

def register():
    from bpy.utils import register_class
    # for cls in classes:
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.prepend(VIEW3D_MT_context_menus)

def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.remove(VIEW3D_MT_context_menus)