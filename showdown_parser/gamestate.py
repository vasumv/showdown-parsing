class Gamestate(object):

    def __init__(self, teams=None, faint=None, health=None):
        self.teams = teams or ([], [])

    def add_poke(self, team_num, poke_name):
        self.teams[team_num].append(Pokemon(poke_name))

    def set_poke_name(self, team_num, poke_name, new_name):
        _, poke = self.find_poke(team_num, poke_name)
        poke.set_name(new_name)

    def copy(self, flip=False):
        if flip:
            return Gamestate(teams=(self.get_team(1), self.get_team(0)))
        return Gamestate(teams=(self.get_team(0), self.get_team(1)))

    def get_team(self, team_num):
        return [p.copy() for p in self.teams[team_num]]

    def set_team(self, team_num, team):
        self.teams[team_num] = team

    def get_faint(self, team_num):
        return self.teams[team_num][0].get_faint()

    def set_faint(self, team_num):
        self.teams[team_num][0].set_faint(True)

    def get_health(self, team_num):
        return self.teams[team_num][0].get_health()

    def set_health(self, team_num, health):
        self.teams[team_num][0].set_health(health)

    def get_faints(self, team_num):
        return [p.get_faint() for p in self.teams[team_num]]

    def get_healths(self, team_num):
        return [p.get_health() for p in self.teams[team_num]]

    def get_primary(self, team_num):
        team = self.get_team(team_num)
        if len(team) == 0:
            return None
        return team[0]

    def find_poke(self, team_num, poke_name):
        for i, poke in enumerate(self.teams[team_num]):
            if poke.get_name() == poke_name:
                return i, poke

    def set_primary(self, team_num, poke_name):
        team = self.teams[team_num]
        index, _ = self.find_poke(team_num, poke_name)
        team[index], team[0] = team[0], team[index]

    def __repr__(self):
        return "State([%s| %s])" % (self.get_primary(0).get_name(), self.get_primary(1).get_name())

class Pokemon(object):

    def __init__(self, name, faint=False, health=1.0):
        self.name = name
        self.faint = faint
        self.health = health

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_faint(self):
        return self.faint

    def set_faint(self, faint):
        self.faint = faint

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def copy(self):
        return Pokemon(self.name,
                       faint=self.faint,
                       health=self.health)

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
