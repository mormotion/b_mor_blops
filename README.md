# Various operators for Blender 2.80

Lot of old operators that needed to filtered, sorted, and prepped for release to the community.



File
===
### op_file_save_incremental
> FILE_OT_save_incremental / wm.save_incremental  
> Save blend file with incremented trailing digit

Material
===
### op_material_set_objects_materials_interp_mode
> OBJECT_OT_set_objects_material_images_interp / object.set_objects_materials_image_interp  
> Set the interpolation of all images found on the selected objects' materials' image nodes

Mesh
===
### op_mesh_additional_selections
> MESH_OT_select_faces_by_normal / mesh.select_faces_by_normal  
> Select faces based on angle between a normal and each face normal. 
> Limited by a threshold  
> Cutoff doesn't do shit yet

> MESH_OT_select_faces_by_normal / mesh.select_faces_by_location_range  
> Select faces based on a bounding box

### op_mesh_grid_split

### op_mesh_grid_bisect
> OBJECT_OT_grid_bisect_mesh / object.grid_bisect_mesh  
> Grid bisect mesh in local space based on IntVectorProperty  

### op_mesh_to_obj_name 

Object
===

### op_object_drop_to_floor_rbd
### op_object_enumerate_ids
### op_object_explode_selected
### op_object_floor_objects
### op_object_grep_select
### op_object_line_arrange
### op_object_rename_active
### op_object_replace_with_dupligroup
