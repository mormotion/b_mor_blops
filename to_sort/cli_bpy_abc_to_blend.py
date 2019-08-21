import bpy
import sys

def main():
    # import alembic
    abc_file = sys.argv[-1]
    bpy.ops.wm.alembic_import(filepath="", as_background_job=False)

    # Identify unique mesh datablocks
    unique_meshes = [m.name.split('.')[0] for m in bpy.data.meshes]
    unique_meshes = list(set(unique_meshes))

    # Create new group for each unique mesh
    new_groups = []
    reference_objects = []
    for mesh in unique_meshes:
        group = bpy.data.groups.new(mesh.name)
        new_groups.append(group)
        obj = bpy.data.objects.new(mesh.name + '_source', mesh)
        reference_objects.append(obj)
        group.objects.link(obj)

        # Solo on layer 5
        obj.layers[5] = True
        for index, value in enumerate(obj.layers):
            if index != 5:
                obj.layers[index] = False

    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if obj in reference_objects:
            continue
        for ref_obj in reference_objects:
            if ref_obj.data.name not in obj.data.name:
                continue
            # Create new instance
            ref_group = ref_obj.users_group[0]
            new_instance = bpy.data.objects.new(name=ref_obj.data.name, object_data=None)
            bpy.data.scenes[0].objects.link(new_instance)
            transform = obj.matrix_world
            new_instance.matrix_world = transform
            new_instance.dupli_type = 'GROUP'
            new_instance.dupli_group = ref_group
        bpy.data.objects.remove(obj)





    # bpy.data.objects[0].matrix_world

    
    # Find original instance give it a group and reset PSR
    
    
        
    # empty = bpy.data.objects.new(name='name', object_data=None)
    # bpy.data.scenes[0].objects.link(empty)


if __name__ == '__main__':
    main()