### 2.5 ルートデバイス名を調べる

[共通設定](<<= guide_link('common.md') =>>) の AMI ID を [AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>) の値（[（任意）ソフトウェアを導入済みの AMI を用意する](<<= guide_link('staff/preparation/ami-find.md#24-ami') =>>) で導入済みの AMI にした場合はその AMI ID）へ更新して実行し、表示された値（例: `/dev/sda1`）を、開催の設定ファイル（`{{CONFIG_DIR}}/gclue-ai-handson-config.yml`）の `aws.handson_cdk.instance.root_device_name`（起動ディスクのデバイス名）へ転記します。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-images --image-ids {{AMI_ID}} \
  --query 'Images[0].RootDeviceName' --output text
```

この値が AMI と違うと、指定した容量のディスクが起動ディスクにならず、追加のディスクになってしまいます。

直前の AMI 情報確認コマンドで表示された起動ディスクのデバイス名を、下の欄へ転記します。例: `/dev/sda1`。開催の設定ファイルにも同じ値を書いてください。フォームへの入力だけでは設定ファイルは更新されません。元 AMI 用のルートデバイス欄とは別です。

<div data-aws-values-panel data-aws-inline data-aws-fields="ROOT_DEVICE_NAME"></div>

以下は開催の設定ファイルの該当箇所の記載例です。

```yaml
aws:
  handson_cdk:
    instance:
      root_device_name: {{ROOT_DEVICE_NAME_YAML}}
```

### 2.6 Availability Zone を選ぶ

AWS がその GPU インスタンスタイプを提供する Availability Zone（リージョン内のデータセンターの区画）と、AWS が今その区画で用意できる空き容量は別です。各区画で同時に用意できる GPU インスタンスの台数には、AWS 側の設備容量による限りがあります。他の利用者の使用などによって AWS 側の空き容量が不足し、提供対象の区画でも起動に失敗することがあります。

次のコマンドは、そのインスタンスタイプを提供する Availability Zone の一覧を表示します。リアルタイムの空き容量を確認・確保するコマンドではなく、起動できることを保証しません。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-instance-type-offerings \
  --location-type availability-zone \
  --filters Name=instance-type,Values={{INSTANCE_TYPE}} \
  --query 'InstanceTypeOfferings[].Location' --output text
```

開催の設定ファイルは、次のどちらかで記載します。

- **特に指定しない場合**: 記載例のまま（`max_azs: 2`、`availability_zones` と `availability_zone` は書かない）にします。インスタンスは自動で選ばれた Availability Zone に置かれます。
- **インスタンスを置く Availability Zone を指定する場合**: 次の 3 つをそろえて書きます。
  - `max_azs` の行を消す（`availability_zones` と同時には書けません）
  - `availability_zones` に、表示された中から 2 つを書く
  - `availability_zone` に、そのうちインスタンスを置く 1 つを書く

明示指定する場合だけ、表示された Location から異なる2つの AZ を下の欄へ入力します。例: `ap-northeast-1a` と `ap-northeast-1c`。下の欄に入力した値は、開催の設定ファイルの該当箇所にも書いてください。フォームへの入力だけではファイルは更新されません。自動選択なら両方とも空欄のまま、次の記載例は使いません。

<div data-aws-values-panel data-aws-inline data-aws-fields="PRIMARY_AZ SECONDARY_AZ"></div>

```yaml
aws:
  handson_cdk:
    network:
      vpc_cidr: 10.80.0.0/16
      availability_zones:
        - {{PRIMARY_AZ_YAML}}
        - {{SECONDARY_AZ_YAML}}
    instance:
      availability_zone: {{PRIMARY_AZ_YAML}}
```

起動時に `InsufficientInstanceCapacity` が出た場合は、[GPU の空き容量不足で起動できないとき](<<= guide_link('staff/environment/procedures/environment.md#insufficient-instance-capacity') =>>)へ進みます。これは AWS 側の空き容量不足です。アカウントの利用上限である vCPU クォータとは別で、クォータの引き上げでは空き容量不足を解消できません。
