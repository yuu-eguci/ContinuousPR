# NOTE: ざくざく実装するためひとつのファイルにすべてまとめています。のちに整理します。

# Built-in modules.
import json

# Third-party modules.
import requests

# User modules.
import consts
import utils


# ロガーを取得します。
logger = utils.get_my_logger(__name__)

# api.github.com へのアクセスに使う http headers です。
HEADERS_FOR_API = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {consts.TOKEN_REPO_SCOPE}',
}


def create_pull(head_branch: str, base_branch: str) -> int:
    """api.github.com を使って PR を作成します。

    Args:
        head_branch (str): Head branch
        base_branch (str): Base branch

    Returns:
        int: Created issue number
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/pulls'
    payload = {
        'title': f'🚀 [Scheduled] {head_branch} to {base_branch}',
        'head': head_branch,
        'base': base_branch,
        'body': consts.PR_BODY,
    }
    res = requests.post(url, headers=HEADERS_FOR_API, data=json.dumps(payload))

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> dict します。
    dic = res.json()

    # Issue 番号を返します。
    # NOTE: api.github.com の文脈では PR も issue のひとつです。
    #       もともと int のはずですが明示的に int とします。
    return int(dic['number'])


if __name__ == '__main__':
    pass
