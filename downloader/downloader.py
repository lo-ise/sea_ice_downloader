from nsidc.dailyantarctic import DailyAntarctic
from nsidc.dailyarctic import DailyArctic

__downloaders = {
	'Antarctic': DailyAntarctic,
	'Arctic': DailyArctic,
}

def get(k):
	return __downloaders[k]


