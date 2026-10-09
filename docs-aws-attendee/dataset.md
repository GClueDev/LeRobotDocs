# 教材の取得と LeRobot のデータ確認

右上の「各種値の設定」で、講師から受け取った値を確認してください。認証情報ファイルのパス・期限付きURLは保存せず、指定箇所を手動で置き換えます。

{% if audience == "staff" %}

## 講師：教材取得と環境の確認

配布版が一致することを確認し、LeRobotの既知の未検証範囲を共有します。

{% filter staff_headings %}
{% include 'instructor/support/05.md' %}
{% endfilter %}

{% endif %}

## 1. コースと教材を確認する

この基本コースでは、講師がEC2に配置した教材を変更せず、情報と映像を確認します。自分で収集・編集・学習する場合は[実習の進め方](aws-workflow.md)に従ってください。

手元の講義資料は[導入](setup.md)で取得済みです。再取得が必要なら[教材の再取得](reference/files.md#materials)、追加の共有データを指定されたら[共有データの取得](reference/files.md#shared-datasets)を使います。

## 2. EC2 にある実習環境を確かめる

このページは、講師が LeRobot とデータセットを配置済みの EC2 を使います。受講者は構築スクリプトを実行しません。配置場所が違う場合は講師の案内に合わせてください。

[DCV](connect.md) のデスクトップから Terminal を開きます。**以降は EC2 の ubuntu ユーザー** で実行します。`~/lerobot` がない、`uv` がない場合は講師に構築状況を確認してください。

```bash
whoami
cd ~/lerobot
git rev-parse HEAD
uv --version
uv run --no-sync python --version
uv run --no-sync lerobot-edit-dataset --help
```

検証環境は Ubuntu 24.04 / x86_64、LeRobot v0.6.0（`30da8e687a6dfc617fcd94afc367ac7071c376ce`）、Python 3.12.3、uv 0.12.23 でした。`whoami` が `ubuntu`、各バージョンと help が出れば次へ進めます。`--no-sync` は構築済みの依存をそのまま使う指定です。

## 3. データセットの場所を指定する

右上の「各種値の設定」でデータセットの場所と識別名を確認して、次を実行します。`{{DATASET_REPO_ID}}` はバケット名や EC2 名ではなく、データセットの識別名です。

```bash
ls {{DATASET_DIR_SH}}/meta/info.json
```

例えば講師が「EC2の `/home/ubuntu/handson-data/workshop01/attendee01/round1`、識別名は `attendee01/red-cube`」と案内したら、フォームの「EC2 のデータセットディレクトリ」と「データセット識別名」にそれぞれ入力します。この2つは説明用の例です。講師の配置先と指定名を使ってください。

`meta/info.json` のパスが表示されれば配置確認は成功です。検証では `1cam_test` を使いましたが、本番配布する教材名・場所は講師が決めます。

手元だけにデータがある場合は講師に配置を確認してください。[手動コピーの補足](reference/data.md#manual-copy)も参照できます。

## 4. データを変更せず内容を確認する

**EC2** の `~/lerobot` で実行します。

```bash
uv run --no-sync lerobot-edit-dataset \
  --repo_id {{DATASET_REPO_ID_SH}} \
  --root {{DATASET_DIR_SH}} \
  --operation.type info
```

エピソード数・フレーム数・FPS 等が表示され、講師の教材説明と一致すれば成功です。検証に使ったデータは 48 エピソード、14,538 フレーム、30 FPS でした。この数値は別の教材では変わります。

ここで使う `info` は情報表示です。エピソード削除・結合・再エンコード等の変更操作は未検証なので、この基本コースでは実行しません。

## 5. Rerun で映像を表示する

**EC2 の DCV デスクトップ内の Terminal** で実行します。通常の SSH ターミナルから GUI を開こうとせず、DCV 内で操作します。

```bash
cd ~/lerobot
uv run --no-sync rerun {{DATASET_DIR_SH}}
```

Rerun のウィンドウが開き、映像や時系列データを確認できれば成功です。Rerun を閉じ、ターミナルが戻らなければ Ctrl+C で終了します。この主手順は今回の実測で使った Rerun へのデータセットディレクトリ指定に合わせています。

別の可視化コマンドを指定された場合は[可視化の補足](reference/data.md#other-viewers)を参照してください。

表示に失敗した場合は[Git LFS の復旧](reference/data.md#git-lfs)または[困ったとき](troubleshooting.md)を確認してください。

## 学習に進む前に

GPU 学習、ResNet18 重みの事前取得、編集による変更、可視化のポート転送は未検証です。依存導入や Rerun 表示の成功を GPU 学習の成功とみなさず、講師が確認した追加手順に従ってください。既存の Jetson 用 Python 3.10 手順を、この EC2 用 Python 3.12 環境へ混ぜないでください。

確認が終わったら [保存と回収](save.md) へ進みます。
