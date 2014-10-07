from nsidc.dailyantarctic import DailyAntarctic


__downloaders = {
	'dailyantarctic': DailyAntarctic,
}

def get(k):
	return __downloaders[k]


