# AWS へのデータ転送

手元で収集したデータを、自分専用の S3 領域を経由して EC2 へ渡します。[データセットの収集](lerobot/collect.md)の後、[データセットの編集](lerobot/edit.md)または [学習](lerobot/train.md)の前に行う AWS 連携の工程です。

## 1. 収集したデータを自分用の S3 領域へ送る

実行場所: **手元の Jetson／Mac**。受講者ツールを有効にしたターミナルで実行します。S3 の `shared/` は共有教材用です。自分の収集データは自分専用の領域へ保存します。

`LOCAL_DATASET_DIR`は[接続の確認](lerobot/check.md)で決めた手元の収集先です。収集中は転送せず、記録が終了してからフォルダ内のファイルをそのまま送ります。

```bash
test -f "$LOCAL_DATASET_DIR/meta/info.json" &&
  gclue-ai-handson-attendee files upload \
    "$LOCAL_DATASET_DIR" --to datasets
```

フォルダを送ると、元のフォルダ名も保存先に付きます。この手順の収集先の名前は `round1` なので、自分専用の `datasets/round1/` に保存されます。アップロードが成功したことを確認してください。`.DS_Store` はMacの表示用ファイルなので転送対象から除かれます。

新しい収集分では未使用のフォルダ名（例えば `round2`）を使い、次の取得側の `round1` も同じ名前へ揃えます。保存中は収集データを編集・追加しません。

## 2. EC2 へ取得し、データと映像を確認する

実行場所: **手元の PC**。初回は [接続手順](connect.md)で DCV のパスワードを設定します。

```bash
gclue-ai-handson-attendee dcv
```

トンネル用のターミナルは開いたまま、案内された URL から DCV にログインします。DCV デスクトップ内で Terminal を開き、以降の EC2 工程はそこで実行します。

実行場所: **EC2 の Ubuntu**。講師が LeRobot と受講者用の一時認証情報を配置済みであることが前提です。

```bash
whoami
cd ~/lerobot
uv run --no-sync python --version
uv run --no-sync lerobot-train --help
source /tmp/gclue-ai-handson-{{EVENT_ID}}-{{ATTENDEE_ID}}.env
DATASET_DIR={{DATASET_DIR_SH}}
S3_ROOT="s3://$GCLUE_AI_HANDSON_BUCKET"
S3_ROOT+="/$GCLUE_AI_HANDSON_ATTENDEE"
```

`DATASET_DIR`は右上の「各種値の設定」で入力したEC2側の保存先を、このターミナルで取得に使うために覚える変数です。情報確認の識別名も、同じ設定からコマンドへ反映されます。自分の収集データを取得する場合、例えば `/home/ubuntu/handson-data/workshop01/attendee01/round1` のような未使用のフォルダを講師と確認します。配布データの場合は、講師が既に置いた場所を指定します。

`source` は講師がEC2に配置した認証情報ファイルをこのターミナルへ読み込む操作です。ファイル内の `GCLUE_AI_HANDSON_BUCKET` はS3バケット名、`GCLUE_AI_HANDSON_ATTENDEE` は自分の受講者IDで、自分で作る値ではありません。`S3_ROOT`はこの2つから作る自分専用の保存先です。説明用の値なら `s3://example-handson-workshop01/attendee01` となります。

`whoami` が `ubuntu` であることを確認します。認証情報がない・期限切れの場合は講師に再配布を依頼します。EC2 上で依存を追加・更新せず、環境の不足は講師に確認します。

この工程は自分で収集したデータの取得です。講師の配置済み教材を使う場合は[教材とデータ確認](dataset.md)へ進みます。

**まだ存在しない取得先**へ各ファイルをコピーし、データセットの情報ファイルがあることを確認します。

```bash
(
  set -e
  test ! -e "$DATASET_DIR" || {
    echo '取得先が存在します。別のパスを指定してください。' >&2
    exit 1
  }
  mkdir -p "$DATASET_DIR"
  aws s3 cp "$S3_ROOT/datasets/round1/" \
    "$DATASET_DIR/" --recursive
  cd "$DATASET_DIR"
  test -f meta/info.json
)
```

転送がエラーなく終了し、`meta/info.json` の存在確認も成功したら、次の情報・映像確認へ進みます。不足や表示エラーがあれば講師へ相談します。取得が途中で失敗した場合は、部分的なデータが残ることがあるため、別の未使用の取得先を設定してやり直します。

## 3. 情報と映像を確認する

```bash
uv run --no-sync lerobot-edit-dataset \
  --repo_id {{DATASET_REPO_ID_SH}} \
  --root {{DATASET_DIR_SH}} \
  --operation.type info
```

エピソード数、フレーム数、FPS、タスクと、`front`・`side` の2台の映像を収集時の記録と照合します。DCV の Terminal では、次で Rerun を表示します。

```bash
uv run --no-sync rerun {{DATASET_DIR_SH}}
```

失敗したエピソード番号を控えます。配布データが Git LFS のポインタのままの場合は、[Git LFS の復旧](reference/data.md#git-lfs)を使います。


---

[前へ: データセットの収集](lerobot/collect.md) · [次へ: データセットの編集](lerobot/edit.md)

{% if audience == "staff" %}

## 講師：AWSへの転送の到達確認

本人のS3 バケットパス・EC2を確認し、転送結果と取得先、情報表示と映像確認を記録します。認証切れは再発行してPCとEC2それぞれで読み込み直します。

{% endif %}
