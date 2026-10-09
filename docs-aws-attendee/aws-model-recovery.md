# AWS からのモデル回収

[学習](lerobot/train.md)が終了したら、EC2 → 自分専用の S3 領域 → 手元の Jetson／Mac の順にチェックポイントを戻します。ファイルをそのまま転送します。

## 1. EC2 から保存する

実行場所: **EC2 の Ubuntu**。前の学習で使った `RUN_NAME` と `TRAIN_OUTPUT_DIR` を使います。学習が正常に終了し、ファイルへの書き込みが止まったことを確認してから進めます。同じ実行名へ保存し直す場合も、保存中に学習を再開しません。

`RUN_NAME`は[学習](lerobot/train.md)で自動作成された実行名（説明用の例は `act-20261009-103000`）、`TRAIN_OUTPUT_DIR`はその学習結果のEC2内のフォルダです。学習時の値をそのまま使います。バケット名・受講者 ID・リージョンは講師が導入した受講者ツールの設定から読み込みます。`--to` には自分専用の領域内の保存先だけを指定します。

推論に必要な設定ファイルがあることを確認し、チェックポイントの各ファイルを保存します。

```bash
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
(
  set -e
  MODEL_DIR="$TRAIN_OUTPUT_DIR/checkpoints/last/pretrained_model"
  test -s "$MODEL_DIR/config.json"
  gclue-ai-handson-attendee files upload \
    "$TRAIN_OUTPUT_DIR/checkpoints" --to "models/$RUN_NAME"
  printf '学習実行名: %s\n' "$RUN_NAME"
)
```

転送がエラーなく終了したことを確認し、表示された学習実行名を控えます。自分専用の `models/学習実行名/` に保存されます。認証切れなら講師に更新を依頼し、有効化し直してから保存します。

リンクや転送オプションは[チェックポイント転送の補足](reference/files.md#checkpoint-links)を参照してください。

## 2. 手元へ取得し、内容を確認する

実行場所: **手元の Jetson／Mac**。受講者ツールを有効にし、`<学習実行名>` を EC2 で控えた値に置き換えます。新しい保存先へ取得します。[接続の確認](lerobot/check.md)と[カメラの調整](lerobot/camera.md)で使った手元のターミナルを続けて使うと、機器の設定と回収後のモデルの場所を次の推論へ引き継げます。別のターミナルなら、その2ページの設定も再実行します。

例えばEC2で表示された名前が `act-20261009-103000` なら、次の山括弧の部分だけをその値に置き換えます。新しい名前を付けたり、説明用の日時を使ったりしません。`LOCAL_MODEL_DIR`は手元の取得先を自動作成する変数です。

```bash
RUN_NAME='<学習実行名>'
LOCAL_MODEL_DIR=$(mktemp -d)
gclue-ai-handson-attendee files pull --own \
  --prefix "models/$RUN_NAME" --dest "$LOCAL_MODEL_DIR"
```

転送が成功したら、推論に使う設定ファイルとモデルファイルを確認します。

```bash
POLICY_PATH="$LOCAL_MODEL_DIR/checkpoints/last/pretrained_model"
test -s "$POLICY_PATH/config.json"
find "$POLICY_PATH" -maxdepth 1 -type f \
  -name '*.safetensors' -print
printf 'モデル保存先: %s\n' "$LOCAL_MODEL_DIR"
```

`POLICY_PATH`は、取得したフォルダの中で推論に必要なモデルファイルが入っている場所です。例えば取得先が `/tmp/model-example` なら `/tmp/model-example/checkpoints/last/pretrained_model` です。実際の取得先は毎回変わるので、上のコマンドが設定した値を使い、表示されたモデル保存先を控えます。

`config.json` の確認が成功し、`.safetensors` のファイル名が表示されることを確認します。ファイルがなければ推論へ進まず、保存・取得をやり直します。保存先を控え、回収した `POLICY_PATH` を使って[推論の実行](lerobot/run.md)でモデルファイルと機器構成を確認します。

---

[前へ: 学習](lerobot/train.md) · [次へ: 推論の実行](lerobot/run.md)

{% if audience == "staff" %}

## 講師：モデルの回収の到達確認

チェックポイントの転送がエラーなく終了し、回収先の `last/pretrained_model` に `config.json` と `.safetensors` があることを確認します。手元でモデルのconfigを確認するまではEC2の削除へ進みません。

{% endif %}
