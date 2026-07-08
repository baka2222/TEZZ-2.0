# translations.py
# Полный словарь переводов для TEZZ Market bot
# Ключи сгруппированы по функциональным модулям
from functools import lru_cache


TRANSLATIONS = {

    # ---------- Общие / Регистрация / Навигация (commands) ----------
    'choose_language': {
        'ru': '🇷🇺 Выберите язык',
        'kg': '🇰🇬 Тилди тандаңыз',
        'en': '🇬🇧 Choose language',
        'cn': '🇨🇳 选择语言',
    },
    'welcome': {
        'ru': 'Добро пожаловать в TEZZ Market!',
        'kg': 'TEZZ Marketке кош келиңиз!',
        'en': 'Welcome to TEZZ Market!',
        'cn': '欢迎来到 TEZZ Market！',
    },
    'registration_name': {
        'ru': 'Как тебя зовут?\n\nПросто напиши мне своё имя или ник.',
        'kg': 'Атыңыз ким?\n\nЖөн гана атыңызды же никти жазыңыз.',
        'en': 'What is your name?\n\nJust send your name or nickname.',
        'cn': '你叫什么名字？\n\n请发送你的名字或昵称。',
    },
    'registration_phone': {
        'ru': 'Отправь номер телефона кнопкой ниже.\n\nОн нужен, чтобы покупатели могли связаться с тобой.',
        'kg': 'Төмөнкү баскыч менен телефон номериңизди жөнөтүңүз.\n\nАны сатып алуучулар сиз менен байланышуу үчүн колдонушат.',
        'en': 'Send your phone number using the button below.\n\nIt is needed so buyers can contact you.',
        'cn': '请用下方按钮发送你的电话号码。\n\n买家可以通过它联系你。',
    },
    'send_phone_btn': {
        'ru': 'Отправить номер',
        'kg': 'Телефонду жөнөтүү',
        'en': 'Send phone',
        'cn': '发送号码',
    },
    'registration_complete': {
        'ru': '✅ Регистрация завершена!',
        'kg': '✅ Каттоо аяктады!',
        'en': '✅ Registration completed!',
        'cn': '✅ 注册完成！',
    },
    'help': {
        'ru': 'Чтобы получить помощь, напиши в поддержку — @isbakks',
        'kg': 'Жардам керек болсо, колдоо кызматына жазыңыз — @isbakks',
        'en': 'For help, contact support — @isbakks',
        'cn': '如需帮助，请联系支持 — @isbakks',
    },
    'not_registered': {
        'ru': '❗️ Вы не зарегистрированы! Пожалуйста, используйте /start.',
        'kg': '❗️ Сиз катталган эмессиз! /start колдонуңуз.',
        'en': '❗️ You are not registered! Please use /start.',
        'cn': '❗️ 您尚未注册！请使用 /start。',
    },
    'banned': {
        'ru': '🚫 Вы заблокированы и не можете размещать объявления.',
        'kg': '🚫 Сиз бөгөттөлдүңүз жана жарыяларды жайгаштыра албайсыз.',
        'en': '🚫 You are banned and cannot post ads.',
        'cn': '🚫 您已被封禁，无法发布广告。',
    },
    'unknown_category': {
        'ru': 'Неизвестная категория',
        'kg': 'Белгисиз категория',
        'en': 'Unknown category',
        'cn': '未知分类',
    },
    'days': {
        'ru': 'дн.',
        'kg': 'күн.',
        'en': 'days',
        'cn': '天',
    },
    'hours': {
        'ru': 'ч.',
        'kg': 'саат.',
        'en': 'hours',
        'cn': '小时',
    },
    'minutes': {
        'ru': 'мин.',
        'kg': 'минут.',
        'en': 'minutes',
        'cn': '分钟',
    },
    'less_than_minute': {
        'ru': 'менее 1 мин.',
        'kg': '1 минуттан аз',
        'en': 'less than 1 min',
        'cn': '不到1分钟',
    },
    'menu_categories': {
        'ru': '🛒 Доступные маркеты',
        'kg': '🛒 Маркеттер',
        'en': '🛒 Available markets',
        'cn': '🛒 可用市场',
    },
    'price_must_be_number': {
        'ru': '❗️ Цена должна быть числом. Введите только число, например: 3500',
        'kg': '❗️ Баа сан болушу керек. Сан гана жазыңыз, мисалы: 3500',
        'en': '❗️ Price must be a number. Enter only a number, e.g.: 3500',
        'cn': '❗️ 价格必须为数字。只输入数字，例如：3500',
    },
    # Новые ключи:
    'send_text_price': {
        'ru': 'Пожалуйста, отправьте цену текстовым сообщением.',
        'kg': 'Сураныч, бааны текст менен жөнөтүңүз.',
        'en': 'Please send the price as a text message.',
        'cn': '请以文本消息形式发送价格。',
    },
    'send_text_name': {
        'ru': 'Пожалуйста, отправьте название объявления текстом.',
        'kg': 'Сураныч, жарыянын аталышын текст менен жөнөтүңүз.',
        'en': 'Please send the ad title as a text message.',
        'cn': '请以文本消息形式发送广告标题。',
    },
    'send_text_desc': {
        'ru': 'Пожалуйста, отправьте описание текстом.',
        'kg': 'Сураныч, сүрөттөмөнү текст менен жөнөтүңүз.',
        'en': 'Please send the description as a text message.',
        'cn': '请以文本消息形式发送描述。',
    },
    'channels_list': {
        'ru': (
            '<b>🚲 Веломаркет:</b> <a href="https://t.me/teztezfg">велосипеды, аксессуары</a>\n\n'
            '<b>💄 Бьюти маркет:</b> <a href="https://t.me/tezbueaty">косметика, уход</a>\n\n'
            '<b>🏍 Автомотомаркет:</b> <a href="https://t.me/tezautomoto">мопеды, мото, авто</a>\n\n'
            '<b>💻 Техномаркет:</b> <a href="https://t.me/teztechno">электроника, гаджеты</a>\n\n'
            '<b>🏠 Рынок недвижимости:</b> <a href="https://t.me/tezhousing">жильё, коммерция</a>\n\n'
            '<b>💼 Вакансии / Резюме:</b> <a href="https://t.me/tezzjob">работа, подработка</a>'
        ),
        'kg': (
            '<b>🚲 Веломаркет:</b> <a href="https://t.me/teztezfg">велосипеддер, аксессуарлар</a>\n\n'
            '<b>💄 Бьюти маркет:</b> <a href="https://t.me/tezbueaty">косметика, кам көрүү</a>\n\n'
            '<b>🏍 Автомотомаркет:</b> <a href="https://t.me/tezautomoto">мопеддер, мото, авто</a>\n\n'
            '<b>💻 Техномаркет:</b> <a href="https://t.me/teztechno">электроника, гаджеттер</a>\n\n'
            '<b>🏠 Недвижимость рыногу:</b> <a href="https://t.me/tezhousing">турак-жай, коммерция</a>\n\n'
            '<b>💼 Вакансиялар / Резюмелер:</b> <a href="https://t.me/tezzjob">иш, кошумча иш</a>'
        ),
        'en': (
            '<b>🚲 Velomarket:</b> <a href="https://t.me/teztezfg">bikes, accessories</a>\n\n'
            '<b>💄 Beauty market:</b> <a href="https://t.me/tezbueaty">cosmetics, care</a>\n\n'
            '<b>🏍 Automoto market:</b> <a href="https://t.me/tezautomoto">mopeds, motorcycles, cars</a>\n\n'
            '<b>💻 Tech market:</b> <a href="https://t.me/teztechno">electronics, gadgets</a>\n\n'
            '<b>🏠 Real estate:</b> <a href="https://t.me/tezhousing">housing, commercial</a>\n\n'
            '<b>💼 Jobs / Resumes:</b> <a href="https://t.me/tezzjob">work, part-time</a>'
        ),
        'cn': (
            '<b>🚲 自行车市场：</b> <a href="https://t.me/teztezfg">自行车，配件</a>\n\n'
            '<b>💄 美容市场：</b> <a href="https://t.me/tezbueaty">化妆品，护理</a>\n\n'
            '<b>🏍 汽车摩托车市场：</b> <a href="https://t.me/tezautomoto">轻便摩托车，摩托车，汽车</a>\n\n'
            '<b>💻 科技市场：</b> <a href="https://t.me/teztechno">电子产品，小工具</a>\n\n'
            '<b>🏠 房地产市场：</b> <a href="https://t.me/tezhousing">住宅，商业</a>\n\n'
            '<b>💼 工作 / 简历：</b> <a href="https://t.me/tezzjob">工作，兼职</a>'
        ),
    },
    'menu_change_lang': {
        'ru': '🌐 Сменить язык',
        'kg': '🌐 Тилди өзгөртүү',
        'en': '🌐 Change language',
        'cn': '🌐 更改语言',
    },
    'language_changed': {
        'ru': '✅ Язык успешно изменён!',
        'kg': '✅ Тил ийгиликтүү өзгөртүлдү!',
        'en': '✅ Language changed successfully!',
        'cn': '✅ 语言成功更改！',
    },

    # ---------- Меню (общее) ----------
    'menu_market': {
        'ru': '❇ Создать объявление',
        'kg': '❇ Жарыя түзүү',
        'en': '❇ Create ad',
        'cn': '❇ 创建广告',
    },
    'menu_delivery': {
        'ru': '🚚 Доставка',
        'kg': '🚚 Жеткирүү',
        'en': '🚚 Delivery',
        'cn': '🚚 配送',
    },
    'menu_stores': {
        'ru': '🏪 Магазины',
        'kg': '🏪 Дүкөндөр',
        'en': '🏪 Stores',
        'cn': '🏪 商店',
    },
    'menu_support': {
        'ru': '🛠️ Поддержка',
        'kg': '🛠️ Колдоо',
        'en': '🛠️ Support',
        'cn': '🛠️ 支持',
    },
    # Добавьте эти ключи в соответствующие разделы TRANSLATIONS

    # ---------- Пагинация (добавить в любой раздел) ----------
    'forward': {
        'ru': 'Вперед',
        'kg': 'Алдыга',
        'en': 'Forward',
        'cn': '前进',
    },
    'back': {
        'ru': 'Назад',
        'kg': 'Артка',
        'en': 'Back',
        'cn': '返回',
    },

    # ---------- Для уведомлений владельцу магазина ----------
    'date': {
        'ru': 'Дата',
        'kg': 'Дата',
        'en': 'Date',
        'cn': '日期',
    },
    'order_items': {
        'ru': 'Состав заказа',
        'kg': 'Заказдын курамы',
        'en': 'Order items',
        'cn': '订单内容',
    },

    # ---------- Для доставки ----------
    'your_location': {
        'ru': 'Ваше местоположение',
        'kg': 'Сиздин жайгашкан жериңиз',
        'en': 'Your location',
        'cn': '您的位置',
    },

    # ---------- Для кнопки меню (уже есть, но проверьте) ----------
    'menu_button': {
        'ru': 'Меню',
        'kg': 'Меню',
        'en': 'Menu',
        'cn': '菜单',
    },

    # ---------- Для подсказки нажать меню ----------
    'press_menu_button': {
        'ru': '👇 Нажмите кнопку <b>Меню</b> внизу экрана',
        'kg': '👇 Экрандын түбүндөгү <b>Меню</b> баскычын басыңыз',
        'en': '👇 Press the <b>Menu</b> button at the bottom',
        'cn': '👇 请点击底部的<b>菜单</b>按钮',
    },

    # ---------- Для обработчика catch_all ----------
    'error_occurred': {
        'ru': '❌ Произошла ошибка. Пожалуйста, начните заново.',
        'kg': '❌ Ката кетти. Сураныч, кайрадан баштаңыз.',
        'en': '❌ An error occurred. Please start over.',
        'cn': '❌ 发生错误。请重新开始。',
    },
    'menu_promt': {
        'ru': '👇 Нажмите кнопку <b>Меню</b> внизу экрана',
        'kg': '👇 Экрандын түбүндөгү <b>Меню</b> баскычын басыңыз',
        'en': '👇 Press the <b>Menu</b> button at the bottom',
        'cn': '👇 请点击底部的<b>菜单</b>按钮',
    },
    'going_to_menu': {
        'ru': 'Переходим в меню...',
        'kg': 'Менюга өтүүдө...',
        'en': 'Going to menu...',
        'cn': '正在进入菜单...',
    },
    'menu_text': {
        'ru': '🔥 <b>TEZZ — твоя площадка!</b>\n\n'
            '🛍️ Хочешь продать или найти? Дерзай!\n'
            '🚚 Нужна доставка? Без проблем!\n'
            '❓ Вопросы? Пиши в поддержку — ответим!\n\n'
            '🌐 Сайт: <a href="https://tezz.kg/market">tezz.kg/market</a>\n'
            '👇 Выбирай ниже',
        'kg': '🔥 <b>TEZZ — сенин аянтчаң!</b>\n\n'
            '🛍️ Саткың же тапкың келеби? Аракет кыл!\n'
            '🚚 Жеткирүү керекпи? Кыйын эмес!\n'
            '❓ Суроолоруң барбы? Колдоого жаз — жооп беребиз!\n\n'
            '🌐 Сайт: <a href="https://tezz.kg/market">tezz.kg/market</a>\n'
            '👇 Төмөндөн танда',
        'en': '🔥 <b>TEZZ — your marketplace!</b>\n\n'
            '🛍️ Wanna sell or find something? Go for it!\n'
            '🚚 Need delivery? No problem!\n'
            '❓ Questions? Contact support — we’ll help!\n\n'
            '🌐 Website: <a href="https://tezz.kg/market">tezz.kg/market</a>\n'
            '👇 Choose below',
        'cn': '🔥 <b>TEZZ — 你的交易平台！</b>\n\n'
            '🛍️ 想卖东西或找东西？来吧！\n'
            '🚚 需要配送？没问题！\n'
            '❓ 有问题？联系客服 — 我们会帮助您！\n\n'
            '🌐 网站：<a href="https://tezz.kg/market">tezz.kg/market</a>\n'
            '👇 请选择',
    },

    # ---------- Продажа / Объявления (sellbuy) ----------
    'sell_create': {
        'ru': '🛒 <b>Создание нового объявления</b>\n\nВыберите категорию для размещения:',
        'kg': '🛒 <b>Жаңы жарыя түзүү</b>\n\nКатегорияны тандаңыз:',
        'en': '🛒 <b>Create a new ad</b>\n\nChoose a category:',
        'cn': '🛒 <b>创建新广告</b>\n\n请选择分类：',
    },
    'wait_cooldown': {
        'ru': '⏳ Вы уже публиковали в этой категории недавно.\n⏱ Следующее размещение будет доступно через: {time}',
        'kg': '⏳ Сиз бул категорияда жакында жарыя жайгаштырдыңыз.\n⏱ Кийинки жарыя: {time}',
        'en': '⏳ You have recently posted in this category.\n⏱ Next post available in: {time}',
        'cn': '⏳ 您最近在此分类发布过。\n⏱ 下次可发布时间：{time}',
    },
    'pay_placement': {
        'ru': 'Или оплатите платное размещение 15 сом. MBank: 771514979 (Бакай Т).\nПосле оплаты — нажмите кнопку ниже и отправьте чек (фото) боту.',
        'kg': 'Же 15 сом төлөп жайгаштырыңыз. MBank: 771514979 (Бакай Т).\nТөлөгөндөн кийин — төмөнкү баскычты басып, чек (сүрөт) жөнөтүңүз.',
        'en': 'Or pay 15 KGS for paid placement. MBank: 771514979 (Bakay T).\nAfter payment — press the button below and send the receipt (photo) to the bot.',
        'cn': '或支付 15 索姆进行付费发布。MBank: 771514979 (Bakay T)。\n支付后，点击下方按钮并将收据（照片）发送给机器人。',
    },
    'paid_placement': {
        'ru': '💳 Вы выбрали платное размещение объявления.\n\nПожалуйста, оплатите 15 сом на MBank: 771514979 (Бакай Т).\nПосле оплаты — просто отправьте фото чека сюда (в чат бота).',
        'kg': '💳 Сиз жарыяны төлөп жайгаштырууну тандадыңыз.\n\n15 сомду MBank: 771514979 (Бакай Т) аркылуу төлөңүз.\nТөлөгөндөн кийин — чекти (сүрөт) ушул чатка жөнөтүңүз.',
        'en': '💳 You have chosen paid ad placement.\n\nPlease pay 15 KGS to MBank: 771514979 (Bakay T).\nAfter payment — just send the receipt photo here (to the bot chat).',
        'cn': '💳 您选择了付费广告发布。\n\n请向 MBank: 771514979 (Bakay T) 支付 15 索姆。\n支付后，将收据照片发送到此聊天。',
    },
    'send_receipt_photo': {
        'ru': 'Пожалуйста, пришлите фото чека (как изображение).',
        'kg': 'Чекти сүрөт катары жөнөтүңүз.',
        'en': 'Please send the receipt photo (as an image).',
        'cn': '请发送收据照片（作为图片）。',
    },
    'new_receipt': {
        'ru': '💳 Новый чек на проверку',
        'kg': '💳 Жаңы чек текшерүү үчүн',
        'en': '💳 New receipt for review',
        'cn': '💳 新收据待审核',
    },
    'confirm_payment': {
        'ru': '✅ Подтвердить оплату',
        'kg': '✅ Төлөмдү ырастоо',
        'en': '✅ Confirm payment',
        'cn': '✅ 确认付款',
    },
    'decline_payment': {
        'ru': '❌ Отклонить оплату',
        'kg': '❌ Төлөмдү четке кагуу',
        'en': '❌ Decline payment',
        'cn': '❌ 拒绝付款',
    },
    'receipt_sent': {
        'ru': '✅ Спасибо! Ваш чек отправлен администратору на проверку. Ожидайте подтверждения.',
        'kg': '✅ Рахмат! Чегиңиз админге жөнөтүлдү. Ырастоону күтүңүз.',
        'en': '✅ Thank you! Your receipt has been sent to the admin for review. Please wait for confirmation.',
        'cn': '✅ 谢谢！您的收据已发送管理员审核，请等待确认。',
    },
    'payment_confirmed': {
        'ru': '✅ Оплата подтверждена. Вы можете разместить платное объявление в категории «{category}».',
        'kg': '✅ Төлөм ырасталды. «{category}» категориясында жарыя жайгаштыра аласыз.',
        'en': '✅ Payment confirmed. You can post a paid ad in the “{category}” category.',
        'cn': '✅ 付款已确认。您可以在“{category}”分类发布付费广告。',
    },
    'payment_declined': {
        'ru': '❌ Оплата не подтверждена для категории «{category}». Проверьте чек и попробуйте снова или свяжитесь с админом.',
        'kg': '❌ Төлөм ырасталган жок («{category}» категориясы үчүн). Чекти текшериңиз же админге кайрылыңыз.',
        'en': '❌ Payment not confirmed for “{category}”. Check the receipt and try again or contact admin.',
        'cn': '❌ “{category}”分类付款未确认。请检查收据并重试或联系管理员。',
    },
    'ad_title': {
        'ru': '📝 <b>Введите заголовок объявления</b>\n\n<i>Например:\n• iPhone 13 128GB\n• Сдаётся 1-комнатная квартира\n• Требуется бариста\n• Ищу велосипед</i>',
        'kg': '📝 <b>Жарыянын аталышын киргизиңиз</b>\n\n<i>Мисалы:\n• iPhone 13 128GB\n• 1-бөлмөлүү батир ижарага берилет\n• Бариста керек\n• Велосипед издейм</i>',
        'en': '📝 <b>Enter ad title</b>\n\n<i>For example:\n• iPhone 13 128GB\n• 1-room apartment for rent\n• Barista needed\n• Looking for a bike</i>',
        'cn': '📝 <b>输入广告标题</b>\n\n<i>例如：\n• iPhone 13 128GB\n• 出租一居室\n• 需要咖啡师\n• 寻找自行车</i>',
    },
    'ad_desc': {
        'ru': '📝 <b>Опишите объявление подробнее</b>\n\n<i>Можно указать:\n• состояние / опыт / требования\n• характеристики или условия\n• район / комплектацию\n• любую важную информацию</i>',
        'kg': '📝 <b>Жарыяны кеңири сүрөттөп бериңиз</b>\n\n<i>Көрсөтүңүз:\n• абалы / тажрыйба / талаптар\n• өзгөчөлүктөрү же шарттары\n• район / комплектация\n• маанилүү маалымат</i>',
        'en': '📝 <b>Describe the ad in detail</b>\n\n<i>You can specify:\n• condition / experience / requirements\n• features or terms\n• area / package\n• any important info</i>',
        'cn': '📝 <b>详细描述广告</b>\n\n<i>可以注明：\n• 状况/经验/要求\n• 特点或条件\n• 区域/配置\n• 任何重要信息</i>',
    },
    'ad_price': {
        'ru': '💵 <b>Укажите цену в KGS:</b>\n\n<i>Введите только число, например: 2500</i>',
        'kg': '💵 <b>Бааны KGS менен көрсөтүңүз:</b>\n\n<i>Сан гана жазыңыз, мисалы: 2500</i>',
        'en': '💵 <b>Enter the price in KGS:</b>\n\n<i>Enter only a number, e.g.: 2500</i>',
        'cn': '💵 <b>请输入价格（KGS）：</b>\n\n<i>只输入数字，例如：2500</i>',
    },
    'price_must_be_number': {
        'ru': '❗️ Цена должна быть числом. Введите только число, например: 3500',
        'kg': '❗️ Баа сан болушу керек. Сан гана жазыңыз, мисалы: 3500',
        'en': '❗️ Price must be a number. Enter only a number, e.g.: 3500',
        'cn': '❗️ 价格必须为数字。只输入数字，例如：3500',
    },
    'add_photos': {
        'ru': '📸 <b>Добавьте фотографии товара</b>\n\n• Можно загрузить до 10 фото\n• Отправляйте по одному фото\n• Когда закончите — напишите \'Готово\' или нажмите кнопку \'Готово ✅\'',
        'kg': '📸 <b>Товардын сүрөттөрүн кошуңуз</b>\n\n• 10 сүрөткө чейин жүктөңүз\n• Ар бирин өзүнчө жөнөтүңүз\n• Бүткөндө — \'Даяр\' деп жазыңыз же \'Даяр ✅\' баскычын басыңыз',
        'en': '📸 <b>Add product photos</b>\n\n• You can upload up to 10 photos\n• Send one by one\n• When done — type \'Done\' or press \'Done ✅\'',
        'cn': '📸 <b>添加商品照片</b>\n\n• 最多可上传 10 张照片\n• 一次发送一张\n• 完成后输入“完成”或点击“完成 ✅”按钮',
    },
    'max_10_photos': {
        'ru': '⚠️ Максимум 10 фото! Нажмите \'Готово ✅\' когда закончите.',
        'kg': '⚠️ Көп дегенде 10 сүрөт! Бүткөндө \'Даяр ✅\' баскычын басыңыз.',
        'en': '⚠️ Maximum 10 photos! Press \'Done ✅\' when finished.',
        'cn': '⚠️ 最多 10 张照片！完成后请点击“完成 ✅”。',
    },
    'photo_added': {
        'ru': '✅ Фото {n}/10 добавлено. Добавьте ещё или нажмите \'Готово ✅\'.',
        'kg': '✅ {n}/10 сүрөт кошулду. Дагы кошуңуз же \'Даяр ✅\' басыңыз.',
        'en': '✅ Photo {n}/10 added. Add more or press \'Done ✅\'.',
        'cn': '✅ 已添加 {n}/10 张照片。可继续添加或点击“完成 ✅”。',
    },
    'add_at_least_one_photo': {
        'ru': '❌ Сначала добавьте хотя бы одно фото!',
        'kg': '❌ Алгач жок дегенде бир сүрөт кошуңуз!',
        'en': '❌ Add at least one photo first!',
        'cn': '❌ 请先添加至少一张照片！',
    },
    'send_photo_or_done': {
        'ru': '📸 Отправьте фото товара или напишите \'Готово\' когда добавите все фото.',
        'kg': '📸 Товардын сүрөтүн жөнөтүңүз же бүтсөңүз \'Даяр\' деп жазыңыз.',
        'en': '📸 Send product photo or type \'Done\' when finished.',
        'cn': '📸 发送商品照片，完成后输入“完成”。',
    },
    'show_phone': {
        'ru': '📞 Показывать ваш номер телефона в объявлении?',
        'kg': '📞 Жарыяда телефон номериңизди көрсөтөсүзбү?',
        'en': '📞 Show your phone number in the ad?',
        'cn': '📞 在广告中显示您的电话号码吗？',
    },
    'show_phone_yes': {
        'ru': '✅ Показывать номер',
        'kg': '✅ Көрсөтүү',
        'en': '✅ Show',
        'cn': '✅ 显示',
    },
    'show_phone_no': {
        'ru': '❌ Скрыть номер',
        'kg': '❌ Жашыруу',
        'en': '❌ Hide',
        'cn': '❌ 隐藏',
    },
    'hidden': {
        'ru': 'Скрыт',
        'kg': 'Жашыруун',
        'en': 'Hidden',
        'cn': '隐藏',
    },
    'contact': {
        'ru': 'Связаться',
        'kg': 'Байланышуу',
        'en': 'Contact',
        'cn': '联系',
    },
    'ad_preview': {
        'ru': '📝 Предпросмотр объявления. Всё верно?',
        'kg': '📝 Жарыянын алдын ала көрүүсү. Баары туурабы?',
        'en': '📝 Ad preview. Is everything correct?',
        'cn': '📝 广告预览。全部正确吗？',
    },
    'publish': {
        'ru': '🚀 Опубликовать',
        'kg': '🚀 Жариялоо',
        'en': '🚀 Publish',
        'cn': '🚀 发布',
    },
    'cancel': {
        'ru': '❌ Отменить',
        'kg': '❌ Жокко чыгаруу',
        'en': '❌ Cancel',
        'cn': '❌ 取消',
    },
    'ad_published': {
        'ru': '✅ <b>Объявление опубликовано!</b>\nЭто сообщение можете закрепить в лс бота, чтобы не потерять свое объявление.',
        'kg': '✅ <b>Жарыя жарыяланды!</b>\nБул билдирүүнү боттун жеке чатында сактап коюңуз, ошондо жарыяңызды жоготпойсуз.',
        'en': '✅ <b>Ad published!</b>\nYou can pin this message in the bot’s private chat to not lose your ad.',
        'cn': '✅ <b>广告已发布！</b>\n您可以将此消息固定在机器人的私聊中，以免丢失您的广告。',
    },
    'see_in_channel': {
        'ru': '👁️ Посмотреть в канале',
        'kg': '👁️ Каналдан көрүү',
        'en': '👁️ View in channel',
        'cn': '👁️ 在频道查看',
    },
    'feedback': {
        'ru': 'Кстати, если что-то в боте неудобно или у вас есть какие-то предложения - пишите @isbakks',
        'kg': 'Эгер ботто бир нерсе ыңгайсыз болсо же сунуштарыңыз болсо — @isbakks жазгыла',
        'en': 'By the way, if something is inconvenient in the bot or you have suggestions — write to @isbakks',
        'cn': '如果你对机器人有任何建议或不便之处，请联系 @isbakks',
    },
    'sending_ad': {
        'ru': '⏳ Отправляем объявление...',
        'kg': '⏳ Жарыя жөнөтүлүүдө...',
        'en': '⏳ Sending ad...',
        'cn': '⏳ 正在发送广告...',
    },
    'channel_not_found': {
        'ru': '❌ Не удалось определить канал для публикации. Свяжитесь с админом.',
        'kg': '❌ Жарыялоо үчүн канал аныкталган жок. Админге кайрылыңыз.',
        'en': '❌ Failed to determine channel for publication. Contact admin.',
        'cn': '❌ 无法确定发布频道。请联系管理员。',
    },
    'publish_error': {
        'ru': '❌ Ошибка публикации',
        'kg': '❌ Жарыялоо катасы',
        'en': '❌ Publication error',
        'cn': '❌ 发布错误',
    },
    'post_ad': {
        'ru': 'Разместить объявление',
        'kg': 'Жарыя жайгаштыруу',
        'en': 'Post an ad',
        'cn': '发布广告',
    },

    # ---------- Магазины и услуги (shops) ----------
    'shops_title': {
        'ru': '🛒 <b>Магазины и услуги</b>\n\n🗂 <b>Выберите категорию:</b>',
        'kg': '🛒 <b>Дүкөндөр жана кызматтар</b>\n\n🗂 <b>Категорияны тандаңыз:</b>',
        'en': '🛒 <b>Shops and services</b>\n\n🗂 <b>Choose a category:</b>',
        'cn': '🛒 <b>商店和服务</b>\n\n🗂 <b>请选择分类：</b>',
    },
    'no_categories': {
        'ru': 'ℹ️ <b>Нет доступных категорий</b>',
        'kg': 'ℹ️ <b>Категориялар жок</b>',
        'en': 'ℹ️ <b>No available categories</b>',
        'cn': 'ℹ️ <b>没有可用分类</b>',
    },
    'no_shops': {
        'ru': 'ℹ️ <b>Нет магазинов в этой категории</b>',
        'kg': 'ℹ️ <b>Бул категорияда дүкөндөр жок</b>',
        'en': 'ℹ️ <b>No shops in this category</b>',
        'cn': 'ℹ️ <b>此分类下没有商店</b>',
    },
    'choose_shop': {
        'ru': '🏪 <b>Выберите магазин:</b>',
        'kg': '🏪 <b>Дүкөн тандаңыз:</b>',
        'en': '🏪 <b>Choose a shop:</b>',
        'cn': '🏪 <b>请选择商店：</b>',
    },
    'shop_not_found': {
        'ru': '❌ <b>Магазин не найден</b>',
        'kg': '❌ <b>Дүкөн табылган жок</b>',
        'en': '❌ <b>Shop not found</b>',
        'cn': '❌ <b>未找到商店</b>',
    },
    'owner': {
        'ru': 'Владелец',
        'kg': 'Ээси',
        'en': 'Owner',
        'cn': '所有者',
    },
    'address': {
        'ru': 'Адрес',
        'kg': 'Дарек',
        'en': 'Address',
        'cn': '地址',
    },
    'not_specified': {
        'ru': 'Не указан',
        'kg': 'Көрсөтүлгөн эмес',
        'en': 'Not specified',
        'cn': '未指定',
    },
    'description': {
        'ru': 'Описание',
        'kg': 'Сүрөттөмө',
        'en': 'Description',
        'cn': '描述',
    },
    'no_description': {
        'ru': 'Без описания',
        'kg': 'Сүрөттөмөсүз',
        'en': 'No description',
        'cn': '无描述',
    },
    'choose_type': {
        'ru': 'Выберите тип товаров',
        'kg': 'Товар түрүн тандаңыз',
        'en': 'Choose product type',
        'cn': '选择商品类型',
    },
    'products': {
        'ru': 'Товары',
        'kg': 'Товарлар',
        'en': 'Products',
        'cn': '商品',
    },
    'services': {
        'ru': 'Услуги',
        'kg': 'Кызматтар',
        'en': 'Services',
        'cn': '服务',
    },
    'images_count': {
        'ru': 'Фото: {count}',
        'kg': 'Сүрөттөр: {count}',
        'en': 'Photos: {count}',
        'cn': '照片：{count}',
    },
    'preview_add_to_cart': {
        'ru': '🛒 В корзину',
        'kg': '🛒 Себетке',
        'en': '🛒 Add to cart',
        'cn': '🛒 加入购物车',
    },
    'preview_cancel': {
        'ru': '❌ Отменить',
        'kg': '❌ Жокко чыгаруу',
        'en': '❌ Cancel',
        'cn': '❌ 取消',
    },
    'added_to_cart': {
        'ru': '✅ Товар добавлен в корзину.',
        'kg': '✅ Товар себетке кошулду.',
        'en': '✅ Item added to cart.',
        'cn': '✅ 已添加到购物车。',
    },
    'preview_cancelled': {
        'ru': '❌ Просмотр отменён.',
        'kg': '❌ Кароо жокко чыгарылды.',
        'en': '❌ Preview cancelled.',
        'cn': '❌ 预览已取消。',
    },
    'product_not_found': {
        'ru': '❌ Товар не найден.',
        'kg': '❌ Товар табылган жок.',
        'en': '❌ Item not found.',
        'cn': '❌ 未找到商品。',
    },
    'no_images': {
        'ru': '❌ Изображений нет.',
        'kg': '❌ Сүрөттөр жок.',
        'en': '❌ No images.',
        'cn': '❌ 无图像。',
    },
    'page_indicator': {
        'ru': 'Страница {current}/{total}',
        'kg': 'Бет {current}/{total}',
        'en': 'Page {current}/{total}',
        'cn': '第 {current}/{total} 页',
    },
    'preview_item': {
        'ru': 'Предосмотр товара {}',
        'kg': 'Товардын алдын ала көрүүсү {}',
        'en': 'Product preview {}',
        'cn': '产品预览 {}',
    },
    'view_photos': {
        'ru': '🖼 Посмотреть фото',
        'kg': '🖼 Сүрөттөрдү көрүү',
        'en': '🖼 View photos',
        'cn': '🖼 查看照片',
    },
    'back_to_preview': {
        'ru': '↩️ Назад к превью',
        'kg': '↩️ Превьюгө кайтуу',
        'en': '↩️ Back to preview',
        'cn': '↩️ 返回预览',
    },
    'photo_prev': {
        'ru': '⬅️ Предыдущее',
        'kg': '⬅️ Мурунку',
        'en': '⬅️ Previous',
        'cn': '⬅️ 上一张',
    },
    'photo_next': {
        'ru': 'Следующее ➡️',
        'kg': 'Кийинки ➡️',
        'en': 'Next ➡️',
        'cn': '下一张 ➡️',
    },
    'cart': {
        'ru': '🛒 Корзина',
        'kg': '🛒 Себет',
        'en': '🛒 Cart',
        'cn': '🛒 购物车',
    },
    'back_to_type': {
        'ru': '↩️ Назад к выбору типа',
        'kg': '↩️ Түрүн тандоого кайтуу',
        'en': '↩️ Back to type selection',
        'cn': '↩️ 返回类型选择',
    },
    'cart_empty': {
        'ru': '❌ <b>Ваша корзина пуста!</b>',
        'kg': '❌ <b>Себетиңиз бош!</b>',
        'en': '❌ <b>Your cart is empty!</b>',
        'cn': '❌ <b>您的购物车为空！</b>',
    },
    'cart_total': {
        'ru': ' <b>Итого: {total} KGS</b>',
        'kg': ' <b>Жыйынтыгы: {total} KGS</b>',
        'en': ' <b>Total: {total} KGS</b>',
        'cn': ' <b>合计：{total} KGS</b>',
    },
    'order_confirm': {
        'ru': '✅ Оформить заказ',
        'kg': '✅ Заказды ырастоо',
        'en': '✅ Confirm order',
        'cn': '✅ 确认订单',
    },
    'continue_shopping': {
        'ru': '🛒 Продолжить покупки',
        'kg': '🛒 Сатып алууну улантуу',
        'en': '🛒 Continue shopping',
        'cn': '🛒 继续购物',
    },
    'cart_cancel': {
        'ru': '❌ Отменить',
        'kg': '❌ Жокко чыгаруу',
        'en': '❌ Cancel',
        'cn': '❌ 取消',
    },
    'order_done': {
        'ru': '✅ <b>Ваш заказ #{order_id} оформлен!</b>',
        'kg': '✅ <b>Сиздин заказ #{order_id} кабыл алынды!</b>',
        'en': '✅ <b>Your order #{order_id} is placed!</b>',
        'cn': '✅ <b>您的订单 #{order_id} 已下单！</b>',
    },
    'order_completed': {
        'ru': '✅ Заказ завершён! Спасибо за покупку.\n\n📞 Владелец магазина свяжется с вами для уточнения деталей.',
        'kg': '✅ Заказ аяктады! Сатып алганыңыз үчүн рахмат.\n\n📞 Дүкөн ээси сиз менен байланышат.',
        'en': '✅ Order completed! Thank you for your purchase.\n\n📞 The shop owner will contact you for details.',
        'cn': '✅ 订单已完成！感谢您的购买。\n\n📞 店主会与您联系确认细节。',
    },
    'delivery_question': {
        'ru': '🚚 Желаете ли вы доставку заказа?',
        'kg': '🚚 Заказды жеткирүү керекпи?',
        'en': '🚚 Do you want delivery?',
        'cn': '🚚 需要配送吗？',
    },
    'delivery_yes': {
        'ru': '✅ Да',
        'kg': '✅ Ооба',
        'en': '✅ Yes',
        'cn': '✅ 是',
    },
    'delivery_no': {
        'ru': '❌ Нет',
        'kg': '❌ Жок',
        'en': '❌ No',
        'cn': '❌ 否',
    },
    'send_delivery_point': {
        'ru': '📍 Отправьте ваше текущее местоположение (куда нужно привезти заказ):',
        'kg': '📍 Заказды жеткирүүчү даректи жөнөтүңүз:',
        'en': '📍 Send your current location (where to deliver the order):',
        'cn': '📍 发送您的当前位置（送货地址）：',
    },
    'delivery_cancelled': {
        'ru': '❌ Доставка отменена',
        'kg': '❌ Жеткирүү жокко чыгарылды',
        'en': '❌ Delivery cancelled',
        'cn': '❌ 配送已取消',
    },
    'order_error': {
        'ru': '❌ <b>Ошибка:</b> Пользователь не найден!',
        'kg': '❌ <b>Ката:</b> Колдонуучу табылган жок!',
        'en': '❌ <b>Error:</b> User not found!',
        'cn': '❌ <b>错误：</b>未找到用户！',
    },
    'shop_delivery_not_configured': {
        'ru': '❌ В этом магазине не настроена доставка',
        'kg': '❌ Бул дүкөндө жеткирүү жок',
        'en': '❌ Delivery is not configured for this shop',
        'cn': '❌ 此商店未配置配送',
    },
    'send_point_b': {
        'ru': '📍 Отправить точку доставки',
        'kg': '📍 Жеткирүү чекитин жөнөтүү',
        'en': '📍 Send delivery point',
        'cn': '📍 发送配送点',
    },
    'order_preview': {
        'ru': '📌 Предпросмотр заказа',
        'kg': '📌 Заказдын алдын ала көрүүсү',
        'en': '📌 Order preview',
        'cn': '📌 订单预览',
    },
    'point_a': {
        'ru': 'Точка А',
        'kg': 'А чекити',
        'en': 'Point A',
        'cn': 'A点',
    },
    'point_b': {
        'ru': 'Точка Б',
        'kg': 'Б чекити',
        'en': 'Point B',
        'cn': 'B点',
    },
    'distance': {
        'ru': 'Расстояние',
        'kg': 'Аралык',
        'en': 'Distance',
        'cn': '距离',
    },
    'price': {
        'ru': 'Стоимость',
        'kg': 'Баасы',
        'en': 'Price',
        'cn': '价格',
    },
    'comment': {
        'ru': 'Комментарий',
        'kg': 'Комментарий',
        'en': 'Comment',
        'cn': '备注',
    },
    'none': {
        'ru': 'нет',
        'kg': 'жок',
        'en': 'none',
        'cn': '无',
    },
    'confirm': {
        'ru': '✅ Подтвердить',
        'kg': '✅ Ырастоо',
        'en': '✅ Confirm',
        'cn': '✅ 确认',
    },
    'confirm_order': {
        'ru': 'Подтвердите заказ:',
        'kg': 'Заказды ырастоо:',
        'en': 'Confirm the order:',
        'cn': '请确认订单：',
    },
    'send_point_a': {
        'ru': '📍 Отправить точку А',
        'kg': '📍 А чекитин жөнөтүү',
        'en': '📍 Send point A',
        'cn': '📍 发送A点',
    },
    'send_point_a_text': {
        'ru': '📍 Отправьте точку А (забор):',
        'kg': '📍 А чекитин жөнөтүңүз (алуу):',
        'en': '📍 Send point A (pickup):',
        'cn': '📍 发送A点（取货）：',
    },
    'send_point_b_text': {
        'ru': '📍 Отправьте точку Б (доставка):',
        'kg': '📍 Б чекитин жөнөтүңүз (жеткирүү):',
        'en': '📍 Send point B (delivery):',
        'cn': '📍 发送B点（配送）：',
    },
    'enter_comment': {
        'ru': '📝 Введите комментарий или нажмите «Пропустить»',
        'kg': '📝 Комментарий жазыңыз же «Өткөрүү» баскычын басыңыз',
        'en': '📝 Enter a comment or press “Skip”',
        'cn': '📝 输入备注或点击“跳过”',
    },
    'skip': {
        'ru': '📝 Пропустить',
        'kg': '📝 Өткөрүү',
        'en': '📝 Skip',
        'cn': '📝 跳过',
    },
        # ---------- Дополнительные ключи для sellbuy ----------
    'pay_placement_button': {
        'ru': '💵 Оплатить 15 сом (быстро)',
        'kg': '💵 15 сом төлөө (тез)',
        'en': '💵 Pay 15 KGS (fast)',
        'cn': '💵 支付 15 索姆（快速）',
    },
    'choose_status': {
        'ru': '🗂 Категория: <b>{category}</b>\n\n📌 Выберите тип вашего объявления:',
        'kg': '🗂 Категория: <b>{category}</b>\n\n📌 Жарыяңыздын түрүн тандаңыз:',
        'en': '🗂 Category: <b>{category}</b>\n\n📌 Choose the type of your ad:',
        'cn': '🗂 分类：<b>{category}</b>\n\n📌 请选择广告类型：',
    },
    'status_sell': {
        'ru': '💰 Продажа',
        'kg': '💰 Сатуу',
        'en': '💰 Sell',
        'cn': '💰 出售',
    },
    'status_exchange': {
        'ru': '🔄 Обмен',
        'kg': '🔄 Алмашуу',
        'en': '🔄 Exchange',
        'cn': '🔄 交换',
    },
    'status_search': {
        'ru': '🔍 Поиск',
        'kg': '🔍 Издөө',
        'en': '🔍 Search',
        'cn': '🔍 寻找',
    },
    'status_hand': {
        'ru': '🔑 Сдаю',
        'kg': '🔑 Ижарага берем',
        'en': '🔑 Rent out',
        'cn': '🔑 出租',
    },
    'status_resume': {
        'ru': '👨‍💼 Резюме',
        'kg': '👨‍💼 Резюме',
        'en': '👨‍💼 Resume',
        'cn': '👨‍💼 简历',
    },
    'status_vacancy': {
        'ru': '💼 Вакансия',
        'kg': '💼 Вакансия',
        'en': '💼 Vacancy',
        'cn': '💼 职位空缺',
    },
    'status_poda': {
        'ru': '👀 Подаюсь',
        'kg': '👀 Сунуштайм',
        'en': '👀 Offer',
        'cn': '👀 提供',
    },
    'done_button': {
        'ru': 'Готово ✅',
        'kg': 'Даяр ✅',
        'en': 'Done ✅',
        'cn': '完成 ✅',
    },
    'phone': {
        'ru': 'Телефон',
        'kg': 'Телефон',
        'en': 'Phone',
        'cn': '电话',
    },
    'error_invalid_data': {
        'ru': '❌ Ошибка данных. Повторите попытку.',
        'kg': '❌ Маалымат катасы. Кайра аракет кылыңыз.',
        'en': '❌ Data error. Please try again.',
        'cn': '❌ 数据错误。请重试。',
    },
    'error_sending_receipt': {
        'ru': '❌ Ошибка при отправке чека админу: {error}',
        'kg': '❌ Чекти админге жөнөтүүдө ката: {error}',
        'en': '❌ Error sending receipt to admin: {error}',
        'cn': '❌ 向管理员发送收据时出错：{error}',
    },
    'admin_only': {
        'ru': 'Только админ может выполнить это действие.',
        'kg': 'Бул аракетти админ гана жасай алат.',
        'en': 'Only admin can perform this action.',
        'cn': '只有管理员可以执行此操作。',
    },
    'payment_confirmed_admin': {
        'ru': 'Оплата подтверждена',
        'kg': 'Төлөм ырасталды',
        'en': 'Payment confirmed',
        'cn': '付款已确认',
    },
    'payment_declined_admin': {
        'ru': 'Оплата отклонена',
        'kg': 'Төлөм четке кагылды',
        'en': 'Payment declined',
        'cn': '付款被拒绝',
    },
    'error_occurred': {
        'ru': '❌ Произошла ошибка: {error}',
        'kg': '❌ Ката кетти: {error}',
        'en': '❌ An error occurred: {error}',
        'cn': '❌ 发生错误：{error}',
    },
    'no_username': {
        'ru': 'Без username',
        'kg': 'Username жок',
        'en': 'No username',
        'cn': '无用户名',
    },
    'category': {
        'ru': 'Категория',
        'kg': 'Категория',
        'en': 'Category',
        'cn': '分类',
    },
    # ---------- Названия категорий для инлайн-кнопок ----------
    'category_веломаркет': {
        'ru': '🚲 Веломаркет',
        'kg': '🚲 Велосипед рыногу',
        'en': '🚲 Bike market',
        'cn': '🚲 自行车市场',
    },
    'category_бьютимаркет': {
        'ru': '👕 Бьютимаркет',
        'kg': '👕 Сулуулук рыногу',
        'en': '👕 Beauty market',
        'cn': '👕 美容市场',
    },
    'category_техномаркет': {
        'ru': '💻 Техномаркет',
        'kg': '💻 Техно рыногу',
        'en': '💻 Tech market',
        'cn': '💻 科技市场',
    },
    'category_автомотомаркет': {
        'ru': '🚗 Автомотомаркет',
        'kg': '🚗 Автомото рыногу',
        'en': '🚗 Auto-moto market',
        'cn': '🚗 汽车摩托车市场',
    },
    'category_недвижимость': {
        'ru': '🏠 Недвижимость',
        'kg': '🏠 Недвижимость',
        'en': '🏠 Real estate',
        'cn': '🏠 房地产',
    },
    'category_работа': {
        'ru': '💼 Работа',
        'kg': '💼 Иш',
        'en': '💼 Jobs',
        'cn': '💼 工作',
    },
        # ---------- Доставка (delivery) ----------
    'cancel_all': {
        'ru': '❌ Все-все, прекращаем опрос...',
        'kg': '❌ Баары-баары, сурамжылоо токтотулду...',
        'en': '❌ Cancelled, stopping the survey...',
        'cn': '❌ 取消，停止询问...',
    },
    'not_registered_or_banned': {
        'ru': '❗️ Вы не зарегистрированы или заблокированы.',
        'kg': '❗️ Сиз катталган эмессиз же бөгөттөлгөнсүз.',
        'en': '❗️ You are not registered or are banned.',
        'cn': '❗️ 您尚未注册或已被封禁。',
    },
    'send_point_a_btn': {
        'ru': '📍 Отправить точку А',
        'kg': '📍 А чекитин жөнөтүү',
        'en': '📍 Send point A',
        'cn': '📍 发送A点',
    },
    'send_point_a_text': {
        'ru': '📍 Отправьте точку А (забор):',
        'kg': '📍 А чекитин жөнөтүңүз (алуу):',
        'en': '📍 Send point A (pickup):',
        'cn': '📍 发送A点（取货）：',
    },
    'send_point_b_btn': {
        'ru': '📍 Отправить точку Б',
        'kg': '📍 Б чекитин жөнөтүү',
        'en': '📍 Send point B',
        'cn': '📍 发送B点',
    },
    'send_point_b_text': {
        'ru': '📍 Отправьте точку Б (доставка):',
        'kg': '📍 Б чекитин жөнөтүңүз (жеткирүү):',
        'en': '📍 Send point B (delivery):',
        'cn': '📍 发送B点（配送）：',
    },
    'skip_btn': {
        'ru': '📝 Пропустить',
        'kg': '📝 Өткөрүү',
        'en': '📝 Skip',
        'cn': '📝 跳过',
    },
    'enter_comment_text': {
        'ru': '📝 Введите комментарий или нажмите «Пропустить»',
        'kg': '📝 Комментарий жазыңыз же «Өткөрүү» баскычын басыңыз',
        'en': '📝 Enter a comment or press “Skip”',
        'cn': '📝 输入备注或点击“跳过”',
    },
    'order_preview': {
        'ru': '📌 Предпросмотр заказа',
        'kg': '📌 Заказдын алдын ала көрүүсү',
        'en': '📌 Order preview',
        'cn': '📌 订单预览',
    },
    'point_a': {
        'ru': '📍 Точка А',
        'kg': '📍 А чекити',
        'en': '📍 Point A',
        'cn': '📍 A点',
    },
    'point_b': {
        'ru': '📍 Точка Б',
        'kg': '📍 Б чекити',
        'en': '📍 Point B',
        'cn': '📍 B点',
    },
    'distance': {
        'ru': ' Расстояние',
        'kg': ' Аралык',
        'en': ' Distance',
        'cn': ' 距离',
    },
    'price': {
        'ru': ' Стоимость',
        'kg': ' Баасы',
        'en': ' Price',
        'cn': ' 价格',
    },
    'comment': {
        'ru': ' Комментарий',
        'kg': ' Комментарий',
        'en': ' Comment',
        'cn': ' 备注',
    },
    'none': {
        'ru': 'нет',
        'kg': 'жок',
        'en': 'none',
        'cn': '无',
    },
    'confirm_btn': {
        'ru': '✅ Подтвердить',
        'kg': '✅ Ырастоо',
        'en': '✅ Confirm',
        'cn': '✅ 确认',
    },
    'cancel_btn': {
        'ru': '❌ Отменить',
        'kg': '❌ Жокко чыгаруу',
        'en': '❌ Cancel',
        'cn': '❌ 取消',
    },
    'confirm_order_text': {
        'ru': 'Подтвердите заказ:',
        'kg': 'Заказды ырастоо:',
        'en': 'Confirm the order:',
        'cn': '请确认订单：',
    },
    'order_cancelled': {
        'ru': '❌ Заказ отменён.',
        'kg': '❌ Заказ жокко чыгарылды.',
        'en': '❌ Order cancelled.',
        'cn': '❌ 订单已取消。',
    },
    'order_sent_to_couriers': {
        'ru': '✅ Заказ отправлен курьерам.',
        'kg': '✅ Заказ курьерлерге жөнөтүлдү.',
        'en': '✅ Order sent to couriers.',
        'cn': '✅ 订单已发送给快递员。',
    },
    'order_creation_error': {
        'ru': '❌ Ошибка при создании заказа',
        'kg': '❌ Заказ түзүүдө ката кетти',
        'en': '❌ Error creating order',
        'cn': '❌ 创建订单时出错',
    },
    'cannot_take_order': {
        'ru': '❗️ Вы не можете брать заказы',
        'kg': '❗️ Сиз заказдарды ала албайсыз',
        'en': '❗️ You cannot take orders',
        'cn': '❗️ 您不能接单',
    },
    'order_assigned_to_you': {
        'ru': '✅ Заказ назначен вам',
        'kg': '✅ Заказ сизге дайындалды',
        'en': '✅ Order assigned to you',
        'cn': '✅ 订单已分配给您',
    },
    'client': {
        'ru': 'Клиент',
        'kg': 'Клиент',
        'en': 'Client',
        'cn': '客户',
    },
    'order': {
        'ru': 'Заказ',
        'kg': 'Заказ',
        'en': 'Order',
        'cn': '订单',
    },
    'update_status_prompt': {
        'ru': 'Обновите статус заказа:',
        'kg': 'Заказдын статусун жаңыртыңыз:',
        'en': 'Update order status:',
        'cn': '更新订单状态：',
    },
    'order_take_error': {
        'ru': '❌ Ошибка при взятии заказа',
        'kg': '❌ Заказды алууда ката кетти',
        'en': '❌ Error taking order',
        'cn': '❌ 接单时出错',
    },
    'unknown_action': {
        'ru': '❌ Неизвестное действие',
        'kg': '❌ Белгисиз аракет',
        'en': '❌ Unknown action',
        'cn': '❌ 未知操作',
    },
    'order_not_found': {
        'ru': '❌ Заказ не найден',
        'kg': '❌ Заказ табылган жок',
        'en': '❌ Order not found',
        'cn': '❌ 未找到订单',
    },
    'not_your_order': {
        'ru': '❗️ Это не ваш заказ',
        'kg': '❗️ Бул сиздин заказ эмес',
        'en': '❗️ This is not your order',
        'cn': '❗️ 这不是您的订单',
    },
    'order_status_updated': {
        'ru': '🔄 Статус заказа #{order_id} обновлён: {status}',
        'kg': '🔄 #{order_id} заказдын статусу жаңырды: {status}',
        'en': '🔄 Order #{order_id} status updated: {status}',
        'cn': '🔄 订单 #{order_id} 状态已更新：{status}',
    },
    'next_step_prompt': {
        'ru': 'Далее:',
        'kg': 'Андан ары:',
        'en': 'Next:',
        'cn': '下一步：',
    },
    'status_new': {
        'ru': 'Новый',
        'kg': 'Жаңы',
        'en': 'New',
        'cn': '新',
    },
    'status_assigned': {
        'ru': 'Назначен',
        'kg': 'Дайындалган',
        'en': 'Assigned',
        'cn': '已分配',
    },
    'status_to_a': {
        'ru': 'В пути до точки А',
        'kg': 'А чекитине бара жатат',
        'en': 'En route to point A',
        'cn': '前往A点',
    },
    'status_to_b': {
        'ru': 'В пути до точки Б',
        'kg': 'Б чекитине бара жатат',
        'en': 'En route to point B',
        'cn': '前往B点',
    },
    'status_arrived': {
        'ru': 'Приехал',
        'kg': 'Келди',
        'en': 'Arrived',
        'cn': '已到达',
    },
    'status_completed': {
        'ru': 'Завершён',
        'kg': 'Аяктады',
        'en': 'Completed',
        'cn': '已完成',
    },
    'to_a_btn': {
        'ru': '🚩 В пути до A',
        'kg': '🚩 Ага бара жатат',
        'en': '🚩 En route to A',
        'cn': '🚩 前往A点',
    },
    'to_b_btn': {
        'ru': '🚩 В пути до B',
        'kg': '🚩 Бга бара жатат',
        'en': '🚩 En route to B',
        'cn': '🚩 前往B点',
    },
    'arrived_btn': {
        'ru': '✅ Прибыл',
        'kg': '✅ Келди',
        'en': '✅ Arrived',
        'cn': '✅ 已到达',
    },
    'delivery_currency': {
        'ru': 'KGS',
        'kg': 'KGS',
        'en': 'KGS',
        'cn': 'KGS',
    },
    'delivery_distance_unit': {
        'ru': 'км',
        'kg': 'км',
        'en': 'km',
        'cn': '公里',
    },
    'menu_button': {
        'ru': 'Меню',
        'kg': 'Меню',
        'en': 'Menu',
        'cn': '菜单',
    },
    "pin_pls_send_message": {
        'ru': (
            "📌 <b>Закрепление объявления в канале</b>\n\n"
            "Хотите, чтобы ваше объявление всегда было вверху и его никто не пропустил?\n\n"
            "🔹 Отправьте <b>пересланное сообщение</b> из нашего канала (того, где вы разместили объявление).\n"
            "🔹 Я закреплю его на <b>10 дней</b>.\n"
            "🔹 Стоимость — <b>130 сом</b>.\n\n"
            "💡 <i>Закрепление делает ваше предложение заметнее, а значит — больше просмотров и быстрые продажи!</i>\n\n"
            "👉 Просто перешлите своё объявление сюда, и я покажу, как оплатить."
        ),
        'kg': (
            "📌 <b>Каналда жарыяны бекемдөө (закрепление)</b>\n\n"
            "Өзүңүздүн жарыяңыз ар дайым өйдө турсун жана эч ким аны өткөрүп жибербесин каалайсызбы?\n\n"
            "🔹 Биздин каналдан <b>кайра жөнөтүлгөн билдирүүнү</b> (сиз жарыя жайгаштырган каналдан) жибериңиз.\n"
            "🔹 Мен аны <b>10 күнгө</b> бекемдейм.\n"
            "🔹 Баасы — <b>130 сом</b>.\n\n"
            "💡 <i>Бекемдөө сиздин сунушуңузду көзгө урунтат, демек көбүрөөк көрүүлөр жана тез сатылуу!</i>\n\n"
            "👉 Өзүңүздүн жарыяңызды ушул жерге кайра жөнөтүңүз, мен кантип төлөөнү көрсөтөм."
        ),
        'en': (
            "📌 <b>Pin your ad in the channel</b>\n\n"
            "Want your ad to always stay on top and never be missed?\n\n"
            "🔹 Send a <b>forwarded message</b> from our channel (the one where you posted your ad).\n"
            "🔹 I will pin it for <b>10 days</b>.\n"
            "🔹 Price — <b>130 som</b>.\n\n"
            "💡 <i>Pinning makes your offer stand out, which means more views and faster sales!</i>\n\n"
            "👉 Just forward your ad here, and I'll show you how to pay."
        ),
        'cn': (
            "📌 <b>在频道中置顶您的广告</b>\n\n"
            "希望您的广告始终置顶，不被错过？\n\n"
            "🔹 请从我们的频道（您发布广告的那个）<b>转发消息</b>。\n"
            "🔹 我会将其置顶 <b>10 天</b>。\n"
            "🔹 价格 — <b>130 索姆</b>。\n\n"
            "💡 <i>置顶让您的报价更显眼，意味着更多浏览和更快的销售！</i>\n\n"
            "👉 只需将您的广告转发到这里，我会告诉您如何支付。"
        )
    },
    'pin_pls_send_payment': {
        'ru': '📌 Теперь оплатите 120 сом на MBank: 771514979 (Бакай Т) и скиньте фото чека в бот. Закрепление будет действительно в течение 10 дней.',
        'kg': '📌 Учурда 120 сомду MBank: 771514979 (Бакай Т) аккаунтуна төлөңүз жана чектин ботко жөнөтүңүз. Закрепление будет действительно в течение 10 дней.',
        'en': '📌 Now pay 120 som to MBank: 771514979 (Bakai T) and send a photo of the receipt to the bot. The pinning will be valid for 10 days.',
        'cn': '📌 现在请在 MBank: 771514979 (Bakai T) 账户上支付 120 som，并将收据照片发送给机器人。固定将在10天内有效。',
    },
    'pin_forward_only': {
        'ru': '📌 Пожалуйста, отправьте сообщение ИМЕННО С КАНАЛА.',
        'kg': '📌 Сураныч, билдирүү ТАК КАНАЛДАН жөнөтүңүз.',
        'en': '📌 Please send the message EXCLUSIVELY FROM THE CHANNEL.',
        'cn': '📌 请从频道发送消息。',
    },
    "pin_preview": {
        'ru': '✅ Обьявление с {channel_username} готово к закреплению!',
        'kg': '✅ {channel_username} каналындагы жарыя закрепление үчүн даяр!',
        'en': '✅ The ad from {channel_username} is ready for pinning!',
        'cn': '✅ 来自 {channel_username} 的广告已准备好固定！',
    },
    "pin_command_start": {
        'ru': '📌 Отправьте пересланное сообщение с канала для закрепления на 10 дней.',
        'kg': '📌 Каналдан билдирүү жөнөтүңүз, 10 күнге закрепление үчүн.',
        'en': '📌 Send a forwarded message from the channel to pin for 10 days.',
        'cn': '📌 发送频道转发的消息以固定10天。',
    },
    "pin_payment_instruction": {
        'ru': '💳 Для закрепления на 10 дней оплатите 130 сом. MBank: 771514979 (Бакай Т). Отправьте фото чека оплаты.',
        'kg': '💳 10 күнге закрепление үчүн 130 сом төлөңүз. MBank: 771514979 (Бакай Т). Төлөм чекинин сүрөтүн жөнөтүңүз.',
        'en': '💳 To pin for 10 days, pay 130 som. MBank: 771514979 (Bakai T). Send a photo of the payment receipt.',
        'cn': '💳 要固定10天，请支付130索姆。MBank: 771514979 (Bakai T)。发送付款收据的照片。',
    },
    "pin_receipt_sent": {
        'ru': '✅ Чек отправлен на проверку админу.',
        'kg': '✅ Чек админге текшерүү үчүн жөнөтүлдү.',
        'en': '✅ Receipt sent for admin verification.',
        'cn': '✅ 收据已发送给管理员验证。',
    },
    "pin_payment_confirmed": {
        'ru': '✅ Оплата подтверждена! Сообщение закреплено на 10 дней.',
        'kg': '✅ Төлөм тастыкталды! Билдирүү 10 күнге закрепленди.',
        'en': '✅ Payment confirmed! Message pinned for 10 days.',
        'cn': '✅ 付款确认！消息固定10天。',
    },
    "pin_payment_declined": {
        'ru': '❌ Оплата отклонена.',
        'kg': '❌ Төлөм четке кагылды.',
        'en': '❌ Payment declined.',
        'cn': '❌ 付款被拒绝。',
    },
    "pin_confirm_admin": {
        'ru': '✅ Подтвердить закрепление',
        'kg': '✅ Закрепление тастыктоо',
        'en': '✅ Confirm pinning',
        'cn': '✅ 确认固定',
    },
    "pin_decline_admin": {
        'ru': '❌ Отклонить',
        'kg': '❌ Четке кагуу',
        'en': '❌ Decline',
        'cn': '❌ 拒绝',
    },
    "pin_unpinned": {
        'ru': '📌 Сообщение автоматически откреплено.',
        'kg': '📌 Билдирүү автоматтык түрдө открепленди.',
        'en': '📌 Message automatically unpinned.',
        'cn': '📌 消息自动取消固定。',
    },
    "pin_wrong_channel": {
        'ru': 'Сообщение должно быть из одного из наших каналов.',
        'kg': 'Билдирүү биздин каналдардан биринен болушу керек.',
        'en': 'The message must be from one of our channels.',
        'cn': '消息必须来自我们的频道之一。',
    },
    "send_receipt_photo": {
        'ru': '📸 Отправьте фото чека оплаты.',
        'kg': '📸 Төлөм чекинин сүрөтүн жөнөтүңүз.',
        'en': '📸 Send a photo of the payment receipt.',
        'cn': '📸 发送付款收据的照片。',
    },
    "error_sending_receipt": {
        'ru': '❌ Ошибка отправки чека: {error}',
        'kg': '❌ Чек жөнөтүүдө ката: {error}',
        'en': '❌ Error sending receipt: {error}',
        'cn': '❌ 发送收据错误：{error}',
    },
    "pin_begin": {
        'ru': '📌 Закреп',
        'en': '📌 Pinning',
        'kg': '📌 Закреп',
        'cn': '📌 固定',
    },
    "subscription_menu": {
        'ru': '💎 Подписка',
        'kg': '💎 Жазылуу',
        'en': '💎 Subscription',
        'cn': '💎 订阅'
    },
    'subscription_active': {
        'ru': "✅ Ваша подписка активирована! До ее окончания осталось {time}",
        'kg': "✅ Сиздин жазылууңуз активдештирилди! Анын аякталышына {time} калды.",
        'en': "✅ Your subscription is activated! It will expire in {time}.",
        'cn': "✅ 您的订阅已激活！它将在 {time} 后过期。",
    },
    'subscription_start': {
        'ru': (
            "🌟 <b>Подписка TEZZ — твой безлимит на 30 дней!</b>\n\n"
            "💰 Всего <b>500 сом</b> — и ты получаешь:\n"
            "✅ Безлимитные объявления во всех маркетах\n"
            "✅ Никаких задержек и ограничений\n"
            "✅ Экономию времени и нервов\n\n"
            "👥 Можно пользоваться <b>самому</b> или <b>делить с друзьями</b> (до 3 человек)!\n\n"
            "🔥 Окупится с первого же объявления — попробуй!"
        ),
        'kg': (
            "🌟 <b>TEZZ жазылуусу — 30 күнгө чексіз мүмкүндүк!</b>\n\n"
            "💰 Баары <b>500 сом</b> — жана сиз аласыз:\n"
            "✅ Бардык маркеттерде чексіз жарыялар\n"
            "✅ Эч кандай кечигүү жана чектөөлөр\n"
            "✅ Убакытты жана нервдерди үнөмдөө\n\n"
            "👥 Өзүңүз <b>пайдалана аласыз</b> же <b>досторуңуз менен бөлүшө аласыз</b> (3 кишиге чейин)!\n\n"
            "🔥 Биринчи жарыяңыздан эле өзүн актайт — аракет кылып көрүңүз!"
        ),
        'en': (
            "🌟 <b>TEZZ Subscription — unlimited power for 30 days!</b>\n\n"
            "💰 Only <b>500 som</b> and you get:\n"
            "✅ Unlimited ads in all markets\n"
            "✅ No delays or restrictions\n"
            "✅ Save time and nerves\n\n"
            "👥 Use it <b>yourself</b> or <b>share with friends</b> (up to 3 people)!\n\n"
            "🔥 Pays off with your very first ad — give it a try!"
        ),
        'cn': (
            "🌟 <b>TEZZ 订阅 — 30天无限畅用！</b>\n\n"
            "💰 只需 <b>500 索姆</b>，你将获得：\n"
            "✅ 在所有市场无限发布广告\n"
            "✅ 无延迟，无限制\n"
            "✅ 节省时间和精力\n\n"
            "👥 可以<b>自己使用</b>或<b>与朋友分享</b>（最多3人）！\n\n"
            "🔥 第一个广告就回本 — 快来试试吧！"
        )
    },
    'subscription_pls_send_payment': {
        'ru': '💳 Пожалуйста, пополните 500 сом на MBank: 771514979 (Бакай Т), затем отправьте чек сразу сюда в бот.',
        'kg': '💳 Сураныч, 500 сомду MBank: 771514979 (Бакай Т) аккаунтуна төлөңүз, андан кийин чектин сүрөтүн ушул жерге жөнөтүңүз.',
        'en': '💳 Please deposit 500 som to MBank: 771514979 (Bakay T), then send the receipt here to the bot.',
        'cn': '💳 请充值500索姆到MBank: 771514979 (Bakay T)，然后将收据发送到这里给机器人。'
    },
    'subscription_receipt_sent': {
        'ru': '✅ Чек отправлен администратору. После подтверждения подписка станет активной.',
        'kg': '✅ Чек администраторго жөнөтүлдү. Ырастоодон кийин жазылуу активдүү болот.',
        'en': '✅ Receipt sent to admin. Subscription will be activated after confirmation.',
        'cn': '✅ 收据已发送给管理员。确认后订阅将被激活。',
    },
    'subscription_payment_confirmed': {
        'ru': '✅ Подписка активирована на {days} дней! Теперь у вас безлимит во всех маркетах.',
        'kg': '✅ Жазылуу {days} күнгө активдештирилди! Эми бардык маркеттерде чексіз мүмкүндүк.',
        'en': '✅ Subscription activated for {days} days! Now you have unlimited access to all markets.',
        'cn': '✅ 订阅已激活 {days} 天！现在您在所有市场都享有无限权限。',
    },
    'subscription_payment_declined': {
        'ru': '❌ Оплата не подтверждена. Попробуйте ещё раз или свяжитесь с поддержкой.',
        'kg': '❌ Төлөм ырасталган жок. Кайра аракет кылыңыз же колдоо кызматына кайрылыңыз.',
        'en': '❌ Payment not confirmed. Please try again or contact support.',
        'cn': '❌ 付款未确认。请重试或联系客服。',
    },
    'enter_subcategory': {
        'ru': '📂 Выберите подходяющую подкатегорию:',
        'kg': '📂 Ылайыктуу подкатегорияны тандаңыз:',
        'en': '📂 Choose a subcategory:',
        'cn': '📂 请选择子类别：',
    },
    'subcategory_frameset': {'ru': 'Рамы', 'kg': 'Рамкалар', 'en': 'Frames', 'cn': '车架'},
    'subcategory_wheelset': {'ru': 'Колёса', 'kg': 'Дөңгөлөктөр', 'en': 'Wheels', 'cn': '车轮'},
    'subcategory_fullbike': {'ru': 'Полный велосипед', 'kg': 'Толук велосипед', 'en': 'Complete bike', 'cn': '整车'},
    'subcategory_components': {'ru': 'Комплектующие', 'kg': 'Тетиктер', 'en': 'Components', 'cn': '配件'},
    'subcategory_crankset': {'ru': 'Каркас', 'kg': 'Каркас', 'en': 'Frame', 'cn': '车架'},
    'subcategory_accessories': {'ru': 'Аксессуары', 'kg': 'Аксессуарлар', 'en': 'Accessories', 'cn': '附件'},
    'subcategory_clothing': {'ru': 'Одежда', 'kg': 'Кийим', 'en': 'Clothing', 'cn': '服装'},
    'subcategory_velo': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    # Бьютимаркет
    'subcategory_makeup': {'ru': 'Макияж', 'kg': 'Макияж', 'en': 'Makeup', 'cn': '化妆'},
    'subcategory_skincare': {'ru': 'Уход за кожей', 'kg': 'Териге кам көрүү', 'en': 'Skincare', 'cn': '护肤'},
    'subcategory_haircare': {'ru': 'Уход за волосами', 'kg': 'Чачка кам көрүү', 'en': 'Haircare', 'cn': '护发'},
    'subcategory_fragrance': {'ru': 'Духи', 'kg': 'Атыр', 'en': 'Perfume', 'cn': '香水'},
    'subcategory_tools': {'ru': 'Инструменты', 'kg': 'Аспаптар', 'en': 'Tools', 'cn': '工具'},
    'subcategory_nails': {'ru': 'Маникюр и педикюр', 'kg': 'Маникюр жана педикюр', 'en': 'Manicure & Pedicure', 'cn': '美甲/足部护理'},
    'subcategory_models': {'ru': 'Модели', 'kg': 'Моделдер', 'en': 'Models', 'cn': '模特'},
    'subcategory_beauty': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    # Техномаркет
    'subcategory_phones': {'ru': 'Телефоны', 'kg': 'Телефондор', 'en': 'Phones', 'cn': '手机'},
    'subcategory_laptops': {'ru': 'Ноутбуки', 'kg': 'Ноутбуктар', 'en': 'Laptops', 'cn': '笔记本电脑'},
    'subcategory_tablets': {'ru': 'Планшеты', 'kg': 'Планшеттер', 'en': 'Tablets', 'cn': '平板电脑'},
    'subcategory_wearables': {'ru': 'Гаджеты', 'kg': 'Гаджеттер', 'en': 'Gadgets', 'cn': '智能设备'},
    'subcategory_audio': {'ru': 'Аудио', 'kg': 'Аудио', 'en': 'Audio', 'cn': '音频'},
    'subcategory_gaming': {'ru': 'Игры', 'kg': 'Оюндар', 'en': 'Games', 'cn': '游戏'},
    'subcategory_cameras': {'ru': 'Фото и видео', 'kg': 'Фото жана видео', 'en': 'Photo & Video', 'cn': '摄影与视频'},
    'subcategory_techno': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    # Автомотомаркет
    'subcategory_cars': {'ru': 'Легковые автомобили', 'kg': 'Жеңил унаалар', 'en': 'Cars', 'cn': '乘用车'},
    'subcategory_motorcycles': {'ru': 'Мотоциклы', 'kg': 'Мотоциклдер', 'en': 'Motorcycles', 'cn': '摩托车'},
    'subcategory_parts': {'ru': 'Запчасти', 'kg': 'Запастык тетиктер', 'en': 'Spare parts', 'cn': '零部件'},
    'subcategory_tires': {'ru': 'Шины', 'kg': 'Шиналар', 'en': 'Tires', 'cn': '轮胎'},
    'subcategory_automoto': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    # Недвижимость
    'subcategory_apartment': {'ru': 'Квартира', 'kg': 'Квартира', 'en': 'Apartment', 'cn': '公寓'},
    'subcategory_house': {'ru': 'Дом', 'kg': 'Үй', 'en': 'House', 'cn': '住宅'},
    'subcategory_land': {'ru': 'Земельный участок', 'kg': 'Жер тилкеси', 'en': 'Land plot', 'cn': '地块'},
    'subcategory_commercial': {'ru': 'Коммерческая недвижимость', 'kg': 'Коммерциялык кыймылсыз мүлк', 'en': 'Commercial property', 'cn': '商业地产'},
    'subcategory_rent': {'ru': 'Аренда', 'kg': 'Ижара', 'en': 'Rent', 'cn': '租赁'},
    'subcategory_one-bedroom': {'ru': 'Однокомнатная', 'kg': 'Бир бөлмөлүү', 'en': 'One-bedroom', 'cn': '一室'},
    'subcategory_two-bedroom': {'ru': 'Двухкомнатная', 'kg': 'Эки бөлмөлүү', 'en': 'Two-bedroom', 'cn': '两室'},
    'subcategory_three-bedroom': {'ru': 'Трёхкомнатная', 'kg': 'Үч бөлмөлүү', 'en': 'Three-bedroom', 'cn': '三室'},
    'subcategory_housing': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    # Работа
    'subcategory_fulltime': {'ru': 'Полная занятость', 'kg': 'Толук күндүк жумуш', 'en': 'Full-time', 'cn': '全职'},
    'subcategory_parttime': {'ru': 'Частичная занятость', 'kg': 'Толук эмес күндүк жумуш', 'en': 'Part-time', 'cn': '兼职'},
    'subcategory_contract': {'ru': 'Контракт / Проектная работа', 'kg': 'Келишим / Долбоордук иш', 'en': 'Contract / Project work', 'cn': '合同/项目工作'},
    'subcategory_office': {'ru': 'В офисе', 'kg': 'Кеңседе', 'en': 'In office', 'cn': '在办公室'},
    'subcategory_athome': {'ru': 'Удалённая работа', 'kg': 'Алыстан иштөө', 'en': 'Remote work', 'cn': '远程工作'},
    'subcategory_job': {'ru': 'Другое', 'kg': 'Башка', 'en': 'Other', 'cn': '其他'},
    'negotiated_price': {
        'ru': 'Договорная',
        'kg': 'Келишим баасы',
        'en': 'Negotiated',
        'cn': '面议',
    },
    'delete_ad': {
        'ru': '❌ Деактивация объявления',
        'kg': '❌ Жарыяны өчүрүү',
        'en': '❌ Ad deactivation',
        'cn': '❌ 广告停用',
    },
    'ask_for_message_to_delete': {
        'ru': '❌ Деактивация объявления. Пожалуйста, отправьте пересланное сообщение С КАНАЛА с вашим объявлением.',
        'kg': '❌ Жарыяны өчүрүү. Сураныч, КАНАЛДАН жарыяңыз менен кайра жөнөтүлгөн билдирүүнү жибериңиз.',
        'en': '❌ Ad deactivation. Please send a forwarded message FROM THE CHANNEL with your ad.',
        'cn': '❌ 广告停用。请发送一个来自频道的转发消息，内容是您的广告。',
    },
    'delete_ad_not_your_ad': {
        'ru': '❌ Это не ваше объявление. Пожалуйста, отправьте пересланное сообщение С КАНАЛА с вашим объявлением.',
        'kg': '❌ Бул сиздин жарыяңыз эмес. Сураныч, КАНАЛДАН жарыяңыз менен кайра жөнөтүлгөн билдирүүнү жибериңиз.',
        'en': '❌ This is not your ad. Please send a forwarded message FROM THE CHANNEL with your ad.',
        'cn': '❌ 这不是您的广告。请发送一个来自频道的转发消息，内容是您的广告。',
    },
    'delete_confirmation': {
        'ru': '❓ Вы точно хотите деактивировать это объявление?',
        'kg': '❓ Бул жарыяны өчүрүүгө чын эмели?',
        'en': '❓ Are you sure you want to deactivate this ad?',
        'cn': '❓ 您确定要停用这个广告吗？',
    },
    'delete_yes': {
        'ru': '✅ Да',
        'kg': '✅ Ооба',
        'en': '✅ Yes',
        'cn': '✅ 是的',
    },
    'delete_no': {
        'ru': '❌ Нет',
        'kg': '❌ Жок',
        'en': '❌ No',
        'cn': '❌ 不',
    },
    'delete_success': {
        'ru': '✅ Объявление деактивировано.',
        'kg': '✅ Жарыя өчүрүлдү.',
        'en': '✅ Ad deactivated.',
        'cn': '✅ 广告已停用。',
    },
    'delete_ad_cancelled': {
        'ru': '❌ Деактивация объявления отменена.',
        'kg': '❌ Жарыяны өчүрүү жокко чыгарылды.',
        'en': '❌ Ad deactivation cancelled.',
        'cn': '❌ 广告停用已取消。',
    },
    'delete_already_sold': {
        'ru': '❌ Невозможно деактивировать объявление, так как товар уже продан.',
        'kg': '❌ Товар сатылгандыктан жарыяны өчүрүү мүмкүн эмес.',
        'en': '❌ Cannot deactivate ad because the item is already sold.',
        'cn': '❌ 无法停用广告，因为商品已经售出。',
    },
    "ask_for_message_to_edit": {
        "ru": "📝 Перешлите сообщение с вашим объявлением из канала, которое хотите отредактировать.",
        "kg": "📝 Каналдагы өз жарыяңызды өзгөртүү үчүн аны ботко кайра жөнөтүңүз.",
        "en": "📝 Forward your ad message from the channel to edit it.",
        "cn": "📝 转发您在频道中的广告消息以进行编辑。",
    },
    "edit_ad_not_your_ad": {
        "ru": "❌ Это объявление принадлежит другому пользователю. Вы можете редактировать только свои объявления.",
        "kg": "❌ Бул жарыя башка колдонуучуга таандык. Өзүңүздүн жарыяңызды гана түзөтө аласыз.",
        "en": "❌ This ad belongs to another user. You can only edit your own ads.",
        "cn": "❌ 此广告属于其他用户。您只能编辑自己的广告。",
    },
    "choose_field_to_edit": {
        "ru": "Что вы хотите изменить?",
        "kg": "Эмнени өзгөрткүңүз келет?",
        "en": "What do you want to change?",
        "cn": "您想更改什么？",
    },
    "edit_status_prompt": {
        "ru": "Выберите новый статус:",
        "kg": "Жаңы статустун түрүн тандаңыз:",
        "en": "Select a new status:",
        "cn": "选择新状态：",
    },
    "edit_subcategory_prompt": {
        "ru": "Выберите новую подкатегорию:",
        "kg": "Жаңы подкатегорияны тандаңыз:",
        "en": "Select a new subcategory:",
        "cn": "选择新的子类别：",
    },
    "edit_name_prompt": {
        "ru": "Введите новое название объявления:",
        "kg": "Жарыянын жаңы аталышын киргизиңиз:",
        "en": "Enter the new ad title:",
        "cn": "输入新广告标题：",
    },
    "edit_desc_prompt": {
        "ru": "Введите новое описание:",
        "kg": "Жаңы сыпаттаманы киргизиңиз:",
        "en": "Enter a new description:",
        "cn": "输入新描述：",
    },
    "edit_price_prompt": {
        "ru": "Введите новую цену (только цифры):",
        "kg": "Жаңы бааны киргизиңиз (сан менен гана):",
        "en": "Enter a new price (numbers only):",
        "cn": "输入新价格（仅数字）：",
    },
    "edit_phone_prompt": {
        "ru": "Показывать номер телефона в объявлении?",
        "kg": "Жарыяда телефон номери көрүнсүнбү?",
        "en": "Show phone number in the ad?",
        "cn": "在广告中显示电话号码？",
    },
    "field_updated": {
        "ru": "✅ Поле «{field}» обновлено на:\n{value}",
        "kg": "✅ «{field}» талаасы жаңыртылды:\n{value}",
        "en": "✅ Field '{field}' updated to:\n{value}",
        "cn": "✅ 字段“{field}”已更新为：\n{value}",
    },
    "invalid_name": {
        "ru": "Название не может быть пустым.",
        "kg": "Аталыш бош болушу мүмкүн эмес.",
        "en": "Title cannot be empty.",
        "cn": "标题不能为空。",
    },
    "edit_success": {
        "ru": "✅ Объявление успешно обновлено!",
        "kg": "✅ Жарыя ийгиликтүү жаңыртылды!",
        "en": "✅ Ad successfully updated!",
        "cn": "✅ 广告更新成功！",
    },
    "edit_error": {
        "ru": "❌ Ошибка при обновлении: {error}",
        "kg": "❌ Жаңыртууда ката кетти: {error}",
        "en": "❌ Error updating: {error}",
        "cn": "❌ 更新错误：{error}",
    },
    "edit_cancelled": {
        "ru": "Редактирование отменено.",
        "kg": "Түзөтүү жокко чыгарылды.",
        "en": "Editing cancelled.",
        "cn": "编辑已取消。",
    },
    "phone_visibility": {
        "ru": "📞 Видимость телефона",
        "kg": "📞 Телефон көрүнүшү",
        "en": "📞 Phone visibility",
        "cn": "📞 电话可见性",
    },
    'title': {
        'ru': '📝 Название',
        'kg': '📝 Аталыш',
        'en': '📝 Title',
        'cn': '📝 标题',
    },
    'description': {
        'ru': '🖊️ Описание',
        'kg': '🖊️ Сыпаттама',
        'en': '🖊️ Description',
        'cn': '🖊️ 描述',
    },
    "status": {
        "ru": "📌 Статус",
        "kg": "📌 Статус",
        "en": "📌 Status",
        "cn": "📌 状态",
    },
    "subcategory": {
        "ru": "📂 Подкатегория",
        "kg": "📂 Подкатегория",
        "en": "📂 Subcategory",
        "cn": "📂 子类别",
    },
    "phone": {
        "ru": "📞 Телефон",
        "kg": "📞 Телефон",
        "en": "📞 Phone",
        "cn": "📞 电话",
    },
    'edit_price': {
        'ru': '💰 Цена',
        'kg': '💰 Баасы',
        'en': '💰 Price',
        'cn': '💰 价格',
    },
    'edit_ad_button_inline': {
        'ru': '✏️ Редактировать объявление',
        'kg': '✏️ Жарыяны түзөтүү',
        'en': '✏️ Edit Ad',
        'cn': '✏️ 编辑广告',
    }
}


@lru_cache(maxsize=1024)
def t(key: str, lang: str = 'ru') -> str:
    """
    Возвращает перевод строки по ключу и языку.
    Если ключа нет или нет перевода для языка, возвращает русский вариант.
    """
    translations = TRANSLATIONS.get(key)
    if not translations:
        return key
    return translations.get(lang) or translations.get('ru', key)