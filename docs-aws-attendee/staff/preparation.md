# 講習会側の事前準備

受講者の実習を始める前に、環境構築担当者が環境を構築し、講師が教材を配布します。左の目次の「講習会側の準備」は、担当ごとに「環境構築担当者」と「講師」に分かれています。自分の担当の項目から、工程ごとのページを開けます。

運用・構築コマンドは、**ai-learning-handson-aws-infra** の作業環境で実行します。ai-learning-handson-aws-infra は、講習会の AWS 環境の構築と、教材の配布・認証情報の払出しなどの運用に使うツールをまとめた Git リポジトリです。

このガイドの原稿は、別の Git リポジトリ **LeRobotDocs** にあります。受講者の PC で実行するコマンドや、LeRobotDocs の中で実行するコマンド（ガイドのビルドなど）と区別してください。

## 進める順番

自分の担当に合わせて、読み始めるページを選んでください。

- **環境構築担当者**：1 の[開始条件と道具](preparation/environment-start.md)から始め、11 の[講師への引き渡し](preparation/handoff.md)まで進めます。
- **講師**：1〜11 は環境構築担当者の作業なので、読む必要はありません。環境構築担当者から引き渡しの連絡を受けたら、12 の[講師の準備](preparation/instructor-start.md)から始めます。

| 順番 | 工程 | 担当 |
| --- | --- | --- |
| 1 | [開始条件と道具](preparation/environment-start.md) | 環境構築担当者 |
| 2 | [開催設定とAMIの選定](preparation/event-settings.md) | 環境構築担当者 |
| 3 | [導入済みAMIの確認](preparation/ami-find.md) | 環境構築担当者 |
| 4 | [一時インスタンスの起動](preparation/ami-launch.md) | 環境構築担当者 |
| 5 | [ソフトウェアの導入](preparation/ami-software.md) | 環境構築担当者 |
| 6 | [AMIの作成](preparation/ami-create.md) | 環境構築担当者 |
| 7 | [ルートデバイスと配置先](preparation/placement.md) | 環境構築担当者 |
| 8 | [構築前の確認](preparation/validate.md) | 環境構築担当者 |
| 9 | [環境の構築](preparation/deploy.md) | 環境構築担当者 |
| 10 | [構築後の確認](preparation/verify.md) | 環境構築担当者 |
| 11 | [講師への引き渡し](preparation/handoff.md) | 環境構築担当者 |
| 12 | [講師の準備](preparation/instructor-start.md) | 講師 |
| 13 | [教材の公開](preparation/materials.md) | 講師 |
| 14 | [EC2への教材配布](preparation/rollout.md) | 講師 |

導入済みAMIの準備は任意です。利用できるAMIがある場合は、[ルートデバイスと配置先](preparation/placement.md)へ進みます。

教材配布と各受講者の EC2 への受講者ツール導入・本人設定の確認を済ませたら、[受講者のPCの準備](../setup.md)へ進み、以降の共通ページで受講者の操作と担当者の操作を同じ順番で確認します。
