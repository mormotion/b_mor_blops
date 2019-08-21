import bpy
# from bpy.types import BoolProperty, FloatProperty, EnumProperty


"""
THIS IS AN AWFUL HACKY SOLUTION


GET THEM PROP REFERENCES
    def draw(self, context):
        layout = self.layout
        
        mod = context.object.modifiers[0]
        prop_strings = [prop.identifier for prop in mod.bl_rna.properties]
        for prop_string in prop_strings[3:]:
            row = layout.row()
            row.prop(mod, prop_string)

"""
def find_common_modifiers(objects):
    """ Takes list of objects, Return a list of modifiers common to each object in objects """
    reference_object = objects[0]
    common_modifiers = [mod.type for mod in reference_object.modifiers]
    for obj in objects[1:]:
        # Get obj modifiers
        obj_modifier_types = [mod.type for mod in obj.modifiers]
        # Reduce common modifier base don lack of match of local modofier
        common_modifiers = list(filter(lambda mod : mod in obj_modifier_types, common_modifiers))
    return common_modifiers


class OBJECT_OT_copy_common_modifier_settings(bpy.types.Operator):
    bl_idname = 'object.copy_shared_modifier_settings'
    bl_label = 'Copy common modifier settings'
    bl_description = 'Copy common modifier settings'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        target_objects = [o for o in context.selected_objects if o.type == 'MESH']
        reference_object = context.active_object
        for common_modifier_type in find_common_modifiers(target_objects):
            for reference_modifier in reference_object.modifiers:
                if reference_modifier.type != common_modifier_type:
                    continue
                prop_strings = [prop.identifier for prop in reference_modifier.bl_rna.properties]
                for obj in target_objects:
                    if obj == reference_object:
                        continue
                    for target_mod in obj.modifiers:
                        if target_mod.type != reference_modifier.type:
                            continue
                        for prop_string in prop_strings[3:]:
                            value = getattr(reference_modifier, prop_string)
                            setattr(target_mod, prop_string, value)
                        
        return {'FINISHED'}


class OBJECT_PT_edit_shared_modifiers(bpy.types.Panel):
    bl_label = "Common Modifiers"
    bl_idname = "MODIFIER_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.copy_shared_modifier_settings', text='Apply Changes')

        objects = [o for o in context.selected_objects if o.type == 'MESH']
        if len(objects) > 0:
            for modifier_type in find_common_modifiers(objects):
                for modifier in context.active_object.modifiers:
                    if modifier.type == modifier_type:
                        row = layout.row()
                        row.label(text=str(modifier))
                        row = layout.row()

                        prop_strings = [prop.identifier for prop in modifier.bl_rna.properties]
                        string_backlist = ['show_expanded', 'use_apply_on_spline']
                        for i, prop_string in enumerate(prop_strings[3:]):
                            if prop_string in string_backlist:
                                continue
                            if i < 6:
                                split = layout.split()
                                col = split.column(align=True)
                                row.prop(modifier, prop_string)
                            else:
                                row = layout.row()
                                row.prop(modifier, prop_string)
