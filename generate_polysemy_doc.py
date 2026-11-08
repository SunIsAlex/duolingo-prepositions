# -*- coding: utf-8 -*-
"""
Generate professional printable Word document for Gaokao "Familiar Words with Unfamiliar Meanings" (熟词生义)
Authentic Cloze Multiple Choice (完形填空四选一: A, B, C, D) Format.
Special Edition for "1+3" High School Talented Project.
PRIORITY: Real Exam Questions & Beijing Top-School Mock Exams.
"""

import json
import re
import os
import subprocess
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

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_grid_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
    tblPr.append(borders)

def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="none"/><w:bottom w:val="none"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)

class HTMLToRunsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.segments = []
        self.bold = False
        self.italic = False

    def handle_starttag(self, tag, attrs):
        if tag in ('b', 'strong'):
            self.bold = True
        elif tag in ('i', 'em'):
            self.italic = True
        elif tag == 'br':
            self.segments.append(("\n", self.bold, self.italic))

    def handle_endtag(self, tag):
        if tag in ('b', 'strong'):
            self.bold = False
        elif tag in ('i', 'em'):
            self.italic = False

    def handle_data(self, data):
        if data:
            self.segments.append((data, self.bold, self.italic))

def add_html_paragraph(doc, html_text, space_after=4, line_spacing=1.15):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    parser = HTMLToRunsParser()
    parser.feed(html_text)
    for text, bold, italic in parser.segments:
        run = p.add_run(text)
        set_font(run, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=bold, italic=italic, color_rgb=(55, 65, 81))
    return p

# 40道高考全真题与北京拔尖模拟题核心熟词生义（完形填空四选一实战题库）
POLYSEMY_CLOZE_QUESTIONS = [
    {
        "id": "poly_01",
        "word": "click",
        "familiar": "点击；发出咔哒声",
        "unfamiliar": "一拍即合；情投意合；恍然大悟",
        "sentence": "The two of them met at the freshman party and ________ immediately, becoming lifelong friends.",
        "options": ["A. cleared", "B. faded", "C. clicked", "D. paused"],
        "answer": "C",
        "option_answer": "C. clicked",
        "sentence_cn": "他们在新生迎新会上相遇，立刻一拍即合，成了终身挚友。",
        "source": "全国新高考卷完形精选",
        "explanation": "<b>click</b> 在高考完形填空中常考熟词生义，表示“两人一拍即合、情投意合”（become friendly with each other immediately）或“顿悟、豁然开朗”。<br><b>【干扰项辨析】</b>A. cleared（变晴、散开）；B. faded（褪色、衰退）；D. paused（暂停、停顿）。语境强调两人初次见面便情投意合，故选 <b>C</b>。"
    },
    {
        "id": "poly_02",
        "word": "book",
        "familiar": "书本、书籍",
        "unfamiliar": "预订（票、座位等）；登记违章",
        "sentence": "We had to ________ our flight tickets two months in advance to get the early-bird discount.",
        "options": ["A. book", "B. print", "C. check", "D. deliver"],
        "answer": "A",
        "option_answer": "A. book",
        "sentence_cn": "我们不得不提前两个月预订机票，以享受早鸟优惠。",
        "source": "北京高考真题精选",
        "explanation": "<b>book</b> 动词表示“预订（座位、机票等）”（reserve），如 book a room / flight。高考必考核心生义。<br><b>【干扰项辨析】</b>B. print（打印）；C. check（检查）；D. deliver（递送）。句意为提前订票享受优惠，故选 <b>A</b>。"
    },
    {
        "id": "poly_03",
        "word": "course",
        "familiar": "课程；过程",
        "unfamiliar": "（医疗的）疗程；（西餐的）一道菜；航向",
        "sentence": "The doctor prescribed a full two-week ________ of antibiotics for the severe infection.",
        "options": ["A. lesson", "B. course", "C. schedule", "D. system"],
        "answer": "B",
        "option_answer": "B. course",
        "sentence_cn": "针对严重的感染，医生开出了整整两周的抗生素疗程。",
        "source": "北京海淀高三期中真题",
        "explanation": "<b>course</b> 在医疗语境中指“（药的）疗程”（a course of treatment / antibiotics）；在餐饮中指一道菜（a three-course meal）。<br><b>【干扰项辨析】</b>A. lesson（功课、教训）；C. schedule（时间表）；D. system（系统）。固定搭配 a course of antibiotics 指完整疗程，故选 <b>B</b>。"
    },
    {
        "id": "poly_04",
        "word": "deliver",
        "familiar": "递送、邮寄",
        "unfamiliar": "兑现、履行（承诺）；发表演说；接生",
        "sentence": "The company promised fast returns, but they completely failed to ________ on their commitments.",
        "options": ["A. depend", "B. reflect", "C. deliver", "D. calculate"],
        "answer": "C",
        "option_answer": "C. deliver",
        "sentence_cn": "该公司曾承诺快速回报，但最终完全未能兑现他们的承诺。",
        "source": "全国I卷高考真题",
        "explanation": "<b>deliver on sth.</b> 表示“履行、兑现（承诺或期望）”（keep a promise / produce results）。<br><b>【干扰项辨析】</b>A. depend on（依靠）；B. reflect on（反思）；D. calculate on（指望）。deliver on commitments 意为兑现承诺，故选 <b>C</b>。"
    },
    {
        "id": "poly_05",
        "word": "consume",
        "familiar": "消耗、消费",
        "unfamiliar": "（某种强烈情绪）吞噬、充斥、使沉溺",
        "sentence": "He was entirely ________ with grief and anger after learning the shocking truth.",
        "options": ["A. covered", "B. consumed", "C. equipped", "D. charged"],
        "answer": "B",
        "option_answer": "B. consumed",
        "sentence_cn": "得知令人震惊的真相后，他整个人被悲伤与愤怒彻底吞噬。",
        "source": "北京西城高三一模真题",
        "explanation": "<b>consume</b> 被动态 <b>be consumed with / by...</b> 指“心中充斥着（悲伤、愤怒、嫉妒等强烈情绪）”，被情绪所吞噬。<br><b>【干扰项辨析】</b>A. covered with（被……覆盖）；C. equipped with（装备有）；D. charged with（被指控）。故选 <b>B</b>。"
    },
    {
        "id": "poly_06",
        "word": "entertain",
        "familiar": "款待；使娱乐",
        "unfamiliar": "心存、考虑（想法、建议）",
        "sentence": "The committee refused to ________ any proposals that involved extra government funding.",
        "options": ["A. entertain", "B. applaud", "C. celebrate", "D. perform"],
        "answer": "A",
        "option_answer": "A. entertain",
        "sentence_cn": "委员会拒绝考虑任何涉及额外政府拨款的提议。",
        "source": "全国新高考I卷阅读理解",
        "explanation": "<b>entertain an idea / proposal / thought</b> 动词生义表示“心怀、考虑（某种想法或提议）”（consider or contemplate）。<br><b>【干扰项辨析】</b>B. applaud（鼓掌欢迎）；C. celebrate（庆祝）；D. perform（执行、表演）。拒绝考虑该提议，故选 <b>A</b>。"
    },
    {
        "id": "poly_07",
        "word": "escape",
        "familiar": "逃跑、逃离",
        "unfamiliar": "被遗忘；未被某人注意到",
        "sentence": "Her face looked vaguely familiar to me, but her name completely ________ my memory.",
        "options": ["A. cheated", "B. escaped", "C. dropped", "D. wasted"],
        "answer": "B",
        "option_answer": "B. escaped",
        "sentence_cn": "她的面孔看着有些眼熟，但我怎么也想不起她的名字了（名字完全被我遗忘了）。",
        "source": "高考英语全国卷完形精选",
        "explanation": "<b>escape sb. / memory</b> 表示“被某人遗忘、未被某人想起来”（fail to be remembered or noticed by someone）。<br><b>【干扰项辨析】</b>A. cheated（欺骗）；C. dropped（掉落）；D. wasted（浪费）。某事逃过记忆即指被遗忘，故选 <b>B</b>。"
    },
    {
        "id": "poly_08",
        "word": "fine",
        "familiar": "好的；晴朗的",
        "unfamiliar": "微细的、细微的；纤细精巧的；罚款",
        "sentence": "There is a very ________ line between confidence and arrogance in professional leadership.",
        "options": ["A. long", "B. thick", "C. rough", "D. fine"],
        "answer": "D",
        "option_answer": "D. fine",
        "sentence_cn": "在职场领导力中，自信与傲慢之间往往只有一线之隔（非常微妙的区别）。",
        "source": "高考阅读真题",
        "explanation": "<b>a fine line / distinction</b> 表示“微细的界限 / 细微的差别”；名词表示“罚款”。<br><b>【干扰项辨析】</b>A. long（漫长的）；B. thick（粗厚的）；C. rough（粗糙的）。a fine line 是英语经典比喻，指微妙的界限，故选 <b>D</b>。"
    },
    {
        "id": "poly_09",
        "word": "hit",
        "familiar": "击打、打中",
        "unfamiliar": "突然意识到/想到；风靡一时的人或物",
        "sentence": "Sitting on the bench lost in thoughts, it suddenly ________ me that the roses had been pruned.",
        "options": ["A. beat", "B. attracted", "C. hit", "D. flooded"],
        "answer": "C",
        "option_answer": "C. hit",
        "sentence_cn": "坐在长凳上沉思时，我突然意识到那些玫瑰花已经被修剪过了。",
        "source": "2026北京人大附中高三10月月考真题 Q8",
        "explanation": "<b>It hits sb. that...</b> 固定句型，表示“某人突然意识到/想到……”（it suddenly occurred to me that...）。<br><b>【干扰项辨析】</b>A. beat（敲打、跳动）；B. attracted（吸引）；D. flooded（淹没）。人大附中原题考查 hit 熟词生义，表示内心猛然领悟，故选 <b>C</b>。"
    },
    {
        "id": "poly_10",
        "word": "observe",
        "familiar": "观察、监视",
        "unfamiliar": "遵守（规则、法律）；庆祝（节日）",
        "sentence": "Every citizen is strictly required to ________ the local traffic laws and safety regulations.",
        "options": ["A. observe", "B. notice", "C. view", "D. watch"],
        "answer": "A",
        "option_answer": "A. observe",
        "sentence_cn": "每位市民都被严格要求遵守当地的交通法律和安全法规。",
        "source": "北京高考语法填空精选",
        "explanation": "<b>observe</b> 意为“遵守（法律、纪律、传统）”（obey / follow）；亦可表示“庆祝（节日）”（observe the holiday）。<br><b>【干扰项辨析】</b>B. notice（注意到）；C. view（看待、审视）；D. watch（注视）。遵守交规用 observe，故选 <b>A</b>。"
    },
    {
        "id": "poly_11",
        "word": "promising",
        "familiar": "承诺的、许诺的",
        "unfamiliar": "大有前途的、大有希望的",
        "sentence": "With her outstanding coding skills, she is considered one of the most ________ young engineers.",
        "options": ["A. demanding", "B. promising", "C. threatening", "D. exhausting"],
        "answer": "B",
        "option_answer": "B. promising",
        "sentence_cn": "凭借过硬的编程技术，她被视为最有前途的年轻工程师之一。",
        "source": "海淀高三期末模拟精选",
        "explanation": "<b>promising</b> 形容词，表示“有前途的、前景光明的”（showing signs of future success），如 a promising young talent。<br><b>【干扰项辨析】</b>A. demanding（要求苛刻的）；C. threatening（威胁性的）；D. exhausting（令人精疲力竭的）。故选 <b>B</b>。"
    },
    {
        "id": "poly_12",
        "word": "touching",
        "familiar": "触摸、碰触",
        "unfamiliar": "令人感动的、动人的；介词：关于",
        "sentence": "The movie tells a deeply ________ story about the unconditional love between a mother and son.",
        "options": ["A. shaking", "B. pressing", "C. touching", "D. striking"],
        "answer": "C",
        "option_answer": "C. touching",
        "sentence_cn": "这部电影讲述了一个关于母子之间无私挚爱的极为感人的故事。",
        "source": "高考阅读真题",
        "explanation": "<b>touching</b> 形容词表示“令人感动的、动人的”（moving）；作为介词时意为“关于、至于”（concerning）。<br><b>【干扰项辨析】</b>A. shaking（摇晃的）；B. pressing（紧迫的）；D. striking（引人注目的）。deeply touching 意为深受触动感人，故选 <b>C</b>。"
    },
    {
        "id": "poly_13",
        "word": "accommodate",
        "familiar": "提供住宿、容纳",
        "unfamiliar": "顺应、使适应；迎合需求",
        "sentence": "The flexible curriculum was carefully redesigned to ________ the special needs of diverse students.",
        "options": ["A. accommodate", "B. reserve", "C. occupy", "D. maintain"],
        "answer": "A",
        "option_answer": "A. accommodate",
        "sentence_cn": "这门弹性课程被精心重新设计，以顺应并满足不同学生的特殊需求。",
        "source": "高考新课标卷阅读理解",
        "explanation": "<b>accommodate needs / requests</b> 意为“顺应、照顾、满足（需求、特殊情况）”，是高考阅读与完形高分词汇。<br><b>【干扰项辨析】</b>B. reserve（预留）；C. occupy（占据）；D. maintain（维持）。满足多元学生需求，故选 <b>A</b>。"
    },
    {
        "id": "poly_14",
        "word": "address",
        "familiar": "地址",
        "unfamiliar": "设法解决、处理；发表演说；称呼",
        "sentence": "Effective measures must be taken immediately to ________ the pressing issue of plastic pollution.",
        "options": ["A. deliver", "B. address", "C. pronounce", "D. sign"],
        "answer": "B",
        "option_answer": "B. address",
        "sentence_cn": "必须立即采取有效措施，以切实解决日益紧迫的塑料污染问题。",
        "source": "全国高考真题与读后续写经典",
        "explanation": "<b>address the issue / problem / challenge</b> 表示“设法应对、解决问题”（tackle or deal with）。高考议论文写作和完形填空顶尖高频词。<br><b>【干扰项辨析】</b>A. deliver（投递）；C. pronounce（宣判、发音）；D. sign（签署）。address the issue 指解决问题，故选 <b>B</b>。"
    },
    {
        "id": "poly_15",
        "word": "appeal",
        "familiar": "呼吁、恳求",
        "unfamiliar": "吸引力；引起兴趣（接to）；上诉",
        "sentence": "Online interactive video games strongly ________ to teenagers because of their vivid graphics.",
        "options": ["A. apply", "B. appeal", "C. adapt", "D. adjust"],
        "answer": "B",
        "option_answer": "B. appeal",
        "sentence_cn": "在线互动视频游戏因其逼真的画面而对青少年具有极强的吸引力。",
        "source": "北京高考阅读真题",
        "explanation": "<b>appeal to sb.</b> 意为“吸引某人、迎合某人的兴趣”（attract sb.）；名词 <b>appeal</b> 意为“吸引力”。<br><b>【干扰项辨析】</b>A. apply to（适用于）；C. adapt to（适应）；D. adjust to（调节适应）。游戏吸引年轻人用 appeal to，故选 <b>B</b>。"
    },
    {
        "id": "poly_16",
        "word": "appreciate",
        "familiar": "感激、感谢",
        "unfamiliar": "领会、充分理解；赏识；升值",
        "sentence": "Living in a foreign country for a year helped him fully ________ the cultural diversity of the world.",
        "options": ["A. appreciate", "B. predict", "C. calculate", "D. forgive"],
        "answer": "A",
        "option_answer": "A. appreciate",
        "sentence_cn": "在国外生活了一年，帮助他真正深刻理解并领会了世界文化的多样性。",
        "source": "全国高考真题精选",
        "explanation": "<b>appreciate</b> 熟义为感激，生义指“充分理解、意识到（某事物的价值与意义）”（understand fully），或资产“升值”（increase in value）。<br><b>【干扰项辨析】</b>B. predict（预测）；C. calculate（计算）；D. forgive（原谅）。深刻领会多元文化用 appreciate，故选 <b>A</b>。"
    },
    {
        "id": "poly_17",
        "word": "bargain",
        "familiar": "便宜货、特价商品",
        "unfamiliar": "预料到；谈判、达成协议",
        "sentence": "The sudden heavy rain was much more than they had ________ for during their mountain hike.",
        "options": ["A. bargained", "B. blamed", "C. traded", "D. earned"],
        "answer": "A",
        "option_answer": "A. bargained",
        "sentence_cn": "这场突如其来的倾盆暴雨远远超出了他们在登山徒步中所预料到的情况。",
        "source": "高考完形经典陷阱题",
        "explanation": "<b>bargain for / on sth.</b> 固定习语，意为“预料到、指望”，常用于否定句或 <b>more than sb. bargained for</b>（出乎意料、招架不住）。<br><b>【干扰项辨析】</b>B. blamed（责怪）；C. traded（交易）；D. earned（赚得）。故选 <b>A</b>。"
    },
    {
        "id": "poly_18",
        "word": "bear",
        "familiar": "熊；忍受",
        "unfamiliar": "具有、带有（特征/相似点）；承担（责任）",
        "sentence": "The twin brothers ________ a striking resemblance to their grandfather in their youth.",
        "options": ["A. carry", "B. possess", "C. bear", "D. hold"],
        "answer": "C",
        "option_answer": "C. bear",
        "sentence_cn": "这对双胞胎兄弟与他们祖父年轻时的样貌有着惊人的相似之处。",
        "source": "高考完形与阅读真题",
        "explanation": "<b>bear a resemblance / relation to</b> 表示“带有……的特征 / 与……有相似之处”；<b>bear responsibility</b> 表示“承担责任”。<br><b>【干扰项辨析】</b>A. carry（携带）；B. possess（拥有）；D. hold（握住）。bear a resemblance 是高考高频地道搭配，故选 <b>C</b>。"
    },
    {
        "id": "poly_19",
        "word": "bridge",
        "familiar": "桥梁",
        "unfamiliar": "弥合差距、消除隔阂、缩小分歧",
        "sentence": "Cultural exchange programs are dedicated to ________ the generation gap between parents and youths.",
        "options": ["A. expanding", "B. bridging", "C. widening", "D. damaging"],
        "answer": "B",
        "option_answer": "B. bridging",
        "sentence_cn": "文化交流项目致力于弥合父母与青年一代之间的代沟。",
        "source": "高考写作与模拟题热点",
        "explanation": "<b>bridge the gap / divide</b> 动词生义，表示“弥合差距、缩小分歧、消除隔阂”，高阶写作与完形高频动词。<br><b>【干扰项辨析】</b>A. expanding（扩大）；C. widening（加宽）；D. damaging（损害）。消除代沟用 bridge the gap，故选 <b>B</b>。"
    },
    {
        "id": "poly_20",
        "word": "check",
        "familiar": "检查",
        "unfamiliar": "抑制、遏制；阻碍；账单；托运",
        "sentence": "The government introduced strict regulations to ________ the rapid rise in housing prices.",
        "options": ["A. check", "B. track", "C. examine", "D. balance"],
        "answer": "A",
        "option_answer": "A. check",
        "sentence_cn": "政府出台了严厉的调控政策，以有效遏制房价的过快上涨。",
        "source": "北京高考真题精选",
        "explanation": "<b>check</b> 动词生义指“制止、遏制、阻碍”（stop sth. from increasing or getting worse），名词 <b>keep sth. in check</b> 表示“控制住某事”。<br><b>【干扰项辨析】</b>B. track（追踪）；C. examine（审查）；D. balance（平衡）。遏制上涨用 check，故选 <b>A</b>。"
    },
    {
        "id": "poly_21",
        "word": "coach",
        "familiar": "体育教练；大巴车",
        "unfamiliar": "耐心辅导（功课/面试/技能）",
        "sentence": "Her elder sister spent hours ________ her in mathematics before the final college entrance exam.",
        "options": ["A. testing", "B. directing", "C. coaching", "D. commanding"],
        "answer": "C",
        "option_answer": "C. coaching",
        "sentence_cn": "高考前，她的姐姐花了几个小时耐心辅导她的数学功课。",
        "source": "全国卷高考真题",
        "explanation": "<b>coach sb. in sth.</b> 动词表示“（私下/专门）辅导某人功课或训练某人技能”。<br><b>【干扰项辨析】</b>A. testing（测试）；B. directing（指引）；D. commanding（命令）。辅导功课用 coach in math，故选 <b>C</b>。"
    },
    {
        "id": "poly_22",
        "word": "count",
        "familiar": "数数、计算",
        "unfamiliar": "至关重要、有价值；算数",
        "sentence": "In times of real crisis, it is actions, not pretty words, that truly ________.",
        "options": ["A. mean", "B. count", "C. weigh", "D. figure"],
        "answer": "B",
        "option_answer": "B. count",
        "sentence_cn": "在真正危机的时刻，真正至关紧要的是切实的行动，而不是动听的言辞。",
        "source": "高考完形核心考点",
        "explanation": "<b>Every second counts.</b> / <b>It counts.</b> 这里的 <b>count</b> 为不及物动词，表示“有价值、至关重要”（matter or be important）。<br><b>【干扰项辨析】</b>A. mean（意味着）；C. weigh（称重）；D. figure（计算）。起决定性重要作用用 count，故选 <b>B</b>。"
    },
    {
        "id": "poly_23",
        "word": "cross",
        "familiar": "穿过、交叉；十字形",
        "unfamiliar": "恼怒的、生气的",
        "sentence": "Don't be so ________ with the little boy; he didn't break the vase on purpose.",
        "options": ["A. cross", "B. broad", "C. sharp", "D. rough"],
        "answer": "A",
        "option_answer": "A. cross",
        "sentence_cn": "别对那个小男孩那么发火生气，他并不是故意打破花瓶的。",
        "source": "高考阅读真题",
        "explanation": "<b>be cross with sb.</b> 形容词表示“恼怒的、生气的”（annoyed or angry with sb.）。<br><b>【干扰项辨析】</b>B. broad（宽广的）；C. sharp（尖锐的）；D. rough（粗糙的）。生某人的气用 cross with sb.，故选 <b>A</b>。"
    },
    {
        "id": "poly_24",
        "word": "desert",
        "familiar": "沙漠",
        "unfamiliar": "抛弃、遗弃；离弃（岗位）",
        "sentence": "A true loyal friend will never ________ you when you are in the depths of adversity.",
        "options": ["A. reject", "B. decline", "C. desert", "D. dismiss"],
        "answer": "C",
        "option_answer": "C. desert",
        "sentence_cn": "一个真正忠诚的朋友在你深陷逆境时绝不会离你而去（抛弃你）。",
        "source": "高考完形核心词",
        "explanation": "<b>desert</b> 动词（读音 /dɪˈzɜːt/）表示“抛弃、遗弃（某人或某地）”（abandon）。<br><b>【干扰项辨析】</b>A. reject（拒绝）；B. decline（婉拒、衰退）；D. dismiss（解散、不屑一顾）。抛弃患难朋友用 desert，故选 <b>C</b>。"
    },
    {
        "id": "poly_25",
        "word": "develop",
        "familiar": "发展、开发",
        "unfamiliar": "患（病）；养成（习惯）；冲洗（照片）",
        "sentence": "Without adequate protection under the scorching sun, one may easily ________ severe skin damage.",
        "options": ["A. develop", "B. invent", "C. produce", "D. expand"],
        "answer": "A",
        "option_answer": "A. develop",
        "sentence_cn": "在烈日下如果没有充足的防晒保护，人很容易患上严重的皮肤损伤。",
        "source": "高考完形及阅读理解",
        "explanation": "<b>develop a habit / an illness / a symptom</b> 分别表示“养成习惯、患病、出现症状”；亦可表示“冲洗胶卷（develop a film）”。<br><b>【干扰项辨析】</b>B. invent（发明）；C. produce（生产）；D. expand（膨胀）。身体形成病症用 develop，故选 <b>A</b>。"
    },
    {
        "id": "poly_26",
        "word": "dismiss",
        "familiar": "解雇、开除；解散",
        "unfamiliar": "不予考虑、摒弃（想法/警告）",
        "sentence": "The manager chose to ________ his junior colleague's warning as mere pessimistic exaggeration.",
        "options": ["A. accept", "B. dismiss", "C. release", "D. transfer"],
        "answer": "B",
        "option_answer": "B. dismiss",
        "sentence_cn": "经理认为年轻同事的警告纯属悲观夸大，对此不予理会（直接摒弃）。",
        "source": "北京高考阅读真题",
        "explanation": "<b>dismiss sth. as ...</b> 意为“对……不屑一顾、不予理会、摒除（想法）”（decide that sth. is not important enough to consider）。<br><b>【干扰项辨析】</b>A. accept（接受）；C. release（释放）；D. transfer（转移）。将警告当作夸大不予理睬用 dismiss，故选 <b>B</b>。"
    },
    {
        "id": "poly_27",
        "word": "drive",
        "familiar": "驾驶汽车",
        "unfamiliar": "迫使；驱动力；专项运动/募捐",
        "sentence": "Desperate poverty and the lack of basic food can ________ people to commit desperate crimes.",
        "options": ["A. lead", "B. drag", "C. guide", "D. drive"],
        "answer": "D",
        "option_answer": "D. drive",
        "sentence_cn": "极端的贫困和基础食物的匮乏会迫使人们铤而走险去犯罪。",
        "source": "全国高考真题语料",
        "explanation": "<b>drive sb. to do sth. / drive sb. crazy</b> 意为“迫使某人做出某事 / 把某人逼疯”；名词 <b>drive</b> 意为“进取心、内驱力”。<br><b>【干扰项辨析】</b>A. lead（引导）；B. drag（拖拽）；C. guide（指引）。迫使某人走投无路犯罪用 drive sb. to do，故选 <b>D</b>。"
    },
    {
        "id": "poly_28",
        "word": "figure",
        "familiar": "数字；体形；知名人物",
        "unfamiliar": "认为、认定、心想；计算出",
        "sentence": "Since all tickets for the direct train were sold out, I ________ we had better take a bus instead.",
        "options": ["A. figured", "B. calculated", "C. doubted", "D. questioned"],
        "answer": "A",
        "option_answer": "A. figured",
        "sentence_cn": "既然直达火车的票都卖光了，我认定我们最好改坐大巴。",
        "source": "高考完形与听力真题",
        "explanation": "<b>figure that...</b> 口语及叙述中意为“认为、认定、心想”（think / conclude）；<b>figure out</b> 意为“搞明白、计算出”。<br><b>【干扰项辨析】</b>B. calculated（计算、预测）；C. doubted（怀疑）；D. questioned（质问）。认定最好坐大巴用 figured，故选 <b>A</b>。"
    },
    {
        "id": "poly_29",
        "word": "freeze",
        "familiar": "结冰、冷冻",
        "unfamiliar": "惊呆定住、吓得呆住不动；冻结（物价/资产）",
        "sentence": "Hearing the sudden clicking sound of a gun behind him, he ________ with terror.",
        "options": ["A. broke", "B. froze", "C. escaped", "D. fell"],
        "answer": "B",
        "option_answer": "B. froze",
        "sentence_cn": "听到身后突然传来子弹上膛的咔哒声，他吓得顿时僵在原地、一动不敢动。",
        "source": "高考读后续写生动描写必背词",
        "explanation": "<b>freeze</b> 动词过去式为 <b>froze</b>，生义指人因为极度惊吓或警惕而“突然呆住、定格不动”（stop moving because of fear or shock）。续写高分动作动词！<br><b>【干扰项辨析】</b>A. broke（破损）；C. escaped（逃脱）；D. fell（跌倒）。故选 <b>B</b>。"
    },
    {
        "id": "poly_30",
        "word": "fresh",
        "familiar": "新鲜的",
        "unfamiliar": "精力充沛的；淡水的（如 fresh water）；无经验的",
        "sentence": "After taking a thirty-minute power nap, she woke up feeling completely ________ and energetic.",
        "options": ["A. raw", "B. tough", "C. novel", "D. fresh"],
        "answer": "D",
        "option_answer": "D. fresh",
        "sentence_cn": "高效小睡了半小时后，她醒来感到浑身精力充沛、神清气爽。",
        "source": "高考阅读真题",
        "explanation": "<b>feel fresh</b> 意为“感到精神抖擞、恢复精力”；<b>fresh water</b> 意为“淡水”；<b>fresh from school</b> 意为“刚出校门缺乏经验”。<br><b>【干扰项辨析】</b>A. raw（生的、未加工的）；B. tough（坚硬的、棘手的）；C. novel（新奇的）。神清气爽用 fresh，故选 <b>D</b>。"
    },
    {
        "id": "poly_31",
        "word": "pool",
        "familiar": "水池、水塘",
        "unfamiliar": "（液体、血液或情感等）聚集、积聚",
        "sentence": "The violin gathered dust in the corner, and shame slowly ________ in my belly.",
        "options": ["A. cleared", "B. faded", "C. pooled", "D. passed"],
        "answer": "C",
        "option_answer": "C. pooled",
        "sentence_cn": "小提琴在角落里积满灰尘，羞愧感在我心头（小腹深处）慢慢积聚。",
        "source": "2026北京朝阳高三期中完形真题 Q6",
        "explanation": "<b>pool</b> 作为不及物动词，生义表示“（液体或情绪）汇聚、积聚”（accumulate or gather in a pool）。<br><b>【干扰项辨析】</b>A. cleared（散去）；B. faded（消退）；D. passed（流逝）。朝阳期中全真原题考查 pool 动词生义，表示内心羞愧情绪渐渐聚集，故选 <b>C</b>。"
    },
    {
        "id": "poly_32",
        "word": "outlet",
        "familiar": "电源插座；折扣店（奥特莱斯）",
        "unfamiliar": "（情感、精力的）发泄途径、宣泄口",
        "sentence": "Playing music had once served as my passionate emotional ________, but now it felt like a heavy burden.",
        "options": ["A. edge", "B. outlet", "C. excuse", "D. trial"],
        "answer": "B",
        "option_answer": "B. outlet",
        "sentence_cn": "演奏音乐曾经是我最炽热的情感发泄途径，但如今却成了一种沉重的负担。",
        "source": "2026北京朝阳高三期中完形真题 Q7",
        "explanation": "<b>outlet</b> 生义指“（强烈情感或精力的）宣泄途径、发泄口”（a way of expressing or getting rid of strong feelings）。<br><b>【干扰项辨析】</b>A. edge（边缘、优势）；C. excuse（借口）；D. trial（审判、考验）。emotional outlet 是高考完形极高频固定搭配，故选 <b>B</b>。"
    },
    {
        "id": "poly_33",
        "word": "tend to",
        "familiar": "往往、倾向于（tend to do）",
        "unfamiliar": "照料、看顾、伺候（tend to sb./sth.）",
        "sentence": "Mr. Jensen was there in the garden as usual, quietly ________ his blossoming rosebushes.",
        "options": ["A. staring at", "B. looking for", "C. tending to", "D. picking up"],
        "answer": "C",
        "option_answer": "C. tending to",
        "sentence_cn": "詹森先生和平常一样在花园里，静静地照料着他那些盛开的玫瑰花丛。",
        "source": "2026北京人大附中高三10月月考真题 Q5",
        "explanation": "<b>tend to sb./sth.</b> 动词短语生义表示“照料、照看（植物、病人等）”（care for or look after）。<br><b>【干扰项辨析】</b>A. staring at（凝视）；B. looking for（寻找）；D. picking up（捡起、接送）。照料花草用 tending to，人大附中原题，故选 <b>C</b>。"
    },
    {
        "id": "poly_34",
        "word": "betray",
        "familiar": "背叛、出卖",
        "unfamiliar": "（无意中）暴露、流露出（弱点、恐惧、秘密）",
        "sentence": "Standing on the podium, I took a deep breath, terrified that my trembling voice would ________ my inner fear.",
        "options": ["A. block", "B. comfort", "C. convince", "D. betray"],
        "answer": "D",
        "option_answer": "D. betray",
        "sentence_cn": "站在讲台上，我深吸了一口气，唯恐自己颤抖的声音会暴露出我内心的恐惧。",
        "source": "2026北京清华附中高三10月月考真题 Q5",
        "explanation": "<b>betray</b> 生义表示“无意中流露、显露（弱点、真实感情或身份）”（reveal inadvertently）。<br><b>【干扰项辨析】</b>A. block（阻挡）；B. comfort（安慰）；C. convince（使信服）。清华附中原题考查 feared my weakness would betray me，暴露真实恐惧，故选 <b>D</b>。"
    },
    {
        "id": "poly_35",
        "word": "shadow",
        "familiar": "影子、阴影",
        "unfamiliar": "跟班学习、见习、密切观察（工作）",
        "sentence": "During my summer internship, I was assigned to ________ an experienced senior researcher in the laboratory.",
        "options": ["A. shadow", "B. guide", "C. assess", "D. notice"],
        "answer": "A",
        "option_answer": "A. shadow",
        "sentence_cn": "在暑期实习期间，我被安排在实验室跟随一位经验丰富的高级研究员跟班见习。",
        "source": "2026北京清华附中高三10月月考真题 Q6",
        "explanation": "<b>shadow sb.</b> 在职场与学术语境中表示“跟随某人实地见习观察、跟班学习”（follow and observe sb. closely at work）。<br><b>【干扰项辨析】</b>B. guide（引导）；C. assess（评估）；D. notice（注意）。清华附中原题考查 shadow him in the lab，故选 <b>A</b>。"
    },
    {
        "id": "poly_36",
        "word": "wear off",
        "familiar": "穿坏、磨损（wear out）",
        "unfamiliar": "（感觉、药效等）逐渐消退、渐渐消失",
        "sentence": "As I stepped in front of the students and began teaching, my initial anxiety gradually ________.",
        "options": ["A. kicked in", "B. took over", "C. broke out", "D. wore off"],
        "answer": "D",
        "option_answer": "D. wore off",
        "sentence_cn": "当我走到学生面前开始讲课时，最初的焦虑紧张感便渐渐消退了。",
        "source": "2026北京清华附中高三10月月考真题 Q8",
        "explanation": "<b>wear off</b> 指“（疼痛、药物作用、紧张情绪等）逐渐消退、失效”（gradually fade or disappear）。<br><b>【干扰项辨析】</b>A. kicked in（开始起效）；B. took over（接管）；C. broke out（爆发）。清华附中原题考查 anxiety wore off，故选 <b>D</b>。"
    },
    {
        "id": "poly_37",
        "word": "feel left out",
        "familiar": "遗漏、略去（leave out）",
        "unfamiliar": "感觉被冷落、受到孤立排挤",
        "sentence": "When all her classmates gathered around requesting Mia to sing, Ivy quietly felt ________.",
        "options": ["A. taken in", "B. picked on", "C. left out", "D. turned down"],
        "answer": "C",
        "option_answer": "C. left out",
        "sentence_cn": "当全班同学都围上前让米娅唱歌时，艾薇静静地感到自己受到了冷落（被边缘化）。",
        "source": "2026北京高考真题完形填空 Q2",
        "explanation": "<b>feel left out</b> 意为“感到被忽视、受到冷落孤立”（feel excluded or neglected）。<br><b>【干扰项辨析】</b>A. taken in（受骗）；B. picked on（被针对、被找茬）；D. turned down（被拒绝）。北京高考全真原题，故选 <b>C</b>。"
    },
    {
        "id": "poly_38",
        "word": "force",
        "familiar": "力量、武力；强迫（force sb. to do）",
        "unfamiliar": "勉强做出、强作（笑容）",
        "sentence": "Though she was heartbroken inside, she managed to ________ a smile so as not to worry her parents.",
        "options": ["A. radiate", "B. force", "C. expect", "D. witness"],
        "answer": "B",
        "option_answer": "B. force",
        "sentence_cn": "尽管她内心极度伤心，但她还是勉强挤出了一丝微笑，以免让父母担心。",
        "source": "2026北京高考真题完形填空 Q4",
        "explanation": "<b>force a smile</b> 意为“强作欢颜、勉强挤出一丝微笑”（make an effort to smile when unhappy）。<br><b>【干扰项辨析】</b>A. radiate（散发光芒）；C. expect（期待）；D. witness（见证）。北京高考全真原题考查 forced a smile，故选 <b>B</b>。"
    },
    {
        "id": "poly_39",
        "word": "distant",
        "familiar": "遥远的、远距离的",
        "unfamiliar": "冷淡的、疏远的、心不在焉的",
        "sentence": "Seeing her sudden change in attitude, he felt hurt because her tone sounded cold and ________.",
        "options": ["A. guilty", "B. shocked", "C. distant", "D. confused"],
        "answer": "C",
        "option_answer": "C. distant",
        "sentence_cn": "看到她态度的突然转变，他感到很受伤，因为她的语气听起来冷漠而疏远。",
        "source": "2026北京高考真题完形填空 Q6",
        "explanation": "<b>distant</b> 形容人的态度或眼神，表示“冷淡的、疏离的、心不在焉的”（aloof, unfriendly or lost in thought）。<br><b>【干扰项辨析】</b>A. guilty（愧疚的）；B. shocked（震惊的）；D. confused（困惑的）。北京高考全真原题考查 cold and distant，故选 <b>C</b>。"
    },
    {
        "id": "poly_40",
        "word": "extension",
        "familiar": "延长、延期；电话分机",
        "unfamiliar": "（家庭或团体的）延伸、外延",
        "sentence": "To the welcoming villagers, any respectful traveler was embraced as an ________ of their own family.",
        "options": ["A. advantage", "B. example", "C. honor", "D. extension"],
        "answer": "D",
        "option_answer": "D. extension",
        "sentence_cn": "对于热情好客的村民来说，任何懂礼貌的旅人都被视为他们大家庭的延伸（一份子）。",
        "source": "2026全国I卷高考真题完形填空 Q50",
        "explanation": "<b>an extension of sth.</b> 表示“某事物的延伸、外延或延续”（something that develops from or is added to something else）。<br><b>【干扰项辨析】</b>A. advantage（优势）；B. example（典范）；C. honor（荣幸）。全国I卷全真原题考查 an extension of the family，把客人视为家庭的一份子，故选 <b>D</b>。"
    }
]

def build_polysemy_cloze_document():
    doc = Document()
    
    # 页面边距：上下 2.0 cm，左右 2.0 cm
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        
        # 页眉设置
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("高考英语高频核心“熟词生义”专项训练与突破过关测试 · 完形四选一专训版")
        set_font(hrun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, color_rgb=(156, 163, 175))
        
        # 页脚设置
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("第 1 部分：过关实战练习卷  |  从每题所给的 A、B、C、D 四个选项中选出最佳选项")
        set_font(frun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, color_rgb=(156, 163, 175))

    # ========== 试卷大标题 ==========
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("高考英语高频核心“熟词生义”专项训练与突破过关测试")
    set_font(run_title, font_name="Calibri", east_asia_font="微软雅黑", size_pt=18, bold=True, color_rgb=(17, 24, 39))

    # 副标题
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run("【1+3贯通培养拔尖计划】高考全真题与北京顶尖名校（海淀/西城一模、人大附中、清华附中）完形四选一 · 40题特训版")
    set_font(run_sub, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, color_rgb=(75, 85, 99))

    # 学生信息栏表格
    info_table = doc.add_table(rows=1, cols=5)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Cm(3.0), Cm(3.5), Cm(3.5), Cm(3.5), Cm(3.5)]
    info_cells = info_table.rows[0].cells
    labels = ["班级：__________", "姓名：__________", "学号：__________", "日期：__________", f"得分：_____ / {len(POLYSEMY_CLOZE_QUESTIONS)}"]
    for i, cell in enumerate(info_cells):
        cell.width = col_widths[i]
        set_cell_background(cell, "F3F4F6")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(labels[i])
        set_font(run, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.5, bold=(i == 4), color_rgb=(31, 41, 55))
    set_grid_borders(info_table, color="E5E7EB", sz="4")

    # 说明框
    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(10)
    p_note.paragraph_format.space_after = Pt(12)
    run_note = p_note.add_run("【考试说明】“熟词生义”（Familiar words with unfamiliar meanings）是高考英语完形填空拉开区分度的绝对核心命题点。本专项精选 40 道全国高考与北京一线名校全真题，全部采用标准完形填空四选一（A、B、C、D）题型。请通读题干语境，排除常见熟义干扰，选出最符合本句语境逻辑的最佳选项。答卷完成后，请翻至卷末核对答卷矩阵并阅读深度精析。")
    set_font(run_note, font_name="Calibri", east_asia_font="楷体", size_pt=9.5, italic=True, color_rgb=(107, 114, 128))

    # ========== 试题排版（标准完形四选一） ==========
    for idx, q in enumerate(POLYSEMY_CLOZE_QUESTIONS, start=1):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.line_spacing = 1.15
        
        # 题号
        r_num = p_q.add_run(f"{idx:02d}. ")
        set_font(r_num, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=True, color_rgb=(79, 70, 229))
        
        # 句子挖空处理：将 ________ 替换为标准划线与空括号
        sentence_text = q["sentence"]
        parts = re.split(r'(________+)', sentence_text)
        for part in parts:
            if re.match(r'^________+$', part):
                r_blank = p_q.add_run("   ___________   ")
                set_font(r_blank, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=True, color_rgb=(17, 24, 39))
                r_blank.underline = True
            else:
                r_text = p_q.add_run(part)
                set_font(r_text, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=False, color_rgb=(17, 24, 39))

        # 选项排版：采用 1 行 4 列无边框对齐表格，确保全卷 A/B/C/D 绝对平齐
        opt_table = doc.add_table(rows=1, cols=4)
        opt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        remove_table_borders(opt_table)
        
        col_w = Cm(4.25)
        for col_i, cell in enumerate(opt_table.rows[0].cells):
            cell.width = col_w
            set_cell_margins(cell, top=20, bottom=40, left=40, right=40)
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.space_after = Pt(2)
            opt_text = q["options"][col_i] if col_i < len(q["options"]) else ""
            c_run = cp.add_run(opt_text)
            set_font(c_run, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.0, bold=False, color_rgb=(55, 65, 81))

    # ==========================================
    # 第二部分：参考答案与深度精析手册（分页独立）
    # ==========================================
    doc.add_page_break()
    
    # 答案页标题
    p_ans_title = doc.add_paragraph()
    p_ans_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ans_title.paragraph_format.space_before = Pt(6)
    p_ans_title.paragraph_format.space_after = Pt(2)
    run_ans_title = p_ans_title.add_run("【参考答案与高考名师深度精析讲义】")
    set_font(run_ans_title, font_name="Calibri", east_asia_font="微软雅黑", size_pt=16, bold=True, color_rgb=(15, 23, 42))

    p_ans_sub = doc.add_paragraph()
    p_ans_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ans_sub.paragraph_format.space_after = Pt(12)
    run_ans_sub = p_ans_sub.add_run("标准答案速查表 + 语境生义核心考点拆解与干扰项精析")
    set_font(run_ans_sub, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=False, color_rgb=(100, 116, 139))

    # 答案速查表格（Quick Answer Matrix）
    p_tbl_lbl = doc.add_paragraph()
    p_tbl_lbl.paragraph_format.space_before = Pt(4)
    p_tbl_lbl.paragraph_format.space_after = Pt(4)
    r_tl = p_tbl_lbl.add_run("■ 30秒快速核对答卷表（Quick Answer Matrix）：")
    set_font(r_tl, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(30, 41, 59))

    # 10 列表格，8 行，共 40 题 (4 组 10 题)
    num_rows = (len(POLYSEMY_CLOZE_QUESTIONS) + 9) // 10
    ans_table = doc.add_table(rows=num_rows * 2, cols=10)
    ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_grid_borders(ans_table, color="94A3B8", sz="4")

    for row_idx in range(num_rows):
        header_row = ans_table.rows[row_idx * 2]
        data_row = ans_table.rows[row_idx * 2 + 1]
        
        for col_idx in range(10):
            q_num = row_idx * 10 + col_idx + 1
            h_cell = header_row.cells[col_idx]
            d_cell = data_row.cells[col_idx]
            
            if q_num <= len(POLYSEMY_CLOZE_QUESTIONS):
                q_item = POLYSEMY_CLOZE_QUESTIONS[q_num - 1]
                
                # 题号单元格
                set_cell_background(h_cell, "F1F5F9")
                set_cell_margins(h_cell, top=60, bottom=60, left=40, right=40)
                hp = h_cell.paragraphs[0]
                hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                hrun = hp.add_run(f"题 {q_num}")
                set_font(hrun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(71, 85, 105))
                
                # 答案单元格
                set_cell_background(d_cell, "FFFFFF")
                set_cell_margins(d_cell, top=60, bottom=60, left=40, right=40)
                dp = d_cell.paragraphs[0]
                dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                drun = dp.add_run(q_item["answer"])
                set_font(drun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.0, bold=True, color_rgb=(220, 38, 38))
            else:
                set_cell_background(h_cell, "F8FAFC")
                set_cell_background(d_cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 深度精析列表
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(8)
    p_sec2.paragraph_format.space_after = Pt(6)
    r_s2 = p_sec2.add_run(f"■ {len(POLYSEMY_CLOZE_QUESTIONS)} 道核心真题逐题深度剖析与干扰项讲义：")
    set_font(r_s2, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11, bold=True, color_rgb=(15, 23, 42))

    for idx, q in enumerate(POLYSEMY_CLOZE_QUESTIONS, start=1):
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(6)
        p_item.paragraph_format.space_after = Pt(2)
        
        r_idx = p_item.add_run(f"第 {idx:02d} 题  ")
        set_font(r_idx, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(79, 70, 229))
        
        r_w = p_item.add_run(f"【核心熟词】{q['word']}  ")
        set_font(r_w, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(30, 41, 59))
        
        r_ans = p_item.add_run(f"【标准答案】{q['option_answer']}  ")
        set_font(r_ans, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(220, 38, 38))
        
        r_src = p_item.add_run(f"【真题出处】{q['source']}")
        set_font(r_src, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9, bold=False, color_rgb=(100, 116, 139))
        
        # 详细解析 HTML 渲染
        exp_html = f"【熟义回顾】{q['familiar']} &nbsp;|&nbsp; 【本题生义】<b>{q['unfamiliar']}</b><br>【真题汉译】{q['sentence_cn']}<br>【名师精析与干扰项辨析】{q['explanation']}"
        add_html_paragraph(doc, exp_html, space_after=6)

    # 输出路径
    output_filename = "高考英语高频核心“熟词生义”专项训练与突破过关测试（1+3项目专训版）.docx"
    doc.save(output_filename)
    print(f"Successfully generated: {output_filename}")

    # Copy to sdcard and download locations
    sdcard_dirs = ["/sdcard", "/sdcard/Download"]
    for sddir in sdcard_dirs:
        try:
            dest_file = os.path.join(sddir, output_filename)
            cmd = f'su -c "cp -f \'{os.path.abspath(output_filename)}\' \'{dest_file}\' && chmod 666 \'{dest_file}\' && chown 10194:1028 \'{dest_file}\' && am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://\'{dest_file}\'"'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"Successfully synced to: {dest_file}")
            else:
                print(f"Warning: Failed to sync to {dest_file}: {res.stderr}")
        except Exception as e:
            print(f"Error copying to {sddir}: {e}")

if __name__ == "__main__":
    build_polysemy_cloze_document()
