import bpy
import os
import sys


""" 
Split multipass image into individual files 
Like most cli scripts, this should be run with --factory-startup
DOES NOT SUPPORT SUPPORT SEQUENCES YET
"""

VALID_IMAGE_FORMATS = ('BMP', 'IRIS', 'PNG', 'JPEG', 'JPEG2000', 'TARGA', 
                       'TARGA_RAW', 'CINEON', 'DPX', 'OPEN_EXR_MULTILAYER',
                       'OPEN_EXR', 'HDR', 'TIFF')

def main():
    input_image_path = sys.argv[-3]
    output_format = sys.argv[-2] 
    output_path = sys.argv[-1]

    input_image_path = os.path.abspath(input_image_path)
    input_basename = os.path.basename(input_image_path)
    output_prefix, input_extension = os.path.splitext(input_basename)
    input_extension = input_extension[1:].upper()
    output_prefix += '_'
    output_format = output_format.upper()
    output_path = os.path.abspath(output_path)

    # Check valid args
    if not os.path.exists(input_image_path):
        print('Could not find input file: {}'.format(input_image_path))

    # File Settings
    scene = bpy.data.scenes[0]
    scene.view_settings.view_transform = 'Raw'
    scene.view_settings.look = 'None'
    
    scene.use_nodes = True
    
    # comp_tree = bpy.data.scenes[0].node_tree
    comp_tree = bpy.context.scenes.node_tree
    comp_tree.nodes.clear()
    input_image = bpy.data.images.load(input_image_path)

    # Node Creation    
    file_input_node = comp_tree.nodes.new(type='CompositorNodeImage')
    file_input_node.location = (0, 0)
    file_input_node.image = input_image
    file_output_node = comp_tree.nodes.new(type='CompositorNodeOutputFile')
    file_output_node.location = (300, 0)
    file_output_node.layer_slots.clear()
    file_output_node.format.file_format = output_format
    file_output_node.base_path = output_path
    
    # Linking
    for image_pass in file_input_node.outputs:
        pass_name = image_pass.name
        output_socket = file_output_node.layer_slots.new(output_prefix + pass_name + '_')
        
        comp_tree.links.new(output_socket, image_pass)


if __name__ == '__main__':
    main()