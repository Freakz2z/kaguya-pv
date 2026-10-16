# 星降る海 · 动画代码与制作记录

一部以《超かぐや姫！》为题材的二维手书同人 PV 的源码整理。最终工程长 **62.2 秒**，画布 **1920×1080 / 30 fps**，使用 HyperFrames、GSAP、Canvas 和 Python 构建。

**当前状态：项目创作结束，本仓库仅在本地准备，尚未创建 GitHub 远端或公开发布。**

这份仓库公开候选版保留时间线、动态排版、鼓点脉冲、音符轨迹、转场和构建脚本。默认演示使用几何占位图、静音音轨、示例字幕和系统字体，不能代表完整成片的美术效果。人物画稿、原曲、官方图像、封面和录屏不随候选仓库分发。用户提供的烟花模板未附带许可证，演示已换用独立实现。完整原工程仍单独保留。

## 快速开始

需要 Node.js 22+；HyperFrames 检查和预览还需要 FFmpeg 与可用浏览器。

```sh
npm ci
npm run audit:repo
npm run dev
```

`npm ci` 的安装钩子会生成占位图、240 秒静音 WAV，并从锁定的 npm 依赖复制 GSAP。上述资源均在 Git 忽略目录中。原时间线使用的音乐源偏移从 169.1 秒开始，因此静音文件也覆盖该区间。首次预览会通过 npx 获取固定版本的 HyperFrames 0.8.162。

代理需要持久预览时使用 `npx --yes hyperframes@0.8.162 preview --background`。前台预览由人操作即可。这个项目整理阶段不需要渲染 MP4。

## 修改与重建

可直接编辑 `index.html` 或 `compositions/`，也可在 HyperFrames Studio 修改。当前 HTML 是最终时间线的可编辑快照；`source/` 保留生成这些镜头所需的 Python/JavaScript 依赖，不包含早期废弃实验。

```sh
python3 -m venv .venv
# Windows 使用 .venv\Scripts\activate
source .venv/bin/activate
python -m pip install -r source/requirements-build.txt
npm run build
npm run check
```

构建会检查 `source/generated-files.json`，检测到尚未同步的 Studio/HTML 修改时拒绝覆盖。先提交并把改动同步回构建脚本；只有确认同步完成后，才手动使用 `python source/build.py --overwrite-edited`。日语字体使用系统回退，外观会随系统变化；中文书法字体的 OFL 许可随仓库保存。

## 本地还原完整版本

你持有本项目最终原工程时，可把它导入一个独立、被 Git 忽略的预览目录：

```sh
python3 scripts/import_private.py ../path-to-original-project
npm run dev:private
```

导入器首先核验原 HTML 快照的 SHA-256，再复制该时间线真正引用的素材。它不会下载音乐，不会改写公开候选版源码，也不会覆盖已有私有预览。完整版本的音乐、译文、角色图、官方标志和字体仍遵循各自权利条件。

## 目录

| 路径 | 用途 |
| --- | --- |
| `index.html` | 62.2 秒主时间线、音轨与镜头挂载 |
| `compositions/` | 逐镜 HTML、中文示例字幕、全片转场 |
| `source/` | 最终构建所需的镜头、轨迹、文字和鼓点代码 |
| `config/` | 素材尺寸/摘要及私有还原快照清单 |
| `scripts/` | 安装、资源审计、私有还原工具 |
| `docs/` | 架构、素材边界、归档与检查记录 |
| `LICENSES/` | 第三方许可证副本 |

## 制作与参考

制作：Freakz2z。AI 参与创意整理、画稿生成与修订、动画代码和动态排版，使用 Codex 与 ImageGen。技术栈为 HyperFrames、GSAP、Canvas、Python；原制作流程使用 FFmpeg。

音乐信息：Aqu3ra／月見ヤチヨ（cv.早見沙織）—《星降る海》。[官方 MV](https://www.youtube.com/watch?v=h5XQqKuek5A)。演出参考：[【超时空辉夜姬/手书】へんしん!](https://www.bilibili.com/video/BV1nYZ3BCEHL/)。本项目为非官方同人创作。

项目自有代码使用 MIT；第三方部分按自身许可执行，详见 [NOTICE](NOTICE.md) 与 [素材边界](docs/ASSETS.md)。这些许可不授予角色、音乐、歌词、商标或官方画面的权利。

后续发布前参阅 [发布检查](docs/RELEASE.md)；具体已完成的验证与限制记录在 [检查记录](docs/VALIDATION.md)。
