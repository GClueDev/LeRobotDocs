# 教材・ファイルの取得と保存の補足

通常の実習では教材は[導入](../setup.md)で取得し、学習結果は[モデル回収](../aws-model-recovery.md)で回収します。以下は追加教材やモデル以外のファイルを扱う場合の補足です。

## 現行教材を再取得する {#materials}

**手元の PC** で講習会用の環境を有効化してから実行します。

```bash
gclue-ai-handson-attendee files pull --dest ./materials
```

`manifest.json のとおりであることを SHA-256 で確認しました。` が成功条件です。版の指定がある場合は `--version '<版>'` を追加します。

## 指定された共有データを取得する {#shared-datasets}

共有データセットは、講師が指定したS3 バケットパスから取得します。`--prefix` には共有領域 `shared/` からの相対パスを指定します。次の `datasets/` は配置例です。

```bash
gclue-ai-handson-attendee files pull --prefix datasets/ \
  --dest ./datasets
```

これは共有領域 `shared/datasets/` の取得です。取得後は `meta/info.json` の存在と、データの情報・映像を確認してください。

## モデル以外のファイルを保存するとき

以下は単独の保存例です。通し実習のチェックポイントは[モデル回収](../aws-model-recovery.md)の保存先と手順を使い、例の保存先と混ぜないでください。チェックポイントを圧縮する必要はありません。

## 手元のファイルを保存する {#upload}

```bash
gclue-ai-handson-attendee files upload ./checkpoints \
  --to models/day1
```

- `./checkpoints`: 保存するファイルまたはフォルダ。フォルダを指定すると、その名前のフォルダとして保存します。
- `--to <保存先>`: 自分専用の場所の中の保存先（例: `models/day1`）。省略すると、自分専用の場所の直下に保存します。

`… にアップロードしました。` と表示されれば成功です。

## EC2 のファイルを保存する {#ec2-upload}

講師が EC2 に用意した受講者ツールを使います。DCV の Terminal（`ubuntu` ユーザー）で有効化し、手元と同じ `files upload` を実行します。

```bash
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
gclue-ai-handson-attendee files upload ./checkpoints \
  --to models/day1
```

フォルダ名も付くため、自分専用の `models/day1/checkpoints/` に保存されます。通し実習では[モデル回収](../aws-model-recovery.md)の実行名と保存先を使い、この例と混ぜないでください。

## 保存したファイルを取り戻す {#recover}

自分専用の場所に保存した成果を、手元の機器に取得します。

```bash
gclue-ai-handson-attendee files pull --own --prefix models/day1 \
  --dest ./recovered
```

- `--own`: 自分専用の場所から取得します。
- `--prefix <保存先>`: 保存したときの保存先（`--to` に指定した値）。省略すると自分専用の場所の全体を取得します。
- `--dest <フォルダ>`: 手元の保存先のフォルダ。

`… を ./recovered に取得しました。` と表示されれば成功です。


## 小さなファイルで保存経路を確認する {#check-route}

**手元の PC** で空の作業フォルダから実行します。

```bash
mkdir -p ~/handson-save-check
cd ~/handson-save-check
printf "handson save check\n" > proof.txt
gclue-ai-handson-attendee files upload ./proof.txt \
  --to checks/day1
gclue-ai-handson-attendee files pull --own --prefix checks/day1 \
  --dest ./downloaded
cmp proof.txt downloaded/proof.txt
```

`cmp` が何も表示せず終了すれば内容が一致しています。フォルダを upload した場合はフォルダ名も保存されるので、例の `checkpoints` は回収先の `./recovered/checkpoints/` に入ります。

EC2 でも受講者ツールを有効化してから実行し、有効期限切れなら講師に更新を依頼してください。転送の成功だけで回収完了とせず、手元へ戻したファイルのサイズ・内容または `cmp` も確認します。

## 導入先を変更した場合の片付け {#custom-directory}

導入時に `--dir` を指定した場合は、実際の導入先を削除します。残す成果を先に回収し、対象を確かめてから[片付け](../finish.md)の削除コマンドのパスを導入先へ置き換えてください。

## チェックポイントのリンクと転送オプション {#checkpoint-links}

`checkpoints/last` が別のチェックポイントへのシンボリックリンクでも、リンク先のファイルを `last/` の名前で転送します。手元では `last` は通常のディレクトリになります。各ステップのチェックポイントも回収します。

`files upload` はフォルダ内のファイルとリンク先の実体を転送します。受講者が `--recursive` や `--follow-symlinks` を指定する必要はありません。フォルダ名 `checkpoints` も保存先に付きます。`files pull --own --prefix models/学習実行名` で取得すると、その中の `checkpoints/` が取得先に作られます。
