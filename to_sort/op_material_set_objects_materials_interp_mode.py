import bpy
from bpy.props import EnumProperty


def main(context, interpolation):
    # Get all materials from selected
    materials = []
    for o in context.selected_objects:
        obj_mats = [i.material for i in o.material_slots]
        materials += obj_mats
                
    image_nodes = []
    for mat in materials:
        nodes = mat.node_tree.nodes
        mat_img_nodes = [node for node in nodes if node.type == "TEX_IMAGE"]
        image_nodes += mat_img_nodes
    
    for node in image_nodes:
        node.interpolation = interpolation
        
    
class OBJECT_OT_set_objects_material_images_interp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_objects_materials_image_interp"
    bl_label = "Set Objects Materials Image Interp"
    bl_options = {"REGISTER", "UNDO"}
    
    interpolation = EnumProperty(items=[('Linear', 'Linear', 'Linear Interpolation'),
                                        ('Closest', 'Closest', 'Closest Interpolation'),
                                        ('Cubic', 'Cubic', 'Cubic Interpolation'),
                                        ('Smart', 'Smart', 'Smart Interpolation')],
                                 name="Image Interpolation",default='Linear')
                                 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, self.interpolation)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_set_objects_material_images_interp)

def unregister():
    bpy.utils.unregister_class(OBJECT_set_objects_material_images_interp)

if __name__ == "__main__":
    register()
