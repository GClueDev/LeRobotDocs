# 導入・更新の逆引き

[PC の準備](../setup.md)の通常手順から、必要な項目だけ開いてください。
実行場所は **手元の PC のターミナル**です。

## 必要なソフトウェアを入れる {#dependencies}

使う機器の OS に合わせて準備します。
自分の EC2 へ接続しない機器（データのやり取りだけに使う Jetson など）では、Session Manager プラグイン（SSM 経由のシェル接続・ポート転送用）・OpenSSH・git は不要です。

| ソフトウェア | 用途 |
| --- | --- |
| bash・curl | 導入スクリプトと講習会用のコマンドの実行 |
| AWS CLI v2 | AWS の操作 |
| Session Manager プラグイン | EC2 へのシェル接続と、SSH・リモートデスクトップ用のポート転送 |
| OpenSSH（`ssh`・`ssh-keygen`） | SSH・git・VS Code での接続 |
| git | 手元のリポジトリと自分の EC2 のやり取り |

### macOS の場合

macOS に最初から入っている bash と curl をそのまま使えます。
AWS CLI v2 と Session Manager プラグインは、次の AWS の公式の手順で入れます。
導入スクリプトは、macOS には AWS CLI v2 を自動では入れません。

- AWS CLI v2: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- Session Manager プラグイン: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

git が入っていない場合は、ターミナルで `git` を実行すると表示される案内に従って入れます。

### Linux（Ubuntu・Jetson）の場合

curl・unzip・git・OpenSSH を入れます。

```bash
sudo apt install curl unzip git openssh-client
```

AWS CLI v2 が入っていなければ、導入スクリプトが講習会用のフォルダの中に入れます（x86_64 と aarch64 の機器に対応）。
Session Manager プラグインも、導入スクリプトの `--with-ssm-plugin` で講習会用のフォルダの中に入れられます。

### Windows の場合

Windows では WSL（Windows Subsystem for Linux）の Ubuntu の中で使います。
WSL の Ubuntu を入れたら、Ubuntu のターミナルを開き、上の「Linux（Ubuntu・Jetson）の場合」と同じ手順で進めます。
以降のコマンドは、すべて WSL の Ubuntu のターミナルで実行します。

### 入ったことを確かめる

次のコマンドを 1 つずつ実行し、バージョンが表示されることを確かめます。

```bash
bash --version
```

```bash
curl --version
```

```bash
aws --version
```

`aws --version` は `aws-cli/2.` で始まる表示であれば使えます。
Linux で AWS CLI を導入スクリプトに入れてもらう場合は、ここで見つからなくてもかまいません。

自分の EC2 へ接続する機器では、次も確かめます。

```bash
session-manager-plugin --version
```

```bash
ssh -V
```

```bash
git --version
```

## 導入方法を変える {#install-options}

通常は [PC の準備](../setup.md)の `bash bootstrap.sh --env-file ...` を使います。
講師から指示があった場合だけ、次のオプションを同じコマンドの末尾に付けます。

| オプション | 使う場面 |
| --- | --- |
| `--with-ssm-plugin` | Linux で Session Manager プラグインが入っていないとき。講習会用のフォルダの中に入れます |
| `--version <版>` | 講師から特定の講義資料の版を指示されたとき |
| `--no-materials` | 講義資料を取得せず、コマンドだけを用意するとき |
| `--dir <フォルダ>` | 既定とは別の場所に用意するとき |
| `--no-hook` | 講義資料に含まれる機器の準備作業を実行しないとき（講師から指示された場合だけ） |

講義資料がまだ公開されていない場合は、資料を取得せずに終わります。
公開後に下の「講習会用の環境を更新する」で取得できます。


`--dir` で保存先を変えた場合は、表示されたフォルダの `activate` を読み込みます。
同じ導入コマンドの再実行は、同じフォルダの内容を更新します。

## 有効化を戻す・コマンドの使い方を調べる {#help}

元の状態に戻すには次を実行します。

```bash
gclue_ai_handson_deactivate
```

各コマンドの使い方は `-h` で表示できます。次は保存・回収の説明を開く例です。

```bash
gclue-ai-handson-attendee files -h
```

## 講習会用の環境を更新する {#update}

講師から更新するよう案内があったら、次のコマンドを実行します。
講習会用のコマンドと、講師が公開している最新の講義資料を取得し直します。

```bash
gclue-ai-handson-attendee env update
```

`講義資料の版 <版> を … に用意しました。` と表示されれば成功です。
講義資料は `~/gclue-ai-handson/{{EVENT_ID}}/materials/current/` から開けます。

- 特定の版を指示された場合は、`--version <版>` を付けます。
- コマンドだけを更新する場合は、`--tools-only` を付けます。

## 認証情報を入れ替える {#credentials}

認証情報には有効期限があります（`env info` の「認証情報の有効期限」）。
期限が切れたときや、講師から新しい認証情報ファイルを受け取ったときは、次のコマンドで入れ替えます。

```bash
gclue-ai-handson-attendee env credentials \
  --env-file '<新しい認証情報ファイルの絶対パス>'
```

- `<新しい認証情報ファイル>`: 新しく受け取った `{{ATTENDEE_ID}}.env` のパス。

`認証情報を … に置きました。` と表示されたら、開いているターミナルごとに `activate` を読み込み直します。

```bash
source ~/gclue-ai-handson/{{EVENT_ID}}/activate
```

`env info` で、認証情報の有効期限が新しくなっていることを確かめます。
