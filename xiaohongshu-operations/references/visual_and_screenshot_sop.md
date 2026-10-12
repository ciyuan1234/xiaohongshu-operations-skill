# 小红书真实视觉与原生截图 SOP (Visual & Screenshot SOP)

> 核心教训：读者极度反感花哨的合成卡片与 AI 渲染图。用户曾因合成卡片被讽刺而直接删除笔记。只有真机原生截图与官方仓库截图才能带来真实的信任。

---

## 一、视觉红线与负面清单 (Strict Negative Rules)

1. **绝对禁止 AI 生成图**：不要使用 Midjourney、Flux 或 Stable Diffusion 绘制的概念插图。在科技工具领域，AI 图意味着内容虚假、没有实际测试。
2. **绝对禁止合成 HTML/CSS 假卡片**：
   - 带有仿 macOS 交通灯红黄绿圆点的假窗口；
   - 带有花哨渐变紫/深蓝背景的 Bento Grid 排版；
   - 带有大号标题框、警示感叹号图标和右上角角标（`1/4`）的营销外壳。
3. **禁止在终端截图中注入假注释**：
   - 严禁在 `ls` 或 `du` 等系统命令输出后人为拼接 `# 这是自动快照` 等人工注释，读者一眼就能识破伪造。
4. **禁止使用模糊放大的低清图**：必须保证Retina屏幕下的清晰度与真实字体子像素渲染效果。

---

## 二、三类合法且高信任的配图来源 (Legitimate Sources)

1. **官方 GitHub 仓库与产品 Landing Page**：
   - 包含 Star 数、Release Notes、真实架构图或官方对比 Slider 的截屏。
   - 能够直接传递开源公信力。
2. **真机原生屏幕捕获 (Native OS Screen Captures)**：
   - macOS 终端真实窗口（Ghostty、iTerm2、Terminal）。
   - 真实开发环境（Cursor、VS Code、Xcode、NeoVim）。
   - 真实的系统监控工具（Activity Monitor、`htop`、Disk Space Analyzer）。
3. **真实社区测评与用户报错现场**：
   - 真实的 Traceback 堆栈报错信息。
   - 社区 Issue 讨论或真实配置对比。

---

## 三、原生 3:4 比例裁剪与清晰度标准

小红书移动端最优画幅比例为 **3:4**，标准分辨率为 **1080 × 1440** 或 **1200 × 1600**。

### 1. macOS 命令行直接捕获与裁剪流程
```bash
# 1. 窗口截取原生高清图
screencapture -x -w /tmp/raw_window.png

# 2. 居中裁切至 3:4 (高度优先)
sips -c 1600 1200 /tmp/raw_window.png --out /tmp/cropped.png

# 3. 缩放到标准 1080x1440
sips -z 1440 1080 /tmp/cropped.png --out ./assets/cover_01.png
```

或者使用本项目提供的自动化脚本：
```bash
python3 scripts/crop_tool.py --input /tmp/raw_window.png --output ./assets/cover_01.png
```

### 2. 视觉排版细节检查清单
- [ ] 窗口是否包含真实的窗口边框、系统字体和原生阴影？
- [ ] 截图中是否有真实的路径或版本标识（如 `v1.4.2`、`~/projects/`）？
- [ ] 图片主体是否占据画面 80% 以上面积，避免无效留白？
- [ ] 没有任何人工添加的营销箭头、红圈或花哨贴纸？
