# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Delete Disabled Tracks",
    "author" : "Kuldeep Singh",
    "description" : "This tool deletes all disabled tracks in the current frame range.",
    "blender": (3, 6, 0),
    "version" : (0, 0, 1),
    "category": "Tracking",
}

import bpy

class DeleteDisabledTracksOperator(bpy.types.Operator):
    bl_idname = "tracking.delete_disabled_tracks"
    bl_label = "Delete Disabled Tracks"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'CLIP_EDITOR'

    def execute(self, context):
        clip = context.space_data.clip
        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end
        
        for tracking_object in clip.tracking.objects:
            for track in tracking_object.tracks:
                sframe = track.markers[0].frame
                eframe = track.markers[-1].frame
                if sframe <= start_frame and eframe >= end_frame:
                    track.hide = True

        bpy.ops.clip.select_all(action='SELECT')
        bpy.ops.clip.delete_track()
        bpy.ops.clip.hide_tracks_clear()            
        
        return {'FINISHED'}

class DeleteDisabledTracksPanel(bpy.types.Panel):
    bl_label = "Delete Disabled Tracks"
    bl_idname = "PT_DeleteDisabledTracksPanel"
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("tracking.delete_disabled_tracks")

def register():
    bpy.utils.register_class(DeleteDisabledTracksOperator)
    bpy.utils.register_class(DeleteDisabledTracksPanel)

def unregister():
    bpy.utils.unregister_class(DeleteDisabledTracksOperator)
    bpy.utils.unregister_class(DeleteDisabledTracksPanel)

if __name__ == "__main__":
    register()
