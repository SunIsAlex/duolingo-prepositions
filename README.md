# 🦉 多邻国介词语法填空 | Duolingo Prepositions

一个自用的英语介词搭配语法填空 Web 应用，无需登录，即开即练。包含详细语法逻辑解析、易混辨析，并深度复刻多邻国（Duolingo）经典的反馈音效与动效。

![Duolingo Prepositions](https://img.shields.io/badge/Duolingo-Prepositions-58cc02?style=for-the-badge&logo=duolingo&logoColor=white)
![EdgeOne](https://img.shields.io/badge/Deployed%20on-EdgeOne%20Pages-0052d9?style=for-the-badge&logo=tencent-cloud&logoColor=white)

---

## ✨ 核心特性

- **🎧 100% 原版音效还原**：直接从本机正版 Duolingo APK 逆向提取：
  - 答对提示音：`right_answer.mp3`（经典欢快双音提示音）
  - 答错提示音：`wrong_answer.mp3`（低音 Buzz 警示音）
  - 5/10 连击音效：`streak_5.mp3`（闪电连击音效）
  - 关卡结算与欢呼：`da_ding.mp3` + `applause.mp3`
  - 按钮点击触感：`tap.mp3`
- **🦉 官方矢量 Lottie 动效**：
  - 多多鸟欢呼 / 跳跃庆祝（`duo_cheer.json`、`duo_hop.json`）
  - 答错委屈哭泣神态（`duo_sad.json`）
  - 顶部燃烧连击火焰（`flame.json`）
  - 单元通关五彩纸屑彩带粒子（`confetti`）
- **📚 76+ 高频介词搭配精选库**：
  - **动词 + 介词**：如 `dance to music`、`listen to`、`look forward to`、`depend on`、`insist on`、`prevent from` 等
  - **形容词 + 介词**：如 `accustomed to`、`proud of`、`capable of`、`immune to`、`keen on` 等
  - **易混淆专区**：如 `dance to` vs `dance with`、`die of` vs `die from`、`familiar to` vs `familiar with`、`charge with` vs `accuse of` 等
  - **介词短语**：如 `at the expense of`、`in terms of`、`on behalf of`、`in spite of` 等
- **💡 深度解析与避坑指南**：不仅给出正确答案，还剖析“为什么用这个介词”、中式英语常见误区及同类拓展。
- **⚡ 极速键盘盲打交互**：
  - 输入答案后按 **`Enter`** 立即提交检查；
  - 面板滑出后按 **`Enter`** 或 **`Space`** 瞬间切换至下一题；
  - 也可直接点击下方常用介词词块（Tiles）进行选择；
  - 原生英语语音合成朗读（Web Speech API）。
- **💾 双重学习进度存储**：
  - 浏览器 `localStorage` 离线毫秒级存储；
  - 服务端 `data/progress.json` 自动防抖异步保存；
  - 支持查看学习成就看板（统计总刷题量、正确率、掌握题数），并提供 **一键导出 / 导入 JSON 备份**。
- **➕ 自选题库支持**：随时点击 ➕ 添加自己在阅读中遇到的专属介词题目。

---

## 🚀 本地运行

无需安装重量级框架，纯标准库支持：

```bash
# 启动本地开发服务 (默认端口 8080)
./start.sh
# 或
python3 server.py
```

- 本地访问：[http://localhost:8080](http://localhost:8080)
- 局域网/手机访问：`http://<局域网IP>:8080`

---

## 🌐 部署到 EdgeOne Pages

项目通过腾讯云 EdgeOne CLI 构建并全球边缘加速分发：

```bash
edgeone pages deploy public --name duolingo-prepositions
```

---

## 📂 项目结构

```
.
├── public/                 # 静态前端资源 (EdgeOne Pages 部署目录)
│   ├── index.html          # 主界面
│   ├── css/style.css       # 多邻国 3D 拟物与弹簧抽屉动效样式
│   ├── js/
│   │   ├── app.js          # 核心交互与打卡、错题、存储逻辑
│   │   ├── audio-manager.js# Web Audio API 0ms 低延迟音效播放与朗读
│   │   └── questions.js    # 76+ 精选介词题库及详尽语法解析
│   ├── libs/               # 离线打包的 Lottie 与 Confetti 引擎
│   └── assets/
│       ├── audio/          # Duolingo APK 提取的原版音频文件
│       └── anim/           # Duolingo APK 提取的矢量 Lottie JSON 动画
├── data/
│   └── progress.json       # 本地练习进度与掌握度数据
├── edgeone.json            # 腾讯云 EdgeOne Pages 配置
├── server.py               # 本地轻量级 HTTP 服务及进度同步 API
├── start.sh / stop.sh      # 启停脚本
└── README.md
```
