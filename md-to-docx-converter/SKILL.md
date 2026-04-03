---
name: md-to-docx-converter
description: Convert Markdown files to Word documents (.docx) with Chinese typography standards. Use when users need to convert .md files to .docx format, generate formal documents from Markdown, create reports with proper Chinese fonts (SimSun for body text, SimHei for headings), or convert technical documentation to Word format. This skill applies proper formatting including SongTi (SimSun) for body text, HeiTi (SimHei) for headings, Times New Roman for English text, and 12pt font size.
compatibility: Requires Python 3 and pandoc installed on the system. Works on Windows, macOS, and Linux.
---

# Markdown to Word Converter

Convert Markdown files to professionally formatted Word documents with Chinese typography standards.

## When to Use

Use this skill when:
- User asks to convert Markdown to Word/Docx
- User needs to generate formal documents from .md files
- User wants proper Chinese font formatting (宋体正文, 黑体标题)
- User needs technical reports converted to Word format
- User mentions "转成Word", "生成docx", "导出Word" with Markdown files

## Instructions

### Step 1: Identify Input File

Check if the user has specified a Markdown file path:
- If provided, verify the file exists
- If not provided, look for common Markdown files in the current directory (*.md)
- Default to `技术可行性报告正文.md` if no file is specified

### Step 2: Run Conversion Script

Execute the conversion script with the identified Markdown file:

```bash
python scripts/convert_report_to_docx.py <input.md> [output.docx]
```

Parameters:
- `input.md`: Path to the Markdown file (required)
- `output.docx`: Path for the output Word document (optional, defaults to same name as input)

### Step 3: Verify Output

After execution, verify:
- The .docx file was created successfully
- File size is reasonable (not empty or corrupted)
- No error messages in the output

### Step 4: Report Results

Inform the user:
- Location of the generated .docx file
- Any formatting notes (fonts applied, etc.)
- Confirmation of successful conversion

## Formatting Standards Applied

The conversion automatically applies these Chinese document standards:

| Element | Font | Size |
|---------|------|------|
| Body Text | SimSun (宋体) / Times New Roman | 12pt (小四) |
| Heading 1 | SimHei (黑体) | 15pt |
| Heading 2 | SimHei (黑体) | 14pt |
| Heading 3-4 | SimHei (黑体) | 12pt Bold |
| Heading 5-6 | SimHei (黑体) | 11pt |
| Code/Verbatim | Consolas | 9pt |
| Captions | SimSun (宋体) | 10pt |

All text is set to black color for professional appearance.

## Examples

### Example 1: Basic Conversion
User says: "Convert my report.md to Word"
Actions:
1. Verify report.md exists
2. Run: `python scripts/convert_report_to_docx.py report.md`
3. Confirm: report.docx created with proper formatting

### Example 2: Custom Output Name
User says: "Convert input.md to output.docx"
Actions:
1. Verify input.md exists
2. Run: `python scripts/convert_report_to_docx.py input.md output.docx`
3. Confirm: output.docx created

### Example 3: Default File
User says: "Generate the Word document"
Actions:
1. Check for 技术可行性报告正文.md
2. Run: `python scripts/convert_report_to_docx.py`
3. Confirm: 技术可行性报告正文.docx created

## Error Handling

### Error: "找不到: [filename]"
Cause: The specified Markdown file does not exist
Solution: Verify the file path or check available .md files in the directory

### Error: "pandoc not found"
Cause: Pandoc is not installed on the system
Solution: Install pandoc from https://pandoc.org/installing.html

### Error: Permission denied
Cause: No write access to output directory
Solution: Check directory permissions or choose a different output location

## Dependencies

Required system dependencies:
- Python 3.6+
- Pandoc (document conversion tool)

The script handles all font styling automatically without additional dependencies.
