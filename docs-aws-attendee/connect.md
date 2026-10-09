# EC2 への接続

実行場所: **手元の PC の、受講者環境を有効化したターミナル**。
まだ有効化していない場合は、[PC の準備](setup.md#3)へ戻ってください。
このページでは、自分の EC2 のデスクトップを開きます。

## 1. 初回ログイン用のパスワードを決める {#first-connection}

まず手元で次を実行し、自分の EC2 へ接続します。

```bash
gclue-ai-handson-attendee shell
```

接続後のプロンプトは **EC2 側**です。ユーザーは `ssm-user` で正常です。
DCV（リモートデスクトップ）で使う `ubuntu` のパスワードを、EC2 側で設定して手元へ戻ります。

```bash
sudo /var/lib/handson/bin/handson-dcv-password set
exit
```

表示に従って8文字以上のパスワードを2回入力します。文字は画面に表示されません。
`ubuntu のパスワードを設定しました。` を確認してから `exit` で接続を終了します。
設定済みの場合は、この段階を省略できます。

## 2. EC2 のデスクトップを開く

手元に戻った同じターミナルで実行します。

```bash
gclue-ai-handson-attendee dcv
```

表示された `https://localhost:8443/` を **同じ PC のブラウザ**で開き、
ユーザー名 `ubuntu` と先ほど設定したパスワードでログインしてください。
デスクトップが表示されれば成功です。
このターミナルは接続のために開いたままにし、終了するときだけ Ctrl+C を押します。

[ポートが使用中・パスワード忘れ・証明書の警告](reference/connect.md#dcv)は逆引きページを確認してください。
次は手元の Jetson／Mac に戻り、[ロボットとカメラの接続確認](lerobot/check.md)へ進みます。DCV の接続用ターミナルは開いたまま、手元の操作には別のターミナルを使い、[導入時の有効化](setup.md#3)を行ってから続けてください。

学習を行わない基本コースでは、手元の収集・学習・推論を省略し、[配布教材の確認](dataset.md)へ進みます。

別の方法で作業する場合の [SSH・VS Code 接続](reference/connect.md#ssh)、
[Git の送受信](reference/connect.md#git)は逆引きページにあります。
{% if attendee_console_access %}
[AWS コンソール](reference/connect.md#console)や
[S3 の画面](reference/connect.md#s3-console)を開く方法も、必要なときに参照してください。
{% endif %}

{% if audience == "staff" %}

## 講師：接続の到達確認

受講者本人の画面で、接続先・ログインユーザー・終了方法を順に確認します。

{% filter staff_headings %}
{% include 'instructor/support/02.md' %}
{% endfilter %}

{% filter staff_headings %}
{% include 'instructor/support/04.md' %}
{% endfilter %}

{% endif %}
