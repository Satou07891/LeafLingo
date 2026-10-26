from PIL import Image, ImageTk
import sys, os, io, json, zlib, gzip, struct, shutil, re, time, zipfile, threading, traceback
import base64
import tempfile
from pathlib import Path
from hashlib import sha256
from collections import defaultdict

import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

try:
    import nbtlib
    from nbtlib import parse_nbt, Compound, List as NBTList, String as NBTString
except ImportError:
    print("请先安装 nbtlib: pip install nbtlib")
    sys.exit(1)


# ==========================================
# 窗口内嵌图标 (这里是之前的 Base64，如果需要换新图标，请运行替换补丁)
# ==========================================
ICON_BASE64 = """
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
0WyJtQ2aNnoAAAAASUVORK5CYII=
"""

def apply_icon(window):
    """把内嵌的Base64图标应用为窗口图标，并完美适配任务栏高清显示"""
    try:
        # 解码 Base64 数据
        icon_data = base64.b64decode(ICON_BASE64)
        temp_dir = tempfile.gettempdir()
        temp_icon_path = os.path.join(temp_dir, "leaflingo_temp_icon.ico")
        with open(temp_icon_path, "wb") as f:
            f.write(icon_data)
        
        # 1. 设置左上角图标（兼容性最好）
        window.iconbitmap(temp_icon_path)
        
        # 2. 【核心修复】使用 ImageTk 生成一张 256x256 的高清 PNG 给任务栏用
        img = Image.open(temp_icon_path)
        img = img.convert("RGBA").resize((256, 256), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        # 将这个高清图片设置为窗口图标
        window.wm_iconphoto(True, photo)
        
        # 注意：一定要把 photo 挂载到 window 上，否则会被 Python 垃圾回收，导致图标不显示！
        window._icon_photo = photo
        
    except Exception as e:
        print(f"[警告] 内嵌图标加载失败: {e}")

# ==========================================
# UI 主题常量（白灰系保持不变，供后续新增使用）
# ==========================================
ctk.set_appearance_mode("light")  # 锁死浅色，避免系统深色下花脸

C_BG          = "#FFFFFF"
C_SURFACE     = "#F0F2F5"
C_SURFACE_ALT = "#FAFAFA"
C_BORDER      = "#E0E0E0"
C_TEXT        = "#333333"
C_TEXT_MUTED  = "#777777"
C_TEXT_LIGHT  = "#888888"

C_PRIMARY       = "#007ACC"
C_PRIMARY_HOVER = "#005A9E"
C_DANGER        = "#B84C3D"
C_DANGER_HOVER  = "#9B3A2E"
C_SUCCESS       = "#E4E7ED"
C_SUCCESS_HOVER = "#D0D0D0"

FONT_FAMILY  = "Microsoft YaHei"
FONT_TITLE   = (FONT_FAMILY, 24, "bold")
FONT_HEADING = (FONT_FAMILY, 16, "bold")
FONT_BODY    = (FONT_FAMILY, 13)
FONT_SMALL   = (FONT_FAMILY, 11)

def _fit_size(win, w, h):
    """窗口尺寸自适应：不超过屏幕 90%"""
    try:
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        return min(w, int(sw * 0.9)), min(h, int(sh * 0.9))
    except Exception:
        return w, h

# ==========================================
# 全局配置与路径
# ==========================================
if getattr(sys, 'frozen', False):
    # 如果是打包后的 exe 环境，获取 exe 所在目录
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # 如果是源码运行，获取当前 py 文件所在目录
    BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / "LeafLingo_work"
DATA_JSON = WORK_DIR / "data.json"
DATA_ORIG_JSON = WORK_DIR / "data_orig.json"
LANG_JSON = WORK_DIR / "lang.json"
DP_DATA_JSON = WORK_DIR / "dp_data.json"
DP_DATA_ORIG_JSON = WORK_DIR / "dp_data_orig.json"
DP_LANG_JSON = WORK_DIR / "dp_lang.json"
WORLD_BACKUP = BASE_DIR.parent / (BASE_DIR.name + "_backup")
DP_BACKUP = WORK_DIR / "datapacks_backup"

UNZIPPED_RECORDS = [] 

# ==========================================
# 辅助函数
# ==========================================
# ==========================================
# 手动翻译：提取 / 回填 辅助函数
# ==========================================

def _is_base64_blob(s):
    """判断是否为 Base64 乱码（如皮肤数据）"""
    if not isinstance(s, str): return False
    t = s.strip()
    if t.startswith("eyJ") or t.startswith("ewog"): return True
    if len(t) > 64 and re.fullmatch(r'[a-zA-Z0-9+/=\n\r]+', t): return True
    return False

def _is_playsound_text(s):
    """判断是否纯 /playsound 音效指令，剥掉所有私有区字符再判断。"""
    if not isinstance(s, str): return False
    clean = re.sub(r'[\ue000-\uf8ff\u0000-\u001f]', '', s)
    return clean.strip().lstrip("./: ").lower().startswith("playsound ")

_URL_PREFIX_RE = re.compile(r'^(?:https?://|www\.)', re.I)
_URL_DOMAIN_RE = re.compile(r'^[A-Za-z0-9.-]+\.(?:com|net|org|io|cn|gg|tv|me|co|app|dev|cc|xyz)$', re.I)

def _is_url_text(s):
    """判断是否为网址/域名，不应翻译。"""
    if not isinstance(s, str): return False
    t = s.strip()
    if not t: return False
    if _URL_PREFIX_RE.match(t): return True
    if _URL_DOMAIN_RE.match(t): return True
    return False

def _text_fp(s):
    """文本指纹：SHA256 前 8 位，用于 TXT 导入导出按内容匹配。"""
    if not isinstance(s, str): return ""
    return sha256(s.encode("utf-8")).hexdigest()[:8]

def _manual_should_skip(s):
    if not isinstance(s, str): return True
    t = s.strip()
    if t == "": return True
    if _is_playsound_text(t): return True
    if _is_base64_blob(t): return True     # ← 【新增】跳过头颅皮肤等 Base64 乱码
    if _is_url_text(t): return True
    if t.startswith("minecraft:"): return True
    if re.match(r'^\[\d{2}:\d{2}:\d{2}\]\s*$', t): return True
    if not re.search(r'[a-zA-Z]', t): return True
    return False

def _extract_tag_texts(tag_str):
    """从 tag NBT 字符串里按位置顺序提取所有 text 英文（兼容单层和双层转义）。"""
    results = []
    for m in re.finditer(r'\\"text\\":\\"((?:[^"\\]|\\.)*?)\\"', tag_str):
        results.append((m.start(), m.group(1)))
    for m in re.finditer(r'(?<!\\)"text":"((?:[^"\\]|\\.)*?)"', tag_str):
        results.append((m.start(), m.group(1)))
    results.sort(key=lambda x: x[0])
    return [v for _, v in results if not _manual_should_skip(v)]


def _apply_tag_texts(tag_str, it):
    """从 tag NBT 字符串里按位置顺序回填中文（保留原转义形态）。"""
    matches = []
    for m in re.finditer(r'\\"text\\":\\"((?:[^"\\]|\\.)*?)\\"', tag_str):
        matches.append((m.start(), m.end(), 'double', m.group(1)))
    for m in re.finditer(r'(?<!\\)"text":"((?:[^"\\]|\\.)*?)"', tag_str):
        matches.append((m.start(), m.end(), 'single', m.group(1)))
    matches.sort(key=lambda x: x[0])

    replacements = []
    for start, end, fmt, en in matches:
        if _manual_should_skip(en):
            continue
        try:
            zh = next(it)
        except StopIteration:
            break
        new_esc = zh.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        if fmt == 'double':
            new_str = f'\\"text\\":\\"{new_esc}\\"'
        else:
            new_str = f'"text":"{new_esc}"'
        replacements.append((start, end, new_str))

    result = tag_str
    for start, end, new_str in reversed(replacements):
        result = result[:start] + new_str + result[end:]
    return result


def _walk_extract(obj, out, skip_text=False):
    if isinstance(obj, dict):
        is_player = obj.get("type") == "minecraft:player"
        insertion = obj.get("insertion") if isinstance(obj.get("insertion"), str) else None
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                skip_this = skip_text or is_player or (insertion is not None and v == insertion)
                if not skip_this and not _manual_should_skip(v):
                    out.append(v)
            elif k == "tag" and isinstance(v, str):
                out.extend(_extract_tag_texts(v))
            else:
                _walk_extract(v, out, skip_text or is_player)
    elif isinstance(obj, list):
        for item in obj:
            _walk_extract(item, out, skip_text)


def _walk_apply(obj, it, skip_text=False):
    if isinstance(obj, dict):
        is_player = obj.get("type") == "minecraft:player"
        insertion = obj.get("insertion") if isinstance(obj.get("insertion"), str) else None
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                skip_this = skip_text or is_player or (insertion is not None and v == insertion)
                if not skip_this and not _manual_should_skip(v):
                    try:
                        obj[k] = next(it)
                    except StopIteration:
                        return
            elif k == "tag" and isinstance(v, str):
                obj[k] = _apply_tag_texts(v, it)
            else:
                _walk_apply(v, it, skip_text or is_player)
    elif isinstance(obj, list):
        for item in obj:
            _walk_apply(item, it, skip_text)

def extract_translatable(text):
    stripped = text.strip()
    out = []
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            parsed = json.loads(text)
            _walk_extract(parsed, out)
            return out
        except json.JSONDecodeError:
            pass
    if not _manual_should_skip(text):
        out.append(text)
    return out

def apply_translatable(text, zh_list):
    stripped = text.strip()
    it = iter(zh_list)
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            parsed = json.loads(text)
            _walk_apply(parsed, it)
            return json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
        except json.JSONDecodeError:
            pass
    try:
        return next(it)
    except StopIteration:
        return text

# ==========================================
# 展示 / 回填（手动翻译用）
# ==========================================
def _should_skip_for_display(s):
    """显示用：跳过空、时间戳、minecraft:、纯符号，但保留中文（区别于 _manual_should_skip）。"""
    if not isinstance(s, str): return True
    t = s.strip()
    if t == "": return True
    if _is_playsound_text(t): return True
    if _is_url_text(t): return True
    if t.startswith("minecraft:"): return True
    if re.match(r'^\[\d{2}:\d{2}:\d{2}\]\s*$', t): return True
    if not re.search(r'[a-zA-Z\u4e00-\u9fff]', t): return True
    return False


def _collect_all_texts(obj):
    """收集所有可显示的 text（中英文都收），严格按出现顺序排列。
    text 值本身是 JSON 时递归解析；无引号 JSON 用正则提取 name:/text:。"""
    results = []
    seen = set()
    def add(v):
        if _should_skip_for_display(v): return
        if is_namespace_id(v): return
        if is_translation_key(v): return
        results.append(v)
    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "minecraft:player": return
            insertion = o.get("insertion") if isinstance(o.get("insertion"), str) else None
            for k, v in o.items():
                if k == "text" and isinstance(v, str):
                    if _should_skip_for_display(v): continue
                    if insertion is not None and v == insertion: continue
                    vs = v.strip()
                    if vs.startswith("{") or vs.startswith("["):
                        try:
                            parsed = json.loads(vs)
                            walk(parsed)
                            continue
                        except Exception:
                            for m in re.finditer(r'\\?"?(?:\bname|\btext|\bCustomName)\\?"?\s*:\s*\\?"([^"\\]+)\\?"', vs):
                                vv = m.group(1).replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                                if _should_skip_for_display(vv): continue
                                if is_namespace_id(vv) or is_translation_key(vv): continue
                                if INTERNAL_TAG_RE.match(vv): continue
                                if vv.startswith("generic.") or vv.startswith("minecraft:"): continue
                                add(vv)
                            continue
                    add(v)
                elif k == "tag" and isinstance(v, str):
                    tag_matches = []
                    for m in re.finditer(r'\\"text\\":\\"((?:[^"\\]|\\.)*?)\\"', v):
                        tag_matches.append((m.start(), m.group(1)))
                    for m in re.finditer(r'(?<!\\)"text":"((?:[^"\\]|\\.)*?)"', v):
                        tag_matches.append((m.start(), m.group(1)))
                    tag_matches.sort(key=lambda x: x[0])
                    for _, val in tag_matches:
                        if not _should_skip_for_display(val): add(val)
                else:
                    walk(v)
        elif isinstance(o, list):
            for item in o: walk(item)
    walk(obj)
    return results


def _apply_single_text(raw_text, new_text):
    """精确替换第一个非空 text（可在顶层、extra 或 tag 中）。"""
    try:
        obj = json.loads(raw_text)
    except Exception:
        return new_text
    done = [False]
    new_esc = new_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    def walk(o):
        if done[0]: return
        if isinstance(o, dict):
            if o.get("type") == "minecraft:player": return
            insertion = o.get("insertion") if isinstance(o.get("insertion"), str) else None
            for k, v in list(o.items()):
                if done[0]: return
                if k == "text" and isinstance(v, str):
                    if _should_skip_for_display(v): continue
                    if insertion is not None and v == insertion: continue
                    o[k] = new_text; done[0] = True; return
                elif k == "tag" and isinstance(v, str):
                    td = [False]
                    def repl_d(m):
                        if td[0] or _should_skip_for_display(m.group(1)): return m.group(0)
                        td[0] = True
                        return f'\\"text\\":\\"{new_esc}\\"'
                    v2 = re.sub(r'\\"text\\":\\"((?:[^"\\]|\\.)*?)\\"', repl_d, v)
                    if not td[0]:
                        def repl_s(m):
                            if td[0] or _should_skip_for_display(m.group(1)): return m.group(0)
                            td[0] = True
                            return f'"text":"{new_esc}"'
                        v2 = re.sub(r'(?<!\\)"text":"((?:[^"\\]|\\.)*?)"', repl_s, v2)
                    if td[0]:
                        o[k] = v2; done[0] = True; return
                else:
                    walk(v)
        elif isinstance(o, list):
            for item in o: walk(item)
    walk(obj)
    if done[0]:
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    return new_text

def _replace_all_texts(raw_text, new_lines):
    """将新文本按行精准回填到 JSON 的所有 text 节点中。
       如果玩家删减了行数，多余的节点自动置空；
       如果玩家增加了行数，多出的内容追加到最后一个节点。
    """
    try:
        obj = json.loads(raw_text)
    except Exception:
        return raw_text

    it = iter(new_lines)
    last_node_ref = [None] # 记录最后一个 text 节点的父级引用

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "minecraft:player": return
            insertion = o.get("insertion") if isinstance(o.get("insertion"), str) else None
            for k, v in list(o.items()):
                if k == "text" and isinstance(v, str):
                    if _should_skip_for_display(v): continue
                    if insertion is not None and v == insertion: continue
                    vs = v.strip()
                    if vs.startswith("{") or vs.startswith("["):
                        try:
                            json.loads(vs)
                            _is_inline_json = False
                        except Exception:
                            _is_inline_json = True
                        if _is_inline_json:
                            _replaced = [False]
                            def _repl(m):
                                val = m.group(1)
                                if _should_skip_for_display(val): return m.group(0)
                                if is_namespace_id(val) or is_translation_key(val): return m.group(0)
                                if INTERNAL_TAG_RE.match(val): return m.group(0)
                                if val.startswith("generic.") or val.startswith("minecraft:"): return m.group(0)
                                try:
                                    zh = next(it)
                                except StopIteration:
                                    return m.group(0)
                                _replaced[0] = True
                                esc = zh.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                                prefix = m.group(0)[:m.start(1) - m.start(0)]
                                suffix = m.group(0)[m.end(1) - m.start(0):]
                                return prefix + esc + suffix
                            v2 = re.sub(r'\\?"?(?:\bname|\btext|\bCustomName)\\?"?\s*:\s*\\?"([^"\\]+)\\?"', _repl, v)
                            if _replaced[0]:
                                o[k] = v2
                                last_node_ref[0] = (o, k)
                                continue
                    try:
                        o[k] = next(it)
                        last_node_ref[0] = (o, k)
                    except StopIteration:
                        # 玩家删减了行数：多余的节点置空，保证 JSON 结构不崩
                        o[k] = "" 
                elif k == "tag" and isinstance(v, str):
                    tag_matches = []
                    for m in re.finditer(r'\\"text\\":\\"((?:[^"\\]|\\.)*?)\\"', v):
                        tag_matches.append((m.start(), m.end(), m.group(1), True))
                    for m in re.finditer(r'(?<!\\)"text":"((?:[^"\\]|\\.)*?)"', v):
                        tag_matches.append((m.start(), m.end(), m.group(1), False))
                    tag_matches.sort(key=lambda x: x[0])

                    replacements = []
                    for start, end, val, is_double in tag_matches:
                        if _should_skip_for_display(val): continue
                        try:
                            zh = next(it)
                            new_esc = zh.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                            if is_double:
                                new_str = f'\\"text\\":\\"{new_esc}\\"'
                            else:
                                new_str = f'"text":"{new_esc}"'
                            replacements.append((start, end, new_str))
                        except StopIteration:
                            # 玩家删减了行数：多余的转义节点置空
                            if is_double:
                                replacements.append((start, end, '\\"text\\":\\"\\"'))
                            else:
                                replacements.append((start, end, '"text":""'))
                    
                    for start, end, new_str in reversed(replacements):
                        v = v[:start] + new_str + v[end:]
                    o[k] = v
                else:
                    walk(v)
        elif isinstance(o, list):
            for item in o: walk(item)

    walk(obj)
    
    # 玩家增加了行数：把多出来的行，追加到最后一个节点里，防止文字丢失
    extra_lines = list(it)
    if extra_lines and last_node_ref[0]:
        parent, k = last_node_ref[0]
        parent[k] += " " + " ".join(extra_lines)

    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

def _unwrap_cmd(raw_text):
    """如果指令被包在 JSON 组件里，剥离外壳返回真实的指令字符串"""
    raw_text = raw_text.strip()
    if raw_text.startswith("{") and raw_text.endswith("}"):
        try:
            obj = json.loads(raw_text)
            if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                inner = obj["text"]
                if re.match(r'^/?\s*(?:give|execute|summon|setblock|fill|data|scoreboard|tp|teleport|function|advancement|item|effect|enchant|say|tellraw|title|subtitle|actionbar|me|msg|tell|kill|clear|xp|experience|gamerule|time|weather|spawnpoint|setworldspawn|playsound|particle)\s', inner, re.IGNORECASE):
                    return inner
        except Exception:
            pass
    return raw_text

def _extract_cmd_texts(cmd_str):
    """从长指令中提取纯文本，全面兼容 NBT 转义 (\") 和未转义格式"""
    matches = []
    
    # 1. 匹配 text 节点（兼容 "text":"xxx", "text":"xxx", text:"xxx"）
    for m in re.finditer(r'\\?"?text\\?"?\s*:\s*\\?"((?:[^"\\]|\\.)*?)\\?"', cmd_str):
        matches.append((m.start(1), m.end(1), m.group(1)))

    # 2. 匹配 item_name="xxx" 或 custom_name="xxx"
    for m in re.finditer(r'\b(?:item_name|custom_name)\s*=\s*\\?"([^"\\]+?)\\?"', cmd_str):
        matches.append((m.start(1), m.end(1), m.group(1)))
        
    # 3. 匹配 CustomName:"xxx" 或 CustomName="xxx"
    for m in re.finditer(r'\bCustomName\s*[:=]\s*\\?"((?:[^"\\]|\\.)*?)\\?"', cmd_str):
        matches.append((m.start(1), m.end(1), m.group(1)))
    for m in re.finditer(r'(?:(?<=\{)|(?<=,))\s*[Nn]ame\s*:\s*\\?"((?:[^"\\]|\\.)*?)\\?"', cmd_str):
        matches.append((m.start(1), m.end(1), m.group(1)))

    # 去重并按位置排序
    matches.sort(key=lambda x: x[0])
    unique_matches = []
    last_end = -1
    for start, end, val in matches:
        if start >= last_end:
            unique_matches.append((start, end, val))
            last_end = end
    return unique_matches

def extract_display_text(raw_text):
    raw_text = raw_text.strip()

    # 【过滤】纯文本 /playsound 是音效指令，没有可翻文本
    if _is_playsound_text(raw_text):
        return ""
    # 【过滤】纯文本 URL / 域名
    if _is_url_text(raw_text):
        return ""

    # 检查是否是包装的指令
    unwrapped = _unwrap_cmd(raw_text)
    if unwrapped != raw_text:
        raw_text = unwrapped

    # 无论是英文还是中文，只要是 JSON，统统按行拆开展示
    if raw_text.startswith("{") or raw_text.startswith("["):
        try:
            obj = json.loads(raw_text)
            texts = _collect_all_texts(obj)
            if texts:
                return "\n".join(texts) # 中英文混排，按行输出
        except Exception:
            # 1.8 版本的无引号 JSON 会导致 json.loads 报错，不要直接放弃，继续往下走提取指令
            pass

    # 【无引号 JSON 兜底】json.loads 失败后，直接找 name:"..." / text:"..." / CustomName:"..."
    if raw_text.startswith("{") or raw_text.startswith("["):
        loose = re.findall(r'\\?"?(?:\bname|\btext|\bCustomName)\\?"?\s*:\s*\\?"([^"\\]+)\\?"', raw_text)
        valid = []
        for v in loose:
            vv = v.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
            if not vv.strip() or _is_base64_blob(vv): continue
            if is_namespace_id(vv) or is_translation_key(vv): continue
            if INTERNAL_TAG_RE.match(vv): continue
            if vv.startswith("generic.") or vv.startswith("minecraft:"): continue
            if not re.search(r'[a-zA-Z\u4e00-\u9fff]', vv): continue
            valid.append(vv)
        if valid:
            return "\n".join(valid)
        # loose 非空但 valid 为空：说明里面只有翻译键/命名空间/内部名，整条不显示
        if loose:
            return ""

    # 【1.8 修复】tellraw / title / subtitle / actionbar 开头的无引号 JSON，
    # 直接用宽松正则兜底，不依赖 _extract_cmd_texts 的复杂正则
    if re.match(r'^/?\s*(?:tellraw|title|subtitle|actionbar)\s', raw_text, re.IGNORECASE):
        loose = re.findall(r'text\s*:\s*"([^"]*)"', raw_text)
        if loose:
            valid = [v for v in loose if v.strip() and not _is_base64_blob(v)]
            if valid:
                return "\n".join(valid)

    # 处理指令（如 give / tellraw），只提取里面的文本，不展示整段
    cmd_matches = _extract_cmd_texts(raw_text)
    if cmd_matches:
        # 不过滤中文，只要不是空的、且不是 Base64 就显示
        valid_texts = []
        for _, _, val in cmd_matches:
            # 反转义提取出来的文本
            v = val.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
            if not v.strip() or _is_base64_blob(v): continue
            if is_namespace_id(v) or is_translation_key(v): continue
            if INTERNAL_TAG_RE.match(v): continue
            if v.startswith("generic.") or v.startswith("minecraft:"): continue
            valid_texts.append(v)
        if valid_texts:
            return "\n".join(valid_texts)
        return ""

    _emb = re.search(r'(?<![.\w])(?:say|tell|msg|tm)\s+(.+)$', raw_text, re.I)
    if _emb:
        _t = _emb.group(1).strip()
        if _t.startswith('"') and _t.endswith('"'):
            _t = _t[1:-1]
        if _t and not _is_base64_blob(_t):
            return _t
            
    # 纯文本情况
    items = extract_translatable(raw_text)
    if len(items) == 1:
        return items[0]
    if len(items) > 1:
        return "\n".join(items)
        
    return raw_text


def replace_display_text(raw_text, new_text):
    ns = new_text.strip()
    
    # 用户自己填了完整 JSON，直接覆盖
    if ns.startswith("{") or ns.startswith("["):
        return new_text
        
    # 检查是否是包装的指令
    unwrapped = _unwrap_cmd(raw_text)
    if unwrapped != raw_text:
        inner_replaced = replace_display_text(unwrapped, ns)
        try:
            obj = json.loads(raw_text.strip())
            obj["text"] = inner_replaced
            return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
        except Exception:
            return raw_text

    # 原文是纯文本，直接覆盖，但必须保留首尾空白（如 " \nObjective Item" 的 " \n"）
    if not (raw_text.strip().startswith("{") or raw_text.strip().startswith("[")):
        if not ns: return raw_text  # 用户全删了，保留原样

        # 处理指令（如 give / tellraw），按顺序将译文塞回原指令
        cmd_matches = _extract_cmd_texts(raw_text)
        if cmd_matches:
            # 解除过滤，确保内容能被塞回
            valid_matches = []
            for start, end, val in cmd_matches:
                v = val.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                if not v.strip() or _is_base64_blob(v): continue
                if is_namespace_id(v) or is_translation_key(v): continue
                if INTERNAL_TAG_RE.match(v): continue
                if v.startswith("generic.") or v.startswith("minecraft:"): continue
                valid_matches.append((start, end, val))
            lines = ns.split("\n")
            result = raw_text
            # 【修复】倒序替换，避免前一个替换改变长度后，后一个 start/end 错位
            for i in range(len(valid_matches) - 1, -1, -1):
                start, end, old_val = valid_matches[i]
                if i < len(lines):
                    new_val = lines[i]
                    escaped = new_val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                    result = result[:start] + escaped + result[end:]
            return result

        _emb = re.search(r'(?<![.\w])(?:say|tell|msg|tm)\s+(.+)$', raw_text, re.I)
        if _emb:
            start, end = _emb.start(1), _emb.end(1)
            escaped = ns.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return raw_text[:start] + escaped + raw_text[end:]
        
        # 提取原文的首尾空白
        leading_ws = re.match(r'^\s*', raw_text).group(0) if raw_text else ""
        trailing_ws = re.search(r'\s*$', raw_text).group(0) if raw_text else ""
        
        final_val = ns
        # 如果用户没主动在前面敲空格/回车，就把原文的前导空白补回去
        if not re.match(r'^\s', final_val):
            final_val = leading_ws + final_val
            
        # 如果用户没主动在后面敲，补回尾部空白
        if not re.search(r'\s$', final_val):
            final_val = final_val + trailing_ws
            
        return final_val
        
    # 原文是 JSON，不管玩家填了几行，都按顺序安全回填
    try:
        obj = json.loads(raw_text)
    except Exception:
        # 【修复】无引号 JSON：json.loads 失败时，走 _extract_cmd_texts 按位置替换，
        # 保留 name:/text:/CustomName 周围的 color/clickEvent 等结构。
        cmd_matches = _extract_cmd_texts(raw_text)
        if cmd_matches:
            valid_matches = []
            for start, end, val in cmd_matches:
                v = val.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                if not v.strip() or _is_base64_blob(v): continue
                if is_namespace_id(v) or is_translation_key(v): continue
                if INTERNAL_TAG_RE.match(v): continue
                if v.startswith("generic.") or v.startswith("minecraft:"): continue
                valid_matches.append((start, end, val))
            lines = ns.split("\n")
            result = raw_text
            for i in range(len(valid_matches) - 1, -1, -1):
                start, end, old_val = valid_matches[i]
                if i < len(lines):
                    new_val = lines[i]
                    escaped = new_val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                    result = result[:start] + escaped + result[end:]
            return result
        return new_text

    existing = _collect_all_texts(obj)
    if not existing:
        return new_text
    lines = ns.split("\n")
    return _replace_all_texts(raw_text, lines)

def extract_for_check(raw_text):
    """查漏专用：整段含中文视为已翻译（不报）；纯英文时，
    简单文本显示该文本，长串显示整段 raw_text。"""
    raw_text = raw_text.strip()
    if not raw_text:
        return None
    if re.search(r'[\u4e00-\u9fff]', raw_text):
        return None                       # ← 整段有中文 = 翻译过了，跳过
    items = extract_translatable(raw_text)
    if not items:
        return None
    return items[0] if len(items) == 1 else raw_text

# ==========================================
# 核心业务逻辑
# ==========================================
def parse_chunk_nbt(data: bytes):
    try: return nbtlib.File.parse(io.BytesIO(data))
    except Exception: pass
    try: return nbtlib.load(io.BytesIO(data))
    except Exception: pass
    return nbtlib.parse_nbt(data)

def read_mca(path):
    chunks = {}
    with open(path, "rb") as f:
        header = f.read(8192)
        if len(header) < 8192: return chunks
        for i in range(1024):
            entry = header[i * 4:(i + 1) * 4]
            offset = (entry[0] << 16) | (entry[1] << 8) | entry[2]
            count = entry[3]
            if offset == 0 or count == 0: continue
            f.seek(offset * 4096)
            lb = f.read(4)
            if len(lb) < 4: continue
            length = struct.unpack(">I", lb)[0]
            if length == 0: continue
            comp = f.read(1)[0]
            data = f.read(length - 1)
            try:
                if comp == 1: data = gzip.decompress(data)
                elif comp == 2: data = zlib.decompress(data)
                elif comp == 3: pass
                else: continue
                chunks[i] = data
            except Exception: pass
    return chunks

def write_mca(path, chunks):
    header = bytearray(8192)
    body = bytearray()
    next_sector = 2
    for idx in sorted(chunks.keys()):
        raw = chunks[idx]
        compressed = zlib.compress(raw)
        payload = struct.pack(">I", len(compressed) + 1) + b"\x02" + compressed
        sectors = (len(payload) + 4095) // 4096
        padded = payload + b"\x00" * (sectors * 4096 - len(payload))
        header[idx * 4]     = (next_sector >> 16) & 0xFF
        header[idx * 4 + 1] = (next_sector >> 8) & 0xFF
        header[idx * 4 + 2] = next_sector & 0xFF
        header[idx * 4 + 3] = sectors
        body += padded
        next_sector += sectors
    temp_path = str(path) + ".tmp"
    try:
        with open(temp_path, "wb") as f:
            f.write(bytes(header))
            f.write(bytes(body))
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    except Exception:
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except Exception: pass
        raise

def split_path(path_str):
    if not path_str: return []
    tokens = []
    for part in path_str.split("."):
        has_bracket = False
        while "[" in part:
            has_bracket = True
            name, rest = part.split("[", 1)
            if name: tokens.append(name)
            idx_str, part = rest.split("]", 1)
            tokens.append(int(idx_str))
        if part: tokens.append(part)
        elif not has_bracket: tokens.append("")
    return tokens

def walk_strings(obj, path, result):
    if isinstance(obj, str): result[path] = str(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items(): walk_strings(v, f"{path}.{k}" if path else str(k), result)
    elif isinstance(obj, list):
        for i, v in enumerate(obj): walk_strings(v, f"{path}[{i}]", result)

def get_by_path(root, path_str):
    cur = root
    for t in split_path(path_str):
        try: cur = cur[t]
        except (KeyError, IndexError, TypeError): return None
    return cur

def set_by_path(root, path_str, value):
    tokens = split_path(path_str)
    if not tokens: return
    cur = root
    for t in tokens[:-1]: cur = cur[t]
    cur[tokens[-1]] = NBTString(value)

TRANSLATABLE_LEAF = {
    "text", "title", "pages", "lore", "name", "item_name", "custom_name", "display_name", "subtitle", "description", "value",
    "Text", "Text1", "Text2", "Text3", "Text4", "CustomName", "Name", "Lore", "Title", "Subtitle", "Description",
    "Command", "command", "BlockCommand", "LastOutput", "last_output", "messages", "filtered_messages", "fallback"
}
BLACKLIST_LEAF = {
    "id", "x", "y", "z", "UUID", "UUIDMost", "UUIDLeast", "Owner", "OwnerUUID", "Thrower", "SkullOwner",
    "author", "Color", "color", "Dimension", "Tags", "tag", "Team", "team", "objective", "Objective", "score", "Score"
}
NAMESPACE_ID_RE = re.compile(r"^[a-z_]+:[a-z0-9_/\.\-\+]+$")
TRANSLATION_KEY_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)+$")
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$")
INTERNAL_TAG_RE = re.compile(r"^[a-z][a-z0-9_]{2,30}$")

COMMAND_KEYWORDS = (
    "entitydata ", "blockdata ", "stats ", "data modify ", "data remove ",
    "testfor ", "testforblock ", "execute ", "scoreboard ", "setblock ", "summon ", "function ", "give ", "clear ", "kill ", "tp ", "teleport ", "effect ",
    "particle ", "playsound ", "tag ", "team ", "data merge", "data get", "fill ", "clone ", "advancement ", "gamemode ", "gamerule ",
    "difficulty ", "time ", "weather ", "forceload", "locate ", "loot ", "place ", "recipe ", "reload ", "replaceitem", "schedule ",
    "seed", "setidletimeout", "setworldspawn", "spawnpoint", "spreadplayers", "stopsound", "trigger ", "worldborder ",
    "waypoint ", "ride ", "attribute ", "bossbar ", "damage ", "enchant ", "experience ", "xp ", "op ", "deop ", "random "
)
OUTPUT_COMMANDS = ("say ", "tell ", "msg ", "tellraw ", "title ", "subtitle ", "actionbar ", "me ", "broadcast ", "teammsg ", "tm ")
HAS_TEXT_COMPONENT_RE = re.compile(r'\b(?:minecraft:)?(?:text|translate|custom_name|item_name|lore|display_name|CustomName)\s*[:=]|\bName\s*:\s*(?:"|\\")')
OUTPUT_INLINE_RE = re.compile(r"\b(say|tell|msg|tellraw|title|subtitle|actionbar|me|broadcast|teammsg|tm)\s", re.IGNORECASE)
MC_RESERVED_WORDS = {
    "black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray", "dark_gray", "blue", "green", "aqua", "red",
    "light_purple", "yellow", "white", "reset", "bold", "italic", "underlined", "strikethrough", "obfuscated", "true", "false", "left", "right",
    "center", "up", "down", "mainhand", "offhand", "head", "chest", "legs", "feet", "always", "never", "when_underwater", "when_sprinting",
    "hide", "show", "keep", "replace", "sidebar", "list", "below_name", "day", "night", "noon", "midnight", "north", "south", "east", "west",
    "vertical", "horizontal", "fixed", "none", "locked"
}
LETTER_RE = re.compile(r"[A-Za-z\u00C0-\u024F\u0400-\u04FF\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")

MERGE_SIGN_T1  = "__SIGN_MERGE_T1__"     
MERGE_SIGN_MSG = "__SIGN_MERGE_MSG__"    
MERGE_BOOK     = "__BOOK_MERGE__"        
MERGE_LORE     = "__LORE_MERGE__"        
MERGE_KEYS = (MERGE_SIGN_T1, MERGE_SIGN_MSG, MERGE_BOOK, MERGE_LORE)

def has_translatable_text(s): return bool(LETTER_RE.search(s))
def _strip_slash(s): return s.strip()[1:] if s.strip().startswith("/") else s.strip()
def is_namespace_id(s): return bool(NAMESPACE_ID_RE.match(s.strip()))
def is_translation_key(s): return bool(TRANSLATION_KEY_RE.match(s.strip()))
def is_output_command(s):
    body = _strip_slash(s).lower()
    return any(body.startswith(kw) for kw in OUTPUT_COMMANDS)
def is_logic_command(s):
    raw = s.strip()
    body = _strip_slash(raw).lower()
    if any(body.startswith(kw) for kw in OUTPUT_COMMANDS): return False
    if any(body.startswith(kw) for kw in COMMAND_KEYWORDS): return True
    if raw.startswith("/"): return True
    return False
def contains_text_component(s): return bool(HAS_TEXT_COMPONENT_RE.search(s) or OUTPUT_INLINE_RE.search(s))

def _has_translatable_cmd_text(s):
    """判断指令里是否有真正可翻的文本。过滤内部名、命名空间、NBT 属性名。"""
    for _, _, v in _extract_cmd_texts(s):
        vv = v.replace('\\"', '"').replace("\\\\", "\\")
        if not vv.strip(): continue
        if _is_base64_blob(vv): continue
        if is_namespace_id(vv): continue
        if INTERNAL_TAG_RE.match(vv): continue
        if vv.startswith("generic.") or vv.startswith("minecraft:"): continue
        if not has_translatable_text(vv): continue
        return True
    _m = re.search(r'(?<![.\w])(?:say|tell|msg|tm)\s+(.+)$', s, re.I)
    if _m:
        payload = _m.group(1).strip()
        if payload.startswith('"') and payload.endswith('"'):
            payload = payload[1:-1]
        if payload and not _is_base64_blob(payload) and has_translatable_text(payload):
            return True
    return False

def json_component_has_text(s):
    s = s.strip()
    if not (s.startswith("{") and s.endswith("}")): return True
    try:
        obj = json.loads(s)
    except Exception:
        return True
    def _has_text_value(t):
        if not isinstance(t, str): return False
        if _is_playsound_text(t):
            return False
        ts = t.strip()
        if ts.startswith("{") or ts.startswith("["):
            for m in re.finditer(r'\\?"?(?:\bname|\btext|\bCustomName)\\?"?\s*:\s*\\?"([^"\\]+)\\?"', ts):
                vv = m.group(1).replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                if not has_translatable_text(vv): continue
                if is_namespace_id(vv) or is_translation_key(vv): continue
                if INTERNAL_TAG_RE.match(vv): continue
                if vv.startswith("generic.") or vv.startswith("minecraft:"): continue
                return True
            return False
        if not has_translatable_text(ts): return False
        if _is_url_text(ts): return False
        if is_namespace_id(ts) or is_translation_key(ts): return False
        return True
    def _has(o):
        if isinstance(o, dict):
            if "text" in o and _has_text_value(o.get("text")): return True
            if "name" in o and _has_text_value(o.get("name")): return True
            return any(_has(v) for v in o.values())
        elif isinstance(o, list): return any(_has(v) for v in o)
        return False
    if _has(obj): return True
    for m in re.finditer(r'\b(?:text|[Nn]ame)\s*:\s*\\?"([^"\\]*)\\?"', s):
        v = m.group(1)
        if not has_translatable_text(v): continue
        if is_namespace_id(v) or is_translation_key(v): continue
        return True
    return False

def last_key(path_str):
    for t in reversed(split_path(path_str)):
        if not isinstance(t, int):
            if ":" in t: t = t.split(":", 1)[1]
            return t
    return ""

def should_extract_full(path_str, value, raw_mode=False):
    if raw_mode: return True
    key = last_key(path_str)
    if key in ("Lore", "lore", "__LORE_MERGE__"): return has_translatable_text(value) and not _is_url_text(value)
    if key == "text" and ("Lore" in path_str or "lore" in path_str): return has_translatable_text(value) and not _is_url_text(value)
    if key in MERGE_KEYS: return has_translatable_text(value) and not _is_url_text(value)
    if key in BLACKLIST_LEAF: return False
    if key not in TRANSLATABLE_LEAF: return False

    # 【1.8 命令方块 LastOutput 过滤】
    # "Command set: /testfor ..." 和 "Test passed/failed" 是命令方块状态输出，不是可翻译文本
    if key in ("LastOutput", "last_output"):
        s_low = value.strip().lower()
        if "command set:" in s_low or "test passed" in s_low or "test failed" in s_low:
            return False
        if re.match(r'^(?:/?testfor|/?testforblock|/?scoreboard|/?execute|/?setblock|/?summon|/?fill|/?data)\s', value.strip(), re.IGNORECASE):
            return False

    s = value.strip()
    if not s or not has_translatable_text(s) or is_namespace_id(s) or s.lower() in MC_RESERVED_WORDS: return False
    if _is_url_text(s): return False

    # 【过滤】坐标字符串：x=...,y=...,z=... 或 [x=...,...]
    if re.match(r'^\[?[xyz]=', s):
        return False

    # 【过滤】playsound 是纯音效指令，没有可翻译文本。
    # 去掉开头 ./: 后判断，同时覆盖 /playsound 和 ./playsound 两种写法。
    _s_clean = re.sub(r'[\ue000-\uf8ff\u0000-\u001f]', '', s)
    _s_cmd = _s_clean.strip().lstrip("./: ").lower()
    if _s_cmd.startswith("playsound "):
        return False

    # 【过滤】title/subtitle/actionbar 的 times/clear/reset 子命令，以及空文本
    # 注意：blockdata 不在这里过滤，它里面的 Text1~4 可能有告示牌显示文本
    if re.match(r'^/?\s*(?:title|subtitle|actionbar)\s', s, re.IGNORECASE):
        if re.match(r'^/?\s*(?:title|subtitle|actionbar)\s+\S+\s+(?:times|clear|reset)\b', s, re.IGNORECASE):
            return False
        _loose = re.findall(r'text\s*:\s*\\?"([^"\\]*)\\?"', s)
        if _loose and not any(v.strip() for v in _loose):
            return False
        _m = re.match(r'^/?\s*(?:title|subtitle|actionbar)\s+\S+\s+(?:title|subtitle|actionbar)\s+"([^"]*)"', s, re.IGNORECASE)
        if _m and not _m.group(1).strip():
            return False

    # 【过滤】tellraw 的空 text（有 text: 字段但全为空）
    if re.match(r'^/?\s*tellraw\s', s, re.IGNORECASE):
        _loose = re.findall(r'text\s*:\s*\\?"([^"\\]*)\\?"', s)
        if _loose and not any(v.strip() for v in _loose):
            return False

    if is_output_command(s): return True
    if is_logic_command(s): return _has_translatable_cmd_text(s)
    if is_translation_key(s): return False
    return json_component_has_text(s)

def should_extract_light(path_str, value):
    s = value.strip()
    if not s: return False
    # 【过滤】坐标字符串：x=...,y=...,z=... 或 [x=...,...]
    if re.match(r'^\[?[xyz]=', s):
        return False
    # 【过滤】playsound 是纯音效指令，没有可翻译文本。
    # 去掉开头 ./: 后判断，同时覆盖 /playsound 和 ./playsound 两种写法。
    _s_clean = re.sub(r'[\ue000-\uf8ff\u0000-\u001f]', '', s)
    _s_cmd = _s_clean.strip().lstrip("./: ").lower()
    if _s_cmd.startswith("playsound "):
        return False
    key = last_key(path_str)
    if key in ("Lore", "lore", "__LORE_MERGE__"): return has_translatable_text(s) and not _is_url_text(s)
    if key == "text" and ("Lore" in path_str or "lore" in path_str): return has_translatable_text(s) and not _is_url_text(s)
    if key in MERGE_KEYS: return has_translatable_text(s) and not _is_url_text(s)
    if not has_translatable_text(s) or is_namespace_id(s) or s.lower() in MC_RESERVED_WORDS: return False
    if _is_url_text(s): return False
    if UUID_RE.match(s) or INTERNAL_TAG_RE.match(s): return False
    # 【过滤】light 模式也过滤纯逻辑指令，避免 /playsound 等进入实体提取
    if is_logic_command(s):
        return _has_translatable_cmd_text(s)
    return True

def should_extract_dp(value):
    s = value.strip()
    if not s or not has_translatable_text(s) or is_namespace_id(s) or s.lower() in MC_RESERVED_WORDS: return False
    # 【重要修改】删除了 INTERNAL_TAG_RE 判断，只要它是文本，哪怕是纯小写单词也必须抓！
    if UUID_RE.match(s) or TRANSLATION_KEY_RE.match(s): return False
    return True

def _strip_json_text(val):
    v = val.strip()
    if v.startswith("{") and v.endswith("}"):
        try:
            obj = json.loads(v)
            if isinstance(obj, dict) and isinstance(obj.get("text"), str): return obj["text"]
        except Exception: pass
    return val

def _merge_group(strings, pattern, out_suffix, sep="\n"):
    groups = defaultdict(dict)
    for k in list(strings.keys()):
        m = pattern.match(k)
        if m:
            parent = m.group(1) or ""
            try:
                idx = int(m.group(2))
                groups[parent][idx] = k
            except ValueError: pass
    for parent, idx_map in groups.items():
        if not idx_map: continue
        max_i = max(idx_map.keys())
        lines = [_strip_json_text(strings[idx_map[i]]) if i in idx_map else "" for i in range(max_i + 1)]
        while lines and not lines[-1].strip(): lines.pop()
        if lines and any(l.strip() for l in lines):
            merged_key = f"{parent}.{out_suffix}" if parent else out_suffix
            strings[merged_key] = sep.join(lines)
        for k in idx_map.values(): strings.pop(k, None)

def extract_mca_entities(chunk_root, mode):
    results = []
    def process(arr, root_path):
        if not isinstance(arr, (list, NBTList)): return
        for ent in arr:
            if not isinstance(ent, dict): continue
            strings = {}
            walk_strings(ent, "", strings)

            # 【双重记录】messages[] 的原始值（用于写回时保留 JSON 结构）
            msg_orig = {}
            for k, v in list(strings.items()):
                m_msg = re.match(r"^(?:(.*)\.)?messages\[(\d+)\]$", k)
                if not m_msg: continue
                _p = (m_msg.group(1) or "").rstrip(".")
                try:
                    _i = int(m_msg.group(2))
                except ValueError:
                    continue
                msg_orig.setdefault(_p, {})[_i] = v

            # 【双重记录】提取时，同时记录原始行文本(用于补空行)和格式(用于颜色)
            lore_orig_lines = {}
            lore_formats = {}
            for k, v in list(strings.items()):
                m = re.match(r"^(?:(.*)\.)?(?:Lore|lore)\[(\d+)\](?:\.text)?$", k)
                if not m: continue
                parent = (m.group(1) or "").rstrip(".")
                try:
                    idx = int(m.group(2))
                except ValueError:
                    continue
                
                lore_orig_lines.setdefault(parent, {})[idx] = _strip_json_text(v)
                
                try:
                    obj = json.loads(v)
                    if isinstance(obj, dict):
                        fmt = {}
                        if isinstance(obj.get("color"), str): fmt["color"] = obj["color"]
                        if obj.get("bold"): fmt["bold"] = True
                        if obj.get("italic"): fmt["italic"] = True
                        lore_formats.setdefault(parent, {})[idx] = fmt  # 👈 注意这里，改成用字典存
                except Exception:
                    pass

            _merge_group(strings, re.compile(r"^(?:(.*)\.)?Text([1-4])$"), MERGE_SIGN_T1)
            _merge_group(strings, re.compile(r"^(?:(.*)\.)?messages\[(\d+)\]$"), MERGE_SIGN_MSG)
            _merge_group(strings, re.compile(r"^(?:(.*)\.)?pages\[(\d+)\]$"), MERGE_BOOK, sep="\n===PAGE_BREAK===\n")
            _merge_group(strings, re.compile(r"^(?:(.*)\.)?(?:Lore|lore)\[(\d+)\](?:\.text)?$"), MERGE_LORE)

            filtered = {}
            for k, v in strings.items():
                keep = (mode == "raw") or (mode == "light" and should_extract_light(k, v)) or (mode == "full" and should_extract_full(k, v))
                if keep: filtered[k] = v
            if not filtered: continue

            entry = {"Root": root_path, "PATH": filtered}

            # 组装 LORE_ORIG 和 FORMATS（保证严格对齐）
            lore_orig_dict = {}
            formats_dict = {}
            
            for parent, idx_map in lore_orig_lines.items():
                max_i = max(idx_map.keys())
                lines = [idx_map.get(i, "") for i in range(max_i + 1)]
                
                # 剔除尾部空行，并同步调整 max_i
                while lines and not lines[-1].strip():
                    lines.pop()
                    max_i -= 1
                    
                # 获取颜色映射，并对齐长度
                fmt_map = lore_formats.get(parent, {})
                fmt_list = [fmt_map.get(i, {}) for i in range(max_i + 1)]
                
                merge_key = f"{parent}.{MERGE_LORE}" if parent else MERGE_LORE
                if merge_key in filtered:
                    lore_orig_dict[merge_key] = lines
                    formats_dict[merge_key] = fmt_list
                    
            if lore_orig_dict:
                entry["LORE_ORIG"] = lore_orig_dict
            if formats_dict:
                entry["FORMATS"] = formats_dict

            # 【新增】messages 原始结构（用于写回时保留 JSON 组件字段）
            if msg_orig:
                _msg_dict = {}
                for _p, _idx_map in msg_orig.items():
                    _max_i = max(_idx_map.keys())
                    _raw_list = [_idx_map.get(_i, "") for _i in range(_max_i + 1)]
                    _merge_key = f"{_p}.{MERGE_SIGN_MSG}" if _p else MERGE_SIGN_MSG
                    if _merge_key in filtered:
                        _msg_dict[_merge_key] = _raw_list
                if _msg_dict:
                    entry["MSG_ORIG"] = _msg_dict

            if "UUID" in ent:
                try:
                    ints = [int(x) for x in ent["UUID"]]
                    entry["UUID"] = b"".join(struct.pack(">i", x) for x in ints).hex()
                except Exception: pass
            elif "UUIDMost" in ent and "UUIDLeast" in ent:
                try: entry["UUID"] = struct.pack(">q", int(ent["UUIDMost"])).hex() + struct.pack(">q", int(ent["UUIDLeast"])).hex()
                except Exception: pass
            if "x" in ent and "y" in ent and "z" in ent:
                try: entry["POS"] = [int(ent["x"]), int(ent["y"]), int(ent["z"])]
                except Exception: pass
            results.append(entry)

    level = chunk_root.get("Level")
    if level is not None:
        process(level.get("TileEntities"), "Level.TileEntities")
        process(level.get("Entities"),     "Level.Entities")
    process(chunk_root.get("block_entities"), "block_entities")
    process(chunk_root.get("Entities"),       "Entities")
    return results

def scan_mca_dir(dir_path, dir_name, mode, progress_callback=None):
    result = []
    mca_files = sorted(dir_path.glob("r.*.mca"))
    total = len(mca_files)
    print(f"\n[{dir_name}] 共 {total} 个 .mca")
    for i, mca in enumerate(mca_files):
        print(f"  读取 {mca.name} ...")
        if progress_callback:
            try: progress_callback(i + 1, total, mca.name)
            except Exception: pass
        raw_chunks = read_mca(mca)
        chunk_entries = []
        for idx in sorted(raw_chunks):
            try: root = parse_chunk_nbt(raw_chunks[idx])
            except Exception as e: continue
            ents = extract_mca_entities(root, mode)
            if ents: chunk_entries.append({"X": idx % 32, "Z": idx // 32, "Data": ents})
        if chunk_entries: result.append({"FilePath": f"{dir_name}/{mca.name}", "Chunk": chunk_entries})
    return result

TEXT_FIELD_RE = re.compile(r'"text"\s*:\s*"((?:[^"\\]|\\.)*)"')
def decode_escaped(s):
    try: return json.loads('"' + s + '"')
    except Exception: return s
def encode_escaped(s): return json.dumps(s, ensure_ascii=False)[1:-1]

def scan_mcfunction(path):
    try: 
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except Exception: 
        return []
    
    hits = []
    for i, line in enumerate(lines):
        # ---------------------------------------------------------
        # 策略1：精准结构化解析（解决 tellraw/title 等复杂 JSON）
        # ---------------------------------------------------------
        json_match = re.search(r'(\[.*\]|\{.*\})\s*$', line.strip())
        if json_match:
            json_str = json_match.group(1)
            try:
                parsed = json.loads(json_str)
                texts = _collect_all_texts(parsed) 
                if texts:
                    start_idx = line.find(json_str)
                    end_idx = start_idx + len(json_str)
                    combined_text = "\n".join(texts)
                    hits.append((i, start_idx, end_idx, combined_text))
                    continue # 解析成功，直接跳到下一行
            except json.JSONDecodeError:
                pass # 解析失败，转交策略2

        # ---------------------------------------------------------
        # 策略2：正则兜底解析（抓取带有 "text": 的文本）
        # ---------------------------------------------------------
        for m in TEXT_FIELD_RE.finditer(line):
            d = decode_escaped(m.group(1))
            if should_extract_dp(d):
                hits.append((i, m.start(1), m.end(1), d))
                
        # 补充正则：某些模组的 title 指令或 bossbar 可能不带 "text": 
        if not hits or hits[-1][0] != i:
            title_match = re.search(r'(?:title|subtitle|actionbar)\s+@[aeprs]+\s+"([^"]+)"', line)
            if title_match and should_extract_dp(title_match.group(1)):
                hits.append((i, title_match.start(1), title_match.end(1), title_match.group(1)))
            
            bossbar_match = re.search(r'bossbar\s+.*?name\s+"([^"]+)"', line)
            if bossbar_match and should_extract_dp(bossbar_match.group(1)):
                hits.append((i, bossbar_match.start(1), bossbar_match.end(1), bossbar_match.group(1)))

        # ---------------------------------------------------------
        # 策略3：纯文本输出指令（解决 /say 或 /tell 后面不加引号的裸文本）
        # ---------------------------------------------------------
        if not hits or hits[-1][0] != i:
            line_stripped = line.strip()
            # 去掉开头的斜杠
            body = line_stripped[1:] if line_stripped.startswith("/") else line_stripped
            parts = body.split(None, 1) # 只切分第一次
            
            if parts:
                cmd = parts[0].lower()
                target_text = None
                
                # /say 和 /me 后面全是文本
                if cmd in ("say", "me") and len(parts) == 2:
                    target_text = parts[1].strip()
                # /tell、/msg 等需要剥离目标选择器
                elif cmd in ("tell", "msg", "tm") and len(parts) == 2:
                    sub_parts = parts[1].split(None, 1)
                    if len(sub_parts) == 2:
                        target_text = sub_parts[1].strip()
                
                if target_text:
                    if not target_text.startswith(("{", "[", "\"", "'")) and should_extract_dp(target_text):
                        start_idx = line.find(target_text)
                        if start_idx != -1:
                            end_idx = start_idx + len(target_text)
                            hits.append((i, start_idx, end_idx, target_text))

    return hits

TRANSLATABLE_JSON_KEYS = {"text", "title", "description", "fallback", "subtitle", "name", "lore", "value", "display_name", "item_name", "custom_name"}
def is_lang_file(path): return "lang" in [p.lower() for p in path.parts]
def walk_json(obj, path, out):
    if isinstance(obj, str): out.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items(): walk_json(v, path + (k,), out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj): walk_json(v, path + (i,), out)

def scan_json_dp(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        obj = json.loads(text)
    except Exception: return []
    is_lang = is_lang_file(path)
    items = []
    walk_json(obj, (), items)
    hits = []
    for p, v in items:
        if not isinstance(v, str) or not v.strip(): continue
        if is_lang:
            if p and isinstance(p[-1], str) and p[-1].startswith("_"): continue
            if should_extract_dp(v): hits.append((p, v))
        else:
            if not p or not isinstance(p[-1], str) or p[-1] not in TRANSLATABLE_JSON_KEYS: continue
            if should_extract_dp(v): hits.append((p, v))
    return hits

def set_json_by_path(root, path_tuple, value):
    cur = root
    for t in path_tuple[:-1]: cur = cur[t]
    cur[path_tuple[-1]] = value

def collect_datapack_files():
    dp_dir = BASE_DIR / "datapacks"
    mcfuncs, jsons = [], []
    if not dp_dir.is_dir(): return mcfuncs, jsons
    for f in dp_dir.rglob("*"):
        if not f.is_file(): continue
        low = f.name.lower()
        if low.endswith(".mcfunction"): mcfuncs.append(f)
        elif low.endswith(".json"): jsons.append(f)
    return sorted(mcfuncs), sorted(jsons)

def load_data_json():
    empty = {"MCARegions": [], "MCEntities": []}
    if not DATA_JSON.is_file(): return empty
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return empty
def _atomic_save_json(path, data):
    """原子写入 JSON：先写 .tmp，再 os.replace 覆盖。失败时清理 .tmp，不损坏原文件。"""
    path_str = str(path)
    temp_path = path_str + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path_str)
    except Exception:
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except Exception: pass
        raise

def _atomic_write_text(path, text):
    """原子写入文本文件：先写 .tmp，再 os.replace 覆盖。"""
    path_str = str(path)
    temp_path = path_str + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path_str)
    except Exception:
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except Exception: pass
        raise

def save_data_json(data):
    _atomic_save_json(DATA_JSON, data)

def save_dp_data_json(data):
    _atomic_save_json(DP_DATA_JSON, data)

def unpack_datapacks(dp_dir):
    global UNZIPPED_RECORDS
    UNZIPPED_RECORDS.clear() 
    dp_path = Path(dp_dir)
    if not dp_path.exists(): return
    for file in dp_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".zip":
            extract_dir = dp_path / (file.stem + "_unzip")
            print(f"  [自动解压] {file.name} -> {extract_dir.name}/")
            with zipfile.ZipFile(file, 'r') as zip_ref: zip_ref.extractall(extract_dir)
            UNZIPPED_RECORDS.append((file, extract_dir))

def repack_datapacks():
    global UNZIPPED_RECORDS
    dp_path = BASE_DIR / "datapacks"
    if not dp_path.exists(): return
    for original_zip, extract_dir in UNZIPPED_RECORDS:
        _do_repack(original_zip, extract_dir)
    UNZIPPED_RECORDS.clear()
    for d in dp_path.iterdir():
        if d.is_dir() and d.name.endswith("_unzip"):
            zip_name = d.name[:-6] + ".zip"
            original_zip = dp_path / zip_name
            _do_repack(original_zip, d)

def _do_repack(original_zip, extract_dir):
    if not extract_dir.exists(): return
    print(f"  [重新打包] {extract_dir.name}/ -> {original_zip.name}")
    tmp_zip = str(original_zip) + ".tmp"
    try:
        with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, file_path.relative_to(extract_dir))
        os.replace(tmp_zip, str(original_zip))
        shutil.rmtree(extract_dir)
        print(f"  [清理完毕] {extract_dir.name}/ 已自动删除。")
    except Exception as e:
        if os.path.exists(tmp_zip):
            try: os.remove(tmp_zip)
            except Exception: pass
        print(f"  ❌ [错误] 打包失败（原 zip 未受影响）: {e}")

def smart_wrap_sign_text(text, max_lines=4, max_width=15):
    if not text: return []
    def width(s): return sum(2 if ord(c) > 127 else 1 for c in s)
    if "\n" in text:
        lines = text.split("\n")
        while lines and not lines[-1].strip(): lines.pop()
        return lines[:max_lines]
    parts = re.split(r'([，。！？,.!?；;：:])', text)
    chunks = [parts[i] + parts[i+1] for i in range(0, len(parts)-1, 2)] + ([parts[-1]] if len(parts)%2!=0 and parts[-1] else [])
    lines, current = [], ""
    for chunk in chunks:
        if not chunk: continue
        if width(current + chunk) <= max_width: current += chunk
        else:
            if current: lines.append(current)
            if width(chunk) > max_width:
                temp = ""
                for ch in chunk:
                    if width(temp + ch) > max_width: lines.append(temp); temp = ch
                    else: temp += ch
                current = temp
            else: current = chunk
    if current: lines.append(current)
    if len(lines) > max_lines: lines = lines[:max_lines-1] + ["".join(lines[max_lines-1:])]
    return lines

def _make_comp(text): return json.dumps({"text": text}, ensure_ascii=False, separators=(",", ":"))

def _rebuild_msg_component(text, raw_orig):
    """把译文填回原始 JSON 组件，保留除 text 外的所有字段（color/clickEvent/hoverEvent 等）。
    如果原始不是 JSON 组件（纯文本/空/非 dict），返回纯文本 text，行为与旧版一致。"""
    if not raw_orig or not raw_orig.strip():
        return text
    raw = raw_orig.strip()
    if not (raw.startswith("{") and raw.endswith("}")):
        return text
    try:
        obj = json.loads(raw)
    except Exception:
        return text
    if not isinstance(obj, dict):
        return text
    new_obj = dict(obj)
    new_obj["text"] = text
    return json.dumps(new_obj, ensure_ascii=False, separators=(",", ":"))


# ==========================================
# API 配置管理（config.json）
# ==========================================
CONFIG_FILE = BASE_DIR / "config.json"


def load_api_config():
    if not CONFIG_FILE.is_file():
        return {"active": "", "profiles": {}}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"active": "", "profiles": {}}
        if not isinstance(data.get("profiles"), dict):
            data["profiles"] = {}
        if not isinstance(data.get("active"), str):
            data["active"] = ""
        return data
    except Exception:
        return {"active": "", "profiles": {}}

def save_api_config(cfg):
    try:
        if "_atomic_save_json" in globals():
            _atomic_save_json(CONFIG_FILE, cfg)
            return
    except Exception:
        pass
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def api_profile_names():
    try:
        return sorted(load_api_config().get("profiles", {}).keys())
    except Exception:
        return []

def api_profile_get(name):
    try:
        return load_api_config().get("profiles", {}).get(name)
    except Exception:
        return None

def api_profile_active_name():
    try:
        return load_api_config().get("active", "")
    except Exception:
        return ""

def api_profile_set_active(name):
    cfg = load_api_config()
    if name in cfg.get("profiles", {}):
        cfg["active"] = name
        save_api_config(cfg)

def api_profile_upsert(name, engine, key):
    cfg = load_api_config()
    cfg.setdefault("profiles", {})[name] = {"engine": engine, "key": key}
    cfg["active"] = name
    save_api_config(cfg)

def api_profile_delete(name):
    cfg = load_api_config()
    if name in cfg.get("profiles", {}):
        del cfg["profiles"][name]
    if cfg.get("active") == name:
        cfg["active"] = ""
    save_api_config(cfg)


# ==========================================
# 翻译引擎
# ==========================================
PH_L = "\uE000"
PH_R = "\uE001"
PROTECT_PATTERNS = [
    re.compile(r"§[0-9a-fk-or]"),
    re.compile(r"\\n|\\r|\\t"),
    re.compile(r"%(\d+\$)?[sdif]"),
    re.compile(r"\{[a-zA-Z_][a-zA-Z0-9_]*\}"),
    re.compile(r"\[\[.*?\]\]"),
    re.compile(r"\$\([a-zA-Z_][a-zA-Z0-9_]*\)"),
    # 【新增】保护命名空间 ID，例如 minecraft:diamond_sword 或 custom:magic
    re.compile(r"\b[a-zA-Z0-9_]+:[a-zA-Z0-9_/\.\-\+]+\b")
]

def _protect(text):
    tokens = []
    def repl(m):
        tokens.append(m.group(0))
        return f"{PH_L}{len(tokens)-1:03d}{PH_R}"
    for pat in PROTECT_PATTERNS: text = pat.sub(repl, text)
    return text, tokens

def _restore(text, tokens):
    for i, tok in enumerate(tokens): text = text.replace(f"{PH_L}{i:03d}{PH_R}", tok)
    return text

def _should_skip(text):
    if not text or not text.strip(): return True
    if re.fullmatch(r"[\s§0-9a-fk-or]*", text): return True
    if re.fullmatch(r"[\d\s\.\,\-\+\:]+", text): return True
    
    # 【新增】跳过纯指令
    s = text.strip()
    if s.startswith("/"): return True
    # 匹配常见无斜杠的指令开头
    if re.match(r"^(?:give|execute|summon|setblock|fill|data|scoreboard|tp|teleport|function|advancement|item|effect|enchant|say|tellraw|title|subtitle|actionbar|me|msg|tell|kill|clear|xp|experience|gamerule|time|weather|spawnpoint|setworldspawn|playsound|particle)\s", s, re.IGNORECASE):
        return True
        
    return False

class GoogleEngine:
    def __init__(self, source, target):
        from deep_translator import GoogleTranslator
        self.t = GoogleTranslator(source=source, target=target)
    def translate(self, text): return self.t.translate(text)

class DeepLEngine:
    def __init__(self, source, target, api_key):
        import deepl
        self.t = deepl.Translator(api_key)
        self.source = source.upper()
        self.target = "ZH" if target.lower().startswith("zh") else target.upper()
    def translate(self, text):
        return self.t.translate_text(text, source_lang=self.source, target_lang=self.target).text

class DeepSeekEngine:
    def __init__(self, source, target, api_key, model="deepseek-chat", base_url="https://api.deepseek.com"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.base_url = base_url
        self._fallback_tried = False
        self.hint = f"Source language: {source}, Target language: {target}."
        self.prompt = "You are a professional game localization translator. Translate into Simplified Chinese. Output ONLY translation. Preserve tokens like %s, § codes, {name}. Do not invent."
    def _call(self, text, model):
        resp = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": self.prompt + "\n" + self.hint}, {"role": "user", "content": text}],
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    def translate(self, text):
        try:
            return self._call(text, self.model)
        except Exception as e:
            err_str = str(e).lower()
            if (not self._fallback_tried
                and "openai.com" in self.base_url
                and ("model_not_found" in err_str or "does not exist" in err_str or "404" in err_str)
                and self.model != "gpt-4o-mini"):
                self.model = "gpt-4o-mini"
                self._fallback_tried = True
                return self._call(text, self.model)
            raise

class BaiduEngine:
    def __init__(self, source, target, appid, secret):
        self.appid, self.secret = appid, secret
        self.source = source
        self.target = "zh" if target.lower().startswith("zh") else target
    def translate(self, text):
        import hashlib, random, requests
        salt = str(random.randint(32768, 65536))
        sign = hashlib.md5((self.appid + text + salt + self.secret).encode("utf-8")).hexdigest()
        r = requests.get("https://fanyi-api.baidu.com/api/trans/vip/translate", params={"q": text, "from": self.source, "to": self.target, "appid": self.appid, "salt": salt, "sign": sign}, timeout=10)
        data = r.json()
        if "trans_result" in data: return data["trans_result"][0]["dst"]
        raise RuntimeError(f"百度翻译错误: {data}")

def _translate_one(text, engine, retry=3):
    if _should_skip(text): return text
    if "\n" in text: text = re.sub(r"\n+", " ", text).strip()
    protected, tokens = _protect(text)
    for attempt in range(retry):
        try:
            translated = engine.translate(protected)
            if translated:
                if translated.startswith('"') and translated.endswith('"'): translated = translated[1:-1]
                return _restore(translated, tokens)
        except Exception: time.sleep(1 + attempt)
    return text

# ==========================================
# GUI 界面
# ==========================================
class TextRedirector:
    def __init__(self, textbox): self.textbox = textbox
    def write(self, str):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", str)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
    def flush(self): pass

class ApiProfileManagerDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("🔑 API 配置管理")
        _w, _h = _fit_size(self, 640, 580)
        self.geometry(f"{_w}x{_h}")
        self.attributes("-topmost", True)
        self.configure(fg_color="#FFFFFF")
        try: apply_icon(self)
        except Exception: pass
        try:
            self.transient(parent)
            self.grab_set()
        except Exception: pass
        self.update_idletasks()
        self.geometry(f"+{parent.winfo_x() + (parent.winfo_width() - 640) // 2}+{parent.winfo_y() + (parent.winfo_height() - 580) // 2}")

        header = ctk.CTkFrame(self, fg_color="#F0F2F5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🔑 API 配置管理", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=20)
        ctk.CTkLabel(header, text="保存多套 Key，随时切换", font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(15, 5))

        ctk.CTkLabel(body, text="已保存配置", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(0, 5))

        list_frame = ctk.CTkFrame(body, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=6)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        try:
            style = ttk.Style(self)
            style.theme_use("clam")
        except Exception:
            style = ttk.Style(self)
        style.configure("Profile.Treeview",
                        background="#FFFFFF", fieldbackground="#FFFFFF",
                        foreground="#333333", rowheight=30, borderwidth=0,
                        font=("Microsoft YaHei", 11))
        style.configure("Profile.Treeview.Heading",
                        background="#F0F2F5", foreground="#333333",
                        font=("Microsoft YaHei", 11, "bold"), padding=(6, 6))

        self.tree = ttk.Treeview(list_frame, style="Profile.Treeview",
                                 columns=("engine", "key"), show="headings",
                                 height=8, selectmode="browse")
        self.tree.heading("engine", text="引擎")
        self.tree.heading("key", text="Key 摘要")
        self.tree.column("engine", width=160)
        self.tree.column("key", width=420)
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        edit_frame = ctk.CTkFrame(body, fg_color="#F0F2F5", corner_radius=8)
        edit_frame.pack(fill="x", pady=(0, 5))

        row1 = ctk.CTkFrame(edit_frame, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(12, 5))
        ctk.CTkLabel(row1, text="名称：", font=("Microsoft YaHei", 12), text_color="#333333", width=70, anchor="w").pack(side="left")
        self.name_entry = ctk.CTkEntry(row1, placeholder_text="如：DeepSeek 官方", font=("Microsoft YaHei", 12), height=32, border_color="#E0E0E0", fg_color="#FFFFFF")
        self.name_entry.pack(side="left", fill="x", expand=True)

        row2 = ctk.CTkFrame(edit_frame, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row2, text="引擎：", font=("Microsoft YaHei", 12), text_color="#333333", width=70, anchor="w").pack(side="left")
        self.engine_opt = ctk.CTkOptionMenu(row2, values=["Google 免费", "OpenAI (ChatGPT)", "DeepSeek", "通义千问", "Kimi", "智谱GLM", "硅基流动", "DeepL", "百度"],
                                            font=("Microsoft YaHei", 12), height=32,
                                            fg_color="#FFFFFF", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                            text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        self.engine_opt.pack(side="left", fill="x", expand=True)

        row3 = ctk.CTkFrame(edit_frame, fg_color="transparent")
        row3.pack(fill="x", padx=15, pady=(5, 12))
        ctk.CTkLabel(row3, text="Key：", font=("Microsoft YaHei", 12), text_color="#333333", width=70, anchor="w").pack(side="left")
        self.key_entry = ctk.CTkEntry(row3, placeholder_text="API Key / 百度 AppID,密钥", font=("Microsoft YaHei", 12), height=32, border_color="#E0E0E0", fg_color="#FFFFFF")
        self.key_entry.pack(side="left", fill="x", expand=True)

        btn_bar = ctk.CTkFrame(self, fg_color="#F0F2F5", height=70)
        btn_bar.pack(fill="x", side="bottom")
        btn_bar.pack_propagate(False)

        ctk.CTkButton(btn_bar, text="➕ 新增 / 更新", fg_color="#007ACC", hover_color="#005A9E",
                      font=("Microsoft YaHei", 13, "bold"), height=38, width=140,
                      command=self._save_current).pack(side="left", padx=(20, 5), pady=15)
        ctk.CTkButton(btn_bar, text="设为当前", fg_color="#E4E7ED", hover_color="#D0D0D0", text_color="#333333",
                      font=("Microsoft YaHei", 13, "bold"), height=38, width=100,
                      command=self._set_active).pack(side="left", padx=5, pady=15)
        ctk.CTkButton(btn_bar, text="删除", fg_color="#B84C3D", hover_color="#9B3A2E", text_color="#FFFFFF",
                      font=("Microsoft YaHei", 13, "bold"), height=38, width=80,
                      command=self._delete).pack(side="left", padx=5, pady=15)
        ctk.CTkButton(btn_bar, text="关闭", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 13, "bold"), height=38, width=80,
                      command=self.destroy).pack(side="right", padx=(5, 20), pady=15)

        self._refresh()

    def _refresh(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        names = api_profile_names()
        active = api_profile_active_name()
        for n in names:
            p = api_profile_get(n) or {}
            engine = p.get("engine", "?")
            key = p.get("key", "")
            if len(key) > 16:
                key_summary = key[:10] + "..." + key[-4:]
            else:
                key_summary = key
            mark = "  [当前]" if n == active else ""
            self.tree.insert("", "end", iid=n, values=(engine + mark, key_summary))

    def _on_select(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            return
        name = sel[0]
        p = api_profile_get(name) or {}
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, name)
        self.engine_opt.set(p.get("engine", "Google 免费"))
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, p.get("key", ""))

    def _save_current(self):
        name = self.name_entry.get().strip()
        engine = self.engine_opt.get()
        key = self.key_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请填写配置名称", parent=self)
            return
        if engine in ("DeepSeek", "DeepL", "OpenAI (ChatGPT)", "通义千问", "Kimi", "智谱GLM", "硅基流动") and not key:
            messagebox.showwarning("提示", f"{engine} 需要填 API Key", parent=self)
            return
        if engine == "百度" and "," not in key:
            messagebox.showwarning("提示", "百度需要填 AppID,密钥（英文逗号分隔）", parent=self)
            return
        api_profile_upsert(name, engine, key)
        self._refresh()
        try:
            for iid in self.tree.get_children():
                if iid == name:
                    self.tree.selection_set(iid)
                    break
        except Exception:
            pass

    def _set_active(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("提示", "请先选择一行", parent=self)
            return
        api_profile_set_active(sel[0])
        self._refresh()

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("提示", "请先选择一行", parent=self)
            return
        if not messagebox.askyesno("确认删除", f"确定删除配置「{sel[0]}」吗？", parent=self):
            return
        api_profile_delete(sel[0])
        self._refresh()

class LightThemeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # 确保工作目录存在，并清理上次崩溃残留的 .tmp 文件
        WORK_DIR.mkdir(exist_ok=True)
        for _sub in ("", "region", "entities", "datapacks", "LeafLingo_work"):
            _d = BASE_DIR / _sub if _sub else BASE_DIR
            if not _d.is_dir(): continue
            for _tmp in _d.rglob("*.tmp"):
                try: _tmp.unlink()
                except Exception: pass
        self.title("LeafLingo 地图汉化工具")
        apply_icon(self)
        
        _w, _h = _fit_size(self, 950, 700)
        self.geometry(f"{_w}x{_h}")
        self.configure(fg_color=C_BG)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_tab = "region"

        # 侧边栏
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#F0F2F5")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="LeafLingo 汉化", font=("Microsoft YaHei", 22, "bold"), text_color="#333333")
        self.logo.pack(pady=(30, 30), padx=20, anchor="w")

        nav_btn_kwargs = {"fg_color": "transparent", "text_color": "#555555", "hover_color": "#E4E7ED", "anchor": "w", "font": ("Microsoft YaHei", 14)}
        sub_btn_kwargs = {"fg_color": "transparent", "text_color": "#777777", "hover_color": "#E4E7ED", "anchor": "w", "font": ("Microsoft YaHei", 13)}
        
        # Tab 切换按钮
        self.btn_tab_region = ctk.CTkButton(self.sidebar, text="▶ 地图与实体 (Region)", command=lambda: self.switch_tab("region"), **nav_btn_kwargs)
        self.btn_tab_region.pack(pady=5, padx=15, fill="x")
        
        self.btn_tab_dp = ctk.CTkButton(self.sidebar, text="▶ 数据包 (Datapacks)", command=lambda: self.switch_tab("dp"), **nav_btn_kwargs)
        self.btn_tab_dp.pack(pady=5, padx=15, fill="x")

        # AI 翻译 (折叠菜单)
        self.is_ai_expanded = False
        self.nav_btn_ai = ctk.CTkButton(self.sidebar, text="▶ 🚀 应用 AI 翻译", command=self.toggle_ai_menu, **nav_btn_kwargs)
        self.nav_btn_ai.pack(pady=5, padx=15, fill="x")
        
        self.ai_menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctk.CTkButton(self.ai_menu_frame, text="API 翻译 lang.json", command=lambda: self.open_api_dialog(str(LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")
        ctk.CTkButton(self.ai_menu_frame, text="API 翻译 dp_lang.json", command=lambda: self.open_api_dialog(str(DP_LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")
        ctk.CTkButton(self.ai_menu_frame, text="应用 AI 翻译结果", command=self.open_code_runner, **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")

        # 翻译查漏 (折叠菜单)
        self.is_check_expanded = False
        self.nav_btn_check = ctk.CTkButton(self.sidebar, text="▶ 🔍 翻译查漏", command=self.toggle_check_menu, **nav_btn_kwargs)
        self.nav_btn_check.pack(pady=5, padx=15, fill="x")
        
        self.check_menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctk.CTkButton(self.check_menu_frame, text="查漏 lang.json", command=lambda: self.check_missing(str(LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")
        ctk.CTkButton(self.check_menu_frame, text="查漏 dp_lang.json", command=lambda: self.check_missing(str(DP_LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")

        # 手动翻译 (折叠菜单)
        self.is_manual_expanded = False
        self.nav_btn_manual = ctk.CTkButton(self.sidebar, text="▶ 📝 手动翻译", command=self.toggle_manual_menu, **nav_btn_kwargs)
        self.nav_btn_manual.pack(pady=5, padx=15, fill="x")
        
        self.manual_menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctk.CTkButton(self.manual_menu_frame, text="翻译 lang.json", command=lambda: self.open_manual_translator(str(LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")
        ctk.CTkButton(self.manual_menu_frame, text="翻译 dp_lang.json", command=lambda: self.open_manual_translator(str(DP_LANG_JSON)), **sub_btn_kwargs).pack(pady=2, padx=(30, 15), fill="x")

        self.btn_tutorial = ctk.CTkButton(self.sidebar, text="📖 使用教程", command=self.open_tutorial, fg_color="#E4E7ED", text_color="#333333", hover_color="#D0D0D0", font=("Microsoft YaHei", 14, "bold"))
        self.btn_tutorial.pack(side="bottom", pady=(0, 20), padx=15, fill="x")

        self.btn_clean_work = ctk.CTkButton(self.sidebar, text="🧹 清理工作目录", command=self.clean_work_dir, fg_color="#E4E7ED", text_color="#333333", hover_color="#D0D0D0", font=("Microsoft YaHei", 14, "bold"))
        self.btn_clean_work.pack(side="bottom", pady=(5, 0), padx=15, fill="x")

        # 右侧主区域
        self.main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="操作面板 - 地图与实体", font=("Microsoft YaHei", 24, "bold"), text_color="#222222")
        self.title_label.pack(anchor="w", pady=(0, 5))
        
        self.sub_title = ctk.CTkLabel(self.main_frame, text="请按顺序执行下方 1~4 步操作", font=("Microsoft YaHei", 13), text_color="#888888")
        self.sub_title.pack(anchor="w", pady=(0, 20))

        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x")

        btn_kwargs = {"height": 42, "fg_color": "#F7F8FA", "text_color": "#333333", "hover_color": "#E4E7ED", "border_width": 1, "border_color": "#E0E0E0", "font": ("Microsoft YaHei", 14)}
        
        self.action_btns = []
        btn_texts = ["1. 提取文本", "2. 生成 Lang", "3. 合并回 Data", "4. 写回"]
        for i, text in enumerate(btn_texts):
            btn = ctk.CTkButton(self.btn_frame, text=text, command=lambda s=i+1: self.run_action(s), **btn_kwargs)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.btn_frame.grid_columnconfigure(i, weight=1)
            self.action_btns.append(btn)

        # 进度状态栏（供扫描 / 翻译使用）
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.status_frame.pack(fill="x", pady=(15, 0))
        self.status_label = ctk.CTkLabel(self.status_frame, text="就绪", font=("Microsoft YaHei", 12), text_color="#888888")
        self.status_label.pack(side="left")
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, height=10, progress_color="#888888", fg_color="#E0E0E0", corner_radius=0, width=280)
        self.progress_bar.pack(side="right", padx=(15, 0))
        self.progress_bar.set(0)

        self.log_label = ctk.CTkLabel(self.main_frame, text="运行日志", font=("Microsoft YaHei", 14, "bold"), text_color="#333333")
        self.log_label.pack(anchor="w", pady=(20, 5))
        
        self.log_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13), fg_color="#FAFAFA", text_color="#444444", border_color="#E0E0E0", border_width=1, corner_radius=8)
        self.log_box.pack(fill="both", expand=True, pady=(0, 10))
        
        self.switch_tab("region")
        sys.stdout = TextRedirector(self.log_box)
        self.log_msg(">>> 系统就绪。请点击左下角【使用教程】了解详细流程。")

    def switch_tab(self, tab):
        self.current_tab = tab
        if tab == "region":
            self.btn_tab_region.configure(fg_color="#E4E7ED")
            self.btn_tab_dp.configure(fg_color="transparent")
            self.title_label.configure(text="操作面板 - 地图与实体")
            self.action_btns[1].configure(text="2. 生成 Lang")
            self.action_btns[2].configure(text="3. 合并回 Data")
        else:
            self.btn_tab_region.configure(fg_color="transparent")
            self.btn_tab_dp.configure(fg_color="#E4E7ED")
            self.title_label.configure(text="操作面板 - 数据包 (Datapacks)")
            self.action_btns[1].configure(text="2. 生成 DpLang")
            self.action_btns[2].configure(text="3. 合并回 DpData")

    def run_action(self, step):
        if self.current_tab == "region":
            if step == 1: self.run_extract_region()
            elif step == 2: self.run_region_to_lang()
            elif step == 3: self.run_region_to_data()
            elif step == 4: self.run_apply_region()
        else:
            if step == 1: self.run_extract_datapacks()
            elif step == 2: self.run_dp_to_lang()
            elif step == 3: self.run_dp_to_data()
            elif step == 4: self.run_apply_datapacks()

    def log_msg(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def toggle_ai_menu(self):
        if self.is_ai_expanded:
            self.ai_menu_frame.pack_forget(); self.nav_btn_ai.configure(text="▶ 🚀 应用 AI 翻译"); self.is_ai_expanded = False
        else:
            self.ai_menu_frame.pack(after=self.nav_btn_ai, fill="x", pady=(0, 5)); self.nav_btn_ai.configure(text="▼ 🚀 应用 AI 翻译"); self.is_ai_expanded = True

    def toggle_check_menu(self):
        if self.is_check_expanded:
            self.check_menu_frame.pack_forget(); self.nav_btn_check.configure(text="▶ 🔍 翻译查漏"); self.is_check_expanded = False
        else:
            self.check_menu_frame.pack(after=self.nav_btn_check, fill="x", pady=(0, 5)); self.nav_btn_check.configure(text="▼ 🔍 翻译查漏"); self.is_check_expanded = True

    def toggle_manual_menu(self):
        if self.is_manual_expanded:
            self.manual_menu_frame.pack_forget(); self.nav_btn_manual.configure(text="▶ 📝 手动翻译"); self.is_manual_expanded = False
        else:
            self.manual_menu_frame.pack(after=self.nav_btn_manual, fill="x", pady=(0, 5)); self.nav_btn_manual.configure(text="▼ 📝 手动翻译"); self.is_manual_expanded = True

    # --- 核心操作 (地图) ---
    def run_extract_region(self):
        def task():
            if not (BASE_DIR / "level.dat").is_file() and not (BASE_DIR / "region").is_dir():
                self.log_msg("❌ 错误：当前目录不是地图存档根目录！"); return
            data = load_data_json()
            def _prog(done, total, name):
                pct = done / total if total else 0
                self.after(0, lambda: self.progress_bar.set(pct))
                self.after(0, lambda: self.status_label.configure(text=f"正在扫描 {name}（{done}/{total}）"))
            self.after(0, lambda: self.progress_bar.set(0))
            region_dir = BASE_DIR / "region"
            if region_dir.is_dir(): data["MCARegions"] = scan_mca_dir(region_dir, "region", "full", progress_callback=_prog)
            else: data["MCARegions"] = []
            entities_dir = BASE_DIR / "entities"
            if entities_dir.is_dir(): data["MCEntities"] = scan_mca_dir(entities_dir, "entities", "light", progress_callback=_prog)
            else: data["MCEntities"] = []
            self.after(0, lambda: self.progress_bar.set(1.0))
            
            save_data_json(data)
            
            # 【优化】只有当备份文件不存在时，才写入。保护最原始的数据不被覆盖
            if not DATA_ORIG_JSON.is_file():
                _atomic_save_json(DATA_ORIG_JSON, data)
                    
            self.log_msg("✓ 提取地图文本完成！")
        threading.Thread(target=task).start()

    def run_region_to_lang(self):
        def task():
            if not DATA_JSON.is_file(): return self.log_msg("❌ 找不到 data.json")
            with open(DATA_JSON, "r", encoding="utf-8") as f: data = json.load(f)
            texts = []
            for r in data.get("MCARegions", []):
                for c in r["Chunk"]:
                    for e in c["Data"]: texts.extend(e["PATH"].values())
            for r in data.get("MCEntities", []):
                for c in r["Chunk"]:
                    for e in c["Data"]: texts.extend(e["PATH"].values())
            seen = {}
            for t in texts:
                # 【修复】拦截以 eyJ 开头的 Base64 乱码（头颅皮肤数据），直接跳过
                if _is_base64_blob(t): continue
                if t not in seen: seen[t] = sha256(t.encode("utf-8")).hexdigest()
            result = [{"SHA256": h, "TEXT": t} for t, h in seen.items()]
            _atomic_save_json(LANG_JSON, result)
            self.log_msg(f"✓ 生成 {len(result)} 条唯一文本 -> lang.json")
        threading.Thread(target=task).start()

    def run_region_to_data(self):
        def task():
            src = DATA_ORIG_JSON if DATA_ORIG_JSON.is_file() else DATA_JSON
            if not src.is_file() or not LANG_JSON.is_file(): return self.log_msg("❌ 找不到需要合并的 JSON 文件！")
            with open(src, "r", encoding="utf-8") as f: data = json.load(f)
            with open(LANG_JSON, "r", encoding="utf-8") as f: lang = json.load(f)
            h2t = {i["SHA256"]: i["TEXT"] for i in lang}
            changed = 0
            
            def map_text(v):
                nonlocal changed
                h = sha256(v.encode("utf-8")).hexdigest()
                if h in h2t and h2t[h] != v: changed += 1; return h2t[h]
                return v

            def process_entities(regions):
                for r in regions:
                    for c in r["Chunk"]:
                        for e in c["Data"]:
                            new_path = {}
                            for p, v in e["PATH"].items():
                                new_v = map_text(v)
                                if p.endswith(MERGE_SIGN_T1):
                                    parent = p[:-len(MERGE_SIGN_T1)].rstrip(".")
                                    lines = smart_wrap_sign_text(new_v)
                                    for i in range(4): new_path[f"{parent}.Text{i+1}" if parent else f"Text{i+1}"] = lines[i] if i < len(lines) else ""
                                elif p.endswith(MERGE_SIGN_MSG):
                                    parent = p[:-len(MERGE_SIGN_MSG)].rstrip(".")
                                    orig_msgs = e.get("MSG_ORIG", {}).get(p, [])
                                    lines = smart_wrap_sign_text(new_v)
                                    for i in range(4):
                                        _line = lines[i] if i < len(lines) else ""
                                        _raw = orig_msgs[i] if i < len(orig_msgs) else ""
                                        new_path[f"{parent}.messages[{i}]" if parent else f"messages[{i}]"] = _rebuild_msg_component(_line, _raw)
                                elif p.endswith(MERGE_BOOK):
                                    parent = p[:-len(MERGE_BOOK)].rstrip(".")
                                    for i, page in enumerate(new_v.split("\n===PAGE_BREAK===\n")): new_path[f"{parent}.pages[{i}]" if parent else f"pages[{i}]"] = _make_comp(page)
                                elif p.endswith(MERGE_LORE):
                                    parent = p[:-len(MERGE_LORE)].rstrip(".")
                                    orig_lines = e.get("LORE_ORIG", {}).get(p, [])
                                    fmt_list = e.get("FORMATS", {}).get(p, [])
                                    user_lines = new_v.split("\n") if new_v else []

                                    user_has_blank = any(not l.strip() for l in user_lines)
                                    orig_has_blank = any(not l.strip() for l in orig_lines)

                                    # 1. 先处理空行对齐
                                    if orig_has_blank and not user_has_blank:
                                        result_lines = []
                                        user_idx = 0
                                        for orig_line in orig_lines:
                                            if not orig_line.strip():
                                                result_lines.append(orig_line)
                                            else:
                                                if user_idx < len(user_lines):
                                                    result_lines.append(user_lines[user_idx])
                                                    user_idx += 1
                                                else:
                                                    result_lines.append("")
                                        while user_idx < len(user_lines):
                                            result_lines.append(user_lines[user_idx])
                                            user_idx += 1
                                    else:
                                        result_lines = user_lines

                                    # 2. 再处理颜色回填
                                    for i, line in enumerate(result_lines):
                                        comp = {"text": line}
                                        if i < len(fmt_list):
                                            comp.update(fmt_list[i])
                                        new_path[f"{parent}.Lore[{i}]" if parent else f"Lore[{i}]"] = json.dumps(
                                            comp, ensure_ascii=False, separators=(",", ":")
                                        )
                                else:
                                    # 如果是 JSON 字符串，统一压紧格式去掉空格
                                    final_v = new_v
                                    if isinstance(new_v, str) and (new_v.startswith("{") or new_v.startswith("[")):
                                        try:
                                            parsed = json.loads(new_v)
                                            final_v = json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
                                        except Exception:
                                            pass
                                    new_path[p] = final_v
                            e["PATH"] = new_path

            process_entities(data.get("MCARegions", []))
            process_entities(data.get("MCEntities", []))
            save_data_json(data)
            self.log_msg(f"✓ 成功替换 {changed} 条数据到 data.json！")
        threading.Thread(target=task).start()

    def run_apply_region(self):
        def task():
            if not DATA_JSON.is_file(): return self.log_msg("❌ 找不到 data.json")
            with open(DATA_JSON, "r", encoding="utf-8") as f: data = json.load(f)
            if not data.get("MCARegions") and not data.get("MCEntities"): return self.log_msg("❌ 数据为空。")
            
            if not WORLD_BACKUP.exists():
                self.log_msg(f"正在备份整个存档到 {WORLD_BACKUP.name}...")
                shutil.copytree(BASE_DIR, WORLD_BACKUP)

            # 【进度条】按 .mca 文件数计算进度
            _total_mca = len(data.get("MCARegions", [])) + len(data.get("MCEntities", []))
            _done_mca = [0]
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self.status_label.configure(text=f"准备写回 {_total_mca} 个 .mca ..."))

            def _update_apply_progress(file_path):
                _done_mca[0] += 1
                pct = _done_mca[0] / _total_mca if _total_mca else 0
                _d = _done_mca[0]; _t = _total_mca; _f = file_path
                self.after(0, lambda: self.progress_bar.set(pct))
                self.after(0, lambda: self.status_label.configure(text=f"正在写回 {_d}/{_t}: {_f}"))

            def apply_mca(entries):
                for re in entries:
                    mca_path = BASE_DIR / re["FilePath"]
                    if not mca_path.is_file(): continue
                    
                    # 【优化】用 log_msg 替代 print，这样带有时间戳，且不会重复打印
                    self.log_msg(f"正在写回区块 {re['FilePath']} ...")
                    
                    # 【健壮性修复】逐块解析，单块失败时保留原始 raw bytes，
                    # 写回时原样填回，避免丢失未解析的区块。
                    raw_chunks = read_mca(mca_path)
                    nbt_chunks = {}
                    failed_raw = {}
                    for _idx, _raw in raw_chunks.items():
                        try:
                            nbt_chunks[_idx] = parse_chunk_nbt(_raw)
                        except Exception as _e:
                            failed_raw[_idx] = _raw
                            self.log_msg(f"  ⚠ 区块 {_idx} 解析失败，保留原始数据：{_e}")
                    for ce in re["Chunk"]:
                        root = nbt_chunks.get(ce["Z"] * 32 + ce["X"])
                        if root is None: continue
                        for ee in ce["Data"]:
                            arr = get_by_path(root, ee["Root"])
                            if not isinstance(arr, (list, NBTList)):
                                self.log_msg(f"  ⚠ 路径不存在或不是列表（Root={ee.get('Root', '?')}），已跳过")
                                continue
                            _entry_matched = False
                            for ent in arr:
                                if not isinstance(ent, dict):
                                    continue
                                matched = False
                                # 1) 优先按 POS 坐标匹配
                                if "POS" in ee:
                                    try:
                                        matched = (int(ent["x"]) == ee["POS"][0] and
                                                   int(ent["y"]) == ee["POS"][1] and
                                                   int(ent["z"]) == ee["POS"][2])
                                    except Exception:
                                        matched = False
                                # 2) POS 不匹配时，再按 UUID hex 值精确匹配
                                if not matched and "UUID" in ee:
                                    try:
                                        ent_uuid = None
                                        if "UUID" in ent:
                                            _ints = [int(x) for x in ent["UUID"]]
                                            ent_uuid = b"".join(struct.pack(">i", _x) for _x in _ints).hex()
                                        elif "UUIDMost" in ent and "UUIDLeast" in ent:
                                            ent_uuid = (struct.pack(">q", int(ent["UUIDMost"])).hex() +
                                                        struct.pack(">q", int(ent["UUIDLeast"])).hex())
                                        matched = (ent_uuid is not None and ent_uuid == ee["UUID"])
                                    except Exception:
                                        matched = False
                                if matched:
                                    for p, v in ee["PATH"].items():
                                        try: set_by_path(ent, p, v)
                                        except Exception: pass
                                    _entry_matched = True
                                    break
                            # 【完整版提示】遍历完都没匹配到，区分“缺定位信息”和“有定位但找不到实体”
                            if not _entry_matched:
                                _root_name = ee.get("Root", "?")
                                _has_pos = "POS" in ee
                                _has_uuid = "UUID" in ee
                                if not _has_pos and not _has_uuid:
                                    self.log_msg(f"  ⚠ 条目缺少定位信息（Root={_root_name}），已跳过")
                                else:
                                    self.log_msg(f"  ⚠ 未找到匹配实体（Root={_root_name}, POS={ee.get('POS')}, UUID={ee.get('UUID')}），已跳过")
                    # 【修复】显式序列化每个区块，不依赖 nbtlib.write() 的返回值
                    # 原写法 {idx: bio.getvalue() ... if not r.write(bio)} 在不同 nbtlib 版本下
                    # write() 可能返回字节数，导致正常区块被过滤，写回不完整。
                    rebuilt = {}
                    for _idx, _root_nbt in nbt_chunks.items():
                        _bio = io.BytesIO()
                        _root_nbt.write(_bio)
                        rebuilt[_idx] = _bio.getvalue()
                    # 【数据保护】解析失败的区块原样填回原始 raw bytes，保证不丢失
                    for _idx, _raw in failed_raw.items():
                        rebuilt[_idx] = _raw
                    # 【数据保护】如果一个区块都没有，绝不覆盖原文件
                    # （防止解析全失败时写一个空 .mca，导致该文件所有区块丢失）
                    if not rebuilt:
                        self.log_msg(f"  ⚠ {re['FilePath']} 没有可写回的区块，跳过（原文件未改动）")
                        _update_apply_progress(re["FilePath"] + "（跳过）")
                        continue
                    write_mca(mca_path, rebuilt)
                    _update_apply_progress(re["FilePath"])
            
            if data.get("MCARegions"): apply_mca(data["MCARegions"])
            if data.get("MCEntities"): apply_mca(data["MCEntities"])
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.log_msg("✓ 写回地图完成！")
        threading.Thread(target=task).start()

    # --- 核心操作 (数据包) ---
    def run_extract_datapacks(self):
        def task():
            if not (BASE_DIR / "datapacks").is_dir(): return self.log_msg("❌ 找不到 datapacks/")
            dp_path = BASE_DIR / "datapacks"
            for d in dp_path.iterdir():
                if d.is_dir() and d.name.endswith("_unzip"): shutil.rmtree(d)
            unpack_datapacks(dp_path)
            mcfuncs, jsons = collect_datapack_files()

            # 【进度条】按数据包文件数计算进度
            _total_dp = len(mcfuncs) + len(jsons)
            _done_dp = [0]
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self.status_label.configure(text=f"准备扫描 {_total_dp} 个数据包文件 ..."))

            def _update_dp_progress(name):
                _done_dp[0] += 1
                pct = _done_dp[0] / _total_dp if _total_dp else 0
                _d = _done_dp[0]; _t = _total_dp; _n = name
                self.after(0, lambda: self.progress_bar.set(pct))
                self.after(0, lambda: self.status_label.configure(text=f"正在扫描 {_d}/{_t}: {_n}"))

            out_mcf = []
            for f in mcfuncs:
                hits = scan_mcfunction(f)
                _update_dp_progress(f.name)
                if not hits: continue
                rel = str(f.relative_to(BASE_DIR)).replace("\\", "/")
                out_mcf.append({"FilePath": rel, "Hits": [{"Line": h[0], "Start": h[1], "End": h[2], "TEXT": h[3]} for h in hits]})
            out_json = []
            for f in jsons:
                hits = scan_json_dp(f)
                _update_dp_progress(f.name)
                if not hits: continue
                rel = str(f.relative_to(BASE_DIR)).replace("\\", "/")
                out_json.append({"FilePath": rel, "Hits": [{"Path": list(p), "TEXT": v} for p, v in hits]})
            
            data = {"MCFuncs": out_mcf, "MCJsons": out_json}
            save_dp_data_json(data)
            
            # 【优化】只有当备份文件不存在时，才写入。防止手滑重复提取把原始数据覆盖了
            if not DP_DATA_ORIG_JSON.is_file():
                _atomic_save_json(DP_DATA_ORIG_JSON, data)

            self.after(0, lambda: self.progress_bar.set(1.0))
            self.log_msg(f"✓ 提取数据包完成！共 {len(out_mcf)} 个 mcf, {len(out_json)} 个 json")
        threading.Thread(target=task).start()

    def run_dp_to_lang(self):
        def task():
            if not DP_DATA_JSON.is_file(): return self.log_msg("❌ 找不到 dp_data.json")
            with open(DP_DATA_JSON, "r", encoding="utf-8") as f: data = json.load(f)
            texts = [h["TEXT"] for f in data.get("MCFuncs", []) for h in f["Hits"]] + [h["TEXT"] for f in data.get("MCJsons", []) for h in f["Hits"]]
            seen = {}
            for t in texts:
                # 【修复】同样拦截 Base64 乱码
                if _is_base64_blob(t): continue
                if t not in seen: seen[t] = sha256(t.encode("utf-8")).hexdigest()
            result = [{"SHA256": h, "TEXT": t} for t, h in seen.items()]
            _atomic_save_json(DP_LANG_JSON, result)
            self.log_msg(f"✓ 生成 {len(result)} 条唯一文本 -> dp_lang.json")
        threading.Thread(target=task).start()

    def run_dp_to_data(self):
        def task():
            src = DP_DATA_ORIG_JSON if DP_DATA_ORIG_JSON.is_file() else DP_DATA_JSON
            if not src.is_file() or not DP_LANG_JSON.is_file(): return self.log_msg("❌ 找不到需要的 JSON 文件！")
            with open(src, "r", encoding="utf-8") as f: data = json.load(f)
            with open(DP_LANG_JSON, "r", encoding="utf-8") as f: lang = json.load(f)
            h2t = {i["SHA256"]: i["TEXT"] for i in lang}
            changed = 0
            def map_text(v):
                nonlocal changed
                h = sha256(v.encode("utf-8")).hexdigest()
                if h in h2t and h2t[h] != v: changed += 1; return h2t[h]
                return v
            for f in data.get("MCFuncs", []):
                for h in f["Hits"]: h["TRANSLATED"] = map_text(h["TEXT"])
            for f in data.get("MCJsons", []):
                for h in f["Hits"]: h["TRANSLATED"] = map_text(h["TEXT"])
            save_dp_data_json(data)
            self.log_msg(f"✓ 成功替换 {changed} 条数据到 dp_data.json！")
        threading.Thread(target=task).start()

    def run_apply_datapacks(self):
        def task():
            if not DP_DATA_JSON.is_file(): return self.log_msg("❌ 找不到 dp_data.json")
            with open(DP_DATA_JSON, "r", encoding="utf-8") as f: data = json.load(f)
            if not data.get("MCFuncs") and not data.get("MCJsons"): return self.log_msg("❌ 数据为空。")
            if not DP_BACKUP.exists(): shutil.copytree(BASE_DIR / "datapacks", DP_BACKUP)

            # 【进度条】按数据包文件数计算进度
            _total_dp = len(data.get("MCFuncs", [])) + len(data.get("MCJsons", []))
            _done_dp = [0]
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self.status_label.configure(text=f"准备写回 {_total_dp} 个数据包文件 ..."))

            def _update_dp_write_progress(file_path):
                _done_dp[0] += 1
                pct = _done_dp[0] / _total_dp if _total_dp else 0
                _d = _done_dp[0]; _t = _total_dp; _f = file_path
                self.after(0, lambda: self.progress_bar.set(pct))
                self.after(0, lambda: self.status_label.configure(text=f"正在写回 {_d}/{_t}: {_f}"))

            # 写回 mcfunction
            for entry in data.get("MCFuncs", []):
                f = BASE_DIR / entry["FilePath"]
                if not f.is_file():
                    _update_dp_write_progress(entry["FilePath"] + "（文件不存在）")
                    continue
                lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
                by_line = defaultdict(list)
                for h in entry["Hits"]: by_line[h["Line"]].append(h)
                file_changed = False
                for li, items in by_line.items():
                    if li >= len(lines): continue
                    line = lines[li]
                    items.sort(key=lambda x: x["Start"], reverse=True)
                    for h in items:
                        translated = h.get("TRANSLATED")
                        if not translated or translated == h["TEXT"]: continue
                        start, end = h["Start"], h["End"]
                        if end > len(line): continue
                        
                        current_slice = line[start:end]
                        original_str = h["TEXT"]
                        stripped_slice = current_slice.strip()

                        # 【核心修复】如果提取出来的原文是 JSON 结构
                        if stripped_slice.startswith("{") or stripped_slice.startswith("["):
                            try:
                                # 情况A：如果翻译结果本身就直接是完整的 JSON
                                if translated.strip().startswith("{") or translated.strip().startswith("["):
                                    line = line[:start] + translated + line[end:]
                                    file_changed = True
                                    continue
                                
                                # 情况B：如果翻译结果是纯多行文本，用 _replace_all_texts 安全填回 JSON
                                lines_arr = translated.split("\n")
                                final_json_str = _replace_all_texts(current_slice, lines_arr)
                                if final_json_str != current_slice:
                                    line = line[:start] + final_json_str + line[end:]
                                    file_changed = True
                                continue
                            except Exception:
                                pass

                        # 原有的普通字符串兜底替换
                        escaped_str = encode_escaped(original_str)
                        if current_slice == original_str:
                            line = line[:start] + translated + line[end:]; file_changed = True
                        elif current_slice == escaped_str:
                            line = line[:start] + encode_escaped(translated) + line[end:]; file_changed = True
                    lines[li] = line
                if file_changed: _atomic_write_text(f, "".join(lines))
                _update_dp_write_progress(entry["FilePath"])

            # 写回 json
            for entry in data.get("MCJsons", []):
                f = BASE_DIR / entry["FilePath"]
                if not f.is_file():
                    _update_dp_write_progress(entry["FilePath"] + "（文件不存在）")
                    continue
                try:
                    text = f.read_text(encoding="utf-8"); obj = json.loads(text)
                except Exception: continue
                file_changed = False
                for h in entry["Hits"]:
                    translated = h.get("TRANSLATED")
                    if not translated: continue
                    try:
                        set_json_by_path(obj, tuple(h["Path"]), translated); file_changed = True
                    except Exception: pass
                if file_changed: _atomic_save_json(f, obj)
                _update_dp_write_progress(entry["FilePath"])

            self.after(0, lambda: self.progress_bar.set(1.0))
            self.log_msg("✓ 写回 datapacks 文件完成，正在打包...")
            repack_datapacks()
            self.log_msg("✓ 数据包重新打包完成！")
        threading.Thread(target=task).start()

    # --- AI 翻译与 Python 替换 ---
    def open_api_dialog(self, target_file):
        if not os.path.exists(target_file): return self.log_msg(f"❌ 找不到 {target_file}")
        win = ctk.CTkToplevel(self)
        win.title(f"🚀 API 翻译 - {Path(target_file).name}")
        _w, _h = _fit_size(win, 500, 600)
        win.geometry(f"{_w}x{_h}")
        win.attributes("-topmost", True)
        win.configure(fg_color="#FFFFFF")
        try: apply_icon(win)
        except Exception: pass
        win.update_idletasks()
        win.geometry(f"+{self.winfo_x() + (self.winfo_width() - 500) // 2}+{self.winfo_y() + (self.winfo_height() - 600) // 2}")

        header = ctk.CTkFrame(win, fg_color="#F0F2F5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🚀 API 自动翻译", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=20)
        ctk.CTkLabel(header, text=Path(target_file).name, font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")

        btn_frame = ctk.CTkFrame(win, fg_color="#F0F2F5", height=70)
        btn_frame.pack(fill="x", side="bottom")
        btn_frame.pack_propagate(False)

        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(body, text="翻译引擎", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(0, 5))
        engine_opt = ctk.CTkOptionMenu(body, values=["Google 免费", "OpenAI (ChatGPT)", "DeepSeek", "通义千问", "Kimi", "智谱GLM", "硅基流动", "DeepL", "百度"],
                                       font=("Microsoft YaHei", 12), height=36,
                                       fg_color="#F0F2F5", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                       text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        engine_opt.pack(fill="x", pady=(0, 10))

        key_label = ctk.CTkLabel(body, text="API Key：", font=("Microsoft YaHei", 13, "bold"), text_color="#333333")
        key_label.pack(anchor="w", pady=(0, 5))
        key_entry = ctk.CTkEntry(body, placeholder_text="输入密钥", font=("Microsoft YaHei", 12), height=36,
                                 border_color="#E0E0E0", fg_color="#FFFFFF")
        key_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(body, text="翻译范围", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(0, 5))

        # 【新增】使用已保存配置
        cfg_row = ctk.CTkFrame(body, fg_color="transparent")
        cfg_row.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(cfg_row, text="使用配置", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(side="left", padx=(0, 10))

        _profile_names = api_profile_names()
        _active = api_profile_active_name()
        _cfg_values = ["（不使用配置）"] + _profile_names
        _cfg_initial = _active if _active in _profile_names else "（不使用配置）"
        cfg_opt = ctk.CTkOptionMenu(cfg_row, values=_cfg_values,
                                     font=("Microsoft YaHei", 12), height=36,
                                     fg_color="#F0F2F5", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                     text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        cfg_opt.set(_cfg_initial)
        cfg_opt.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def _apply_profile(name):
            if not name or name == "（不使用配置）":
                return
            p = api_profile_get(name)
            if not p:
                return
            engine = p.get("engine", "")
            key = p.get("key", "")
            hints = {
                "Google 免费": ("API Key（无需填写）：", "Google 免费，直接点开始"),
                "OpenAI (ChatGPT)": ("OpenAI API Key：", "例如：sk-proj-xxxxxxxxxxxxxxxx"),
                "DeepSeek": ("DeepSeek API Key：", "例如：sk-xxxxxxxxxxxxxxxx"),
                "通义千问": ("通义千问 API Key（DashScope）：", "例如：sk-xxxxxxxxxxxxxxxx"),
                "Kimi": ("Kimi API Key（Moonshot）：", "例如：sk-xxxxxxxxxxxxxxxx"),
                "智谱GLM": ("智谱 API Key（BigModel）：", "例如：xxxxxxxxxxxxxxxx"),
                "硅基流动": ("硅基流动 API Key：", "例如：sk-xxxxxxxxxxxxxxxx"),
                "DeepL": ("DeepL API Key：", "例如：xxxx-xxxx-xxxx-xxxx:fx"),
                "百度": ("百度 AppID,密钥（英文逗号分隔）：", "例如：20240315001234567,AbCdEfGhIjKl"),
            }
            if engine in hints:
                engine_opt.set(engine)
                label_text, placeholder = hints[engine]
                key_label.configure(text=label_text)
                key_entry.configure(placeholder_text=placeholder)
            key_entry.delete(0, "end")
            key_entry.insert(0, key)

        def _open_profile_manager():
            dlg = ApiProfileManagerDialog(win)
            win.wait_window(dlg)
            names = api_profile_names()
            active = api_profile_active_name()
            cfg_opt.configure(values=["（不使用配置）"] + names)
            if active in names:
                cfg_opt.set(active)
                _apply_profile(active)
            elif cfg_opt.get() not in names and cfg_opt.get() != "（不使用配置）":
                cfg_opt.set("（不使用配置）")

        ctk.CTkButton(cfg_row, text="管理", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 12, "bold"), height=36, width=70,
                      command=_open_profile_manager).pack(side="left")

        cfg_opt.configure(command=lambda choice: _apply_profile(choice))
        scope_opt = ctk.CTkOptionMenu(body, values=["仅未翻译", "全部（含已翻译）"],
                                      font=("Microsoft YaHei", 12), height=36,
                                      fg_color="#F0F2F5", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                      text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        scope_opt.pack(fill="x", pady=(0, 10))
        scope_opt.set("仅未翻译")

        ctk.CTkLabel(body, text="并发数（越大越快，过高可能触发限流）", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(0, 5))
        conc_opt = ctk.CTkOptionMenu(body, values=["1（最稳）", "3（推荐）", "5（快）", "8（激进）"],
                                     font=("Microsoft YaHei", 12), height=36,
                                     fg_color="#F0F2F5", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                     text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        conc_opt.pack(fill="x", pady=(0, 10))
        conc_opt.set("3（推荐）")

        progress_frame = ctk.CTkFrame(body, fg_color="#F0F2F5", corner_radius=8)
        progress_frame.pack(fill="x", pady=(5, 0))
        status_label = ctk.CTkLabel(progress_frame, text="准备就绪", font=("Microsoft YaHei", 12), text_color="#555555")
        status_label.pack(anchor="w", padx=15, pady=(10, 5))
        progress_bar = ctk.CTkProgressBar(progress_frame, height=16, progress_color="#000000", fg_color="#E0E0E0", corner_radius=0)
        progress_bar.pack(fill="x", padx=15, pady=(0, 12))
        progress_bar.configure(progress_color="#E0E0E0")
        progress_bar.set(0)

        ENGINE_HINTS = {
            "Google 免费": ("API Key（无需填写）：", "Google 免费，直接点开始"),
            "OpenAI (ChatGPT)": ("OpenAI API Key：", "例如：sk-proj-xxxxxxxxxxxxxxxx"),
            "DeepSeek": ("DeepSeek API Key：", "例如：sk-xxxxxxxxxxxxxxxx"),
            "通义千问": ("通义千问 API Key（DashScope）：", "例如：sk-xxxxxxxxxxxxxxxx"),
            "Kimi": ("Kimi API Key（Moonshot）：", "例如：sk-xxxxxxxxxxxxxxxx"),
            "智谱GLM": ("智谱 API Key（BigModel）：", "例如：xxxxxxxxxxxxxxxx"),
            "硅基流动": ("硅基流动 API Key：", "例如：sk-xxxxxxxxxxxxxxxx"),
            "DeepL": ("DeepL API Key：", "例如：xxxx-xxxx-xxxx-xxxx:fx"),
            "百度": ("百度 AppID,密钥（英文逗号分隔）：", "例如：20240315001234567,AbCdEfGhIjKl"),
        }
        def on_engine_change(choice):
            label, ph = ENGINE_HINTS.get(choice, ("API Key：", "输入密钥"))
            key_label.configure(text=label)
            key_entry.configure(placeholder_text=ph)
        engine_opt.configure(command=on_engine_change)
        on_engine_change(engine_opt.get())

        # 启动时如果有 active 配置，自动填充引擎和 Key
        if _cfg_initial != "（不使用配置）":
            try: _apply_profile(_cfg_initial)
            except Exception: pass

        start_btn = ctk.CTkButton(btn_frame, text="▶ 开始自动翻译", fg_color="#007ACC", hover_color="#005A9E",
                                  font=("Microsoft YaHei", 14, "bold"), height=40)
        start_btn.pack(side="left", padx=(20, 5), pady=15, fill="x", expand=True)

        stop_btn = ctk.CTkButton(btn_frame, text="⏹ 停止翻译", fg_color="#B84C3D", hover_color="#9B3A2E", text_color="#FFFFFF",
                                 font=("Microsoft YaHei", 14, "bold"), height=40)

        close_btn = ctk.CTkButton(btn_frame, text="关闭", fg_color="#E4E7ED", hover_color="#D0D0D0",
                                  text_color="#333333", font=("Microsoft YaHei", 14, "bold"), height=40)
        close_btn.pack(side="left", padx=(5, 20), pady=15, fill="x", expand=True)

        cancel_event = threading.Event()
        state = {"running": False}

        def on_progress(current, total):
            if not win.winfo_exists(): return
            pct = current / total if total else 0
            if pct <= 0:
                progress_bar.configure(progress_color="#E0E0E0")
            else:
                progress_bar.configure(progress_color="#000000")
            progress_bar.set(pct)
            status_label.configure(text=f"正在翻译 {current}/{total}（{int(pct*100)}%）", text_color="#000000")

        def on_stop():
            if state["running"]:
                cancel_event.set()
                stop_btn.configure(state="disabled", text="正在停止...")
                status_label.configure(text="正在停止，等待当前批次完成...", text_color="#D9534F")

        stop_btn.configure(command=on_stop)

        def _finish(ok, total, cancelled):
            state["running"] = False
            if not win.winfo_exists(): return
            stop_btn.pack_forget()
            start_btn.pack(side="left", padx=(20, 5), pady=15, fill="x", expand=True, before=close_btn)
            start_btn.configure(text="▶ 再翻译一次", state="normal")
            engine_opt.configure(state="normal")
            key_entry.configure(state="normal")
            scope_opt.configure(state="normal")
            conc_opt.configure(state="normal")
            if total == 0:
                status_label.configure(text="没有需要翻译的条目", text_color="#777777")
            elif cancelled:
                status_label.configure(text=f"⏹ 已停止：翻译 {ok}/{total} 条并保存", text_color="#D9534F")
            else:
                status_label.configure(text=f"✅ 完成：共 {ok}/{total} 条", text_color="#333333")
            _final_pct = ok / total if total else 0
            if _final_pct <= 0:
                progress_bar.configure(progress_color="#E0E0E0")
            else:
                progress_bar.configure(progress_color="#000000")
            progress_bar.set(_final_pct)

        def start():
            engine_type = engine_opt.get()
            key = key_entry.get().strip()
            scope = scope_opt.get()
            try:
                conc = int(conc_opt.get()[0])
            except Exception:
                conc = 3

            if engine_type == "百度":
                if "," not in key:
                    status_label.configure(text="❌ 百度需要填 AppID,密钥（英文逗号分隔）", text_color="#D9534F")
                    return
                a, s = key.split(",", 1)
                if not a.strip() or not s.strip():
                    status_label.configure(text="❌ AppID 或密钥不能为空", text_color="#D9534F")
                    return
            if engine_type in ("DeepSeek", "DeepL", "OpenAI (ChatGPT)", "通义千问", "Kimi", "智谱GLM", "硅基流动") and not key:
                status_label.configure(text=f"❌ {engine_type} 需要填 API Key", text_color="#D9534F")
                return

            state["running"] = True
            cancel_event.clear()
            engine_opt.configure(state="disabled")
            key_entry.configure(state="disabled")
            scope_opt.configure(state="disabled")
            conc_opt.configure(state="disabled")
            start_btn.pack_forget()
            stop_btn.pack(side="left", padx=(20, 5), pady=15, fill="x", expand=True, before=close_btn)
            stop_btn.configure(state="normal", text="⏹ 停止翻译")
            status_label.configure(text="正在初始化...", text_color="#007ACC")

            self._run_api_translate(
                target_file, engine_type, key, scope,
                concurrency=conc,
                cancel_event=cancel_event,
                progress_callback=on_progress,
                on_finish=_finish,
            )

        start_btn.configure(command=start)

        def on_close():
            if state["running"]:
                cancel_event.set()
            win.destroy()
        close_btn.configure(command=on_close)
        win.protocol("WM_DELETE_WINDOW", on_close)


    def _run_api_translate(self, target_file, engine_type, key, scope="仅未翻译",
                           concurrency=3, cancel_event=None, progress_callback=None, on_finish=None):
        if cancel_event is None:
            cancel_event = threading.Event()

        def task():
            from concurrent.futures import ThreadPoolExecutor, as_completed

            try:
                if engine_type == "Google 免费":
                    engine = GoogleEngine("en", "zh-CN")
                elif engine_type == "OpenAI (ChatGPT)":
                    if not key:
                        self.log_msg("❌ OpenAI 需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key,
                                            base_url="https://api.openai.com/v1",
                                            model="gpt-4.1-mini")
                elif engine_type == "DeepSeek":
                    if not key:
                        self.log_msg("❌ DeepSeek 需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key)
                elif engine_type == "通义千问":
                    if not key:
                        self.log_msg("❌ 通义千问需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key,
                                            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                                            model="qwen-plus")
                elif engine_type == "Kimi":
                    if not key:
                        self.log_msg("❌ Kimi 需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key,
                                            base_url="https://api.moonshot.cn/v1",
                                            model="moonshot-v1-8k")
                elif engine_type == "智谱GLM":
                    if not key:
                        self.log_msg("❌ 智谱GLM 需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key,
                                            base_url="https://open.bigmodel.cn/api/paas/v4",
                                            model="glm-4-flash")
                elif engine_type == "硅基流动":
                    if not key:
                        self.log_msg("❌ 硅基流动需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepSeekEngine("en", "zh-CN", key,
                                            base_url="https://api.siliconflow.cn/v1",
                                            model="Qwen/Qwen2.5-7B-Instruct")
                elif engine_type == "DeepL":
                    if not key:
                        self.log_msg("❌ DeepL 需要填 API Key")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = DeepLEngine("en", "zh-CN", key)
                elif engine_type == "百度":
                    if "," not in key:
                        self.log_msg("❌ 百度需要填 AppID,密钥（英文逗号分隔）")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    appid, secret = key.split(",", 1)
                    if not appid.strip() or not secret.strip():
                        self.log_msg("❌ 百度 AppID 或密钥为空")
                        if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                        return
                    engine = BaiduEngine("en", "zh-CN", appid.strip(), secret.strip())
                else:
                    self.log_msg(f"❌ 未知引擎: {engine_type}")
                    if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                    return
            except Exception as e:
                self.log_msg(f"❌ 引擎初始化失败: {e}")
                if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                return

            with open(target_file, "r", encoding="utf-8") as f: data = json.load(f)

            all_targets = []
            for i, item in enumerate(data):
                raw_text = item.get("TEXT", "")
                raw_text = "".join(c for c in raw_text if c.isprintable() or c in "\n\t")
                stripped = raw_text.strip()
                if not stripped: continue
                if _is_base64_blob(stripped): continue
                if stripped.startswith("{") or stripped.startswith("["):
                    try:
                        obj = json.loads(stripped)
                        if not _collect_all_texts(obj): continue
                    except Exception: pass
                else:
                    if stripped.startswith("minecraft:"): continue
                    if not re.search(r"[a-zA-Z\u4e00-\u9fff]", stripped): continue
                    if _is_playsound_text(stripped): continue
                    if _is_url_text(stripped): continue
                display_text = extract_display_text(raw_text)
                if not display_text or not display_text.strip(): continue
                if _is_base64_blob(display_text): continue
                all_targets.append((i, display_text))

            if scope == "仅未翻译":
                targets = [(i, t) for i, t in all_targets if not re.search(r"[\u4e00-\u9fff]", t)]
            else:
                targets = all_targets

            if not targets:
                self.log_msg(f"✓ 没有需要翻译的条目（范围：{scope}）。")
                if on_finish: self.after(0, lambda: on_finish(0, 0, False))
                return

            # ★ 中文原文守卫
            cn_count = sum(1 for _, t in targets if re.search(r"[\u4e00-\u9fff]", t))
            if cn_count > 0 and cn_count >= len(targets) * 0.5:
                _guard = {"ok": False, "done": threading.Event()}
                def _ask():
                    try:
                        _guard["ok"] = messagebox.askyesno(
                            "检测到大量中文原文",
                            f"本次要翻译的 {len(targets)} 条中，有 {cn_count} 条的原文已是中文。\n\n"
                            "这通常说明地图已经翻译过、或 lang.json 不是从英文原版生成的。\n"
                            "继续翻译可能会把中文当英文处理，导致乱译。\n\n"
                            "建议：先恢复英文原版，或只翻译真正未翻译的条目。\n\n"
                            "是否仍要继续？",
                        )
                    except Exception:
                        _guard["ok"] = True
                    finally:
                        _guard["done"].set()
                try:
                    self.after(0, _ask)
                    _guard["done"].wait(timeout=120)
                except Exception:
                    _guard["ok"] = True
                if not _guard["ok"]:
                    self.log_msg("⏹ 已取消（中文原文守卫触发）")
                    if on_finish: self.after(0, lambda: on_finish(0, 0, True))
                    return

            total = len(targets)
            workers = max(1, min(int(concurrency), 16))
            self.log_msg(f"开始使用 {engine_type} 翻译 {total} 条（范围：{scope}，并发 {workers}）...")
            ok = 0
            cancelled = False
            results = {}
            done_count = [0]
            lock = threading.Lock()

            def translate_one(idx, display_text):
                if cancel_event.is_set():
                    return idx, None
                try:
                    if "\n" in display_text:
                        lines = display_text.split("\n")
                        out_lines = []
                        for l in lines:
                            if not l.strip():
                                out_lines.append(l)
                            else:
                                out_lines.append(_translate_one(l, engine))
                        return idx, "\n".join(out_lines)
                    else:
                        return idx, _translate_one(display_text, engine)
                except Exception:
                    return idx, None

            try:
                with ThreadPoolExecutor(max_workers=workers) as executor:
                    futures = {executor.submit(translate_one, i, t): (i, t) for i, t in targets}
                    for future in as_completed(futures):
                        if cancel_event.is_set():
                            for f in futures:
                                f.cancel()
                            cancelled = True
                            break
                        try:
                            idx, translated = future.result()
                            if translated is not None:
                                with lock:
                                    results[idx] = translated
                                    ok += 1
                        except Exception:
                            pass
                        with lock:
                            done_count[0] += 1
                            dc = done_count[0]
                        if dc % 5 == 0 or dc == total:
                            if progress_callback:
                                self.after(0, lambda p=dc, t=total: progress_callback(p, t))
            except Exception as e:
                self.log_msg(f"❌ 翻译线程出错: {e}")

            for idx, translated in results.items():
                try:
                    data[idx]["TEXT"] = replace_display_text(data[idx]["TEXT"], translated)
                except Exception as e:
                    self.log_msg(f"  ⚠ 回填失败: {e}")

            try:
                _atomic_save_json(target_file, data)
            except Exception as e:
                self.log_msg(f"❌ 保存失败: {e}")

            if cancelled:
                self.log_msg(f"⏹ 翻译已停止，已保存 {ok} 条到 {target_file}")
            else:
                self.log_msg(f"✓ 翻译完成，共处理 {ok} 条（并发 {workers}）！")

            if on_finish:
                self.after(0, lambda: on_finish(ok, total, cancelled))

        threading.Thread(target=task, daemon=True).start()


    def open_code_runner(self):
        window = ctk.CTkToplevel(self)
        window.title("🤖 应用 AI 翻译结果")
        _w, _h = _fit_size(window, 800, 700)
        window.geometry(f"{_w}x{_h}")
        window.attributes("-topmost", True)
        window.configure(fg_color="#FFFFFF")
        try: apply_icon(window)
        except Exception: pass
        window.update_idletasks()
        window.geometry(f"+{self.winfo_x() + (self.winfo_width() - 800) // 2}+{self.winfo_y() + (self.winfo_height() - 700) // 2}")

        header = ctk.CTkFrame(window, fg_color="#F0F2F5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🤖 应用 AI 翻译结果", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=20)
        ctk.CTkLabel(header, text="粘贴 AI 脚本，一键回填", font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")

        btn_frame = ctk.CTkFrame(window, fg_color="#F0F2F5", height=70)
        btn_frame.pack(fill="x", side="bottom")
        btn_frame.pack_propagate(False)

        body = ctk.CTkFrame(window, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        top_frame = ctk.CTkFrame(body, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(top_frame, text="本次替换目标：", font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(side="left")
        target_opt = ctk.CTkOptionMenu(top_frame, values=["lang.json", "dp_lang.json"],
                                       font=("Microsoft YaHei", 12), height=36,
                                       fg_color="#F0F2F5", button_color="#E0E0E0", button_hover_color="#D0D0D0",
                                       text_color="#333333", dropdown_fg_color="#FFFFFF", dropdown_text_color="#333333")
        target_opt.pack(side="left", padx=10)

        label_row = ctk.CTkFrame(body, fg_color="transparent")
        label_row.pack(fill="x", pady=(5, 5))

        ctk.CTkLabel(label_row, text="粘贴 AI 返回的中文字典即可（或完整脚本），工具会自动执行：",
                     font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(side="left")

        def import_json_file():
            from tkinter import filedialog
            path = filedialog.askopenfilename(
                title="选择 JSON 字典文件",
                filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
                parent=window,
            )
            if not path:
                return
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    self.log_msg("❌ JSON 根必须是对象 {SHA256: 译文}")
                    return
                content = json.dumps(data, ensure_ascii=False, indent=4)
                code_input.configure(state="normal")
                code_input.delete("1.0", "end")
                code_input.insert("1.0", content)
                self.log_msg(f"✓ 已导入 {len(data)} 条到输入框，点击下方【立即执行并应用】即可")
            except Exception as e:
                self.log_msg(f"❌ 读取失败: {e}")

        ctk.CTkButton(label_row, text="📁 导入 JSON", fg_color="#E4E7ED", hover_color="#D0D0D0", text_color="#333333",
                      font=("Microsoft YaHei", 12, "bold"), height=32, width=120,
                      command=import_json_file).pack(side="right")
        code_input = ctk.CTkTextbox(body, font=("Consolas", 12), height=250,
                                     border_color="#E0E0E0", border_width=1, fg_color="#FFFFFF")
        code_input.pack(fill="x", pady=5)

        ctk.CTkLabel(body, text="执行输出（实时日志）：",
                     font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(10, 5))
        code_output = ctk.CTkTextbox(body, font=("Consolas", 12), fg_color="#FAFAFA",
                                      border_color="#E0E0E0", border_width=1)
        code_output.pack(fill="both", expand=True, pady=(5, 10))
        code_output.configure(state="disabled")

        def execute_code():
            content = code_input.get("1.0", "end-1c").strip()
            if not content: return

            # 剥离 Markdown 代码块（AI 回复常带 ```python ... ```）
            if content.startswith("```"):
                first_nl = content.find("\n")
                if first_nl != -1:
                    content = content[first_nl + 1:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
            if not content:
                return self.log_msg("⚠ 输入内容为空（剥离 Markdown 后）")

            # 用 BASE_DIR 拼绝对路径，不再依赖启动目录
            target_file = str(WORK_DIR / target_opt.get())
            if not os.path.exists(target_file): return self.log_msg(f"❌ 找不到 {Path(target_file).name}")

            code_output.configure(state="normal"); code_output.delete("1.0", "end"); code_output.configure(state="disabled")
            
            def run():
                class RedirectText:
                    def __init__(self, textbox): self.textbox = textbox
                    def write(self, string):
                        self.textbox.configure(state="normal"); self.textbox.insert("end", string); self.textbox.see("end"); self.textbox.configure(state="disabled")
                    def flush(self): pass
                
                old_stdout = sys.stdout; sys.stdout = RedirectText(code_output)
                old_cwd = os.getcwd(); os.chdir(BASE_DIR)
                old_argv = sys.argv
                
                import runpy
                temp_script = os.path.join(WORK_DIR, "_ai_patch_temp.py")
                
                try:
                    # 【核心修复】如果检测到是完整的独立脚本
                    if "sys.argv" in content or "def main()" in content:
                        print(f">>> 检测到独立脚本，正在写入临时文件并注入目标: {target_file} ...")
                        with open(temp_script, "w", encoding="utf-8") as f:
                            f.write(content)
                        
                        # 伪造命令行参数，完美模拟双击/命令行运行环境
                        sys.argv = ["_ai_patch_temp.py", target_file]
                        # 使用 runpy 在独立的环境中运行该脚本
                        runpy.run_path(temp_script, run_name="__main__")
                        
                        self.log_msg(f"✓ 脚本执行完毕（已由脚本自动保存至 {target_file}）！")
                    
                    # 如果是字典或简单代码
                    else:
                        with open(target_file, "r", encoding="utf-8") as f:
                            json_data = json.load(f)
                            
                        def _normalize_to_dict(obj):
                            if isinstance(obj, dict):
                                if "SHA256" in obj and "TEXT" in obj and len(obj) <= 3:
                                    sha = obj.get("SHA256")
                                    txt = obj.get("TEXT")
                                    if isinstance(sha, str) and isinstance(txt, str):
                                        return {sha: txt}
                                return obj
                            if isinstance(obj, list):
                                merged = {}
                                for item in obj:
                                    sub = _normalize_to_dict(item)
                                    if isinstance(sub, dict):
                                        merged.update(sub)
                                return merged if merged else None
                            return None

                        def _try_extract_dict(text):
                            text = text.strip()
                            try:
                                obj = json.loads(text)
                                result = _normalize_to_dict(obj)
                                if result:
                                    return result
                            except Exception:
                                pass
                            decoder = json.JSONDecoder()
                            candidates = []
                            i = 0
                            while i < len(text):
                                ch = text[i]
                                if ch == "{" or ch == "[":
                                    try:
                                        obj, _ = decoder.raw_decode(text[i:])
                                        result = _normalize_to_dict(obj)
                                        if result:
                                            candidates.append(result)
                                    except Exception:
                                        pass
                                i += 1
                            if not candidates:
                                return None
                            return max(candidates, key=lambda d: len(d))

                        translation_dict = _try_extract_dict(content)
                        if translation_dict is not None:
                            print(f">>> 检测到字典（{len(translation_dict)} 条），自动匹配...\n")
                            matched = 0
                            skipped = 0
                            for item in json_data:
                                sha = item.get("SHA256")
                                if sha in translation_dict:
                                    item["TEXT"] = replace_display_text(item["TEXT"], translation_dict[sha])
                                    matched += 1
                                else:
                                    skipped += 1
                            print(f"✓ 匹配替换 {matched} 条")
                            if skipped:
                                print(f"· 跳过 {skipped} 条（字典中未找到对应 SHA256）")
                        else:
                            print(">>> 检测到简短 Python 代码，正在执行...\n")
                            exec_globals = {
                                "__name__": "__main__", 
                                "__file__": os.path.join(BASE_DIR, "ai_patch.py"),
                                "json_data": json_data,
                                "TARGET_FILE": target_file
                            }
                            exec(content, exec_globals)
                        
                        print("\n>>> 正在保存...")
                        _atomic_save_json(target_file, json_data)
                        self.log_msg(f"✓ 应用成功并保存至 {target_file}！")
                        
                except Exception as e:
                    print(f"\n[执行出错]\n{traceback.format_exc()}")
                    self.log_msg(f"✗ 执行出错，请查看上方日志。")
                finally: 
                    sys.stdout = old_stdout; os.chdir(old_cwd)
                    sys.argv = old_argv
                    # 清理临时文件
                    if os.path.exists(temp_script):
                        try: os.remove(temp_script)
                        except: pass
                        
            threading.Thread(target=run).start()
            
        ctk.CTkButton(btn_frame, text="▶ 立即执行并应用", fg_color="#007ACC", hover_color="#005A9E",
                      font=("Microsoft YaHei", 14, "bold"), height=40, command=execute_code).pack(fill="x", padx=20, pady=15)

    # --- 查漏与手动翻译 ---
    def check_missing(self, target_file):
        def task():
            self.log_msg(f"开始扫描 {Path(target_file).name} 中未翻译的文本...")
            try:
                with open(target_file, "r", encoding="utf-8") as f: data = json.load(f)
                missing = []
                for item in data:
                    sha = item.get("SHA256", ""); raw_text = item.get("TEXT", "")
                    if _is_base64_blob(raw_text): continue
                    display = extract_for_check(raw_text)
                    if display and not _is_base64_blob(display):
                        missing.append((sha, display))
                self.after(0, lambda: self._show_missing_window(target_file, missing))
            except Exception as e: self.log_msg(f"✗ 查漏出错: {e}")
        threading.Thread(target=task).start()

    def _show_missing_window(self, target_file, missing):
        if not missing: return self.log_msg(f"✓ {target_file} 没有遗漏的英文，完美！")
        self.log_msg(f"✓ 查漏完毕！共找到 {len(missing)} 条。")

        win = ctk.CTkToplevel(self)
        win.title(f"🔍 查漏结果 - {Path(target_file).name}")
        _w, _h = _fit_size(win, 820, 640)
        win.geometry(f"{_w}x{_h}")
        win.attributes("-topmost", True)
        win.configure(fg_color="#FFFFFF")
        try: apply_icon(win)
        except Exception: pass
        win.update_idletasks()
        win.geometry(f"+{self.winfo_x() + (self.winfo_width() - 820) // 2}+{self.winfo_y() + (self.winfo_height() - 640) // 2}")

        header = ctk.CTkFrame(win, fg_color="#F0F2F5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🔍 翻译查漏结果", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=20)
        ctk.CTkLabel(header, text=f"{Path(target_file).name} · 共 {len(missing)} 条未翻译", font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")

        bottom_bar = ctk.CTkFrame(win, fg_color="#F0F2F5", height=70)
        bottom_bar.pack(fill="x", side="bottom")
        bottom_bar.pack_propagate(False)

        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(15, 10))

        ctk.CTkLabel(body, text="已生成字典格式，直接复制发给 AI 即可：",
                     font=("Microsoft YaHei", 13, "bold"), text_color="#333333").pack(anchor="w", pady=(0, 5))

        textbox = ctk.CTkTextbox(body, font=("Consolas", 13), fg_color="#FAFAFA",
                                 text_color="#333333", border_width=1, border_color="#E0E0E0",
                                 corner_radius=8)
        textbox.pack(fill="both", expand=True, pady=(5, 5))

        result_dict = {sha: text for sha, text in missing}
        result_text = json.dumps(result_dict, ensure_ascii=False, indent=4)
        textbox.insert("1.0", result_text)
        textbox.configure(state="disabled")

        ctk.CTkLabel(body, text="💡 提示：把复制的字典丢给Ai进行翻译。",
                     font=("Microsoft YaHei", 12), text_color="#888888").pack(anchor="w", pady=(5, 0))

        def copy_to_clipboard():
            combined = (
                "请把下面 JSON 字典里的英文 value 翻译成中文，保持 key 不变，",
                "输出完整的 JSON 字典即可（不需要任何代码）：\n\n",
                result_text,
            )
            final_text = "".join(combined)
            win.clipboard_clear()
            win.clipboard_append(final_text)
            self.log_msg(f"✓ 已复制字典（{len(missing)} 条）+ 提示到剪贴板，粘给 AI 即可。")

        def export_json():
            from tkinter import filedialog
            path = filedialog.asksaveasfilename(
                title="保存翻译字典",
                defaultextension=".json",
                filetypes=[("JSON 文件", "*.json")],
                initialfile=f"lang_export_{len(missing)}条.json",
                parent=win,
            )
            if not path:
                return
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(result_dict, f, ensure_ascii=False, indent=2)
                self.log_msg(f"✓ 已导出 {len(result_dict)} 条到 {path}")
            except Exception as e:
                self.log_msg(f"❌ 导出失败: {e}")
        ctk.CTkButton(bottom_bar, text="📋 一键复制字典格式", fg_color="#007ACC", hover_color="#005A9E",
                      font=("Microsoft YaHei", 14, "bold"), height=40,
                      command=copy_to_clipboard).pack(side="left", padx=(20, 5), pady=15, fill="x", expand=True)
        ctk.CTkButton(bottom_bar, text="💾 导出 JSON", fg_color="#E4E7ED", hover_color="#D0D0D0", text_color="#333333",
                      font=("Microsoft YaHei", 14, "bold"), height=40,
                      command=export_json).pack(side="left", padx=5, pady=15, fill="x", expand=True)
        ctk.CTkButton(bottom_bar, text="关闭", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 14, "bold"), height=40,
                      command=win.destroy).pack(side="left", padx=(5, 20), pady=15, fill="x", expand=True)

    def open_manual_translator(self, target_file):
        if not os.path.exists(target_file): return self.log_msg(f"❌ 找不到 {target_file}")
        try:
            with open(target_file, "r", encoding="utf-8") as f: data = json.load(f)
        except Exception as e: return self.log_msg(f"❌ 读取失败: {e}")

        to_translate = []
        for i, item in enumerate(data):
            raw_text = item.get("TEXT", "")
            raw_text = "".join(c for c in raw_text if c.isprintable() or c in "\n\t")
            stripped = raw_text.strip()
            if not stripped: continue
            if _is_base64_blob(stripped): continue

            # 【严格过滤】无可翻文本的条目直接跳过
            if stripped.startswith("{") or stripped.startswith("["):
                try:
                    obj = json.loads(stripped)
                    if not _collect_all_texts(obj):
                        continue   # JSON 里既无待翻英文，也无中文 → 跳过
                except Exception:
                    pass
            else:
                if stripped.startswith("minecraft:"):
                    continue       # 纯 minecraft: 命令跳过
                if not re.search(r'[a-zA-Z\u4e00-\u9fff]', stripped):
                    continue       # 无字母无中文 → 跳过
                if _is_playsound_text(stripped):
                    continue       # 纯 /playsound 音效指令，跳过
                if _is_url_text(stripped):
                    continue       # 纯 URL / 域名，跳过

            display_text = extract_display_text(raw_text)
            if not display_text or not display_text.strip(): continue
            if _is_base64_blob(display_text): continue
            to_translate.append((i, display_text))

        if not to_translate: return self.log_msg(f"✓ {target_file} 中没有需要翻译的纯英文条目。")
        window = ctk.CTkToplevel(self)
        window.title(f"📝 手动翻译 - {Path(target_file).name}")
        _w, _h = _fit_size(window, 900, 800)
        window.geometry(f"{_w}x{_h}")
        window.attributes("-topmost", True)
        window.configure(fg_color="#FFFFFF")
        try: apply_icon(window)
        except Exception: pass
        window.update_idletasks()
        window.geometry(f"+{self.winfo_x() + (self.winfo_width() - 900) // 2}+{self.winfo_y() + (self.winfo_height() - 800) // 2}")
        self._build_translator_ui(window, target_file, data, to_translate)

    def _build_translator_ui(self, window, target_file, data, to_translate):
        # ── 标题行（使用透明背景，消除白色长条） ──
        header = ctk.CTkFrame(window, fg_color="#F0F2F5", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="📝 手动翻译", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=(20, 16))

        info_label = ctk.CTkLabel(
            header,
            text=f"共找到 {len(to_translate)} 条待翻译文本（含已翻译，可来回修改）：",
            font=("Microsoft YaHei", 14, "bold"),
            text_color="#333333")
        info_label.pack(side="left")

        filter_var = ctk.StringVar(value="全部")

        filter_seg = ctk.CTkSegmentedButton(
            header, variable=filter_var,
            values=["全部", "已翻译", "未翻译"],
            font=("Microsoft YaHei", 12),
            height=28,
            fg_color="#E4E7ED",
            selected_color="#FFFFFF",
            selected_hover_color="#F0F2F5",
            unselected_color="#E4E7ED",
            unselected_hover_color="#D0D0D0",
            text_color="#555555",
            border_width=0
        )
        filter_seg.pack(side="right", padx=(0, 20))

        ctk.CTkLabel(header, text="翻译进度:",
                     font=("Microsoft YaHei", 12), text_color="#777777").pack(
                         side="right", padx=(0, 8))

        # ── 列表容器（保持原样） ──
        container = tk.Frame(window, bg="#F7F8FA"); container.pack(fill="both", expand=True, padx=20, pady=5)
        canvas = tk.Canvas(container, bg="#F7F8FA", highlightthickness=0); scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F7F8FA"); scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=820); canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")

        # 【鼠标滚轮】让手动翻译窗口支持滚轮滚动（lang / dp_lang 共用此函数）
        def _on_mousewheel(event):
            if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
                canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
                canvas.yview_scroll(1, "units")

        def _bind_wheel(widget):
            try:
                widget.bind("<MouseWheel>", _on_mousewheel, add="+")
                widget.bind("<Button-4>", _on_mousewheel, add="+")
                widget.bind("<Button-5>", _on_mousewheel, add="+")
            except Exception:
                pass

        def _bind_wheel_recursive(w):
            _bind_wheel(w)
            for child in w.winfo_children():
                _bind_wheel_recursive(child)

        _bind_wheel(canvas)
        _bind_wheel(scroll_frame)

        MAX_ROWS = 10; ui_rows = []
        for _ in range(MAX_ROWS):
            card = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E0E0E0")
            card.pack(fill="x", pady=8, padx=10); card.grid_columnconfigure(0, weight=1); card.grid_columnconfigure(1, weight=1)
            orig_box = ctk.CTkTextbox(card, font=("Microsoft YaHei", 13), height=110, fg_color="#F0F2F5", text_color="#555555", border_width=0)
            orig_box.grid(row=0, column=0, sticky="nsew", padx=(15, 10), pady=15)
            entry_box = ctk.CTkTextbox(card, font=("Microsoft YaHei", 13), height=110, wrap="word", fg_color="#FFFFFF", border_color="#D0D0D0", border_width=1)
            entry_box.grid(row=0, column=1, sticky="nsew", padx=(10, 15), pady=15)
            card.pack_forget()
            # 【B】卡片本身绑定滚轮：鼠标在卡片空白处（边框内、Textbox 外）能滚页面；
            # Textbox 上保留它自己的内部滚动，不会被页面滚动抢走。
            _bind_wheel(card)
            ui_rows.append({"frame": card, "orig": orig_box, "entry": entry_box, "data_idx": -1})

        # ── 状态 ──
        page_size = MAX_ROWS
        translated_dict = {}
        current_filtered = list(to_translate)
        total_pages = [max(1, (len(current_filtered) + page_size - 1) // page_size)]
        current_page = [0]

        # 【新增】搜索框（放在列表上方）
        search_row = ctk.CTkFrame(window, fg_color="transparent")
        search_row.pack(fill="x", padx=20, pady=(5, 0), before=container)
        ctk.CTkLabel(search_row, text="搜索:", font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_row, textvariable=search_var, font=("Microsoft YaHei", 12), height=32, placeholder_text="输入原文或译文关键词...")
        search_entry.pack(side="left", padx=8, fill="x", expand=True)

        page_frame = ctk.CTkFrame(window, fg_color="transparent"); page_frame.pack(fill="x", padx=20, pady=5)
        btn_prev = ctk.CTkButton(page_frame, text="⏮ 上一页", width=100); btn_prev.pack(side="left")
        page_label = ctk.CTkLabel(page_frame, text="第 1 / 1 页", font=("Microsoft YaHei", 13, "bold")); page_label.pack(side="left", expand=True)
        btn_next = ctk.CTkButton(page_frame, text="下一页 ⏭", width=100); btn_next.pack(side="right")

        # ── 辅助函数 ──
        def is_entry_translated(idx):
            text = translated_dict.get(idx, data[idx]["TEXT"])
            return bool(re.search(r'[\u4e00-\u9fff]', text))

        def save_current_page_inputs():
            for row in ui_rows:
                idx = row["data_idx"]
                if idx != -1:
                    val = row["entry"].get("1.0", "end-1c").strip()
                    if val:
                        translated_dict[idx] = replace_display_text(data[idx]["TEXT"], val)
                    elif idx in translated_dict:
                        del translated_dict[idx]

        def refresh_filtered():
            mode = filter_var.get()
            kw = search_var.get().strip().lower()
            result = []
            for idx, text in to_translate:
                tr = is_entry_translated(idx)
                if mode == "全部":
                    ok = True
                elif mode == "已翻译":
                    ok = tr
                else:
                    ok = not tr
                if not ok:
                    continue
                if kw:
                    tr_text = translated_dict.get(idx, data[idx]["TEXT"])
                    if kw not in text.lower() and kw not in tr_text.lower():
                        continue
                result.append((idx, text))
            current_filtered.clear()
            current_filtered.extend(result)
            total_pages[0] = max(1, (len(current_filtered) + page_size - 1) // page_size)
            if current_page[0] >= total_pages[0]:
                current_page[0] = total_pages[0] - 1

            # 【核心修改】动态更新顶部的标题文字
            count = len(current_filtered)
            if mode == "全部":
                info_label.configure(text=f"共找到 {count} 条待翻译文本（含已翻译，可来回修改）：")
            elif mode == "已翻译":
                info_label.configure(text=f"共找到 {count} 条已翻译文本：")
            else:
                info_label.configure(text=f"共找到 {count} 条未翻译文本：")

        def render_page():
            page_label.configure(text=f"第 {current_page[0] + 1} / {total_pages[0]} 页")
            start = current_page[0] * page_size
            end = min(start + page_size, len(current_filtered))
            for i, row in enumerate(ui_rows):
                actual_idx = start + i
                if actual_idx < end:
                    data_idx, text = current_filtered[actual_idx]
                    row["data_idx"] = data_idx
                    row["orig"].configure(state="normal")
                    row["orig"].delete("1.0", "end")
                    row["orig"].insert("1.0", text)
                    row["orig"].configure(state="disabled")
                    row["entry"].delete("1.0", "end")
                    if data_idx in translated_dict:
                        row["entry"].insert("1.0", extract_display_text(translated_dict[data_idx]))
                    row["frame"].pack(fill="x", pady=8, padx=10)
                else:
                    row["data_idx"] = -1
                    row["frame"].pack_forget()

        def on_filter_change(_=None):
            save_current_page_inputs()
            current_page[0] = 0
            refresh_filtered()
            render_page()
            canvas.yview_moveto(0)

        def prev_page():
            save_current_page_inputs()
            if current_page[0] > 0:
                current_page[0] -= 1
                render_page()
                canvas.yview_moveto(0)

        def next_page():
            save_current_page_inputs()
            if current_page[0] < total_pages[0] - 1:
                current_page[0] += 1
                render_page()
                canvas.yview_moveto(0)

        def save_all_translations():
            save_current_page_inputs()
            if not translated_dict:
                return self.log_msg("⚠ 没有输入内容。")
            for idx, val in translated_dict.items():
                data[idx]["TEXT"] = val
            try:
                _atomic_save_json(target_file, data)
                self.log_msg(f"✓ 成功将 {len(translated_dict)} 条写回 {target_file}！")
                window.destroy()
            except Exception as e:
                self.log_msg(f"❌ 保存失败: {e}")

        # ── 绑定事件 & 初始渲染 ──
        filter_seg.configure(command=on_filter_change)
        btn_prev.configure(command=prev_page)
        btn_next.configure(command=next_page)
        def on_search_change(_=None):
            save_current_page_inputs()
            current_page[0] = 0
            refresh_filtered()
            render_page()
            canvas.yview_moveto(0)
        search_entry.bind("<KeyRelease>", on_search_change)

        refresh_filtered()
        render_page()

        bottom_bar = ctk.CTkFrame(window, fg_color="#F0F2F5", height=70)
        bottom_bar.pack(fill="x", side="bottom")
        bottom_bar.pack_propagate(False)

        def export_extracted():
            from tkinter import filedialog
            path = filedialog.asksaveasfilename(
                title="导出手动翻译提取列表",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("JSON 文件", "*.json")],
                initialfile=f"manual_extracted_{len(to_translate)}条.txt",
                parent=window,
            )
            if not path:
                return
            try:
                if path.lower().endswith(".txt"):
                    lines = []
                    for idx, display in to_translate:
                        fp = _text_fp(data[idx].get("TEXT", ""))
                        one = display.replace("\n", "\\n")
                        lines.append(f"[{fp}] {one}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("\n".join(lines))
                else:
                    out = []
                    for idx, display in to_translate:
                        out.append({
                            "idx": idx,
                            "TEXT": data[idx].get("TEXT", ""),
                            "display": display,
                        })
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(out, f, ensure_ascii=False, indent=2)
                self.log_msg(f"✓ 已导出 {len(to_translate)} 条提取列表到 {path}")
            except Exception as e:
                self.log_msg(f"❌ 导出失败: {e}")

        def import_txt():
            from tkinter import filedialog
            path = filedialog.askopenfilename(
                title="选择译文 TXT（每行一条，按提取顺序对应）",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                parent=window,
            )
            if not path:
                return
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
            except Exception as e:
                self.log_msg(f"❌ 读取 TXT 失败: {e}")
                return
            if not lines:
                self.log_msg("⚠ TXT 为空")
                return
            save_current_page_inputs()
            # 建立 fp -> idx 映射，只针对当前 to_translate
            fp2idx = {}
            fp_collision = 0
            for idx, _display in to_translate:
                fp = _text_fp(data[idx].get("TEXT", ""))
                if fp in fp2idx:
                    fp_collision += 1
                fp2idx[fp] = idx
            filled = 0
            skipped_empty = 0
            skipped_bad = 0
            skipped_unknown = 0
            for line in lines:
                if not line.strip():
                    skipped_empty += 1
                    continue
                m = re.match(r'^\s*\[([0-9a-fA-F]{8})\]\s?(.*)$', line)
                if not m:
                    skipped_bad += 1
                    continue
                fp = m.group(1).lower()
                if fp not in fp2idx:
                    skipped_unknown += 1
                    continue
                val = m.group(2).replace("\\n", "\n")
                if not val.strip():
                    skipped_empty += 1
                    continue
                idx = fp2idx[fp]
                translated_dict[idx] = replace_display_text(data[idx]["TEXT"], val)
                filled += 1
            current_page[0] = 0
            refresh_filtered()
            render_page()
            canvas.yview_moveto(0)
            msg = (
                f"✓ 已导入 {filled} 条译文"
                f"（空行 {skipped_empty}，无 [fp] 前缀 {skipped_bad}，fp 不在当前列表 {skipped_unknown}）"
            )
            if fp_collision:
                msg += f" ⚠ 有 {fp_collision} 条文本内容重复，只保留最后一条"
            self.log_msg(msg)

        ctk.CTkButton(bottom_bar, text="📥 导入译文 TXT", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 14, "bold"), height=40, width=160,
                      command=import_txt).pack(side="left", padx=(20, 5), pady=15)
        ctk.CTkButton(bottom_bar, text="📤 导出提取列表", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 14, "bold"), height=40, width=160,
                      command=export_extracted).pack(side="left", padx=5, pady=15)
        ctk.CTkButton(bottom_bar, text="💾 保存并替换所有页", fg_color="#007ACC", hover_color="#005A9E",
                      font=("Microsoft YaHei", 14, "bold"), height=40,
                      command=save_all_translations).pack(side="left", fill="x", expand=True, padx=(5, 20), pady=15)

    # ==========================================
    # 工作目录清理
    # ==========================================
    def clean_work_dir(self):
        """侧边栏按钮：删除整个 LeafLingo_work/ 目录。"""
        if not WORK_DIR.exists():
            messagebox.showinfo("提示", f"工作目录 {WORK_DIR.name} 不存在，无需清理。")
            return
        msg = (
            f"将删除整个工作目录 {WORK_DIR.name}/，包含：\n\n"
            f"  data.json        （提取的原文）\n"
            f"  data_orig.json   （原始备份）\n"
            f"  lang.json        （译文）\n"
            f"  dp_data.json     （数据包原文）\n"
            f"  dp_lang.json     （数据包译文）\n"
            f"  config.json      （API 配置）\n"
            f"  datapacks_backup/（数据包备份）\n\n"
            f"注意：\n"
            f"  · 删除后需要重新【1】→【2】才能再翻译\n"
            f"  · 存档 region/entities/datapacks 本身不会被删除\n"
            f"  · 整存档备份 {WORLD_BACKUP.name} 不会被删除\n\n"
            f"确定删除整个 {WORK_DIR.name}/ 目录吗？"
        )
        if not messagebox.askyesno("确认删除工作目录", msg):
            return
        try:
            shutil.rmtree(WORK_DIR)
            self.log_msg(f"✓ 工作目录 {WORK_DIR.name}/ 已整体删除")
        except Exception as e:
            self.log_msg(f"❌ 删除失败: {e}")

    # ==========================================
    # 使用教程
    # ==========================================
    def open_tutorial(self):
        win = ctk.CTkToplevel(self)
        win.title("📖 使用教程")
        _w, _h = _fit_size(win, 850, 700)
        win.geometry(f"{_w}x{_h}")
        win.attributes("-topmost", True)
        win.configure(fg_color="#FFFFFF")
        try: apply_icon(win)
        except Exception: pass
        win.update_idletasks()
        win.geometry(f"+{self.winfo_x() + (self.winfo_width() - 850) // 2}+{self.winfo_y() + (self.winfo_height() - 700) // 2}")

        header = ctk.CTkFrame(win, fg_color="#F0F2F5", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="📖 使用教程", font=("Microsoft YaHei", 18, "bold"), text_color="#333333").pack(side="left", padx=(20, 16))
        ctk.CTkLabel(header, text="LeafLingo 地图汉化工具", font=("Microsoft YaHei", 12), text_color="#777777").pack(side="left")

        bottom_bar = ctk.CTkFrame(win, fg_color="#F0F2F5", height=70)
        bottom_bar.pack(fill="x", side="bottom")
        bottom_bar.pack_propagate(False)
        ctk.CTkButton(bottom_bar, text="关闭", fg_color="#E4E7ED", hover_color="#D0D0D0",
                      text_color="#333333", font=("Microsoft YaHei", 14, "bold"), height=40,
                      command=win.destroy).pack(side="right", padx=20, pady=15)

        textbox = ctk.CTkTextbox(win, font=("Microsoft YaHei", 14), fg_color="#FAFAFA",
                                 text_color="#333333", border_width=1, border_color="#E0E0E0",
                                 corner_radius=8, wrap="word")
        textbox.pack(fill="both", expand=True, padx=20, pady=(15, 10))

        tutorial_text = """✨ 欢迎使用 LeafLingo 地图汉化工具！ ✨
本工具支持从 1.8 到 1.21+ 的地图存档与数据包汉化，全程自动化处理，安全防损坏！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 一、快速开始（四步极简工作流）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ 在左侧选中【▶ 地图与实体】或【▶ 数据包】标签。
2️⃣ 点击右侧的【1. 提取文本】。
   👉 工具会自动扫描 mca 或解压 zip，将英文提取并保存到 data.json / dp_data.json。
3️⃣ 点击右侧的【2. 生成 Lang】。
   👉 工具会自动去重，生成 lang.json / dp_lang.json 供你翻译。
4️⃣ 翻译完成后（见下文的三种方式），依次点击【3. 合并回 Data】和【4. 写回】。
   👉 大功告成！进游戏享受全中文的地图！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ 二、三种翻译方式（任选其一，可混用）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【🔥 方式A：全自动 API 翻译（最省心）】
点击左侧【🚀 应用 AI 翻译】 -> 【API 翻译 lang.json / dp_lang.json】。

支持 9 个翻译引擎，按场景分三类：
  🆓 完全免费，无需 Key：
     · Google 免费  （走免费通道，量小够用，量大可能限流，可能需要科学上网）
  🇨🇳 国内主流大模型（中文翻译质量最好）：
     · DeepSeek   （推荐，便宜、稳定、理解语境强）
     · 通义千问    （阿里云百炼，中文语境极佳）
     · Kimi       （月之暗面，长上下文优势）
     · 智谱GLM     （免费额度大，适合测试）
     · 硅基流动    （聚合平台，可白嫖多家开源模型）
  🌍 国际服务：
     · OpenAI (ChatGPT)  （质量顶级，但需付费，账号需有对应模型权限）
     · DeepL      （欧美游戏文本翻译首选）
     · 百度        （Key 格式是 AppID,密钥，用英文逗号分隔）

使用步骤：
1. 下拉选择引擎。
2. 填入对应的 API Key（Google 免费不用填）。
3. 首次使用可点【管理】保存为配置（存 config.json），
   下次打开自动带出，不用重复填写。
4. 选择翻译范围（仅未翻译 / 全部）和并发数（推荐 3，过高可能触发限流）。
5. 点【开始自动翻译】，工具会在后台跑完全部翻译。
   · 中途可点【停止翻译】，已翻译的部分会立即保存。
   · 全自动跑完后，如果有英文残留，可以用【🔍 翻译查漏】补。

【🧠 方式B：外部 AI 辅助 + 字典回填（质量最高，强烈推荐）】
大语言模型（如 ChatGPT、DeepSeek）能翻出极通顺的语境，具体流程：
1. 点击左侧【🔍 翻译查漏】 -> 【查漏 lang.json/dp_lang】。
2. 在弹出的窗口中点击【📋 一键复制字典格式】。
   👉 复制出来的是「一行给 AI 的提示 + 纯 JSON 字典」，无需再单独复制提示词。
3. 直接粘给 AI。AI 会返回翻译好的「纯 JSON 字典」，不需要让 AI 写代码。
4. 点击左侧【🚀 应用 AI 翻译】 -> 【应用 AI 翻译结果】。
5. 选择目标文件（lang.json 或 dp_lang.json），粘贴 AI 返回的字典，点击执行。
   👉 工具会自动按 SHA256 匹配、回填译文，并保留颜色、行数、前导空白，
      不需要人工核对，也不会覆盖未匹配到的条目。

【📝 方式C：纯手动翻译（适合精修告示牌/书本）】
点击左侧【📝 手动翻译】 -> 【翻译 lang.json/dp_lang】。
工具会自动剥离复杂的 {"text":"...", "color":"..."} 外壳，只显示纯英文。
你在右侧输入中文【注意: 翻译的中文空行格式要和原文一样】，保存时工具会自动把外壳原样拼回去，保留原有的颜色和排版！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ 三、工具的安全机制（不会破坏存档）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 【防损坏机制】：如果你在手动翻译时，多敲了回车或少填了一行，工具会自动检测到行数不匹配，并保留该条英文原样，绝对不会破坏原本的 JSON 结构。
2. 【自动备份】：工具会自动保留原始的 data_orig.json，你可以放心反复翻译、合并。
3. 【Zip 自动打包】：如果是 zip 格式的数据包，工具会自动解压提取，写回时再自动重新打包成 zip，全程无需手动干预。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 四、常见问题与注意事项
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️不保证全部能汉化到，运用了很多过滤条件来筛选掉不必要的内容，可能会误筛一些，但是能保证翻译占97%以上

❌ 错误：当前目录不是地图存档根目录！
✅ 解决：请确保你的 exe 软件放在包含 level.dat、region 文件夹的存档根目录里。

❌ 错误：无法覆盖旧 zip，可能是游戏没关！
✅ 解决：在点击【写回】前，请务必完全关闭 Minecraft 游戏，否则文件会被游戏锁定。

❌ 游戏里的告示牌文字乱行、显示不全？
✅ 解决：由于 MC 告示牌一行最多只能显示 15 个字符，如果中文过长会被截断。建议去 lang.json 里搜索那句话，手动敲回车（\\n）来分段，然后再重新合并写回。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 五、致谢与开源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
本项目大部分借助AI完成，灵感来自 maptranslate (https://github.com/xmdhs/maptranslate)，
在过滤规则、写回机制、版本兼容性等方面做了大量改进。"""
        textbox.insert("1.0", tutorial_text)
        textbox.configure(state="disabled")

if __name__ == "__main__":
    app = LightThemeApp()
    app.mainloop()