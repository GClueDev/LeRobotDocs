# Cameraの確認

実行場所: **手元の Jetson／Mac**。[接続の確認](check.md)と [キャリブレーション](calibration.md)を済ませ、同じターミナルで進めます。

| コマンドでの名前 | 意味・値の選び方 |
| --- | --- |
| `CAMERAS` | 2台の映像をどのカメラから読むかの設定。`front`は前方、`side`は側面の映像の名前。USB機器の検出結果を次の例へ反映する |
| `DEVICE` | 推論の計算に使う機能。Jetsonは `cuda`、Macは `mps`。自分の機器のタブを使う |
| `DISPLAY_DATA` | 実行中の映像を画面へ表示するか。`true`は表示、`false`は非表示。次のタブの接続条件に合わせる |
| 試験用データの保存先 | カメラの試験用データを置く手元のフォルダ。本収集先の末尾へ `_camera_test` を付ける。例えば `round1_camera_test` |

各設定項目の詳しい意味は[カメラ設定の読み方](../reference/values.md#camera-options)にまとめています。

検出した2台の接続先を入力します。Jetson のタブでは `/dev/video` のパス、Mac のタブでは番号を使います。

<div data-aws-values-panel data-aws-inline data-aws-fields="FRONT_CAMERA SIDE_CAMERA"></div>

## 1. データセット収集（1回）

前方の `front` と側面の `side` の2台で、まず1エピソード、10秒の映像と動作を確認します。本収集と分けたテスト専用の保存先を使います。既にテストデータがある場合は、保存先の名前を変えてください。

=== "Jetson"

    `front` を `/dev/video0`、`side` を `/dev/video2` とした例です。両方とも640×480、MJPG、30 FPSに対応する機器を使います。検出結果が異なる場合は講師と値を合わせます。SSH で操作する場合は GUI 表示を無効にします。

    ```bash
    CAMERAS="{front: {type: opencv,"
    CAMERAS+=" index_or_path: '{{FRONT_CAMERA}}',"
    CAMERAS+=" backend: 200, width: 640, height: 480, fps: 30,"
    CAMERAS+=" fourcc: 'MJPG'},"
    CAMERAS+=" side: {type: opencv,"
    CAMERAS+=" index_or_path: '{{SIDE_CAMERA}}',"
    CAMERAS+=" backend: 200, width: 640, height: 480, fps: 30,"
    CAMERAS+=" fourcc: 'MJPG'}}"
    DEVICE=cuda
    DISPLAY_DATA=false
    ```

=== "Mac"

    `front` をカメラ番号 `0`、`side` を `2` とした例です。検出結果と映像を確認し、それぞれの番号を合わせます。MJPGは固定しません。デスクトップのターミナルを使います。

    ```bash
    CAMERAS='{front: {type: opencv, index_or_path: {{FRONT_CAMERA}},'
    CAMERAS+=' width: 640, height: 480, fps: 30},'
    CAMERAS+=' side: {type: opencv, index_or_path: {{SIDE_CAMERA}},'
    CAMERAS+=' width: 640, height: 480, fps: 30}}'
    DEVICE=mps
    DISPLAY_DATA=true
    ```


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
  --dataset.root={{LOCAL_DATASET_DIR_SH}}_camera_test \
  --dataset.push_to_hub=false \
  --dataset.single_task={{TASK_SH}} \
  --dataset.fps=30 \
  --dataset.episode_time_s=10 \
  --dataset.reset_time_s=5 \
  --dataset.num_episodes=1 \
  --dataset.streaming_encoding=false \
  --display_data="$DISPLAY_DATA"
```

## 2.Rerunを起動

手元のデスクトップのターミナルでテストデータを表示し、`front` と `side` の両方の映像が記録されていることを確認します。2台の名前・向き・画角は本収集と推論でも揃えます。

```bash
lerobot-dataset-viz \
  --repo-id {{DATASET_REPO_ID_SH}} \
  --root {{LOCAL_DATASET_DIR_SH}}_camera_test \
  --episode-index 0 \
  --mode local \
  --num-workers 0 \
  --batch-size 1
```

SSH のみで作業している場合は手元のデスクトップで表示します。EC2 で表示する本収集データは、[収集後のデータ転送](collect.md#transfer-to-ec2)後に Amazon DCV（リモートデスクトップ接続）の ターミナル から確認します。従来の Jetson 向け `192.168.55.1` を EC2 の接続先として使いません。

## 3.Testデータの削除

テストの映像と関節の記録を確認し、Rerun を閉じます。テストデータを残す必要がなければ、表示されたパスがテスト専用の場所であることを確認してから削除します。本収集の `LOCAL_DATASET_DIR` は削除しません。

```bash
printf 'テストデータの削除対象: %s\n' \
  {{LOCAL_DATASET_DIR_SH}}_camera_test
rm -ri -- {{LOCAL_DATASET_DIR_SH}}_camera_test
```

削除の質問に答える前に対象を確認します。保存先は入力した収集先に `_camera_test` を付けたパスです。入力を変更した場合は削除対象も変わるので、実際の試験データの場所と一致することを確認してください。

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: キャリブレーション](calibration.md) · [次へ: データセットの収集](collect.md)

{% if audience == "staff" %}

## 講師：カメラの確認の到達確認

テスト収集で `front` と `side` の2映像、名前とカメラの向きを確認します。削除するのはテストデータで、実習用データセットとは分けます。

{% endif %}
