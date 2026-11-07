# MiniMax調査レポート — 2026-11-07

調査日: 2026-11-07（JST）  
比較対象: `Reports/2026-11-03_MiniMax_Report.md`、`Reports/2026-10-31_MiniMax_Report.md`

## 今週の重要トピック

- **ComfyUI v0.44.0（11月4日公開）でローカルMiniMax H3の使い道が広がりました。** H3 latent upscaler、Sol-H3-VAE、temporal context window対応が追加されています。前回レポートの「新しいH3専用コア更新なし」からの明確な差分です。[公式リリース](https://github.com/Comfy-Org/ComfyUI/releases)
- **RTX 3060 12GBの追加実例:** Pushbulletで取得したX投稿のスレッドでは、Turbo LoRAワークフローを480p・5秒・6 stepsで試し、2本を302秒・288秒で生成したという作者自己申告がありました。独立再現ではなく、前回の別条件の3060ベンチマークと横並び比較できません。[投稿](https://x.com/PixelAigc/status/2117537769912414535)
- **VAEデコード高速化の候補:** ComfyUIのSol-H3-VAE対応PRには、RTX 5090で124フレームをデコードした測定が示されています。品質・速度の方向性を示す参考値ですが、3060性能を保証しません。

## 新機能・アップデート

### 新規 — H3 latent upscaler

ComfyUI v0.44.0はH3用の3D-convolution latent upscaler checkpointをロードする機能と、動画latentを目標幅・高さへ拡大するノードを追加しました。PRの説明では16フレームずつ時間方向に処理し、音声latentはそのまま通します。[PR #17412](https://github.com/Comfy-Org/ComfyUI/pull/17412) · [upscaler model](https://huggingface.co/LBH-123-AI/Minimax_h3_latent_Upscaler)

これはlatent段階の拡大経路です。最終画質の改善量や、3060でのVRAM・実行速度の公開実測は確認できません。高解像度化で処理負荷が増えるため、短いクリップで段階的に確認します。

### 新規 — Sol-H3-VAE

ComfyUI v0.44.0でSol-H3-VAEのデコードに対応しました。PRは、H3 VAE decoderを蒸留した24層のdecoderで、動画クリップ全体を扱う設計と説明しています。RTX 5090・1344×768・124フレームの報告値は以下です。[PR #17411](https://github.com/Comfy-Org/ComfyUI/pull/17411)

| Decoder | 時間 | 最大VRAM |
|---|---:|---:|
| 標準H3 VAE fp16 | 10.7秒 | 5.5 GiB |
| 標準H3 VAE int8 | 4.61秒 | 3.2 GiB |
| Sol fp16 | 3.28秒 | 5.9 GiB |
| Sol int8 | 1.70秒 | 4.3 GiB |

これらはRTX 5090でのデコード測定で、H3全体の生成時間ではありません。PRはSol decoderが時間方向にtileできず、動画が長くなるほど活性値メモリが増える点も記載しています。3060で同じメモリ値・速度になるとは推定できません。

### 新規 — H3 temporal context windows

v0.44.0はH3のcontext-window処理を追加し、時間方向のウィンドウ長・overlap・fuse方法・FreeNoiseなどをノードから指定できます。PR説明では、動画windowを音声範囲へ対応させ、keyframe情報や音声denoise maskも各windowに合わせる構成です。[PR #17425](https://github.com/Comfy-Org/ComfyUI/pull/17425)

これは長いシーケンスをwindowごとに扱う基盤です。長尺でのキャラクター・動き・音声の一貫性や、3060での最大長を保証する結果は確認できません。

### API/Partner Nodes — H3 Max機能群

同じv0.44.0にはH3 Max Recast、Extend、Reframe、Insert、Lip Sync、Camera ControlのPartner Nodesも追加されています。[PR #17424](https://github.com/Comfy-Org/ComfyUI/pull/17424)

これらはComfyUI内で提供されるAPIノード群で、ローカルの公開H3 checkpointに加わったローカル推論機能とは区別します。利用にはサービス/API条件を確認してください。RTX 3060だけで実行できる機能とは扱いません。

## ComfyUI関連

- 前回の標準T2V/I2V/R2Vテンプレートに加え、v0.44.0でH3 latent upscale、Sol VAE decode、context-window処理が標準コアに入りました。
- 先にComfyUI本体をv0.44.0以上へ更新し、モデル・VAE・ワークフローをバックアップしてから試します。custom node更新だけではこのコア機能は入りません。
- 同週のPushbullet投稿で紹介された[Turbo LoRA workflow](https://github.com/pixelaigc/ComfyUI-MiniMax-H3-Workflow)はT2V/I2V等を1つのComfyUI workflowにまとめたコミュニティ配布物です。投稿者は3060 12GBでの動作例を示しましたが、設定や環境を完全に揃えた第三者検証ではありません。

## 長尺動画関連

v0.44.0のcontext windowsが今週の新しい長尺関連項目です。時間window、overlap、融合方式を設定できるため、単一の一括処理とは違う分割処理を組めます。ただし設定値によって境界部分の動き・音声・人物の連続性が変わり得ます。まず短い動画でwindow間の重なりを可視確認し、長さを少しずつ伸ばしてください。H3が公式に保証する生成長を超えると断定できる資料は見つかりませんでした。

## 360°・VR関連

今週、H3で360°・VR向けの新しい公式機能や再現可能なワークフローは確認できませんでした。context windowsやlatent upscaleは360°投影・ステレオVR対応を意味しません。

## RTX3060 12GBで使える手法

### A. Turbo LoRA workflow（投稿者の3060実例）

- **概要:** ComfyUIでH3をTurbo LoRA付きで動かすcommunity workflow。投稿者は480p・5秒・6 stepsで2本生成し、302秒と288秒を報告。
- **VRAM消費:** 投稿にはピークVRAM値がなく未確認。12GBカードで動いたという個人報告のみ。
- **推論速度:** 約4分48秒／5分02秒の投稿者測定。環境・設定が不明なため速度基準にはできません。
- **ComfyUI実装難易度:** 中〜高。workflowに必要なモデル、LoRA版、ComfyUI core、VAE、テキストエンコーダーを揃える必要があります。
- **導入難易度:** 中〜高。モデルファイルとシステムRAM、オフロード条件を確認します。
- **実用性評価:** 3060 12GBでの実行可能性を示す一例。まず480p・短尺から再現する候補です。
- **注意点:** 6 stepsであっても別Turbo LoRAやcheckpointとの組合せをそのまま流用できるとは限りません。ファイル名とworkflow内指定を照合してください。

### B. Sol-H3-VAE

- **概要:** H3動画のlatent decodeを置き換える蒸留decoder。v0.44.0以降のComfyUIが必要。
- **VRAM消費:** RTX 5090で124フレームのSol int8最大4.3 GiB、Sol fp16最大5.9 GiBというPR測定。3060での実測なし。
- **推論速度:** RTX 5090の同じテストではint8 1.70秒、fp16 3.28秒。あくまでVAE decode時間。
- **ComfyUI実装難易度:** 中。本体更新後に対応weightを正しいVAE形式でロードします。
- **導入難易度:** 中。Sol weightを取得し、既存H3 workflowへの接続を確認します。
- **実用性評価:** 画質を保ちつつdecode時間を減らす可能性があるため試す価値があります。ただし3060のVRAM余裕は未確認です。
- **注意点:** decoderは時間方向にtileできず、長い動画・高解像度ほど活性値メモリが増加。短いclipで先に試してください。

### C. H3 latent upscaler

- **概要:** H3 video latentを指定寸法に拡大する3D-convモデルと標準ノード。
- **VRAM消費:** 3060実測なし。16フレーム単位のstreaming処理という実装説明はありますが、必要VRAMの数値ではありません。
- **推論速度:** 公開された3060速度値なし。
- **ComfyUI実装難易度:** 中。ComfyUI v0.44.0と専用checkpointが必要。
- **導入難易度:** 中。latent modelを追加し、短いvideo latentで寸法とdecode後の結果を確認します。
- **実用性評価:** 高解像度化の後処理候補。生成品質・速度改善の独立試験はまだ不足。
- **注意点:** upscale後のSol VAE等のdecodeと組み合わせたメモリ測定が必要。GPU VRAM不足や長時間化に備えます。

## ワークフロー改善情報

1. v0.44.0へ更新する前に動作中のComfyUI環境とworkflow JSONを保存します。
2. 同じseed・解像度・フレーム数で標準VAEとSol-H3-VAEを比較し、decode時間とピークVRAMを別に記録します。
3. latent upscaleは最初に短いclipだけで試し、元latentと拡大後を同じdecoderで比較します。
4. context windowは短い動画から始め、window長・overlap・fuse方式を一項目ずつ変更し、境界での人物・音声の連続性を確認します。
5. 比較記録にGPU、システムRAM、ComfyUI版、モデル/LoRA/VAEの完全なファイル名、steps、CFG、解像度、フレーム数、処理時間を含めます。

## 次週監視項目

- ComfyUI v0.44.0のH3 latent upscalerとcontext-windowを使った公開workflow・3060測定
- Sol-H3-VAEのRTX 3060 decode時間・ピークVRAMと標準VAEとの品質比較
- PixelAigc Turbo workflowの完全なモデル・設定条件と第三者再現
- H3 Max APIノードの利用条件、料金、対象地域・機能
- MiniMax公式H3 checkpoint/APIの更新、人物一貫性・カメラ制御・音声同期の新しい実測
- 360°/VRのH3固有機能・workflow

## 情報源

- [ComfyUI v0.44.0 release](https://github.com/Comfy-Org/ComfyUI/releases)
- [MiniMax H3 latent upscaler PR #17412](https://github.com/Comfy-Org/ComfyUI/pull/17412)
- [H3 latent upscaler model](https://huggingface.co/LBH-123-AI/Minimax_h3_latent_Upscaler)
- [Sol-H3-VAE support PR #17411](https://github.com/Comfy-Org/ComfyUI/pull/17411)
- [H3 context-window PR #17425](https://github.com/Comfy-Org/ComfyUI/pull/17425)
- [H3 Max Partner Nodes PR #17424](https://github.com/Comfy-Org/ComfyUI/pull/17424)
- [PixelAigc Turbo workflow repository](https://github.com/pixelaigc/ComfyUI-MiniMax-H3-Workflow)
- [PixelAigc 3060 12GB report](https://x.com/PixelAigc/status/2117537769912414535)
- [Comfy-Org MiniMax H3 model repository](https://huggingface.co/Comfy-Org/MiniMax-H3)
- [2026-11-03 MiniMax report (comparison)](2026-11-03_MiniMax_Report.md)
