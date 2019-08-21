import bpy

def get_enum_group_names(cls, context):
    groups = []
    for o in context.scene.objects:
        for grp in o.users_group:
            if grp not in groups:
                groups.append(grp)
    return [(group.name, group.name, group.name) for group in groups]

