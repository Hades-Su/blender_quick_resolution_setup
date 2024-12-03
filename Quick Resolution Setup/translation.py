import os
import re
import bpy
import json

###
"""
使用方式
在__init__.py中添加
from .translation import translation
translation.register_module()
translation.unregister_module()
即可
"""
###

def get_locale_dict(loc_file_path):
    with open(loc_file_path, 'r') as fr:
        data = json.load(fr)
    return data

__escape_pattern = re.compile(r'(\\u.{4}|\\.)')

# 替换转义字符
def __replace_escape_character(text):
    text = text.replace("\\\\u", "\\u")
    return __escape_pattern.sub(
        lambda x:x.group(1).encode("utf-8").decode("unicode-escape"),
        text
    )

__quote_pattern = re.compile('"(.*)"', re.S)

# 从 PO 文件加载词典
def load_l10n_dict(po_dir_path, loc_dict):
    l10n_dict = {}

    for po_file in os.listdir(po_dir_path):
        locale_name = po_file[:po_file.find(".po")]

        # 忽略大小写判断是否存在其中
        if locale_name.casefold() in map(str.casefold, loc_dict.keys()):
            locale = loc_dict[locale_name]

            if locale not in l10n_dict:
                l10n_dict[locale] = {}

            po_file_path = os.path.join(po_dir_path, po_file)

            with open(po_file_path, 'r', encoding='utf-8') as file:
                # mode = ('DEFAULT', 'MSGCTXT', 'MSGID' 'MSGSTR')
                mode = 'DEFAULT'
                msgctxt = '*'
                msgid = ""
                msgstr = ""
                for raw_line in file:
                    strip_line = raw_line.strip()
                    line = __replace_escape_character(strip_line)
                    if line.startswith("msgctxt"):
                        mode = 'MSGCTXT'
                        msgctxt = __quote_pattern.findall(line)[0]
                    elif line.startswith("msgid"):
                        mode = 'MSGID'
                        msgid = __quote_pattern.findall(line)[0]
                    elif line.startswith("msgstr"):
                        mode = "MSGSTR"
                        msgstr = __quote_pattern.findall(line)[0]
                    elif line.startswith("\""):
                        text = __quote_pattern.findall(line)[0]
                        if mode =='MSGID':
                            msgid = "".join([msgid, text])
                        elif mode =='MSGSTR':
                            msgstr = "".join([msgstr, text])
                        elif mode =='MSGCTXT':
                            msgctxt = "".join([msgctxt, text])
                    elif mode == "MSGSTR":
                        mode = 'DEFAULT'
                        l10n_dict[locale][(msgctxt, msgid)] = msgstr
                        msgctxt = '*'
                if mode == "MSGSTR":
                    mode = 'DEFAULT'
                    l10n_dict[locale][(msgctxt, msgid)] = msgstr
                    msgctxt = '*'

    return l10n_dict

__locale_pattern = re.compile(r'locale_\d+\.\d+\.\d+.json')

def register_module():
    os.path.dirname(__file__)
    my_dir = os.path.dirname(os.path.realpath(__file__))
    po_dir_path = os.path.join(my_dir, "translation", "language")  # 可以自定义文件夹名称
    lc_dir_path = os.path.join(my_dir, "translation", "resource")  # 可以自定义文件夹名称

    # print("Note: Blender has updated its language locale starting from v4.0.0.")
    # print("注意：Blender已从v4.0.0开始更新了其语言代码。")

    # 基于当前blender版本，选择相对应的locale_x.x.x.json文件
    blender_version = bpy.app.version
    # blender_version = (3, 6, 0)
    # blender_version = (4, 2, 0)

    locale_path_dict = {}
    for lc_file in os.listdir(lc_dir_path):
        # 筛选出带有版本号的
        # 例如不保留'locale.json': ['locale.json', 'locale_2.80.0.json', 'locale_3.0.0.json', 'locale_4.0.0.json']
        if __locale_pattern.search(lc_file):
            locale_version = tuple(int(x) for x in lc_file[:lc_file.find(".json")].split("_")[1].split("."))
            locale_path_dict[locale_version] = os.path.join(lc_dir_path, lc_file)

    locale_path = locale_path_dict[max([locale_version for locale_version in locale_path_dict.keys() if locale_version <= blender_version])]
    # print(f"当前使用语言代码映射文件：{locale_path}\n")
    locale_dict = get_locale_dict(locale_path)

    # locale_list = bpy.app.translations.locales
    # blender 4.0.0 以上 (v4.2.0)
    # locale_list = ('ca_AD', 'en_US', 'es', 'fr_FR', 'ja_JP', 'sk_SK', 'zh_HANS', 'de_DE', 'it_IT', 'ka', 'ko_KR', 'pt_BR', 'pt_PT', 'ru_RU', 'sw', 'ta', 'uk_UA', 'vi_VN', 
    #     'zh_HANT', 'ab', 'ar_EG', 'be', 'bg_BG', 'cs_CZ', 'da', 'el_GR', 'eo', 'eu_EU', 'fa_IR', 'fi_FI', 'ha', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU', 'id_ID', 'km', 
    #     'ky_KG', 'ne_NP', 'nl_NL', 'pl_PL', 'sl', 'sr_RS', 'sr_RS@latin', 'sv_SE', 'th_TH', 'tr_TR')
    # blender 4.0.0 以下 (v3.6.9)
    # locale_list = ('ca_AD', 'en_US', 'es', 'fr_FR', 'ja_JP', 'sk_SK', 'zh_CN', 'cs_CZ', 'de_DE', 'it_IT', 'ka', 'ko_KR', 'pt_BR', 'pt_PT', 'ru_RU', 'uk_UA', 'vi_VN', 'zh_TW', 
    #     'ab', 'ar_EG', 'eo', 'eu_EU', 'fa_IR', 'fi_FI', 'ha', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU', 'id_ID', 'ky_KG', 'nl_NL', 'pl_PL', 'sr_RS', 'sr_RS@latin', 'sv_SE', 
    #     'th_TH', 'tr_TR')
    # blender 3.0.0 以下 (v2.93.18)
    # locale_list = ('en_US', 'es', 'ja_JP', 'sk_SK', 'uk_UA', 'vi_VN', 'zh_CN', 'ar_EG', 'cs_CZ', 'de_DE', 'fr_FR', 'it_IT', 'ko_KR', 'pt_BR', 'pt_PT', 'ru_RU', 'zh_TW', 'ab', 
    #     'ca_AD', 'eo', 'eu_EU', 'fa_IR', 'ha', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU', 'id_ID', 'ky_KG', 'nl_NL', 'pl_PL', 'sr_RS', 'sr_RS@latin', 'sv_SE', 'th_TH', 'tr_TR')

    # print(f"当前支持的语言代码：{locale_list}")

    l10n_dict = load_l10n_dict(po_dir_path, locale_dict)
    # print(f"翻译字典：{l10n_dict}")

    bpy.app.translations.register(__name__, translations_dict=l10n_dict)

def unregister_module():
    bpy.app.translations.unregister(__name__)
