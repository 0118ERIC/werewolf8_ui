from browser import document, html, alert
my_role = None
alive = []
players = {}


players_div = document['players']
actions = document['actions']


@socket.on('players')
def _(names):
players.clear()
for n in names: players[n] = n
render()


@socket.on('alive')
def _(data):
global alive
alive = data
render()


@socket.on('role')
def _(r):
global my_role
my_role = r
alert('你的身分：'+r)


@socket.on('phase')
def _(p):
document['phase'].text = '階段：'+p
actions.clear()
if p=='night': night_ui()


@socket.on('seer_result')
def _(r): alert('查驗結果：'+r)
@socket.on('dead')
def _(n): alert(n+' 死亡')
@socket.on('win')
def _(m): alert(m)




def render():
players_div.clear()
for sid in players:
card = html.DIV(sid, Class='player')
if sid not in alive: card.classList.add('dead')
card.bind('click', lambda ev, s=sid: select(s))
players_div <= card


selected = None


def select(s):
global selected
selected = s
actions.text = f'選擇：{s}'




def night_ui():
if my_role=='werewolf':
actions <= html.BUTTON('殺', onclick=lambda ev: socket.emit('wolf_kill',{'target':selected}))
if my_role=='seer':
actions <= html.BUTTON('查驗', onclick=lambda ev: socket.emit('seer_check',{'target':selected}))
if my_role=='witch':
actions <= html.BUTTON('解藥', onclick=lambda ev: socket.emit('witch_heal'))
actions <= html.BUTTON('毒藥', onclick=lambda ev: socket.emit('witch_poison',{'target':selected}))
actions <= html.BUTTON('夜晚結束', onclick=lambda ev: socket.emit('night_end'))




def join(ev): socket.emit('join',{'name':document['name'].value})
def start(ev): socket.emit('start')


document['join'].bind('click',join)
document['start'].bind('click',start)
