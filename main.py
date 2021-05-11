# Built-in modules.
import datetime
import argparse
import time

# Third-party modules.
import pytz

# User modules.
import utils
import functions


# ロガーを取得します。
logger = utils.get_my_logger(__name__)
current_utc = datetime.datetime.now(tz=pytz.utc)
logger.info(f'Started at {current_utc.isoformat()}')
current_jst = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
logger.info(f'Started at {current_jst.isoformat()}')

# コマンドライン引数を取得します。
# head -> base の PR となります。
# NOTE: TOKEN 等は環境変数で良いですが、ブランチは実行ごとに可変にしたい。
# NOTE: release への PR は通知したいが、 early-access への PR は必要ない。
#       slack_notification 引数はその分岐を行うために追加しました。
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--head', type=str, help='head -> base',
                    default='dev')
parser.add_argument('-B', '--base', type=str, help='head -> base',
                    default='master')
parser.add_argument('-S', '--slack-notification', type=bool,
                    help='Send release note message to Slack', default=False)
args = parser.parse_args()
logger.info(f'PR [{args.head} -> {args.base}] will be made.'
            f' Slack notification is {"on" if args.slack_notification else "off"}.')

# api を使って PR を作ります。
create_pull_result = functions.create_pull(args.head, args.base)
logger.info(f'Successfully created PR: {create_pull_result["html_url"]}')

# NOTE: ここ以降の処理はすべて、
#       「PR の commits 一覧を Slack へ通知したい」
#       「しかも特定 channel に」
#       「その channel にはこの定期 PR 以外の通知はしたくない」というニーズのためだけにある七面倒な処理です。
#       「Slack 通知は不要」「必要だが他の PR と一緒の channel で良い」という場合は以降不要です。
# NOTE: Slack notification コマンドはこちら。
#       /github subscribe OWNER/REPO pulls,comments,+label:"CONTINUOUS-PR"

# api を使って PR にラベルを付与します。
# NOTE: Slack への通知を考慮して行っています。
#       Slack は、特定のラベルをもつ PR についてのみ通知をする設定が可能です。
add_label_result = functions.add_label(create_pull_result['number'])
logger.info(f'Successfully added label: {add_label_result[0]["url"]}')

# api を使って PR の commits 一覧を取得します。
# NOTE: コメントに一覧を含めるための作業です。
#       それが不要ならこちらも不要です。
list_commits_on_pull_result = functions.list_commits_on_pull(
    create_pull_result['number'])
logger.info(f'Successfully listed commits, count: {len(list_commits_on_pull_result)}')  # noqa: E501
comment_body = functions.create_comment_body(list_commits_on_pull_result)

# api を使って PR へコメントを投稿します。
# NOTE: この時点で GitHub を通じて Slack へ通知が送られていることを想定しています。
create_comment_result = functions.create_comment(
    create_pull_result['number'], comment_body)
logger.info(f'Successfully created comment: {create_comment_result["html_url"]}')  # noqa: E501

# その他、個別に Slack へ投稿を行います。
# NOTE: メンション付で投稿を行うための処置です。
#       ここに commits 一覧も含めてしまえばラベルやコメントが不要になります。
#       ただし Slack 側に PR へのリンクも欲しいのでコメント通知を取り入れています。
message = f'''
<!channel> 数日中に、 {args.base} 環境へのリリース作業を行います。
内容は↑に投稿されたリリースノートを確認してください。

【お知らせ】編集担当者の方は、リリースノートを確認して頂き、
お知らせが必要な項目について本 channel に文面を投稿してください。

[本メッセージは自動送信メッセージです]
'''
# NOTE: 待機しているのは、通知の順番をプログラムの実行順と合わせるためです。
#       待機せずに send_slack_message すると、こちらのメッセージが上のコメント通知よりも先に送付されてしまうので。
time.sleep(10)
utils.send_slack_message(message)
logger.info('Successfully sent message to Slack')
