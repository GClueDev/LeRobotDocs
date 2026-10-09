# データ確認の補足と復旧

[教材とデータ確認](../dataset.md)では配置済み教材の情報と映像を確認します。以下は必要な場合だけ使う補足です。

## 手元のデータを直接コピーする {#manual-copy}

手元だけにデータがある場合は、講師に EC2 への配置を依頼するか、[ssh・scp 用の接続設定](connect.md#ssh-config)を作成した後、**手元**からコピーできます。この `scp` による汎用手順は今回の実測対象外です。

```bash
scp -r '<手元のデータセットフォルダ>' \
  'gclue-ai-handson-{{EVENT_ID}}:/home/ubuntu/lerobot/'
```

コピー後に EC2 で `meta/info.json` の存在を確認し、データの情報と映像を確認します。

## Parquet を読めない：Git LFS の実体化 {#git-lfs}

Git LFS は大きなファイル本体を Git の履歴と別に管理し、履歴には小さな参照情報（ポインタ）を残します。通常は clone 時に本体も取得されますが、自動取得の無効化や Git LFS の未導入などで参照情報だけが残ることがあります。

`Corrupt footer` などが出て、Hugging Face 等から Git で clone したデータの場合、実データの代わりに Git LFS の小さなポインタファイルだけがある可能性があります。

講師に、対象が Git LFS を使うデータセットの clone であることと、ネットワーク取得してよいことを確認します。**EC2** で対象の clone に移動して次を実行します。LeRobot 本体のディレクトリではありません。

```bash
cd {{DATASET_DIR_SH}}
git lfs version
git lfs ls-files
git lfs fetch
git lfs checkout
cd ~/lerobot
```

`git lfs` がなければ講師へ導入を依頼します。取得後に[教材とデータ確認](../dataset.md)の情報・映像確認を再実行します。検証では aloha のデータ実体化後の表示が成功しました。pusht の表示成功は確認していません。

## 別の可視化コマンドを使う {#other-viewers}

!!! warning "別の可視化コマンドは未検証です"
    通常の確認は[教材とデータ確認](../dataset.md)の Rerun を使います。別の CLI `lerobot-dataset-viz` は今回の EC2 では未検証です。講師が同じ環境で確認し、案内した場合だけ使ってください。検証範囲は[出典と検証範囲](../verification.md)を参照してください。

[教材とデータ確認へ戻る](../dataset.md)

## 実習環境の版とツールを確認する {#environment}

講師の配置したEC2のAmazon DCV（リモートデスクトップ接続）内Terminalで実行します。通常のデータ確認で問題がなければ、この確認は不要です。

```bash
cd ~/lerobot
git rev-parse HEAD
uv --version
uv run --no-sync python --version
uv run --no-sync lerobot-edit-dataset --help
```

検証時の OS・LeRobot・Python・uv の版は[固定した EC2 環境の記録](../verification.md#runtime-versions)にまとめています。各バージョンと help を講師の指定と照合します。`--no-sync`は構築済みの依存をそのまま使う指定です。違いがあれば受講者自身で更新せず講師へ確認してください。

[データ確認へ戻る](../dataset.md)
