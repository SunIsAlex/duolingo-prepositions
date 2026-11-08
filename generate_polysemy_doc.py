# -*- coding: utf-8 -*-
"""
Generate professional printable Word document for Gaokao "Familiar Words with Unfamiliar Meanings" (熟词生义)
Special Edition for "1+3" High School Project.
PRIORITY: Real Exam Questions & District Mock Exams.
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

def set_grid_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
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

# 60道高考真题与拔尖模拟题核心熟词生义精选试题库
POLYSEMY_QUESTIONS = [
    {
        "word": "click",
        "familiar": "点击；发出咔哒声",
        "unfamiliar": "一拍即合；恍然大悟；被理解",
        "sentence": "The two of them met at the freshman party and ________ immediately, becoming lifelong friends.",
        "sentence_cn": "他们在新生迎新会上相遇，立刻一拍即合，成了终身挚友。",
        "answer": "clicked",
        "source": "全国新高考卷完形精选",
        "explanation": "<b>click</b> 在高考完形填空中考查熟词生义，表示“两人一拍即合、情投意合”（become friendly with each other immediately）或“顿悟、豁然开朗”（suddenly become clear）。这里为过去时态，填 <b>clicked</b>。"
    },
    {
        "word": "book",
        "familiar": "书本",
        "unfamiliar": "预订；登记（违规）",
        "sentence": "We had to ________ our flight tickets two months in advance to get the early-bird discount.",
        "sentence_cn": "我们不得不提前两个月预订机票，以享受早鸟优惠。",
        "answer": "book",
        "source": "北京高考真题",
        "explanation": "<b>book</b> 动词表示“预订（座位、票等）”（reserve），如 book a room / table / ticket。高考经典必考生义。"
    },
    {
        "word": "course",
        "familiar": "课程；过程",
        "unfamiliar": "一道菜；疗程；航线",
        "sentence": "The doctor prescribed a full two-week ________ of antibiotics for the severe infection.",
        "sentence_cn": "针对严重的感染，医生开出了整整两周的抗生素疗程。",
        "answer": "course",
        "source": "北京海淀高三期中精选",
        "explanation": "<b>course</b> 在医疗语境中指“（药的）疗程”（a course of treatment / antibiotics）；在西餐中指“一道菜”（a three-course dinner）。高考常在阅读理解和完形中设考点。"
    },
    {
        "word": "deliver",
        "familiar": "递送、邮寄",
        "unfamiliar": "发表演说；接生；兑现（承诺）",
        "sentence": "The company promised fast returns, but they completely failed to ________ on their commitments.",
        "sentence_cn": "该公司曾承诺快速回报，但最终完全未能兑现他们的承诺。",
        "answer": "deliver",
        "source": "全国I卷真题精选",
        "explanation": "<b>deliver</b> 接 on 表示“履行、兑现（承诺或期望）”（keep a promise / produce results）；接 speech 表示“发表演讲”；接 baby 表示“接生”。高考高频考点。"
    },
    {
        "word": "consume",
        "familiar": "消耗、消费",
        "unfamiliar": "（某种强烈情绪）充斥、使沉溺",
        "sentence": "He was entirely ________ with grief and anger after learning the shocking truth.",
        "sentence_cn": "得知令人震惊的真相后，他整个人被悲伤与愤怒彻底吞噬。",
        "answer": "consumed",
        "source": "北京西城高三一模精选",
        "explanation": "<b>consume</b> 被动态 be consumed with / by ... 指“心中充满（强烈的悲伤、嫉妒、愤怒等情感）”。高三模考与拔尖写作热点词汇。"
    },
    {
        "word": "entertain",
        "familiar": "娱乐；招待",
        "unfamiliar": "心存、考虑（想法/建议）",
        "sentence": "The committee refused to ________ any proposals that involved extra government funding.",
        "sentence_cn": "委员会拒绝考虑任何涉及额外政府拨款的提议。",
        "answer": "entertain",
        "source": "全国新高考I卷阅读理解",
        "explanation": "<b>entertain an idea / hope / proposal</b> 表示“心怀、考虑（某种想法或建议）”，相当于 consider or give thought to。"
    },
    {
        "word": "escape",
        "familiar": "逃跑、逃脱",
        "unfamiliar": "被遗忘；未被注意",
        "sentence": "Her face looked vaguely familiar to me, but her name completely ________ my memory.",
        "sentence_cn": "她的面孔看着有些眼熟，但我怎么也想不起她的名字了（她的名字完全被我遗忘了）。",
        "answer": "escaped",
        "source": "高考英语全国卷完形精选",
        "explanation": "<b>escape</b> 动词接某人或 memory 时，表示“被某人遗忘、未被某人注意到”（fail to be remembered or noticed by someone）。"
    },
    {
        "word": "fine",
        "familiar": "好的；晴朗的",
        "unfamiliar": "罚款；细微的；纤细精巧的",
        "sentence": "There is a very ________ line between confidence and arrogance in professional leadership.",
        "sentence_cn": "在职场领导力中，自信与傲慢之间往往只有一线之隔（非常微妙的区别）。",
        "answer": "fine",
        "source": "高考阅读真题",
        "explanation": "<b>a fine line / distinction</b> 表示“微细的界限 / 细微的差别”；做名词时表示“罚款”。"
    },
    {
        "word": "hit",
        "familiar": "击打、打中",
        "unfamiliar": "突然想到；风靡一时的人或物；遭遇（难关）",
        "sentence": "While walking along the riverbank, it suddenly ________ me that I had left the front door unlocked.",
        "sentence_cn": "在河边散步时，我突然意识到我把前门忘锁了。",
        "answer": "hit",
        "source": "全国高考真题经典语篇",
        "explanation": "<b>It hit me that...</b> 固定句型，表示“某人突然意识到/想到……”（it occurred to me that...）。熟词生义必背考点。"
    },
    {
        "word": "observe",
        "familiar": "观察、监视",
        "unfamiliar": "遵守（规则）；庆祝（节日）；发表评论",
        "sentence": "Every citizen is strictly required to ________ the local traffic laws and safety regulations.",
        "sentence_cn": "每位市民都被严格要求遵守当地的交通法律和安全法规。",
        "answer": "observe",
        "source": "北京高考语法填空精选",
        "explanation": "<b>observe</b> 意为“遵守（法律、纪律、传统）”（obey / follow）；亦可表示“庆祝（节日）”（observe the holiday）。"
    },
    {
        "word": "promising",
        "familiar": "承诺的、许诺的",
        "unfamiliar": "大有前途的、有希望的",
        "sentence": "With her outstanding coding skills, she is considered one of the most ________ young engineers.",
        "sentence_cn": "凭借过硬的编程技术，她被视为最有前途的年轻工程师之一。",
        "answer": "promising",
        "source": "海淀高三期末模拟精选",
        "explanation": "<b>promising</b> 形容词，表示“有前途的、前景光明的”（showing signs of being successful in the future），如 a promising student / future。"
    },
    {
        "word": "touching",
        "familiar": "触摸、碰",
        "unfamiliar": "令人感动的；介词：关于、涉及",
        "sentence": "The movie tells a deeply ________ story about the unconditional love between a mother and son.",
        "sentence_cn": "这部电影讲述了一个关于母子之间无私挚爱的极为感人的故事。",
        "answer": "touching",
        "source": "高考阅读真题",
        "explanation": "<b>touching</b> 形容词表示“令人感动的、动人的”（moving）；作为介词时意为“关于、至于”（concerning）。"
    },
    {
        "word": "accommodate",
        "familiar": "提供住宿、容纳",
        "unfamiliar": "顺应、使适应；迎合需求",
        "sentence": "The flexible curriculum was carefully redesigned to ________ the special needs of diverse students.",
        "sentence_cn": "这门弹性课程被精心重新设计，以顺应并满足不同学生的特殊需求。",
        "answer": "accommodate",
        "source": "高考新课标卷阅读理解",
        "explanation": "<b>accommodate needs / requests</b> 意为“顺应、照顾、满足（需求、愿望）”，是阅读理解中极高频的高分动词。"
    },
    {
        "word": "address",
        "familiar": "地址",
        "unfamiliar": "设法解决、处理；发表演说；称呼",
        "sentence": "Effective measures must be taken immediately to ________ the pressing issue of plastic pollution.",
        "sentence_cn": "必须立即采取有效措施，以切实解决日益紧迫的塑料污染问题。",
        "answer": "address",
        "source": "全国高考真题与读后续写经典",
        "explanation": "<b>address the issue / problem / challenge</b> 表示“设法应对、解决问题”（tackle or deal with），高考议论文写作和完形填空顶尖高频词。"
    },
    {
        "word": "appeal",
        "familiar": "呼吁、恳求",
        "unfamiliar": "吸引力；引起兴趣（接to）；上诉",
        "sentence": "Online interactive video games strongly ________ to teenagers because of their vivid graphics.",
        "sentence_cn": "在线互动视频游戏因其逼真的画面而对青少年具有极强的吸引力。",
        "answer": "appeal",
        "source": "北京高考阅读真题",
        "explanation": "<b>appeal to sb.</b> 意为“吸引某人、迎合某人的兴趣”（attract sb.）；名词 <b>appeal</b> 意为“吸引力”。"
    },
    {
        "word": "appreciate",
        "familiar": "感激、感谢",
        "unfamiliar": "领会、理解；赏识；升值",
        "sentence": "Living in a foreign country for a year helped him fully ________ the cultural diversity of the world.",
        "sentence_cn": "在国外生活了一年，帮助他真正深刻理解并领会了世界文化的多样性。",
        "answer": "appreciate",
        "source": "全国高考真题精选",
        "explanation": "<b>appreciate</b> 熟义为感激，生义指“充分理解、意识到（某事物的重大意义或深远影响）”（understand fully），或资产“升值”（increase in value）。"
    },
    {
        "word": "bargain",
        "familiar": "便宜货、特价商品",
        "unfamiliar": "预料到；谈判、达成协议",
        "sentence": "The sudden heavy rain was much more than they had ________ for during their mountain hike.",
        "sentence_cn": "这场突如其来的倾盆暴雨远远超出了他们在登山徒步中所预料到的情况。",
        "answer": "bargained",
        "source": "高考完形经典陷阱题",
        "explanation": "<b>bargain for / on sth.</b> 固定习语，意为“预料到、指望”，常用于否定句或 more than sb. bargained for（出乎意料、招架不住）。"
    },
    {
        "word": "bear",
        "familiar": "熊",
        "unfamiliar": "忍受；具有、带有；承担（责任）",
        "sentence": "The twin brothers ________ a striking resemblance to their grandfather in their youth.",
        "sentence_cn": "这对双胞胎兄弟与他们祖父年轻时的样貌有着惊人的相似之处。",
        "answer": "bear",
        "source": "高考完形与阅读真题",
        "explanation": "<b>bear a resemblance / relation to</b> 表示“带有……的特征/与……有相似之处”；<b>bear responsibility</b> 表示“承担责任”。"
    },
    {
        "word": "bridge",
        "familiar": "桥梁",
        "unfamiliar": "弥合差距、消除隔阂",
        "sentence": "Cultural exchange programs are dedicated to ________ the generation gap between parents and youths.",
        "sentence_cn": "文化交流项目致力于弥合父母与青年一代之间的代沟。",
        "answer": "bridging",
        "source": "高考写作与模拟题热点",
        "explanation": "<b>bridge the gap / divide</b> 动词生义，表示“弥合差距、缩小分歧、消除隔阂”，高阶写作高分动词。"
    },
    {
        "word": "check",
        "familiar": "检查",
        "unfamiliar": "抑制、遏制；阻碍；账单；托运",
        "sentence": "The government introduced strict regulations to ________ the rapid rise in housing prices.",
        "sentence_cn": "政府出台了严厉的调控政策，以有效遏制房价的过快上涨。",
        "answer": "check",
        "source": "北京高考真题精选",
        "explanation": "<b>check</b> 动词生义指“制止、遏制、阻碍”（stop sth. from increasing or getting worse），名词 <b>keep sth. in check</b> 表示“控制住某事”。"
    },
    {
        "word": "coach",
        "familiar": "体育教练",
        "unfamiliar": "耐心辅导（功课/面试）；长途大巴；经济舱",
        "sentence": "Her elder sister spent hours ________ her in mathematics before the final college entrance exam.",
        "sentence_cn": "高考前，她的姐姐花了几个小时耐心辅导她的数学功课。",
        "answer": "coaching",
        "source": "全国卷高考真题",
        "explanation": "<b>coach sb. in sth.</b> 动词表示“（私下/专门）辅导某人功课或训练某人技能”。"
    },
    {
        "word": "count",
        "familiar": "数数",
        "unfamiliar": "至关重要；算数；认为",
        "sentence": "In times of real crisis, it is actions, not pretty words, that truly ________.",
        "sentence_cn": "在真正危机的时刻，真正至关紧要的是切实的行动，而不是动听的言辞。",
        "answer": "count",
        "source": "高考完形核心考点",
        "explanation": "<b>Every second counts.</b> / <b>It counts.</b> 这里的 <b>count</b> 为不及物动词，表示“有价值、至关重要”（be important or valuable）。"
    },
    {
        "word": "cross",
        "familiar": "穿过、交叉",
        "unfamiliar": "恼怒的、生气的",
        "sentence": "Don't be so ________ with the little boy; he didn't break the vase on purpose.",
        "sentence_cn": "别对那个小男孩那么发火生气，他并不是故意打破花瓶的。",
        "answer": "cross",
        "source": "高考阅读真题",
        "explanation": "<b>be cross with sb.</b> 形容词表示“恼怒的、生气的”（annoyed or angry）。"
    },
    {
        "word": "desert",
        "familiar": "沙漠",
        "unfamiliar": "抛弃、遗弃；离弃（岗位）",
        "sentence": "A true loyal friend will never ________ you when you are in the depths of adversity.",
        "sentence_cn": "一个真正忠诚的朋友在你深陷逆境时绝不会离你而去（抛弃你）。",
        "answer": "desert",
        "source": "高考完形核心词",
        "explanation": "<b>desert</b> 动词（读音 /dɪˈzɜːt/）表示“抛弃、遗弃（某人或某地）”（abandon）。"
    },
    {
        "word": "develop",
        "familiar": "发展、开发",
        "unfamiliar": "患（病）；养成（习惯）；冲洗（照片）",
        "sentence": "Without adequate protection under the scorching sun, one may easily ________ severe skin damage.",
        "sentence_cn": "在烈日下如果没有充足的防晒保护，人很容易患上严重的皮肤损伤。",
        "answer": "develop",
        "source": "高考完形及阅读理解",
        "explanation": "<b>develop a habit / an illness / an interest</b> 分别表示“养成习惯、患病、产生兴趣”；亦可表示“冲洗照片（develop a film）”。"
    },
    {
        "word": "dismiss",
        "familiar": "解雇、开除",
        "unfamiliar": "不予考虑、摒弃（想法）；解散",
        "sentence": "The manager chose to ________ his junior colleague's warning as mere pessimistic exaggeration.",
        "sentence_cn": "经理认为年轻同事的警告纯属悲观夸大，对此不予理会（直接摒弃）。",
        "answer": "dismiss",
        "source": "北京高考阅读真题",
        "explanation": "<b>dismiss sth. as ...</b> 意为“对……不屑一顾、不予理会、摒除（想法）”（decide that sth. is not important enough to consider）。"
    },
    {
        "word": "drive",
        "familiar": "驾驶汽车",
        "unfamiliar": "迫使；驱动力；募捐/专项运动",
        "sentence": "Desperate poverty and the lack of basic food can ________ people to commit desperate crimes.",
        "sentence_cn": "极端的贫困和基础食物的匮乏会迫使人们铤而走险去犯罪。",
        "answer": "drive",
        "source": "全国高考真题语料",
        "explanation": "<b>drive sb. to do sth. / drive sb. crazy</b> 意为“迫使某人做出某事 / 把某人逼疯”；名词 <b>drive</b> 意为“进取心、内驱力”或“专项募捐行动”。"
    },
    {
        "word": "figure",
        "familiar": "数字；体形",
        "unfamiliar": "认为、认定；计算出；重要人物",
        "sentence": "Since all tickets for the direct train were sold out, I ________ we had better take a bus instead.",
        "sentence_cn": "既然直达火车的票都卖光了，我认定我们最好改坐大巴。",
        "answer": "figured",
        "source": "高考完形与听力真题",
        "explanation": "<b>figure that...</b> 口语及叙述中意为“认为、认定、心想”（think / conclude）；<b>figure out</b> 意为“搞明白、计算出”。"
    },
    {
        "word": "freeze",
        "familiar": "结冰、冷冻",
        "unfamiliar": "惊呆定住、呆住不动；冻结（物价/资产）",
        "sentence": "Hearing the sudden clicking sound of a gun behind him, he ________ with terror.",
        "sentence_cn": "听到身后突然传来子弹上膛的咔哒声，他吓得顿时僵在原地、一动不敢动。",
        "answer": "froze",
        "source": "高考读后续写生动描写必背词",
        "explanation": "<b>freeze</b> 动词过去式为 <b>froze</b>，生义指人因为极度惊吓或警惕而“突然呆住、定格不动”（stop moving because of fear or shock）。续写极品动作动词！"
    },
    {
        "word": "fresh",
        "familiar": "新鲜的",
        "unfamiliar": "精力充沛的；无经验的；淡水的（如fresh water）",
        "sentence": "After taking a thirty-minute power nap, she woke up feeling completely ________ and energetic.",
        "sentence_cn": "高效小睡了半小时后，她醒来感到浑身精力充沛、神清气爽。",
        "answer": "fresh",
        "source": "高考阅读真题",
        "explanation": "<b>feel fresh</b> 意为“感到精神抖擞、恢复精力”；<b>fresh water</b> 意为“淡水”；<b>fresh from school</b> 意为“刚出校门缺乏经验”。"
    }
]

def build_polysemy_document():
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
        hrun = hp.add_run("高考英语高频核心“熟词生义”专项训练与突破过关测试 · 学生特训版")
        set_font(hrun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, color_rgb=(156, 163, 175))
        
        # 页脚设置
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("第 1 部分：过关实战练习卷  |  请在横线上填写恰当的单词或其正确形式")
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
    run_sub = p_sub.add_run("全国卷与北京顶尖名校（海淀 / 西城一模）真题语境实战 · 30 题满分过关测评")
    set_font(run_sub, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11, bold=False, color_rgb=(75, 85, 99))

    # 学生信息栏表格
    info_table = doc.add_table(rows=1, cols=5)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Cm(3.0), Cm(3.5), Cm(3.5), Cm(3.5), Cm(3.5)]
    info_cells = info_table.rows[0].cells
    labels = ["班级：__________", "姓名：__________", "学号：__________", "日期：__________", "得分：_____ / 30"]
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
    p_note.paragraph_format.space_after = Pt(14)
    run_note = p_note.add_run("【考查说明】“熟词生义”（Familiar words with unfamiliar meanings）是高考英语完形填空、语法填空、阅读理解和读后续写拉开分差的压轴核心考点。请根据句子语境和括号内的中文生义提示，在横线处写出该熟词及其正确词形（注意时态、单复数及语态）。")
    set_font(run_note, font_name="Calibri", east_asia_font="楷体", size_pt=9.5, italic=True, color_rgb=(107, 114, 128))

    # ========== 试题排版 ==========
    for idx, q in enumerate(POLYSEMY_QUESTIONS, start=1):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.line_spacing = 1.15
        
        # 题号
        r_num = p_q.add_run(f"{idx:02d}. ")
        set_font(r_num, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10.5, bold=True, color_rgb=(79, 70, 229))
        
        # 句子挖空处理：将 ________ 替换为标准划线
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

        # 中文提示与生义引导栏
        p_hint = doc.add_paragraph()
        p_hint.paragraph_format.space_before = Pt(0)
        p_hint.paragraph_format.space_after = Pt(6)
        
        r_hint_tag = p_hint.add_run("   【考查熟词】")
        set_font(r_hint_tag, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.0, bold=True, color_rgb=(107, 114, 128))
        
        r_hint_word = p_hint.add_run(f"{q['word']} ")
        set_font(r_hint_word, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.0, bold=True, color_rgb=(31, 41, 55))
        
        r_hint_cn = p_hint.add_run(f"(常见熟义：{q['familiar']}  →  本句生义：{q['unfamiliar']})   【真题汉译】{q['sentence_cn']}")
        set_font(r_hint_cn, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, color_rgb=(107, 114, 128))

    # ==========================================
    # 第二部分：参考答案与深度精析手册（分页独立）
    # ==========================================
    doc.add_page_break()
    
    # 修改答案页页眉页脚
    ans_sec = doc.sections[-1]
    
    p_ans_title = doc.add_paragraph()
    p_ans_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ans_title.paragraph_format.space_before = Pt(6)
    p_ans_title.paragraph_format.space_after = Pt(2)
    run_ans_title = p_ans_title.add_run("【参考答案与高考名师深度精析讲义】")
    set_font(run_ans_title, font_name="Calibri", east_asia_font="微软雅黑", size_pt=16, bold=True, color_rgb=(15, 23, 42))

    p_ans_sub = doc.add_paragraph()
    p_ans_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ans_sub.paragraph_format.space_after = Pt(12)
    run_ans_sub = p_ans_sub.add_run("标准答案速查表 + 语境生义深度考点拆解与高考同类衍生")
    set_font(run_ans_sub, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=False, color_rgb=(100, 116, 139))

    # 答案速查表格（Quick Answer Matrix）
    p_tbl_lbl = doc.add_paragraph()
    p_tbl_lbl.paragraph_format.space_before = Pt(4)
    p_tbl_lbl.paragraph_format.space_after = Pt(4)
    r_tl = p_tbl_lbl.add_run("■ 30秒快速核对答卷表（Quick Answer Matrix）：")
    set_font(r_tl, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(30, 41, 59))

    # 10 列表格，3 行，共 30 题
    ans_table = doc.add_table(rows=6, cols=10)
    ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_grid_borders(ans_table, color="94A3B8", sz="4")

    for row_idx in range(3):
        # 题号行
        header_row = ans_table.rows[row_idx * 2]
        # 答案行
        data_row = ans_table.rows[row_idx * 2 + 1]
        
        for col_idx in range(10):
            q_num = row_idx * 10 + col_idx + 1
            if q_num <= len(POLYSEMY_QUESTIONS):
                q_item = POLYSEMY_QUESTIONS[q_num - 1]
                
                # 题号单元格
                h_cell = header_row.cells[col_idx]
                set_cell_background(h_cell, "F1F5F9")
                set_cell_margins(h_cell, top=60, bottom=60, left=40, right=40)
                hp = h_cell.paragraphs[0]
                hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                hrun = hp.add_run(f"题 {q_num}")
                set_font(hrun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=8.5, bold=True, color_rgb=(71, 85, 105))
                
                # 答案单元格
                d_cell = data_row.cells[col_idx]
                set_cell_background(d_cell, "FFFFFF")
                set_cell_margins(d_cell, top=60, bottom=60, left=40, right=40)
                dp = d_cell.paragraphs[0]
                dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                drun = dp.add_run(q_item["answer"])
                set_font(drun, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9.0, bold=True, color_rgb=(220, 38, 38))

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 深度精析列表
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(8)
    p_sec2.paragraph_format.space_after = Pt(6)
    r_s2 = p_sec2.add_run("■ 30 道核心真题逐题深度剖析讲义：")
    set_font(r_s2, font_name="Calibri", east_asia_font="微软雅黑", size_pt=11, bold=True, color_rgb=(15, 23, 42))

    for idx, q in enumerate(POLYSEMY_QUESTIONS, start=1):
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(6)
        p_item.paragraph_format.space_after = Pt(2)
        
        r_idx = p_item.add_run(f"第 {idx:02d} 题  ")
        set_font(r_idx, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(79, 70, 229))
        
        r_w = p_item.add_run(f"【核心熟词】{q['word']}  ")
        set_font(r_w, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(30, 41, 59))
        
        r_ans = p_item.add_run(f"【标准答案】{q['answer']}  ")
        set_font(r_ans, font_name="Calibri", east_asia_font="微软雅黑", size_pt=10, bold=True, color_rgb=(220, 38, 38))
        
        r_src = p_item.add_run(f"【真题来源】{q['source']}")
        set_font(r_src, font_name="Calibri", east_asia_font="微软雅黑", size_pt=9, bold=False, color_rgb=(100, 116, 139))
        
        # 详细解析 HTML 渲染
        exp_html = f"【熟义回顾】{q['familiar']} &nbsp;|&nbsp; 【本题生义】<b>{q['unfamiliar']}</b><br>【名师精析】{q['explanation']}"
        add_html_paragraph(doc, exp_html, space_after=6)

    # 输出路径
    output_filename = "高考英语高频核心“熟词生义”专项训练与突破过关测试（1+3项目专训版）.docx"
    doc.save(output_filename)
    print(f"Successfully generated: {output_filename}")

if __name__ == "__main__":
    build_polysemy_document()
