import bpy
import os
from bpy.types import Operator, Panel
from bpy.props import StringProperty, BoolProperty

# Operator to export selected collections along with an armature
class EBT_OT_BatchExportFBX_WithArmature(Operator):
    bl_idname = "collection.batch_export_fbx_with_armature"
    bl_label = "Batch Export FBX (with Armature)"
    bl_description = "Export selected collections with the Armature named 'Armature'"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.FBXExportFolder != ""

    def execute(self, context):
        scene = context.scene
        export_path = os.path.realpath(bpy.path.abspath(scene.FBXExportFolder))

        root_armature = None

        # Check scene collection first
        for obj in scene.collection.objects:
            if obj.type == 'ARMATURE' and obj.name == "Armature":
                root_armature = obj
                break

        # If not found, check Skeletons collection
        skeletons = bpy.data.collections.get("Skeletons")
        if skeletons:
            for obj in skeletons.all_objects:
                if obj.type == 'ARMATURE' and obj.name == "Armature":
                    root_armature = obj
                    break

        if not root_armature:
            self.report({'ERROR'}, "No armature named 'Armature' found in Scene or 'Skeletons' collection.")
            return {'CANCELLED'}

        for coll in context.selected_ids:
            if not isinstance(coll, bpy.types.Collection):
                continue

            bpy.ops.object.select_all(action='DESELECT')

            for ob in coll.all_objects:
                if context.scene.onlyVisible and (not ob.visible_get()):
                    continue
                ob.select_set(True)

            root_armature.select_set(True)

            bpy.ops.export_scene.fbx(
                filepath=os.path.join(export_path, f"{coll.name}.fbx"),
                use_selection=True,
                use_custom_props=True,
                add_leaf_bones=False,
                bake_anim=False
                #use_mesh_modifiers=True,
            )

            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


def core_collection_batch_fbx_armature_export(self, context):
    if any(isinstance(id, bpy.types.Collection) for id in context.selected_ids):
        self.layout.operator(EBT_OT_BatchExportFBX_WithArmature.bl_idname, icon='ARMATURE_DATA', text="Batch Export FBX (with Armature)", text_ctxt="Export selected collections with the root armature")


classes = (
    EBT_OT_BatchExportFBX_WithArmature,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.FBXExportFolder = StringProperty(
        name="Export Folder",
        subtype='DIR_PATH',
        description="Folder where all FBX files are exported"
    )

    bpy.types.Scene.onlyVisible = BoolProperty(
        name="Only Visible",
        description="Export only visible objects in visible collections"
    )

    bpy.types.OUTLINER_MT_collection.prepend(core_collection_batch_fbx_armature_export)


def unregister():
    bpy.types.OUTLINER_MT_collection.remove(core_collection_batch_fbx_armature_export)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.FBXExportFolder
    del bpy.types.Scene.onlyVisible

