import bscout

elim_points = { "W": 30,
				"F": 20,
				"SF": 10,
				"QF": 0}

partner_bonus = 10

def get_points(event_key):
	points = bscout.get_event_district_points(event_key)
	points_dict = {}
	for team in points["points"]:
		team_num = int(team[3:])
		team_points = points["points"][team]
		points_dict[team_num] = (team_points["alliance_points"], team_points["elim_points"])
	return points_dict

def import_results(filename):
	f = open(filename, "rb")
	data = f.readlines()
	alliances = []
	team_scores = {}
	for i in range(2, 10):
		alliances.append(data[i].strip().split(","))
	f.close()

	for alliance in alliances:
		elim_result = elim_points[alliance[4]]
		alliance_num = int(alliance[0])
		ap = (17-alliance_num, 17-alliance_num, alliance_num)
		for i in (0, 1, 2):
			team_scores[int(alliance[i+1])] = (ap[i], elim_result)
	return team_scores

def get_pairings(filename):
	pairings = set()
	if ".csv" in filename:
		f = open(filename, "rb")
		data = f.readlines()
		alliances = []
		for i in range(2, 10):
			alliances.append(data[i].strip().split(","))
		f.close()

		for alliance in alliances:
			teams = [int(alliance[1]), int(alliance[2]), int(alliance[3])]
			for team1 in teams:
				for team2 in teams:
					if team1 != team2:
						pairings.add((min(team1, team2), max(team1, team2)))
	else:
		for alliance in bscout.get_event_info(filename)["alliances"]:
			for team1 in alliance["picks"]:
				for team2 in alliance["picks"]:
					team1_num = int(team1[3:])
					team2_num = int(team2[3:])
					if team1_num != team2_num:
						pairings.add((min(team1_num, team2_num), max(team1_num, team2_num)))
	return pairings

def evaluate(filename, event_key):
	points_earned = {}
	if ".csv" in event_key:
		points_earned = import_results(event_key)
	else:
		points_earned = get_points(event_key)
	points = 0
	prediction = import_results(filename)

	pred_pairings = get_pairings(filename)
	act_pairings = get_pairings(event_key)

	# initialize points with the partner bonus
	points = len(pred_pairings & act_pairings) * partner_bonus

	for team in prediction:
		try:
			for i in (0, 1):
				points += min(prediction[team][i], points_earned[team][i])
		except KeyError:
			pass

	return points

if __name__ == "__main__":
	print "Total points:", evaluate("tim_mkm.csv", "brian_mkm.csv")