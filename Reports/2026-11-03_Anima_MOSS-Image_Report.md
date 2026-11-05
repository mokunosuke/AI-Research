# Anima地域編集とMOSS-Image更新レポート

- 調査日: 2026-11-03（JST）
- 対象: Pushbulletで2026-11-02（JST）に受信したXリンク2件
- 差分基準: `Reports/2026-11-02_画像生成_ComfyUI_Report.md`

## 概要

今回の2件は、ComfyUIでAnimaの地域別プロンプトを扱うLuCiD VRPと、MOSS-Imageの公開カタログ／補助LoRAのまとめです。前回レポートで扱ったMOSS-Image 2ステップアダプター自体は継続情報です。今回の差分は、検索可能なスタイルカタログ、Detailer・スタイルLoRAの紹介、およびAnima向け編集UIです。

## 投稿ごとの要約

### 1. LuCiD VRPでAnimaの地域別プロンプトを試す

- Pushbullet受信: 2026-11-02 00:45 JST
- Xtracticle投稿日時: 2026-11-01 23:30 JST（UTC 14:30）
- [元投稿](https://x.com/malariadx/status/2116900569285554563) · [Xtracticle本文](https://xtracticle.com/malariadx/status/2116900569285554563/)
- [comfyui-lucid-vrp（GitHub）](https://github.com/EBEBEEBE/comfyui-lucid-vrp)

**投稿の内容:** 投稿者はLuCiD VRPを試し、Anima向けワークフローでT2Iのキャラクター配置を行ったと紹介しています。

**一次情報による確認:** GitHubの説明では、LuCiD VRPはComfyUI上で画像読込、レイヤー編集、Anima地域別プロンプト、MOSS-Imageレイアウトプロンプトをまとめる視覚編集インターフェースです。画像または空キャンバスから編集を始められるとされています。投稿例は実作例ですが、SDXL用LoRAの混線が解消することや、特定GPUでの速度・VRAMを示すベンチマークではありません。

**差分と実用上の示唆:** 前回のMOSS-Image／参照素材の話題に対して、今回は領域やレイヤーを視覚的に編集するComfyUI上の別アプローチが加わりました。Anima用の機能として紹介されているため、SDXLやForgeにそのまま適用できるとはみなせません。RTX 3060 12GBでの実測、必要モデル、導入時の詳細条件は今回確認できず、まずリポジトリの現行READMEとワークフローを確認して小規模に試す段階です。

### 2. MOSS-Imageのスタイルカタログと補助LoRA

- Pushbullet受信: 2026-11-02 00:33 JST
- Xtracticle投稿日時: 2026-11-01 15:29 JST（UTC 06:29）
- [元投稿](https://x.com/mapte_fireball/status/2116779613787725909) · [Xtracticle本文・スレッド](https://xtracticle.com/mapte_fireball/status/2116779613787725909/)
- [投稿が参照するRedditまとめ](https://www.reddit.com/r/comfyui/comments/1xkuwhl/a_quick_mossimage_news_roundup_1st_november_2026/)
- [MOSS-Image Character Catalog（Hugging Face Spaces）](https://huggingface.co/spaces/hide1/MOSS-Image-Character-Catalog)
- [2-step adapter（Hugging Face）](https://huggingface.co/akhaliq/MOSS-Image-IDM-2-Steps)

**投稿の内容:** 11月1日のまとめとして、検索可能な314スタイルのカタログと作例、Detailer、複数のスタイルLoRA、および2ステップ生成アダプターを紹介しています。

**差分:** 前回の2026-11-02画像生成レポートは2-step adapterと編集上の制限をすでに扱いました。したがって今回それを新機能として数え直しません。新しく加わる話題は、314スタイルを検索できるカタログ、Detailerとスタイル別配布物の案内です。Redditまとめはコミュニティ投稿で、カタログや配布ページはそれぞれのホスト上で公開状況を確認できます。

**一次情報・制約:** モデルカードでは2-step版は高速T2I向けで、属性変更を超える編集は実験的とされています。また、専用ローダーとbf16 SFT系の前提が示されており、標準ノードだけで同じ動作になるとは限りません。カタログはスタイル選択と作例探索を助けますが、出力品質やスタイル再現を保証しません。RTX 3060での生成速度・VRAMの比較測定は確認できませんでした。

**実用上の示唆:** カタログで候補スタイルとプロンプトを探し、利用する配布物のモデル系列・ライセンス・ローダー要件を個別に確認してください。2-step adapterの速度と編集品質の評価は前回レポートの結論を維持します。

## 横断的な整理

今回の新規性は「制作UI・素材探索の選択肢が増えた」点です。LuCiD VRPはAnimaなどの地域編集ワークフロー、MOSSカタログはスタイル探索を支援します。どちらもSDXL LoRAの混線防止策や、3060での定量性能を実証する資料ではありません。

## 取得できなかった情報

2件のX投稿本文・スレッドはXtracticle経由で確認しました。LuCiD VRPのRTX 3060実測値、カタログ収録物すべてのライセンス、2-step配布物の独立ベンチマークは確認できませんでした。

## 出典

- [MalariaDxのX投稿](https://x.com/malariadx/status/2116900569285554563) · [LuCiD VRP GitHub](https://github.com/EBEBEEBE/comfyui-lucid-vrp)
- [mapte_fireballのX投稿](https://x.com/mapte_fireball/status/2116779613787725909) · [Redditまとめ](https://www.reddit.com/r/comfyui/comments/1xkuwhl/a_quick_mossimage_news_roundup_1st_november_2026/)
- [MOSS-Image Character Catalog](https://huggingface.co/spaces/hide1/MOSS-Image-Character-Catalog)
- [MOSS-Image-IDM-2-Steps model card](https://huggingface.co/akhaliq/MOSS-Image-IDM-2-Steps)
- [MOSS-Image Detailer](https://civitai.com/models/3028777/moss-detailer)
- [Double Exposure Style LoRA](https://civitai.com/models/3028673/double-exposure-style-moss) · [Isometric Diorama Style LoRA](https://civitai.com/models/3028647/isometric-diorama-style-moss) · [Male Flat-top Hair LoRA](https://civitai.com/models/3030664/male-flat-top-hair-moss)
