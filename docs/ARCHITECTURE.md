# 结构与维护

主时间线通过 `data-composition-src` 挂载独立 HTML，按绝对帧 / 30 转为秒。内容、全片转场和字幕使用不同轨道与层叠上下文；图文允许按设计相互遮挡。各子镜头注册一个 paused GSAP timeline 到 `window.__timelines`，保证时间轴 seek 时能复现。

`source/build.py` 从开场五镜开始组装，再读取仍在使用的 `revision-*` 模块。这些数字是构建依赖名，不是可独立切换的发布版本。提取时只保留可达模块，避免把全部试作工程变成安装前提。

关键模块：

- `revision-v24/append.py`：烟花停顿与续段。
- `revision-v25/relay.py`、`journey.py`、`journey-trails.js`：声音接力与音符远行。
- `revision-v25/ending.py`：手势序列、三人舞台和音乐署名。
- `revision-v26/backgrounds.py`、`revision-v27/transitions.py`：背景动态及后段转场。
- `revision-v31/typography.py`、`pulses.py`：文字入场与鼓点缩放。
- `revision-v22/subtitles.py`：独立字幕的方位、入场、颜色及轻微脉冲。

公开候选版对原工程只做打包所需适配：系统字体回退、示例字幕、静音媒体、几何占位图和独立烟花演示。其余时间线、轨迹和文字动效保留。占位模式无法验收人物手势、美术一致性或音乐听感。

不要用 `requestAnimationFrame`、真实时钟或无种子的随机数决定渲染状态；Canvas 效果应由时间线采样。不要把局部 Studio 修改直接丢给构建覆盖。必要时先提交 HTML，再把修改同步到生成代码。
