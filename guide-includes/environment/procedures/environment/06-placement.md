### 2.5 ルートデバイス名を調べる

[共通設定](<<= guide_link('common.md') =>>) の AMI ID を [AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>) の値（[（任意）ソフトウェアを導入済みの AMI を用意する](<<= guide_link('staff/preparation/ami-find.md#24-ami') =>>) で導入済みの AMI にした場合はその AMI ID）へ更新して実行し、表示された値（例: `/dev/sda1`）を `root_device_name` に書きます。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-images --image-ids {{AMI_ID}} \
  --query 'Images[0].RootDeviceName' --output text
```

この値が AMI と違うと、指定した容量のディスクが起動ディスクにならず、追加のディスクになってしまいます。

直前の RootDeviceName の出力を下の欄へ転記し、YAML に同じ値を書きます。例: `/dev/sda1`。元 AMI 用のルートデバイス欄とは別です。

<div data-aws-values-panel data-aws-inline data-aws-fields="ROOT_DEVICE_NAME"></div>

```yaml
root_device_name: {{ROOT_DEVICE_NAME_YAML}}
```

### 2.6 Availability Zone を選ぶ

GPU インスタンスは、Availability Zone（リージョン内のデータセンターの区画）によっては提供されていないか、在庫が足りず起動できないことがあります。
インスタンスタイプが提供されている Availability Zone を表示します。

```bash
aws --profile {{PROFILE_SH}} --region {{REGION}} \
  ec2 describe-instance-type-offerings \
  --location-type availability-zone \
  --filters Name=instance-type,Values={{INSTANCE_TYPE}} \
  --query 'InstanceTypeOfferings[].Location' --output text
```

次のどちらかで書きます。

- **特に指定しない場合**: 記載例のまま（`max_azs: 2`、`availability_zones` と `availability_zone` は書かない）にします。インスタンスは自動で選ばれた Availability Zone に置かれます。
- **インスタンスを置く Availability Zone を指定する場合**: 次の 3 つをそろえて書きます。
  - `max_azs` の行を消す（`availability_zones` と同時には書けません）
  - `availability_zones` に、表示された中から 2 つを書く
  - `availability_zone` に、そのうちインスタンスを置く 1 つを書く

明示指定する場合だけ、表示された Location から異なる2つの AZ を下の欄へ入力します。例: `ap-northeast-1a` と `ap-northeast-1c`。自動選択なら両方とも空欄のまま、この YAML は使いません。

<div data-aws-values-panel data-aws-inline data-aws-fields="PRIMARY_AZ SECONDARY_AZ"></div>

```yaml
    network:
      vpc_cidr: 10.80.0.0/16
      availability_zones:
        - {{PRIMARY_AZ_YAML}}
        - {{SECONDARY_AZ_YAML}}
    instance:
      availability_zone: {{PRIMARY_AZ_YAML}}
```

提供されていても在庫が足りないことはあり、在庫は構築するまで分かりません。
足りなかったときの対処は「うまくいかないとき」にあります。
