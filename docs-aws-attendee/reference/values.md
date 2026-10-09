# 値・機器・追加操作の逆引き

通常の実習は各手順ページの順に進めます。値の意味を確かめる場合や、追加収集・学習継続が必要な場合にこのページを使います。

## 手元の機器と値 {#local-values}

| 設定欄 | 用途・誰が決めるか | 説明用の例 |
| --- | --- | --- |
| 手元の LeRobot 作業フォルダ（`PROJECT_DIR`） | 講師に確認した手元の配置先。EC2とは別 | Mac `/Users/student/lerobot`、Jetson `/home/student/lerobot` |
| Leader の USB 接続先（`TELEOP_PORT`） | 人が動かすアームの検出結果を本人と講師が確認する | Mac `/dev/tty.usbmodem12301`、Jetson `/dev/ttyACM0` |
| Follower の USB 接続先（`ROBOT_PORT`） | 追従するアームの検出結果。Leaderと取り違えない | Mac `/dev/tty.usbmodem12302`、Jetson `/dev/ttyACM1` |
| `LOCAL_DATASET_DIR` | 手元の収集先。接続確認の入力欄で決める | `/Users/student/handson-data/workshop01/attendee01/round1` |
| `TASK` | 収集・推論で同じ課題文を使う | `Pick up the red cube` |

例をそのまま入力せず、実際の配置先と検出結果を使います。機器やUSB接続を変えた場合は「各種値の設定」を更新し、改めて表示されたコマンドをコピーしてください。

## 追加収集 {#additional-collection}

実行場所・前提は[データセットの収集](../lerobot/collect.md)と同じです。通常の初回実習では実行しません。


追加するときは初回と同じ識別名、保存先、カメラ構成、FPS、タスクで、`--resume=true` を使います。以下は5エピソードを追加する例です。

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
  --dataset.num_episodes=5 \
  --dataset.streaming_encoding=false \
  --display_data="$DISPLAY_DATA" \
  --resume=true
```

`num_episodes=5` は追加する数です。新規30エピソードの後なら合計35になります。追加後も件数と2台の映像を確認します。1台構成で作成した既存データセットには、この2台構成で追加せず、新しい保存先で収集し直します。


## 学習の継続 {#resume-training}

実行場所・前提は[学習](../lerobot/train.md)と同じです。通常の初回実習では実行しません。


`steps` は追加回数ではなく、継続後に到達させる総ステップ数です。5000から15000ステップへ続ける例です。

```bash
TRAIN_CONFIG_PATH={{TRAIN_OUTPUT_DIR_SH}}/checkpoints/last
TRAIN_CONFIG_PATH+="/pretrained_model/train_config.json"
uv run --no-sync lerobot-train \
  --config_path="$TRAIN_CONFIG_PATH" \
  --resume=true \
  --steps=15000 \
  --policy.push_to_hub=false \
  --save_checkpoint_to_hub=false \
  --wandb.enable=false
```

`TRAIN_CONFIG_PATH`は前回の学習条件を記録したファイルの場所で、下の設定で学習結果のフォルダの中の `checkpoints/last/pretrained_model/train_config.json` を指します。別の学習結果を指定しないよう、同じ `TRAIN_OUTPUT_DIR` を使います。

実際にできた `train_config.json` の場所を確認します。`RUN_NAME` と `TRAIN_OUTPUT_DIR` を控えます。


## 編集時のエラー {#edit-errors}

### `AssertionError: Episode length mismatch`

エピソード長の不一致や読み込みエラーが出たら変更編集を続けず、[困ったとき](../troubleshooting.md)と [データ確認](../dataset.md)を確認し、講師に元データの状態を伝えます。


## カメラ設定の読み方 {#camera-options}

カメラの `width`・`height` は画像の横・縦の画素数（例は640×480）、`fps` は1秒あたりの画像枚数（例は30）です。`index_or_path` は機器の接続先、`fourcc` の `MJPG` は映像の形式、Jetsonの `backend: 200` はLinuxのカメラ読取方式の指定です。対応を確認した講師の設定に合わせます。

