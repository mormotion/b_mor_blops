import bpy
import csv
import shutil
import os
import json

# TODO: Yo, this shit doesn't do anything yet

class recreated_node:
    def __init__(self, original_name, node_properties, node_inputs):
        self.original_name = original_name
        self.node_properties = node_properties
        self.node_inputs = node_inputs
    

def node_to_dict(node):
    """ Convert node to a dictionary in preparation with export """
    # identifier = bpy.data.materials['Material'].node_tree.nodes[0].bl_rna.identifier

    # node_name = node.name
    node_identifier = node.bl_rna.identifier
    print(node_identifier)

    # Get writable node properites
    writable_prop_identifies = (prop.identifier for prop in node.bl_rna.properties if not prop.is_readonly)
    props_dict = {}
    for prop_name in writable_prop_identifies:
        props_dict.update({prop_name: getattr(node, prop_name)})
    print(props_dict)

    # Get node inputs
    inputs_dict = {}
    for node_input in node.inputs:
        identifier = node_input.identifier
        # Check if value is array
        if isinstance(node_input.default_value, (bpy.types.bpy_prop_array)):
            # Might need convert to string
            default_value = [value for value in node_input.default_value]
        else:
            default_value = node_input.default_value
        inputs_dict.update({identifier: default_value})
    print(inputs_dict)

    print('whaaaa')
    props_dict['inputs'] = inputs_dict

        # Get node outputs
        # I don't think these values are ever exposed?
        # outputs_dict = {}
        # for node_output in node.outputs:
        #     identifier = node_output.identifier
        #     # Check if value is array
        #     if hasattr(node_output, 'default_value'):
        #         if isinstance(node_output.default_value, (bpy.types.bpy_prop_array)):
        #             # Might need convert to string
        #             default_value = [value for value in node_output.default_value]
        #         else:
        #             default_value = node_output.default_value
        #         outputs_dict.update({identifier: default_value})

        # print(outputs_dict)
    # get links:
    # node_tree = context.space_data.node_tree
    # node_links = []
    # for link in node_tree.links:
    #     # Skip links to untargetted nodes
    #     if not all(map(lambda linked: linked in target_nodes, (link.to_node, link.from_node))):
    #         continue

    #     node_links.append({'link': (link.from_node.name, link.to_node.name)})
    # with open(output_filepath, 'w') as output_file:


def get_selected_nodes(operator, context):
    space = context.space_data
    node_tree = space.node_tree
    selected_nodes = [node for node in node_tree.nodes.values() if node.select]
    
    if not selected_nodes or len(selected_nodes) < 2:
        operator.report({'ERROR'}, "2 nodes must be selected")

    return selected_nodes


class NODES_OT_nodes_to_json(bpy.types.Operator):
    """ Save selected nodes as json file """
    bl_idname = "node.selected_nodes_to_json"
    bl_label = "Selected nodes to json"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'NODE_EDITOR'

    def execute(self, context):
        nodes = get_selected_nodes(self, context)
        node_to_dict(nodes[0])
        # nodes_to_json(context, nodes, output_filepath='./testo.json')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(NODES_OT_nodes_to_json)


def unregister():
    bpy.utils.unregister_class(NODES_OT_nodes_to_json)


if __name__ == "__main__":
    register()
    # test call
