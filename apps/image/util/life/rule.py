#apps.image.util.life.rule

#django

#local

#util

#rules
class _Rule(object):
	born = []
	survive = []

	def verdict(self, alive=True, neighbours=0):
		return (alive and neighbours in survive) or (not alive and neighbours in born) #dies by default

	def from_rule_string(self, rulestring):
		born_string, survive_string = tuple(rulestring.split('/'))
		self.born = [int(b) for b in born_string.split('')]
		self.survive = [int(s) for s in survive_string.split('')]

class Conway(_Rule):
	born = [3]
	survive = [2,3]

class Death(_Rule):
    born = []
    survive = [4,5,6,7,8]

class Vote(_Rule):
	born = [5,6,7,8]
	survive = [4,5,6,7,8]

class WalledCities(_Rule):
    born = [4,5,6,7,8]
    survive = [2,3,4,5]

class Coagulations(_Rule):
	born = [3,7,8]
	survive = [2,3,5,6,7,8]

class LiveFreeOrDie(_Rule):
	born = [2]
	survive = [0]

class LifeWithoutDeath(_Rule):
    born = [3]
    survive = [0,1,2,3,4,5,6,7,8]

class FillIn(_Rule):
    born = [5,6,7,8]
    survive = [0,1,2,3,4,5,6,7,8]

class L_B_S678(_Rule):
	born = []
	survive = [6,7,8]

class L_B_S45678(_Rule):
	born = []
	survive = [4,5,6,7,8]

#rule set
class _RuleSet(object):
	rules = [] #list of rules
	timestamps = [] #list of ints

	def get_rule(self, timestamp=0):
		total_time = sum(self.timestamps)
		mod_timestamp = timestamp % total_time

		total = 0
		bin = 0
		for i, time in enumerate(self.timestamps):
			total += time
			if total > mod_timestamp:
				bin = i
				break

		return self.rules[bin]

class _SingleRuleSet(_RuleSet):
	def __init__(self, rule):
		self.rules = [rule]
		self.timestamps = [1]

#types
class ConwayInfinite(_SingleRuleSet):
	def __init__(self, rule=Conway):
		super(ConwayInfinite, self).__init__(rule)

class DeathInfinite(_SingleRuleSet):
	def __init__(self, rule=Death):
		super(DeathInfinite, self).__init__(rule)

class FillInInfinite(_SingleRuleSet):
	def __init__(self, rule=FillIn):
		super(FillInInfinite, self).__init__(rule)

class VoteInfinite(_SingleRuleSet):
	def __init__(self, rule=Vote):
		super(VoteInfinite, self).__init__(rule)

class WalledCitiesInfinite(_SingleRuleSet):
	def __init__(self, rule=WalledCities):
		super(WalledCitiesInfinite, self).__init__(rule)

class LifeWithoutDeathInfinite(_SingleRuleSet):
	def __init__(self, rule=LifeWithoutDeath):
		super(LifeWithoutDeathInfinite, self).__init__(rule)

class L_B_S678Infinite(_SingleRuleSet):
	def __init__(self, rule=L_B_S678):
		super(L_B_S678Infinite, self).__init__(rule)

class L_B_S45678Infinite(_SingleRuleSet):
	def __init__(self, rule=L_B_S45678):
		super(L_B_S45678Infinite, self).__init__(rule)

class OneCoagulationsTenVote(_RuleSet):
	rules = [Coagulations, Vote]
	timestamps = [1,10]

class LiveFreeOrDieInfinite(_RuleSet):
	def __init__(self, rule=LiveFreeOrDie):
		super(LiveFreeOrDieInfinite, self).__init__(rule)
