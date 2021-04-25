from slacker import Slacker
slack = Slacker('xoxb-1328826168885-1499204785509-AT29qreiAuEEfqRFogQJvxfN')

markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''

attach_dict = {
    'color'      :'#ff0000',
    'author_name': 'INVESTAR',
    "author_link": 'github.com/investar',
    'title'      : '오늘의 증시 KOSPI',
    'title_link' : 'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'text'       : '2,326.13 △11.89 (+0.51%)',
    'image_url'  : 'ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}

attach_list = [attach_dict]
slack.chat.post_message(channel="#general", text=markdown_text, attachments=attach_list)

''' 위 코드로 보낸 메시지의 내용은 Kospi 그래프 그림 파일을 일크하여 표시했고, 작성자나 제목 텍스트를누르면
    지정한 웹페이지로 자동으로 연결되도록 했다.'''