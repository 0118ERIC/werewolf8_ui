from flask import Flask, request
alive.add(request.sid)
emit('players', list(players.values()), broadcast=True)


@socketio.on('start')
def start():
global phase
if len(players) != 8: return
sids = list(players.keys())
random.shuffle(sids)
for sid, role in zip(sids, ROLES):
roles[sid] = role
emit('role', role, room=sid)
if role == 'witch':
witch[sid] = {'heal': True, 'poison': True}
phase = 'night'
emit('phase', 'night', broadcast=True)
emit('alive', list(alive), broadcast=True)


@socketio.on('wolf_kill')
def wolf_kill(data): night['wolf'] = data['target']


@socketio.on('seer_check')
def seer_check(data): emit('seer_result', roles[data['target']], room=request.sid)


@socketio.on('witch_heal')
def witch_heal():
if witch[request.sid]['heal']:
night['wolf'] = None
witch[request.sid]['heal'] = False


@socketio.on('witch_poison')
def witch_poison(data):
if witch[request.sid]['poison']:
night['poison'] = data['target']
witch[request.sid]['poison'] = False


@socketio.on('night_end')
def night_end():
global phase
deaths = set()
if night['wolf']: deaths.add(night['wolf'])
if night['poison']: deaths.add(night['poison'])
for d in deaths:
alive.discard(d)
emit('dead', players[d], broadcast=True)
night['wolf'] = night['poison'] = None
phase = 'day'
emit('phase', 'day', broadcast=True)
emit('alive', list(alive), broadcast=True)
check_win()


@socketio.on('vote')
def vote(data):
votes[request.sid] = data['target']
if len(votes) >= len(alive):
target = max(votes.values(), key=list(votes.values()).count)
alive.discard(target)
emit('dead', players[target], broadcast=True)
votes.clear()
emit('phase', 'night', broadcast=True)
emit('alive', list(alive), broadcast=True)
check_win()




def check_win():
wolves = [s for s in alive if roles[s]=='werewolf']
others = [s for s in alive if roles[s]!='werewolf']
if not wolves:
emit('win','🎉 村民勝利',broadcast=True)
elif len(wolves)>=len(others):
emit('win','🐺 狼人勝利',broadcast=True)


if __name__=='__main__': socketio.run(app,debug=True)
