# 講習会終了時の片付け

右上の「各種値の設定」で、講師から受け取った値を確認してください。認証情報ファイルのパス・期限付きURLは保存せず、指定箇所を手動で置き換えます。

**この工程は手順・実装照合のみで、今回の終了時実測は未実施です。** 残したい成果の回収・内容確認を完了してから進めます。EC2 の停止・削除や AWS 資源の撤去は講師・構築担当者が行います。

実行場所: **手元の PC**。共通値の開催 ID と削除対象が一致していることを確認してください。確認に答える前に表示されたパスを確かめます。

## 10. 講習会の終了後に片付ける

手元の機器から、講習会用の環境をすべて削除します。
自分専用の場所に保存した成果のうち残したいものは、先に[成果の保存と回収](save.md)で手元に取得しておきます。

1. 講習会用の環境を有効にしているターミナルでは、元に戻します。

   ```bash
   gclue_ai_handson_deactivate
   ```

2. 講習会用のフォルダを削除します。

   ```bash
   rm -ri "$HOME/gclue-ai-handson/{{EVENT_ID}}"
   ```

   導入先を変更した場合は[削除対象の確認](reference/files.md#custom-directory)を参照してください。

3. `ssh-config` を使った場合は、`~/.ssh/config` に追加した `Include "…"` の行を削除します。
4. 受け取った認証情報ファイル（`{{ATTENDEE_ID}}.env`。同時に配布された場合は `.credentials` も）と、取得した `bootstrap.sh` を削除します。

ダウンロード先の認証情報と追加したSSH設定も片付けたことを確認します。回収して残す成果は削除しません。
[PC の準備](setup.md)で入れたソフトウェアは、ほかに使わなければアンインストールしてかまいません。

{% if audience == "staff" %}

## 講師：全員の回収後の片付け

未回収者がいないことを確認してから実施し、結果を環境構築担当者へ渡します。

{% filter staff_headings %}
{% include 'instructor/closing/02.md' %}
{% endfilter %}

{% filter staff_headings %}
{% include 'instructor/closing/03.md' %}
{% endfilter %}

{% endif %}

{% if audience == "staff" %}

## 環境構築担当者：環境の撤去

講師から回収・失効・バックアップの確認結果を受け取ってから実施します。再利用するAMIは開催環境の撤去と分けます。

{% filter staff_headings %}
{% include 'environment/procedures/environment/11.md' %}
{% endfilter %}

{% filter staff_headings %}
{% include 'environment/procedures/environment/12.md' %}
{% endfilter %}

{% endif %}
