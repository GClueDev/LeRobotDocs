## 2. 開催の設定ファイルを用意する

ここは構築の設定値です。構築担当・管理者が確定した内容を入力し、同じ内容を開催の設定ファイルに記載します。フォームを変えても設定ファイルは変更されません。AMI を作り直す工程の元・新・一時 ID は、この開催用 AMI の欄と区別します。

<div data-aws-values-panel data-aws-inline data-aws-fields="CONFIG_DIR EVENT_ID ACCOUNT_ID REGION PROFILE INSTANCE_TYPE AMI_ID"></div>

### 2.1 記載例をコピーする

[共通設定](<<= guide_link('common.md') =>>) の設定ディレクトリ（`{{CONFIG_DIR}}`）を使います。開催ごとに別のディレクトリにしてください。
`config/environments/` は Git の管理対象外です。

```bash
mkdir -p {{CONFIG_DIR_SH}}
```

```bash
cp config/env.template/gclue-ai-handson-config.yml {{CONFIG_DIR_SH}}
```

### 2.2 値を埋める

`{{CONFIG_DIR}}/gclue-ai-handson-config.yml` をエディタで開き、次の値を埋めます。

| 項目 | 埋める値 | 値の調べ方 |
| --- | --- | --- |
| `aws.profile` | 自分の作業環境に作った AWS CLI プロファイルの名前 | 自分で決める（作り方は [管理者に依頼するもの](<<= guide_link('staff/preparation/environment-start.md#11') =>>) の下の説明） |
| `aws.handson.deployment_id` | 開催 ID | [用意するもの](<<= guide_link('staff/preparation/environment-start.md#_6') =>>) |
| `aws.handson.account` | アカウント ID（12 桁。`"` で囲む） | [AWS アカウントの状態を確かめる](<<= guide_link('staff/preparation/environment-start.md#13-aws') =>>) で表示した値 |
| `aws.handson.region` | リージョン（例: `ap-northeast-1`） | 管理者から受け取る |
| `aws.handson.attendees` | 受講者 ID の一覧（1 件につき EC2 を 1 台作る。`shared` は使えない） | [用意するもの](<<= guide_link('staff/preparation/environment-start.md#_6') =>>) |
| `aws.handson.attendee_console_access` | 受講者のAWSコンソール利用。真偽値 `true` / `false`、省略時true。インフラと資料で同じ開催の設定ファイルを使用 | [コンソール利用設定の切替・適用確認](<<= guide_link('staff/environment/specs/access-control.md#false') =>>)に従う |
| `aws.handson.max_session_duration_seconds` | 受講者に渡す認証情報の有効期間の上限（秒、3600〜43200）。通常は 43200（12 時間）のまま | — |
| `aws.handson.dcv_port` | Amazon DCV（リモートデスクトップ接続）の待ち受けポート。通常は 8443 のまま | — |
| `aws.handson_cdk.network.vpc_cidr` | VPC の IP アドレスの範囲。アカウント内の他の VPC と重ならなければ記載例のまま | 下の VPC CIDR 確認コマンド |
| `aws.handson_cdk.network.availability_zones` / `max_azs` | [Availability Zone を選ぶ](<<= guide_link('staff/preparation/placement.md#26-availability-zone') =>>) を参照 | [Availability Zone を選ぶ](<<= guide_link('staff/preparation/placement.md#26-availability-zone') =>>) |
| `aws.handson_cdk.instance.ami_id` | AMI ID | [AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>)（[（任意）ソフトウェアを導入済みの AMI を用意する](<<= guide_link('staff/preparation/ami-find.md#24-ami') =>>) で導入済みの AMI にした場合はその AMI ID） |
| `aws.handson_cdk.instance.instance_type` | インスタンスタイプ。通常は `g6e.2xlarge` のまま | — |
| `aws.handson_cdk.instance.root_volume_size_gb` | ルートディスクの容量（GB）。通常は 512 のまま | — |
| `aws.handson_cdk.instance.root_device_name` | AMI のルートデバイス名 | [ルートデバイス名を調べる](<<= guide_link('staff/preparation/placement.md#25') =>>) |
| `aws.handson_cdk.instance.availability_zone` | インスタンスを置く Availability Zone（任意） | [Availability Zone を選ぶ](<<= guide_link('staff/preparation/placement.md#26-availability-zone') =>>) |
| `aws.handson_cdk.issuer.access_key_serial` | 1 のまま | 変えるのは [払出し用の鍵を作り直す](<<= guide_link('staff/environment/procedures/environment.md#64') =>>) のときだけ |

手元の ターミナル（インフラリポジトリ直下）で、既存 VPC の CIDR を確認します。表示された範囲と重ならない範囲を設定してください。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-vpcs --query 'Vpcs[].CidrBlock' --output text
```

### 2.3 AMI を選ぶ

今回の再現対象は **Ubuntu 24.04 / x86_64 / Python 3.12 / NVIDIA ドライバー導入済み** の AMI です。管理者から対象リージョンで利用できる AMI ID を受け取り、次で状態・OS の説明・アーキテクチャを確認します。`available`、`x86_64` と対象の説明が成功条件です。この時点では、まだインスタンスは起動していません。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-images --image-ids {{AMI_ID}} \
  --query 'Images[0].[State,Architecture,Name,Description]' \
  --output text
```

AMI の中身（OS、ドライバー、GPU）は、インスタンスを起動した後に、[（任意）インスタンスの中身を確かめる](<<= guide_link('staff/preparation/verify.md#54') =>>)で確かめます。

Ubuntu 22.04 の AMI は、同梱スクリプトの対象外です。DCV と NVIDIA ドライバーの導入はこのスクリプトに含まれないため、それらが備わる AMI を用意します。今回の資料では新しい AMI の取得・起動・作成を実施していません。

次の機能を使う講習会では、AMI に条件があります（理由は [インフラ構成の仕様](<<= guide_link('staff/environment/specs/infrastructure.md') =>>)）。

- DCV（リモートデスクトップ）で接続する: Amazon DCV サーバーを入れた AMI が必要です。Deep Learning AMI には入っていません。
- 受講者が SSH・git で接続する: SSH のサーバー（sshd）、`git`、`flock` が入っていて、Session Manager（シェル接続・ポート転送）で入ったユーザーから `ubuntu` ユーザーへパスワードなしで `sudo` できる AMI が必要です。Ubuntu の AWS 公式の AMI と Deep Learning AMI は、通常この条件を満たします。

講義に使う大きなソフトウェア（PyTorch、LeRobot とその依存など）が [AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>) の AMI に入っていない場合は、次の [（任意）ソフトウェアを導入済みの AMI を用意する](<<= guide_link('staff/preparation/ami-find.md#24-ami') =>>) で、それを入れた AMI を用意します。
