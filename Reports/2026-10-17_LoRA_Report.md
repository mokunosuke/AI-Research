# LoRA Research Report — 2026-10-17

> 調査実施日: 2026-10-25（Asia/Tokyo）  
> 対象: 複数キャラクターLoRAの混線防止、領域条件付け、キャラクター一貫性。依頼されたファイル名を維持しています。したがって本稿は10月17日付レポートの体裁ですが、調査には10月17日以後に公開された情報も含みます。

## 今週の重要トピック

1. **ComfyUIでキャラクターごとのLoRAを領域単位で適用する実装が増加。** RS MultiCharacter Samplerは最大10領域、点・矩形・マスクによる配置、キャラクター別LoRA、ローカル詳細化をまとめています。Krea 2専用Composerや軽量なRegional Character LoRAノードも、LoRAの寄与を領域内へ制限する実装を公開しています。通常のLoRAをグローバルに重ねることで起きる顔・髪・服の混線を、プロンプトだけでなくモデル出力側の空間制御で抑える方向が主流です。
2. **10月21日公開の参照画像機能は実験扱い。** RS Samplerのリリースは複数モデル系統を対象にしていますが、作者自身が推奨せず、品質のばらつきや検証範囲の不足を明記しています。キャラクターLoRAの代替として本番導入する根拠はまだ弱く、LoRAが使えるならLoRAを優先します。
3. **モデル系統ごとの互換性が重要。** Krea 2向けRegional LoRAはKrea 2学習済みLoRAを要求し、SDXL/Flux用LoRAを読み込めても意図した結果にならないと説明されています。RS Samplerも各モデル用ワークフローと適合するモデル・エンコーダー・VAEを指定しています。
4. **RTX 3060 12GBでの確実な実測値は公開情報から確認できず。** 領域制御自体はマスクや条件付けの追加ですが、複数LoRAの独立推論や大規模モデル、参照バックエンドがVRAM・時間を増やします。12GBではSDXL系を先に試し、Krea 2/Flux系は量子化・オフロード設定と解像度を抑えた検証が必要です。

## 混線防止関連アップデート

### 新規情報

- **RS MultiCharacter Sampler 0.2.5（10月21日）:** キャラクターごとの画像参照を実験機能として追加。領域位置は既存の点・矩形・マスクを共有し、モデル系統ごとに異なる実装を持ちます。リリース記載では8つの代表モデル系統で計21回の統合生成を成功としていますが、任意マスク、参照3枚以上、参照とキャラクター別LoRAの併用は同等の生成検証を経ていません。SDXLの衣装再現や過飽和も制約として記載されています。
- **Krea2 Multi-LoRA Composer:** 1〜5体について、キャラクターのトリガー、説明、強度、領域、denoising scheduleを設定。LoRA差分を担当領域に限定し、テキスト側のトークン分離と領域attention biasを組み合わせます。Krea 2専用で、対応ComfyUIとKrea 2モデル・CLIP・VAE、およびKrea 2用LoRAが必要です。
- **Krea2 Regional Character LoRA:** 2または3領域にキャラクターLoRAを割り当て、各領域最大3つのLoRAを重ねるノード群。キャラクターLoRAを通常のグローバルLoRAチェーンに入れず、当該ノード側へ接続する構成を案内しています。標準LoRA形式が対象で、LoHa/LyCORISは非対応です。

### 更新情報

- **RS Samplerの適用範囲と注意点が明確化。** 最大10スロット、各キャラクターの独立プロンプト・LoRA・位置指定、OpenPose由来の近似人物マスク、検出ベースのローカル詳細化に対応。一方、人数・同一性・ポーズの正確さはモデル依存で、混雑した構図や交差する小物は混線・人物欠落・重複の原因になり得ます。キャラクター別ネガティブや条件付けスケジュールは非対応。FLUX Fill/Control、SD2、inpainting/refinerモデル、外部ControlNet/attention patchもregional samplerの対象外です。
- **ComfyUIコミュニティの実用パターン:** 共通のシーン説明とキャラクター別プロンプトを分け、各キャラクターに領域とLoRAを割り当てる方法が継続。領域指定後も顔や細部に漂移が残る場合は、各人物を専用LoRAで個別にマスク詳細化する段階処理が現実的です。

### 継続監視

- 似た外見のキャラクターや狭い領域での属性交換、髪色・衣装・顔の漏れ。
- 領域境界を越える腕・髪・衣装などの自然さと、領域を厳しくしすぎた際の切り抜き感。
- SDXL/Illustrious、Flux系、Krea 2、Anima、MOSSで同じノードの挙動が再現するか。
- 参照画像機能の独立LoRA併用・複数参照・任意マスクでの第三者再現検証。

## ComfyUI関連

| 手法/ノード | 用途 | 実用上の評価 |
|---|---|---|
| RS MultiCharacter Sampler | 1つの生成内で複数人物のプロンプト、位置、LoRAを管理 | モデル別サンプルと詳細化まで揃い、汎用候補。ただし対応モデル一覧・制限を確認する |
| Krea2 Multi-LoRA Composer | Krea 2で1〜5体の領域LoRA合成 | 差分ルーティング、トークン分離、配置UIを備える。Krea 2専用で、ノード説明の主張と第三者再現性は区別する |
| Krea2 Regional Character LoRA | 2〜3領域への直接的なLoRA割当 | 構成が比較的単純。標準LoRA対応、LoHa/LyCORIS非対応。マスクのfeatherやtext strengthを調整する |
| AttentionCouple + Advanced-ControlNet hooks | Attention領域とLoRA hookを組み合わせる | 5人の一括生成例が公開されているが53ノード構成。利用モデル・フック互換性の確認が必要 |
| Civitai Eazy Regional Prompter workflow | Illustrious/SDXLで領域別プロンプトとLoRA | 10月9日更新情報。領域プロンプト欄にLoRAとトリガーを書く方式。導入しやすい候補だが、SDXL系に限定して評価する |

公開ワークフローのうち、ComfyUI node packsの説明ではAttentionCouple、Advanced-ControlNetのLoRA hooks、マスク生成ノードを組み合わせて単一パスで複数人を生成しています。構成が複雑なため、まず2人・単純な左右分割から検証するのがよいでしょう。

## Flux関連

- Krea 2 / Flux.2 Klein系では、キャラクターごとの領域LoRA実装が具体化しています。ただし、Krea 2用に学習されたLoRAと対応する基盤モデルの組み合わせが前提です。異なる系統のLoRAをロードできることは、同等品質や正しい同一性を意味しません。
- RS SamplerはFLUX.1/2/3用ワークフローやモデル別設定を掲げていますが、regional samplerにはFLUX Fill/Controlの制限があります。さらに実験的な参照バックエンドの対応表と、各モデル系統での性能・品質実証を混同しないでください。
- 検索したHugging Face上のKrea 2 Regional Multi-LoRA資料はKrea 2向けLoRAの制約を説明しています。RTX 3060上の正式な速度・VRAM測定や、異種モデルLoRAの移植性を裏付ける公開ベンチマークは見つかりませんでした。

## 実運用で使える手法

### 1. 領域別プロンプト + 領域別LoRA（まず試す方法）

**概要:** 共有シーンプロンプトに、人物ごとの外見・動作プロンプト、位置（矩形またはマスク）、対応するキャラクターLoRAを割り当てます。ComfyUIではRS Sampler、Krea 2専用ノード、AttentionCouple系などからモデルに合うものを選びます。

**効果:** LoRAとテキストの影響を担当領域へ集中させ、全画面にLoRAを適用する通常のスタックで起きるIdentity/Feature Bleedingを減らす狙い。構図や領域に依存し、混線ゼロを保証するものではありません。

**RTX3060 12GBでの実用性:** SDXL/Illustriousの低〜中解像度から試すのが堅実です。Krea 2などの大規模モデルは量子化版・オフロードの有無で変わるため、モデルごとの実測が必要です。1人ずつ追加してVRAMを記録してください。

**ComfyUI実装難易度:** 中。対応するノードとモデル別ワークフローを導入し、2人の単純領域から始めます。

**Forge実装難易度:** SDXL系のregional workflowやForge Neo/Krea 2対応が利用できる場合は中〜高。ComfyUI向けの独自hookノードをそのままForgeに移植できるとは限りません。

**注意点:** LoRAとベースモデルの系統・学習元を合わせる。領域の境界を人物の髪や手足の端に置かず、多少余白を持たせる。強度を上げすぎない。共通プロンプトで人数とシーンを明確にし、個別プロンプトにはその人物の識別特徴を短く明確に記載します。

### 2. 領域別生成後に人物ごとにマスク詳細化

**概要:** 全体の構図を先に作り、人物ごとのマスク、プロンプト、LoRAで顔や衣装を低denoiseのimg2img/detailer処理します。

**効果:** 最終段で一人ずつ修正できるため、局所的な顔・服の漂移を抑えやすい一方、人物間の接触・重なりや光の整合を壊すことがあります。

**RTX3060 12GBでの実用性:** 一度に全モデルを保持せず、人物ごとに処理すれば現実的。クロップ解像度を抑え、まずdenoise 0.2〜0.3程度を起点に確認します（作者のDetailer例は0.25）。

**ComfyUI実装難易度:** 中。Impact Pack等の依存追加と検出器設定が必要な場合があります。

**Forge実装難易度:** 中。ADetailer/マスク付きinpaintで代替可能ですが、専用LoRAを人物単位で切り替える構成は環境により異なります。

**注意点:** 自動検出が人物を誤対応していないか確認。境界が見える場合はマスクを拡張・ぼかし、denoiseを下げます。元画像のメタデータやモデルが必要なワークフローでは再現用に保存してください。

## RTX3060 12GB評価

| 構成 | VRAMの見立て | 推奨設定/速度 | 安定性 |
|---|---|---|---|
| SDXL/Illustrious + 2領域 + 2 LoRA | 中。実測値なし。通常のSDXLよりノード実装分の一時メモリが増える可能性 | 768〜1024級の控えめな解像度、バッチ1、領域は2つから。追加LoRAごとに速度を比較 | 比較的試しやすい。似たキャラや狭い領域は要修正 |
| Krea 2 / Flux.2 Kleinの領域LoRA | 中〜高。量子化とオフロードに依存。公式な3060測定は未確認 | 対応するFP8等の配布モデルがあれば低解像度で試す。まず単一LoRAと2領域で動作確認 | 依存するComfyUIの新しいモデルラッパーやノード互換性を確認 |
| 複数参照画像バックエンド | 高くなる可能性。必要重みは有効化時に追加ロード | 初回ロード後にVRAMピークと速度を記録。12GBで余裕がなければOFF/strength 0 | 2026-10-21時点で実験的。LoRAの代用としては未推奨 |
| 人物別Detailer | クロップ処理なら抑えやすい | バッチ1、denoise 0.25を出発点に、検出・マスクを確認 | 検出誤りやマスク端の継ぎ目に注意 |

**注意:** 公開ソースにRTX 3060 12GBの再現可能なVRAM・秒数計測はありません。上表の区分は構造に基づく目安で、実測値ではありません。実運用では同じ解像度・seed・stepsで、LoRAなし/1本/2本のピークVRAM、生成時間、混線率を比較してください。

## 次週監視項目

1. RS MultiCharacter Samplerの参照機能で、キャラクターLoRAとの併用、3枚以上の参照、SDXL衣装再現に関する追加検証が公開されるか。
2. Krea2 Multi-LoRA ComposerおよびKrea2 Regional Character LoRAの独立した比較画像、互換性一覧、ComfyUI更新追随。
3. Forge NeoでKrea 2系の領域LoRAが使える範囲と、ComfyUI実装との機能差。
4. RTX 3060 12GBを含むGPU別VRAM・速度の利用者報告。
5. 人物同士の接触・重なりを保ちつつ、領域漏れや境界線を抑える手法。
6. 10人対応など大きな上限の実用性。まず2〜3人での品質を基準にし、上限値だけで採用判断しない。

## 情報源

### GitHub

- [RS MultiCharacter Sampler](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler) — ノード、対応モデル、利用制限。
- [RS Sampler Releases](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler/releases) — 0.2.5（2026-10-21）の画像参照機能と検証範囲。
- [Krea2 Multi-LoRA Composer](https://github.com/lokitsar/ComfyUI-Krea2-MultiLoRA-Composer) — 領域ルーティングと要件。
- [Krea2 Regional Character LoRA](https://github.com/billautomata/krea_regional_lora) — 2/3領域、LoRA stack、対応形式。
- [Multi-character regional prompting workflow](https://github.com/digitalinnovator/comfyui-production-workflows/tree/main/06-multi-character-regional-prompting) — AttentionCoupleとADE hookを使うサンプル。

### Hugging Face

- [Sentinel7/krea2 の資料コミット](https://huggingface.co/Sentinel7/krea2/commit/883090df36ab0db60ae6f98b6f5928c06df8dbff) — Krea 2 Regional Multi-LoRA資料とLoRAのモデル系統制約。

### Civitai

- [Eazy Regional Prompter — Illustrious Workflow v0.7](https://civitai.com/models/339604) — 検索結果で確認できた2026-10-09更新情報。各地域にLoRAとトリガーを指定する方式。URLのモデルページは更新が続くため、利用時に最新版の説明とワークフローを確認してください。

### X (Twitter)

- 公開ウェブ検索では、今回の新規実装について一次確認できるX投稿を特定できませんでした。未確認の投稿を情報源として扱わず、GitHubのリリース・READMEを一次資料にしています。

### ComfyUI Community / 利用者報告

- [ComfyUI Community: multiple characters in one image](https://www.reddit.com/r/comfyui/comments/1ws23ur/multiple_characters_in_one_single_generated_image/) — 2026-09-28の相談。複数人物での属性分離に、地域指定・inpaintingが引き続き必要という課題。
- [ComfyUI Community: six characters in one image](https://www.reddit.com/r/comfyui/comments/1wkh6if/how_to_generate_6_characters_in_a_single_image/) — 多人数では顔・属性の低下、混線、個別inpaintを指摘。
- [Civitai/ComfyUI community workflow update](https://civitai.com/models/339604) — Eazy Regional Prompterの地域別LoRA指定。コミュニティ配布ワークフローとして扱い、作者記載の効果を独立検証済みとみなさない。

---

**まとめ:** いま試す価値が高いのは、基盤モデルと同じ系統のLoRAを使い、人物別プロンプトと領域マスクを割り当てる方法です。仕上げの顔・衣装だけ人物ごとにdetailer/inpaintで直すと、12GB環境でも処理を分割できます。参照画像の自動化や大人数一括生成は、追加検証と手元のVRAM実測を待つのが妥当です。
