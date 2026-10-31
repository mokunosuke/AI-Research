# LoRA調査レポート — 2026-10-31

調査日: 2026-10-31（JST）  
対象: 複数キャラクターの混線・一貫性、ComfyUI/Forge、RTX 3060 12GB  
前回比較: `Reports` にLoRAレポートが見当たらないため、今回は比較基準となる初回記録。

## 今週の重要トピック

- **ComfyUIでキャラクターごとにLoRAを割り当てる地域サンプラーが公開・更新されています。** RS MultiCharacter Samplerは、位置・矩形・マスクで最大10領域を定義し、各キャラクターに別のプロンプトとLoRAを割り当てます。SDXL/Illustrious用ワークフローも掲載され、通常のグローバルLoRAとの併用もできます。[GitHub](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)
- **SDXLの検証手順を公開した小規模な評価リポジトリも確認できました。** 12枚の学習画像を使った単一キャラクター実験では、同じ説明文にLoRAを足した条件で顔認識の一貫性指標が上がりました。一方、6枚ずつの比較など規模は小さく、著者自身が差のノイズ幅や指標の限界を明記しています。[GitHub](https://github.com/Colin-J-Emmanuel/character-consistency-lora)
- **ComfyUI以外への適用はモデル系列ごとです。** Krea 2/Klein用のリージョナルLoRA実装がForge Neo向けにも公開されていますが、これはSDXL向け機能の移植ではありません。SDXL/Forgeの既存構成にそのまま使えると解釈しないでください。[GitHub](https://github.com/Adeliox/krea-multi-lora)

## 混線防止関連アップデート

### 新規情報 — RS MultiCharacter Sampler

この拡張は、共通シーン説明と各キャラクターの説明・LoRA・位置情報を分ける構成です。SDXL/Illustriousの二人用ワークフローが案内され、LoRAとCLIPの強度を人物単位で設定できます。OpenPoseから近似マスクを作る機能、人物別のDetailerもあります。[SDXL/Illustriousワークフローと対応範囲](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)

**実用上の評価:** 既存のSDXLキャラクターLoRAを使い、キャラクター同士の位置・属性の混線を軽減する選択肢になります。作者資料でも、人物数・属性の分離・ポーズはモデル依存で、密なレイアウトや交差する小物では人物の重複・欠落・属性混合が起こり得るとされています。設定だけで混線が解消する保証はありません。

### 更新情報 — LoRA効果を測る小規模SDXL実験

公開評価では、同一のシーン・seed・sampler等を使い、テキストのみ、トリガー語+LoRA、説明文+LoRAを比較。説明文+LoRAの顔類似度は、テキストのみより3条件で0.15〜0.26高くなったと報告されています。ただし、6画像での比較が中心で、著者は一部の差がサンプル数のノイズ範囲にあること、シーン編集性を測るCLIP指標の限界を述べています。一般的な性能保証や、多人数の混線評価ではありません。[評価条件・全結果](https://github.com/Colin-J-Emmanuel/character-consistency-lora/blob/main/RESULTS.md)

## ComfyUI関連

### RTX 3060 12GBで試す場合

- **第一候補:** SDXL/Illustriousの同梱二人用ワークフローから始め、モデル・VAE・プロンプト・seedを固定して通常のグローバルLoRA構成と比較します。
- **配置:** 最初は二領域（左右など）に限定し、人物の境界とプロンプトの担当範囲を明確にします。必要に応じてOpenPoseマスクまたは手動マスクを追加します。
- **強度:** LoRA強度の万能値は確認できません。作者の対応表に従い低めから調整し、人物の特徴が弱ければ段階的に上げます。異なる作者のLoRAを同時に強くすると品質が揺れる可能性があります。
- **VRAM・速度:** RTX 3060 12GBでこの拡張を使った独立ベンチマークは確認できませんでした。人物ごとの別LoRA予測やDetailerは追加計算・メモリを使うため、まず低解像度・少ないステップ・二人で動作を確認し、段階的に増やしてください。
- **制限:** 共通ネガティブプロンプトは人物別ではなく、人物別の予定付きテキスト条件にも対応しません。SD2、inpainting/refiner、FLUX Fill/Control、外部ControlNet/attention patchなど、未対応の組み合わせがあります。利用前に対応表を確認してください。

## Flux・Forge関連

- **Forge Neo:** [krea-multi-lora](https://github.com/Adeliox/krea-multi-lora) はKrea 2/Kleinの複数LoRAを領域別に適用する実装です。SDXLモデル向けではなく、Forge Neoとの互換性も対象リポジトリのモデル・バージョン範囲に限られます。
- **Flux:** 今回の調査で、RTX 3060上で再現可能なFlux向け混線防止策の新規一次情報は確認できませんでした。リージョナルLoRA機能はモデル系列ごとに動作方式・対応形式が異なるため、SDXLの設定値を流用しないでください。
- **Forge通常版:** 今回、SDXLの人物別LoRA適用を確認できる新しいForge標準機能は見つかりませんでした。

## Civitai・Hugging Face・X・コミュニティ

- GitHubで上述の拡張・実験を確認しました。
- Hugging Face Papersの既存研究は調査しましたが、今週のSDXL実運用で新たに採用できる公式実装・重みは特定できませんでした。
- Civitai検索では、今回のテーマに関して比較可能な新規モデルや検証データを一次資料と照合できませんでした。
- X投稿は検索結果から対象投稿を特定できず、投稿者名や似た話題から内容を推測していません。
- ComfyUIコミュニティの実利用情報は、該当プロジェクトの説明・制限事項を確認する補足として扱いました。

## RTX3060 12GB評価

| 項目 | 評価 |
|---|---|
| VRAM | 2人・SDXLの通常サイズから試す。人物数やDetailerを増やすほど負荷上昇が予想されるが、当該拡張の3060実測値は未確認。 |
| 推奨設定 | 同梱ワークフロー、二領域、seed固定、低めの解像度から開始。まずLoRA強度と領域位置を個別に調整。 |
| 速度 | 人物ごとに予測を分ける処理があるため単一LoRAより遅くなり得る。具体的な速度倍率は未確認。 |
| ComfyUI導入難易度 | 中。ManagerまたはGit導入後、ComfyUIを再起動し、対応モデル・ワークフローを選ぶ。 |
| Forge導入難易度 | 中〜高。確認された例はForge NeoのKrea 2/Klein向けで、Forge系・モデル系列の条件確認が必須。 |
| 安定性 | 小規模の作者検証とコミュニティ公開例。独立したSDXL/3060ベンチマークは不足。 |

## 次週監視項目

- RS MultiCharacter SamplerのSDXL対応範囲、リリースノート、3060での実測
- 地域ごとのLoRA強度、OpenPoseマスク、Detailerの組み合わせによる人物混線の評価
- Forge NeoのKrea 2/Klein向け地域LoRAの更新と、通常Forge・SDXL対応の有無
- Civitai/Hugging Faceにおける再現可能な多人数LoRA評価や学習データ公開

## 情報源

- [RS MultiCharacter Sampler — GitHub](https://github.com/raspie10032/ComfyUI_RS_MultiCharacter_Sampler)
- [SDXL Character Consistency LoRA — GitHub](https://github.com/Colin-J-Emmanuel/character-consistency-lora)
- [実験結果と評価上の制約 — GitHub](https://github.com/Colin-J-Emmanuel/character-consistency-lora/blob/main/RESULTS.md)
- [Forge Neo Krea Multi-LoRA — GitHub](https://github.com/Adeliox/krea-multi-lora)
- [Area-based LoRA Pipeline — GitHub](https://github.com/andreszs/ComfyUI-Lora-Pipeline)
- [ComfyUI Community / Comfy ICU node listing](https://comfy.icu/node/RSMultiCharacterLoRA)
