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
    "name": "BMOR Blender Operators ",
    "description": "Various workflow operators",
    "author": "Benjamin Morrison",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Object",
    }


import bpy

# load and reload submodules
##################################
from . import view3d_context_additions
from . import data_block_management
from . import scene_enumerate_ids
from . import object_add_extras

import importlib
importlib.reload(view3d_context_additions)
importlib.reload(data_block_management)
importlib.reload(scene_enumerate_ids)
importlib.reload(object_add_extras)

# register
##################################

# viewport_draw_image.VIEW3D_OT_draw_image_test,
# op_node_management.NODES_OT_nodes_to_json,
local_modules = [
    view3d_context_additions,
    data_block_management,
    scene_enumerate_ids,
    object_add_extras,
]

def register():
    for mod in local_modules:
        mod.register()

def unregister():
    for mod in local_modules:
        mod.unregister()
