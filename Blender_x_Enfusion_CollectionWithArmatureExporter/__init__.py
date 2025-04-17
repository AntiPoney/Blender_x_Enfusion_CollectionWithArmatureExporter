bl_info = {
    "name": "Enfusion Tools - [Addon] Collection With Armature Exporter",
    "author": "'AntiPoney' Jérôme Noël",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "Outliner > selected object(s) > right clic menu",
    "description": "Export the selected collection(s) into the batch fbx export folder along with the armature named 'Armature' that should be children of scene collection .",
    "category": "Import-Export",
    "doc_url": "https://github.com/AntiPoney/Blender_x_Enfusion_CollectionWithArmatureExporter",
    "tracker_url": "https://github.com/AntiPoney/Blender_x_Enfusion_CollectionWithArmatureExporter/issues",
}

import bpy
import os

# Register and Unregister
def register():
    
    from . import CollectionExportWithArmature
    CollectionExportWithArmature.register()

def unregister():
    
    from . import CollectionExportWithArmature
    CollectionExportWithArmature.unregister()

if __name__ == "__main__":
    register()