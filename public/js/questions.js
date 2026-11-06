// 介词填空题库数据 (Preposition Collocations Question Bank)
const PREPOSITION_QUESTIONS = [
  {
    "id": "v01",
    "phrase": "dance ___ music",
    "sentence": "The children love to dance ___ the music.",
    "sentence_cn": "孩子们喜欢随着音乐跳舞。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>dance to ...</b> 表示“随着……（节拍/旋律/音乐）跳舞”。这里的介词 <b>to</b> 表示“配合、伴随、对应……的节拍”，相当于 in time to / accompanied by。<br>【常见误区】切勿用中式思维直译为 <i>dance with music</i>。<i>with</i> 通常表示与某人共舞（如 dance with him），而随着音乐节奏则固定用 <b>to</b>。<br>【同类拓展】<b>sing to the guitar</b>（伴着吉他声唱歌）、<b>march to the drumbeat</b>（随着鼓点行进）、<b>sway to the rhythm</b>（随着节奏摇摆）。",
    "tags": [
      "高频核心",
      "常考易错"
    ]
  },
  {
    "id": "v02",
    "phrase": "listen ___ the radio",
    "sentence": "She likes to listen ___ the radio while cooking dinner.",
    "sentence_cn": "她喜欢一边做晚饭一边听收音机。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>listen</b> 是不及物动词，接宾语时必须加上介词 <b>to</b>，表示“倾听、听从”。<br>【记忆口诀】听到什么用 to，听人劝告用 listen to advice。<br>【同类拓展】<b>pay attention to</b>（注意）、<b>attend to</b>（专心于、照料）。",
    "tags": [
      "基础高频"
    ]
  },
  {
    "id": "v03",
    "phrase": "look forward ___ hearing from you",
    "sentence": "I am looking forward ___ hearing from you soon.",
    "sentence_cn": "我期待着早日收到您的来信。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>look forward to</b> 表示“盼望、期待”。注意这里的 <b>to 是介词</b>，而不是不定式符号，后面必须接名词或动名词（doing），常考语法陷阱！<br>【经典考点】I look forward to <i>seeing</i> you (不能用 see)。<br>【同类含介词to的短语】<b>devote oneself to</b> doing、<b>object to</b> doing、<b>be accustomed to</b> doing。",
    "tags": [
      "常考陷阱",
      "动名词搭配"
    ]
  },
  {
    "id": "v04",
    "phrase": "depend ___ your hard work",
    "sentence": "Your success will depend ___ how much effort you put in.",
    "sentence_cn": "你的成功取决于你付出了多少努力。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>depend on / upon</b> 表示“依靠、取决于、视……而定”。<br>【同类拓展】<b>rely on</b>（依赖）、<b>count on</b>（指望）、<b>hinge on</b>（以……为转移/关键取决于）。<br>【日常表达】<i>That depends.</i>（视情况而定 / 那可不一定）。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v05",
    "phrase": "insist ___ doing things her own way",
    "sentence": "She insisted ___ paying for everyone's meal.",
    "sentence_cn": "她坚持要为所有人的餐费买单。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>insist on / upon (doing) sth</b> 表示“坚持要（做某事）、一定要”。<br>【对比辨析】若后接 that 从句，则从句谓语动词常用虚拟语气 (should) do：<i>He insisted that we (should) leave at once.</i> 但接宾语/动名词时必须用 <b>on</b>。",
    "tags": [
      "常考搭配"
    ]
  },
  {
    "id": "v06",
    "phrase": "prevent him ___ making a mistake",
    "sentence": "Nothing can prevent us ___ achieving our dreams.",
    "sentence_cn": "没有什么能阻止我们实现梦想。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>prevent sb/sth from doing sth</b> 表示“阻止/防止某人做某事”。介词 <b>from</b> 具有“远离、阻隔、分离”的核心概念。<br>【同类句型】<b>stop sb (from) doing</b>、<b>keep sb from doing</b>（keep 中的 from 不可省）、<b>ban sb from doing</b>、<b>discourage sb from doing</b>。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v07",
    "phrase": "remind me ___ my hometown",
    "sentence": "This old melody always reminds me ___ my childhood.",
    "sentence_cn": "这首老旋律总是让我想起童年。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>remind sb of sth</b> 表示“提醒某人某事，让某人想起某事”。这里的 <b>of</b> 引出关联内容。<br>【对比】<i>remind sb to do sth</i>（提醒某人去做某事）；<i>remind sb that ...</i>（提醒某人……）。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v08",
    "phrase": "result ___ great success",
    "sentence": "Continuous practice will ultimately result ___ mastery.",
    "sentence_cn": "持续的练习最终会带来精通熟练。",
    "answer": "in",
    "acceptable": [
      "in"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【易混辨析】<br>1. <b>result in</b>：导致、产生某种结果（主语是因，宾语是果），相当于 <i>lead to / bring about</i>。<br>2. <b>result from</b>：由……引起、起因于（主语是果，宾语是因），相当于 <i>be caused by</i>。<br>例：Hard work resulted <b>in</b> success. vs Success resulted <b>from</b> hard work.",
    "tags": [
      "易混辨析",
      "高频考点"
    ]
  },
  {
    "id": "v09",
    "phrase": "accuse him ___ theft",
    "sentence": "The police accused the suspect ___ stealing the jewelry.",
    "sentence_cn": "警方指控嫌疑人盗窃珠宝。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>accuse sb of (doing) sth</b> 表示“指控/指责某人犯某罪或做错事”。<br>【常考辨析】对比 <b>charge sb with sth</b>（同样是指控某人某罪，但 charge 必须搭配 with！）。口诀：accuse of, charge with！",
    "tags": [
      "易混辨析",
      "常考核心"
    ]
  },
  {
    "id": "v10",
    "phrase": "belong ___ the library",
    "sentence": "This precious edition belongs ___ the municipal library.",
    "sentence_cn": "这本珍贵的版本属于市立图书馆。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>belong to</b> 表示“属于；是……的一员”。<br>【重要语法点】belong to <b>没有被动语态</b>，也<b>不能用于进行时</b>！只能说 <i>It belongs to me</i>，不能说 <i>It is belonged to me</i>。",
    "tags": [
      "基础高频",
      "语法规则"
    ]
  },
  {
    "id": "v11",
    "phrase": "succeed ___ solving the puzzle",
    "sentence": "After days of effort, they finally succeeded ___ finding the solution.",
    "sentence_cn": "经过数天的努力，他们终于成功找到了解决办法。",
    "answer": "in",
    "acceptable": [
      "in"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>succeed in (doing) sth</b> 表示“在……方面取得成功、成功做成某事”。<br>【同义替换】<i>manage to do sth</i>（设法做成了某事）。<br>【注意区分】succeed 作为及物动词时表示“继承、接替”，如 <i>succeed to the throne</i>（继承王位）。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v12",
    "phrase": "apologize ___ her for the delay",
    "sentence": "He went to apologize ___ the manager for being late.",
    "sentence_cn": "他去找经理为迟到而道歉。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】完整搭配为：<b>apologize to sb for sth</b>（向某人为某事道歉）。<br>【介词记忆】对象用 <b>to</b>（指向人），原因用 <b>for</b>（因为某事）。<br>名词形式：<b>make an apology to sb for sth</b>。",
    "tags": [
      "日常高频"
    ]
  },
  {
    "id": "v13",
    "phrase": "concentrate ___ your study",
    "sentence": "Turn off the phone so that you can concentrate ___ your work.",
    "sentence_cn": "把手机关掉，这样你才能专心于工作。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>concentrate on (doing) sth</b> 表示“全神贯注于、集中注意力于”。<br>【同类短语】<b>focus on</b>（聚焦于）、<b>be centered on</b>（以……为中心）。",
    "tags": [
      "日常高频"
    ]
  },
  {
    "id": "v14",
    "phrase": "graduate ___ Oxford University",
    "sentence": "She graduated ___ Oxford with honors last summer.",
    "sentence_cn": "去年夏天她以优异的成绩从牛津大学毕业。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>graduate from + 学校</b> 表示“从某校毕业”。<br>【对比辨析】<b>graduate in + 专业</b>（如 graduate in physics 毕业于物理专业）。从哪所学校出来用 <b>from</b>（表示来源出处）。",
    "tags": [
      "易混辨析"
    ]
  },
  {
    "id": "v15",
    "phrase": "consist ___ five chapters",
    "sentence": "The committee consists ___ seven experienced members.",
    "sentence_cn": "该委员会由七名经验丰富的成员组成。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>consist of</b> 表示“由……组成/构成”。<br>【语法红线】consist of <b>不可用于被动语态</b>！不能写成 <i>is consisted of</i>。<br>【同义替换（有被动）】<b>be composed of</b>、<b>be made up of</b>、<b>comprise</b>。",
    "tags": [
      "常考陷阱",
      "语法规则"
    ]
  },
  {
    "id": "v16",
    "phrase": "comply ___ safety regulations",
    "sentence": "All employees are strictly required to comply ___ safety rules.",
    "sentence_cn": "所有员工都必须严格遵守安全规程。",
    "answer": "with",
    "acceptable": [
      "with"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>comply with</b> 表示“顺从、遵照、符合（规定、法律、要求）”。<br>【同类表达】<b>abide by</b> the rules、<b>conform to</b> standards、<b>adhere to</b> policies。",
    "tags": [
      "书面用语",
      "常考核心"
    ]
  },
  {
    "id": "v17",
    "phrase": "differ ___ each other",
    "sentence": "British English differs ___ American English in several aspects.",
    "sentence_cn": "英式英语在几个方面不同于美式英语。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>differ from sb/sth</b> 表示“与……不同/有区别”，from 表示差异的对比基准。<br>【拓展搭配】<b>differ with sb on/about sth</b> 表示“在某事上与某人意见分歧”。形容词：<b>be different from</b>。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v18",
    "phrase": "participate ___ class discussions",
    "sentence": "Every student is encouraged to participate actively ___ group work.",
    "sentence_cn": "鼓励每位学生积极参与小组讨论。",
    "answer": "in",
    "acceptable": [
      "in"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>participate in</b> 表示“参加、参与某项活动”，in 表示进入活动情境之中。<br>【同义短语】<b>take part in</b>、<b>join in</b>。",
    "tags": [
      "基础高频"
    ]
  },
  {
    "id": "v19",
    "phrase": "rob the bank ___ all its cash",
    "sentence": "The masked bandits robbed the jewelry store ___ valuable gems.",
    "sentence_cn": "蒙面劫匪抢劫了珠宝店所有贵重的宝石。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>rob sb/sw of sth</b> 表示“抢劫某人/某处的某物”。注意：被抢的人/地点作宾语，被抢走的财物跟在介词 <b>of</b> 后面。<br>【对比辨析】<b>steal sth from sb/sw</b>（steal 后直接接被偷的物品！）。口诀：rob人/地点 of 财物，steal 财物 from 人/地点。",
    "tags": [
      "常考陷阱",
      "易混辨析"
    ]
  },
  {
    "id": "v20",
    "phrase": "devote herself ___ scientific research",
    "sentence": "Marie Curie devoted her whole life ___ the study of radioactivity.",
    "sentence_cn": "居里夫人将毕生精力奉献给了放射性研究。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>devote oneself/time/energy to (doing) sth</b> 表示“投身于、致力于某事”。这里的 <b>to 是介词</b>，后面接名词或动名词！<br>【被动形式】<b>be devoted to (doing) sth</b>（专心于、深爱……）。",
    "tags": [
      "高频考点",
      "动名词搭配"
    ]
  },
  {
    "id": "v21",
    "phrase": "substitute apple sauce ___ oil",
    "sentence": "In this healthy recipe, you can substitute yogurt ___ cream.",
    "sentence_cn": "在这个健康食谱中，你可以用酸奶代替奶油。",
    "answer": "for",
    "acceptable": [
      "for"
    ],
    "category": "动词搭配",
    "difficulty": 3,
    "explanation": "【用法解析】<b>substitute A for B</b> 结构中，A 是“新用的替代品”，B 是“被替换掉的原物”，意为“用 A 替代 B”。这里的 <b>for</b> 表示“代表/替代原有之物”。<br>【容易混淆】<i>replace B with A</i>（用 A 替换 B，注意宾语顺序和介词不同！）。",
    "tags": [
      "常考陷阱",
      "深度辨析"
    ]
  },
  {
    "id": "v22",
    "phrase": "cure the patient ___ the disease",
    "sentence": "Modern penicillin helped cure millions ___ dangerous infections.",
    "sentence_cn": "现代青霉素治愈了数百万人致命的感染疾病。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>cure sb of sth</b> 表示“治愈某人的某种疾病/去除某人的某种恶习”。这里的 <b>of</b> 具有剥离、去除含义（同 rob sb of, clear sb of, rid sb of）。<br>【辨析】cure 后接人，后面 of 接疾病。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "v23",
    "phrase": "congratulate him ___ winning the prize",
    "sentence": "We gathered to congratulate our colleague ___ his promotion.",
    "sentence_cn": "我们聚在一起祝贺同事晋升。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>congratulate sb on (doing) sth</b> 表示“就某事向某人道贺”。这里的介词必须用 <b>on</b>！<br>【易错提醒】很多同学误用 for，请牢记：congratulate sb <b>on</b> sth！名词同理：<i>congratulations on your graduation!</i>",
    "tags": [
      "常考易错",
      "高频核心"
    ]
  },
  {
    "id": "v24",
    "phrase": "cater ___ the needs of consumers",
    "sentence": "The new entertainment app caters ___ the tastes of teenagers.",
    "sentence_cn": "这款全新的娱乐应用迎合了青少年的喜好。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>cater to sb/sth</b> 表示“迎合、满足……的需要或偏好”。<br>【拓展】<b>cater for</b> 多用于英式英语中表示“为……提供饮食或服务”，而在表达“迎合某种口味/需求”时普遍用 <b>cater to</b>。",
    "tags": [
      "高频词组"
    ]
  },
  {
    "id": "v25",
    "phrase": "hinge ___ the judge's final verdict",
    "sentence": "The future of the company hinges ___ the outcome of this negotiation.",
    "sentence_cn": "公司的前途完全取决于这次谈判的结果。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon"
    ],
    "category": "动词搭配",
    "difficulty": 3,
    "explanation": "【用法解析】<b>hinge on / upon</b> 字面意为“铰链安装在……上”，引申为“完全取决于……、以……为枢纽/关键”。相当于 <i>depend entirely on</i>。<br>例：Everything hinges on your decision.",
    "tags": [
      "高级写作",
      "高阶短语"
    ]
  },
  {
    "id": "a01",
    "phrase": "be accustomed ___ working late",
    "sentence": "Having lived in London for five years, he is accustomed ___ rainy weather.",
    "sentence_cn": "在伦敦生活了五年后，他已经习惯了阴雨天气。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>be accustomed to (doing) sth</b> 表示“习惯于……”。其中的 <b>to 是介词</b>，后面接名词或动名词！<br>【同义替换】<b>be used to (doing) sth</b>。<br>【混淆提醒】注意区分 <i>used to do sth</i>（过去常常做某事，to是不定式，接动词原形）。",
    "tags": [
      "常考重点",
      "动名词搭配"
    ]
  },
  {
    "id": "a02",
    "phrase": "be proud ___ her son",
    "sentence": "The parents were immensely proud ___ their daughter's courage.",
    "sentence_cn": "父母为女儿的勇敢感到无比自豪。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be proud of sb/sth</b> 表示“为……感到骄傲/自豪”。<br>【同根动词替换】<b>take pride in</b>（以……为豪，注意名词搭配是 in！）；<b>pride oneself on</b>（在……方面感到自豪，反身动词搭配 on！）。三种句型介词各不相同，必考题！",
    "tags": [
      "基础高频",
      "三套变换"
    ]
  },
  {
    "id": "a03",
    "phrase": "be capable ___ doing the task",
    "sentence": "She has proven that she is capable ___ leading the research team.",
    "sentence_cn": "她已经证明了自己完全有能力领导该研究团队。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be capable of (doing) sth</b> 表示“有能力做某事、能胜任”。<br>【对比辨析】<b>be able to do sth</b>（able 接不定式 to do，而 capable 搭配 of + doing / 名词）。",
    "tags": [
      "高频核心",
      "对比记忆"
    ]
  },
  {
    "id": "a04",
    "phrase": "be addicted ___ online games",
    "sentence": "Many teenagers become addicted ___ smartphone screens.",
    "sentence_cn": "许多青少年对手机屏幕上了瘾。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be addicted to sth / doing sth</b> 表示“对……上瘾、沉溺于”。其中的 <b>to 是介词</b>。<br>【同类短语】<b>be hooked on</b>（迷上）、<b>be obsessed with</b>（痴迷于）。",
    "tags": [
      "日常高频"
    ]
  },
  {
    "id": "a05",
    "phrase": "be famous ___ its delicate cuisine",
    "sentence": "France is famous ___ its wine, cheese, and romantic culture.",
    "sentence_cn": "法国因其葡萄酒、奶酪和浪漫文化而闻名。",
    "answer": "for",
    "acceptable": [
      "for"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【辨析三剑客】<br>1. <b>be famous for</b>：因某种特质/产物而著名（for表原因）。<br>2. <b>be famous as</b>：作为某种身份而闻名（as表作为）。例：He is famous as a poet.<br>3. <b>be famous to</b>：对某人群而言广为人知（to表对象）。例：His name is famous to children.",
    "tags": [
      "易混辨析",
      "高频考点"
    ]
  },
  {
    "id": "a06",
    "phrase": "be good ___ playing chess",
    "sentence": "My little brother is exceptionally good ___ mathematics.",
    "sentence_cn": "我弟弟在数学方面特别擅长。",
    "answer": "at",
    "acceptable": [
      "at"
    ],
    "category": "易混辨析",
    "difficulty": 1,
    "explanation": "【good 搭配辨析】<br>1. <b>be good at</b>：擅长于某领域/活动。<br>2. <b>be good for</b>：对……有益处（例：Vegetables are good for health）。<br>3. <b>be good to</b>：对某人友好、关照（例：She has always been good to us）。",
    "tags": [
      "基础高频",
      "易混辨析"
    ]
  },
  {
    "id": "a07",
    "phrase": "be interested ___ ancient architecture",
    "sentence": "Ever since childhood, he has been keenly interested ___ astronomy.",
    "sentence_cn": "从童年起，他就对天文学产生了浓厚的兴趣。",
    "answer": "in",
    "acceptable": [
      "in"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be interested in (doing) sth</b> 表示“对……感兴趣”。<br>【名词搭配】<b>show/have an interest in</b>（同样用 in）。<br>【动词短语】<b>take an interest in</b>。",
    "tags": [
      "基础核心"
    ]
  },
  {
    "id": "a08",
    "phrase": "be responsible ___ customer safety",
    "sentence": "The flight captain is directly responsible ___ the safety of all passengers.",
    "sentence_cn": "机长对所有乘客的安全负有直接责任。",
    "answer": "for",
    "acceptable": [
      "for"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be responsible for sth/doing sth</b> 表示“对某事负责任；是导致……的原因”。<br>【如果对人负责】<b>be responsible to sb</b>（向某人负责/汇报，如 responsible to the Board of Directors）。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "a09",
    "phrase": "be similar ___ the original model",
    "sentence": "Your new laptop is remarkably similar ___ mine in design.",
    "sentence_cn": "你的新笔记本电脑在外观设计上与我的非常相似。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be similar to sb/sth</b> 表示“与……相似”。这里的介词是 <b>to</b>，切勿误用 with。<br>【同反义词】反义：<b>be different from</b>；相同：<b>the same as</b>。",
    "tags": [
      "基础高频"
    ]
  },
  {
    "id": "a10",
    "phrase": "be tired ___ doing repetitive homework",
    "sentence": "She was sick and tired ___ his constant complaints.",
    "sentence_cn": "她对他没完没了的抱怨感到厌烦透顶。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【易混辨析】<br>1. <b>be tired of</b>：对……感到厌烦/厌倦（心理上的腻烦）。<br>2. <b>be tired from / with</b>：因……而感到疲惫/劳累（生理上的劳累）。<br>例：I am tired <b>from</b> walking all day, and I am tired <b>of</b> this boring meeting.",
    "tags": [
      "易混辨析",
      "常考考点"
    ]
  },
  {
    "id": "a11",
    "phrase": "be keen ___ learning new skills",
    "sentence": "The fresh graduates are very keen ___ taking on challenging projects.",
    "sentence_cn": "应届毕业生非常渴望承担具有挑战性的项目。",
    "answer": "on",
    "acceptable": [
      "on"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>be keen on (doing) sth</b> 表示“热衷于、喜爱、对……着迷”。<br>【对比】<i>be keen to do sth</i>（急于/渴望做某事，后接不定式）。",
    "tags": [
      "英式常用",
      "高频短语"
    ]
  },
  {
    "id": "a12",
    "phrase": "be indifferent ___ public criticism",
    "sentence": "He remained completely indifferent ___ the rumors circulating about him.",
    "sentence_cn": "他对周围流传的关于自己的谣言完全无动于衷。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>be indifferent to sth</b> 表示“对……漠不关心、无动于衷”。这里的 <b>to</b> 表示心理感受所朝向的对象。<br>【同义词】<b>unconcerned about</b>、<b>apathetic toward</b>。",
    "tags": [
      "常考重点",
      "四六级核心"
    ]
  },
  {
    "id": "a13",
    "phrase": "be immune ___ the virus",
    "sentence": "People who recovered from the mild illness were found to be immune ___ the virus.",
    "sentence_cn": "被发现康复的轻症患者对该病毒产生了免疫力。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>be immune to sth</b> 表示“对……有免疫力的；不受……影响的”。<br>引申用法：<i>No one is immune to flattery.</i>（没有人能对奉承阿谀完全不动心）。",
    "tags": [
      "常考核心"
    ]
  },
  {
    "id": "a14",
    "phrase": "be susceptible ___ catching a cold",
    "sentence": "Elderly individuals are particularly susceptible ___ respiratory infections in winter.",
    "sentence_cn": "老年人在冬季尤其容易受到呼吸道感染的影响。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "形容词搭配",
    "difficulty": 3,
    "explanation": "【用法解析】<b>be susceptible to sth</b> 表示“易受……影响的、易患……病的”。<br>【同类表达】<b>be vulnerable to</b>（容易受到……伤害/攻击）。介词均使用 <b>to</b>。",
    "tags": [
      "高阶词汇",
      "考研雅思"
    ]
  },
  {
    "id": "a15",
    "phrase": "be ashamed ___ his bad behavior",
    "sentence": "You should be ashamed ___ lying to your best friends.",
    "sentence_cn": "你应该为欺骗自己最好的朋友而感到羞愧。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be ashamed of (doing) sth</b> 表示“为某事感到羞愧/惭愧”。<br>【对比】<i>be ashamed to do sth</i>（难为情/不好意思去做某事）。",
    "tags": [
      "日常高频"
    ]
  },
  {
    "id": "p01",
    "phrase": "at the expense ___ your physical health",
    "sentence": "Do not pursue rapid success at the expense ___ your health.",
    "sentence_cn": "不要以牺牲你的健康为代价去追求快速成功。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>at the expense of ...</b> 表示“以……为代价、牺牲……”。这里的 <b>of</b> 引出被牺牲的事物。<br>【同义短语】<b>at the cost of ...</b>、<b>at the sacrifice of ...</b>。",
    "tags": [
      "书面写作",
      "常考短语"
    ]
  },
  {
    "id": "p02",
    "phrase": "in terms ___ overall performance",
    "sentence": "In terms ___ user engagement, the new feature was a huge success.",
    "sentence_cn": "从用户参与度的角度来看，新功能取得了巨大成功。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 1,
    "explanation": "【用法解析】<b>in terms of ...</b> 表示“在……方面、从……的角度来看”。是学术写作与职场高频过渡短语。<br>例：What does this mean <i>in terms of</i> cost?",
    "tags": [
      "写作必备",
      "高频核心"
    ]
  },
  {
    "id": "p03",
    "phrase": "on behalf ___ our whole class",
    "sentence": "I would like to express our gratitude on behalf ___ the entire team.",
    "sentence_cn": "我想代表整个团队表达我们的由衷谢意。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 1,
    "explanation": "【用法解析】<b>on behalf of sb</b> 表示“代表某人、为了某人的利益”。<br>【英美拼写】美式常用 <i>on behalf of</i>，英式也可见 <i>in behalf of</i>（常表利益），通常统一使用 <b>on behalf of</b>。",
    "tags": [
      "高频核心",
      "正式场合"
    ]
  },
  {
    "id": "p04",
    "phrase": "by means ___ relentless efforts",
    "sentence": "Humans communicate abstract thoughts by means ___ complex language.",
    "sentence_cn": "人类通过复杂的语言手段来交流抽象的思想。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>by means of ...</b> 表示“依靠……方式、通过……手段”。<br>【相关短语辨析】<br><b>by all means</b>：当然可以、务必；<br><b>by no means</b>：决不、决非（置于句首句子倒装）。",
    "tags": [
      "经典短语",
      "倒装考点"
    ]
  },
  {
    "id": "p05",
    "phrase": "in accordance ___ official guidelines",
    "sentence": "The building was erected strictly in accordance ___ fire safety standards.",
    "sentence_cn": "该建筑物严格按照消防安全标准建造。",
    "answer": "with",
    "acceptable": [
      "with"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>in accordance with ...</b> 表示“依照、根据、与……一致”。注意这里的介词必须使用 <b>with</b>！<br>【同义替换】<i>in line with</i>、<i>according to</i>、<i>in compliance with</i>。",
    "tags": [
      "正式用语",
      "常考核心"
    ]
  },
  {
    "id": "p06",
    "phrase": "with regard ___ the current project",
    "sentence": "Do you have any further questions with regard ___ the proposed budget?",
    "sentence_cn": "关于所拟议的预算，您还有什么进一步的问题吗？",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>with regard to ...</b> 表示“关于、至于”。这里的介词固定搭配为 <b>to</b>。<br>【特别注意】不要写成 <i>with regards to</i>（加了s是不规范用法）；也可以写成 <b>in regard to</b> 或直接用 <b>regarding</b>。",
    "tags": [
      "写作高频",
      "常考易错"
    ]
  },
  {
    "id": "p07",
    "phrase": "in spite ___ the heavy downpour",
    "sentence": "They carried on the open-air concert in spite ___ the heavy downpour.",
    "sentence_cn": "尽管暴雨倾盆，他们依然继续举行露天音乐会。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 1,
    "explanation": "【用法解析】<b>in spite of ...</b> 表示“尽管、虽然”，介词为 <b>of</b>，后接名词或代词。<br>【常考替换】<b>despite</b>（注意：despite 后面<b>绝对不加 of</b>！即 despite the rain = in spite of the rain）。",
    "tags": [
      "语法陷阱",
      "高频考点"
    ]
  },
  {
    "id": "p08",
    "phrase": "at the mercy ___ violent sea storms",
    "sentence": "The tiny wooden raft was left at the mercy ___ the ocean waves.",
    "sentence_cn": "小木筏完全任凭大海波涛的摆布。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>at the mercy of ...</b> 表示“完全受……支配、任凭……摆布、在……掌骨之中”。mercy 意为仁慈、恩惠。<br>例：Farmers were often at the mercy of the weather.",
    "tags": [
      "优美表达",
      "高阶短语"
    ]
  },
  {
    "id": "p09",
    "phrase": "for the sake ___ human peace",
    "sentence": "Let's put aside our personal rivalries for the sake ___ unity.",
    "sentence_cn": "为了团结，让我们搁置个人恩怨吧。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 1,
    "explanation": "【用法解析】<b>for the sake of ...</b> 表示“为了……的缘故/利益”。<br>口语常见：<i>For heaven's sake!</i>（看在老天的份上！）。",
    "tags": [
      "高频核心"
    ]
  },
  {
    "id": "p10",
    "phrase": "on the verge ___ breaking down",
    "sentence": "She was on the verge ___ tears when she heard the tragic news.",
    "sentence_cn": "听到这个悲惨的消息时，她几乎快要掉下眼泪来。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>on the verge of (doing) sth</b> 表示“濒临、正要、即将……”。verge 原意指边缘。<br>【同义替换】<b>on the brink of</b>、<b>on the edge of</b>。",
    "tags": [
      "高频短语",
      "写作亮点"
    ]
  },
  {
    "id": "c01",
    "phrase": "die ___ lung cancer",
    "sentence": "The old smoker sadly died ___ respiratory failure.",
    "sentence_cn": "这位老烟民令人难过地死于呼吸衰竭。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【经典易混辨析】<br>1. <b>die of</b>：多死于疾病、衰老、饥寒等<b>内部生理原因</b>（如 die of cancer, die of old age, die of hunger）。<br>2. <b>die from</b>：多死于事故、创伤、污染、过度劳累等<b>外部原因</b>（如 die from an accident, die from overwork, die from a car crash）。",
    "tags": [
      "经典易错",
      "必考辨析"
    ]
  },
  {
    "id": "c02",
    "phrase": "arrive ___ Tokyo International Airport",
    "sentence": "The plane is scheduled to arrive ___ the terminal at 8:00 PM.",
    "sentence_cn": "飞机预定于晚上8点到达航站楼。",
    "answer": "at",
    "acceptable": [
      "at"
    ],
    "category": "易混辨析",
    "difficulty": 1,
    "explanation": "【arrive 介词搭配】<br>1. <b>arrive at</b>：到达小地点（如机场 airport、车站 station、村庄 village、学校 school）。<br>2. <b>arrive in</b>：到达大地点（如国家 country、大城市 city、大省份 province）。<br>这里的 terminal/airport 是具体小地点，所以用 <b>at</b>。",
    "tags": [
      "基础常考"
    ]
  },
  {
    "id": "c03",
    "phrase": "be familiar ___ local customs",
    "sentence": "As an experienced tourist guide, she is very familiar ___ local history.",
    "sentence_cn": "作为一名经验丰富的导游，她对当地历史非常熟悉。",
    "answer": "with",
    "acceptable": [
      "with"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【主客体辨析口诀】<br>1. <b>人 + be familiar with + 物</b>：某人熟悉某物。<br>2. <b>物 + be familiar to + 人</b>：某物对某人来说是熟悉的。<br>本句主语是人（she），所以用 <b>familiar with</b>。反之：<i>This song is familiar to all of us.</i>",
    "tags": [
      "必考辨析",
      "口诀记忆"
    ]
  },
  {
    "id": "c04",
    "phrase": "compare childhood ___ a blossoming spring",
    "sentence": "Shakespeare frequently compared the world ___ a grand stage.",
    "sentence_cn": "莎士比亚经常把世界比作一个大舞台。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【compare 辨析】<br>1. <b>compare A to B</b>：把 A 比作 B（打比方、比喻）；有时也可表示相比。<br>2. <b>compare A with B</b>：把 A 和 B 相对比（横向比较异同优劣）。<br>本句是将世界“比拟作”舞台，是修辞比喻，固定搭配 <b>compare ... to ...</b>。",
    "tags": [
      "修辞考点",
      "常考搭配"
    ]
  },
  {
    "id": "c05",
    "phrase": "agree ___ the terms of the proposal",
    "sentence": "Both parties finally agreed ___ the draft agreement after hours of talk.",
    "sentence_cn": "经过数小时的会谈，双方最终就协议草案达成了一致。",
    "answer": "on",
    "acceptable": [
      "on",
      "upon",
      "to"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【agree 家族大盘点】<br>1. <b>agree on / upon</b>：多方“就某议题/条款达成共识”（如 agree on the price / terms）。<br>2. <b>agree to</b>：单方“同意某项提议、计划或安排”（如 agree to the plan / proposal）。<br>3. <b>agree with sb</b>：同意某人的看法，或气候/食物适宜某人。<br>本句中两者协商达成一致，用 <b>on</b> 或 <b>to</b> 均可接收！",
    "tags": [
      "辨析全解"
    ]
  },
  {
    "id": "c06",
    "phrase": "be angry ___ his unreasonable behavior",
    "sentence": "The teacher was furious and angry ___ what the boy had done.",
    "sentence_cn": "老师对男孩所做的事情感到非常愤怒。",
    "answer": "at",
    "acceptable": [
      "at",
      "about"
    ],
    "category": "易混辨析",
    "difficulty": 1,
    "explanation": "【angry 介词辨析】<br>1. <b>be angry at / about sth</b>：因某事、因某人的行为言论而生气。<br>2. <b>be angry with sb</b>：生某人的气（对人生气用 with）。<br>本句是对所做的事生气，因此选用 <b>at</b> 或 <b>about</b>。",
    "tags": [
      "高频辨析"
    ]
  },
  {
    "id": "c07",
    "phrase": "hear ___ an old schoolmate through email",
    "sentence": "I haven't heard ___ my college roommate for more than two years.",
    "sentence_cn": "我已经两年多没有收到大学室友的来信或消息了。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【hear 介词辨析】<br>1. <b>hear from sb</b>：收到某人的来信、电话或消息（收到联络）。<br>2. <b>hear of / about sb/sth</b>：听说、知悉有关某人某事的消息（知道存在）。<br>本句表示双方保持联络通讯，故用 <b>from</b>。",
    "tags": [
      "经典辨析"
    ]
  },
  {
    "id": "c08",
    "phrase": "consist ___ continuous self-discipline",
    "sentence": "True happiness consists ___ being content with what one has.",
    "sentence_cn": "真正的幸福在于对自己所拥有的一切感到知足。",
    "answer": "in",
    "acceptable": [
      "in"
    ],
    "category": "易混辨析",
    "difficulty": 3,
    "explanation": "【consist 难点辨析】<br>1. <b>consist of</b>：由……构成（强调组成要素，如 A car consists of parts）。<br>2. <b>consist in</b>：在于、存在于（强调核心本质，相当于 lie in，如 Happiness consists in peace of mind）。<br>本句强调“幸福的本质在于知足”，故精准介词为 <b>in</b>！",
    "tags": [
      "高阶陷阱",
      "深度辨析"
    ]
  },
  {
    "id": "c09",
    "phrase": "care ___ the feelings of others",
    "sentence": "A good leader always cares deeply ___ the wellbeing of employees.",
    "sentence_cn": "一个优秀的领导者总是深切关心员工的福祉。",
    "answer": "about",
    "acceptable": [
      "about"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【care 辨析】<br>1. <b>care about</b>：在乎、关切、放在心上。<br>2. <b>care for</b>：照料/照顾（= take care of）；喜欢/想吃（多用于否定与疑问，如 <i>Would you care for some coffee?</i>）。<br>本句表示关切、在乎，故搭配 <b>about</b>。",
    "tags": [
      "高频辨析"
    ]
  },
  {
    "id": "c10",
    "phrase": "charge the suspect ___ armed robbery",
    "sentence": "The court officially charged the former officer ___ corruption.",
    "sentence_cn": "法院正式指控这名前官员犯有贪腐罪。",
    "answer": "with",
    "acceptable": [
      "with"
    ],
    "category": "易混辨析",
    "difficulty": 2,
    "explanation": "【指控搭配对比】<br><b>charge sb with (crime)</b>：以某罪名指控某人。<br>对比 <b>accuse sb of (crime)</b>：指控某人犯某罪。<br>口诀：<b>charge 搭配 with，accuse 搭配 of</b>！必背考点！",
    "tags": [
      "法庭词汇",
      "必考辨析"
    ]
  },
  {
    "id": "v26",
    "phrase": "appeal ___ the younger generation",
    "sentence": "The short-form video app appeals strongly ___ teenagers and young adults.",
    "sentence_cn": "这款短视频应用对青少年和年轻群体极具吸引力。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>appeal to sb</b> 表示“吸引某人；向某人呼吁/求助”。<br>【同类表达】<i>attract sb</i>（及物动词）、<i>call on sb</i>（呼吁）。",
    "tags": [
      "高频词汇"
    ]
  },
  {
    "id": "v27",
    "phrase": "resort ___ violent measures",
    "sentence": "We should settle our disputes through dialogue rather than resort ___ violence.",
    "sentence_cn": "我们应该通过对话解决争端，而不是诉诸暴力。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>resort to sth / doing sth</b> 表示“诉诸于、采取（通常指不得已或极端的手段）”。其中的 <b>to 是介词</b>。<br>例：<i>as a last resort</i>（作为最后的万不得已手段）。",
    "tags": [
      "常考动词"
    ]
  },
  {
    "id": "v28",
    "phrase": "yield ___ intense pressure",
    "sentence": "The courageous hero refused to yield ___ enemy threats.",
    "sentence_cn": "这位勇敢的英雄拒绝向敌人的威胁屈服。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>yield to sb/sth</b> 表示“向……屈服、让步”。<br>【同义替换】<b>give in to</b>、<b>succumb to</b>、<b>surrender to</b>。均搭配介词 <b>to</b>！",
    "tags": [
      "阅读核心"
    ]
  },
  {
    "id": "v29",
    "phrase": "abstain ___ alcohol during pregnancy",
    "sentence": "Doctors strictly advise expectant mothers to abstain ___ smoking and drinking.",
    "sentence_cn": "医生严格建议准妈妈戒除烟酒。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "动词搭配",
    "difficulty": 3,
    "explanation": "【用法解析】<b>abstain from sth / doing sth</b> 表示“戒除、放弃、弃权”。介词 <b>from</b> 表达远离。<br>【同类短语】<b>refrain from doing</b>（克制、忍住不做某事）。",
    "tags": [
      "高级动词",
      "常考介词"
    ]
  },
  {
    "id": "v30",
    "phrase": "stem ___ cultural traditions",
    "sentence": "Many contemporary festival rituals stem ___ ancient harvest celebrations.",
    "sentence_cn": "许多现代节日习俗都源自于古代的丰收庆典。",
    "answer": "from",
    "acceptable": [
      "from"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>stem from ...</b> 表示“起源于、发源于、由……造成”。<br>【同类替换】<b>originate from / in</b>、<b>derive from</b>、<b>spring from</b>。",
    "tags": [
      "学术高频",
      "因果关系"
    ]
  },
  {
    "id": "a16",
    "phrase": "be eligible ___ a full scholarship",
    "sentence": "Only students with outstanding academic records are eligible ___ this award.",
    "sentence_cn": "只有学业成绩优异的学生才有资格获得这项奖励。",
    "answer": "for",
    "acceptable": [
      "for"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>be eligible for sth</b> 表示“有资格获得/享受某物”。若接动词可用 <i>be eligible to do sth</i>。<br>例：<i>eligible for a discount</i>（有资格享受折扣）。",
    "tags": [
      "实用英语",
      "常考形容词"
    ]
  },
  {
    "id": "a17",
    "phrase": "be generous ___ financial donations",
    "sentence": "The wealthy philanthropist was always generous ___ the underprivileged.",
    "sentence_cn": "这位富有的慈善家对弱势群体总是十分慷慨大方。",
    "answer": "to",
    "acceptable": [
      "to",
      "with"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<br>1. <b>be generous to sb</b>：对某人很慷慨大方（本句指对弱势群体，用 to）。<br>2. <b>be generous with sth</b>：在某物（钱财、时间、赞美）上出手阔绰/不吝啬。<br>两个介词都属纯正用法！",
    "tags": [
      "高频形容词"
    ]
  },
  {
    "id": "a18",
    "phrase": "be guilty ___ patent infringement",
    "sentence": "The jury found the company guilty ___ copyright violation.",
    "sentence_cn": "陪审团裁定该企业犯有侵犯版权罪。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "形容词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>be guilty of sth</b> 表示“犯有某罪行、对某错事内疚”。<br>反义词：<b>be innocent of sth</b>（无某罪的、清白的，同样搭配 of！）。",
    "tags": [
      "司法英语",
      "常考核心"
    ]
  },
  {
    "id": "p11",
    "phrase": "out ___ the question",
    "sentence": "Traveling abroad during the stormy season is completely out ___ the question.",
    "sentence_cn": "在暴风雨季节出国旅行是完全不可能的。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "易混辨析",
    "difficulty": 3,
    "explanation": "【绝杀易混对比】<br>1. <b>out of the question</b>（有 the）：不可能的（= impossible）。<br>2. <b>out of question</b>（无 the）：毫无疑问的（= beyond doubt / undoubtedly）。<br>口诀：<b>有 the 是不可能，没 the 是毫无疑问</b>！",
    "tags": [
      "经典陷阱",
      "高频辨析"
    ]
  },
  {
    "id": "p12",
    "phrase": "in light ___ recent developments",
    "sentence": "We had to revise our original project plan in light ___ recent developments.",
    "sentence_cn": "鉴于最近的事态发展，我们不得不修改最初的项目计划。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>in light of ...</b> 表示“鉴于、考虑到、根据”。这里的 light 引申为“照射明晰、启示”。<br>【同义替换】<i>in view of</i>、<i>taking into consideration</i>。",
    "tags": [
      "高阶写作"
    ]
  },
  {
    "id": "p13",
    "phrase": "by accident rather than ___ purpose",
    "sentence": "Did you spill the glass of water by accident or ___ purpose?",
    "sentence_cn": "你是无意打翻水杯的，还是故意的？",
    "answer": "on",
    "acceptable": [
      "on"
    ],
    "category": "介词短语",
    "difficulty": 1,
    "explanation": "【对比短语】<br>1. <b>on purpose</b>：故意地、特意地（= deliberately）。<br>2. <b>by accident / by chance</b>：偶然地、意外地（= accidentally）。<br>两者常作为反义词成对出现！",
    "tags": [
      "高频短语",
      "基础重点"
    ]
  },
  {
    "id": "v31",
    "phrase": "subscribe ___ the monthly magazine",
    "sentence": "She has decided to subscribe ___ the online science journal.",
    "sentence_cn": "她决定订阅该在线科学期刊。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "动词搭配",
    "difficulty": 1,
    "explanation": "【用法解析】<b>subscribe to sth</b> 表示“订阅（杂志/频道/服务）；赞同（某种观点或信念）”。<br>例：<i>I don't subscribe to that theory.</i>（我并不赞同那个理论）。",
    "tags": [
      "互联网高频",
      "常考动词"
    ]
  },
  {
    "id": "v32",
    "phrase": "rejoice ___ the glorious victory",
    "sentence": "The whole country rejoiced ___ the news of peace.",
    "sentence_cn": "举国为和平的好消息而欣喜若狂。",
    "answer": "at",
    "acceptable": [
      "at",
      "in",
      "over"
    ],
    "category": "动词搭配",
    "difficulty": 2,
    "explanation": "【用法解析】<b>rejoice at / in / over sth</b> 表示“为……感到欢欣鼓舞、狂喜”。<br>介词 <b>at</b> 最为常见，表达对某个喜讯的直接情绪反应（如同 surprise at, delighted at）。",
    "tags": [
      "高级动词"
    ]
  },
  {
    "id": "a19",
    "phrase": "be worthy ___ high praise",
    "sentence": "His selfless devotion to charity work is worthy ___ everyone's respect.",
    "sentence_cn": "他对于慈善事业的无私奉献值得所有人尊敬。",
    "answer": "of",
    "acceptable": [
      "of"
    ],
    "category": "形容词搭配",
    "difficulty": 2,
    "explanation": "【worth / worthy 句型大辨析】<br>1. <b>be worthy of + 名词/being done</b>：值得……（介词用 of！）。<br>2. <b>be worthy to be done</b>：接不定式被动。<br>3. <b>be worth + 名词/doing</b>：值得（worth是介词，直接接名词或主动表被动的动名词doing）。",
    "tags": [
      "必考辨析",
      "常考句型"
    ]
  },
  {
    "id": "p14",
    "phrase": "in proportion ___ its actual size",
    "sentence": "The punishment should always be in proportion ___ the severity of the crime.",
    "sentence_cn": "惩罚应当与罪行的严重程度成比例。",
    "answer": "to",
    "acceptable": [
      "to"
    ],
    "category": "介词短语",
    "difficulty": 2,
    "explanation": "【用法解析】<b>in proportion to ...</b> 表示“与……成比例、与……相称”。<br>反义表达：<b>out of proportion to ...</b>（与……不成比例）。",
    "tags": [
      "学术高阶",
      "写作亮点"
    ]
  },
  {
    "id": "v33",
    "phrase": "thrive ___ competitive challenges",
    "sentence": "Some creative individuals truly thrive ___ stressful deadlines.",
    "sentence_cn": "某些富有创造力的人在充满压力的截止日期下反而表现得特别出色。",
    "answer": "on",
    "acceptable": [
      "on"
    ],
    "category": "动词搭配",
    "difficulty": 3,
    "explanation": "【用法解析】<b>thrive on sth</b> 表示“以……为动力茁壮成长、在……中越干越起劲”。原意为蓬勃繁荣，这里 <b>on</b> 表示赖以生长的养分基石。",
    "tags": [
      "地道表达",
      "高阶词汇"
    ]
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = { PREPOSITION_QUESTIONS };
}
