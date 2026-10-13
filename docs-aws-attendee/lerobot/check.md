# 接続の確認

従来と同じ順で、ロボットを接続した手元の Jetson／Mac を確認します。AWS の受講者環境は先に [PC の準備と導入](../setup.md)で用意し、右上の「各種値の設定」で開催・受講者・データセットの値を入力してください。[設定の使い方](../common.md)も参照できます。

## 1. 接続確認

実行場所: **ロボットとカメラを接続した手元の Jetson／Mac**。EC2 の USB ポートとして指定するものではありません。

![SO-101 とカメラの接続](../assets/robot-connection.png)

指定の USB 接続先を確認します。Jetson で起動後に接続を変えて認識番号が変わった場合は、講師の案内に沿って接続を戻し、再起動後に検出し直します。

## 2. SO-101のポート確認

=== "Jetson"

    ```bash
    ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null || true
    lerobot-find-port
    ```

=== "MacBook"

    ```bash
    ls -l /dev/tty.usbmodem* /dev/tty.usbserial* 2>/dev/null || true
    lerobot-find-port
    ```

検出したLeaderとFollowerの接続先を下の欄へ入力します。右上の「各種値の設定」と同じ値を共有します。手元のLeRobot作業フォルダも講師に確認して入力してください。例えばMacなら `/Users/student/lerobot`、Leaderは `/dev/tty.usbmodem12301`、Followerは `/dev/tty.usbmodem12302` ですが、実際の検出結果を使います。Jetsonの例と各値の意味は[値と機器の対応](../reference/values.md#local-values)を参照してください。


<div data-aws-values-panel data-aws-inline data-aws-fields="PROJECT_DIR TELEOP_PORT ROBOT_PORT LOCAL_DATASET_DIR TASK"></div>
手元の収集先は未使用の絶対パスを入力します。`round1` というフォルダ名で収集する主手順です。ホームの場所は手元のターミナルで次を実行して確認できます。

```bash
echo "$HOME"
```

課題文も講師と合わせ、収集・推論で同じ値を使います。以下は作業フォルダへ移るコマンドです。

```bash
cd {{PROJECT_DIR_SH}}
```

`round1`は今回の収集分の名前、課題文の説明例 `Pick up the red cube` は「赤い立方体を持ち上げる」です。新しい収集分は未使用の名前にし、講師と転送先も合わせてください。フォルダ・USB接続先・データの識別名は、ブラウザで入力した値が後続のコマンドへ直接入ります。

## 3. カメラ確認

```bash
lerobot-find-cameras opencv
```

前方カメラと側面カメラの2台を接続し、検出結果と実際の映像で対応を確認します。Jetson の `/dev/video0` と `/dev/video2` を使う例では、両方が640×480、MJPG、30 FPSに対応していることを確認します。

```bash
for CAMERA_PATH in /dev/video0 /dev/video2; do
  v4l2-ctl -d "$CAMERA_PATH" --list-formats-ext
  v4l2-ctl -d "$CAMERA_PATH" --get-fmt-video
  v4l2-ctl -d "$CAMERA_PATH" --get-parm
done
```

番号は接続環境で変わります。2台が別々の機器であることを確認し、同じカメラの別ノードを2台として指定しないでください。Macでも2台の検出番号と映像を確認します。次の [カメラの調整](camera.md)で、収集・推論に使うカメラ設定を用意します。

## リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)

---

[前へ: EC2 への接続](../connect.md) · [次へ: キャリブレーション](calibration.md)

{% if audience == "staff" %}

## 講師：接続確認の到達確認

LeaderとFollowerのポート、2台のカメラの番号と映像を本人と確認します。複数組の機器を取り違えず、各組の対応を控えます。

{% endif %}
