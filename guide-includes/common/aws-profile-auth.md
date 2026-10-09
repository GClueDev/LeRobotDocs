利用する認証方式のタブを選びます。**以降のコマンドを実行する dev container 内の ターミナル** で準備してください。ホスト側の設定を共有していない場合、コンテナー内にも同じ名前のプロファイルが必要です。プロファイル名は入力欄の `{{PROFILE}}` を使います。

=== "IAM Identity Center"

    管理者から SSO の開始 URL・SSO リージョン・対象アカウント・権限セットを受け取ります。プロファイルが未定義なら、対話入力で準備します。既に定義済みなら設定を繰り返す必要はありません。

    ```bash
    aws configure sso --profile {{PROFILE_SH}}
    ```

    作業開始前と SSO の期限切れ時にログインします。ブラウザに表示された案内に従ってください。

    ```bash
    aws sso login --profile {{PROFILE_SH}}
    ```

    [AWS CLI の IAM Identity Center 設定](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)も参照できます。

=== "IAMユーザー"

    管理者から、この作業に必要な権限を持つ IAM ユーザーのアクセスキーを受け取ります。プロファイルが未定義なら、AWS CLI の対話入力で準備します。既に設定済みの有効なキーがあれば、この入力は不要です。

    ```bash
    aws configure --profile {{PROFILE_SH}}
    ```

    `AWS Access Key ID` と `AWS Secret Access Key` は ターミナル の対話プロンプトへ直接入力します。`Default region name` は `{{REGION}}`、`Default output format` は `json` を指定します。キーをコマンド引数・資料・このページの入力フォーム・設定JSONへ記載しません。キーは AWS CLI がローカルの `~/.aws/credentials`、プロファイル設定は `~/.aws/config` で管理します。このガイドの保存値とは別です。

    IAM ユーザーのキーを使う場合は `aws sso login` を実行しません。キーの無効化・更新時は管理者の案内に従ってプロファイルの設定を更新します。

    MFA や AssumeRole が必要な環境では、管理者から対象ロール・接続元プロファイル・認証手順を受け取ってください。上のキー設定だけで条件を満たすとは扱いません。この資料では MFA セッションの発行などを独自に追加せず、管理者が確認したプロファイルを以降の `PROFILE` と開催 YAML の `aws.profile` に指定します。

    [AWS CLI の名前付きプロファイルと認証設定](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)も参照できます。

どちらの方式でも、この後の `get-caller-identity` で対象アカウントと利用者・ロールを確認してから進みます。これは構築担当・講師自身の接続元の認証です。受講者への一時認証情報は、別工程でスタックの「払出し専用ユーザー」を使って発行します。
