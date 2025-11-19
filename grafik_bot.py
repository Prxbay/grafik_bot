async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text.startswith(TARGET_PREFIX):
        return
    if TARGET_LINE_PREFIX not in text:
        return
    if not any(month in text.lower() for month in MONTHS):
        return

    # Извлекаем дату (без преобразования)
    date_match = re.search(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")", text.lower())
    if date_match:
        day, month = date_match.groups()
        formatted_date = f"{day} {month}"
    else:
        formatted_date = "дату не удалось извлечь"

    # Извлекаем часы отключения для строки 3.2
    line_match = re.search(r"3\.2\s+([^\n\r]+)", text)
    if line_match:
        line_times = line_match.group(1).strip()
    else:
        line_times = "не удалось извлечь часи"

    # Формируем сообщение
    message = f"🗓️ Дата: {formatted_date}\n💡 Часи: {line_times}"

    for user_id in RECIPIENTS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")