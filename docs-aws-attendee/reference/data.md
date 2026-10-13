# データ確認の補足と復旧

[教材とデータ確認](../dataset.md)では配置済み教材の情報と映像を確認します。以下は必要な場合だけ使う補足です。

## 手元のデータを直接コピーする {#manual-copy}

手元だけにデータがある場合は、講師に EC2 への配置を依頼するか、[ssh・scp 用の接続設定](connect.md#ssh-config)を作成した後、**手元**からコピーできます。

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

`git lfs` がなければ講師へ導入を依頼します。取得後に[教材とデータ確認](../dataset.md)の情報・映像確認を再実行します。

## 別の可視化コマンドを使う {#other-viewers}

!!! warning "講師の案内がある場合だけ使います"
    通常の確認は[教材とデータ確認](../dataset.md)の Rerun を使います。別の CLI `lerobot-dataset-viz` は、講師が同じ環境で確認し、案内した場合だけ使ってください。

[教材とデータ確認へ戻る](../dataset.md)

## 実習環境の版とツールを確認する {#environment}

講師の配置したEC2のAmazon DCV（リモートデスクトップ接続）内ターミナルで実行します。通常のデータ確認で問題がなければ、この確認は不要です。

```bash
cd ~/lerobot
git rev-parse HEAD
uv --version
uv run --no-sync python --version
uv run --no-sync lerobot-edit-dataset --help
```

OS・LeRobot・Python・uv などの版は、後述の[固定した EC2 環境](#runtime-versions)のとおりです。各バージョンと help を講師の指定と照合します。`--no-sync`は構築済みの依存をそのまま使う指定です。違いがあれば受講者自身で更新せず講師へ確認してください。

[データ確認へ戻る](../dataset.md)

## 固定した EC2 環境 {#runtime-versions}

実習で使う EC2 の環境は、次の組合せに固定されています。

| 項目 | 版 |
| --- | --- |
| OS / CPU | Ubuntu 24.04 / x86_64 |
| LeRobot | v0.6.0、`30da8e687a6dfc617fcd94afc367ac7071c376ce` |
| Python / uv | 3.12.3 / 0.12.23 |
| torch / torchvision | 2.11.0+cu128 / 0.26.0+cu128 |
| av / torchcodec | 15.1.0 / 0.11.1+cpu |
| rerun-sdk | 0.33.1 |
| AWS CLI | 2.37.10 |

この一覧は最新推奨版の主張ではなく、固定した組合せの記録です。環境構築は講師・構築担当者が行い、受講者は途中で依存を入れ替えません。
