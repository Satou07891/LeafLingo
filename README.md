<img width="1901" height="1024" alt="image" src="https://github.com/user-attachments/assets/8f3cb2e2-848a-40d4-8c48-4f21227a4037" />LeafLingo 地图汉化工具
一款Minecraft地图存档汉化工具，支持1.8至1.21+版本的region、entities及datapacks文本的提取、翻译与写回，全程带备份，不会破坏存档。

✨ 功能
两种提取模式
region / entities：扫描.mca区块，提取告示牌、书本、物品名、lore、实体名、命令方块输出等
datapacks：扫描 .mcfunction / .json，自动解压 zip，写回时重新打包

三种翻译方式
手动翻译：左侧原文，右侧输入中文，支持搜索、分页、筛选
fp TXT 导入导出：导出带 [fp] 前缀的纯文本，丢给 AI 按行翻译，导入时按内容哈希精确回填，不怕重新生成 lang
API 自动翻译：Google / DeepL / DeepSeek / 通义千问 / Kimi / 智谱GLM / 硅基流动 / OpenAI / 百度

安全写回
整存档自动备份到 存档名_backup/
原子写入，单区块解析失败保留原始字节
空数据不覆盖，防止写坏

工作目录隔离
所有中间文件均位于 LeafLingo_work/ 目录下，不会污染归档根目录
汉化完成后可一键删除整个工作目录
过滤规则

自动跳过：playsound、URL、Base64 皮肤、翻译键、命名空间 ID、坐标、颜色保留词、纯符号
告示牌 Text1~4、书本 pages、messages、Lore 自动合并成多行条目，写回时按行还原
Lore 保留颜色、粗体、斜体格式

🚀 快速开始
方式一：下载 exe（推荐）
到 Releases 下载最新 LeafLingo.exe
把 exe 放到地图存档根目录（和 level.dat、region/ 同级）
双击运行

方式二：源码运行
bash
pip install nbtlib customtkinter pillow
python LeafLingo地图汉化工具.py
API 翻译需要额外装对应依赖：

bash
pip install deep-translator   # Google
pip install deepl             # DeepL
pip install openai            # DeepSeek / OpenAI / 通义千问 / Kimi / 智谱 / 硅基流动
pip install requests          # 百度

📖 使用流程
区域/实体主线
文本
1. 提取文本   → LeafLingo_work/data.json
2. 生成 Lang  → LeafLingo_work/lang.json
   ↓ 翻译（见下方三种方式）
3. 合并回 Data → 按 SHA256 把译文写回 data.json
4. 写回        → 写回 region/ entities/，自动备份整存档
datapacks 主线
文本
6. 提取 datapacks → LeafLingo_work/dp_data.json
7. 生成 DpLang    → LeafLingo_work/dp_lang.json
   ↓ 翻译
9. 合并回 DpData  → dp_data.json
10. 写回          → datapacks/，自动备份并重新打包 zip
只有在有数据包时才需要走第二条线。写回前请完全关闭 Minecraft，否则文件被占用。

🌐 三种翻译方式
A. 手动翻译 + fp TXT（推荐，最稳）
文本
📝 手动翻译 → 翻译 lang.json
→ 📤 导出提取列表（默认 .txt，每行 [fp] 原文）
→ 丢给 AI，让它按行翻译，保留 [fp] 前缀
→ 📥 导入译文 TXT（按 fp 精确回填）
→ 💾 保存并替换所有页

B. 手动翻译直接填
左侧原文，右侧输入中文，点「保存并替换所有页」。

C. API 自动翻译
文本
🚀 应用 AI 翻译 → API 翻译 lang.json
→ 选引擎、填 Key、选范围、并发 3
→ 开始自动翻译
支持保存多套 API 配置，下次自动带出。

🛡️ 安全机制
整存档备份：首次写回前自动 copytree 到 存档名_backup/
数据包备份：写回 datapacks 前备份到 LeafLingo_work/datapacks_backup/
原子写入：.tmp + os.replace，写一半崩溃不损坏原文件
区块级容错：单区块解析失败保留原始字节，不丢区块
空数据保护：data.json 为空时拒绝写回
行数对齐：手动翻译多敲/少敲回车，写回时自动补空或追加，不破坏 JSON 结构

📁 目录结构
文本
存档目录/
  level.dat
  region/
  entities/
  datapacks/
  LeafLingo_work/          ← 工具自动创建
    data.json
    data_orig.json
    lang.json
    dp_data.json
    dp_data_orig.json
    dp_lang.json
    config.json
    datapacks_backup/
  LeafLingo地图汉化工具.exe
汉化完成后，侧边栏「🧹 清理工作目录」可删除整个 LeafLingo_work/，存档和 datapacks 不受影响。

❓ 常见问题
Q：提示「当前目录不是地图存档根目录」？
把 exe 放到含 level.dat 和 region/ 的存档根目录。

Q：写回失败，提示文件被占用？
完全关闭 Minecraft 再写回。

Q：告示牌中文显示不全？
MC 告示牌一行最多 15 字符。在 lang.json 里搜到那句话，手动加 \n 分段，再重新合并写回。

Q：重新提取后 fp TXT 还能导入吗？
只要原文 TEXT 内容没变，fp 不变，旧 TXT 依然可导入。原文改了，那条会跳过。

Q：翻译后游戏里还是英文？
检查是否走了完整流程：1 → 2 → 翻译 → 3 → 4。只翻译 lang.json 不合并回 data.json、不写回，游戏里不会变。

📜 开源协议
本项目基于 MIT License 开源。

灵感来自 maptranslate，在过滤规则、写回机制、版本兼容性等方面做了大量改进。

🙏 致谢
nbtlib — NBT 解析

CustomTkinter — UI

maptranslate — 灵感来自

⚠️ 本工具不保证 100% 覆盖所有文本，过滤规则可能会误筛少量边角内容，但主体展示文本（告示牌、书本、物品、实体名、标题）覆盖率在 97% 以上。如遇明显漏翻，欢迎提交 Issue 并附上TEXT原文
<img width="1901" height="1023" alt="屏幕截图 2026-10-26 083053" src="https://github.com/user-attachments/assets/2ef3f27f-987e-4501-80ba-93362ca35aa2" />
<img width="1125" height="1007" alt="屏幕截图 2026-10-26 091633" src="https://github.com/user-attachments/assets/b25752f2-5204-4323-9bd2-0e4bd898f507" />
<img width="622" height="783" alt="屏幕截图 2026-10-26 092632" src="https://github.com/user-attachments/assets/d37f18c3-d4f8-4e11-ba04-551de777a15d" />
一些演示
1.21.11 Microscope
<img width="1920" height="1080" alt="2026-10-26_09 20 31" src="https://github.com/user-attachments/assets/7e1ebc19-d301-47ec-a3c8-f000f2a9601a" />
1.8 Asleep
<img width="1920" height="1080" alt="2026-10-26_10 22 21" src="https://github.com/user-attachments/assets/f6dbe083-0ad4-44ce-bee7-ecc6abae4e88" />







