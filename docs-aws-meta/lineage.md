# 出典と版（リネージュ）

## 作成の経緯

この資料は 2026-10-09 に、AWS 講習会の既存手順・CLI 実装と 2026-10-08〜09 の実測記録を基に作成した。資料作成時に AWS 操作・EC2 の起動は行っていない。追加した「LeRobot 実習と AWS 連携の進め方」では従来の LeRobot 資料を統合し、公式の v0.6.0 の学習設定・推論 CLI も照合した。

## 元資料の版

元資料は `GClueDev/ai-learning-handson-aws-infra` の、検証当時のブランチ `feature/20261008_docs_updates`、参照時コミット `ccfd1a3` である。当時は未マージの検証版を参照した。2026-10-09 に手元の運用リポジトリの `main` へこのコミットが取り込まれていることを履歴で確認した。取り込みは、後続版で AWS・EC2 の通し手順を再検証したことを意味しない。採用版は構築担当と確認し、差分と CLI の契約を点検する。以下は元リポジトリ内のパスで、ローカルの絶対パスには依存しない。

受講者向けの元資料と、その反映先は次のとおり。

- `docs/procedures/attendee.md`: 導入、認証更新、接続、Git、教材取得、保存、片付けの手順を再構成。
- `src/handson_tools/assets/attendee/bin/gclue-ai-handson-attendee`: サブコマンド、依存、環境とライブラリの契約を照合。
- `src/handson_tools/assets/attendee/lib/gclue-ai-handson/files.sh`: pull/upload の引数、S3 バケットパス、フォルダ名、SHA 検証範囲を照合。
- `agent-work/handoff.md`（末尾 7〜9）: Git 修正の配布状況、EC2 実測、未完了工程を反映。
- `agent-work/research/lerobot-training-dependencies.md`（末尾実測追記）: 固定環境、LFS 復旧、Rerun と info の確認結果を反映。

`agent-work` の資料は元リポジトリでは Git 管理外の検証メモである。本資料へ認証情報や期限付き URL、アカウント固有値を転載していない。受講者ツールや導入スクリプトはこのドキュメントリポジトリに同梱しない。講師が元リポジトリから修正版を配布する必要がある。

## 環境構築担当者向けの出典

インフラリポジトリの `feature/20261008_docs_updates`、`ccfd1a3` の次のファイルを読み、構築手順と仕様を移植・調整した。

- `docs/procedures/environment.md`、`docs/specs/infrastructure.md`、`docs/specs/access-control.md`
- `src/handson_cdk/gclue_ai_handson_cdk/cli.py` と `application.py`（synth / diff / deploy `--approve` / destroy `--confirm-destroy` の契約）
- `scripts/setup-lerobot-ec2.sh`

実測の正本は元リポジトリの Git 管理外の `agent-work/handoff.md` 末尾、`agent-work/research/lerobot-training-dependencies.md` 追補、`config/environments/p1test/verification-20261008-continuation.md` と `ec2-environment-20261009/inventory.txt` である。実値を含む原文は転載せず、結果を一般化している。

## 講師向けの出典

運用リポジトリ名は `ai-learning-handson-aws-infra`、参照ブランチは `feature/20261008_docs_updates`、コミットは `ccfd1a3` である。講師向けの運用手順は `docs/procedures/instructor.md` を基に補足・再構成した。

- `docs/procedures/instructor.md`、`attendee.md`、`environment.md`、`timeline.md`: 運用順序と役割。
- `docs/specs/access-control.md`、`releases.md`: 認証・配布の契約。
- `src/handson_tools/gclue_ai_handson/commands/credentials.py`、`release.py`、`rollout.py`: オプションと成功メッセージ。
- `src/handson_tools/assets/attendee/lib/gclue-ai-handson/files.sh`: 保存と取得のパス。
- `agent-work/handoff.md` の 7〜9 節、`agent-work/todo.md`、開催別 `timeline.md`、`verification-20261008-continuation.md`、`ec2-environment-20261009/inventory.txt`: 実測範囲（Git 管理外の記録は構築担当が管理）。

原典の確認例（運用リポジトリ内、読み取り専用）:

```bash
git show ccfd1a3:docs/procedures/instructor.md
git show \
  ccfd1a3:src/handson_tools/gclue_ai_handson/commands/credentials.py
```

## コンソール制御の実装参照

受講者コンソール制御の実装参照は `GClueDev/ai-learning-handson-aws-infra` の `feature/20261008_docs_updates`、コミット `e1415f2b1daf5ad503e69a97698c9282b3f1903a` である。過去の接続実測の出典とは別に、開催 YAML 契約・IAM 拒否・払い出し前確認・配布フラグを照合している。実 AWS での適用は本資料作成時に未実施である。

## 同梱スクリプトの契約

同梱の `setup-lerobot-ec2.sh` は、上記 `ccfd1a3` の実ファイルを基に掲載している。`--cache-resnet18` の用途が伝わるようヘルプの説明文を更新し、実行処理は維持している。Ubuntu 24.04 x86_64 の `ubuntu` ユーザー向けで、sudo とインターネット接続が必要である。OS パッケージ、uv、AWS CLI、LeRobot の固定版を導入する。既存版や Git SHA、追跡ファイルの変更が合わない場合は停止する。

NVIDIA ドライバー、SSM Agent、SSH、Amazon DCV の導入、AWS リソース作成、認証情報の払出し、データセット取得、学習は行わない。元の検証では構文、ヘルプ、隔離 mock 14 ケースが成功している。スクリプト全体の EC2 実行は未検証で、手動で同じ依存が導入できたことは、一括実行成功の証明ではない。インスタンスストア NVMe の利用は将来の検討項目で、自動フォーマットは行わない。

## ローカル検証の記録

2026-10-09、元の独立した環境構築担当ガイドで、固定依存（MkDocs 1.6.1 / Material 9.7.6）で `mkdocs build --strict -f mkdocs.aws-environment.yml` を実行し成功した。内部ファイルリンクとアンカーの警告をエラーとして扱っている。外部サイトの疎通や AWS 上の再実行は含まない。

当初の転載時には、同梱スクリプトの `bash -n` と `--help` が成功し、元コミットのファイルとバイト単位で一致した。当時の SHA-256 は `ba927d6bbb3cffe7d8475a3d254e6262656ba48de236c713df9af18e2e6f5190` である。14 mock ケースは元リポジトリの検証記録で、この資料の作成時には再実行していない。その後、`--cache-resnet18` のヘルプを画像特徴抽出用 ResNet18 の事前学習済み重みの取得と明記した。更新後の現行ファイルは、上の当初の照合値とは異なる。構文・ヘルプと、ヘルプ以外の実行処理の一致を再確認している。EC2 上での導入・GPU 計算・重みの取得は、この文言変更時にも実行していない。

## 部分ファイルの版

`guide-includes/sources.json` に、元資料の版と部分ファイルの一覧を記録している。他の作業コピーからの自動同期は行わない。
