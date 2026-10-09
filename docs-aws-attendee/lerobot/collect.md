# データセットの収集

実行場所: **手元の Jetson／Mac**。[カメラの調整](camera.md)で設定した `CAMERAS`、`DEVICE`、`DISPLAY_DATA` と、[接続の確認](check.md)で作った手元の収集先と課題文を使います。USB接続先と識別名は右上の設定からコマンドへ入ります。2台のカメラ名 `front` と `side`、それぞれの位置・解像度・FPS、タスクは収集と推論で合わせます。

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
  --dataset.root="$LOCAL_DATASET_DIR" \
  --dataset.push_to_hub=false \
  --dataset.single_task="$TASK" \
  --dataset.fps=30 \
  --dataset.episode_time_s=10 \
  --dataset.reset_time_s=5 \
  --dataset.num_episodes=30 \
  --dataset.streaming_encoding=false \
  --display_data="$DISPLAY_DATA"
```

`episode_time_s` は1エピソードの時間、`reset_time_s` は次のエピソードまでの準備時間です。収集後、[カメラの調整](camera.md)と同じ `lerobot-dataset-viz` コマンドの `--root` を `"$LOCAL_DATASET_DIR"` にして映像を確認します。

追加の操作が必要な場合は[追加収集](../reference/values.md#additional-collection)を参照してください。

## AWS へのデータ転送

収集が完了したら [AWS へのデータ転送](../aws-transfer.md)で、自分専用の S3 領域へ送り、EC2 へ取得します。講師の配布データを使う場合は収集・送信を飛ばし、同ページで EC2 の作業環境とデータの場所を確認してください。

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: カメラの調整](camera.md) · [次へ: AWS へのデータ転送](../aws-transfer.md)

{% if audience == "staff" %}

## 講師：収集結果の到達確認

新規収集・追加収集のエピソード数、`front` と `side` の映像、保存先を確認してからAWSへ転送します。

{% endif %}
