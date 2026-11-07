# -*- coding: utf-8 -*-
"""
Zuoyebang Crawler Importer for English Learning Web App
Integrates with /data/ccm/home/zuoyebang-crawler (zyb package)
Fetches questions from activities.zuoyebang.com, parses English sentences/quizzes,
and converts them into Duolingo-style cloze/grammar questions.
"""

import os
import sys
import re
import json
import html

# Add zuoyebang-crawler to sys.path
ZYB_DIR = '/data/ccm/home/zuoyebang-crawler'
if ZYB_DIR not in sys.path and os.path.exists(ZYB_DIR):
    sys.path.insert(0, ZYB_DIR)

try:
    from zyb.api import fetch_question, parse_share_url, ShareLinkError, ApiError
    from zyb.render import normalize
except ImportError:
    fetch_question = None
    normalize = None

# Pre-extracted high-yield questions from Zuoyebang questions & Beijing High School mock papers
ZYB_CURATED_QUESTIONS = [
    {
        "id": "zyb_01",
        "phrase": "kick ___ decades of linguistic argument",
        "sentence": "Franz Boas returned with a discovery that would kick ___ decades of linguistic argument.",
        "sentence_cn": "博厄斯带回了一个发现，该发现引发了长达数十年的语言学争论。",
        "answer": "off",
        "acceptable": ["off"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·词组搭配】<b>kick off</b> 意为“开始、引发、拉开序幕”（源自足球比赛开球）。在此句中指博厄斯的语言学发现拉开了数十年来学术大讨论的序幕。<br>【同义替换】set off, trigger, initiate。<br>【同类拓展】<b>kick off a meeting</b>（启动会议）、<b>kick off with</b>（以……开始）。",
        "tags": ["作业帮真题", "阅读真题", "动词短语"]
    },
    {
        "id": "zyb_02",
        "phrase": "___ his count, the language had four words for snow",
        "sentence": "___ his count, the local Inuit language had four words for snow.",
        "sentence_cn": "据他统计，当地因纽特语中有四个表示雪的词汇。",
        "answer": "by",
        "acceptable": ["by"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·介词辨析】<b>by one's count / by one's reckoning</b> 表示“据某人估算/统计”。介词 <b>by</b> 在此表示“依据、按照”。<br>【易混搭配】<i>in one's opinion</i>（依某人看来）、<i>according to statistics</i>（据统计）。",
        "tags": ["作业帮真题", "介词短语"]
    },
    {
        "id": "zyb_03",
        "phrase": "a link ___ language and physical environment",
        "sentence": "The study suggested a link ___ language and physical environment.",
        "sentence_cn": "研究表明语言与物理环境之间存在联系。",
        "answer": "between",
        "acceptable": ["between"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【作业帮真题·固定搭配】<b>a link / connection between A and B</b> 表示“A与B之间的关联”。<br>【同类考点】<b>a relationship between</b>、<b>a compromise between</b>。",
        "tags": ["作业帮真题", "基础高频"]
    },
    {
        "id": "zyb_04",
        "phrase": "___ a single term, there are 100 synonyms",
        "sentence": "An article claimed the Inuit have 100 synonyms for snow ___ a single term.",
        "sentence_cn": "一篇文章声称因纽特人在同一个概念术语下有100个雪的同义词。",
        "answer": "under",
        "acceptable": ["under"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·高频介词】<b>under a term / category / heading</b> 表示“归属于某标题/术语/类别之下”。介词 <b>under</b> 表分类所属。<br>【例句】Items listed under the heading 'Miscellaneous'.",
        "tags": ["作业帮真题", "阅读真题"]
    },
    {
        "id": "zyb_05",
        "phrase": "offer a window ___ language speakers' culture",
        "sentence": "The results offer a window ___ language speakers' culture.",
        "sentence_cn": "这些研究结果为透视说话者的文化提供了一扇窗口。",
        "answer": "onto",
        "acceptable": ["onto", "into"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·地道表达】<b>offer a window onto / into sth</b> 意为“提供了解……的一扇窗口/视角”。<b>onto</b> 强调由内向外透视全局视角，<b>into</b> 强调深入内部洞察。<br>【真题原句】Charles Kemp says the results offer a window onto language speakers' culture.",
        "tags": ["作业帮真题", "地道表达"]
    },
    {
        "id": "zyb_06",
        "phrase": "look ___ lexical elaboration in language",
        "sentence": "Researchers analyzed dictionaries, looking ___ lexical elaboration.",
        "sentence_cn": "研究人员分析了词典，寻找词汇细化现象。",
        "answer": "for",
        "acceptable": ["for"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【作业帮真题·动词搭配】<b>look for</b> 表示“寻找、搜寻”。<br>【辨析】<b>look after</b>（照看）、<b>look into</b>（调查）、<b>look through</b>（浏览）。",
        "tags": ["作业帮真题", "核心动词"]
    },
    {
        "id": "zyb_07",
        "phrase": "filled ___ words to describe the desert",
        "sentence": "Australian languages are filled ___ words to describe the desert.",
        "sentence_cn": "澳洲原住民语言中充满了描述沙漠的词汇。",
        "answer": "with",
        "acceptable": ["with"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【作业帮真题·形容词搭配】<b>be filled with sth</b> 意为“装满、充满……”，相当于 <b>be full of</b>。<br>【同义辨析】be crowded with（挤满）、be packed with（塞满）。",
        "tags": ["作业帮真题", "高频搭配"]
    },
    {
        "id": "zyb_08",
        "phrase": "known ___ the Sapir-Whorf hypothesis",
        "sentence": "Linguistic relativity is known ___ the Sapir-Whorf hypothesis.",
        "sentence_cn": "语言相对论被称为萨丕尔-沃尔夫假说。",
        "answer": "as",
        "acceptable": ["as"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【作业帮真题·被动搭配】<b>be known as ...</b> 意为“作为……而闻名/被称作……”（表身份、名称）。<br>【辨析口诀】be known for（以某特征闻名），be known to（为某人所知晓），be known as（作为……闻名）。",
        "tags": ["作业帮真题", "常考易错"]
    },
    {
        "id": "zyb_09",
        "phrase": "all bilingual dictionaries map back ___ English",
        "sentence": "All the bilingual dictionaries in this study map back ___ English.",
        "sentence_cn": "该研究中所有双语词典都映射对应回英语。",
        "answer": "to",
        "acceptable": ["to"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·学术词组】<b>map back to ...</b> 意为“映射回、归结对应至……”。<b>to</b> 表示方向与对应终点。",
        "tags": ["作业帮真题", "学术词汇"]
    },
    {
        "id": "zyb_10",
        "phrase": "emerge in response ___ daily demands",
        "sentence": "A new word will often emerge in response ___ its demand in daily life.",
        "sentence_cn": "新词汇往往会顺应日常生活中的实际需求而应运而生。",
        "answer": "to",
        "acceptable": ["to"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·选项原句】<b>in response to ...</b> 意为“作为对……的回应、顺应……”。注意这里的 <b>to 是介词</b>，后面接名词/代词。<br>【同类拓展】<b>in reply to</b>（回复）、<b>in answer to</b>（回应）。",
        "tags": ["作业帮真题", "阅读真题", "高频介词"]
    },
    {
        "id": "zyb_11",
        "phrase": "increase undergraduate enrollment ___ about 150",
        "sentence": "Tsinghua University plans to increase its undergraduate enrollment ___ about 150 in 2025.",
        "sentence_cn": "清华大学计划在2025年将本科招生人数增加约150人。",
        "answer": "by",
        "acceptable": ["by"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【高考模考真题·语法填空】<b>increase by ...</b> 表示“增加了……”（后接幅度/差额），而 <b>increase to ...</b> 表示“增加到……”（后接最终总量）。题目中是增加额度，故填 <b>by</b>。<br>【真题出处】北京市西城区高三统测试题 语法填空题。",
        "tags": ["作业帮真题", "高考填空", "幅度介词"]
    },
    {
        "id": "zyb_12",
        "phrase": "make use ___ Tsinghua's strengths",
        "sentence": "The new school will make use ___ Tsinghua's strengths in technology.",
        "sentence_cn": "新学院将充分利用清华大学在科技领域的优势。",
        "answer": "of",
        "acceptable": ["of"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·固定词组】<b>make use of ...</b> 意为“利用、使用”。<br>【拓展表达】<b>make good/full use of</b>（充分利用）、<b>make the most of</b>（尽量利用）。",
        "tags": ["作业帮真题", "高考填空", "常用搭配"]
    },
    {
        "id": "zyb_13",
        "phrase": "aim ___ explore AI-driven learning models",
        "sentence": "It aims ___ explore AI-driven learning models and develop student skills.",
        "sentence_cn": "它的目标是探索AI驱动的学习模式并培养学生技能。",
        "answer": "to",
        "acceptable": ["to"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·动词句型】<b>aim to do sth</b> 意为“旨在、目的在于做某事”。也可表达为 <b>aim at doing sth</b>。",
        "tags": ["作业帮真题", "高考填空"]
    },
    {
        "id": "zyb_14",
        "phrase": "benefit ___ our community donations",
        "sentence": "Many vulnerable families benefited greatly ___ our donations.",
        "sentence_cn": "许多困难家庭从我们的捐款中大获裨益。",
        "answer": "from",
        "acceptable": ["from"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·动词搭配】<b>benefit from ...</b> 意为“从……中获益、得益于”。注意主语是受益者；如果是某事物有利于某人，则用 <b>benefit sb / be of benefit to sb</b>。",
        "tags": ["作业帮真题", "高考填空", "高频考点"]
    },
    {
        "id": "zyb_15",
        "phrase": "completed its first lift ___ March 2024",
        "sentence": "The super crane completed its remarkable first lift ___ March 2024.",
        "sentence_cn": "这台超级起重机于2024年3月完成了引人注目的首次吊装。",
        "answer": "in",
        "acceptable": ["in"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·时间介词】在年月、季节、世纪前用介词 <b>in</b>（如 in March 2024, in spring）；在具体某一天或某天的早中晚用 <b>on</b>（如 on March 5th, on Monday morning）；在钟点前用 <b>at</b>（如 at 3:00）。",
        "tags": ["作业帮真题", "高考填空", "时间介词"]
    },
    {
        "id": "zyb_16",
        "phrase": "lifted blades to a height ___ 162 meters",
        "sentence": "It lifted the heavy blades to a dizzying height ___ 162 meters.",
        "sentence_cn": "它将沉重的叶片提升到了162米的惊人高度。",
        "answer": "of",
        "acceptable": ["of"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·度量介词】<b>to a height / depth / length of ...</b> 表示“达到……的高度/深度/长度”。介词 <b>of</b> 引出具体的度量数值。",
        "tags": ["作业帮真题", "高考填空", "度量表达"]
    },
    {
        "id": "zyb_17",
        "phrase": "felt an immediate sense ___ belonging",
        "sentence": "They moved to the city and felt an immediate sense ___ belonging.",
        "sentence_cn": "他们搬到这座城市，立即感受到了一种归属感。",
        "answer": "of",
        "acceptable": ["of"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【高考模考真题·名词词组】<b>a sense of belonging</b> 意为“归属感”。<br>【同类拓展】<b>a sense of humor</b>（幽默感）、<b>a sense of achievement</b>（成就感）、<b>a sense of responsibility</b>（责任感）。",
        "tags": ["作业帮真题", "完形填空", "常用搭配"]
    },
    {
        "id": "zyb_18",
        "phrase": "take them ___ your hands",
        "sentence": "If you have unwanted items, we will gladly take them ___ your hands.",
        "sentence_cn": "如果你有多余不用的物品，我们很乐意替你接手处理。",
        "answer": "off",
        "acceptable": ["off"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【高考模考真题·地道习语】<b>take sth off sb's hands</b> 意为“从某人手里接管/买下（不再需要的东西），替某人分担负担”。<br>【真题原句】We'll take them off your hands.",
        "tags": ["作业帮真题", "完形填空", "习语搭配"]
    },
    {
        "id": "zyb_19",
        "phrase": "devote several days a week ___ picking up flowers",
        "sentence": "The volunteers devote their weekends ___ helping stray animals.",
        "sentence_cn": "志愿者们把周末时间都奉献给救助流浪动物。",
        "answer": "to",
        "acceptable": ["to"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【高考模考真题·经典陷阱】<b>devote ... to (doing) sth</b> 表示“把……投入/奉献给……”。特别注意：这里的 <b>to 是介词</b>，后面接动名词（doing）或名词，是高考英语最高频的考点之一！",
        "tags": ["作业帮真题", "完形填空", "动名词搭配"]
    },
    {
        "id": "zyb_20",
        "phrase": "make a real difference ___ each other's lives",
        "sentence": "Kind neighbors can come together to make a real difference ___ each other's lives.",
        "sentence_cn": "热心的邻居们齐心协力，能为彼此的生活带来真正的改变。",
        "answer": "in",
        "acceptable": ["in", "to"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【高考模考真题·高频搭配】<b>make a difference in / to ...</b> 意为“对……产生影响/带来改变”。<b>in one's life</b> 强调在生活内部各个方面产生积极影响。<br>【真题原句】come together to make a real difference in each other's lives.",
        "tags": ["作业帮真题", "高考常考", "写作高频"]
    },
    {
        "id": "zyb_21",
        "phrase": "correlation ___ distracted eating and weight gain",
        "sentence": "Studies show a correlation ___ distracted eating and weight gain.",
        "sentence_cn": "研究表明分心饮食与体重增加之间存在关联。",
        "answer": "between",
        "acceptable": ["between"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·七选五真题】<b>a correlation between A and B</b> 意为“A与B之间的相关性/关联”。介词 <b>between</b> 连接两个互相影响的事物。",
        "tags": ["作业帮真题", "七选五", "学术词汇"]
    },
    {
        "id": "zyb_22",
        "phrase": "the body needs to be ___ a relaxed state",
        "sentence": "The human body needs to be ___ a relaxed state for healthy digestion.",
        "sentence_cn": "人体需要处于放松状态才能保持健康消化。",
        "answer": "in",
        "acceptable": ["in"],
        "category": "作业帮真题",
        "difficulty": 1,
        "explanation": "【作业帮真题·状态介词】<b>in a state of ...</b> 意为“处于……的状态中”。表示状态、境况通常使用介词 <b>in</b>，如 in good condition（处于良好状态）、in trouble（身处困境）。",
        "tags": ["作业帮真题", "七选五", "状态介词"]
    },
    {
        "id": "zyb_23",
        "phrase": "be at peace ___ the difficult situation",
        "sentence": "You must learn to accept reality and be at peace ___ that.",
        "sentence_cn": "你必须学会接受现实，并对此保持释怀与内心的平静。",
        "answer": "with",
        "acceptable": ["with"],
        "category": "作业帮真题",
        "difficulty": 2,
        "explanation": "【作业帮真题·七选五选项】<b>be at peace with sth/sb</b> 意为“与……和解、对……感到释怀/坦然接受”。介词 <b>with</b> 表示对象关系。",
        "tags": ["作业帮真题", "七选五", "地道表达"]
    },
    {
        "id": "zyb_24",
        "phrase": "a voice note is a demand ___ someone else's time",
        "sentence": "Sending an unrequested voice note is a demand ___ someone else's precious time.",
        "sentence_cn": "随意发送语音消息是对他人宝贵时间的一种索取。",
        "answer": "on",
        "acceptable": ["on"],
        "category": "作业帮真题",
        "difficulty": 3,
        "explanation": "【作业帮真题·七选五选项】<b>a demand on / upon sb/sth</b> 表示“对……的要求、占用、索取或沉重负担”。例如：The job makes heavy demands on her energy.（这项工作极度消耗她的精力）。",
        "tags": ["作业帮真题", "七选五", "高阶介词"]
    }
]


def crawl_zuoyebang_link(share_url: str) -> list[dict]:
    """
    Crawls a Zuoyebang share link and extracts English cloze/quiz items.
    """
    if not fetch_question or not normalize:
        raise RuntimeError("zyb crawler module not found")

    data = fetch_question(share_url)
    prob = normalize(data, share_url=share_url)

    text = html.unescape(prob.share_content or "")
    # Check if there is item question_html
    for it in prob.items:
        if it.question_html:
            text += "\n" + html.unescape(it.question_html)

    extracted_questions = []

    # 1. Look for explicit fill-in-the-blank patterns: (1) ... ______ / ___
    sub_patterns = re.findall(r'[（\(](\d+)[）\)](.*?)(?=[（\(]\d+[）\)]|$)', text, re.DOTALL)
    for num, q_body in sub_patterns:
        cleaned_body = q_body.strip()
        # Look for blanks
        if '___' in cleaned_body or '______' in cleaned_body:
            # Check options A. B. C. D.
            opts = re.findall(r'([A-D])\.([^\sA-D]+)', cleaned_body)
            # Find the sentence part before options
            sent_part = re.split(r'[A-D]\.', cleaned_body)[0].strip()
            # If there's an option match
            ans = ""
            acceptable = []
            if opts:
                # Prepositions often appear in cloze options
                acceptable = [o[1].strip().lower() for o in opts]
                ans = acceptable[0] if acceptable else ""

            extracted_questions.append({
                "id": f"zyb_c_{int(num):02d}_{abs(hash(share_url)) % 10000}",
                "phrase": f"Zuoyebang Q{num}",
                "sentence": sent_part,
                "sentence_cn": f"【作业帮真题第{num}题】",
                "answer": ans or "to",
                "acceptable": acceptable or ["to"],
                "category": "作业帮真题",
                "difficulty": 2,
                "explanation": f"【作业帮真题第{num}题解析】来源：{share_url}",
                "tags": ["作业帮真题", "爬虫抓取"]
            })

    # If no explicit numbered items, extract sentences containing prepositions
    if not extracted_questions:
        # Split text into sentences
        sentences = re.split(r'(?<=[.?!;])\s+', text)
        for s in sentences:
            s_clean = s.strip()
            # If sentence contains English prepositions and length is reasonable
            if 30 < len(s_clean) < 180 and re.search(r'\b(to|in|on|at|by|for|with|about|into|from|between|through)\b', s_clean, re.I):
                match = re.search(r'\b(to|in|on|at|by|for|with|about|into|from|between|through)\b', s_clean, re.I)
                if match:
                    prep = match.group(0).lower()
                    blanked_sent = s_clean[:match.start()] + '___' + s_clean[match.end():]
                    extracted_questions.append({
                        "id": f"zyb_ext_{abs(hash(s_clean)) % 100000}",
                        "phrase": f"cloze: {prep}",
                        "sentence": blanked_sent,
                        "sentence_cn": "【作业帮英语阅读真题金句填空】",
                        "answer": prep,
                        "acceptable": [prep],
                        "category": "作业帮真题",
                        "difficulty": 2,
                        "explanation": f"【作业帮真题语境】原句为：<i>{s_clean}</i><br>介词 <b>{prep}</b> 在句中与前后文搭配，请注意在真实考试阅读篇章中的地道用法。",
                        "tags": ["作业帮真题", "阅读真题", "语境真题"]
                    })
                    if len(extracted_questions) >= 5:
                        break

    return extracted_questions


if __name__ == '__main__':
    print(f"Loaded {len(ZYB_CURATED_QUESTIONS)} curated Zuoyebang exam questions.")
