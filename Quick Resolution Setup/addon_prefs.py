# -*- cofing:utf-8 -*-

import bpy


class AUTORELOAD_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    display_author : bpy.props.BoolProperty(
        name='Display author name?',
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.alignment = "LEFT"
        row.prop(self, "display_author")

# ----------------------------

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)

# ----------------------------

### REGISTER ---
def register_module():
    bpy.utils.register_class(AUTORELOAD_PF_addon_prefs)

def unregister_module():
    bpy.utils.unregister_class(AUTORELOAD_PF_addon_prefs)
