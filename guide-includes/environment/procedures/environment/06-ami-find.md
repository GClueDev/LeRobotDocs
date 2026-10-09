### 2.4 （任意）ソフトウェアを導入済みの AMI を用意する

選定済みの開催用 AMI ID を入力して状態を確認します。例: `ami-0123456789abcdef0`。これから作成する元の AMI や、作成直後の ID は別の欄で扱います。

<div data-aws-values-panel data-aws-inline data-aws-fields="AMI_ID"></div>

[AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>) の AMI（以下「元の AMI」）に講義で使うソフトウェアを入れた AMI（以下「導入済みの AMI」）を使うと、受講者全員のインスタンスが、そのソフトウェアが入った状態で起動します。
導入済みの AMI は、特定の開催のものではなく、同じ AWS アカウント・リージョンの複数の開催で使い回せます。
前の開催で作った導入済みの AMI を使うのが通常で、[作ってある導入済みの AMI を探す](<<= guide_link('staff/preparation/ami-find.md#241-ami') =>>) で見つかれば、その AMI ID を設定ファイルに書くだけで済みます。
新しく作るのは、使える導入済みの AMI がない場合だけです（[一時的なインスタンスを起動する](<<= guide_link('staff/preparation/ami-launch.md#242') =>>)〜[AMI を作る](<<= guide_link('staff/preparation/ami-create.md#244-ami') =>>)）。
AMI の作成は AWS CLI で手動で行い、LeRobot の導入にはインフラリポジトリのシェルスクリプトを使います（理由は [インフラ構成の仕様](<<= guide_link('staff/environment/specs/infrastructure.md') =>>) の「AMI」）。
[AMI を選ぶ](<<= guide_link('staff/preparation/event-settings.md#23-ami') =>>) の AMI に必要なソフトウェアがそろっている場合は、[（任意）ソフトウェアを導入済みの AMI を用意する](<<= guide_link('staff/preparation/ami-find.md#24-ami') =>>) を飛ばして [ルートデバイス名を調べる](<<= guide_link('staff/preparation/placement.md#25') =>>) へ進みます。

#### 2.4.1 作ってある導入済みの AMI を探す

1. このアカウント・リージョンにある導入済みの AMI の ID、名前、作成日時、説明を表示します。

   説明には、入れたソフトウェアが書いてあります。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 describe-images --owners self \
     --filters Name=tag-key,Values=gclue-ai-handson-ami \
     --query 'Images[].[ImageId,Name,CreationDate,Description]' \
     --output text
   ```

2. 講義に合うものがあれば、その AMI の状態を確かめます。

   1 行目に `available` とルートデバイス名、2 行目以降にディスクごとのデバイス名・大きさ（GB）・スナップショット ID が表示されます。
   ルートデバイス名の行の大きさが、設定ファイルの `root_volume_size_gb` 以下であることを確かめます。

   ```bash
   QUERY='Images[0].[[State,RootDeviceName],BlockDeviceMappings[].'
   QUERY+='[DeviceName,Ebs.VolumeSize,Ebs.SnapshotId]]'

   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ec2 describe-images --image-ids {{AMI_ID}} --query "$QUERY" \
     --output text
   ```

3. 使える AMI があれば、設定ファイルの `aws.handson_cdk.instance.ami_id` にその AMI ID を書き、[注意](<<= guide_link('staff/preparation/ami-create.md#245') =>>) の注意を読んでから [ルートデバイス名を調べる](<<= guide_link('staff/preparation/placement.md#25') =>>) へ進みます。

   使える AMI がなければ、[一時的なインスタンスを起動する](<<= guide_link('staff/preparation/ami-launch.md#242') =>>) から新しく作ります。
