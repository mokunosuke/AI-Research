# 画像生成・ComfyUI関連X投稿レポート

## 概要

- 対象URL: Pushbulletで2026-11-01（日本時間）に受信したX投稿4件
- 調査日: 2026-11-02（日本時間）
- 全体の要点: MOSS-Imageの高速生成・編集アダプター、参照素材ライブラリ、MiniMax H3向けComfyUI補助ノードを扱う投稿です。投稿者の説明と、配布元が示す機能・制約を区別してまとめます。

## 記事・投稿ごとの要約

### 1. CottonMoss: MOSS-Imageベースのマージモデル

- Pushbullet受信: 2026-11-01 12:17 JST
- Xtracticle投稿日時: 2026-11-01 10:12 JST (01:12 UTC)
- 元投稿: [R@aiaicreateの投稿](https://x.com/aiaicreate/status/2116699897462452332)
- Xtracticle本文: [R@aiaicreateの投稿本文](https://xtracticle.com/aiaicreate/status/2116699897462452332/)
- モデル: [CottonMoss（Civitai）](https://civitai.com/models/3026318)

**投稿の内容:** MOSS-Image-Baseへ複数のLoRA（8ステップ化用など）を控えめな強度で統合した実験的マージモデルとして紹介。投稿者は12ステップ、er_sde sampler、CFG 3を推奨し、マージの影響でプロンプト追従やキャラクター再現が不安定になる場合があると注意しています。

**背景・確認:** CottonMossは公式MOSS-Imageそのものではなく、コミュニティによる派生マージです。OpenMOSSの[公式MOSS-Image説明](https://openmoss.ai/MOSS-Image/)は、公開モデルをテキストから画像を生成するモデルとして説明しています。既存画像編集の機能を公式ベースモデルの標準機能として混同しないよう注意が必要です。

**実用上の示唆:** 投稿の設定値は試行開始点として扱い、同一プロンプト・seedで比較してください。キャラクター一貫性やプロンプト追従性を重視する用途では、投稿者自身が述べる不安定さを考慮し、まず少数のテスト生成で確認するのがよさそうです。推奨設定の独立再現は確認できていません。

### 2. MOSS-Imageの2ステップ生成・編集アダプター

- Pushbullet受信: 2026-11-01 12:15 JST
- Xtracticle投稿日時: 2026-11-01 04:48 JST (2026-10-31 19:48 UTC)
- 元投稿: [AI Searchの投稿](https://x.com/aisearchio/status/2116618294090437055)
- Xtracticle本文: [AI Searchの投稿本文](https://xtracticle.com/aisearchio/status/2116618294090437055/)
- 関連アダプター: [MOSS-Image-IDM-2-Steps（Hugging Face）](https://huggingface.co/akhaliq/MOSS-Image-IDM-2-Steps)

**投稿の内容:** MOSSで画像生成と編集を1つのモデルで行え、2ステップで数秒生成できると紹介しています。

**背景・一次情報による確認:** アダプターのモデルカードは、2ステップを主に高速な画像生成用として説明し、編集は実験的としています。編集の比較では、CFG 2で表情や色味などの属性変更は機能する一方、スケッチから写真への変更や白黒画像の着色など構造的な編集は2ステップではうまくいかず、50ステップの編集経路を推奨しています。OpenMOSSの[公式説明](https://openmoss.ai/MOSS-Image/)ではベースモデルはテキストからの画像生成モデルです。したがって「2ステップで生成も編集もできる」は編集の種類・設定に条件がある要約です。

**実用上の示唆:** 2ステップは高速な生成や簡単な属性変更の下書き向けとして評価し、形状・構造を保った編集にはモデルカードの高ステップ手順と比較してください。「数秒」は環境依存で、投稿には測定環境・解像度が示されていません。

### 3. ポーズ・衣装・顔の参照ライブラリ

- Pushbullet受信: 2026-11-01 12:04 JST
- Xtracticle投稿日時: 2026-10-31 23:57 JST (14:57 UTC)
- 元投稿: [Alizehの投稿](https://x.com/alizeh_ai/status/2116545079733325935)
- Xtracticle本文: [Alizehの投稿本文](https://xtracticle.com/alizeh_ai/status/2116545079733325935/)
- リポジトリ: [anhao/ai-pose-gallery-zh（GitHub）](https://github.com/anhao/ai-pose-gallery-zh)

**投稿の内容:** 無料・オープンソースの参照素材ライブラリとして、ポーズスケッチ1,439点、衣装1,407点、顔参照1,499点を挙げ、ComfyUIノードと素材を組み合わせるスタジオも紹介しています。

**背景・一次情報による確認:** GitHubのREADMEは、ポーズ1,439点、衣装1,407点、人物参照1,499点の各ライブラリを説明しています。ポーズは複数角度の参照画像、衣装・顔画像も別の素材集として整理されています。READMEの記載と投稿の件数は一致します。画像素材の利用条件・再配布条件はソースごとに異なるため、素材利用時はリポジトリおよび各素材サイトの最新条件を確認してください。

**実用上の示唆:** ポーズ、衣装、顔の参照を分けて探せるため、画像生成時の参照選びやキャラクター案の比較に使えます。ただし参照を与えても、生成結果の構図・衣装・人物の一貫性が保証されるわけではありません。ComfyUI連携やスタジオの動作条件はREADMEに沿って確認してください。

**引用投稿との区別:** Xtracticleには、Flintという別のロールプレイ用モデルに関する引用投稿も含まれていました。拒否率の数値は引用元の投稿者による主張で、ポーズ素材ライブラリの機能とは別の話題のため、本レポートの評価対象には含めていません（[引用投稿](https://x.com/alizeh_ai/status/2116463699171127375)、[モデルカード](https://huggingface.co/mradermacher/flint-roleplay-antislop-heretic-GGUF)）。

### 4. MiniMax H3 Character Sheet Designer for ComfyUI

- Pushbullet受信: 2026-11-01 12:02 JST
- Xtracticle投稿日時: 2026-10-31 19:38 JST (10:38 UTC)
- 元投稿: [dextuneの投稿](https://x.com/dextune/status/2116479903575245228)
- Xtracticle本文: [dextuneの投稿本文](https://xtracticle.com/dextune/status/2116479903575245228/)
- 実装: [H3-Character-Sheet-Designer（GitHub）](https://github.com/ukr8b3g-cmyk/H3-Character-Sheet-Designer)

**投稿の内容:** 「H3 Character Sheet Designer」について、13種類のビューを選べるキャラクターシート設計ノードとして紹介。1枚のキャラクター画像と最大3枚の任意参照画像を受け取り、顔・頭・服・手・靴など参照の役割を指定します。投稿にはv1.2.2でJSON適用後の古いパーツプロンプトを修正し、既存ノードIDとワークフローは変わらないとあります。

**背景・一次情報による確認:** GitHubの[プロジェクト説明](https://github.com/ukr8b3g-cmyk/H3-Character-Sheet-Designer)も、ComfyUI用のキャラクターシート設計・プロンプト生成ノードと説明しています。ノードがプロンプトや出力寸法を組み立て、実際の画像／動画生成はMiniMax H3側のワークフローで行います。参照画像に基づく外観や各パネルの正確さは保証されず、作者もビュー構成や衣装の表現に制約があると記載しています。

**実用上の示唆:** 既存キャラクターから複数ビューのシートを作る際の指示作成補助として使えます。ノードの導入に加え、対応するComfyUI環境とH3モデル／生成ワークフローが必要です。導入前にREADMEのバージョン要件とライセンス、既存ワークフローへの影響を確認してください。

## 横断的な整理

4件はいずれも画像生成の制作補助を扱い、モデル本体、コミュニティ派生物、参照素材、ComfyUIノードという異なる層の情報が混在しています。特にMOSS-Imageは、公式ベースモデルの機能とコミュニティ製の編集・高速化アダプターを分けて理解する必要があります。「数秒で生成できる」という速度の説明は投稿者の紹介であり、同じ条件での第三者比較は確認できていません。CottonMossの投稿自体も、マージ後のプロンプト追従性とキャラクター再現に課題があるとしています。使う場合は、モデル／ノードの配布元が示す要件とライセンスを確認し、小さなテストで出力を評価してください。

## 取得できなかった情報

4件のX投稿本文とスレッドを、XtracticleのMarkdown API（x.comからxtracticle.comへのホスト置換で利用）で取得しました。aiaicreate投稿は2件のスレッドで、返信にCivitaiのCottonMossモデルページがありました。Xtracticleが返した投稿日時はUTC表記のため、JSTに換算しています。投稿本文・配布元の説明以上に独立して再現された性能検証は確認できていません。

## 出典

- [R@aiaicreateのX投稿](https://x.com/aiaicreate/status/2116699897462452332) / [CottonMoss（Civitai）](https://civitai.com/models/3026318) / [OpenMOSS公式MOSS-Image](https://openmoss.ai/MOSS-Image/)
- [AI SearchのX投稿](https://x.com/aisearchio/status/2116618294090437055) / [MOSS-Image-IDM-2-Steps（Hugging Face）](https://huggingface.co/akhaliq/MOSS-Image-IDM-2-Steps)
- [AlizehのX投稿](https://x.com/alizeh_ai/status/2116545079733325935) / [ai-pose-gallery-zh（GitHub）](https://github.com/anhao/ai-pose-gallery-zh)
- [dextuneのX投稿](https://x.com/dextune/status/2116479903575245228) / [H3-Character-Sheet-Designer（GitHub）](https://github.com/ukr8b3g-cmyk/H3-Character-Sheet-Designer)






