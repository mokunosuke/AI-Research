# LoRA調査レポート — 2026-11-03

調査日: 2026-11-03（JST）  
比較対象: `Reports/2026-10-31_LoRA_Report.md`  
対象: 複数キャラクターの混線・一貫性、ComfyUI/Forge、RTX 3060 12GB

## 今週の重要トピック

- **新しいSDXL混線防止策は確認できませんでした。** 前回のRS MultiCharacter Sampler、少数画像の一貫性実験、Forge NeoのKrea向け機能を上回る、今週公開の一次資料・3060実測は見つかりませんでした。
- **地域別プロンプトの新しい実例はAnima向けです。** LuCiD VRPはComfyUIの視覚編集UIとAnima地域別プロンプトを組み合わせますが、SDXLのLoRA混線を解決する証拠ではありません。[GitHub](https://github.com/EBEBEEBE/comfyui-lucid-vrp)
- **今回の運用上の結論:** 既存のSDXLワークフローは前回の推奨どおり二人・二領域から固定seedで評価し、モデル系列を跨ぐ機能の流用は避けます。

## 混線防止関連アップデート

### 新規情報 — LuCiD VRP（適用範囲はAnima等）

X投稿ではAnima向けワークフローでキャラクター配置を試した例が示されました。GitHubの説明は、画像編集・レイヤー操作・Anima地域別プロンプト・MOSS-Imageレイアウト指示をまとめるComfyUI用インターフェースです。[プロジェクトREADME](https://github.com/EBEBEEBE/comfyui-lucid-vrp)

**前回との差分:** 地域編集を支援する別モデル系列のUI実例が加わりました。SDXL LoRAを人物ごとに分離する機能、Forge対応、RTX 3060 12GB実測は確認できていません。前回のRS MultiCharacter Samplerを置き換える根拠はありません。

### 更新情報 — 既存手法の評価を維持

- RS MultiCharacter Samplerは前回レポートの主要なSDXL候補です。今週、独立したベンチマークや新しい制限解除を確認できませんでした。[GitHub](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)
- `character-consistency-lora`は単一キャラクターの小規模評価であり、多人数間の混線テストとは異なります。結果を一般化しない前回の扱いを維持します。[実験結果](https://github.com/Colin-J-Emmanuel/character-consistency-lora/blob/main/RESULTS.md)
- Krea Multi-LoRAはForge Neo上のKrea 2/Klein向けで、SDXL/通常Forgeの対応を示すものではありません。[GitHub](https://github.com/Adeliox/krea-multi-lora)

## ComfyUI関連

今週、SDXL/Illustriousに対する新規の混線対策ノード・学習手法を裏付ける一次資料は確認できませんでした。LuCiD VRPはComfyUI連携の新しい制作補助候補ですが、対応モデル・導入条件・3060での負荷をREADMEで確認してから、Anima/MOSS用途として別枠で評価してください。

## Flux関連

今週、Fluxのキャラクター分離・一貫性に関する再現可能な新情報は確認できませんでした。前回同様、SDXLの地域LoRA設定をFluxへ流用しない方針です。

## 実運用で使える手法

### 1. RS MultiCharacter Sampler（継続）

- **概要:** 領域ごとにプロンプトとLoRAを設定するComfyUI拡張。SDXL/Illustriousのワークフロー例があります。
- **効果:** キャラクター別の空間条件を分け、属性の混線を抑える方向に使えます。完全な分離を保証しません。
- **RTX3060 12GB:** 専用実測は未確認。二人・低解像度から試し、人物数やDetailerを段階的に増やします。
- **ComfyUI実装難易度:** 中。対応版・ワークフローに合わせた導入が必要。
- **Forge実装難易度:** 高／対応確認なし。Forge標準機能として使える根拠はありません。
- **注意点:** マスク境界、交差する小物、ポーズやモデル差による混線が残ります。

### 2. LuCiD VRP（新規、Anima系）

- **概要:** レイヤー編集、地域プロンプト、MOSS-Imageレイアウト指示を扱うComfyUI用UI。[GitHub](https://github.com/EBEBEEBE/comfyui-lucid-vrp)
- **効果:** 投稿者はAnimaでキャラクター配置を示しています。SDXL LoRAの混線抑制効果は未検証。
- **RTX3060 12GB:** VRAM・速度の実測なし。必要なモデルと拡張を確認し、小さな入力から試す必要があります。
- **ComfyUI実装難易度:** 中（READMEの依存関係・対象ワークフロー次第）。
- **Forge実装難易度:** 対応情報なし。現時点では適用対象にしません。
- **注意点:** モデル系列専用機能をSDXL/Forge機能と混同しないこと。

## RTX3060 12GB評価

| 項目 | 今週の評価 |
|---|---|
| VRAM | 新規手法の3060実測はなし。既存SDXL手法は二人・小さな解像度から検証。 |
| 推奨設定 | 前回どおりseed・モデル・解像度を固定し、通常構成と地域分割を比較。 |
| 実行速度 | LuCiD VRP、RS samplerの今週の比較値なし。人物別予測やDetailerは負荷増の可能性があるが倍率は未測定。 |
| 安定性 | 独立再現情報なし。まず短いテストでワークフローを確認。 |
| ComfyUI | RS samplerは既知候補。LuCiD VRPはAnima用途の追加候補。 |
| Forge | SDXLの新しい人物別LoRA機能は確認できず。Krea Neo例の対象範囲を維持。 |

## 次週監視項目

- RS MultiCharacter Samplerの更新、SDXL対応表、第三者による3060評価
- LuCiD VRPの対応モデル、導入要件、地域編集の再現例
- SDXL/Illustrious向けの独立した混線評価データと学習手法
- Forge通常版・NeoのSDXL人物別LoRA対応
- Fluxの地域分離・キャラクター一貫性に関する公開実装

## 情報源

- [RS MultiCharacter Sampler](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)
- [Character Consistency LoRA実験](https://github.com/Colin-J-Emmanuel/character-consistency-lora)
- [Forge Neo Krea Multi-LoRA](https://github.com/Adeliox/krea-multi-lora)
- [LuCiD VRP GitHub](https://github.com/EBEBEEBE/comfyui-lucid-vrp)
- [2026-10-31 LoRAレポート（比較基準）](2026-10-31_LoRA_Report.md)
