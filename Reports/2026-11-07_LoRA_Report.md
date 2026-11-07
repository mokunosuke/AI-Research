# LoRA調査レポート — 2026-11-07

調査日: 2026-11-07（JST）  
比較対象: `Reports/2026-11-03_LoRA_Report.md`、`Reports/2026-10-31_LoRA_Report.md`  
対象: SDXL LoRAの複数人物混線・一貫性、ComfyUI/Forge、RTX 3060 12GB

## 今週の重要トピック

- **新しいSDXL向けの混線防止手法や3060実測は確認できませんでした。** 前回の主軸であるRS MultiCharacter Samplerは更新されていますが、最近の更新はプロンプト補助や操作UIの改善で、SDXL人物LoRAの分離性能を新たに実証したものではありません。
- **前回レポートの更新漏れを補います。** RS MultiCharacter Sampler v1.1.2（10月31日）とv1.1.3（11月1日）は、前回の11月3日レポートに反映されていませんでした。前者はWorkspaceのワークフロー保存修正、後者はプロンプト補完です。新しい生成性能ではなく、操作・再現性の改善です。[リリース履歴](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler/releases)
- **地域プロンプトの実験的選択肢:** Conditioning Layersは塗れる影響領域とFIXED/BLENDED合成を提供しますが、公開alphaの確認済み対象はKrea 2で、SDXL・人物別LoRA対応ではありません。[GitHub](https://github.com/SurrealByDesign/conditioning-layers)

## 混線防止関連アップデート

### 更新情報 — RS MultiCharacter Sampler v1.1.x

前回レポートではRS samplerをSDXL/Illustriousの主要候補として扱いました。GitHubのリリース記録を照合すると、前回時点ですでに次の更新が公開されていました。

- **v1.1.2（10月31日）:** ComfyUI Workspaceのworkflow/widget設定保存でProxyオブジェクトを正しくJSON形式へ保存する修正。
- **v1.1.3（11月1日）:** Workspaceの入力欄にプロンプト補完を追加し、既知の補完拡張との連携と、タグ・wildcardファイルによる軽量オフライン候補を案内。

これらは生成エンジンやLoRA分離方法の新機能ではありません。前回の11月3日レポートに記載が抜けていた既公開更新として記録します。[v1.1.2 / v1.1.3 release notes](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler/releases)

現行READMEでは、SDXL/Illustrious二人用ワークフローと人物別LoRA設定が引き続き案内されています。領域指定は人物の完全分離を保証せず、交差する小物・密な配置では属性混線や人物の複製・欠落が起こり得ます。人物ごとの異なるLoRA組合せは予測計算を分けるモードがあり、速度と一時メモリのコストを伴います。[READMEと制限事項](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)

### 新規に確認した地域プロンプト拡張 — Conditioning Layers

2026-10-26公開のalpha.6は、ComfyUIのmasked conditioningを基礎に、ペイント可能なグレースケールInfluence Field、領域を排他的に割り当てるFIXED、重みを正規化して混ぜるBLENDED、Selective Blend Groupsを提供します。[alpha.6 release](https://github.com/SurrealByDesign/conditioning-layers/releases/tag/v0.1.0-alpha.6)

**差分と適用範囲:** 前回レポート後に見つけた追加候補ですが、公開READMEはKrea 2向けの実験的alpha、ComfyUI 0.34.6 / frontend 1.49.6を適格環境として示しています。SDXL、人物別LoRA制御、Forgeへの対応は確認できず、SDXL混線防止策として数えることはできません。新規公開の週次情報というより、前回レポートで未記録だった周辺技術です。

## ComfyUI関連

- **RS MultiCharacter Sampler:** SDXL/Illustrious向け人物別LoRA・領域指定を継続候補とします。Workspaceの保存修正と入力補完は使い勝手の更新で、生成性能の改善証拠ではありません。
- **Conditioning Layers:** 地域の形を細かく塗り、プロンプトの参加範囲と混ざり方を調整できます。ただし公開alphaの対象はKrea 2で、マスク境界・意味的漏れが残ると作者が明記しています。モデルデータは別途必要で、README記載のモデルファイル合計は約31.78 GB（ダウンロード値）です。これはVRAM使用量ではありません。
- 今週、Forge通常版またはForge NeoにおけるSDXLの人物別LoRA分離の新しい標準機能は確認できませんでした。

## Flux関連

今週、Flux向けキャラクター分離・一貫性維持について、RTX 3060で再現できる新規一次資料は確認できませんでした。RS samplerのFlux系パスがあってもモデル別制限があり、SDXLの設定をそのまま転用しないでください。

## 実運用で使える手法

### 1. RS MultiCharacter Sampler — SDXL/Illustrious（継続）

#### 概要
人物ごとのプロンプト・LoRA・位置やマスクを組み、共通シーン条件と分けて生成します。SDXL/Illustriousの二人用例を作者が公開しています。

#### 効果
人物の空間配置と特徴条件を分けることで、属性の混線を減らす方向に使えます。人物数、衣装、ポーズ、モデルの理解に依存し、完全分離は保証されません。

#### RTX3060 12GBでの実用性
専用の3060 VRAM・速度測定は見つかりません。二人・低めの解像度・固定seedから始め、標準LoRA構成との出力を比較します。人物ごとに異なるLoRA適用は追加予測計算になるため、単一LoRAより遅くなる可能性があります。

#### ComfyUI実装難易度
中。ComfyUI本体と拡張の対応版を確認し、同梱ワークフローのモデル系列を合わせます。v1.1.3のWorkspaceは実験的UIであり、通常のノードグラフでもワークフローを確認してください。

#### Forge実装難易度
高。通常Forgeでの互換性は未確認です。既報のKrea Multi-LoRAはForge Neo上のKrea 2/Klein向けで、SDXLに転用できる根拠がありません。

#### 注意点
人物位置・マスク、交差アイテム、局所Detailerによる変化を個別に評価し、prompt・seed・モデル・LoRA強度・ComfyUI版を保存します。

### 2. Conditioning Layers — Krea 2限定の地域プロンプト実験

#### 概要
ペイントしたInfluence Fieldでprompt conditioningの空間的な割当・ブレンドを指定します。LoRA個別適用機能とは別の仕組みです。

#### 効果
曲線や重なりを含む領域のプロンプト参加度を編集できます。領域が画素単位で厳密に守られる保証はなく、semantic leakageや継ぎ目が残ります。

#### RTX3060 12GBでの実用性
本拡張を3060で測定した資料はありません。サンプルのKrea 2 Turboモデル一式は約31.78 GBのダウンロード容量が記載され、VRAM/RAM条件とは別にディスク容量も必要です。

#### ComfyUI実装難易度
中〜高。alpha.6、適格ベースのComfyUI 0.34.6 / frontend 1.49.6、モデル3種を揃えます。新しいホストとの完全互換性はREADME上で未検証です。

#### Forge実装難易度
対象外。Forge用の実装は確認できません。

#### 注意点
SDXLや人物別LoRAの対策として評価せず、Krea 2でのprompt領域編集を試す場合に限ります。

## RTX3060 12GB評価

| 項目 | 今週の評価 |
|---|---|
| VRAM消費 | RS samplerの3060実測なし。Conditioning Layersも3060でのVRAM測定なし。モデルのファイルサイズをVRAM必要量と混同しない。 |
| 推奨設定 | SDXLのRS samplerは2人・低解像度・seed固定。Conditioning Layersは作者のKrea 2設定に限定して導入条件を照合。 |
| 実行速度 | RSの人物別LoRA経路は組合せごとの独立予測を使う場合、速度コストがある。具体的な倍率は不明。 |
| 安定性 | v1.1.2はWorkspaceの保存不具合を修正したが、v1.1.3のサードパーティ補完全構成は未検証。実行前に通常ノードグラフへ戻せる状態を維持。 |
| Forge | SDXLの新規対応情報なし。 |

## 次週監視項目

- RS samplerのSDXL/Illustrious版リリース、人物別LoRAの独立検証と3060実測
- RS WorkspaceでのSDXLワークフロー保存・復元の第三者確認
- Conditioning LayersのKrea 2以外への対応、実験alphaからの変更、地域漏れ評価
- Forge Neoまたは通常ForgeのSDXL人物別LoRA対応
- Flux向け地域LoRA制御の実用例とモデル別制約

## 情報源

- [RS MultiCharacter Sampler — GitHub](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)
- [RS MultiCharacter Sampler — Releases](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler/releases)
- [Conditioning Layers — GitHub](https://github.com/SurrealByDesign/conditioning-layers)
- [Conditioning Layers alpha.6 release](https://github.com/SurrealByDesign/conditioning-layers/releases/tag/v0.1.0-alpha.6)
- [2026-11-03 LoRAレポート（比較対象）](2026-11-03_LoRA_Report.md)
