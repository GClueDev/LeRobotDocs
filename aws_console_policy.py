"""Project the authoritative event YAML into static documentation."""
from pathlib import Path
import hashlib
import html
import logging
import os
import re
import yaml


class UniqueSafeLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def read_policy():
    selected = os.environ.get("LEROBOT_HANDSON_CONFIG")
    if selected is None:
        return {"enabled": True, "source": "未指定（通常プレビュー）",
                "sha256": "—", "explicit": False}
    if not selected.strip():
        raise ValueError("LEROBOT_HANDSON_CONFIG must select an event YAML")
    path = Path(selected).expanduser().resolve(strict=True)
    raw = path.read_bytes()
    data = yaml.load(raw, Loader=UniqueSafeLoader)
    def check_location(node, location=()):
        if isinstance(node, dict):
            for key, child in node.items():
                path = location + (key,)
                if key == "attendee_console_access" and path != (
                    "aws", "handson", "attendee_console_access"
                ):
                    raise ValueError("attendee_console_access is misplaced")
                check_location(child, path)
        elif isinstance(node, list):
            for child in node:
                check_location(child, location)
    check_location(data)
    for namespace in ("aws", "handson"):
        if not isinstance(data, dict) or namespace not in data:
            raise ValueError(f"Event YAML requires namespace: {namespace}")
        data = data[namespace]
    if not isinstance(data, dict):
        raise ValueError("aws.handson must be a mapping")
    value = data.get("attendee_console_access", True)
    if type(value) is not bool:
        raise ValueError("aws.handson.attendee_console_access must be bool")
    return {"enabled": value, "source": html.escape(path.name).replace("|", "&#124;").replace("`", "&#96;"),
            "sha256": hashlib.sha256(raw).hexdigest(), "explicit": True}


def define_policy(env):
    if "attendee_console_access" in env.conf.get("extra", {}):
        raise ValueError("Use the event YAML, not extra.attendee_console_access")
    policy = read_policy()
    audience = env.conf.get("extra", {}).get("audience")
    if audience not in {"attendee", "staff", "instructor", "environment"}:
        raise ValueError("Unknown documentation audience")
    env.variables["attendee_console_access"] = policy["enabled"]
    env.variables["console_policy"] = policy
    # Watch the selected YAML; never expose its other fields to templates.
    if policy["explicit"]:
        env.conf.setdefault("watch", []).append(
            str(Path(os.environ["LEROBOT_HANDSON_CONFIG"]).expanduser().resolve())
        )
    logging.getLogger("mkdocs").info(
        "Console policy: audience=%s, YAML=%s, bool=%s, SHA256=%s",
        audience, policy["source"], str(policy["enabled"]).lower(),
        policy["sha256"],
    )


def on_pre_page_macros(env):
    policy = env.variables["console_policy"]
    audience = env.conf["extra"]["audience"]
    page = env.variables["page"].file.src_uri
    notice = ""
    if not policy["enabled"]:
        notice = ('!!! warning "このビルド：受講者のAWSコンソール手順は無効"\n'
                  '    CLI・SSM（シェル接続）・SSH・Amazon DCV（リモートデスクトップ接続）を使用します。'
                  'これは静的な資料の設定であり、AWS側の適用確認ではありません。\n\n')
    summaries = {"index.md", "common.md", "staff/preparation.md",
                 "staff/preparation/event-settings.md",
                 "staff/instructor/index.md", "staff/environment/index.md"}
    if audience != "attendee" and page in summaries:
        status = "有効" if policy["enabled"] else "無効（掲載しません）"
        audience_label = {
            "attendee": "受講者",
            "staff": "講習会側（講師・環境構築担当者）",
            "instructor": "講師",
            "environment": "環境構築担当者",
        }[audience]
        console_status = "掲載する（true）" if policy["enabled"] else "掲載しない（false）"
        summary = f"""

## このビルドで有効・無効な手順

<table class="aws-build-summary">
<thead><tr><th>項目</th><th>このビルドの設定</th></tr></thead>
<tbody>
<tr><td>対象読者</td><td>{audience_label}</td></tr>
<tr><td>読み込んだ講習会設定ファイル</td><td>{policy['source']}</td></tr>
<tr><td>設定ファイルの照合値（SHA-256）</td><td><code>{policy['sha256']}</code></td></tr>
<tr><td>受講者の AWS コンソール利用手順<br>（設定名：<code>aws.handson.attendee_console_access</code>）</td><td>{console_status}</td></tr>
<tr><td>受講者のコンソールURL生成・直接操作・S3画面リンク</td><td>{status}</td></tr>
<tr><td>講師による受講者向けコンソールURLの配布案内</td><td>{status}</td></tr>
<tr><td>講師・構築担当者自身の管理コンソール手順</td><td>有効（管理者自身の権限を使用）</td></tr>
<tr><td>CLIによるS3転送・SSM（シェル接続）・SSH・Amazon DCV（リモートデスクトップ接続）</td><td>有効</td></tr>
</tbody>
</table>

講習会設定ファイルは、AWS 環境と講習資料に共通で使う設定ファイルです。照合値（SHA-256）は、同じ入力ファイルを使ったかを確認するための値です。

この表は資料に掲載する手順の設定を示します。実際の AWS の権限設定を確認した証明ではありません。設定ファイルを指定しない通常プレビューでは、互換性のためコンソール利用手順を掲載します（true）。開催用の配布資料は、AWS 環境の構築に使った正本の設定ファイルを指定して再ビルドしてください。ブラウザの各種値や JSON インポートでこの設定は変更できません。

コンソール利用手順を掲載しない設定（false）へ変更する場合は、同じ正本の設定ファイルを変更 → AWS Sign-Inの有効化状態を確認 → CDK deploy → 受講者・インスタンスロールのIAM適用を確認 → 資格情報の払い出しと資料の再ビルド、の順で進めます。資料だけを非掲載（false）にしても AWS のアクセスは拒否されません。

---

"""
        # Insert after the first source heading, keeping it as the page title.
        markdown = env.markdown
        match = re.search(r"^# [^\n]+\n", markdown, re.M)
        if match:
            env.markdown = markdown[:match.end()] + summary + markdown[match.end():]
        else:
            env.markdown = markdown + summary
    env.markdown = notice + env.markdown
