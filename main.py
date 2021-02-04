# Built-in modules.
import datetime
import argparse

# Third-party modules.
import pytz

# User modules.
import utils


# ロガーを取得します。
logger = utils.get_my_logger(__name__)
current_utc = datetime.datetime.now(tz=pytz.utc)
logger.info(f'Started at {current_utc.isoformat()}')
current_jst = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
logger.info(f'Started at {current_jst.isoformat()}')

# head branch と base branch を引数から取得します。
# head -> base の PR となります。
# NOTE: TOKEN 等は環境変数で良いですが、ブランチは実行ごとに可変にしたい。
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--head', type=str, help='head -> base',
                    default='dev')
parser.add_argument('-B', '--base', type=str, help='head -> base',
                    default='master')
args = parser.parse_args()
logger.info(f'PR [{args.head} -> {args.base}] will be made.')

# api を使って PR を作ります。

# NOTE: ここ以降の処理はすべて、
#       「PR の commits 一覧を Slack へ通知したい」
#       「しかも特定 channel に」
#       「その channel にはこの定期 PR 以外の通知はしたくない」というニーズのためだけにある七面倒な処理です。
#       「Slack 通知は不要」「必要だが他の PR と一緒の channel で良い」という場合は以降不要です。

# api を使って PR にラベルを付与します。
# NOTE: Slack への通知を考慮して行っています。
#       Slack は、特定のラベルをもつ PR についてのみ通知をする設定が可能です。

# api を使って PR の commits 一覧を取得します。
# NOTE: コメントに一覧を含めるための作業です。
#       それが不要ならこちらも不要です。

# api を使って PR へコメントを投稿します。
# NOTE: この時点で GitHub を通じて Slack へ通知が送られていることを想定しています。

# その他、個別に Slack へ投稿を行います。
# NOTE: メンション付で投稿を行うための処置です。
#       ここに commits 一覧も含めてしまえばラベルやコメントが不要になります。
#       ただし Slack 側に PR へのリンクも欲しいのでコメント通知を取り入れています。
