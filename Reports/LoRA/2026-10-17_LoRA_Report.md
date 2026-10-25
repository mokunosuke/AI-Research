# LoRA Research Report — 2026-10-17

> 調査日: 2026-10-25（Asia/Tokyo）  
> 今回は指定された日付のファイル名を使用しています。調査日は10月25日で、10月17日以後に公開された情報も含みます。

## 今週の重要トピック

- **キャラクターごとに領域とLoRAを割り当てる方向が実装面で進展。** ComfyUIのRS MultiCharacter Samplerは最大10領域、人物別プロンプト・LoRA・位置指定、マスク作成、人物別detailerを備えます。モデル側の空間領域制御により、LoRAを全画面へ適用する際の顔・髪・衣装の混線を抑える設計です。
- **画像参照機能は追加されたが、実験段階。** 10月21日公開のRS Sampler 0.2.5は人物ごとに参照画像を割り当てます。リリース自身が「非推奨」とし、モデルごとの品質差、SDXLでの衣装忠実度や過飽和、参照とLoRAの併用など未検証範囲を挙げています。適合LoRAがある場合はLoRAを優先するのが妥当です。
- **Krea 2専用のマルチLoRA制御が具体化。** ComfyUI向けComposerは1〜5人、各LoRAの空間ルーティング、対象トークン分離、領域attention biasを組み合わせます。Krea 2向けに学習されたLoRAが前提で、他系統LoRAの読み込みが適切な結果を保証するわけではありません。
- **実用面では、領域指定 + 人物ごとの後段修正が堅実。** 生成時に人物の大枠を分離し、残る顔・衣装の崩れは個別マスク付きdetailer/inpaintで補います。RTX 3060 12GBでの統一ベンチマークは確認できず、モデル・解像度・ノード実装ごとの計測が必要です。

## 混線防止関連アップデート

### 新規情報

- **RS MultiCharacter Sampler 0.2.5（10月21日）:** 1キャラクター1画像参照を任意機能として追加。参照画像は既存の点・ボックス・マスク領域に割り当て、強度の初期値は0.6。8つの代表モデル系統で計21回の統合生成を成功したと作者が報告しています。ただし、任意マスク・3枚以上の参照・人物別LoRAとの併用に同等の生成検証はなく、品質の一貫性も未確立です。
- **Krea2 Multi-LoRA Composer:** 1〜5体のLoRAを配置領域ごとに設定し、LoRA差分を担当領域へ限定。トリガー語の分離と画像領域へのattention biasも使用します。Krea 2モデル、対応CLIP/VAE、Krea 2用LoRA、新しめのComfyUIが必要です。
- **Krea2 Regional Character LoRA:** 2または3領域にLoRAを適用し、各領域に最大3つまでスタック可能。キャラクターLoRAは通常のグローバルLoraLoaderに入れず、専用ノードへ渡します。標準LoRA形式が対象で、LoHa/LyCORISは非対応。

### 更新情報

- **RS Samplerの機能と制約が明確化。** 領域は点・ボックス・外部マスク・描画マスクで指定できます。OpenPoseデータからは骨格制御ではなく概略人物マスクを作成。人物別detailerは対応キャラクターの元プロンプトとLoRAを再利用します。最大10スロットですが、密集構図や交差する小物は人数の欠落・重複・属性混合を起こし得ます。人物別ネガティブプロンプトや時間変化するテキスト条件は非対応です。
- **既存の領域制御手法も継続。** AttentionCouple、Advanced-ControlNetのLoRA hooks、マスク生成を組み合わせる単一パス例があります。一方、ノード数が多く、モデル・フック互換性の確認が必要です。SDXL/Illustrious向けCivitaiワークフローでは、領域テキストにLoRA指定とトリガー語を書く形式も見られます。

### 継続監視項目

- 類似したキャラクター間の髪色、顔、衣装、属性の交換。
- 髪・腕・小物が領域境界をまたぐ構図での漏れと、境界を厳しくした場合の切り抜き感。
- SDXL/Illustrious、FLUX、Anima、Krea 2、MOSSでのノード・LoRA互換性と第三者再現例。
- 画像参照機能と複数LoRAの併用、3人以上、任意マスクの独立評価。

## ComfyUI関連

| 手法 | 使いどころ | 注意点 |
|---|---|---|
| RS MultiCharacter Sampler | モデル別に人物プロンプト、LoRA、位置、マスク、detailerを統合 | 対応するモデル・CLIP・VAEが必要。高密度配置や交差物は不安定 |
| Krea2 Multi-LoRA Composer | Krea 2で1〜5人のLoRAと領域を一画面で編集 | Krea 2専用。LoRA差分を領域に限定するという作者の実装説明であり、全プロンプト・全構図で混線ゼロを保証しない |
| Krea2 Regional Character LoRA | 2〜3領域のキャラクターLoRA適用 | 標準LoRA対象。各領域3本まで。LoHa/LyCORIS非対応 |
| AttentionCouple + ADE LoRA hooks | 領域attentionとLoRA hookを組み合わせる | 構成が複雑。モデルや各ノードの互換性を確認 |
| Eazy Regional Prompter（Civitai） | Illustrious/SDXL向け領域プロンプトとLoRA | 10月9日更新情報を検索で確認。SDXL系のワークフローとして評価し、他モデルへ一般化しない |

## Flux関連

- RS SamplerはFLUX.1/2/3のモデル別ワークフローを掲げ、参照機能にも各系統の実装があります。ただしFLUX Fill/Controlは地域サンプラーの対応外など、機能ごとの制限があります。
- Krea 2系の地域LoRAは、Krea 2用に学習されたLoRAとの組み合わせが前提です。FLUX/SDXL LoRAをロードできるかどうかと、適切な同一性・画質が得られるかは別の問題です。
- 検索したHugging Face資料ではKrea 2向け地域LoRAの説明や対応ノードは確認できましたが、RTX 3060上で異なる系統のLoRAを比較した再現可能な測定は見つかりませんでした。

## 実運用で使える手法

### 1. 人物別プロンプト + 領域別LoRA

**概要:** 共通の場面・画風・人数を全体プロンプトに置き、人物ごとの外見・行動、担当位置、専用LoRAを分けます。領域は最初は左右など単純なボックスから始めます。

**効果:** LoRAとテキストの寄与を担当領域へ集中させ、全画面LoRAスタックによるIdentity/Feature Bleedingを抑える狙いです。人物同士の接触や領域外には影響が残ります。

**RTX3060 12GBでの実用性:** SDXL/Illustriousの低〜中解像度、バッチ1から試すのが現実的です。Krea 2などのモデルでは量子化やオフロードに左右され、同GPUでの公開比較値はありません。

**ComfyUI実装難易度:** 中。モデルに合うノード導入、プロンプト・領域・LoRAの行番号合わせが必要です。

**Forge実装難易度:** 中〜高。Forge Neoなどに対応した地域LoRA機能がある場合も、ComfyUIの専用hookノードを直接移植できるとは限りません。

**注意点:** ベースモデルとLoRAの学習系統をそろえます。LoRA強度は控えめから調整し、各人物の領域に少し余白を持たせます。共通プロンプトで人数・場面を明示し、人物ごとの特徴説明は簡潔にします。

### 2. 人物ごとのマスク詳細化

**概要:** まず全体構図を生成し、残った顔や衣装を人物別マスク、プロンプト、LoRAで局所的に再描画します。

**効果:** 一人ずつ修正できるため細部の同一性を補いやすい方法です。接触部や照明、背景との一体感を壊す場合があります。

**RTX3060 12GBでの実用性:** クロップ単位で順に処理すれば実行しやすくなります。RS Detailerの作者例では顔SEGM、WD ViT v3、denoise 0.25が開始点です。

**ComfyUI実装難易度:** 中。Impact Pack等の追加ノードと検出モデルが必要になる場合があります。

**Forge実装難易度:** 中。ADetailerまたはマスクinpaintで代替し、人物別LoRAの切り替えを設定します。

**注意点:** 検出器が正しい人物を選んだか確認し、マスク端の継ぎ目があれば拡張・ぼかしやdenoise調整を行います。

## RTX3060 12GB評価

| 構成 | VRAM/速度の見立て | 推奨の始め方 | 実用性 |
|---|---|---|---|
| SDXL/Illustrious、2人物、領域LoRA | 中程度。公開された3060統一実測なし | 低〜中解像度、バッチ1、LoRAを1本ずつ追加しピークVRAMを記録 | 導入候補。構図を単純にして有効性を確認 |
| Krea 2の地域LoRA | モデル量子化・オフロード依存。GPU別計測不足 | 対応モデルで2領域から試し、異系統LoRAは避ける | モデル・ノードの互換性確認が先 |
| 人物別detailer/inpaint | クロップ処理なら比較的抑えやすい | 1人物ずつ、denoise 0.25を起点に調整 | 後段の細部修正に有効 |
| 画像参照（RS 0.2.5） | 参照バックエンドが追加モデルをロードし、VRAM・時間が増える可能性 | まずOFF。使用時は1参照、低めの解像度から検証 | 実験機能。LoRAの代替としては未推奨 |

公開情報に3060 12GBの同一条件比較はありません。値の断定は避け、同じ解像度・seed・stepsで「LoRAなし／1本／2本」のピークVRAM、生成時間、混線の頻度を記録してください。

## 次週監視項目

1. RS 0.2.5の人物LoRA併用・複数参照・任意マスクでの独立検証。
2. Krea 2 Composer/Regional LoRAの対応ComfyUI版、実例、第三者の再現性。
3. Forge Neoの地域別LoRA機能とComfyUI実装との差。
4. RTX 3060 12GBを含むGPU別VRAM・速度・品質報告。
5. 人物同士が接触・重複する場面での領域境界、自然な光・影・手足の整合。

## 情報源

### GitHub

- [RS MultiCharacter Sampler](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler) — 現行ノード・モデル対応・制約。
- [RS Sampler Releases](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler/releases) — 0.2.5画像参照機能と検証範囲（2026-10-21）。
- [Krea2 Multi-LoRA Composer](https://github.com/lokitsar/ComfyUI-Krea2-MultiLoRA-Composer) — トークン分離と地域ルーティング。
- [Krea2 Regional Character LoRA](https://github.com/billautomata/krea_regional_lora) — 2/3領域、LoRAスタック、形式制約。
- [ComfyUI production workflows: Multi-Character Regional Prompting](https://github.com/digitalinnovator/comfyui-production-workflows/tree/main/06-multi-character-regional-prompting) — AttentionCouple + ADE hooksの実例。

### Hugging Face

- [Sentinel7/krea2資料コミット](https://huggingface.co/Sentinel7/krea2/commit/883090df36ab0db60ae6f98b6f5928c06df8dbff) — Krea 2地域LoRAとモデル系統の注意。

### Civitai

- [Eazy Regional Prompter — Illustrious Workflow v0.7](https://civitai.com/models/339604) — 2026-10-09更新情報。地域別プロンプト欄にLoRA・トリガーを指定するワークフロー。

### X (Twitter)

- 今回の調査で、上記の新規実装を一次確認できる公開X投稿を特定できませんでした。確認できた仕様・日付はGitHubのリリースとREADMEを一次資料として記録しています。

### ComfyUI Community

- [r/comfyui: multiple characters in one image](https://www.reddit.com/r/comfyui/comments/1ws23ur/multiple_characters_in_one_single_generated_image/) — 2026-09-28の相談。複数人物の属性分離や領域指定の課題。
- [r/comfyui: six characters in one image](https://www.reddit.com/r/comfyui/comments/1wkh6if/how_to_generate_6_characters_in_a_single_image/) — 多人数化での顔・特徴の劣化、個別inpaintの報告。

---

**まとめ:** まずモデルと同系統のキャラクターLoRAを使い、人物別プロンプトと領域指定を組み合わせる方法が実運用向きです。残る顔や衣装の崩れは人物単位のdetailer/inpaintで補えます。画像参照機能は追加されたものの実験段階であり、3060環境では低解像度・バッチ1から手元のVRAMと結果を測りながら試してください。
