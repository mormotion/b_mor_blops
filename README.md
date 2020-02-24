# Various operators for Blender 2.80


## Additional Context Menu Operators
* Change type of selected lights through context menu  
* Selected Track New Empty: Create a new empty at cursor position. Add a track to contraint to each selected object and target the new empty
* Selected Track To Active: Add a track to constraint to each selected object targetted to active object. Will attempt to use existing track to constaint before creating a new one.
* Selected Target Active: Point selected objects at active, (-Z, Y+)


## Object Operators



`data_block_management.py`  
object.object_name_to_data_block  
Rename Data to Match Object  