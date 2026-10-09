# データ確認の補足と復旧

[教材とデータ確認](../dataset.md)では配置済み教材の情報と映像を確認します。以下は必要な場合だけ使う補足です。

## 手元のデータを直接コピーする {#manual-copy}

手元だけにデータがある場合は、講師に EC2 への配置を依頼するか、[SSH 設定](../connect.md)を作成した後、**手元**からコピーできます。この `scp` による汎用手順は今回の実測対象外です。

```bash
scp -r '<手元のデータセットフォルダ>' \
  'gclue-ai-handson-{{EVENT_ID}}:/home/ubuntu/lerobot/'
```

コピー後に EC2 で `meta/info.json` の存在を確認し、講師から受け取ったチェックサムで照合します。

## Parquet を読めない：Git LFS の実体化 {#git-lfs}

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

LeRobot の `lerobot-dataset-viz --repo-id ... --root ... --episode-index 0 --mode local` は別の CLI です。今回そのコマンドでの表示を実測済みとはしていません。講師が別途確認した場合に使ってください。

[教材とデータ確認へ戻る](../dataset.md)
