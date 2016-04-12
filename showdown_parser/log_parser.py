from gamestate import Gamestate, Move, Switch

MOVE_CORRECTIONS = {"ExtremeSpeed": "Extreme Speed",
                    "ThunderPunch": "Thunder Punch",
                    "SolarBeam": "Solar Beam",
                    "DynamicPunch": "Dynamic Punch"}

IGNORE = set([
])

def get_player_nick(info):
    player, nick = info[0].split(':', 1)
    nick = nick[1:]
    player = int(player[1]) - 1
    return player, nick

def parse_line(line):
    line = line.split('|')
    if len(line) <= 1:
        return None, None
    line = line[1:]
    type, info = line[0], line[1:]
    return type, info

def check_turn_over(line):
    type, info = parse_line(line)
    return type == 'turn'

def handle_turn(log, state, nicks, players):

    start_state = state.copy()
    actions = {}
    rewards = {0: 0, 1:0}

    while len(log) > 0:
        line = log[0]
        if check_turn_over(line):
            current_state = state.copy()
            for player, action in actions.items():
                if player == 0:
                    yield (start_state, action, rewards[player], current_state)
                elif player == 1:
                    yield (start_state.copy(flip=True), action, rewards[player], state.copy(flip=True))
            start_state = current_state

        line = log.pop(0)
        type, info = parse_line(line)

        if type == 'player':
            if len(info) > 1:
                player, name = info[0], info[1]
                player = int(player[1]) - 1
                players[name] = player
        if type == 'poke':
            player, poke = info[:2]
            player = int(player[1]) - 1
            state.add_poke(player, poke)
        elif type == 'detailschange':
            player, nick = get_player_nick(info)
            poke = info[1]

            old_name = nicks[player][nick]
            state.set_poke_name(player, old_name, poke)
            nicks[player][nick] = poke

        elif type == 'switch':
            player, nick = get_player_nick(info)
            poke = info[1]

            nicks[player][nick] = poke
            state.set_primary(player, poke)

            actions[player] = Switch(poke)
        elif type == 'move':
            player, nick = get_player_nick(info)
            move = info[1]
            if move in MOVE_CORRECTIONS:
                move = MOVE_CORRECTIONS[move]

            actions[player] = Move(move)
        elif type == 'drag':
            player, nick = get_player_nick(info)
            poke = info[1]

            nicks[player][nick] = poke
            state.set_primary(player, poke)
        elif type == 'win':
            player = players[info[0]]
            rewards[player] = 1
            rewards[1 - player] = -1
        elif type == 'faint':
            player, nick = get_player_nick(info)
            state.set_faint(player)
        elif type == '-heal' or type == '-damage':
            player, nick = get_player_nick(info)

            health = info[1].split(' ')[0].split('\\/')

            if len(health) == 1:
                health = float(health[0]) / 100
            else:
                health = float(health[0]) / float(health[1])

            state.set_health(player, health)

    current_state = state.copy()
    for player, action in actions.items():
        if player == 0:
            yield (start_state, action, rewards[player], current_state)
        elif player == 1:
            yield (start_state.copy(flip=True), action, rewards[player], state.copy(flip=True))

def parse_log(log):
    log = log.split('\n')
    state = Gamestate()
    nicks = {0:{}, 1:{}}
    players = {}
    start = 2
    while len(log) > 0:
        experiences = handle_turn(log, state, nicks, players)
        for experience in experiences:
            if start > 0:
                start -= 1
            else:
                yield experience

if __name__ == "__main__":
    from database import ReplayDatabase
    from tqdm import tqdm
    r = ReplayDatabase("replays_all.db")
    experience_db = []
    for (id, replay_id, log) in tqdm(r.get_replays()[:1]):
        if not replay_id[:2] == 'ou':
            continue
        if replay_id in IGNORE:
            continue
        try:
            for experience in parse_log(log):
                experience_db.append(experience)
        except:
            print "Failed on replay:", replay_id
            # import traceback
            # traceback.print_exc()
            # raise Exception()
