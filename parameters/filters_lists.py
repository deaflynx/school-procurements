filter_keywords = ['шк[оі]л', 'загальноосвітн', 'гімназ', 'ліце[йя]', 'колегіум', 'сад[ко][аку]', 'яс[ле][ал]']
filter_keywords_strict = ['зош', 'знз', 'сзш', '[ун]вк', 'днз']


""" Блок 1
    Шкільні заклади, які мають окрему нумерацію.
        Вечірня (змінна) школа
        Спеціальна загальноосвітня школа
        Загальносвітня санаторна школа
        Міжшкільний навчально-виробничий комбінат
"""

filter_vechirni = ['вечір.*змінн', 'вечір.*школ']
filter_vechirni_name = 'Вечірня (змінна) школа'

filter_specialna = ['спеціальн[аоь].*шк[іо]л']
filter_specialna_name = 'Спеціальна загальноосвітня школа'

filter_sanatorna = ['санаторн[аоу].*шк[оі]л', '.*шк[оі]л.*санаторн[аоу]']
filter_sanatorna_name = 'Загальносвітня санаторна школа'

filter_kombinat = ['міжшкільн[ио].*комбінат']
filter_kombinat_name = 'Міжшкільний навчально-виробничий комбінат'


""" Блок 2 
    Шкільні інтернати. Мають свою єдину систему нумерації і мають різні варіації назв: 
        гімназія-інтернат
        загальносвітня школа-інтернат
        ліцей-інтернат
        спеціалізована школа-інтернат
        спеціальна загальносвітня школа-інтернат
        загальносвітня санаторна школа-інтернат
"""

filter_internat = ['інтернат']
filter_internat_name = 'Інтернат'


""" Блок 3
    Загальні шкільні заклади. Мають свою єдину систему нумерації і мають 5 варіацій назв:
        загальносвітня школа
        спеціалізована школа
        ліцей
        гімназія
        навчально-виховний комплекс (об'єднання)
    filter_gimnasium, filter_liceum, filter_specializovana, filter_nvk
"""

filter_subtype_3 = 'Загальні шкільні заклади'

filter_nvk = ['[ун]вк', 'навчальн.*виховн.*комплекс', 'нво', 'навчальн.*виховн.*об']
filter_nvk_name = "Навчально-виховний комплекс (об'єднання)"

filter_gimnasium = ['гімназі[яї]']
filter_gimnasium_name = 'Гімназія'

filter_liceum = ['ліце[йяю]']
filter_liceum_name = 'Ліцей'

filter_specializovana = ['спеціалізован']
filter_specializovana_name = 'Спеціалізована школа'

filter_shkola = ['загальноосвітн', 'І.*ступен', 'колегіум', '.*зош', '.*сзш', 'загальн.*середн', 'початков.*школ']
filter_shkola_name = 'Загальноосвітня школа'

""" Блок 4
    ДНЗ в довіднику має підкласи в довіднику Міністерства освіти тільки для кількох міст. 
    Тому "ДНЗ" - це єдиний запис для садків:
        ДНЗ (дитячий будинок) інтернатного типу
        ДНЗ (дитячий садок)
        ДНЗ (центр розвитку дитини)
        ДНЗ (ясла)
        ДНЗ (ясла-садки)
        ДНЗ (ясла-садок) комбінованого типу
        ДНЗ (ясла-садок) компенсуючого типу
"""

filter_sadik = ['днз', 'сад[ок][ка]', 'дошкільн', 'яс[ле][ал]', 'центр.*розвитк.*дитин']
filter_sadik_name = 'ДНЗ'

""" Блок 5
    Позашкільні заклади. 
"""

filter_poza = ['.*позашкільн', 
               'художн', 
               'мистецтв', 'дхш', 
               'дмш', 'музич', 
               'юнацьк.*спортивн', 'дюсш', 'дитяч.*спортивн'] 
filter_poza_name = 'Позашкільне'

filter_inshe = 'Інше'


filter_priority = [
    filter_shkola,
    filter_nvk,
    filter_gimnasium,
    filter_liceum,
    filter_specializovana,
    filter_internat,
    filter_kombinat,
    filter_sanatorna,
    filter_specializovana,
    filter_specialna,
    filter_sadik
]
filter_name_priority = [
    filter_shkola_name,
    filter_nvk_name,
    filter_gimnasium_name,
    filter_liceum_name,
    filter_specializovana_name,
    filter_internat_name,
    filter_kombinat_name,
    filter_sanatorna_name,
    filter_specializovana_name,
    filter_specialna_name,
    filter_sadik_name
]
