
"""
New Context Menus
Camera Context
    Set selected camera as active scene camera

TODO:

"""

import bpy
import bpy_extras
from bpy.props import EnumProperty, BoolProperty

# Define Operators
##############################################
class OBJECT_OT_look_at(bpy.types.Operator):
    bl_idname = 'object.look_at'
    bl_label = 'Look At'
    bl_options = {'REGISTER', 'UNDO'}

    mode : EnumProperty(name='Mode',
                        items=(
                            ('CURSOR', 'Cursor', 'Target Cursor'),
                            ('ACTIVE', 'Active', 'Target Active Object'),
                        ))
    track_to : BoolProperty(name='Track To', default=False)


    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        if self.mode == 'CURSOR':
            input_objects = context.selected_objects[:]
            target_loc = context.scene.cursor.location
        if self.mode == 'ACTIVE':
            input_objects = [obj for obj in context.selected_objects if obj is not context.active_object]
            if not input_objects:
                self.report({'INFO'}, 'No valid operator targets')
                return {'CANCELLED'}
            target_loc = context.active_object.location

        if self.track_to:

            if self.mode == 'ACTIVE':
                obj_target = context.active_object
            else:
                obj_target = bpy_extras.object_utils.object_data_add(context, obdata=None, operator=None, name='target')

            for obj in input_objects:
                # Get Last constaint of type Track_to
                try:
                    track_to = [c for c in obj.constraints if c.type == 'TRACK_TO'][-1]
                # If unabe to find track to, create one
                except IndexError:
                    track_to = obj.constraints.new('TRACK_TO')
                track_to.target = obj_target
                track_to.track_axis = 'TRACK_NEGATIVE_Z'
                track_to.up_axis = 'UP_Y'

        # Not setting tracking
        else:
            for obj in input_objects:
                obj_loc = obj.matrix_world.to_translation()
                direction = target_loc - obj_loc
                point_at_quat = direction.to_track_quat('-Z', 'Y')
                point_at_matrix = point_at_quat.to_matrix().to_4x4()
                new_m = point_at_matrix
                new_m.translation = obj_loc
                obj.matrix_world = new_m
    
        return {'FINISHED'}


# Define Menus
##############################################

# It would be prefereble for this sort of operator, mass property
# setter, to be acheivable with the existing wm.context_set** ops
# Rewrite them for personal use then maybe draft a patch for bf?

# Light Types Menu
class VIEW3D_MT_change_light_type(bpy.types.Menu):
    bl_label = "Change Light Type"

    def draw(self, context):
        layout = self.layout
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
    

# Targetting Menu
class VIEW3D_MT_targeting(bpy.types.Menu):
    bl_label = 'Look At'

    def draw(self, context):
        layout = self.layout
        op = layout.operator(OBJECT_OT_look_at.bl_idname, text='Look at Cursor')
        op.mode = 'CURSOR'
        op.track_to = False
        op = layout.operator(OBJECT_OT_look_at.bl_idname, text='Look at Active')
        op.mode = 'ACTIVE'
        op.track_to = False
        op = layout.operator(OBJECT_OT_look_at.bl_idname, text='Track to New Empty')
        op.mode = 'CURSOR'
        op.track_to = True
        op = layout.operator(OBJECT_OT_look_at.bl_idname, text='Track to Active')
        op.mode = 'ACTIVE'
        op.track_to = True


def VIEW3D_MT_context_extras(self, context):
    obj = context.object
    layout = self.layout
    layout.separator()
    
    if obj.type == 'CAMERA':
        # Set Camera As Active
        op_btn = layout.operator("wm.context_set_id", text="Set Camera as Active")
        op_btn.data_path = "scene.camera"
        op_btn.value = obj.name

    
    if obj.type == 'LIGHT':
        # layout.menu("VIEW3D_MT_change_light_type")
        layout.menu(VIEW3D_MT_change_light_type.__name__)

    layout.separator()
    layout.menu(VIEW3D_MT_targeting.__name__)
    layout.separator()

classes = (
    VIEW3D_MT_change_light_type,
    VIEW3D_MT_targeting,
    OBJECT_OT_look_at,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.prepend(VIEW3D_MT_context_extras)

def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.remove(VIEW3D_MT_context_extras)