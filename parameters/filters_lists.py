# Ключові слова для початкового загального фільтрування закупівель закладів або для закладів освіти
filter_keywords = ['шк[оі]л', 
                   'загальноосвітн', 
                   'гімназ', 
                   'ліце[йя]', 
                   'колегіум', 
                   'сад[ко][аку]', 
                   'яс[ле][ал]',
                   'центр розвитку дитини',
                   'навчальн.*виховн.*комплекс']

# Ключові слова теж для фільтрування освітніх закладів, але вони шукаються тільки як окремі слова
filter_keywords_strict = ['зош', 'знз', 'сзш', '[ун]вк', 'днз', 'нво']

# Для зручності перевірки якості визначення типу та номеру освітнього закладу вони були поділені на умовні блоки, в залежності від системи нумерування та найменування закладів.
""" Block 1
    
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


""" Block 2

    Шкільні заклади, які мають окрему нумерацію.
        Вечірня (змінна) школа
        Спеціальна загальноосвітня школа
        Загальносвітня санаторна школа
        Міжшкільний навчально-виробничий комбінат
"""

filter_vechirni = ['вечір.*змінн', 'вечір.*школ']
filter_vechirni_name = 'Вечірня (змінна) школа'

filter_specialna = ['спеціальн']
filter_specialna_name = 'Спеціальна загальноосвітня школа'

filter_sanatorna = ['санаторн.*шк', '.*шк.*санаторн']
filter_sanatorna_name = 'Загальносвітня санаторна школа'

filter_kombinat = ['міжшкільн.*комбінат']
filter_kombinat_name = 'Міжшкільний навчально-виробничий комбінат'


""" Block 3
    
    Загальні шкільні заклади. Мають свою єдину систему нумерації і мають 5 варіацій назв:
        загальносвітня школа
        спеціалізована школа
        ліцей
        гімназія
        навчально-виховний комплекс (об'єднання)
    filter_gimnasium, filter_liceum, filter_specializovana, filter_nvk
"""

filter_subtype_3 = 'Загальні шкільні заклади'

filter_nvk = ['увк', 'нвк', 'навчальн.*виховн.*комплекс', 'нво', 'навчальн.*виховн.*об']
filter_nvk_name = "Навчально-виховний комплекс (об'єднання)"

filter_gimnasium = ['гімназі[яї]']
filter_gimnasium_name = 'Гімназія'

filter_liceum = ['ліце[йяю]']
filter_liceum_name = 'Ліцей'

filter_specializovana = ['спеціалізован']
filter_specializovana_name = 'Спеціалізована школа'

filter_shkola = ['загальноосвітн', 'І.*ступен', 'колегіум', 'зош', 'сзш', 'загальн.*середн', 'початков.*школ']
filter_shkola_name = 'Загальноосвітня школа'

""" Block 4
    
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

filter_sadik = ['днз', 'сад[ок][ка]', 'дошкільн', 'яс[ел][ла]', 'центр розвитку дитини']
filter_sadik_name = 'ДНЗ'

# ПРІОРИТЕТНІСТЬ ВИЗНАЧЕННЯ ТИПУ ЗАКЛАДУ: ТІ ЩО НА ПОЧАТКУ СПИСКУ, МАЮТЬ ВИЩИЙ ПРІОРИТЕТ.
# ВИКОРИСТОВУЮТЬСЯ У classification_by_type_one_column, classification_by_type_three_cols

filter_priority = [
        filter_internat, # Block 1
        filter_vechirni, # Block 2
        filter_specialna, # Block 2
        filter_sanatorna, # Block 2
        filter_kombinat, # Block 2
        filter_nvk, # Block 4
        filter_sadik, # Block 3
        filter_gimnasium, # Block 4 
        filter_liceum, # Block 4 
        filter_specializovana, # Block 4
        filter_shkola # Block 4
    ]

filter_name_priority = [
        filter_internat_name,
        filter_vechirni_name,
        filter_specialna_name,
        filter_sanatorna_name,
        filter_kombinat_name,
        filter_nvk_name,
        filter_sadik_name,
        filter_gimnasium_name,
        filter_liceum_name,
        filter_specializovana_name,
        filter_shkola_name
    ]

""" 
Ключові слова освітніх закладів, які є закладми середньої освіти чи дошкільної.
Використовуються у Крок 4
"""
filter_poza = ['художн', 
               'мистецтв', 'дхш', 
               'дмш', 'музич', 
               'юнацьк.*спортивн', 'дюсш', 'дитяч.*спортивн'] 