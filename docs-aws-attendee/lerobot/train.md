# 学習

実行場所: **EC2 の Ubuntu**。[収集後のデータ転送](collect.md#transfer-to-ec2)、必要なら [データセットの編集](edit.md)を済ませた同じ Terminal で進めます。講師が CUDA と GPU 計算、ACT が画像特徴抽出に使う ResNet18 の事前学習済み重みのキャッシュを確認済みであることが前提です。今回の EC2 の GPU 学習は未検証です。

## 1. ACT学習（新規）

[ACT（Action Chunking with Transformers）](https://huggingface.co/docs/lerobot/act)は、収集した手本の操作からロボットの動かし方を学習する AI モデルです。ここでは自分のデータセットを使って操作モデルを学習します。

Jetson 用のメモリ設定や Mac の `mps` を EC2 へそのまま移しません。GPU と PyTorch を確認します。

```bash
nvidia-smi
uv run --no-sync python - <<'PY'
import torch
print(torch.__version__, torch.cuda.is_available())
PY
```

学習対象のデータに `observation.images.front` と `observation.images.side` の両方が含まれ、2台の映像が正しく対応していることを確認します。配布データを使う場合も同じ2台構成のデータを選びます。

GPU が表示され、PyTorch の結果が `True` なら、まず5000ステップで確認します。下の欄に未使用の学習実行名と出力先を入力し、過去の成果を削除しません。

<div data-aws-values-panel data-aws-inline data-aws-fields="DATASET_DIR DATASET_REPO_ID RUN_NAME TRAIN_OUTPUT_DIR"></div>


| コマンドでの名前 | 意味・どこで使うか | 説明用の例・決め方 |
| --- | --- | --- |
| `RUN_NAME` | 学習を1回実行した結果に付ける名前。後でS3から同じ結果を取り戻す目印 | `act-20261009-103000`。本人が日時などを含む未使用の名前を入力する |
| `TRAIN_OUTPUT_DIR` | EC2で学習結果とチェックポイントを保存するフォルダ | `/home/ubuntu/handson-work/workshop01/attendee01/outputs/act-20261009-103000`。本人が未使用の絶対パスを入力する |
| `HF_HUB_OFFLINE` | 外部のモデル配布サイトへ取得に行かず、準備済みのファイルを使う設定 | `1`。この講習会では案内どおり使う |

`DATASET_DIR`は学習に読むデータの場所、`DATASET_REPO_ID`はその識別名です。編集済みなら[編集の手順](edit.md)で切り替えた値を使います。上の日時・パスは説明例です。今回の実行名と未使用の出力先を入力してください。

```bash
export HF_HUB_OFFLINE=1
uv run --no-sync lerobot-train \
  --dataset.root={{DATASET_DIR_SH}} \
  --dataset.repo_id={{DATASET_REPO_ID_SH}} \
  --dataset.video_backend=pyav \
  --policy.type=act \
  --output_dir={{TRAIN_OUTPUT_DIR_SH}} \
  --job_name={{RUN_NAME_SH}} \
  --policy.device=cuda \
  --policy.push_to_hub=false \
  --save_checkpoint_to_hub=false \
  --wandb.enable=false \
  --steps=5000 \
  --save_freq=5000 \
  --batch_size=2 \
  --num_workers=0 \
  --policy.use_amp=true \
  --policy.use_vae=false \
  --policy.chunk_size=50 \
  --policy.n_action_steps=50
```

学習ログの終了とチェックポイントを確認します。5000ステップだけでタスクが成功するとは限りません。従来の Jetson の学習時間を EC2 の実績としては扱いません。

追加の操作が必要な場合は[学習の継続](../reference/values.md#resume-training)を参照してください。

## 2. 推論用のモデルを手元へ戻す {#recover-model}

学習を正常に終了し、チェックポイントへの書き込みが止まったら、推論する手元の機器へ戻します。EC2 → 自分専用の S3 領域 → 手元の PC の順に、ファイルをそのまま転送します。

### 1. EC2 から保存する

実行場所: **EC2 の Ubuntu**。前の学習で入力した実行名と結果の保存先がコマンドに入ります。学習が正常に終了し、ファイルへの書き込みが止まったことを確認してから進めます。同じ実行名へ保存し直す場合も、保存中に学習を再開しません。

`RUN_NAME`は[学習](train.md)で入力した実行名（説明用の例は `act-20261009-103000`）、`TRAIN_OUTPUT_DIR`はその学習結果のEC2内のフォルダです。学習時の値をそのまま使います。バケット名・受講者 ID・リージョンは講師が導入した受講者ツールの設定から読み込みます。`--to` には自分専用の領域内の保存先だけを指定します。


<div data-aws-values-panel data-aws-inline data-aws-fields="RUN_NAME TRAIN_OUTPUT_DIR"></div>

推論に必要な設定ファイルがあることを確認し、チェックポイントの各ファイルを保存します。

```bash
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
(
  set -e
  MODEL_DIR={{TRAIN_OUTPUT_DIR_SH}}/checkpoints/last/pretrained_model
  test -s "$MODEL_DIR/config.json"
  gclue-ai-handson-attendee files upload \
    {{TRAIN_OUTPUT_DIR_SH}}/checkpoints --to models/{{RUN_NAME}}
  printf '学習実行名: %s\n' {{RUN_NAME_SH}}
)
```

転送がエラーなく終了したことを確認し、表示された学習実行名を控えます。自分専用の `models/学習実行名/` に保存されます。認証切れなら講師に更新を依頼し、有効化し直してから保存します。

リンクや転送オプションは[チェックポイント転送の補足](../reference/files.md#checkpoint-links)を参照してください。

### 2. 手元へ取得し、内容を確認する

実行場所: **手元の Jetson／Mac**。受講者ツールを有効にし、下の欄の学習実行名を EC2 で使った値に合わせます。新しい保存先へ取得します。[接続の確認](check.md)と[カメラの調整](camera.md)で使った手元のターミナルを続けて使うと、機器の設定と回収後のモデルの場所を次の推論へ引き継げます。別のターミナルなら、その2ページのカメラ設定を再実行します。収集先と課題文はフォームの保存値を使います。

例えばEC2で表示された名前が `act-20261009-103000` なら、学習実行名欄にその値を入力します。新しい名前を付けたり、説明用の日時を使ったりしません。`LOCAL_MODEL_DIR`は手元の取得先を自動作成する変数です。


<div data-aws-values-panel data-aws-inline data-aws-fields="RUN_NAME"></div>

```bash
LOCAL_MODEL_DIR=$(mktemp -d)
gclue-ai-handson-attendee files pull --own \
  --prefix models/{{RUN_NAME}} --dest "$LOCAL_MODEL_DIR"
```

転送が成功したら、推論に使う設定ファイルとモデルファイルを確認します。

```bash
POLICY_PATH="$LOCAL_MODEL_DIR/checkpoints/last/pretrained_model"
test -s "$POLICY_PATH/config.json"
find "$POLICY_PATH" -maxdepth 1 -type f \
  -name '*.safetensors' -print
printf 'モデル保存先: %s\n' "$LOCAL_MODEL_DIR"
printf '推論モデルの場所: %s\n' "$POLICY_PATH"
```

表示された「推論モデルの場所」を下の欄へ入力します。推論のコマンドにも直接反映されます。

<div data-aws-values-panel data-aws-inline data-aws-fields="POLICY_PATH"></div>

`POLICY_PATH`は、取得したフォルダの中で推論に必要なモデルファイルが入っている場所です。例えば取得先が `/tmp/model-example` なら `/tmp/model-example/checkpoints/last/pretrained_model` です。実際の取得先は毎回変わるので、上のコマンドが設定した値を使い、表示されたモデル保存先を控えます。

`config.json` の確認が成功し、`.safetensors` のファイル名が表示されることを確認します。ファイルがなければ推論へ進まず、保存・取得をやり直します。保存先を控え、回収した `POLICY_PATH` を使って[推論の実行](run.md)でモデルファイルと機器構成を確認します。

{% if audience == "staff" %}

### 講師：モデルの回収の到達確認

チェックポイントの転送がエラーなく終了し、回収先の `last/pretrained_model` に `config.json` と `.safetensors` があることを確認します。手元でモデルのconfigを確認するまではEC2の削除へ進みません。

{% endif %}

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: データセットの編集](edit.md) · [次へ: 推論の実行](run.md)

{% if audience == "staff" %}

## 講師：学習前の環境の到達確認

GPU学習は未検証です。同じデータ・版・EC2での事前試験、GPUと依存、保存先、実行時間を確認してから開始します。学習なしコースでは情報表示とRerunで終了します。

{% endif %}
