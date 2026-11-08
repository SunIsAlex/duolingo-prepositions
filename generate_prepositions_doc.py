# -*- coding: utf-8 -*-
"""
Generate professional printable Word document for Gaokao Preposition Collocations
Special Edition for "1+3" High School Project.
"""

import json
import re
import os
from html.parser import HTMLParser
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_font(run, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, italic=False, color_rgb=(17, 24, 39)):
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), east_asia_font)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = RGBColor(*color_rgb)

def set_cell_background(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)

def set_grid_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
    tblPr.append(borders)

class HTMLToRunsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.segments = [] # list of (text, bold, italic)
        self.bold = False
        self.italic = False

    def handle_starttag(self, tag, attrs):
        if tag in ('b', 'strong'):
            self.bold = True
        elif tag in ('i', 'em'):
            self.italic = True
        elif tag == 'br':
            self.segments.append(("\n", False, False))

    def handle_endtag(self, tag):
        if tag in ('b', 'strong'):
            self.bold = False
        elif tag in ('i', 'em'):
            self.italic = False

    def handle_data(self, data):
        if data:
            self.segments.append((data, self.bold, self.italic))

def add_formatted_html_text(paragraph, html_text, base_size=9.5, base_color=(55, 65, 81)):
    parser = HTMLToRunsParser()
    parser.feed(html_text)
    for text, is_bold, is_italic in parser.segments:
        if text == "\n":
            paragraph.add_run("\n")
            continue
        run = paragraph.add_run(text)
        color = (30, 58, 138) if is_bold else base_color
        set_font(run, font_name="Calibri", east_asia_font="微软雅黑", size_pt=base_size,
                 bold=is_bold, italic=is_italic, color_rgb=color)

def main():
    questions_file = "public/js/questions.js"
    with open(questions_file, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r"const PREPOSITION_QUESTIONS = (\[.*?\]);", content, re.DOTALL)
    if not m:
        raise ValueError("Could not find PREPOSITION_QUESTIONS in " + questions_file)

    questions = json.loads(m.group(1))
    print(f"Loaded {len(questions)} questions.")

    # Create document
    doc = Document()

    # Set margins to 2.0 cm
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # ----------------------------------------------------
    # COVER / HEADER SECTION
    # ----------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(4)
    title_p.paragraph_format.space_after = Pt(2)
    r = title_p.add_run("高考英语高频核心介词与短语填空专项过关检测")
    set_font(r, font_name="Arial", east_asia_font="微软雅黑", size_pt=18, bold=True, color_rgb=(30, 58, 138))

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(10)
    r = sub_p.add_run("【1+3 贯通培养拔尖计划 · 高考真题名校统练特训卷】")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11.5, bold=True, color_rgb=(75, 85, 99))

    # Meta banner table (Scores / Class / Name / Date)
    info_table = doc.add_table(rows=1, cols=4)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_grid_borders(info_table, color="93C5FD", sz="6", val="single")

    headers_meta = [
        ("班级：________________", WD_ALIGN_PARAGRAPH.LEFT),
        ("姓名：________________", WD_ALIGN_PARAGRAPH.LEFT),
        ("日期：____月____日", WD_ALIGN_PARAGRAPH.LEFT),
        ("得分：______ / 120 分", WD_ALIGN_PARAGRAPH.RIGHT)
    ]
    for i, (text, align) in enumerate(headers_meta):
        cell = info_table.rows[0].cells[i]
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=True, color_rgb=(30, 58, 138))

    # Note / Instructions
    note_p = doc.add_paragraph()
    note_p.paragraph_format.space_before = Pt(10)
    note_p.paragraph_format.space_after = Pt(14)
    r = note_p.add_run("【考试说明】")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=True, color_rgb=(180, 83, 9))
    r = note_p.add_run("本专项训练共六大部分，涵盖高考最高频动词/形容词介词搭配、核心固定习语、易混辨析，以及作业帮与2026北京名校期中/月考真题（海淀/朝阳/人大附中/清华附中）。共 120 题，满分 120 分。请在每小题句中的横线处填写 1 个恰当的介词或短语缺词。卷末附有快速核对答卷矩阵及详尽名师考点剖析。")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9, bold=False, color_rgb=(75, 85, 99))

    # Categories definition in order
    category_order = [
        ("动词搭配", "第一部分：动词核心介词搭配专项训练", "考查重点：及物/不及物动词与核心介词（to, with, on, for, of, in 等）的精准搭配，切勿以汉语思维直译。"),
        ("形容词搭配", "第二部分：形容词与介词固定搭配专项训练", "考查重点：形容词作表语或后置修饰时的固定介词选择，如 be familiar with/to, be keen on, be patient with 等。"),
        ("介词短语", "第三部分：核心介词短语与固定习语专项训练", "考查重点：成套高频介词短语与情境表达，如 in advance, on purpose, at the expense of 等。"),
        ("易混辨析", "第四部分：高考高危易混介词辨析与考点陷阱", "考查重点：一词多介词（familiar with vs familiar to / compare to vs compare with）及'介词 to'后接动名词陷阱。"),
        ("作业帮真题", "第五部分：全国高考与名校联考真题精选（作业帮特训）", "考查重点：近三年全国高考甲/乙/新课标卷及名校模考题中完形填空与语法填空核心实战考点。"),
        ("菁师帮真题", "第六部分：2026北京名校最新期中与月考真题精选（菁师帮特训）", "考查重点：2026届海淀、朝阳、人大附中、清华附中最新高三期中/月考真题知识运用与语篇填空真题。")
    ]

    # Map questions by category
    cat_to_questions = {}
    for q in questions:
        cat = q["category"]
        if cat not in cat_to_questions:
            cat_to_questions[cat] = []
        cat_to_questions[cat].append(q)

    # ----------------------------------------------------
    # PART I: STUDENT WORKSHEET / EXAM
    # ----------------------------------------------------
    global_question_idx = 1
    # Save mapping for answer key: (global_idx, question_obj)
    ordered_questions = []

    for cat_name, part_title, part_intro in category_order:
        cat_qs = cat_to_questions.get(cat_name, [])
        if not cat_qs:
            continue

        # Section Header
        sec_p = doc.add_paragraph()
        sec_p.paragraph_format.space_before = Pt(14)
        sec_p.paragraph_format.space_after = Pt(2)
        sec_p.paragraph_format.keep_with_next = True
        
        # Add badge box for section
        r = sec_p.add_run(f"■ {part_title} （共 {len(cat_qs)} 题，每题 1 分，共 {len(cat_qs)} 分）")
        set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=12, bold=True, color_rgb=(30, 58, 138))

        # Section intro
        intro_p = doc.add_paragraph()
        intro_p.paragraph_format.space_before = Pt(1)
        intro_p.paragraph_format.space_after = Pt(8)
        intro_p.paragraph_format.keep_with_next = True
        r = intro_p.add_run(part_intro)
        set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9, bold=False, italic=True, color_rgb=(107, 114, 128))

        # Render questions
        for q in cat_qs:
            ordered_questions.append((global_question_idx, q))
            
            # Question sentence
            qp = doc.add_paragraph()
            qp.paragraph_format.space_before = Pt(4)
            qp.paragraph_format.space_after = Pt(1)
            qp.paragraph_format.line_spacing = 1.15
            qp.paragraph_format.left_indent = Cm(0.6)
            qp.paragraph_format.first_line_indent = Cm(-0.6)

            # Number
            r_num = qp.add_run(f"{global_question_idx}. ")
            set_font(r_num, font_name="Arial", east_asia_font="微软雅黑", size_pt=10.5, bold=True, color_rgb=(30, 58, 138))

            # Replace '___' in sentence with a clear underlined fill-in blank
            raw_sentence = q["sentence"]
            # Split by ___
            parts = re.split(r"_{2,}", raw_sentence)
            if len(parts) > 1:
                for idx, part in enumerate(parts):
                    if part:
                        r_text = qp.add_run(part)
                        set_font(r_text, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, color_rgb=(17, 24, 39))
                    if idx < len(parts) - 1:
                        # Add fill-in blank: underlined space
                        r_blank = qp.add_run("   ___________   ")
                        set_font(r_blank, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=True, color_rgb=(30, 58, 138))
                        r_blank.font.underline = True
            else:
                r_text = qp.add_run(raw_sentence)
                set_font(r_text, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, color_rgb=(17, 24, 39))

            # Hint & Chinese subline
            sub_p = doc.add_paragraph()
            sub_p.paragraph_format.space_before = Pt(0)
            sub_p.paragraph_format.space_after = Pt(5)
            sub_p.paragraph_format.left_indent = Cm(0.6)

            # Phrase hint tag
            r_hint_label = sub_p.add_run("【搭配提示】")
            set_font(r_hint_label, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(37, 99, 235))
            r_hint = sub_p.add_run(f"{q['phrase']}    ")
            set_font(r_hint, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(55, 65, 81))

            # Chinese translation
            r_cn_label = sub_p.add_run("【汉译】")
            set_font(r_cn_label, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(75, 85, 99))
            r_cn = sub_p.add_run(f"{q['sentence_cn']}")
            set_font(r_cn, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=False, color_rgb=(107, 114, 128))

            global_question_idx += 1

    # ----------------------------------------------------
    # PART II: ANSWER KEY & DETAILED EXPLANATIONS
    # ----------------------------------------------------
    doc.add_page_break()

    ans_title_p = doc.add_paragraph()
    ans_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ans_title_p.paragraph_format.space_before = Pt(10)
    ans_title_p.paragraph_format.space_after = Pt(2)
    r = ans_title_p.add_run("第二部分：全真参考答案与考点深度解析")
    set_font(r, font_name="Arial", east_asia_font="微软雅黑", size_pt=16, bold=True, color_rgb=(30, 58, 138))

    ans_sub_p = doc.add_paragraph()
    ans_sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ans_sub_p.paragraph_format.space_before = Pt(0)
    ans_sub_p.paragraph_format.space_after = Pt(12)
    r = ans_sub_p.add_run("（教师备课授课 · 课后自主核对 · 语法错题纠偏专用手册）")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, italic=True, color_rgb=(107, 114, 128))

    # SECTION 1: QUICK ANSWER MATRIX TABLE (10 columns: Q1-Q10, Q11-Q20...)
    matrix_heading = doc.add_paragraph()
    matrix_heading.paragraph_format.space_before = Pt(6)
    matrix_heading.paragraph_format.space_after = Pt(4)
    r = matrix_heading.add_run("◆ 120 题快速核对参考答案表（Quick Answer Matrix）")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11.5, bold=True, color_rgb=(30, 58, 138))

    # Table layout: 10 questions per row, 2 rows per group (Number row, Answer row)
    total_q = len(ordered_questions)
    cols = 10
    rows_needed = ((total_q + cols - 1) // cols) * 2

    ans_table = doc.add_table(rows=rows_needed, cols=cols)
    ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_grid_borders(ans_table, color="BFDBFE", sz="4", val="single")

    for block_idx in range((total_q + cols - 1) // cols):
        row_num_idx = block_idx * 2
        row_ans_idx = block_idx * 2 + 1
        
        row_num = ans_table.rows[row_num_idx]
        row_ans = ans_table.rows[row_ans_idx]

        for col_idx in range(cols):
            q_idx = block_idx * cols + col_idx
            cell_num = row_num.cells[col_idx]
            cell_ans = row_ans.cells[col_idx]

            set_cell_margins(cell_num, top=60, bottom=60, left=80, right=80)
            set_cell_margins(cell_ans, top=80, bottom=80, left=80, right=80)

            if q_idx < total_q:
                num, q = ordered_questions[q_idx]
                set_cell_background(cell_num, "EFF6FF")
                p_n = cell_num.paragraphs[0]
                p_n.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_n.paragraph_format.space_before = Pt(0)
                p_n.paragraph_format.space_after = Pt(0)
                r_n = p_n.add_run(f"题 {num}")
                set_font(r_n, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(30, 58, 138))

                set_cell_background(cell_ans, "FFFFFF")
                p_a = cell_ans.paragraphs[0]
                p_a.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_a.paragraph_format.space_before = Pt(0)
                p_a.paragraph_format.space_after = Pt(0)
                r_a = p_a.add_run(q["answer"])
                set_font(r_a, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=True, color_rgb=(185, 28, 28))
            else:
                set_cell_background(cell_num, "F9FAFB")
                set_cell_background(cell_ans, "F9FAFB")

    # SECTION 2: DETAILED GRAMMAR EXPLANATIONS
    detail_heading = doc.add_paragraph()
    detail_heading.paragraph_format.space_before = Pt(16)
    detail_heading.paragraph_format.space_after = Pt(6)
    detail_heading.paragraph_format.keep_with_next = True
    r = detail_heading.add_run("◆ 120 题核心考点精析与名师讲义（Detailed Collocation Guide）")
    set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=12, bold=True, color_rgb=(30, 58, 138))

    current_cat = None
    for num, q in ordered_questions:
        if q["category"] != current_cat:
            current_cat = q["category"]
            cat_p = doc.add_paragraph()
            cat_p.paragraph_format.space_before = Pt(12)
            cat_p.paragraph_format.space_after = Pt(4)
            cat_p.paragraph_format.keep_with_next = True
            r = cat_p.add_run(f"【{current_cat} 专项解析】")
            set_font(r, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11, bold=True, color_rgb=(29, 78, 216))

        # Item container
        item_p = doc.add_paragraph()
        item_p.paragraph_format.space_before = Pt(4)
        item_p.paragraph_format.space_after = Pt(2)
        item_p.paragraph_format.keep_with_next = True
        item_p.paragraph_format.left_indent = Cm(0.4)

        # Number & Phrase
        r_num = item_p.add_run(f"第 {num} 题：")
        set_font(r_num, font_name="Arial", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(30, 58, 138))

        # Complete phrase
        complete_phrase = q["phrase"].replace("___", q["answer"])
        r_phrase = item_p.add_run(f"{complete_phrase}   ")
        set_font(r_phrase, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(17, 24, 39))

        # Answer badge
        r_ans_label = item_p.add_run("【标准答案】 ")
        set_font(r_ans_label, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=True, color_rgb=(185, 28, 28))
        ans_str = q["answer"]
        if len(q.get("acceptable", [])) > 1:
            alt_answers = [a for a in q["acceptable"] if a.lower() != q["answer"].lower()]
            if alt_answers:
                ans_str += f" (亦可接受: {', '.join(alt_answers)})"
        r_ans = item_p.add_run(f"{ans_str}   ")
        set_font(r_ans, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=True, color_rgb=(185, 28, 28))

        # Tags badge
        tags_str = " · ".join(q.get("tags", []))
        if tags_str:
            r_tags = item_p.add_run(f"[{tags_str}]")
            set_font(r_tags, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=False, color_rgb=(107, 114, 128))

        # Explanation paragraph
        exp_p = doc.add_paragraph()
        exp_p.paragraph_format.space_before = Pt(1)
        exp_p.paragraph_format.space_after = Pt(6)
        exp_p.paragraph_format.left_indent = Cm(0.8)
        exp_p.paragraph_format.line_spacing = 1.15

        add_formatted_html_text(exp_p, q["explanation"], base_size=9.5, base_color=(55, 65, 81))

    output_filename = "高考英语高频核心介词搭配专项训练与过关测试（1+3项目专训版）.docx"
    doc.save(output_filename)
    print(f"Successfully generated: {output_filename} ({os.path.getsize(output_filename)} bytes)")

if __name__ == "__main__":
    main()
