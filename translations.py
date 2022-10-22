from i18n import add_translation, set as iset

iset('locale', 'en')


def fill_translations():
	def add_en(k, t):
		add_translation(k, t, 'en')

	def add_ru(k, t):
		add_translation(k, t, 'ru')

	add_en('GROWTH', 'Population change, %, 2000->2020 (RU: 2002->2022), {where}')
	add_ru('GROWTH', 'Изменение населения, %, 2000->2020 (Россия*: 2002->2022**), {where}')

	add_en('ALL_COUNTRIES', 'All countries')
	add_ru('ALL_COUNTRIES', 'Все страны')

	add_en('AMOUNT', 'Amount of countries')
	add_ru('AMOUNT', 'Всего стран')

	add_en('ONLY', 'Only countries with: ')
	add_ru('ONLY', 'Только мировые лидеры с: ')

	add_en('POPULATION', 'P: population')
	add_ru('POPULATION', 'P: население (Россия: 146.8М)')

	add_en('EXPECTANCY', 'LE: Life expectancy')
	add_ru('EXPECTANCY', 'LE: Ср. продолжительность жизни (Россия: 73.4, РИА)')

	add_en('NOBLES', 'NB: Total nobel prizes')
	add_ru('NOBLES', 'NB: Всего нобелевских премий (Россия: 32)')

	add_en('NOTE_RU', '')
	_txt = "* Учтено, что часть округов были объединены между 2002 и 2022, см. Корякский автономный округ и т.д.\n"
	_txt += "** для России нет таблиц 2000->2020, правка интервала на 2 года не влияет на результат, т.к. COVID < 0.3% \n"
	add_ru('NOTE_RU', _txt)
