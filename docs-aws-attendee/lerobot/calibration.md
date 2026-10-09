# キャリブレーション

キャリブレーションは、ロボットの関節位置と可動範囲を調整し、操作用アームと追従するアームの動きを対応させる準備です。Leader は人が動かす操作用アーム、Follower はその動きに追従するアームです。

実行場所: **手元の Jetson／Mac**。[接続の確認](check.md)で右上の設定へ入力したポートがコマンドに入ります。機器の可動範囲を空け、停止操作ができる状態で進めます。

`--teleop.id` の `my_leader_arm` と `--robot.id` の `my_follower_arm` は、LeRobotが機器ごとの調整結果を保存・再利用するための名前です。この手順ではこの2つを使います。講師が機器ごとに別名を指定した場合は、以下と後続の収集・推論のコマンドをすべて同じ指定名へ揃えてください。USB接続先のポート名とは別です。

## 1. キャリブレーション（Leader）

既存のキャリブレーションをやり直す場合は、質問に `c` を入力し、表示された案内に従います。

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port={{TELEOP_PORT_SH}} \
  --teleop.id=my_leader_arm
```

## 2. キャリブレーション（Follower）

同じく、やり直す場合は質問に `c` を入力します。

```bash
lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port={{ROBOT_PORT_SH}} \
  --robot.id=my_follower_arm
```

## 3. テレオペレーション

テレオペレーションは、人が Leader を動かして Follower を操作することです。調整後の2台が対応した動きになるか確認します。

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port={{ROBOT_PORT_SH}} \
  --robot.id=my_follower_arm \
  --teleop.type=so101_leader \
  --teleop.port={{TELEOP_PORT_SH}} \
  --teleop.id=my_leader_arm
```

Follower が Leader に追従することを確認し、Ctrl+C で終了します。`my_leader_arm` と `my_follower_arm` は、同じ機器の収集・推論でも変えません。

## 4. リファレンス

- [LeRobot v0.6.0](https://github.com/huggingface/lerobot/releases/tag/v0.6.0)
- [出典と検証範囲](../verification.md)

---

[前へ: 接続の確認](check.md) · [次へ: カメラの調整](camera.md)

{% if audience == "staff" %}

## 講師：キャリブレーションの到達確認

各受講者のLeaderとFollowerのキャリブレーション完了を確認してからテレオペレーションへ進みます。

{% endif %}
