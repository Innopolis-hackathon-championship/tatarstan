LEXICON_RU: dict[str, str] = {
    '/start': 'Для начала торговли Вам требуется принять правила нашего бота\n\n'
              'С правилами вы можете ознаокмиться по ссылке ниже:\n',
    '/help': 'Меню помощи:\n'
             '/profile - открыть профиль\n'
             '/menu - открыть меню для торгов\n'
             '/support - показать контакты поддержки\n'
             '/help - меню помощи',
    'no_echo': 'Данный тип апдейтов не поддерживается '
               'методом send_copy',
    '/menu': 'Выберите актив, в который вы хотите инвестировать:',
    'welcome': 'Добро пожаловать в stolovaya bot, используя\n'
               'нашего бота вы сможете торговать акциями, \nфиатами и'
               'криптовалютой.\n\n'
               'Меню помощи:\n'
               '/profile - открыть профиль\n'
               '/menu - открыть меню для торгов\n'
               '/support - показать контакты поддержки\n'
               '/help - меню помощи',
    '/profile': f"🪪 ID: {user_data['user_id']}\n\n"
                                         f"👤 ФИО: {user_data['username'] if user_data['username'] else 'не заполнено'}\n\n"
                                         f"🏠 Адрес: {user_data['adress'] if user_data['adress'] else 'не заполнено'}\n\n"
                                         f"☎️ Номер телефона: {user_data['phone_number'] if user_data['phone_number'] else 'не заполнено'}\n\n"
                                         f"🛒 Всего покупок: {user_data['order_value']}\n\n"
                                         f"🔥 Персональная скидка: {user_data['personal_sale']}%\n\n"
                                         f"🗒 Примечания: {user_data['notes'] if user_data['notes'] else 'не заполнено'}",
    'rules_accept_button': '✅Принять'}
