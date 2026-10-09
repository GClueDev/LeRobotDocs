#### 2.4.2 一時的なインスタンスを起動する

以下は AMI 作成専用の設定です。元の AMI・subnet・インスタンスプロファイルは管理者の指定と確認結果、名前・容量は今回の作業計画を入力します。開催用 AMI ID や受講者 EC2 ID は変更しません。

<div data-aws-values-panel data-aws-inline data-aws-fields="SOURCE_AMI_ID BUILD_PROFILE_NAME BUILD_AMI_NAME BUILD_VOLUME_GB"></div>

新しく作る前に、次のものを管理者から受け取っておきます（1.1）。

- 一時的なインスタンスに付けるインスタンスプロファイルの名前（AWS 管理ポリシー `AmazonSSMManagedInstanceCore` を付けたロールのもの）
- AMI を作る権限（一覧は [アクセス制御の仕様](<<= guide_link('staff/environment/specs/access-control.md') =>>) の「管理者の作業」。`AdministratorAccess` があれば足ります）

新しく作るときは、次を守ります。

- 元の AMI から起動した一時的なインスタンスだけから作ります。受講者が使った講習会のインスタンスからは作りません（受講者の成果や認証情報が AMI に入り、別の開催に持ち込まれるのを防ぐためです）。
- AMI の名前は `GClueAiHandsOn-AMI-<用途>-<作成日>` とします。`<用途>` は入れるソフトウェアを表す英小文字の短い語（例: `lerobot`）、`<作成日>` は `YYYYMMDD` の形の日付（例: `20261008`）です。以下、この名前を `{{BUILD_AMI_NAME}}` と書きます。

一時的なインスタンスは講習会のスタックの外のもので、作業が終わったら削除します。
このインスタンスも GPU の vCPU クォータを使うため、受講者のインスタンスと同時に動かす場合は 1.3 の計算に 1 台分を加えます。

1. インスタンスを置く subnet を選びます。

   既定の VPC の subnet と、その Availability Zone を表示します。
   2.6 の方法で、インスタンスタイプが提供されている Availability Zone の subnet を選んでください。
   何も表示されない場合は、インターネットに出られる既存の subnet の ID を管理者に確かめます。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 describe-subnets \
     --filters Name=default-for-az,Values=true \
     --query 'Subnets[].[SubnetId,AvailabilityZone]' --output text
   ```

   表示された SubnetId のうち、使用するものを下の欄へ入力します。例: `subnet-0123456789abcdef0`。

<div data-aws-values-panel data-aws-inline data-aws-fields="BUILD_SUBNET_ID"></div>

2. 元の AMI のルートデバイス名を表示します（例: `/dev/sda1`）。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 describe-images --image-ids {{SOURCE_AMI_ID}} \
     --query 'Images[0].RootDeviceName' --output text
   ```

   直前の RootDeviceName の出力を転記します。例: `/dev/sda1`。元の AMI について確認した値を使います。

<div data-aws-values-panel data-aws-inline data-aws-fields="BUILD_ROOT_DEVICE"></div>

3. 一時的なインスタンスを起動します。

   `{{INSTANCE_TYPE}}` は講習会と同じもの（例: `g6e.2xlarge`）にします。
   `{{BUILD_VOLUME_GB}}` はソフトウェアを入れられる大きさ（GB）にします。
   この値が新しい AMI のスナップショットの大きさになるため、設定ファイルの `root_volume_size_gb` 以下にしてください。
   表示された `i-` で始まる値が、一時的なインスタンスの ID です。

   ```bash
   BLOCK_DEVICES='DeviceName={{BUILD_ROOT_DEVICE}},Ebs={VolumeSize='
   BLOCK_DEVICES+='{{BUILD_VOLUME_GB}},VolumeType=gp3}'
   TAGS='ResourceType=instance,Tags=[{Key=Name,Value='
   TAGS+='{{BUILD_AMI_NAME}}-'
   TAGS+='build}]'
   INSTANCE_PROFILE='{"Name":"{{BUILD_PROFILE_NAME}}"}'

   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 run-instances --image-id {{SOURCE_AMI_ID}} \
     --instance-type {{INSTANCE_TYPE}} \
     --subnet-id {{BUILD_SUBNET_ID}} \
     --associate-public-ip-address \
     --iam-instance-profile "$INSTANCE_PROFILE" \
     --block-device-mappings "$BLOCK_DEVICES" \
     --tag-specifications "$TAGS" --query 'Instances[0].InstanceId' \
     --output text
   ```

   `run-instances` の最後に表示された `i-` の値を転記します。例: `i-0123456789abcdef0`。ここから停止・削除まで、同じ一時 EC2 の ID を使います。

<div data-aws-values-panel data-aws-inline data-aws-fields="BUILD_INSTANCE_ID"></div>

4. 起動が終わるまで待ちます。

   エラーが表示されずにコマンドが終われば、起動しています（数分かかります）。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 wait instance-status-ok \
     --instance-ids {{BUILD_INSTANCE_ID}}
   ```

   Session Manager で接続できることを確かめます。
   `Online` と表示されれば接続できます。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ssm describe-instance-information \
     --filters Key=InstanceIds,Values={{BUILD_INSTANCE_ID}} \
     --query 'InstanceInformationList[0].PingStatus' --output text
   ```
