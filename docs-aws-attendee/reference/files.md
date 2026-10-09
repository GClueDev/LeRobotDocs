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

講師が自分の EC2 に認証情報ファイルを書き込んだ場合は、自分の EC2 から直接保存できます。
SSH か DCV のターミナル（`ubuntu` ユーザー）で、次のコマンドを順に実行します。

```bash
source /tmp/gclue-ai-handson-{{EVENT_ID}}-{{ATTENDEE_ID}}.env
```

```bash
S3_DEST="s3://$GCLUE_AI_HANDSON_BUCKET/$GCLUE_AI_HANDSON_ATTENDEE/mod"
S3_DEST+="els/day1/checkpoints/"

aws s3 cp --recursive ./checkpoints "$S3_DEST"
```

- `S3_DEST`はAWS上の保存先をまとめて覚える変数です。講師の認証ファイル内のバケット名と受講者IDから作り、説明用の例なら `s3://example-handson-workshop01/attendee01/models/day1/checkpoints/` になります。`models/day1`はこの保存例の分類名で、通し実習の `models/学習実行名/` とは別です。[モデル回収](../aws-model-recovery.md)を進めている場合は、そちらの保存先と取得手順を使います。
- 認証情報ファイルの場所は、講師から別の場所を案内された場合はそれに従います。
- `./checkpoints`: 保存するフォルダ。`models/day1/checkpoints/` は保存先で、変えてもかまいません。

エラーが表示されずに、`upload:` で始まる行がファイルごとに表示されれば成功です。

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

EC2 で AWS CLI を使うときは、講師が用意した一時認証情報を読み込んでから実行し、有効期限切れなら再配布を依頼してください。`aws s3 cp` の成功だけで回収完了とせず、手元へ戻したファイルのサイズ・内容または `cmp` も確認します。

## 導入先を変更した場合の片付け {#custom-directory}

導入時に `--dir` を指定した場合は、実際の導入先を削除します。残す成果を先に回収し、対象を確かめてから[片付け](../finish.md)の削除コマンドのパスを導入先へ置き換えてください。

## チェックポイントのリンクと転送オプション {#checkpoint-links}

`checkpoints/last` が別のチェックポイントへのシンボリックリンクでも、リンク先のファイルを `last/` の名前で転送します。手元では `last` は通常のディレクトリになります。各ステップのチェックポイントも回収します。[AWS CLI のリンクの扱い](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)も参照してください。

`--recursive` はフォルダ内の各ファイルを、`--follow-symlinks` はリンク先の実体を転送する指定です。[モデル回収](../aws-model-recovery.md)では必要な指定を含めているので、変更せず使ってください。
