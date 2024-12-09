'''
Copyright (C) 2018 苏冥 (Hades Su)

Created by 苏冥(Hades Su)

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
    "name": "Quick Resolution Setup",
    "author": "苏冥(Hades Su)",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "category": "Render",
    "doc_url": "https://github.com/Hades-Su/blender_quick_resolution_setup",
    "tracker_url": "https://github.com/Hades-Su/blender_quick_resolution_setup/issues",
    "description": "Adjust camera resolution quickly, automatically and easily.",
    "location": "Properties > Render > Format",
}

import bpy
import math
from . import addon_prefs, translation

# =========================================================

# -- 初始化下拉框内容 [["Group Name", [((1920, 1080), ("1920x1080", "1920x1080", "...")), ...], ...]
# -- Initialize the drop-down box content

# 下拉框"分辨率格式"选项列表内容
# Contents of the drop-down box "Resolution format" option list
qcr_resolution_items = [
    ["Common Format", [
        (None, ("default", "Select Format", "")),
        None,
        ((640, 360), ("640x360", "H: 640 x 360 (360P)", "360p is a common format for low-resolution video, often used for web videos and mobile devices.")), 
        ((720, 480), ("720x480", "H: 720 x 480 (480P)", "480p is a common resolution for standard definition video.")), 
        ((1280, 720), ("1280x720", "H: 1280 x 720 (720P)", "720p, also known as 720i, is the standard resolution for high definition, suitable for small displays such as mobile phones and tablets.")), 
        ((1920, 1080), ("1920x1080", "H: 1920 x 1080 (1080P)", "1080p, also known as 1080i, is the standard resolution of Full HD and is the most widely used, suitable for most computer monitors and TVs.")), 
        ((2560, 1440), ("2560x1440", "H: 2560 x 1440 (1440P/‌2K)", "1440p, also known as 2k, is a resolution between 1080p and 4K, suitable for professional users to perform fine processing of graphics and video content, while also providing an excellent gaming experience‌.")), 
        ((3840, 2160), ("3840x2160", "H: 3840 x 2160 (2160P/‌4K)", "2160p, also known as 4k, is the standard resolution for ultra-high definition and is widely used in fields such as professional graphic design, video editing, and high-definition movies.")), 
        ((5120, 2880), ("5120x2880", "H: 5120 x 2880 (5K)", "5K is suitable for fields such as professional graphic design, video editing and photography, providing higher image quality and detail performance than 4K.")), 
        ((7680, 4320), ("7680x4320", "H: 7680 x 4320 (8K)", "8K is the current highest resolution display standard, suitable for experimental purposes and high-end applications, providing extremely high image quality‌.")), 
        None,
        ((360, 640), ("360x640", "V: 360 x 640", "")), 
        ((480, 720), ("480x720", "V: 480 x 720", "")), 
        ((720, 1280), ("720x1280", "V: 720 x 1280", "")), 
        ((1080, 1448), ("1080x1448", "V: 1080 x 1448", "")), 
        ((1080, 1920), ("1080x1920", "V: 1080 x 1920", "")),
        None,
        ((100, 100), ("100x100", "S: 100 x 100", "")), 
        ((512, 512), ("512x512", "S: 512 x 512", "It is commonly used in areas such as video generation and editing, super-resolution video enhancement, etc. in generative video tools.")), 
        ((1024, 1024), ("1024x1024", "S: 1024 x 1024", "Commonly used in areas such as generative video tools, ultra-high-definition video applications, infrared thermal imagers, convolutional neural network applications, and full-body image generation.")), 
    ]], 
    ["Uncommon Format", [
        ((1998, 1080), ("1998x1080", "H: 1998 x 1080", "")), 
        ((2534, 1080), ("2534x1080", "H: 2534 x 1080", "")), 
        ((1920, 960), ("1920x960", "H: 1920 x 960", "For editing monoscopic equirectangular VR files in 1920h x 960v 2:1 video format.")), 
        ((3840, 1920), ("3840x1920", "H: 3840 x 1920", "For editing monoscopic equirectangular VR files in 3840h x 1920v 2:1 video format.")), 
        ((4096, 2048), ("4096x2048", "H: 4096 x 2048", "For editing monoscopic equirectangular VR files in 4096h x 2048v 2:1 video format.")), 
        ((4096, 2304), ("4096x2304", "H: 4096 x 2304", "For editing stereographic VR files in 4096h x 2304v 16:9 video format.")), 
        ((8192, 4096), ("8192x4096", "H: 8192 x 4096", "For editing monoscopic equirectangular VR files in 8192h x 4096v 2:1 video format.")), 
        None,
        ((640, 853), ("640x853", "V: 640x853", "")), 
        ((1080, 1448), ("1080x1448", "V: 1080 x 1448", "")), 
        ((1080, 2338), ("1080x2338", "V: 1080 x 2338", "")), 
        None,
        ((2048, 2048), ("2048x2048", "S: 2048 x 2048", "For editing stereographic VR files in 2048h x 2048v 1:1 video format.")), 
        ((2880, 2880), ("2880x2880", "S: 2880 x 2880", "For editing stereographic VR files in 2880h x 2880v 1:1 video format.")), 
        ((4096, 4096), ("4096x4096", "S: 4096 x 4096", "For editing stereographic VR files in 4096h x 4096v 1:1 video format.")), 
        ((6144, 6144), ("6144x6144", "S: 6144 x 6144", "For editing stereographic VR files in 6144h x 6144v 1:1 video format.")), 
        ((8192, 8192), ("8192x8192", "S: 8192 x 8192", "For editing stereographic VR files in 8192h x 8192v 1:1 video format.")), 
    ]], 
]
# 下拉框"分辨率比例"选项列表内容
# Contents of the drop-down box "Resolution ratio" option list
qcr_proportion_items = [
    ["Common Proportion", [
        (None, ("default", "Custom", "")),
        None,
        ((1, 1), ("1x1", "1 : 1", "Square ratio, suitable for icons, logos, social media avatars, etc. Common resolution formats: 100x100, 512x512, 1024x1024.")),
        None,
        ((2, 3), ("2x3", "2 : 3", "Portrait ratio, suitable for mobile phone photography, social media vertical video and other scenes. Common resolution formats: 640x960, 1080x1620, 1280x1920.")),
        ((3, 4), ("3x4", "3 : 4", "Portrait ratio, suitable for mobile phone photography, social media vertical video and other scenes. Common resolution formats: 640x853, 1080x1448, 1280x1707.")),
        ((9, 16), ("9x16", "9 : 16", "Vertical screen ratio, suitable for scenes such as mobile phone videos and social media vertical screen videos. Common resolution formats: 1080x1920, 1280x2272, 1440x2560.")),
        None,
        ((4, 3), ("4x3", "4 : 3", "Horizontal screen ratio, suitable for computer monitors, TV programs, slides, etc. Common resolution formats: 1024x768, 1280x960, 1600x1200.")),
        ((16, 9), ("16x9", "16 : 9", "Horizontal screen ratio, suitable for movies, TV shows, computer monitors, smart phones, etc. Common resolution formats: 1280x720, 1920x1080, 2560x1440.")),
        ((21, 9), ("21x9", "21 : 9", "Ultra-wide screen ratio, suitable for movies, games, professional displays, etc. Common resolution formats: 2560x1080, 3440x1440, 3840x1600.")),
    ]], 
    ["Uncommon Proportion", [
        ((1, 2), ("1x2", "1 : 2", "Long strip ratio, suitable for banner ads, web design and other scenarios. Common resolution formats: 100x200, 200x400, 500x1000.")),
        ((1, 3), ("1x3", "1 : 3", "Long strip ratio, suitable for banner ads, web design and other scenarios. Common resolution formats: 100x300, 200x600, 500x1500.")),
        ((9, 14), ("9x14", "9 : 14", "Vertical screen ratio, suitable for scenes such as mobile phone videos and social media vertical screen videos. Common resolution formats: 1080x1680, 1280x1920, 1440x2240.")),
        ((9, 21), ("9x21", "9 : 21", "Ultra-wide screen ratio, suitable for movies, games, professional displays, etc. Common resolution formats: 1920x4320, 2560x5760, 3840x8640.")),
        None,
        ((2, 1), ("2x1", "2 : 1", "Long strip ratio, suitable for banner ads, web design and other scenarios. Common resolution formats: 200x100, 400x200, 1000x500.")),
        ((3, 1), ("3x1", "3 : 1", "Long strip ratio, suitable for banner ads, web design and other scenarios. Common resolution formats: 300x100, 600x200, 1500x500.")),
        ((3, 2), ("3x2", "3 : 2", "Vertical screen ratio, suitable for mobile phone photography, social media vertical screen video and other scenes. Common resolution formats: 640x960, 1080x1440, 1280x1920.")),
        ((5, 4), ("5x4", "5 : 4", "Horizontal screen ratio, suitable for computer monitors, TV programs, slides, etc. Common resolution formats: 800x640, 1280x1024, 1600x1280.")),
        ((14, 9), ("14x9", "14 : 9", "Ultra-wide screen ratio, suitable for movies, games, professional displays, etc. Common resolution formats: 1920x1080, 2560x1440, 3840x2160.")),
        ((16, 10), ("16x10", "16 : 10", "Ultra-wide screen ratio, suitable for movies, games, professional displays, etc. Common resolution formats: 1280x800, 1600x1000, 2560x1600.")),
        None,
        ((1.850000023841858, 1), ("1.85x1", "1.85 : 1", "")),
        ((2.333333333333333, 1), ("4.5k", "4.5k (2.33 : 1)", "2.3333~x1")), 
        ((2.3462962962962962962962962962963, 1), ("2.35x1", "2.35 : 1", "")),
        ((2.390000104904175, 1), ("2.39x1", "2.39 : 1", "")),
        ((1, 2.1648148148148148148148148148148), ("1x2.16", "5.8''", "")),
    ]], 
]

# -- 转换结构
# -- Conversion structure
# 转成符合EnumProperty的结构 [("", "Group Name", ""), ("1920x1080", "1920x1080", "..."), None, ...]
# Convert to a structure that conforms to EnumProperty

# 分辨率格式选项列表
# List of resolution format options
qcr_resolution_setup_items = []
for group_items in qcr_resolution_items:
    group = group_items[0]
    if group:
        qcr_resolution_setup_items.append(("", group, ""))
    for item in group_items[1]:
        if item:
            qcr_resolution_setup_items.append(item[1])
        else:
            qcr_resolution_setup_items.append(None)

# 分辨率比例选项列表
# List of resolution scale options
qcr_proportion_select_items = []
for group_items in qcr_proportion_items:
    group = group_items[0]
    if group:
        qcr_proportion_select_items.append(("", group, ""))
    for item in group_items[1]:
        if item:
            qcr_proportion_select_items.append(item[1])
        else:
            qcr_proportion_select_items.append(None)

# -- 转换结构
# -- Conversion structure
# 将所有非None选项的值都筛选出来 {"1920x1080": (1920, 1080), ...}
# Filter out all non-None option values
qcr_resolution_options = {item[1][0]: item[0] for group_items in qcr_resolution_items for item in group_items[1] if item}
qcr_proportion_options = {item[1][0]: item[0] for group_items in qcr_proportion_items for item in group_items[1] if item}

# 初始化历史分辨率及比例记录
# Initialize historical resolution and scale records
qcr_pre_px = 1920
qcr_pre_py = 1080
qcr_aspect_ratio = qcr_pre_px / qcr_pre_py

# =========================================================

# -- 实时监听事件 --
# -- Real-time monitoring events --

# 实时按分辨率更新下拉框选项
# Update drop-down box options in real time according to resolution
def qcr_update_select(self, context):
    render_settings = bpy.context.scene.render
    qcr_px = render_settings.resolution_x
    qcr_py = render_settings.resolution_y
    # print("update", qcr_px, qcr_py)

    if qcr_px != qcr_pre_px or qcr_py != qcr_pre_py:
        qcr_pxpy = f"{qcr_px}x{qcr_py}"
        if qcr_pxpy in qcr_resolution_options.keys():
            context.scene.qcr_resolution_setup = qcr_pxpy
        else:
            context.scene.qcr_resolution_setup = "default"

# -- 控件触发后的实时监听事件 --
# -- Real-time monitoring events after the control is triggered --

# 按比例更新分辨率
# Update resolution proportionally
def qcr_update_resolution(self, context):
    if context.scene.qcr_lock_proportion:
        global qcr_pre_px, qcr_pre_py, qcr_aspect_ratio

        render_settings = bpy.context.scene.render
        qcr_px = render_settings.resolution_x
        qcr_py = render_settings.resolution_y

        if qcr_px != qcr_pre_px or qcr_py != qcr_pre_py:
            if qcr_px == qcr_pre_px and qcr_py != qcr_pre_py:
                # 用新的分辨率Y和原来的比例计算出新的分辨率X
                # Calculate the new resolution X using the new resolution Y and the original ratio
                qcr_new_px = int(math.ceil(qcr_py * qcr_aspect_ratio))
                render_settings.resolution_x = qcr_new_px
                qcr_pre_px = qcr_new_px
                qcr_pre_py = qcr_py
            elif qcr_px != qcr_pre_px and qcr_py == qcr_pre_py:
                # 用新的分辨率X和原来的比例计算出新的分辨率Y
                # Calculate the new resolution Y using the new resolution X and the original ratio
                qcr_new_py = int(math.ceil(qcr_px / qcr_aspect_ratio))
                render_settings.resolution_y = qcr_new_py
                qcr_pre_px = qcr_px
                qcr_pre_py = qcr_new_py
            elif qcr_px != qcr_pre_px and qcr_py != qcr_pre_py:
                # 用新的分辨率X和原来的比例计算出新的分辨率Y
                # Calculate the new resolution Y using the new resolution X and the original ratio
                qcr_new_py = int(math.ceil(qcr_px / qcr_aspect_ratio))
                render_settings.resolution_y = qcr_new_py
                qcr_pre_px = qcr_px
                qcr_pre_py = qcr_new_py
            else:
                pass

# -- 控件触发事件 --
# -- Control triggers events --

# 选择分辨率比例（16x9）
# Select resolution ratio (16x9)
# “分辨率比例下拉框”选择时触发事件
# Trigger event when selecting "resolution ratio drop-down box"
def qcr_update_proportion_select(self, context):
    global qcr_aspect_ratio

    qcr_proportion_selected = bpy.context.scene.qcr_proportion_select
    # print(qcr_proportion_selected)

    if qcr_proportion_selected in qcr_proportion_options.keys():
        proportion_option_selected = qcr_proportion_options[qcr_proportion_selected]
        qcr_aspect_ratio = float(proportion_option_selected[0] / proportion_option_selected[1])
    else:
        pass

# 选择分辨率格式（1080p = 1920x1080）
# Select the resolution format (1080p = 1920x1080)
# “分辨率格式下拉框”选择时触发事件
# Trigger event when selecting "resolution format drop-down box"
def qcr_update_resolution_setup(self, context):
    qcr_format_selected = bpy.context.scene.qcr_resolution_setup
    # print(qcr_format_selected)

    if qcr_format_selected in qcr_resolution_options.keys():
        global qcr_pre_px, qcr_pre_py
        qcr_px, qcr_py = qcr_resolution_options[qcr_format_selected]

        bpy.context.scene.render.resolution_x = qcr_px
        bpy.context.scene.render.resolution_y = qcr_py
        qcr_pre_px = qcr_px
        qcr_pre_py = qcr_py
    else:
        pass

# 复选框勾选事件
# Checkbox check event
def qcr_check_lock_proportion(self, context):
    qcr_px = bpy.context.scene.render.resolution_x
    qcr_py = bpy.context.scene.render.resolution_y

    if context.scene.qcr_lock_proportion:
        # 将当前分辨率和分辨率比例保存(初始化)为历史记录
        # Save (initialize) the current resolution and resolution ratio as history
        qcr_pre_px = qcr_px
        qcr_pre_py = qcr_py
        qcr_aspect_ratio = qcr_px / qcr_py

        # 根据"当前分辨率比例"更新比例下拉框选项
        # Update the scale drop-down box options according to the "current resolution scale"
        qcr_pxpy_gcd = math.gcd(qcr_px, qcr_py)
        qcr_axay = f"{int(qcr_px / qcr_pxpy_gcd)}x{int(qcr_py / qcr_pxpy_gcd)}"  # e.g.16x9
        if qcr_axay in qcr_proportion_options:
            context.scene.qcr_proportion_select = qcr_axay
        else:
            context.scene.qcr_proportion_select = "default"

        # 注册监听事件
        # Registering Listener Events
        bpy.app.handlers.depsgraph_update_post.append(qcr_update_resolution)
    else:
        # 注销监听事件
        # Unregistering Listening Events
        if qcr_update_resolution in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(qcr_update_resolution)

        # 设置分辨率格式下拉框选项的值
        # Set the value of the resolution format drop-down box option
        qcr_pxpy = f"{qcr_px}x{qcr_py}"  # e.g.640x360
        if qcr_pxpy in qcr_resolution_options.keys():
            context.scene.qcr_resolution_setup = qcr_pxpy

# =========================================================

# 创建按钮事件处理函数
# Create a button event handler
class QCR_ButtonOperator(bpy.types.Operator):
    bl_idname = "qcr.render_format_setup"
    bl_label = "Render Format Setup"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    mode: bpy.props.IntProperty()

    def execute(self, context):
        global qcr_pre_px, qcr_pre_py, qcr_aspect_ratio

        qcr_px = bpy.context.scene.render.resolution_x
        qcr_py = bpy.context.scene.render.resolution_y

        if self.mode == 1:  # 调换 (Swap)
            bpy.context.scene.render.resolution_x = qcr_py
            bpy.context.scene.render.resolution_y = qcr_px
            qcr_pre_px = qcr_py
            qcr_pre_py = qcr_px

            # 判断是否处于锁定比例状态下
            # Determine whether it is in the locked ratio state
            if context.scene.qcr_lock_proportion:
                # -- 如果处于锁定比例的状态下，调换之后也要重新计算比例
                # -- If the ratio is locked, the ratio must be recalculated after the swap
                qcr_aspect_ratio = qcr_pre_px / qcr_pre_py
                # -- 如果处于锁定比例的状态下，调换之后也要重新更新下拉框选项
                # -- If the ratio is locked, the drop-down box options must be updated after the switch.
                # 获取当前分辨率的(最大)公约数 1920x1080的公约数是120，也就是1920/120=16、1080/120=9，所以最小比例是16x9
                # Get the (maximum) common divisor of the current resolution. The common divisor of 1920x1080 is 120, that is, 1920/120=16, 1080/120=9, so the minimum ratio is 16x9
                qcr_pxpy_gcd = math.gcd(qcr_pre_px, qcr_pre_py)
                qcr_axay = f"{int(qcr_pre_px / qcr_pxpy_gcd)}x{int(qcr_pre_py / qcr_pxpy_gcd)}"  # e.g.9x16
                if qcr_axay in qcr_proportion_options.keys():
                    context.scene.qcr_proportion_select = qcr_axay
            else:
                qcr_pxpy = f"{qcr_pre_px}x{qcr_pre_py}"  # e.g.640x360
                if qcr_pxpy in qcr_resolution_options.keys():
                    context.scene.qcr_resolution_setup = qcr_pxpy
        elif self.mode == 2:  # 缩小 (Zoom out)
            bpy.context.scene.render.resolution_x = math.ceil(qcr_px / 2)
            bpy.context.scene.render.resolution_y = math.ceil(qcr_py / 2)
            qcr_pre_px = math.ceil(qcr_px / 2)
            qcr_pre_py = math.ceil(qcr_py / 2)

            if not context.scene.qcr_lock_proportion:
                qcr_pxpy = f"{qcr_pre_px}x{qcr_pre_py}"  # e.g.640x360
                if qcr_pxpy in qcr_resolution_options.keys():
                    context.scene.qcr_resolution_setup = qcr_pxpy
        elif self.mode == 3:  # 放大 (Zoom in)
            bpy.context.scene.render.resolution_x = math.ceil(qcr_px * 2)
            bpy.context.scene.render.resolution_y = math.ceil(qcr_py * 2)
            qcr_pre_px = math.ceil(qcr_px * 2)
            qcr_pre_py = math.ceil(qcr_py * 2)

            if not context.scene.qcr_lock_proportion:
                qcr_pxpy = f"{qcr_pre_px}x{qcr_pre_py}"  # e.g.640x360
                if qcr_pxpy in qcr_resolution_options.keys():
                    context.scene.qcr_resolution_setup = qcr_pxpy
        else:
            pass

        return {"FINISHED"}

# =========================================================

class QCR_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_quick_camera_resolution'
    bl_label = 'Resolution Adjustment'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    # bl_category = 'QCR'
    bl_context = 'output'
    bl_order = 0
    bl_parent_id = 'RENDER_PT_format'
    bl_ui_units_x=0

    def draw(self, context):
        layout = self.layout

        # 启用属性分割，将属性标签和值分开显示
        # Enable attribute splitting to display attribute labels and values ​​separately
        layout.use_property_split = True
        # 禁用属性的装饰，即不显示动画关键帧图标
        # Disable the decoration of the property, that is, do not display the animation keyframe icon
        layout.use_property_decorate = False  # No animation.

        # 复选框（锁定比例）
        # Checkbox (Lock Proportions)
        # 勾选后，当更改分辨率其中一项时，自动按比例同步计算并更新另一项的值
        # After checking, when one of the resolutions is changed, the value of the other item will be automatically calculated and updated proportionally.
        layout_col = layout.column(heading="Resolution Ratio")
        layout_col.prop(context.scene, "qcr_lock_proportion", text="Locked" if context.scene.qcr_lock_proportion else "Lock")

        # 下拉框（设置分辨率）
        # Drop-down box (set resolution)
        if context.scene.qcr_lock_proportion:
            # 分辨率比例选择
            # Resolution Proportion selection
            layout.prop(context.scene, "qcr_proportion_select", text="Select Proportion", expand=False)
        else:
            # 分辨率格式设置
            # Resolution Resolution settings
            layout.prop(context.scene, "qcr_resolution_setup", text="Setup Resolution", expand=False)

        # Button (convenience button)
        layout_row = layout.row(heading='', align=False)
        # 缩小（Zoom Out）
        layout_row.operator('qcr.render_format_setup', text='Scale / 2', icon="ZOOM_OUT", emboss=True, depress=False).mode = 2
        # 调转（Swap）
        layout_row.operator('qcr.render_format_setup', text='Swap X/Y', icon="FILE_REFRESH", emboss=True, depress=False).mode = 1  # or icon_value=692
        # 放大（Zoom In）
        layout_row.operator('qcr.render_format_setup', text='Scale * 2', icon="ZOOM_IN", emboss=True, depress=False).mode = 3

        # -- 基于插件面板设置来更改 Panel名称
        # -- Change the Panel name based on the plugin panel settings

        # 获取插件偏好设置
        # Get addon preferences
        prefs = addon_prefs.get_addon_preferences()
        # 判断是否显示作者名称
        # Determine whether to display the author's name
        if prefs.display_author:
            self.bl_label = 'Resolution Adjustment (by Hades Su)'
        else:
            self.bl_label = 'Resolution Adjustment'

# =========================================================

classes = (
    QCR_Panel, 
    QCR_ButtonOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # 注册属性
    # Registration Properties
    bpy.types.Scene.qcr_resolution_setup = bpy.props.EnumProperty(
        name="Setup Resolution",
        description="", 
        items=qcr_resolution_setup_items,
        default="default",
        update=qcr_update_resolution_setup,
    )
    bpy.types.Scene.qcr_proportion_select = bpy.props.EnumProperty(
        name="Select Proportion",
        description="", 
        items=qcr_proportion_select_items,
        default="default",
        update=qcr_update_proportion_select,
    )
    bpy.types.Scene.qcr_lock_proportion = bpy.props.BoolProperty(
        name="Lock Resolution Ratio", 
        description="",
        default=False,
        update=qcr_check_lock_proportion,
    )

    # 注册监听事件
    # Registering Events
    bpy.app.handlers.depsgraph_update_post.append(qcr_update_select)

    # 注册翻译
    # Register translation
    translation.register_module()
    # 注册插件偏好设置
    # Register addon preferences
    addon_prefs.register_module()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.qcr_resolution_setup
    del bpy.types.Scene.qcr_proportion_select
    del bpy.types.Scene.qcr_lock_proportion

    if qcr_update_select in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(qcr_update_select)

    translation.unregister_module()
    addon_prefs.unregister_module()


if __name__ == "__main__":
    register()
