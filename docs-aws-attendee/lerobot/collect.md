# データセットの収集

実行場所: **手元の Jetson／Mac**。[カメラの調整](camera.md)で設定した `CAMERAS`、`DEVICE`、`DISPLAY_DATA` と、[接続の確認](check.md)で入力した手元の収集先と課題文を使います。USB接続先と識別名は右上の設定からコマンドへ入ります。2台のカメラ名 `front` と `side`、それぞれの位置・解像度・FPS、タスクは収集と推論で合わせます。

## 1. データセット収集（新規）

本収集では30エピソードを記録します。既存の同名データセットを削除せず、`LOCAL_DATASET_DIR` を新しい場所に変えてください。カメラ確認用のテストデータは本収集に混ぜません。

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port={{ROBOT_PORT_SH}} \
  --robot.id=my_follower_arm \
  --teleop.type=so101_leader \
  --teleop.port={{TELEOP_PORT_SH}} \
  --teleop.id=my_leader_arm \
  --robot.cameras="$CAMERAS" \
  --dataset.repo_id={{DATASET_REPO_ID_SH}} \
  --dataset.root={{LOCAL_DATASET_DIR_SH}} \
  --dataset.push_to_hub=false \
  --dataset.single_task={{TASK_SH}} \
  --dataset.fps=30 \
  --dataset.episode_time_s=10 \
  --dataset.reset_time_s=5 \
  --dataset.num_episodes=30 \
  --dataset.streaming_encoding=false \
  --display_data="$DISPLAY_DATA"
```

`episode_time_s` は1エピソードの時間、`reset_time_s` は次のエピソードまでの準備時間です。収集後、[カメラの調整](camera.md)と同じ `lerobot-dataset-viz` コマンドの `--root` を `{{LOCAL_DATASET_DIR_SH}}` にして映像を確認します。

追加の操作が必要な場合は[追加収集](../reference/values.md#additional-collection)を参照してください。

## 2. 学習用 EC2 へデータを渡す {#transfer-to-ec2}

収集を終了し、記録への書き込みが止まったら、データを EC2 へ渡します。手元の PC → 自分専用の S3 領域 → EC2 の順に、ファイルをそのまま転送します。

### 1. 収集したデータを自分用の S3 領域へ送る

実行場所: **手元の Jetson／Mac**。受講者ツールを有効にしたターミナルで実行します。S3 の `shared/` は共有教材用です。自分の収集データは自分専用の領域へ保存します。

`LOCAL_DATASET_DIR`は[接続の確認](check.md)で決めた手元の収集先です。収集中は転送せず、記録が終了してからフォルダ内のファイルをそのまま送ります。

```bash
test -f {{LOCAL_DATASET_DIR_SH}}/meta/info.json &&
  gclue-ai-handson-attendee files upload \
    {{LOCAL_DATASET_DIR_SH}} --to datasets
```

フォルダを送ると、元のフォルダ名も保存先に付きます。この手順の収集先の名前は `round1` なので、自分専用の `datasets/round1/` に保存されます。アップロードが成功したことを確認してください。`.DS_Store` はMacの表示用ファイルなので転送対象から除かれます。

新しい収集分では未使用のフォルダ名（例えば `round2`）を使い、次の取得側の `round1` も同じ名前へ揃えます。保存中は収集データを編集・追加しません。

### 2. EC2 へ取得し、データと映像を確認する

実行場所: **手元の PC**。初回は [接続手順](../connect.md)で Amazon DCV（リモートデスクトップ接続）のパスワードを設定します。

```bash
gclue-ai-handson-attendee dcv
```

トンネル用のターミナルは開いたまま、案内された URL から DCV にログインします。DCV デスクトップ内で Terminal を開き、以降の EC2 工程はそこで実行します。

実行場所: **EC2 の Ubuntu**。講師が LeRobot と受講者ツールを準備済みであることが前提です。

```bash
whoami
cd ~/lerobot
uv run --no-sync python --version
uv run --no-sync lerobot-train --help
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
```

下の欄へ入力した EC2 側の保存先が、取得コマンドへ直接入ります。情報確認の識別名も、同じ設定からコマンドへ反映されます。自分の収集データを取得する場合、例えば `/home/ubuntu/handson-data/workshop01/attendee01/round1` のような未使用のフォルダを講師と確認します。配布データの場合は、講師が既に置いた場所を指定します。

`source` は講師が EC2 に用意した受講者ツールを有効化します。バケット名・受講者 ID・リージョンは導入済みの設定から読み込まれるので、S3 バケットパスを組み立てる必要はありません。`--own` は自分専用の領域、`--prefix datasets/round1` はその中の保存先を指定します。

`whoami` が `ubuntu` であることを確認します。ツールがない・認証情報が期限切れの場合は講師へ確認します。EC2 上で依存を追加・更新せず、環境の不足は講師に確認します。

この工程は自分で収集したデータの取得です。講師の配置済み教材を使う場合は[教材とデータ確認](../dataset.md)へ進みます。


<div data-aws-values-panel data-aws-inline data-aws-fields="DATASET_DIR DATASET_REPO_ID"></div>

**まだ存在しない取得先**へ各ファイルをコピーし、データセットの情報ファイルがあることを確認します。

```bash
(
  set -e
  test ! -e {{DATASET_DIR_SH}} || {
    echo '取得先が存在します。別のパスを指定してください。' >&2
    exit 1
  }
  mkdir -p {{DATASET_DIR_SH}}
  gclue-ai-handson-attendee files pull --own \
    --prefix datasets/round1 --dest {{DATASET_DIR_SH}}
  cd {{DATASET_DIR_SH}}
  test -f meta/info.json
)
```

転送がエラーなく終了し、`meta/info.json` の存在確認も成功したら、次の情報・映像確認へ進みます。不足や表示エラーがあれば講師へ相談します。取得が途中で失敗した場合は、部分的なデータが残ることがあるため、別の未使用の取得先を設定してやり直します。

### 3. 情報と映像を確認する

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

失敗したエピソード番号を控えます。配布データが Git LFS のポインタのままの場合は、[Git LFS の復旧](../reference/data.md#git-lfs)を使います。


{% if audience == "staff" %}

### 講師：AWSへの転送の到達確認

本人のS3 バケットパス・EC2を確認し、転送結果と取得先、情報表示と映像確認を記録します。認証切れは再発行してPCとEC2それぞれで読み込み直します。

{% endif %}

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: カメラの調整](camera.md) · [次へ: データセットの編集](edit.md)

{% if audience == "staff" %}

## 講師：収集結果の到達確認

新規収集・追加収集のエピソード数、`front` と `side` の映像、保存先を確認してからAWSへ転送します。

{% endif %}
