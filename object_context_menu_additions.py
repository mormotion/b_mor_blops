import bpy
from bpy.types import Menu

"""
New Context Menus
Camera Context
    Set selected camera as active scene camera

TODO:
    Change Light Type

"""

# It would be prefereble for this sort of operator, mass property
# setting, to be acheivable with the existing wm.context_set** ops
# Rewrite them for personal use then maybe draft a patch for bf?

class OBJECT_OT_set_light_type(bpy.types.Operator):
    bl_idname = 'object.set_light_type'
    bl_label = 'Set type of selected lights'
    bl_description = 'Set light type of all selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    light_type : bpy.props.EnumProperty(name='Light Type',
                        items=[('POINT', 'Point', 'Point'),
                               ('SUN', 'Sun', 'Sun'),
                               ('SPOT', 'Spot', 'Spot'),
                               ('AREA', 'Area', 'Area'),],
                        )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) is not 0

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == "LIGHT":
                obj.data.type = self.light_type
        return {'FINISHED'}

# Light Types Menu
class VIEW3D_MT_change_light_type(Menu):
    bl_label = "Change Light Type"

    def draw(self, context):
        layout = self.layout
        op_btn = layout.operator("object.set_light_type", text='Point')
        op_btn.light_type = 'POINT'
        op_btn = layout.operator("object.set_light_type", text='Sun')
        op_btn.light_type = 'SUN'
        op_btn = layout.operator("object.set_light_type", text='Spot')
        op_btn.light_type = 'SPOT'
        op_btn = layout.operator("object.set_light_type", text='Area')
        op_btn.light_type = 'AREA'

def draw_menu(self, context):

    obj = context.object

    layout = self.layout
    layout.separator()
    
    if obj.type == "CAMERA":
        # Set Camera As
        op_btn = layout.operator("wm.context_set_id", text="Set Camera as Active")
        op_btn.data_path = "scene.camera"
        op_btn.value = obj.name
    
    if obj.type == 'LIGHT':
        layout.menu("VIEW3D_MT_change_light_type")

    layout.separator()

classes = (
    VIEW3D_MT_change_light_type,
    OBJECT_OT_set_light_type,
)

def register():
    from bpy.utils import register_class
    # for cls in classes:
    for cls in classes:
        register_class(cls)
    # register_class(VIEW3D_MT_change_light_type)

    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_menu)

def unregister():
    from bpy.utils import unregister_class
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)

    for cls in classes:
        unregister_class(cls)