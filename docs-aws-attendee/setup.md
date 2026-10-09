# 手元の PC の準備

実行場所: **手元の PC のターミナル**。このページでは、受講者用のコマンドと教材を用意します。
macOS での導入は実測済みです。Ubuntu / Jetson / WSL は元手順に基づく案内で、今回の端末実測には含めません。

最初に「各種値の設定」へ、講師から受け取った設定JSONをインポートしてください。
JSONがない場合も、右上の「各種値の設定」で講師から受け取った値を入力します。
入力方法の詳細は [設定の使い方](common.md)で確認できます。
認証情報ファイルの場所と期限付き URL はフォームに保存せず、下のコマンドで指定します。

## 用意するもの

| 講師から受け取るもの | 使い方 |
| --- | --- |
| `{{ATTENDEE_ID}}.env` | 自分として AWS に接続するための認証情報。手元の PC に保存する |
| 各種値の設定JSON | 受け取った場合は「各種値の設定」の「インポート」で読み込む |
| 導入スクリプトの URL | `https://` で始まる期限付き URL。受け取ったら早めに使う |

通常の配布では `.env` だけを使います。講師が `aws-profile` 形式で発行した場合だけ、
一緒に渡された `.credentials` も同じフォルダに保存します。
認証情報はあなたとして AWS を操作できる鍵です。他人に渡したり、チャットに貼り付けたりしないでください。
講師には、この資料が前提とする修正版（修正 `fc6e58d` を含む版）のツールと教材が公開済みであることを確認してください。

## 1. 手元の PC のソフトウェアを確認する

次をまとめて実行し、バージョンが表示されることを確認します。
AWS CLI は `aws-cli/2.` で始まる表示を使います。

```bash
bash --version
curl --version
aws --version
session-manager-plugin --version
ssh -V
git --version
```

bash・curl は導入に、AWS CLI は AWS の操作に、Session Manager プラグインは EC2 への接続に使います。
SSH・git は後の教材取得や接続で使います。
見つからないものがある場合は、[OS 別のソフトウェア導入](reference/setup.md#dependencies)を先に進めてください。
Linux で AWS CLI を導入スクリプトに入れてもらう場合は、ここで見つからなくてもかまいません。

{% if audience == "staff" %}

## 講師：導入前の認証情報の発行

以下は講師の運用環境で実行します。受講者に導入URLと本人の認証ファイルを渡してから、受講者の導入手順へ進みます。

{% filter staff_headings %}
{% include 'instructor/operations/06.md' %}
{% endfilter %}

{% endif %}

## 2. 受講者用のコマンドと教材を用意する

講師から受け取った URL から導入スクリプトを取得し、自分の認証情報ファイルを指定して実行します。
`<...>` を実際の値に置き換え、前後の引用符は残してください。

```bash
curl -fsSL '<導入スクリプトの URL>' -o bootstrap.sh
bash bootstrap.sh --env-file '<認証情報ファイルの絶対パス>'
```

認証情報ファイルの場所の例は、Macなら `/Users/student/Downloads/user01.env`、
Jetsonなら `/home/student/Downloads/user01.env` です。
`student` は本人の端末のユーザー名、`user01.env` は配布された自分のファイル名に置き換えます。
認証情報の本文を貼り付ける欄ではありません。

最後に `gclue-ai-handson の実行環境を用意しました:` と、開催 ID・受講者 ID が表示されれば成功です。
自分に配布された ID と一致することを確認します。
コマンドと教材は既定で `~/gclue-ai-handson/{{EVENT_ID}}/` に用意され、
管理者権限（sudo）は使いません。
[保存先や教材の版を変更する場合](reference/setup.md#install-options)は、講師の指示を確認してください。

## 3. このターミナルで使えることを確認する

新しくターミナルを開くたびに、次を実行します。
`{{EVENT_ID}}` には導入時に表示された開催 ID（例: `p1test`）を使います。
「各種値の設定」に同じ開催 ID を入力しておくと、このコードにも反映されます。

```bash
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
gclue-ai-handson-attendee env info
```

開催 ID・受講者 ID が自分のもの、認証情報の有効期限が現在より後であることを確認してください。
このターミナルを続けて使い、次の [EC2 への接続](connect.md)へ進みます。

講師から案内があった場合の [ツール・教材の更新](reference/setup.md#update)、
[認証情報の更新](reference/setup.md#credentials)、
[有効化を戻す方法・ヘルプ](reference/setup.md#help)は逆引きページにあります。

{% if audience == "staff" %}

## 講師：導入・更新後の確認

本人の開催ID・受講者ID・有効期限を確認します。

{% filter staff_headings %}
{% include 'instructor/support/01.md' %}
{% endfilter %}

{% endif %}
