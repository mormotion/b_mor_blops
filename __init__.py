'''
Copyright (C) 2018 Benjamin Morrison
morrisonmotion@gmail.com

Created by Benjamin Morrison

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "B Mor Operator Workflow Operators Pack",
    "description": "Various workflow operators",
    "author": "Benjamin Morrison",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Object",
    }


import bpy

# load and reload submodules
##################################
# from . import op_file_save_incremental
# from . import op_node_management
from . import object_context_menu_additions
# from . import viewport_draw_image


import importlib
# importlib.reload(op_file_save_incremental)
# importlib.reload(op_node_management)
# importlib.reload(viewport_draw_image)
importlib.reload(object_context_menu_additions)

# register
##################################

# viewport_draw_image.VIEW3D_OT_draw_image_test,
# op_node_management.NODES_OT_nodes_to_json,
# classes = [
# 
# ]


def register():
    # for cls in classes:
    #     bpy.utils.register_class(cls)
    object_context_menu_additions.register()


def unregister():
    # for cls in classes:
    #     bpy.utils.unregister_class(cls)
    object_context_menu_additions.unregister()
