import bpy
import bmesh
from bpy.props import EnumProperty, FloatProperty, FloatVectorProperty, BoolProperty
from math import radians
from mathutils import Vector

GEO_ENUM = (('VERTEX', 'Vertex', 'Vertex Selection'),
            ('FACE', 'Face', 'Face Selection'),)

def select_faces_by_bbox(mesh_data, bbox_a, bbox_b):
    """ Select mesh_data faces by a location range"""
    mesh_data = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(mesh_data)

    x_min, x_max = sorted([bbox_a.x, bbox_b.x])
    y_min, y_max = sorted([bbox_a.y, bbox_b.y])
    z_min, z_max = sorted([bbox_a.z, bbox_b.z])

    for face in bm.faces:
        median = face.calc_center_median()
        if median.x < x_min or median.x > x_max:
            continue
        if median.y < y_min or median.y > y_max:
            continue
        if median.z < z_min or median.z > z_max:
            continue
        face.select = True

    bmesh.update_edit_mesh(mesh_data)


def select_geo_by_normal(mesh_data, direction, angle_threshold, use_cutoff, cutoff):
    """ Select mesh_data geo by angle(degress) of face.normal to normal """
    # CUTOFF DOESN"T WORK, baaaaaaah I'm too tired for the math right now
    angle_threshold = radians(angle_threshold)
    direction.normalize()

    bm = bmesh.from_edit_mesh(mesh_data)

    # print('\n')
    # WRONG WRONG WRONG
    # for face in bm.faces:
    #     angle = face.normal.angle(direction)
    #     if angle <= angle_threshold:
    #         if use_cutoff:
    #             median = face.calc_center_median()
    #             v1 = median - cutoff
    #             v2 = (direction + cutoff) - cutoff
    #             # v1.normalize()
    #             # v2.normalize()
    #             print(v1.dot(v2))
    #             if v1.dot(v2) >= 0:
    #                 face.select = True
    #         else:
    #             face.select = True

    for face in bm.faces:
        angle = face.normal.angle(direction)
        if angle <= angle_threshold:
            face.select = True

    bmesh.update_edit_mesh(mesh_data)


def select_by_range(mesh_data, min_loc, max_loc, mesh_component, mode):
    pass

class MESH_OT_select_faces_by_normal(bpy.types.Operator):
    bl_idname = "mesh.select_faces_by_normal"
    bl_label = "Select Mesh Faces By Normal"
    bl_description = "Select Mesh Faces by Normal"
    bl_options = {"REGISTER", "UNDO"}

    normal = FloatVectorProperty(name="Normal", min=-1, max=1, subtype='XYZ', default=(0,0,1))
    threshold = FloatProperty(name='Angle Threshold', default=45)
    clear_existing = BoolProperty(name='Clear Existing', default=False)

    use_cutoff = BoolProperty(name='Use Cutoff', default=False)
    cutoff = FloatVectorProperty(name='Cutoff', subtype='TRANSLATION', default=(0,0,0))
    

    @classmethod
    def poll(self, context):
        if context.active_object.type != 'MESH':
            return False
        if context.active_object.mode != 'EDIT':
            return False
        return True

    def execute(self, context):
        if self.clear_existing:
            bpy.ops.mesh.select_all(action='DESELECT')
        select_geo_by_normal(context.active_object.data, self.normal, self.threshold, self.use_cutoff, self.cutoff)

        return {"FINISHED"}


class MESH_OT_select_faces_by_bbox(bpy.types.Operator):
    bl_idname = "mesh.select_faces_by_location_range"
    bl_label = "Select Mesh Faces By Location Range"
    bl_description = "Select Mesh Faces by Location Range"
    bl_options = {"REGISTER", "UNDO"}

    bbox_a = FloatVectorProperty(name='BBox A', subtype='TRANSLATION', default=(1,1,1))
    bbox_b = FloatVectorProperty(name='BBox B', subtype='TRANSLATION', default=(-1,-1,-1))
    clear_existing = BoolProperty(name='Clear Existing', default=False)

    @classmethod
    def poll(self, context):
        if context.active_object.type != 'MESH':
            return False
        if context.active_object.mode != 'EDIT':
            return False
        return True

    def execute(self, context):
        if self.clear_existing:
            bpy.ops.mesh.select_all(action='DESELECT')
        select_faces_by_bbox(context.active_object.data, self.bbox_a, self.bbox_b)
        return {"FINISHED"}