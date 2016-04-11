class Gamestate(object):
    def __init__(self, teams=None):
        self.teams = teams or ([], [])

    def add_poke(self, team_num, poke_name):
        self.teams[team_num].append(poke_name)

    def set_poke(self, team_num, poke_name, new_name):
        team = self.teams[team_num]
        team[team.index(poke_name)] = new_name

    def copy(self, flip=False):
        if flip:
            return Gamestate(teams=(self.get_team(1), self.get_team(0)))
        return Gamestate(teams=(self.get_team(0), self.get_team(1)))

    def get_team(self, team_num):
        return self.teams[team_num][:]

    def set_team(self, team_num, team):
        self.teams[team_num] = team

    def get_primary(self, team_num):
        team = self.get_team(team_num)
        if len(team) == 0:
            return None
        return team[0]

    def set_primary(self, team_num, poke_name):
        team = self.teams[team_num]
        index = team.index(poke_name)
        team[index], team[0] = team[0], team[index]

    def __repr__(self):
        return "State([%s| %s])" % (self.get_primary(0), self.get_primary(1))

class Action(object):
    pass

    def is_move(self):
        return False

    def is_switch(self):
        return False

class Move(Action):
    def __init__(self, name):
        self.name = name

    def is_move(self):
        return True

    def __repr__(self):
        return "Move(%s)" % self.name

class Switch(Action):
    def __init__(self, poke_name):
        self.name = poke_name

    def is_switch(self):
        return True

    def __repr__(self):
        return "Switch(%s)" % self.name
