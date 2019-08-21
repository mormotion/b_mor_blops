import bpy
import bmesh

def mesh_to_convex_hull(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    initial_faces = bm.faces[:]
    convex_hull = bmesh.ops.convex_hull(bm, input=bm.verts)
    bmesh.ops.delete(bm, geom=initial_faces, context=5)
    bm.to_mesh(mesh)



class MESH_OT_mesh_to_convex_hull(bpy.types.Operator):
    bl_idname = 'mesh.opname'
    bl_label = 'label'
    bl_description = 'description'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

if __name__ == '__main__':
    mesh = bpy.context.active_object.data
    mesh_to_convex_hull(mesh)
    