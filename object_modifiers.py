import bpy
from mathutils import Vector
from bpy.props import BoolProperty, FloatProperty, IntProperty


class OBJECT_OT_Add_Scaled_Lattice(bpy.types.Operator):
    bl_idname = 'object.add_scaled_lattice'
    bl_label = 'Add Scaled Lattice'
    bl_options = {'REGISTER', 'UNDO'}

    x_divs : IntProperty(name='X Divs', min=2, max=64, default=2)
    y_divs : IntProperty(name='Y Divs', min=2, max=64, default=2)
    z_divs : IntProperty(name='Z Divs', min=2, max=64, default=2)

    per_selected : BoolProperty(name='Per Object', default=False)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        valid_target_types = ['MESH','CURVE','FONT']
        if self.per_selected:
            valid_targets = [obj for obj in context.selected_objects if obj.type in valid_target_types]
            if not valid_targets:
                return {'CANCELLED'}
            for obj in context.selected_objects:
                self.add_scaled_lattice(context, obj)
        else:
            if context.active_object.type not in valid_target_types:
                return {'CANCELLED'}
            self.add_scaled_lattice(context, context.active_object)
        return {'FINISHED'}

    def add_scaled_lattice(self, context, target_object):
        target = target_object
        target_center = self.get_objects_center(context, [target])

        # Create lattice object
        lattice_data = bpy.data.lattices.new(name=f'{target.name}')
        lattice_obj = bpy.data.objects.new(name=f'{target.name}_lattice', object_data=lattice_data)
        context.view_layer.active_layer_collection.collection.objects.link(lattice_obj)

        # Match lattice transforms
        # target_matrix.translation = target_center
        # lattice_obj.matrix_world = target_matrix
        # lattice_obj.location = target_center
        lattice_obj.scale = self.get_object_dimensions(context, target)

        # Parent to target
        lattice_obj.parent = target

        # Set divisions
        lattice_data.points_u = self.x_divs
        lattice_data.points_v = self.y_divs
        lattice_data.points_w = self.z_divs

        # Setup Modifier
        lattice_mod = target.modifiers.new('lattice', type='LATTICE') 
        lattice_mod.object = lattice_obj


    def get_object_dimensions(self, context, target_object):
        target = target_object

        bbox = [Vector((t)) for t in target.bound_box]
        x_values = sorted([v.x for v in bbox])
        y_values = sorted([v.y for v in bbox])
        z_values = sorted([v.z for v in bbox])

        x_len = abs(x_values[0] - x_values[-1])
        y_len = abs(y_values[0] - y_values[-1])
        z_len = abs(z_values[0] - z_values[-1])

        return Vector((x_len, y_len, z_len))


    def get_objects_center(self, context, target_objects:list):
        # Calculate the center based on world space bounds of target objects
        bbox_points = [] 
        for obj in target_objects:
            bbox_points += [obj.matrix_world @ Vector((p)) for p in obj.bound_box]

        center = Vector((
            sum([v.x for v in bbox_points]) / len(bbox_points),
            sum([v.y for v in bbox_points]) / len(bbox_points),
            sum([v.z for v in bbox_points]) / len(bbox_points),
        ))
        return center

classes = [
    OBJECT_OT_Add_Scaled_Lattice,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)