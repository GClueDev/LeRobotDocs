#### 2.4.3 ソフトウェアを入れる {#243-ソフトウェアを入れる}

[一時インスタンスの起動](<<= guide_link('staff/preparation/ami-launch.md#242') =>>)で AMI 作成用の一時 EC2 を起動した結果として表示された、`i-` で始まるインスタンス ID を使います。下の欄にその ID を入力して接続します。受講者用 EC2 の ID は使いません。

<div data-aws-values-panel data-aws-inline data-aws-fields="BUILD_INSTANCE_ID"></div>

1. Session Manager（シェル接続・ポート転送）で一時的なインスタンスに入ります（Session Manager プラグインが必要です）。

   AWS マネジメントコンソールの EC2 の画面で、インスタンスを選んで「接続」から「Session Manager」で入ることもできます。

   ```bash
   aws --profile {{PROFILE_SH}} --region {{REGION}} \
     ssm start-session --target {{BUILD_INSTANCE_ID}}
   ```

2. `ubuntu` ユーザーに切り替えます。

   ```bash
   sudo -i -u ubuntu
   ```

3. LeRobot を使う場合は、[導入スクリプト](<<= guide_link('staff/environment/scripts/setup-lerobot-ec2.sh') =>>)を EC2 にコピーして実行します。

    !!! warning "一括導入の確認範囲"
        このスクリプトの EC2 上での一括実行は未検証です。手動導入の実測結果とは区別し、一時的な検証用 EC2 で確認してから採用してください。[同梱スクリプトの検証記録](<<= guide_link('staff/environment/verification.md#script-verification') =>>)に確認済みの範囲をまとめています。

   Ubuntu 24.04・x86_64・Python 3.12・GPU ドライバー導入済みの EC2 が対象です。導入先と固定する版は [インフラ構成の仕様](<<= guide_link('staff/environment/specs/infrastructure.md#ec2-のソフトウェア導入スクリプト') =>>) を参照してください。

   **手元の ターミナル** で、LeRobotDocs の直下から次を実行し、表示された全文をコピーします。

   ```bash
   SETUP_SCRIPT=docs-aws-attendee/staff/environment/scripts/
   SETUP_SCRIPT+=setup-lerobot-ec2.sh
   base64 < "$SETUP_SCRIPT" | fold -w 76
   ```

   **EC2 の ターミナル**（`sudo -iu ubuntu` で切り替えた `ubuntu` ユーザー）で、次の 1 行を実行します。

   ```bash
   base64 -d > ~/setup-lerobot-ec2.sh <<'SETUP_BASE64'
   ```

   コピーした全文を貼り付け、最後に新しい行で `SETUP_BASE64` と入力して Enter を押します。その後、実行します。

   ```bash
   bash ~/setup-lerobot-ec2.sh
   ```

   既に SSH の接続先を設定している場合は、base64 の代わりに手元で次を実行してコピーできます。下の SSH 接続先欄へ、接続確認済みの Host 名を入力します。例: `ubuntu@ami-builder.local`。この工程では、一時 EC2 へ接続するために用意した SSH 接続先だけを使います。受講者 EC2 用の `gclue-ai-handson-{{EVENT_ID}}` は AMI 作成元の接続先ではありません。


<div data-aws-values-panel data-aws-inline data-aws-fields="SSH_HOST"></div>

   ```bash
   SETUP_SCRIPT=docs-aws-attendee/staff/environment/scripts/
   SETUP_SCRIPT+=setup-lerobot-ec2.sh
   scp "$SETUP_SCRIPT" {{SSH_HOST_SH}}:~/setup-lerobot-ec2.sh
   ```

   導入が成功したら、EC2 で次を実行します。GPU が使えることと、各コマンドの版・ヘルプが表示されることを確かめます。

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   aws --version
   ffmpeg -version
   git lfs version
   cd ~/lerobot
   uv run --no-sync python - <<'PY'
   import av
   import torch
   import torchcodec

   print(
       torch.__version__,
       torch.cuda.is_available(),
       av.__version__,
       torchcodec.__version__,
   )
   PY
   uv run --no-sync lerobot-train --help
   uv run --no-sync lerobot-edit-dataset --help
   uv run --no-sync rerun --version
   ```

   - `--check-gpu` は GPU で小さな行列計算を行う任意の確認です。
   - `--cache-resnet18` は画像特徴抽出用の ResNet18 の事前学習済み重みを取得する任意オプションです。[ACT（Action Chunking with Transformers）](https://huggingface.co/docs/lerobot/act)は、手本の操作からロボットの動かし方を学習する AI モデルです。ACT がカメラ画像を処理する部分に ResNet18 を使うため、その重みを事前に用意します。ACT 全体の操作モデルを取得するオプションではありません。
   - GPU 計算と重みの事前取得は、EC2 の実機では未検証です。
   - 導入先を変える場合は `--lerobot-dir /home/ubuntu/<フォルダ>` を追加し、確認時の `cd` もそのフォルダに変えます。
   - Amazon DCV（リモートデスクトップ接続）の ターミナル 内で `Monospace 12pt` を設定する場合は `--terminal-font` を追加します。SSM のシェルではこのオプションを付けません。
   - `sudo`、通信、空き容量のエラーは原因を解消してから同じコマンドを再実行します。既存の uv・AWS CLI の版が異なる場合は管理者に確認します。LeRobot の版が異なる場合や変更がある場合は、必要なら `--lerobot-dir` で別の配置先を指定します。
   - GPU の確認で失敗した場合は `nvidia-smi` の出力を管理者に共有します。CPU のみの環境に導入する場合は `--check-gpu` を省略します。

   データセットを Git で取得した場合は、そのフォルダで次を実行してから Rerun や編集ツールを使います。Git LFS が管理するデータファイル本体を取得するためです。通常は clone 時にも取得されますが、未導入・自動取得の無効化などで参照情報だけが残ることがあります。`fetch` で本体をダウンロードし、`checkout` で作業フォルダの参照情報を本体へ置き換えます。取得後は動画の再生や Rerun の表示を確認します。

   ```bash
   git lfs fetch
   git lfs checkout
   ```

   LeRobot 以外のソフトウェアは、その公式の導入手順に従って導入・動作確認します。`/opt/handson` には置かないでください（講師の一斉配布が管理する場所です）。

4. AMI の条件を満たしていることを確かめます。

   ソフトウェアを入れた後も、SSM Agent（EC2 側で接続・操作を受け付けるソフトウェア）、ed25519 のホスト鍵を持つ sshd、`git`、`flock`、GNU の `date`、`ubuntu` ユーザーへのパスワードなしの `sudo` が使える必要があります（DCV を使う講習会では DCV サーバーも。条件は [インフラ構成の仕様](<<= guide_link('staff/environment/specs/infrastructure.md') =>>) の「AMI」）。
   `exit` で `ubuntu` ユーザーから抜け、Session Manager で入ったユーザーのまま、[（任意）インスタンスの中身を確かめる](<<= guide_link('staff/preparation/verify.md#54') =>>) と同じ確認のコマンドを実行します。
   `sudo-ok`、`sshd-ok`、`hostkey-ok` と、`git` と `flock` の場所の 2 行が表示されれば満たしています。

5. AMI に残してはいけないものを消します。

   作業中に置いた AWS の認証情報があれば消します。

   ```bash
   sudo rm -rf /root/.aws /home/ubuntu/.aws
   ```

   パッケージとダウンロードの一時ファイルを消します。
   あらかじめ取得した ResNet18 の重み（`~/.cache/torch/hub/checkpoints/`）は残ります。

   ```bash
   sudo apt-get clean
   ```

   ```bash
   sudo rm -rf /home/ubuntu/.cache/pip /root/.cache/pip
   ```

   コマンドの履歴を消します。

   ```bash
   sudo rm -f /root/.bash_history /home/ubuntu/.bash_history
   ```

   `exit` で Session Manager から抜けます。
