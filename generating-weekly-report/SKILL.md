---
name: "generating-weekly-report"
description: "Generates weekly work report templates with proper markdown structure. Use when user needs to create weekly reports, update report formats, or batch generate report templates for multiple weeks."
template: |
  ## 【周报】{{year}}年{{month}}月{{day}}日-{{name}}

  汇报周期：{{monday_date}} - {{friday_date}}（第{{week_number}}周）

  ### 本周工作内容：

  #### 【周一】
  1. 
  2. 
  3. 
  4. 

  #### 【周二】
  1. 
  2. 
  3. 
  4. 

  #### 【周三】
  1. 
  2. 
  3. 

  #### 【周四】
  1. 
  2. 
  3. 

  #### 【周五】
  1. 
  2. 
  3. 
  4. 
  5. 

  ### 想法记录：（该项必填，至少100字，不限制任何想法，可以是工作、自身、未来、目标等各角度思考）
---
## When to Use

触发关键词：周报、weekly report、生成周报、创建周报、批量生成

- 用户需要创建新的周报
- 用户需要批量生成未来几周的周报模板
- 用户需要更新现有周报格式

## Name Detection

生成周报前，检查输出目录中的现有文件以确定用户姓名：

1. 扫描输出目录中的 `【周报】YYYY年MM月DD日-Name.md` 文件
2. 从文件名中提取姓名（最后一个 `-` 和 `.md` 之间的部分）
3. 如果存在一致的姓名，新报告使用该姓名
4. 如果没有现有文件或姓名不一致，使用 "Name" 作为占位符

## Report Date Calculation

- 报告日期为该周的**周五**（最后一个工作日）
- 文件名使用周五日期：`【周报】YYYY年MM月DD日-Name.md`
- 汇报周期显示周一到周五的日期范围
- 周数从当年1月1日开始计算

## Output Location

默认输出路径：`e:\系统文件夹\Desktop\Channing\My-Control-Odyssey\Intership\厦门卓智云投资有限公司\周报\`

文件名格式：`【周报】YYYY年MM月DD日-Name.md`

> 注：如果路径不存在，自动创建目录结构。

## Error Handling

- 如果输出目录不存在，自动创建目录
- 如果无法从现有文件中提取姓名，使用 "Name" 作为占位符
- 如果日期计算出现错误，默认使用当前周的周五日期

## Example

**输入：** "生成下周的周报"
**输出：** 文件 `【周报】2026年03月06日-Channing.md`，包含标准周报模板

**输入：** "批量生成3月份的周报"
**输出：** 生成3月份所有周的周报模板文件（共4-5个文件）
