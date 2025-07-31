# Текстовый квест-бот для Telegram

Бот реализует интерактивную историю с системой репутации и здоровья, где выбор игрока влияет на развитие сюжета.

## Основные компоненты

### Инициализация бота
```python
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
```

```bash
YOUR_TOKEN = 'YOUR TOKEN HERE'
bot = telebot.TeleBot(YOUR_TOKEN)
Базы данных игры
Диалоги и сцены
python
dialogue_map = {
    (0, 1): "You dont remember neither who you are...",
    (0, 2): "Suddenly, you found yourself driving...",
    # ... остальные диалоги ...
    (-1, 1): "Game over."
}
Варианты выбора и последствия
python
dialogue_map_branches = {
    (0, 5): [
        [1, "Yes sir! Washing floors...", 0, -100, 1],
        [2, "No.", -20, 20, 2],
        [3, "Its time to fight!", -40, -40, 3]
    ],
    # ... остальные варианты выбора ...
}
Описания последствий
python
conss_map = {
    1: "Your boss is happy. And your reputation is not.",
    2: "Auch. Everybody are impressed...",
    # ... остальные последствия ...
}
```

### Игровая логика
Генерация клавиатуры
```bash
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("<", callback_data="kb_prev"),
               InlineKeyboardButton(">", callback_data="kb_next"))
    try:
        for x in dialogue_map_branches[(branch, position)]:
            markup.add((InlineKeyboardButton(x[1], callback_data=x[4])))
    except:
        pass
    return markup
```


Обработка действий игрока
```bash
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global position, branch, reputation, health
    
    # Логика обработки навигации и выбора вариантов
    if call.data == "kb_next":
        # ... код обработки ...
    elif call.data == "kb_prev":
        # ... код обработки ...
    else:
        # ... код обработки выбора ...
```


Запуск игры

```bash
@bot.message_handler(commands=["start"])
def message_handler(message):
    global branch, position, health, reputation
    branch = 0
    position = 1
    health = 0
    reputation = 0
    bot.send_message(message.chat.id, 
                    f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", 
                    reply_markup=gen_markup())

bot.infinity_polling()
```



## Особенности реализации

### Система ветвления сюжета:

1. Диалоги организованы в виде (ветка, позиция)
2. Каждый выбор влияет на статистику персонажа

### Игровая механика:

1. Параметры "Здоровье" и "Репутация"
2. Критические значения параметров приводят к Game Over

### Навигация:

1. Кнопки "<" и ">" для перемещения по тексту
2. Интерактивные кнопки выбора действий

### Динамическая клавиатура:

1. Кнопки генерируются в зависимости от текущей сцены
2. Отображаются только доступные варианты выбора



## Для запуска замените YOUR TOKEN HERE на действительный токен вашего бота.
