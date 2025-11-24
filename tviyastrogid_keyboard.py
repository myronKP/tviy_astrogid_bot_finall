from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🔮 Розклад Таро на запитання – 10🃏"), KeyboardButton(text="💤 Мені наснився сон – 10🃏")],
        [KeyboardButton(text="🌟 Запитати Астрологиню – 15🃏"), KeyboardButton(text="🌀 У мене проблема – 10🃏")],
        [KeyboardButton(text="✋ Гадання на лодоні – 30🃏"), KeyboardButton(text="🌙 Астральна звичка дня – 3🃏")],
        [KeyboardButton(text="❤️‍🔥 Дізнатись сумісність душ – 25🃏")],
        [KeyboardButton(text="🤝 Запросити друга")],
        [KeyboardButton(text="🛒Мої карти")]
    ])
kwiz_question1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ні!", callback_data="answer1_1")],
    [InlineKeyboardButton(text="Так!", callback_data="answer1_2")],
])

zodiac_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Овен ♈️", callback_data="zodiac_Овен")],
    [InlineKeyboardButton(text="Телець ♉️", callback_data="zodiac_Телець")],
    [InlineKeyboardButton(text="Близнюки ♊️", callback_data="zodiac_Близнюки")],
    [InlineKeyboardButton(text="Рак ♋️", callback_data="zodiac_Рак")],
    [InlineKeyboardButton(text="Лев ♌️", callback_data="zodiac_Лев")],
    [InlineKeyboardButton(text="Діва ♍️", callback_data="zodiac_Діва")],
    [InlineKeyboardButton(text="Терези ♎️", callback_data="zodiac_Терези")],
    [InlineKeyboardButton(text="Скорпіон ♏️", callback_data="zodiac_Скорпіон")],
    [InlineKeyboardButton(text="Стрілець ♐️", callback_data="zodiac_Стрілець")],
    [InlineKeyboardButton(text="Козеріг ♑️", callback_data="zodiac_Козеріг")],
    [InlineKeyboardButton(text="Водолій ♒️", callback_data="zodiac_Водолій")],
    [InlineKeyboardButton(text="Риби ♓️", callback_data="zodiac_Риби")],
])

kwiz_question2_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зробити розклад Таро 🔮", callback_data="taro")]
])

taro_question1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="3 карти", callback_data="taro_answer1_1")],
    [InlineKeyboardButton(text="5 карт", callback_data="taro_answer1_2")],
    [InlineKeyboardButton(text="7 карт", callback_data="taro_answer1_3")],
])
music_q1_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Спокійний і глибокий, як тиха вода", callback_data="Спокійний і глибокий, як тиха вода")],
    [InlineKeyboardButton(text="Швидкий і рваний, як серцебиття перед стрибком", callback_data="Швидкий і рваний, як серцебиття перед стрибком")],
    [InlineKeyboardButton(text="Рівномірний і впевнений, як кроки по знайомій дорозі", callback_data="Рівномірний і впевнений, як кроки по знайомій дорозі")],
    [InlineKeyboardButton(text="Млявий і розмитий, як дощовий ранок", callback_data="Млявий і розмитий, як дощовий ранок")],
    [InlineKeyboardButton(text="Легкий і грайливий, як весняний вітер", callback_data="Легкий і грайливий, як весняний вітер")]
])

music_q2_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Рівний і спокійний, як дихання у тиші", callback_data="Рівний і спокійний, як дихання у тиші")],
    [InlineKeyboardButton(text="Швидкий і рваний, як серце після бігу", callback_data="Швидкий і рваний, як серце після бігу")],
    [InlineKeyboardButton(text="Повільний і тягучий, як осінній дощ", callback_data="Повільний і тягучий, як осінній дощ")],
    [InlineKeyboardButton(text="Пульсуючий, як світло крізь фіранки", callback_data="Пульсуючий, як світло крізь фіранки")],
    [InlineKeyboardButton(text="Нерівний і неспокійний, як думки перед сном", callback_data="Нерівний і неспокійний, як думки перед сном")]
])

music_q3_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Тепла і присутності близької людини", callback_data="Тепла і присутності близької людини")],
    [InlineKeyboardButton(text="Відчуття спокою і внутрішньої рівноваги", callback_data="Відчуття спокою і внутрішньої рівноваги")],
    [InlineKeyboardButton(text="Справжнього драйву та енергії", callback_data="Справжнього драйву та енергії")],
    [InlineKeyboardButton(text="Чіткого сенсу і розуміння свого шляху", callback_data="Чіткого сенсу і розуміння свого шляху")],
    [InlineKeyboardButton(text="Простоти і легкості без турбот", callback_data="Простоти і легкості без турбот")]
])

music_q4_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Приховую все всередині, навіть від себе", callback_data="Приховую все всередині, навіть від себе")],
    [InlineKeyboardButton(text="Виплескую у творчість або рух", callback_data="Виплескую у творчість або рух")],
    [InlineKeyboardButton(text="Довіряю близьким і говорю відкрито", callback_data="Довіряю близьким і говорю відкрито")],
    [InlineKeyboardButton(text="Ігнорую, поки не вибухаю", callback_data="Ігнорую, поки не вибухаю")],
    [InlineKeyboardButton(text="Спокійно спостерігаю і приймаю їх", callback_data="Спокійно спостерігаю і приймаю їх")]
])

music_q5_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="У дитинстві, коли все було простим", callback_data="У дитинстві, коли все було простим")],
    [InlineKeyboardButton(text="У моменті самоти на природі", callback_data="У моменті самоти на природі")],
    [InlineKeyboardButton(text="Під час глибокої розмови з кимось важливим", callback_data="Під час глибокої розмови з кимось важливим")],
    [InlineKeyboardButton(text="Коли займався тим, що люблю всією душею", callback_data="Коли займався тим, що люблю всією душею")],
    [InlineKeyboardButton(text="Не пам’ятаю, здається, це ще попереду", callback_data="Не пам’ятаю, здається, це ще попереду")]
])

music_q6_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Шепіт вітру в кронах дерев", callback_data="Шепіт вітру в кронах дерев")],
    [InlineKeyboardButton(text="Пульсуючий електронний біт", callback_data="Пульсуючий електронний біт")],
    [InlineKeyboardButton(text="М'які акорди фортепіано", callback_data="М'які акорди фортепіано")],
    [InlineKeyboardButton(text="Ритмічне тиканя годинника в тиші", callback_data="Ритмічне тиканя годинника в тиші")],
    [InlineKeyboardButton(text="Нерівні кроки на старій дерев’яній підлозі", callback_data="Нерівні кроки на старій дерев’яній підлозі")]
])

music_q7_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Самота і тиша", callback_data="Самота і тиша")],
    [InlineKeyboardButton(text="Музика, що ніби розчиняє думки", callback_data="Музика, що ніби розчиняє думки")],
    [InlineKeyboardButton(text="Розмова з тим, хто розуміє", callback_data="Розмова з тим, хто розуміє")],
    [InlineKeyboardButton(text="Рутина і чіткий порядок", callback_data="Рутина і чіткий порядок")],
    [InlineKeyboardButton(text="Прогулянка під відкритим небом", callback_data="Прогулянка під відкритим небом")]
])
music_q8_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ранній ранок — чистий аркуш і спокій", callback_data="Ранній ранок — чистий аркуш і спокій")],
    [InlineKeyboardButton(text="Полудень — ясність і зосередженість", callback_data="Полудень — ясність і зосередженість")],
    [InlineKeyboardButton(text="Сутінки — легка тривога і тиша", callback_data="Сутінки — легка тривога і тиша")],
    [InlineKeyboardButton(text="Ніч — глибина, роздуми, самота", callback_data="Ніч — глибина, роздуми, самота")],
    [InlineKeyboardButton(text="Світанок — надія і передчуття нового", callback_data="Світанок — надія і передчуття нового")]
])

music_q9_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Втекти від усього і побути наодинці", callback_data="Втекти від усього і побути наодинці")],
    [InlineKeyboardButton(text="Відчути глибокий сенс у буденному", callback_data="Відчути глибокий сенс у буденному")],
    [InlineKeyboardButton(text="Поділитись собою з кимось справжнім", callback_data="Поділитись собою з кимось справжнім")],
    [InlineKeyboardButton(text="Виплеснути емоції у творчість або рух", callback_data="Виплеснути емоції у творчість або рух")],
    [InlineKeyboardButton(text="Просто нічого не відчувати і розчинитися в спокої", callback_data="Просто нічого не відчувати і розчинитися в спокої")]
])

music_q10_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Глибокі розмови і щирі люди", callback_data="Глибокі розмови і щирі люди")],
    [InlineKeyboardButton(text="Краса природи і споглядання", callback_data="Краса природи і споглядання")],
    [InlineKeyboardButton(text="Музика, яка говорить без слів", callback_data="Музика, яка говорить без слів")],
    [InlineKeyboardButton(text="Мрії про майбутнє і зміни", callback_data="Мрії про майбутнє і зміни")],
    [InlineKeyboardButton(text="Темні емоції, що перетворюються на силу", callback_data="Темні емоції, що перетворюються на силу")]
])

music_q11_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="З хвилею, що то набігає, то відступає", callback_data="З хвилею, що то набігає, то відступає")],
    [InlineKeyboardButton(text="З полум’ям, яке не дає спокою", callback_data="З полум’ям, яке не дає спокою")],
    [InlineKeyboardButton(text="З хмарою, що пливе без мети", callback_data="З хмарою, що пливе без мети")],
    [InlineKeyboardButton(text="З деревом, що стоїть і росте мовчки", callback_data="З деревом, що стоїть і росте мовчки")],
    [InlineKeyboardButton(text="З іскрою, що ще шукає, чим загорітись", callback_data="З іскрою, що ще шукає, чим загорітись")]
])

music_q12_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Очікування", callback_data="Очікування")],
    [InlineKeyboardButton(text="Нестабільність", callback_data="Нестабільність")],
    [InlineKeyboardButton(text="Прозорість", callback_data="Прозорість")],
    [InlineKeyboardButton(text="Напруга", callback_data="Напруга")],
    [InlineKeyboardButton(text="Спокій", callback_data="Спокій")]
])

music_q13_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Рівний, як подих у тиші", callback_data="Рівний, як подих у тиші")],
    [InlineKeyboardButton(text="Зламаний і уривчастий", callback_data="Зламаний і уривчастий")],
    [InlineKeyboardButton(text="Швидкий, майже як паніка", callback_data="Швидкий, майже як паніка")],
    [InlineKeyboardButton(text="Повільний, тягучий і важкий", callback_data="Повільний, тягучий і важкий")],
    [InlineKeyboardButton(text="Пульсуючий, як танець світла", callback_data="Пульсуючий, як танець світла")]
])

music_q14_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Тиші без думок", callback_data="Тиші без думок")],
    [InlineKeyboardButton(text="Сміху, що йде з глибини", callback_data="Сміху, що йде з глибини")],
    [InlineKeyboardButton(text="Зрозуміти себе до кінця", callback_data="Зрозуміти себе до кінця")],
    [InlineKeyboardButton(text="Бути почутим і прийнятим", callback_data="Бути почутим і прийнятим")],
    [InlineKeyboardButton(text="Просто спокою без причин", callback_data="Просто спокою без причин")]
])

music_q15_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="У тишу, подалі від усього", callback_data="У тишу, подалі від усього")],
    [InlineKeyboardButton(text="До нових вражень і змін", callback_data="До нових вражень і змін")],
    [InlineKeyboardButton(text="У спогади, що досі живі", callback_data="У спогади, що досі живі")],
    [InlineKeyboardButton(text="У глибину себе, щоб щось знайти", callback_data="У глибину себе, щоб щось знайти")],
    [InlineKeyboardButton(text="Невідомо куди — але чомусь довіряю", callback_data="Невідомо куди — але чомусь довіряю")]
])

archetype_test_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дізнатись сумісність душ", callback_data="start_archetype_test")]
])

architips_q1_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Йду далі, пробую нове", callback_data="Мандрівник")],
    [InlineKeyboardButton(text="Допомагаю іншим", callback_data="Цілитель")],
    [InlineKeyboardButton(text="Борюсь до кінця", callback_data="Воїн")],
    [InlineKeyboardButton(text="Аналізую і планую", callback_data="Мудрець")]
])

architips_q2_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Свободу та враження", callback_data="Мандрівник")],
    [InlineKeyboardButton(text="Гармонію та близькість", callback_data="Цілитель")],
    [InlineKeyboardButton(text="Справедливість і силу волі", callback_data="Воїн")],
    [InlineKeyboardButton(text="Знання та розуміння", callback_data="Мудрець")]
])

architips_q3_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Вирушаю кудись", callback_data="Мандрівник")],
    [InlineKeyboardButton(text="Бачуся з другом", callback_data="Цілитель")],
    [InlineKeyboardButton(text="Займаюсь спортом/ділом", callback_data="Воїн")],
    [InlineKeyboardButton(text="Читаю чи думаю", callback_data="Мудрець")]
])

architips_q4_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Застрягнути, втратити сенс", callback_data="Мандрівник")],
    [InlineKeyboardButton(text="Підвести близьких", callback_data="Цілитель")],
    [InlineKeyboardButton(text="Бути слабким", callback_data="Воїн")],
    [InlineKeyboardButton(text="Помилитися", callback_data="Мудрець")]
])

architips_q5_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Як компас — усі різні", callback_data="Мандрівник")],
    [InlineKeyboardButton(text="Як душі, що потребують тепла", callback_data="Цілитель")],
    [InlineKeyboardButton(text="Як союзників або опонентів", callback_data="Воїн")],
    [InlineKeyboardButton(text="Як загадку для розуму", callback_data="Мудрець")]
])

architips_start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="😌 Для себе", callback_data="person_you")],
    [InlineKeyboardButton(text="💫 Для партнера", callback_data="person_partner")]
])

architips_partner_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="😌💫 Почати для партнера", callback_data="person_partner")]
])
explanation_cards_taro_y_or_n = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пояснення розкладу-7🃏", callback_data="explanation_cards")]
])
daily_bonus_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🎁 Отримати карти", callback_data="daily_bonus")]
])
#buy_cards_kb = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text="💳 50 карт — 25 грн", url="https://send.monobank.ua/jar/XXXXX")],
 #   [InlineKeyboardButton(text="💳 100 карт — 40 грн", url="https://send.monobank.ua/jar/YYYYY")],
 #   [InlineKeyboardButton(text="💳 200 карт — 70 грн", url="https://send.monobank.ua/jar/ZZZZZ")],
#    [InlineKeyboardButton(text="💳 500 карт — 150 грн", url="https://send.monobank.ua/jar/WWWWW")],
 #   [InlineKeyboardButton(text="💳 1000 карт — 250 грн", url="https://send.monobank.ua/jar/QQQQQ")]
#])
