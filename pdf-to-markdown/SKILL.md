---
name: pdf-to-markdown
description: >
  将 PDF 或图片文件通过 PaddleOCR 版面解析 API 转换为规范排版的 Markdown 文件。
  当用户需要 PDF 转 MD、PDF 转 Markdown、文档 OCR 识别、版面解析、图片转文字存为 Markdown 时使用此 skill。
  一个 PDF 输出一个 .md 文件，输出内容由 AI 进行 Markdown 标准语法排版优化。
---

# PDF → Markdown

## 快速使用

```bash
python "C:\Users\Admin\.cursor\skills\pdf-to-markdown\pdf2md.py" <PDF或图片路径> [输出目录]
```

- 输出目录默认为文件所在目录
- 支持格式：`.pdf` / `.jpg` / `.jpeg` / `.png` / `.bmp` / `.tiff` / `.webp`

## 执行流程

1. 运行脚本，等待 API 返回（大文件可能需要 30~120 秒）
2. 脚本输出 `__SUMMARY__` 后的 JSON，包含 `raw_md_path`
3. 读取 `raw_md_path` 文件内容
4. 对原始内容进行 Markdown 排版优化（见下方规范）
5. 将优化后内容写入 `<输出目录>/<原文件名>.md`
6. 删除临时文件 `<原文件名>_raw.md`

## Markdown 排版规范

对原始 OCR 文本按以下规则优化：

**结构**
- 识别并修正标题层级（`#` `##` `###`），确保层级语义合理
- 标题前后各保留一个空行
- 段落之间保留一个空行，不超过一个连续空行

**列表**
- 统一使用 `-` 作为无序列表符号
- 有序列表使用 `1.` `2.` 格式
- 列表块前后各保留一个空行

**表格**
- 修正表格对齐，确保每列有分隔符行 `| --- |`
- 表格前后各保留一个空行

**代码**
- 代码块使用三反引号包裹，标注语言类型
- 行内代码使用单反引号

**其他**
- 去除行尾多余空格
- 文件末尾保留且仅保留一个换行
- 多页之间的分隔线 `---` 保留

## 配置

`.env` 文件位于 skill 目录下：

```
PADDLEOCR_TOKEN=你的token
PADDLEOCR_API_URL=https://k2c3j2vau3u8d332.aistudio-app.com/layout-parsing
```

## 依赖

```bash
pip install requests
```

（`python-dotenv` 不需要，脚本内置了 `.env` 解析）
