import bpy

# WARNING: Uses operators

def temp_rbd_drop_selected_objects(context):
    targets = context.selected_objects
    scene = context.screen.scene
    frame_at_execution = scene.frame_current

    # Make Active RBD selected_objects
    bpy.ops.rigidbody.objects_add(type='ACTIVE')

    # Create Ground Collider
    bpy.ops.mesh.primitive_plane_add(radius=100, location=(0,0,0))
    ground = context.active_object

    # Set as Collider
    bpy.ops.rigidbody.object_add(type='PASSIVE')

    scene.frame_current = scene.frame_end

    # Run sim
    bpy.ops.ptcache.free_bake_all()
    bpy.ops.ptcache.bake_all()
    scene.update()


    for obj in scene.objects:
        if obj in targets:
            obj.select = True
        else:
            obj.select = False

    scene.update()
    bpy.ops.object.visual_transform_apply()
    bpy.ops.rigidbody.objects_remove()

    # Reset Framae
    scene.frame_current = frame_at_execution

    # Remove Collider
    bpy.data.objects.remove(ground)


class OBJECT_OT_drop_to_floor_rbd(bpy.types.Operator):
    bl_idname = "object.drop_to_floor_rbd"
    bl_label = "Drop to floor rbd"
    bl_description = "Drop object to floor using temporary rbd setup"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D' and context.active_object is not None:
            return True

    def execute(self, context):
        temp_rbd_drop_selected_objects(context)
        return {"FINISHED"}
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
