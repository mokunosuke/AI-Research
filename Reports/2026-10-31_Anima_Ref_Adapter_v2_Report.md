# Anima Ref Adapter v2 調査レポート

調査日：2026年10月31日  
対象投稿：[malariadxのX投稿](https://x.com/malariadx/status/2116141819159249040)

## 要約

投稿はComfyUI-Anima-Ref-Adapter v2を紹介し、2人のキャラクター参照にも対応すると案内している。作者の公開説明では、参照画像からキャラクターの外見や画風の一部を引き継ぎ、ポーズ・背景・構図はプロンプトで指定する。2人を出す場合は、2枚の参照画像を並べて使う。

## 公式配布情報

- ComfyUIカスタムノード：[ElectronGirl/ComfyUI-Anima-Ref-Adapter](https://github.com/ElectronGirl/ComfyUI-Anima-Ref-Adapter)
- 重み：[ElectronGirl/anima-ref-adapter](https://huggingface.co/ElectronGirl/anima-ref-adapter)
- v2の重みは約183 MBで、Anima v1.0、Qwen3-0.6Bテキストエンコーダー、Qwen-Image VAEが前提。
- 公開作例ではRTX 3060 Ti 8GB、832×1216、30ステップで、参照なし約33秒、v2参照あり約65〜67秒という作者計測が示される。別設定ではさらに短縮される。

## 品質上の限界

作者は、人物の同一性は画風より移りやすく、強い絵画調の画風、小さな模様・傷・アクセサリー、珍しい肌色などは維持しにくいと説明している。服の大きな色がずれる場合や、参照キャラクターが背景物として再登場することもある。学習画像はAnima生成画像であり、ベースモデル由来の偏りを引き継ぐ。

## 開発状況

Hugging Faceのモデル説明では、資金不足のため開発を一時停止しており、キャラクター参照と画風参照を分離する計画などは未公開とされる。したがって、投稿の「v2」表記は確認できるが、今後の機能追加が続く前提では考えない方がよい。

## RTX 3060 12GBへの見通し

作者の8GB GPU計測例があるため、12GBカードはVRAM容量の面で試しやすい部類と考えられる。ただし、これは3060 12GBでの実測ではなく、速度はGPU・Attention実装・設定に依存する。必要なAnima一式のモデルダウンロード容量も別途確保する必要がある。

## 出典

- [対象X投稿](https://x.com/malariadx/status/2116141819159249040)
- [Anima Ref Adapter v2（Hugging Face・作者の仕様と計測）](https://huggingface.co/ElectronGirl/anima-ref-adapter)
- [ComfyUIカスタムノード（GitHub）](https://github.com/ElectronGirl/ComfyUI-Anima-Ref-Adapter)
- [PPMによる互換実装（GitHub）](https://github.com/pamparamm/ComfyUI-ppm)

## 取得状況と制約

対象X投稿は以前にブラウザで確認した内容を使用し、仕様・重み・速度は作者のHugging Face公開説明で照合した。今回、Xtracticle経由の再取得は完了していない。速度値は作者の計測であり、独立ベンチマークではない。
