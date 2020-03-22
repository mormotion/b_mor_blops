import bpy
from bpy.props import FloatVectorProperty


class WORLD_OT_default_world_node_tree(bpy.types.Operator):
    bl_idname = 'world.default_world_node_tree'
    bl_label = 'Default World Node Tree'
    bl_description = 'Default Active Scenes World Node Tree'
    bl_options = {'REGISTER', 'UNDO'}

    background_color = FloatVectorProperty(name='Background Color', subtype='COLOR',
                                           size=4, default=(0.9, 0.9, 0.9, 1))

    @classmethod
    def poll(cls, context):
        return context.scene.world.use_nodes

    def execute(self, context):
        node_tree = context.scene.world.node_tree
        node_tree.nodes.clear()
        # Create Nodes
        output_node = node_tree.nodes.new(type='ShaderNodeOutputWorld')
        background_node = node_tree.nodes.new(type='ShaderNodeBackground')
        # Set Locations
        output_node.location = (730, 35)
        background_node.location = (318, 35)
        # Link
        node_tree.links.new(output_node.inputs['Surface'],
                            background_node.outputs['Background'])
        # Set Background Color
        background_node.inputs['Color'].default_value = self.background_color

        return {'FINISHED'}

classes = [
    WORLD_OT_default_world_node_tree,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)