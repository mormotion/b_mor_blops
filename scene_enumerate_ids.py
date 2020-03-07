import bpy
from bpy.props import BoolProperty, EnumProperty

class SCENE_OT_EnumerateScenePassIndexes(bpy.types.Operator):
    bl_idname = 'scene.enumerate_scene_pass_indexes'
    bl_label = 'Enumerate Pass Indexes'
    bl_options = {'REGISTER', 'UNDO'}

    only_selected : BoolProperty(name='Only Selected', default=True)
    do_materials : BoolProperty(name='Objects', default=True)
    do_objects : BoolProperty(name='Materials', default=False)

    @classmethod
    def poll(cls, context):
        return len(context.scene.objects) > 1

    def execute(self, context):
        target_objects = context.selected_objects if self.only_selected else context.scene.objects
        existing_obj_ids = [obj.pass_index for obj in bpy.data.objects if hasattr(obj, 'pass_index')]
        existing_mat_ids = [mat.pass_index for mat in bpy.data.materials]

        if self.do_materials:
            # Gather assigned materials
            slot_sets = [obj.material_slots for obj in target_objects if obj.material_slots]
            
            materials = [] 
            for slot_set in slot_sets:
                for slot in slot_set:
                    if slot.material and slot.material not in materials:
                        materials.append(slot.material)
            
            for mat in materials:
                mat_id = mat.pass_index
                while mat_id in existing_mat_ids:
                    mat_id += 1
                mat.pass_index = mat_id
                existing_mat_ids.append(mat_id)
        
        if self.do_objects:
            for obj in target_objects:
                obj_id = obj.pass_index
                while obj_id in existing_obj_ids:
                    obj_id += 1
                obj.pass_index = obj_id
                existing_obj_ids.append(obj_id)

        return {'FINISHED'}

classes = [
    SCENE_OT_EnumerateScenePassIndexes,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()