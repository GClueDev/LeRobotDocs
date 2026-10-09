# 出典と検証範囲

この資料は 2026-10-09 に、AWS 講習会の既存手順・CLI 実装と 2026-10-08〜09 の実測記録を基に作成しました。資料作成時に AWS 操作・EC2 の起動は行っていません。AWS の基本手順は下記の固定した実装・記録に基づきます。追加した [LeRobot 実習と AWS 連携の進め方](aws-workflow.md)では従来の LeRobot 資料を統合し、公式の v0.6.0 の学習設定・推論 CLI も照合しました。

## 出典と版の確認 {#source-version}

元資料は `GClueDev/ai-learning-handson-aws-infra` の、検証当時のブランチ `feature/20261008_docs_updates`、参照時コミット `ccfd1a3` です。当時は未マージの検証版を参照しました。2026-10-09 に手元の運用リポジトリの `main` へこのコミットが取り込まれていることを履歴で確認しています。取り込みは、後続版で AWS・EC2 の通し手順を再検証したことを意味しません。採用版は構築担当と確認し、差分と CLI の契約を点検してください。以下は元リポジトリ内のパスです。ローカルの絶対パスには依存しません。

| 元資料 | この資料への反映 |
| --- | --- |
| `docs/procedures/attendee.md` | 導入、認証更新、接続、Git、教材取得、保存、片付けの手順を再構成 |
| `src/handson_tools/assets/attendee/bin/gclue-ai-handson-attendee` | サブコマンド、依存、環境とライブラリの契約を照合 |
| `src/handson_tools/assets/attendee/lib/gclue-ai-handson/files.sh` | pull/upload の引数、S3 バケットパス、フォルダ名、SHA 検証範囲を照合 |
| `agent-work/handoff.md`（末尾 7〜9） | Git 修正の配布状況、EC2 実測、未完了工程を反映 |
| `agent-work/research/lerobot-training-dependencies.md`（末尾実測追記） | 固定環境、LFS 復旧、Rerun と info の確認結果を反映 |

`agent-work` の資料は元リポジトリでは Git 管理外の検証メモです。本資料へ認証情報や期限付き URL、アカウント固有値を転載していません。受講者ツールや導入スクリプトはこのドキュメントリポジトリに同梱しません。講師が元リポジトリから修正版を配布する必要があります。

## 実測と未検証の境界

| 項目 | 状態・範囲 |
| --- | --- |
| Mac の導入・認証情報更新 | 実測済み |
| SSM のシェル接続、SSH、Amazon DCV（リモートデスクトップ接続）、ssh-config | 実測済み。VS Code アプリでの接続操作は今回の実測対象外 |
| Git push → EC2 コミット → pull | 修正ライブラリを指定して実測済み。未コミットファイルは送られない |
| macOS Bash 3.2 / C.UTF-8 の修正 | `fc6e58d` に修正済み。旧配布版の更新は未実施。新しい配布版のローカルビルド・dry-run と実際の公開は別工程 |
| 現行教材の files pull と SHA 検証 | 実測済み |
| 手元 / EC2 → S3 → 手元への保存・再取得 | 小さな検証ファイルの内容一致を実測済み。最終成果全件の回収は未実施 |
{% if attendee_console_access %}| フェデレーションコンソール | EC2 / Systems Manager（SSM：接続・操作の管理）の表示成功。S3 の自分の領域 / shared の直 URL 表示成功 |{% else %}| フェデレーションコンソール（過去の記録） | このビルドの受講者手順には含めません。 |{% endif %}
{% if attendee_console_access %}| S3 コンソールで取得・書込・削除 | 未検証。バケット一覧権限は付与されていない |{% else %}| S3 コンソールで取得・書込・削除（過去の記録） | このビルドの受講者手順には含めません。 |{% endif %}
| LeRobot 依存導入 | `uv sync --locked --extra training --extra dataset_viz --python 3.12` が成功 |
| Rerun 表示 | aloha の Git LFS 実体化後、および実績データ `1cam_test` で成功。pusht の表示は未確認 |
| データ情報表示 | `lerobot-edit-dataset --operation.type info` が成功 |
| GPU 学習、ResNet18 事前取得、変更編集 | 未検証 |
| 統合手順の収集 → S3 転送 → EC2 学習 → モデル回収 → 実機推論 | 文書・構文確認。現行手順は PC・EC2 とも受講者ツールの `files upload/pull` を使用し、無圧縮ファイル転送後にデータの情報・映像、モデルの設定ファイル・モデルファイルを確認する。実装を使ったローカル模擬で upload/pull の保存階層・データとモデルの往復・リンク先の実体化・既存取得先の保護を確認。EC2 へのツール導入、変更後の AWS 転送とロボット実機を含む通し実行は未検証 |
| 講習会側の準備の入力フォーム・コマンド置換 | 準備15ページを点検。コンソール有効・無効の隔離ブラウザで入力同期、ID用途の分離、教材の版変更時のハッシュ消去、JSON受け渡し、コピーを確認。描画された AMI 起動・作成コマンドをローカルの引数記録用 mock で確認。AWS API・構築・デプロイは実行していない |
| 終了時の最終回収・撤去 | 手順・CLI 照合のみ。全体タイムラインの最終工程は未実施 |
| Ubuntu / Jetson / WSL の受講者導入 | 元手順に基づく案内。今回の端末実測は Mac |

## 固定した EC2 環境

| 項目 | 実測値 |
| --- | --- |
| OS / CPU | Ubuntu 24.04 / x86_64 |
| LeRobot | v0.6.0、`30da8e687a6dfc617fcd94afc367ac7071c376ce` |
| Python / uv | 3.12.3 / 0.12.23 |
| torch / torchvision | 2.11.0+cu128 / 0.26.0+cu128 |
| av / torchcodec | 15.1.0 / 0.11.1+cpu |
| rerun-sdk | 0.33.1 |
| AWS CLI | 2.37.10 |

この一覧は最新推奨版の主張ではなく、検証した組合せの記録です。環境構築は講師・構築担当者が行い、受講者は途中で依存を入れ替えません。

{% if audience == "staff" %}

## 講習会側：担当者手順の出典と確認範囲

[講師の検証範囲](staff/instructor/verification.md)と[環境構築担当者の検証範囲](staff/environment/verification.md)も確認します。元資料の実測済み・未実施の区別を維持しています。

{% endif %}
