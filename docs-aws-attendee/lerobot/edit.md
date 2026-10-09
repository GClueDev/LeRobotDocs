# データセットの編集

収集したデータセットから、失敗したエピソードを取り除きます。実行場所は **EC2 の Ubuntu** です。[収集後のデータ転送](collect.md#transfer-to-ec2)で確認したデータの場所と識別名（右上の設定からコマンドへ入ります）を使い、元データを保った別の場所へ出力します。変更編集は今回の EC2 実測対象外です。

## 1. 準備

講師が用意した LeRobot 環境のまま作業します。従来の手元向け `pip install` は EC2 では行わず、ツールがない場合は講師に確認します。

```bash
cd ~/lerobot
export HF_HUB_OFFLINE=1
```

## 2. データセットの内容を確認する

### 概要を表示する

```bash
uv run --no-sync lerobot-edit-dataset \
  --repo_id {{DATASET_REPO_ID_SH}} \
  --root {{DATASET_DIR_SH}} \
  --operation.type info
```

エピソード数、フレーム数、FPS、タスクを収集時の記録と照合します。エピソード番号は0から始まります。

### エピソードごとの長さを確認する

従来と同じくメタデータの Parquet を読み、短すぎる・長すぎるエピソードを確認します。

```bash
uv run --no-sync python - {{DATASET_DIR_SH}} <<'PY'
import glob
import json

import pyarrow.parquet as pq

import sys
root = sys.argv[1]
fps = json.load(open(f"{root}/meta/info.json"))["fps"]

pattern = f"{root}/meta/episodes/chunk-*/file-*.parquet"
columns = ["episode_index", "length", "tasks"]
rows = []
for path in sorted(glob.glob(pattern)):
    rows += pq.read_table(path, columns=columns).to_pylist()
rows.sort(key=lambda r: r["episode_index"])

mean = sum(r["length"] for r in rows) / len(rows)
print("episode  frames  seconds  vs_mean  task")
for r in rows:
    seconds = r["length"] / fps
    ratio = r["length"] / mean
    task = ", ".join(r["tasks"])
    print(f"{r['episode_index']:7d}  {r['length']:6d}  "
          f"{seconds:7.1f}  {ratio:6.0%}  {task}")
PY
```

### エピソードを可視化して確認する

Amazon DCV（リモートデスクトップ接続）のデスクトップ内の Terminal で表示します。

```bash
uv run --no-sync rerun {{DATASET_DIR_SH}}
```

### 確認結果を控える

失敗したエピソード番号と理由を控えます。削除後は番号が振り直されるため、元の番号との対応を残します。

## 3. エピソードを削除する

`CLEAN_DATASET_DIR`は編集後のデータを置くEC2の新しいフォルダです。元の場所が `/home/ubuntu/handson-data/workshop01/attendee01/round1` なら末尾に `_clean` が付きます。新しい識別名も、元が `attendee01/red-cube` なら `attendee01/red-cube_clean` になります。どちらも下のコマンドが作る値で、元データと区別するためのものです。

`[1, 2]` は確認した番号へ置き換えます。出力先が既にある場合は削除せず、別の名前にします。

```bash
export HF_HUB_OFFLINE=1
uv run --no-sync lerobot-edit-dataset \
  --repo_id {{DATASET_REPO_ID_SH}} \
  --root {{DATASET_DIR_SH}} \
  --new_repo_id {{DATASET_REPO_ID_SH}}_clean \
  --new_root {{DATASET_DIR_SH}}_clean \
  --operation.type delete_episodes \
  --operation.episode_indices '[1, 2]'
```

## 4. 結果を確認する

編集後の件数と映像を確認します。

```bash
uv run --no-sync lerobot-edit-dataset \
  --repo_id {{DATASET_REPO_ID_SH}}_clean \
  --root {{DATASET_DIR_SH}}_clean \
  --operation.type info
```
```bash
uv run --no-sync rerun {{DATASET_DIR_SH}}_clean
```

## 5. 元のデータセットと差し替える

AWS 版では元データのフォルダを移動・削除せず、学習で参照する値を編集結果へ切り替えます。結果を確認できてから実行します。

現在の保存先・識別名に `_clean` を付けた編集結果を、下の欄へ入力し直します。情報と映像を確認できてから切り替え、元データは残します。学習コマンドもこの入力値を直接使います。編集しない場合はこの切替を飛ばします。


<div data-aws-values-panel data-aws-inline data-aws-fields="DATASET_DIR DATASET_REPO_ID"></div>

別のブラウザやURLで学習する場合は、設定JSONで受け渡すか同じ値を入力してください。

## 出力先の注意

`--root` は元データ、`--new_root` は別の出力先です。同じ場所を指定しません。元データと確認記録は、実習の成果を回収するまで保管します。

編集時のエラーは[編集時のエラー](../reference/values.md#edit-errors)を参照してください。

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: データセットの収集](collect.md#transfer-to-ec2) · [次へ: 学習](train.md)

{% if audience == "staff" %}

## 講師：編集結果の到達確認

削除対象を本人と確認し、元データと編集後の出力先を分けます。件数と映像を確認するまでは元データと差し替えません。

{% endif %}
