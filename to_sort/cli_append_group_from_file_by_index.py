import bpy
import os
import sys

"""
Expected usage
blender -b blendfile.blend -P append_group_from_file_by_index index
"""

LINK_LAYER = 5

def main():
    import_source_file = sys.argv[-2]
    import_source_file = os.path.abspath(import_source_file)
    import_group_index = int(sys.argv[-1])
    if not os.path.exists(import_source_file):
        sys.exit('{} could not be found'.format(import_source_file))
    if '.blend' not in import_source_file:
        sys.exit('{} does not contain .blend'.format(import_source_file))

    # append group
    with bpy.data.libraries.load(filepath=import_source_file, link=False) as (data_src, data_dst):
        group_at_index = data_src.groups[import_group_index]
        print('loading group "{}" to layer {} from {}'.format(group_at_index, LINK_LAYER, import_source_file))
        data_dst.groups = [group_at_index]
    
    # Store initial layers
    intial_layers = list(bpy.context.screen.scene.layers)

    # Temp solo layers
    temp_layers = [False] * 20
    temp_layers[LINK_LAYER] = True 
    bpy.context.screen.scene.layers = temp_layers

    # link group objects 
    for o in data_dst.groups[0].objects:
        bpy.context.scene.objects.link(o)
    bpy.context.screen.scene.update() # Probably not needed

    # Restore initial layers
    bpy.context.screen.scene.layers = intial_layers

    # Save
    bpy.ops.wm.save_as_mainfile()




if __name__ == '__main__':
    main()
