# MiniMax調査レポート — 2026-10-31

調査日: 2026-10-31（JST）  
前回比較: `Reports/2026-10-17_MiniMax_Report.md`（前回調査は2026-10-25）。今回は10月17日以降に確認できたComfyUI/Hugging Face更新と3060実測例を中心に追記。

## 今週の重要トピック

- **RTX 3060 12GBでMiniMax H3の約10秒動画を高解像度生成したコミュニティ実測が追加されました。** 10月27日付の投稿は2336×1312、243フレーム、DMAD 4-step、Comfy Kitchen INT8 Sparse Attention、32GB RAMで約33分を報告しています。単一ユーザーの自己申告であり、一般的な速度保証や別環境での再現確認ではありません。[実測投稿](https://www.reddit.com/r/comfyui/comments/1xgu6b8/minimax_h3_rtx_3060_12gb_minimax_h3_native_23361312_snow/)
- **ComfyUI本体とモデル置き場に細かな改善・追加が続いています。** ComfyUI v0.39にはMiniMax VAEのオフロード修正と埋め込み一時メモリ解放が含まれ、Hugging FaceのComfy-Org/MiniMax-H3最新履歴にはPika H3 Flex LoRA（FL2VA/Ref2VA）の追加が表示されています。[ComfyUI Releases](https://github.com/Comfy-Org/ComfyUI/releases) · [Hugging Face model files](https://huggingface.co/Comfy-Org/MiniMax-H3)
- **長尺はチャンク継続、速度は蒸留LoRA/attention設定、高解像度は追加メモリ最適化という別課題です。** RTX 3060の報告例は大きく進歩していますが、速度・画質・参照一致・RAM使用量のトレードオフが残ります。

## 新機能・アップデート

### 新規・更新情報（10月17日以降）

1. **ComfyUI v0.39のH3関連修正**  
   10月5日公開のリリースノートには、MiniMax VAEのオフロード不具合修正、H3埋め込み一時データの解放が記載されています。低VRAM環境で試す際は古いビルドを固定せず、依存拡張を含めて更新前後の互換性を確認してください。[v0.39 release notes](https://github.com/Comfy-Org/ComfyUI/releases)

2. **Pika H3 Flex LoRA adapters**  
   10月31日時点でHugging FaceのComfy-Org/MiniMax-H3履歴に、FL2VAおよびRef2VA用Pika H3 Flex LoRAアダプターの追加が表示されています。対応するH3モデル系列とチェックポイントを合わせる必要があります。これは配布リポジトリの追加情報で、MiniMax公式製品発表やRTX 3060上の性能保証を意味しません。[Hugging Face model repository](https://huggingface.co/Comfy-Org/MiniMax-H3)

3. **10月のRTX 3060 12GBコミュニティ実測**  
   10月26日頃の投稿は1536×864・243フレーム・4-stepを608秒で生成した例を報告。10月27日の別投稿では2336×1312・同じ243フレームを1989.93秒で生成したとしています。両方とも自己申告で、モデル（Singularity Ref2VA V2 / Pruned INT8 ConvRot R2）、入力参照、attention設定等が異なるため、性能比較はできません。[1536×864 / 608秒](https://www.reddit.com/r/comfyui/comments/1xf3khv/minimax_h3_singularity_v2_on_rtx_3060_12gb/) · [2336×1312 / 33分](https://www.reddit.com/r/comfyui/comments/1xgu6b8/minimax_h3_rtx_3060_12gb_minimax_h3_native_23361312_snow/)

### 更新・継続情報

- **ComfyUI標準対応:** 公式ドキュメントにはT2V、I2V、R2V、Multiframe Reference、Fun ControlNet Unionのテンプレートが掲載されています。標準H3ワークフローはComfyUI 0.30.0以降、Multiframe Referenceは0.34.0以降、Union 2.0やSparse Attention等は0.35.0以降が必要と記載されています。FastH3向けの速度重視機能は0.36.0以降の案内です。[ComfyUI H3 docs](https://github.com/Comfy-Org/docs/blob/main/tutorials/video/minimax/minimax-h3.mdx)
- **メモリ:** ComfyUI公式紹介は、量子化・重みのprune・動的VRAMオフロードでH3モデルの配置を縮小し、RTX 3060級でもローカル実行できると説明しています。ただしこれは「モデル全体が12GB VRAMに載る」という意味ではありません。前回レポート記載のモデル一式ディスク/RAM要件と併せて解釈してください。[ComfyUI公式紹介](https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui)
- **長尺・高解像度補助:** Flow-Aligned Regenerate v0.3.14（10月17日）は、低解像度の軌跡を使った二段階再生成や同一スケジュール内の解像度handoffを提供すると説明しています。学習不要のコミュニティノードであり、画質向上や時間短縮はワークフロー・モデル・設定ごとに検証が必要です。[GitHub](https://github.com/xmarre/MiniMax-H3-Flow-Aligned-Regenerate)
- **ComfyUI v0.40系列以降:** リリース履歴にH3関連修正・新しい各種ワークフローが続いています。更新はカスタムノードとモデルファイル双方に影響するため、動作中ワークフローはJSONと使用モデル名を保存してから更新するのが安全です。[Releases](https://github.com/Comfy-Org/ComfyUI/releases)

## ComfyUI関連

- 初回導入はComfyUI Template LibraryのT2V/I2V/R2Vから行い、欠落ノードがあればComfyUI本体を更新します。H3の標準ノードは本体機能です。[公式H3チュートリアル](https://github.com/Comfy-Org/docs/blob/main/tutorials/video/minimax/minimax-h3.mdx)
- RTX 3060向けには、まずpruned INT8 ConvRot系と対応VAE/テキストエンコーダーを使う。Turbo/DMAD LoRAは配布先が指定するモデル系統、ステップ数、CFGを崩さない。
- 高解像度・長尺をいきなり回さず、短いテストでモデル読込、VAE decode、音声同期、システム安定性を確認する。Sparse Attentionの設定やメモリchunkingは作者の動作条件を再確認する。
- 2026年10月10日開始のComfyUI GitHub Issueには、Windows/RTX 3060 12GB環境でNVFP4 encoder/offload利用時にPC全体がフリーズしたという未解決報告があります。投稿者はcustom nodeを使用し、クリーン環境での再現も確立していません。原因がNVFP4やComfyUI本体だとは断定できません。[Issue #16946](https://github.com/Comfy-Org/ComfyUI/issues/16946)

## 長尺動画関連

- **実用パターン:** まず短いクリップでシーンと参照の効き方を確かめ、その後フレーム数を増やす。チャンク継続を使う場合はContinuum等の対応する拡張とComfyUIコアのバージョンを固定する。
- **Flow-Aligned Regenerate:** 低解像度生成の構造やノイズ軌跡を後段の高解像度生成へ渡す設計で、低VRAMで最終解像度を狙う実験的選択肢です。RTX 3060での標準的な速度・品質ベンチマークは今回確認できませんでした。
- **限界:** 243フレーム級の成功例があっても、物語全体の人物・衣装・音・動作の連続性は個別に確認が必要です。4-step蒸留の画質やprompt adherenceはモデル・LoRA別に検証してください。

## 360°・VR関連

10月17日以降の調査で、MiniMax H3の360°/VR生成に関する新しい公式機能・3060上の再現可能な一次資料は特定できませんでした。前回レポートに記載したパノラマ/VR180のコミュニティ実験は継続監視対象です。通常のH3動画をVR用の立体映像や継ぎ目のない360°映像とみなすことはできません。

## RTX3060 12GBで使える手法

| 項目 | 評価 |
|---|---|
| VRAM | 動的オフロード・pruned/量子化モデルが前提。12GBに全モデルが常駐する構成ではない。 |
| 実測の一例 | 32GB RAM、3060 12GB、243 frames、2336×1312、4-step、約33分という単一コミュニティ投稿。別設定では1536×864・243 framesで約10分。 |
| 推奨開始点 | 公式テンプレート、低い解像度・短い長さ、対応するpruned INT8 ConvRot、モデル指定どおりのTurbo/DMAD設定。 |
| 推論速度 | 大きく設定依存。10秒級が約10〜33分の実測例はあるが、横並びベンチマークではない。 |
| 導入難易度 | 中〜高。大容量モデル、ComfyUI版、Torch/CUDA、VAE、量子化形式、カスタムノードの整合が必要。 |
| 安定性 | 個人測定は実用可能性を示す一方、Windowsの未解決フリーズ報告もある。重要データを保存し、短いテストから行う。 |

## ワークフロー改善情報

1. ComfyUIとH3用VAE/モデルを同じタイミングで整合させる。特に古いComfyUIで最新VAEやH3モデルを混在させない。
2. Seedと入力フレームを固定し、解像度・フレーム数・attention設定を一項目ずつ変更して速度と品質を記録する。
3. 実測を残す際はGPU、RAM、モデルの完全なファイル名、steps、FPS/frames、解像度、使用ノードを記録し、自己申告値を別環境の保証と混同しない。

## 次週監視項目

- Pika H3 Flex LoRAの利用条件、対象チェックポイント、品質比較
- ComfyUI v0.40以降のH3 VAE/オフロードと埋め込みメモリ改善の実利用報告
- RTX 3060 12GBの独立再現、必要なシステムRAM、Sparse Attentionの画質・速度比較
- H3 Flow-Aligned RegenerateおよびContinuum系の更新、長尺継続時の破綻とVRAM実測
- 公式MiniMax発表でのローカル重み・ライセンス・H3 Max等の変更

## 情報源

- [MiniMax H3公式ComfyUI対応記事](https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui)
- [ComfyUI H3公式チュートリアル](https://github.com/Comfy-Org/docs/blob/main/tutorials/video/minimax/minimax-h3.mdx)
- [ComfyUI Releases](https://github.com/Comfy-Org/ComfyUI/releases)
- [Comfy-Org MiniMax-H3 — Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3)
- [RTX 3060 12GB: 2336×1312 / 33分の投稿](https://www.reddit.com/r/comfyui/comments/1xgu6b8/minimax_h3_rtx_3060_12gb_minimax_h3_native_23361312_snow/)
- [RTX 3060 12GB: 1536×864 / 608秒の投稿](https://www.reddit.com/r/comfyui/comments/1xf3khv/minimax_h3_singularity_v2_on_rtx_3060_12gb/)
- [未解決フリーズIssue #16946](https://github.com/Comfy-Org/ComfyUI/issues/16946)
- [MiniMax H3 Flow-Aligned Regenerate](https://github.com/xmarre/MiniMax-H3-Flow-Aligned-Regenerate)
