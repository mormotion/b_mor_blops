import bpy
from bpy.props import IntVectorProperty
import bmesh
from mathutils import Vector


def grid_bisect_mesh(object_mode, mesh, bbox, x_steps, y_steps, z_steps):
    mesh = mesh
    # Vectors (left hand, z-up)
    root = Vector(bbox[0][:])
    x = Vector(bbox[4][:])
    y = Vector(bbox[3][:])
    z = Vector(bbox[1][:])

    root_to_x = x - root
    root_to_y = y - root
    root_to_z = z - root

    x_plane_normal = Vector((1,0,0))
    y_plane_normal = Vector((0,1,0))
    z_plane_normal = Vector((0,0,1))
   
    x_step_size = root_to_x / x_steps if x_steps > 0 else 0
    y_step_size = root_to_y / y_steps if y_steps > 0 else 0
    z_step_size = root_to_z / z_steps if z_steps > 0 else 0

    planes = []
    normals = []
    for x in range(x_steps):
        if root_to_x.length == 0:
            break
        planes.append( root + (x_step_size * x) )
        normals.append(x_plane_normal)
    for y in range(y_steps):
        if root_to_y.length == 0:
            break
        planes.append( root + (y_step_size * y) )
        normals.append(y_plane_normal)
    for z in range(z_steps):
        if root_to_z.length == 0:
            break
        planes.append( root + (z_step_size * z) )
        normals.append(z_plane_normal)

    if object_mode == 'OBJECT':
        bm = bmesh.new()
        bm.from_mesh(mesh)
    elif object_mode == 'EDIT':
        bm = bmesh.from_edit_mesh(mesh)

    for plane, normal in zip(planes, normals):
        geom = bm.edges[:] + bm.faces[:]
        # result = bmesh.ops.bisect_plane(bm, dist=0.01, geom=geom, plane_co=(0, 0, 0), plane_no=(0, 1, 0))
        result = bmesh.ops.bisect_plane(bm, dist=0.01, geom=geom, plane_co=plane, plane_no=normal)

    if object_mode == 'OBJECT':
        bm.to_mesh(mesh)
    elif object_mode == 'EDIT':
        bmesh.update_edit_mesh(mesh, tessface=True)
    bm.free()


class OBJECT_OT_grid_bisect_mesh(bpy.types.Operator):
    bl_idname = 'object.grid_bisect_mesh'
    bl_label = 'Grid Bisect Mesh'
    bl_description = 'Grid Bisect Mesh'
    bl_options = {"REGISTER", "UNDO"}

    divisions = IntVectorProperty(name='Divisions', min=1, options={'SKIP_SAVE'}, default=(1,1,1))

    @classmethod
    def poll(self, context):
        return bpy.context.active_object is not None

    def execute(self, context):
        targets = [t for t in context.selected_objects if t.type == 'MESH']
        for target in targets:
            grid_bisect_mesh(target.mode, target.data, target.bound_box, *self.divisions[:])
        return {'FINISHED'}
