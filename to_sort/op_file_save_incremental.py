import bpy
import re

class FILE_OT_save_incremental(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.save_incremental"
    bl_label = "Increment Save File"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.data.is_saved:
            f = bpy.data.filepath.replace('.blend','')
            m = re.search(r'\d+$', f)
            if m is not None:
                new_number = str(int(m.group()) + 1)
                new_filename = re.sub(r'\d+$',new_number, f) + '.blend'
            else:
                new_filename = f + '_1.blend'     
            
            bpy.ops.wm.save_as_mainfile(filepath=new_filename)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'File has not been saved.')
            return {'CANCELLED'}
        

def register():
    bpy.utils.register_class(FILE_OT_save_incremental)

def unregister():
    bpy.utils.unregister_class(FILE_OT_save_incremental)


if __name__ == "__main__":
    register()
