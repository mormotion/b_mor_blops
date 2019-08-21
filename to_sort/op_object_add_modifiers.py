import bpy
from bpy.props import EnumProperty

# I can't find this enum in the api
OBJECT_MODIFIERS = (
    'DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'UV_PROJECT',
    'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY',
    'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT',
    'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW',
    'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WIREFRAME',
    'ARMATURE', 'CAST', 'CORRECTIVE_SMOOTH', 'CURVE', 'DISPLACE',
    'HOOK', 'LAPLACIANSMOOTH', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM',
    'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'WARP', 'WAVE',
    'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'FLUID_SIMULATION',
    'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'SMOKE', 'SOFT_BODY', 'SURFACE'
)

def get_object_modifier_enum(self, context):
    return [(m, m, m) for m in OBJECT_MODIFIERS]


class OBJECT_OT_add_modifier_to_selected(bpy.types.Operator):
    bl_idname = 'object.add_modifier_to_selected'
    bl_label = 'Add Modifier to Selected Objects'
    bl_description = 'Add Modifier to Selected Objects'
    bl_property = 'modifier_name' # Search popup uses this
    bl_options = {'REGISTER', 'UNDO'}

    modifier_name = EnumProperty(items=get_object_modifier_enum)

    @classmethod
    def poll(self, context):
        return len(context.selected_objects) is not 0

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}

    def execute(self, context):
        # print(self.modifier_name)
        for o in context.selected_objects:
            if o.type != 'MESH':
                continue
            o.modifiers.new(self.modifier_name, self.modifier_name)
            context.scene.update()

        return {'FINISHED'}


if __name__ == '__main__':
    pass