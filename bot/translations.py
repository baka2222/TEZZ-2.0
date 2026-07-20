# translations.py
# Полный словарь переводов для TEZZ Market bot
# Ключи сгруппированы по функциональным модулям
from functools import lru_cache


TRANSLATIONS = {
    'up_ad_button': {
        'ru': '⬆️ Поднять объявление',
        'kg': '⬆️ Жарыяны көтөрүү',
        'en': '⬆️ Promote ad',
        'cn': '⬆️ 提升广告',
    },
    'up_ad_low_balance': {
        'ru': '❌ Недостаточно средств для поднятия объявления. Требуется {price} сом. Ваш баланс {balance} сом.',
        'kg': '❌ Жарыяны көтөрүү үчүн жетишсиз каражат. {price} сом талап кылынат. Сиздин балансыңыз {balance} сом.',
        'en': '❌ Insufficient funds to promote the ad. {price} KGS required. Your balance is {balance} KGS.',
        'cn': '❌ 提升广告所需资金不足。需要 {price} 索姆。您的余额是 {balance} 索姆。',
    },
    'up_ad_confirm': {
        'ru': '❌ Вы уверены, что хотите поднять объявление? Это будет стоить {price} сом. Ваш баланс {balance} сом.',
        'kg': '❌ Жарыяны көтөрүүнү чын эле жасамагыңыз керек пиши? Бу {price} сомга айланат. Сиздин балансыңыз {balance} сом.',
        'en': '❌ Are you sure you want to promote the ad? This will cost {price} KGS. Your balance is {balance} KGS.',
        'cn': '❌ 你确定要推广广告吗？这将花费 {price} 索姆。你的余额是 {balance} 索姆。',
    },
    'up_ad_success': {
        'ru': '✅ Объявление успешно поднято!',
        'kg': '✅ Жарыя ийгиликтүү көтөрүлдү!',
        'en': '✅ The ad has been successfully promoted!',
        'cn': '✅ 广告已成功推广！',
    },
    'up_ad_confirm_free': {
        'ru': '⬆️ Поднять объявление наверх канала? Кулдаун не активен, это бесплатно.',
        'kg': '⬆️ Жарыяны каналдын башына көтөрөбүзбү? Кулдаун активдүү эмес, бул акысыз.',
        'en': '⬆️ Move the ad to the top of the channel? Cooldown is not active, this is free.',
        'cn': '⬆️ 将广告移到频道顶部？冷却时间未激活，此操作免费。',
    },

    # ---------- Общие / Регистрация / Навигация (commands) ----------
    'remembered_client': {
        'ru': '👋🏻 О, я тебя помню. То, что ты вернулся - правильное решение. Вместе веселее!\n\nСтарое дорбое меню можешь открыть тут 👇🏻',
        'kg': '👋🏻 О, мен сени эстейм. Кайтып келгендигиң туура чечим. Бирге көңүлдүү!\n\nЭски жакшы менюну бул жерден ачсаң болот 👇🏻',
        'en': '👋🏻 Oh, I remember you. Coming back is the right decision. It’s more fun together!\n\nYou can open the old good menu here 👇🏻',
        'cn': '👋🏻 哦，我记得你。回来是正确的决定。一起更有趣！\n\n你可以在这里打开旧的好菜单 👇🏻',
    },
    'profile_inline_button': {
        'ru': '👤 Настройки профиля',
        'kg': '👤 Профильдик параметрлери',
        'en': '👤 Profile Settings',
        'cn': '👤 个人资料设置',
    },
    'choose_language': {
        'ru': '🌐 Выберите язык',
        'kg': '🌐 Тилди тандаңыз',
        'en': '🌐 Choose language',
        'cn': '🌐 选择语言',
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
        'ru': '🛒 А вот и наши маркеты:',
        'kg': '🛒 Бул биздин маркеттер:',
        'en': '🛒 Here are our markets:',
        'cn': '🛒 这是我们的市场：',
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
        'ru': '◀️ Назад',
        'kg': '◀️ Артка',
        'en': '◀️ Back',
        'cn': '◀️ 返回',
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
        'ru': '💵 <b>Укажите цену:</b>\n\n<i>Введите только число, например: 2500</i>\n<i>Или нажмите «💬 Договорная», если цена обсуждается.</i>',
        'kg': '💵 <b>Бааны көрсөтүңүз:</b>\n\n<i>Сан гана жазыңыз, мисалы: 2500</i>\n<i>Же баа келишим боюнча болсо «💬 Келишим баада» баскычын басыңыз.</i>',
        'en': '💵 <b>Enter the price:</b>\n\n<i>Enter only a number, e.g.: 2500</i>\n<i>Or tap «💬 Negotiable» if the price is negotiable.</i>',
        'cn': '💵 <b>请输入价格：</b>\n\n<i>只输入数字，例如：2500</i>\n<i>如价格面议，请点击「💬 面议」。</i>',
    },
    'price_negotiable': {
        'ru': 'Договорная',
        'kg': 'Келишим баада',
        'en': 'Negotiable',
        'cn': '面议',
    },
    'btn_negotiable': {
        'ru': '💬 Договорная',
        'kg': '💬 Келишим баада',
        'en': '💬 Negotiable',
        'cn': '💬 面议',
    },
    'price_must_be_number': {
        'ru': '❗️ Цена должна быть числом. Введите только число, например: 3500',
        'kg': '❗️ Баа сан болушу керек. Сан гана жазыңыз, мисалы: 3500',
        'en': '❗️ Price must be a number. Enter only a number, e.g.: 3500',
        'cn': '❗️ 价格必须为数字。只输入数字，例如：3500',
    },
    'price_too_large': {
        'ru': '❗️ Слишком большая цена. Максимум {max}.',
        'kg': '❗️ Баа өтө чоң. Эң көбү {max}.',
        'en': '❗️ Price is too large. Maximum {max}.',
        'cn': '❗️ 价格过大。最多 {max}。',
    },
    'name_too_long': {
        'ru': '❗️ Слишком длинный заголовок. Максимум {max} символов.',
        'kg': '❗️ Аталышы өтө узун. Эң көбү {max} белги.',
        'en': '❗️ Title is too long. Maximum {max} characters.',
        'cn': '❗️ 标题过长。最多 {max} 个字符。',
    },
    'desc_too_long': {
        'ru': '❗️ Слишком длинное описание. Максимум {max} символов.',
        'kg': '❗️ Сүрөттөмө өтө узун. Эң көбү {max} белги.',
        'en': '❗️ Description is too long. Maximum {max} characters.',
        'cn': '❗️ 描述过长。最多 {max} 个字符。',
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
        'ru': 'Написать продавцу',
        'kg': 'Сатууга байланышуу',
        'en': 'Contact seller',
        'cn': '联系卖家',
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
        'ru': '✅ <b>Объявление опубликовано!</b>\nВсе ваши обьявления можете найти в профиле.',
        'kg': '✅ <b>Жарыя жарыяланды!</b>\nБаардык жарнамаларыңызды профилиңизден таба аласыз.',
        'en': '✅ <b>Ad published!</b>\nAll your ads can be found in your profile.',
        'cn': '✅ <b>广告已发布！</b>\n您可以在个人资料中找到所有广告。',
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
    'publish_in_progress': {
        'ru': '⏳ Публикация уже началась, подождите.',
        'kg': '⏳ Жарыялоо башталды, күтө туруңуз.',
        'en': '⏳ Publishing already started, please wait.',
        'cn': '⏳ 发布已开始，请稍候。',
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
        'ru': 'Цена',
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
        'ru': 'Описание',
        'kg': 'Сыпаттама',
        'en': 'Description',
        'cn': '描述',
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
        "ru": "Телефон",
        "kg": "Телефон",
        "en": "Phone",
        "cn": "电话",
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
    },

    # ---------- Профиль (profile) ----------
    'profile_title': {
        'ru': '👤 <b>Мой профиль</b>',
        'kg': '👤 <b>Менин профилим</b>',
        'en': '👤 <b>My profile</b>',
        'cn': '👤 <b>我的资料</b>',
    },
    'profile_name': {
        'ru': '🪪 Имя',
        'kg': '🪪 Аты',
        'en': '🪪 Name',
        'cn': '🪪 姓名',
    },
    'profile_phone': {
        'ru': '📱 Телефон',
        'kg': '📱 Телефон',
        'en': '📱 Phone',
        'cn': '📱 电话',
    },
    'profile_balance': {
        'ru': '💰 Баланс',
        'kg': '💰 Баланс',
        'en': '💰 Balance',
        'cn': '💰 余额',
    },
    'profile_ads_count': {
        'ru': '📢 Активных объявлений',
        'kg': '📢 Активдүү жарыялар',
        'en': '📢 Active ads',
        'cn': '📢 有效广告',
    },
    'profile_sub_until': {
        'ru': '💎 Подписка до: <b>{date}</b>',
        'kg': '💎 Жазылуу бүткөнгө чейин: <b>{date}</b>',
        'en': '💎 Subscription until: <b>{date}</b>',
        'cn': '💎 订阅至：<b>{date}</b>',
    },
    'profile_sub_none': {
        'ru': '💎 Подписка: нет',
        'kg': '💎 Жазылуу: жок',
        'en': '💎 Subscription: none',
        'cn': '💎 订阅：无',
    },
    'btn_my_ads': {
        'ru': '📢 Мои объявления',
        'kg': '📢 Менин жарыяларым',
        'en': '📢 My ads',
        'cn': '📢 我的广告',
    },
    'btn_favorites': {
        'ru': '⭐ Избранные',
        'kg': '⭐ Тандалмалар',
        'en': '⭐ Favorites',
        'cn': '⭐ 收藏',
    },
    'btn_transactions': {
        'ru': '💳 Транзакции',
        'kg': '💳 Транзакциялар',
        'en': '💳 Transactions',
        'cn': '💳 交易记录',
    },
    'btn_edit_name': {
        'ru': '✏️ Изменить имя',
        'kg': '✏️ Атын өзгөртүү',
        'en': '✏️ Change name',
        'cn': '✏️ 修改姓名',
    },
    'btn_edit_phone': {
        'ru': '📱 Изменить номер',
        'kg': '📱 Номерди өзгөртүү',
        'en': '📱 Change phone',
        'cn': '📱 修改电话',
    },
    'my_ads_title': {
        'ru': '📢 <b>Мои объявления</b>\n\nВыберите объявление:',
        'kg': '📢 <b>Менин жарыяларым</b>\n\nЖарыяны тандаңыз:',
        'en': '📢 <b>My ads</b>\n\nChoose an ad:',
        'cn': '📢 <b>我的广告</b>\n\n请选择广告：',
    },
    'no_ads': {
        'ru': '🤷 У вас пока нет объявлений.',
        'kg': '🤷 Сизде азырынча жарыялар жок.',
        'en': '🤷 You have no ads yet.',
        'cn': '🤷 您还没有广告。',
    },
    'ad_status_active': {
        'ru': '🟢 Активно',
        'kg': '🟢 Активдүү',
        'en': '🟢 Active',
        'cn': '🟢 有效',
    },
    'ad_status_inactive': {
        'ru': '🔴 Неактивно',
        'kg': '🔴 Активдүү эмес',
        'en': '🔴 Inactive',
        'cn': '🔴 无效',
    },
    'ad_card': {
        'ru': '🏷️ <b>{name}</b>\n\n🗂 Категория: {category}\n📂 Подкатегория: {subcategory}\n💵 Цена: <b>{price}</b>\n📊 Статус: {status}\n📅 Создано: {date}',
        'kg': '🏷️ <b>{name}</b>\n\n🗂 Категория: {category}\n📂 Подкатегория: {subcategory}\n💵 Баасы: <b>{price}</b>\n📊 Абалы: {status}\n📅 Түзүлгөн: {date}',
        'en': '🏷️ <b>{name}</b>\n\n🗂 Category: {category}\n📂 Subcategory: {subcategory}\n💵 Price: <b>{price}</b>\n📊 Status: {status}\n📅 Created: {date}',
        'cn': '🏷️ <b>{name}</b>\n\n🗂 分类：{category}\n📂 子分类：{subcategory}\n💵 价格：<b>{price}</b>\n📊 状态：{status}\n📅 创建：{date}',
    },
    'btn_edit_ad_name': {
        'ru': '✏️ Название',
        'kg': '✏️ Аталышы',
        'en': '✏️ Title',
        'cn': '✏️ 标题',
    },
    'btn_edit_ad_price': {
        'ru': '💰 Цена',
        'kg': '💰 Баасы',
        'en': '💰 Price',
        'cn': '💰 价格',
    },
    'btn_deactivate': {
        'ru': '🚫 Деактивировать',
        'kg': '🚫 Өчүрүү',
        'en': '🚫 Deactivate',
        'cn': '🚫 停用',
    },
    'deactivate_confirm': {
        'ru': '🚫 Деактивировать объявление?\nВ канале оно будет помечено как <b>ПРОДАНО</b>.',
        'kg': '🚫 Жарыяны өчүрөсүзбү?\nКаналда ал <b>САТЫЛДЫ</b> деп белгиленет.',
        'en': '🚫 Deactivate the ad?\nIt will be marked as <b>SOLD</b> in the channel.',
        'cn': '🚫 停用广告？\n它将在频道中被标记为<b>已售出</b>。',
    },
    'ad_deactivated': {
        'ru': '✅ Объявление деактивировано.',
        'kg': '✅ Жарыя өчүрүлдү.',
        'en': '✅ Ad deactivated.',
        'cn': '✅ 广告已停用。',
    },
    'channel_update_failed': {
        'ru': '⚠️ Не удалось обновить пост в канале, но данные сохранены.',
        'kg': '⚠️ Каналдагы постту жаңыртуу мүмкүн болгон жок, бирок маалымат сакталды.',
        'en': '⚠️ Failed to update the channel post, but the data was saved.',
        'cn': '⚠️ 无法更新频道帖子，但数据已保存。',
    },
    'enter_new_ad_name': {
        'ru': '✏️ Введите новое название объявления:',
        'kg': '✏️ Жарыянын жаңы аталышын жазыңыз:',
        'en': '✏️ Enter the new ad title:',
        'cn': '✏️ 请输入新的广告标题：',
    },
    'enter_new_ad_price': {
        'ru': '💰 Введите новую цену (только число) или нажмите «💬 Договорная»:',
        'kg': '💰 Жаңы бааны жазыңыз (сан гана) же «💬 Келишим баада» баскычын басыңыз:',
        'en': '💰 Enter the new price (number only) or tap «💬 Negotiable»:',
        'cn': '💰 请输入新价格（仅数字）或点击「💬 面议」：',
    },
    'ad_updated': {
        'ru': '✅ Объявление обновлено!',
        'kg': '✅ Жарыя жаңыртылды!',
        'en': '✅ Ad updated!',
        'cn': '✅ 广告已更新！',
    },
    'ad_not_found': {
        'ru': '❌ Объявление не найдено.',
        'kg': '❌ Жарыя табылган жок.',
        'en': '❌ Ad not found.',
        'cn': '❌ 未找到广告。',
    },
    'favorites_title': {
        'ru': '⭐ <b>Избранные объявления</b>',
        'kg': '⭐ <b>Тандалма жарыялар</b>',
        'en': '⭐ <b>Favorite ads</b>',
        'cn': '⭐ <b>收藏的广告</b>',
    },
    'no_favorites': {
        'ru': '🤷 В избранном пока пусто.\nПерешлите пост объявления из нашего канала, чтобы добавить его.',
        'kg': '🤷 Тандалмалар азырынча бош.\nКошуу үчүн каналдан жарыянын постун жөнөтүңүз.',
        'en': '🤷 Favorites are empty.\nForward an ad post from our channel to add it.',
        'cn': '🤷 收藏夹是空的。\n从我们的频道转发广告帖子即可添加。',
    },
    'btn_add_favorite': {
        'ru': '➕ Добавить',
        'kg': '➕ Кошуу',
        'en': '➕ Add',
        'cn': '➕ 添加',
    },
    'btn_remove_favorite': {
        'ru': '💔 Убрать из избранного',
        'kg': '💔 Тандалмалардан алып салуу',
        'en': '💔 Remove from favorites',
        'cn': '💔 从收藏中移除',
    },
    'forward_ad_for_favorite': {
        'ru': '📩 Перешлите пост объявления из нашего канала, и я добавлю его в избранное.',
        'kg': '📩 Каналдан жарыянын постун жөнөтүңүз, мен аны тандалмаларга кошом.',
        'en': '📩 Forward an ad post from our channel and I will add it to favorites.',
        'cn': '📩 从我们的频道转发广告帖子，我会将其添加到收藏夹。',
    },
    'favorite_added': {
        'ru': '⭐ Добавлено в избранное!',
        'kg': '⭐ Тандалмаларга кошулду!',
        'en': '⭐ Added to favorites!',
        'cn': '⭐ 已添加到收藏！',
    },
    'favorite_removed': {
        'ru': '💔 Убрано из избранного.',
        'kg': '💔 Тандалмалардан алынып салынды.',
        'en': '💔 Removed from favorites.',
        'cn': '💔 已从收藏中移除。',
    },
    'already_favorite': {
        'ru': '⭐ Это объявление уже в избранном.',
        'kg': '⭐ Бул жарыя мурунтан эле тандалмаларда.',
        'en': '⭐ This ad is already in favorites.',
        'cn': '⭐ 该广告已在收藏中。',
    },
    'favorite_not_found': {
        'ru': '❌ Это объявление не найдено в базе. Возможно, оно опубликовано до запуска избранного.',
        'kg': '❌ Бул жарыя базадан табылган жок. Балким, ал тандалмалар иштегенге чейин жарыяланган.',
        'en': '❌ This ad was not found in the database. It may have been published before favorites were launched.',
        'cn': '❌ 数据库中未找到该广告。它可能是在收藏功能上线之前发布的。',
    },
    'transactions_title': {
        'ru': '💳 <b>Последние транзакции</b>',
        'kg': '💳 <b>Акыркы транзакциялар</b>',
        'en': '💳 <b>Recent transactions</b>',
        'cn': '💳 <b>最近交易</b>',
    },
    'no_transactions': {
        'ru': '🤷 Транзакций пока нет.',
        'kg': '🤷 Азырынча транзакциялар жок.',
        'en': '🤷 No transactions yet.',
        'cn': '🤷 暂无交易。',
    },
    'tx_to': {
        'ru': 'кому',
        'kg': 'кимге',
        'en': 'to',
        'cn': '给',
    },
    'tx_from': {
        'ru': 'от',
        'kg': 'кимден',
        'en': 'from',
        'cn': '来自',
    },
    'enter_new_name': {
        'ru': '✏️ Введите новое имя:',
        'kg': '✏️ Жаңы атыңызды жазыңыз:',
        'en': '✏️ Enter your new name:',
        'cn': '✏️ 请输入新姓名：',
    },
    'name_updated': {
        'ru': '✅ Имя обновлено!',
        'kg': '✅ Аты жаңыртылды!',
        'en': '✅ Name updated!',
        'cn': '✅ 姓名已更新！',
    },
    'phone_updated': {
        'ru': '✅ Номер телефона обновлён!',
        'kg': '✅ Телефон номери жаңыртылды!',
        'en': '✅ Phone number updated!',
        'cn': '✅ 电话号码已更新！',
    },
    'phone_not_yours': {
        'ru': '⚠️ Пожалуйста, отправьте <b>свой</b> контакт кнопкой ниже. Пересланные и чужие контакты не принимаются.',
        'kg': '⚠️ Сураныч, төмөнкү баскыч менен <b>өз</b> контактыңызды жөнөтүңүз. Башка бирөөнүн контактысы кабыл алынбайт.',
        'en': '⚠️ Please send <b>your own</b> contact using the button below. Forwarded or other people\'s contacts are not accepted.',
        'cn': '⚠️ 请使用下方按钮发送<b>您本人</b>的联系方式。不接受转发或他人的联系方式。',
    },
    'phone_need_contact': {
        'ru': '📱 Нужен именно номер телефона. Отправьте его кнопкой «Отправить номер» или вернитесь в меню.',
        'kg': '📱 Дал телефон номери керек. Аны «Телефонду жөнөтүү» баскычы менен жөнөтүңүз же менюга кайтыңыз.',
        'en': '📱 A phone number is required. Send it with the “Send phone” button or return to the menu.',
        'cn': '📱 需要电话号码。请用“发送号码”按钮发送，或返回菜单。',
    },
    'btn_confirm_yes': {
        'ru': '✅ Да',
        'kg': '✅ Ооба',
        'en': '✅ Yes',
        'cn': '✅ 是',
    },
    'btn_confirm_no': {
        'ru': '❌ Нет',
        'kg': '❌ Жок',
        'en': '❌ No',
        'cn': '❌ 否',
    },

    # ---------- Профиль: таблицы, редактирование, закрепление, подписка ----------
    'tbl_name': {
        'ru': 'Товар',
        'kg': 'Товар',
        'en': 'Item',
        'cn': '商品',
    },
    'tbl_price': {
        'ru': 'Цена',
        'kg': 'Баасы',
        'en': 'Price',
        'cn': '价格',
    },
    'tbl_state': {
        'ru': 'Ст.',
        'kg': 'Абал',
        'en': 'St.',
        'cn': '状态',
    },
    'page_of': {
        'ru': 'Стр. {current}/{total}',
        'kg': 'Бет {current}/{total}',
        'en': 'Page {current}/{total}',
        'cn': '第 {current}/{total} 页',
    },
    'btn_edit_ad_status': {
        'ru': '📊 Тип объявления',
        'kg': '📊 Жарыянын түрү',
        'en': '📊 Ad type',
        'cn': '📊 广告类型',
    },
    'btn_edit_ad_subcat': {
        'ru': '📂 Подкатегория',
        'kg': '📂 Подкатегория',
        'en': '📂 Subcategory',
        'cn': '📂 子类别',
    },
    'btn_edit_ad_desc': {
        'ru': '📝 Описание',
        'kg': '📝 Сүрөттөмө',
        'en': '📝 Description',
        'cn': '📝 描述',
    },
    'btn_edit_ad_phone': {
        'ru': '📱 Показ телефона',
        'kg': '📱 Телефонду көрсөтүү',
        'en': '📱 Phone visibility',
        'cn': '📱 电话显示',
    },
    'btn_pin_ad': {
        'ru': '📌 Закрепить',
        'kg': '📌 Бекитүү',
        'en': '📌 Pin',
        'cn': '📌 置顶',
    },
    'enter_new_ad_desc': {
        'ru': '📝 Введите новое описание объявления:',
        'kg': '📝 Жарыянын жаңы сүрөттөмөсүн жазыңыз:',
        'en': '📝 Enter the new ad description:',
        'cn': '📝 请输入新的广告描述：',
    },
    'choose_ad_status': {
        'ru': '📊 Выберите тип объявления:',
        'kg': '📊 Жарыянын түрүн тандаңыз:',
        'en': '📊 Choose the ad type:',
        'cn': '📊 请选择广告类型：',
    },
    'choose_ad_subcat': {
        'ru': '📂 Выберите подкатегорию:',
        'kg': '📂 Подкатегорияны тандаңыз:',
        'en': '📂 Choose a subcategory:',
        'cn': '📂 请选择子类别：',
    },
    'choose_phone_visibility': {
        'ru': '📱 Показывать номер телефона в объявлении?',
        'kg': '📱 Жарыяда телефон номерин көрсөтөсүзбү?',
        'en': '📱 Show the phone number in the ad?',
        'cn': '📱 在广告中显示电话号码吗？',
    },
    'pin_offer': {
        'ru': '📌 Закрепить объявление на {days} дн. за <b>{price}</b>?\n💰 Ваш баланс: <b>{balance}</b>',
        'kg': '📌 Жарыяны {days} күнгө <b>{price}</b> үчүн бекитесизби?\n💰 Балансыңыз: <b>{balance}</b>',
        'en': '📌 Pin the ad for {days} days for <b>{price}</b>?\n💰 Your balance: <b>{balance}</b>',
        'cn': '📌 以 <b>{price}</b> 置顶广告 {days} 天？\n💰 您的余额：<b>{balance}</b>',
    },
    'pin_paid': {
        'ru': '✅ Объявление закреплено на {days} дн.!',
        'kg': '✅ Жарыя {days} күнгө бекитилди!',
        'en': '✅ Ad pinned for {days} days!',
        'cn': '✅ 广告已置顶 {days} 天！',
    },
    'pin_low_balance': {
        'ru': '❌ Недостаточно средств. Нужно {price}, у вас {balance}. Пополните баланс.',
        'kg': '❌ Каражат жетишсиз. {price} керек, сизде {balance}. Балансты толуктаңыз.',
        'en': '❌ Insufficient funds. Need {price}, you have {balance}. Please top up.',
        'cn': '❌ 余额不足。需要 {price}，您有 {balance}。请充值。',
    },
    'pin_failed': {
        'ru': '❌ Не удалось закрепить (нет прав или ошибка). Средства возвращены.',
        'kg': '❌ Бекитүү мүмкүн болбоду (укук жок же ката). Каражат кайтарылды.',
        'en': '❌ Failed to pin (no rights or error). Funds refunded.',
        'cn': '❌ 置顶失败（无权限或出错）。已退款。',
    },
    'sub_offer': {
        'ru': '💎 <b>Подписка</b> на {days} дн. — <b>{price}</b>\n💰 Ваш баланс: <b>{balance}</b>\n\nЕсли у вас уже есть подписка, то оплата пойдет на ее продление.\n\nБезлимитные публикации во всех маркетах без кулдауна.',
        'kg': '💎 <b>Жазылуу</b> {days} күнгө — <b>{price}</b>\n💰 Балансыңыз: <b>{balance}</b>\n\nЭгер сизде узактык жазылуу бар болсо, төлөм салынып кетет.\n\nБардык маркеттерде кулдаунсуз чексиз жарыялоо.',
        'en': '💎 <b>Subscription</b> for {days} days — <b>{price}</b>\n💰 Your balance: <b>{balance}</b>\n\nIf you already have a subscription, the payment will go towards its renewal.\n\nUnlimited posting in all markets without cooldown.',
        'cn': '💎 <b>订阅</b> {days} 天 — <b>{price}</b>\n💰 您的余额：<b>{balance}</b>\n\n如果您的订阅已存在，支付将用于续订。\n\n在所有市场无限发布，无冷却时间。',
    },
    'btn_sub_from_balance': {
        'ru': '💰 Оплатить с баланса',
        'kg': '💰 Баланстан төлөө',
        'en': '💰 Pay from balance',
        'cn': '💰 用余额支付',
    },
    'btn_sub_by_check': {
        'ru': '🧾 Оплатить чеком',
        'kg': '🧾 Чек менен төлөө',
        'en': '🧾 Pay by receipt',
        'cn': '🧾 凭收据支付',
    },
    'sub_paid': {
        'ru': '✅ Подписка активирована на {days} дн.!',
        'kg': '✅ Жазылуу {days} күнгө активдештирилди!',
        'en': '✅ Subscription activated for {days} days!',
        'cn': '✅ 订阅已激活 {days} 天！',
    },
    'sub_low_balance': {
        'ru': '❌ Недостаточно средств. Нужно {price}, у вас {balance}. Пополните баланс.',
        'kg': '❌ Каражат жетишсиз. {price} керек, сизде {balance}. Балансты толуктаңыз.',
        'en': '❌ Insufficient funds. Need {price}, you have {balance}. Please top up.',
        'cn': '❌ 余额不足。需要 {price}，您有 {balance}。请充值。',
    },

    # ---------- Валюта ----------
    'currency': {
        'ru': 'тезиков',
        'kg': 'тезик',
        'en': 'teziks',
        'cn': '泰兹币',
    },

    # ---------- Перевод тезиков ----------
    'btn_transfer': {
        'ru': '💸 Перевести тезики',
        'kg': '💸 Тезик которуу',
        'en': '💸 Send teziks',
        'cn': '💸 转账泰兹币',
    },
    'btn_replenish': {
        'ru': '➕ Пополнить баланс',
        'kg': '➕ Балансты толуктоо',
        'en': '➕ Top up balance',
        'cn': '➕ 充值余额',
    },
    'btn_choose_user': {
        'ru': '👤 Выбрать пользователя',
        'kg': '👤 Колдонуучуну тандоо',
        'en': '👤 Choose user',
        'cn': '👤 选择用户',
    },
    'transfer_choose_user': {
        'ru': '💸 Кому перевести тезики? Нажмите кнопку ниже и выберите пользователя.',
        'kg': '💸 Тезиктерди кимге которосуз? Төмөнкү баскычты басып, колдонуучуну тандаңыз.',
        'en': '💸 Who to send teziks to? Tap the button below and choose a user.',
        'cn': '💸 向谁转账泰兹币？点击下方按钮选择用户。',
    },
    'transfer_pick_user_hint': {
        'ru': '👇 Пожалуйста, выберите пользователя кнопкой «Выбрать пользователя».',
        'kg': '👇 Сураныч, «Колдонуучуну тандоо» баскычы менен тандаңыз.',
        'en': '👇 Please choose a user with the “Choose user” button.',
        'cn': '👇 请用“选择用户”按钮选择用户。',
    },
    'transfer_user_not_found': {
        'ru': '❌ Этот пользователь не зарегистрирован в системе — перевод невозможен.',
        'kg': '❌ Бул колдонуучу системада катталган эмес — которуу мүмкүн эмес.',
        'en': '❌ This user is not registered in the system — transfer is not possible.',
        'cn': '❌ 该用户未在系统注册 — 无法转账。',
    },
    'transfer_self': {
        'ru': '❌ Нельзя перевести тезики самому себе.',
        'kg': '❌ Тезиктерди өзүңүзгө которо албайсыз.',
        'en': '❌ You cannot send teziks to yourself.',
        'cn': '❌ 不能给自己转账泰兹币。',
    },
    'transfer_enter_amount': {
        'ru': '💸 Введите сумму перевода для <b>{name}</b>:',
        'kg': '💸 <b>{name}</b> үчүн которуу суммасын жазыңыз:',
        'en': '💸 Enter the amount to send to <b>{name}</b>:',
        'cn': '💸 请输入转给 <b>{name}</b> 的金额：',
    },
    'transfer_amount_invalid': {
        'ru': '❌ Введите корректную сумму (число больше 0).',
        'kg': '❌ Туура сумманы жазыңыз (0дөн чоң сан).',
        'en': '❌ Enter a valid amount (a number greater than 0).',
        'cn': '❌ 请输入有效金额（大于0的数字）。',
    },
    'transfer_insufficient': {
        'ru': '❌ Недостаточно тезиков. Ваш баланс: <b>{balance}</b>.',
        'kg': '❌ Тезик жетишсиз. Балансыңыз: <b>{balance}</b>.',
        'en': '❌ Not enough teziks. Your balance: <b>{balance}</b>.',
        'cn': '❌ 泰兹币不足。您的余额：<b>{balance}</b>。',
    },
    'transfer_done': {
        'ru': '✅ Вы перевели <b>{amount}</b> пользователю <b>{name}</b>.\n💰 Баланс: <b>{balance}</b>',
        'kg': '✅ Сиз <b>{name}</b> колдонуучуга <b>{amount}</b> которуп бердиңиз.\n💰 Баланс: <b>{balance}</b>',
        'en': '✅ You sent <b>{amount}</b> to <b>{name}</b>.\n💰 Balance: <b>{balance}</b>',
        'cn': '✅ 您已向 <b>{name}</b> 转账 <b>{amount}</b>。\n💰 余额：<b>{balance}</b>',
    },
    'transfer_received': {
        'ru': '💰 Вам перевели <b>{amount}</b> от <b>{name}</b>!\n💰 Ваш баланс: <b>{balance}</b>',
        'kg': '💰 Сизге <b>{name}</b> <b>{amount}</b> которду!\n💰 Балансыңыз: <b>{balance}</b>',
        'en': '💰 You received <b>{amount}</b> from <b>{name}</b>!\n💰 Your balance: <b>{balance}</b>',
        'cn': '💰 您收到来自 <b>{name}</b> 的 <b>{amount}</b>！\n💰 您的余额：<b>{balance}</b>',
    },

    # ---------- Пополнение баланса ----------
    'replenish_choose': {
        'ru': '💳 Выберите сумму пополнения:',
        'kg': '💳 Толуктоо суммасын тандаңыз:',
        'en': '💳 Choose a top-up amount:',
        'cn': '💳 请选择充值金额：',
    },
    'replenish_warning': {
        'ru': '⚠️ <b>Важно:</b> отправьте <b>ровно выбранную сумму</b>. Если сумма не совпадёт, тезики могут не начислиться автоматически — вопрос придётся решать с админом, а это требует времени.',
        'kg': '⚠️ <b>Маанилүү:</b> <b>так тандалган сумманы</b> жөнөтүңүз. Эгер сумма дал келбесе, тезиктер автоматтык түрдө кошулбай калышы мүмкүн — маселени админ менен чечүү керек болот, ал убакыт талап кылат.',
        'en': '⚠️ <b>Important:</b> send <b>exactly the chosen amount</b>. If it does not match, teziks may not be credited automatically — you will have to resolve it with the admin, which takes time.',
        'cn': '⚠️ <b>重要：</b>请发送<b>恰好所选的金额</b>。若金额不符，泰兹币可能不会自动到账 — 需与管理员解决，这需要时间。',
    },
    'replenish_instruction': {
        'ru': '💳 Пополнение на <b>{amount}</b>.\n\nОплатите на MBank и отправьте фото чека сюда.',
        'kg': '💳 <b>{amount}</b> толуктоо.\n\nMBank аркылуу төлөп, чектин сүрөтүн ушул жерге жөнөтүңүз.',
        'en': '💳 Top-up of <b>{amount}</b>.\n\nPay via MBank and send the receipt photo here.',
        'cn': '💳 充值 <b>{amount}</b>。\n\n请通过 MBank 付款并将收据照片发送到这里。',
    },
    'replenish_receipt_sent': {
        'ru': '✅ Чек отправлен на проверку. После подтверждения тезики будут зачислены.',
        'kg': '✅ Чек текшерүүгө жөнөтүлдү. Ырасталгандан кийин тезиктер кошулат.',
        'en': '✅ Receipt sent for review. Teziks will be credited after confirmation.',
        'cn': '✅ 收据已发送审核。确认后泰兹币将到账。',
    },
    'replenish_confirmed': {
        'ru': '✅ Ваш баланс пополнен на <b>{amount}</b>!',
        'kg': '✅ Балансыңыз <b>{amount}</b> толукталды!',
        'en': '✅ Your balance has been topped up by <b>{amount}</b>!',
        'cn': '✅ 您的余额已充值 <b>{amount}</b>！',
    },
    'replenish_declined': {
        'ru': '❌ Пополнение отклонено. Свяжитесь с поддержкой, если это ошибка.',
        'kg': '❌ Толуктоо четке кагылды. Ката болсо, колдоо кызматына кайрылыңыз.',
        'en': '❌ Top-up declined. Contact support if this is a mistake.',
        'cn': '❌ 充值被拒绝。如有误请联系客服。',
    },

    # ---------- Таблица транзакций ----------
    'tbl_amount': {
        'ru': 'Сумма',
        'kg': 'Сумма',
        'en': 'Amount',
        'cn': '金额',
    },
    'tbl_party': {
        'ru': 'Контрагент',
        'kg': 'Тарап',
        'en': 'Party',
        'cn': '对方',
    },

    # ---------- Флоу выставления объявления ----------
    'step_status': {'ru': 'Тип', 'kg': 'Түрү', 'en': 'Type', 'cn': '类型'},
    'step_subcategory': {'ru': 'Раздел', 'kg': 'Бөлүм', 'en': 'Section', 'cn': '分类'},
    'step_name': {'ru': 'Название', 'kg': 'Аталышы', 'en': 'Title', 'cn': '名称'},
    'step_desc': {'ru': 'Описание', 'kg': 'Сүрөттөмө', 'en': 'Desc', 'cn': '描述'},
    'step_price': {'ru': 'Цена', 'kg': 'Баасы', 'en': 'Price', 'cn': '价格'},
    'step_photos': {'ru': 'Фото', 'kg': 'Сүрөт', 'en': 'Photos', 'cn': '照片'},
    'step_phone': {'ru': 'Телефон', 'kg': 'Телефон', 'en': 'Phone', 'cn': '电话'},
    'flow_start_notice': {
        'ru': 'ℹ️ Во время создания объявления вернуться и изменить введённое нельзя. Но процесс можно приостановить кнопкой «Меню» — кулдаун при этом не спишется.',
        'kg': 'ℹ️ Жарыяны түзүү учурунда киргизилгенди артка кайтарып өзгөртүү мүмкүн эмес. Бирок процессти «Меню» баскычы менен токтотсоңуз болот — кулдаун эсептелбейт.',
        'en': 'ℹ️ While creating an ad you cannot go back and edit what you entered. But you can pause with the “Menu” button — the cooldown will not be applied.',
        'cn': 'ℹ️ 创建广告过程中无法返回修改已输入的内容。但可用“菜单”按钮暂停 — 冷却时间不会计算。',
    },
    'choose_subcategories': {
        'ru': '📂 Выберите подкатегории (от 1 до 3), затем нажмите «Готово»:',
        'kg': '📂 Подкатегорияларды тандаңыз (1-3), анан «Даяр» басыңыз:',
        'en': '📂 Choose subcategories (1 to 3), then tap “Done”:',
        'cn': '📂 请选择子分类（1-3个），然后点击“完成”：',
    },
    'btn_subcat_done': {
        'ru': '✅ Готово',
        'kg': '✅ Даяр',
        'en': '✅ Done',
        'cn': '✅ 完成',
    },
    'subcat_max': {
        'ru': '⚠️ Можно выбрать максимум {n} подкатегории.',
        'kg': '⚠️ Эң көбү {n} подкатегория тандаса болот.',
        'en': '⚠️ You can choose at most {n} subcategories.',
        'cn': '⚠️ 最多可选择 {n} 个子分类。',
    },
    'subcat_min': {
        'ru': '⚠️ Выберите хотя бы одну подкатегорию.',
        'kg': '⚠️ Жок дегенде бир подкатегория тандаңыз.',
        'en': '⚠️ Choose at least one subcategory.',
        'cn': '⚠️ 请至少选择一个子分类。',
    },
    'choose_currency': {
        'ru': '💱 Выберите валюту цены:',
        'kg': '💱 Баанын валютасын тандаңыз:',
        'en': '💱 Choose the price currency:',
        'cn': '💱 请选择价格货币：',
    },
    'cooldown_pay_offer': {
        'ru': '💸 Опубликовать досрочно за <b>{price}</b> с баланса?\n💰 Ваш баланс: <b>{balance}</b>',
        'kg': '💸 Мөөнөтүнөн мурда <b>{price}</b> баланстан төлөп жарыялайсызбы?\n💰 Балансыңыз: <b>{balance}</b>',
        'en': '💸 Publish early for <b>{price}</b> from your balance?\n💰 Your balance: <b>{balance}</b>',
        'cn': '💸 用余额支付 <b>{price}</b> 提前发布？\n💰 您的余额：<b>{balance}</b>',
    },
    'cooldown_paid': {
        'ru': '✅ Оплачено! Продолжайте создание объявления.',
        'kg': '✅ Төлөндү! Жарыяны түзүүнү улантыңыз.',
        'en': '✅ Paid! Continue creating your ad.',
        'cn': '✅ 已支付！请继续创建广告。',
    },
    'cooldown_low_balance': {
        'ru': '❌ Недостаточно тезиков (нужно {price}, у вас {balance}).\nПополните баланс: Меню → 👤 Профиль → ➕ Пополнить баланс, затем вернитесь к созданию объявления.',
        'kg': '❌ Тезик жетишсиз ({price} керек, сизде {balance}).\nБалансты толуктаңыз: Меню → 👤 Профиль → ➕ Балансты толуктоо, анан жарыя түзүүгө кайтыңыз.',
        'en': '❌ Not enough teziks (need {price}, you have {balance}).\nTop up: Menu → 👤 Profile → ➕ Top up balance, then return to creating the ad.',
        'cn': '❌ 泰兹币不足（需要 {price}，您有 {balance}）。\n请充值：菜单 → 👤 个人资料 → ➕ 充值余额，然后返回创建广告。',
    },
    'sub_confirm_charge': {
        'ru': '💎 Списать <b>{price}</b> с баланса за подписку?\n💰 Ваш баланс: <b>{balance}</b>',
        'kg': '💎 Жазылуу үчүн баланстан <b>{price}</b> алынсынбы?\n💰 Балансыңыз: <b>{balance}</b>',
        'en': '💎 Charge <b>{price}</b> from your balance for the subscription?\n💰 Your balance: <b>{balance}</b>',
        'cn': '💎 从余额扣除 <b>{price}</b> 用于订阅？\n💰 您的余额：<b>{balance}</b>',
    },

    # ---------- Поддержка / FAQ ----------
    'faq_title': {
        'ru': '❓ <b>Частые вопросы</b>\n\nВыберите раздел, который вас интересует:',
        'kg': '❓ <b>Көп берилүүчү суроолор</b>\n\nСизди кызыктырган бөлүмдү тандаңыз:',
        'en': '❓ <b>Frequently asked questions</b>\n\nChoose a section you are interested in:',
        'cn': '❓ <b>常见问题</b>\n\n请选择您感兴趣的板块：',
    },
    'faq_category_title': {
        'ru': '<b>{category}</b>\n\nВыберите вопрос:',
        'kg': '<b>{category}</b>\n\nСуроону тандаңыз:',
        'en': '<b>{category}</b>\n\nChoose a question:',
        'cn': '<b>{category}</b>\n\n请选择问题：',
    },
    'faq_empty': {
        'ru': '🤷 Здесь пока нет справочных материалов. Загляните позже.',
        'kg': '🤷 Бул жерде азырынча маалымат жок. Кийинчерээк кайрылыңыз.',
        'en': '🤷 No help articles here yet. Please check back later.',
        'cn': '🤷 暂无帮助内容，请稍后再来。',
    },
    'faq_no_items': {
        'ru': '🤷 В этом разделе пока нет вопросов.',
        'kg': '🤷 Бул бөлүмдө азырынча суроолор жок.',
        'en': '🤷 No questions in this section yet.',
        'cn': '🤷 此板块暂无问题。',
    },
    'faq_contact': {
        'ru': '💬 Написать в поддержку',
        'kg': '💬 Колдоо кызматына жазуу',
        'en': '💬 Contact support',
        'cn': '💬 联系客服',
    },
    'faq_back_categories': {
        'ru': '◀️ К разделам',
        'kg': '◀️ Бөлүмдөргө',
        'en': '◀️ To sections',
        'cn': '◀️ 返回板块',
    },
    'faq_back_items': {
        'ru': '◀️ К вопросам',
        'kg': '◀️ Суроолорго',
        'en': '◀️ To questions',
        'cn': '◀️ 返回问题',
    },
    'faq_to_menu': {
        'ru': '🏠 Меню',
        'kg': '🏠 Меню',
        'en': '🏠 Menu',
        'cn': '🏠 菜单',
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