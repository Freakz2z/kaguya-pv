# 源码发布说明

作者于 2026-10-21 授权将整理后的源码仓库公开至 `Freakz2z/kaguya-pv`。2026-10-16 是本地归档日期，不是 GitHub 发布日期。`package.json` 的 `private: true` 用于防止误发 npm，不影响 GitHub 仓库公开。

仓库使用全新历史，只包含整理后的源文件。原项目的提交、素材与交付物继续保留在原归档中，不重写原仓库历史。

发布与后续更新时：

1. 重新检查 `git status` 与 `npm run audit:repo`，确保 `.private-preview`、音乐、官方图片、导出物和本机路径没有进入跟踪列表。
2. 阅读 `NOTICE.md`，确认代码、第三方组件和素材的许可边界；仓库默认提供的是演示源码。
3. 从全新克隆执行 `npm ci`、构建和 HyperFrames 检查，审看效果；机器检查不等于音乐或美术验收。
4. 只推送独立源码仓库；不要把原 CPK 历史、私有预览或交付目录加入远端。

项目不附带原作素材或成片。检查范围见 `VALIDATION.md`；最终公开状态以 GitHub 仓库和提交记录为准。

## 首次公开记录

- 日期：2026-10-21。
- 仓库：https://github.com/Freakz2z/kaguya-pv ，可见性已核实为 Public，默认分支为 `main`。
- 首个公开版本：`v1.0.0`，对应提交 `b1e90f397a9c0d40c6372fb9ec4a5287f3bc6be2`。
- 首轮 Source checks 已通过：[GitHub Actions 记录](https://github.com/Freakz2z/kaguya-pv/actions/runs/39623391547)。后续状态以 Actions 与 README 徽章为准。
- 本地原 CPK 工程及私有素材没有推送；候选仓库成为当前公开源码仓库。
