import bpy
import bmesh
import random
from math import pi, radians
from mathutils import Vector, Matrix, Euler, bvhtree
from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty, FloatVectorProperty, BoolProperty
from . import enum_populators
from . import mathutil_types_random

import importlib
importlib.reload(mathutil_types_random)

def populate_plane_from_group(context, group, generations, loc_range, scale_min, scale_max,
                              vertex_steps, seed, do_new_groups, rand_rot_range, rot_offset,
                              cast_offset, ray_scaler):
    mathutil_types_random.seed(seed)
    loc_max = loc_range - (loc_range * 0.5)
    loc_min = loc_max * -1
    rot_max = rand_rot_range
    # rot_min = Euler((0,0,0))
    rot_min = Euler((rot_max.x * -1,
                     rot_max.y * -1,
                     rot_max.z * -1))
    
    grp_objs = [o for o in group.objects]
    spawned_objects = []
    collision_members = []
    collision_mesh = bpy.data.meshes.new('ray_catcher')
    
    for gen_num in range(generations):
        print('Starting Generation: ', gen_num)
        rand_obj = random.choice(grp_objs)
        tranlation_matrix = mathutil_types_random.rand_translation_matrix(loc_min, loc_max)
        rotation_matrix = mathutil_types_random.rand_rotation_matrix(rot_min, rot_max)
        scale_matrix = Matrix.Scale( random.uniform(scale_min, scale_max), 4)
        transform_candidate = tranlation_matrix * scale_matrix * rotation_matrix.to_4x4()

        if spawned_objects:
            # Update Collision Mesh
            for spwn_obj in spawned_objects:
                if spwn_obj not in collision_members:
                    ray_collider_bm = bmesh.new()
                    # Add and transform new geo
                    ray_collider_bm.from_object(spwn_obj, context.scene)
                    for v in ray_collider_bm.verts[:]:
                        v.co = spwn_obj.matrix_world * v.co
                    # Get Existing Geo
                    ray_collider_bm.from_mesh(collision_mesh)
                    ray_collider_bm.to_mesh(collision_mesh)
                    ray_collider_bm.free()
                    # Confirm new geo part of collider
                    collision_members.append(spwn_obj)
            
            # Setup BVH for raycasting
            ray_collider_bm = bmesh.new()
            ray_collider_bm.from_mesh(collision_mesh)
            bmesh.ops.triangulate(ray_collider_bm, faces=ray_collider_bm.faces)
            ray_collider_tree = bvhtree.BVHTree.FromBMesh(ray_collider_bm)
            ray_collider_bm.free()
            # del ray_collider_bm

            # Ray Caster
            ray_cast_offset = cast_offset
            ray_dir = ray_cast_offset.normalized() * -1
            ray_len = ray_cast_offset.length * ray_scaler

            ray_src_mesh = rand_obj.data
            ray_source_bm = bmesh.new()
            ray_source_bm.from_mesh(ray_src_mesh)
            for v in ray_source_bm.verts[:]:
                v.co = (transform_candidate * v.co) + ray_cast_offset
            ray_casters = [v.co for i, v in enumerate(ray_source_bm.verts) if i % vertex_steps == 0]
            # ray_source_bm.free() # Free caster bmesh from memory
            # del ray_source_bm

            # Do Casting
            collision_registered = False
            for ray_src in ray_casters:
                ray = ray_collider_tree.ray_cast(ray_src, ray_dir, ray_len)
                if None not in ray:
                    collision_registered = True
                    break

            if not collision_registered:
                # Create New Object because valid placement found
                new_object = rand_obj.copy()
                context.scene.objects.link(new_object)
                new_object.matrix_world = transform_candidate
                spawned_objects.append(new_object)

        else:    
            # Create New Object because none exist
            new_object = rand_obj.copy()
            context.scene.objects.link(new_object)
            new_object.matrix_world = transform_candidate
            spawned_objects.append(new_object)




class OBJECT_OT_populate_plane_from_group(bpy.types.Operator):
    """ Create a plane populated with random objects from a group using dart throwing """
    bl_idname = 'object.populate_plane_from_group'
    bl_label = 'Populate plane from group'
    bl_description = 'Populate plane with random members from group'
    bl_options = {'REGISTER', 'UNDO'}

    group_name = EnumProperty(name='Group Name', items=enum_populators.get_enum_group_names)
    generations = IntProperty(name='Generations', min=0, default=1, options={'SKIP_SAVE'})
    vertex_steps = IntProperty(name='Vertex Steps', min=1, default=1, options={'SKIP_SAVE'})
    loc_range = FloatVectorProperty(name='Location Range', size=2, min=0, subtype='TRANSLATION', default=(1, 1))
    rand_rot_range = FloatVectorProperty(name='Rotation Range', size=3, subtype='EULER', default=(0, 0, 0))
    rot_offset = FloatVectorProperty(name='Rotation Offset', size=3, subtype='EULER', default=(0, 0, 0))
    scale_min = FloatProperty(name='Scale Min', min=0, default=1, options={'SKIP_SAVE'}) 
    scale_max = FloatProperty(name='Scale Max', min=0, default=1, options={'SKIP_SAVE'}) 
    seed = IntProperty(name='Seed', min=0, default=1, options={'SKIP_SAVE'})
    do_new_groups = BoolProperty(name='New Groups', default=False, options={'SKIP_SAVE'})
    cast_offset = FloatVectorProperty(name='Raycast Offset', size=3, min=0, subtype='TRANSLATION', default=(0, 0, 1))
    ray_scaler = FloatProperty(name='Ray Scaler', min=0, default=1.5, options={'SKIP_SAVE'}) 

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if self.group_name:
            group = bpy.data.groups[self.group_name]
            populate_plane_from_group(context, group=group, generations=self.generations,
                                      loc_range=self.loc_range, vertex_steps=self.vertex_steps,
                                      seed=self.seed, do_new_groups=self.do_new_groups,
                                      rand_rot_range=self.rand_rot_range, rot_offset=self.rot_offset,
                                      cast_offset=self.cast_offset, ray_scaler=self.ray_scaler,
                                      scale_min=self.scale_min, scale_max=self.scale_max)

        if not self.group_name:
            self.report(type={'INFO'}, message='No Groups in Scene')
        return {'FINISHED'}