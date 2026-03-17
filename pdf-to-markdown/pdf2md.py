#!/usr/bin/env python3
# pdf2md.py — 调用 PaddleOCR 版面解析 API，将 PDF/图片转为原始 Markdown
# 用法: python pdf2md.py <文件路径> [输出目录]
#
# 依赖: pip install requests python-dotenv
# 配置: 在脚本同目录下创建 .env 文件，填写 PADDLEOCR_TOKEN 和 PADDLEOCR_API_URL

import sys
import os
import base64
import json
import requests
from pathlib import Path

# ── 加载 .env ──────────────────────────────────────────────────────────────────
_skill_dir = Path(__file__).parent
_env_path = _skill_dir / ".env"

if _env_path.exists():
    with open(_env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

API_URL = os.environ.get("PADDLEOCR_API_URL", "https://k2c3j2vau3u8d332.aistudio-app.com/layout-parsing")
TOKEN   = os.environ.get("PADDLEOCR_TOKEN", "")

if not TOKEN:
    print("ERROR: 未找到 PADDLEOCR_TOKEN，请在 .env 文件中配置。")
    sys.exit(1)

# ── 文件类型判断 ────────────────────────────────────────────────────────────────
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}

def get_file_type(path: Path) -> int:
    """0=PDF, 1=图片"""
    return 0 if path.suffix.lower() == ".pdf" else 1

# ── 调用 API ───────────────────────────────────────────────────────────────────
def call_api(file_path: Path) -> list:
    file_bytes = file_path.read_bytes()
    file_data  = base64.b64encode(file_bytes).decode("ascii")

    payload = {
        "file":     file_data,
        "fileType": get_file_type(file_path),
        "useDocOrientationClassify": False,
        "useDocUnwarping":           False,
        "useChartRecognition":       False,
    }
    headers = {
        "Authorization": f"token {TOKEN}",
        "Content-Type":  "application/json",
    }

    print(f"正在上传并解析: {file_path.name} ...")
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)

    if resp.status_code != 200:
        print(f"ERROR: API 返回 {resp.status_code}\n{resp.text}")
        sys.exit(1)

    return resp.json()["result"]["layoutParsingResults"]

# ── 合并多页结果 ────────────────────────────────────────────────────────────────
def merge_pages(results: list, output_dir: Path) -> tuple[str, list]:
    """
    合并所有页的 markdown text，同时下载内嵌图片到 output_dir/images/。
    返回 (合并后的 markdown 文本, 下载失败的图片列表)
    """
    pages = []
    failed_images = []
    img_dir = output_dir / "images"

    for i, res in enumerate(results):
        md_text = res["markdown"]["text"]

        # 下载 markdown 内嵌图片
        for img_rel_path, img_url in res["markdown"].get("images", {}).items():
            local_path = output_dir / img_rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                img_bytes = requests.get(img_url, timeout=30).content
                local_path.write_bytes(img_bytes)
            except Exception as e:
                failed_images.append((img_rel_path, str(e)))

        pages.append(md_text)

    return "\n\n---\n\n".join(pages), failed_images

# ── 主流程 ─────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("用法: python pdf2md.py <文件路径> [输出目录]")
        sys.exit(1)

    file_path  = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else file_path.parent

    if not file_path.exists():
        print(f"ERROR: 文件不存在: {file_path}")
        sys.exit(1)

    suffix = file_path.suffix.lower()
    if suffix != ".pdf" and suffix not in IMAGE_EXTS:
        print(f"ERROR: 不支持的文件类型: {suffix}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # 调用 API
    results = call_api(file_path)

    # 合并页面
    raw_md, failed = merge_pages(results, output_dir)

    # 保存原始结果（供 agent 优化排版用）
    raw_path = output_dir / f"{file_path.stem}_raw.md"
    raw_path.write_text(raw_md, encoding="utf-8")

    print(f"\n原始 Markdown 已保存至: {raw_path}")
    print(f"共 {len(results)} 页")

    if failed:
        print(f"\n以下图片下载失败:")
        for p, e in failed:
            print(f"  {p}: {e}")

    # 输出供 agent 读取的 JSON 摘要
    summary = {
        "raw_md_path":  str(raw_path),
        "output_dir":   str(output_dir),
        "stem":         file_path.stem,
        "page_count":   len(results),
        "failed_images": failed,
    }
    print("\n__SUMMARY__")
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == "__main__":
    main()
