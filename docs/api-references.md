# API References

## Meta Graph API (Instagram)

### Публикация фото

```http
POST https://graph.facebook.com/v21.0/{ig-user-id}/media
Content-Type: application/x-www-form-urlencoded

image_url={url}&caption={caption}&access_token={token}
```

Response:
```json
{"id": "17920212345678901"}
```

### Публикация (publish)

```http
POST https://graph.facebook.com/v21.0/{ig-user-id}/media_publish
Content-Type: application/x-www-form-urlencoded

creation_id={id}&access_token={token}
```

### Проверка статуса

```http
GET https://graph.facebook.com/v21.0/{creation_id}?fields=status_code&access_token={token}
```

Status codes: `FINISHED`, `IN_PROGRESS`, `ERROR`

### Карусель

1. Загрузить каждое изображение отдельно → получить `id` каждого
2. Создать контейнер карусели:
```http
POST /{ig-user-id}/media
children={id1,id2,id3}&media_type=CAROUSEL&caption={caption}&access_token={token}
```
3. Опубликовать через `media_publish` с `creation_id`

### Reels

1. Загрузить видео через `media` с `media_type=REELS` и `video_url`
2. Ждать `status_code=FINISHED` (до 5 минут)
3. Опубликовать через `media_publish`

### Важно
- Все изображения — JPEG
- Размер < 8MB
- Соотношение сторон: 1:1 (квадрат), 4:5 (портрет), 1.91:1 (ландшафт)
- Видео Reels: 9:16, минимум 720px, MP4
- Токен — System User Token (не протухает)

---

## HeyGen API (Avatar Video)

### Создание видео

```http
POST https://api.heygen.com/v2/video/generate
Content-Type: application/json
X-Api-Key: {key}

{
  "video_inputs": [{
    "character": {
      "type": "avatar",
      "avatar_id": "{avatar_id}",
      "avatar_style": "normal"
    },
    "voice": {
      "type": "text",
      "input_text": "Привет, сегодня разберём...",
      "voice_id": "{voice_id}"
    }
  }],
  "dimension": {"width": 1080, "height": 1920}
}
```

Response:
```json
{"data": {"video_id": "xxx"}}
```

### Статус

```http
GET https://api.heygen.com/v1/video_status.get?video_id={video_id}
X-Api-Key: {key}
```

---

## OpenRouter API (LLM)

```http
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer {key}
Content-Type: application/json

{
  "model": "openai/gpt-5.4",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ]
}
```

---

## DALL-E 3 (Image Generation)

```http
POST https://api.openai.com/v1/images/generations
Authorization: Bearer {key}
Content-Type: application/json

{
  "model": "dall-e-3",
  "prompt": "...",
  "size": "1024x1024",
  "quality": "standard",
  "n": 1
}
```

---

## Telegram Bot API

Используем `python-telegram-bot`. Ключевые методы:

```python
await context.bot.send_message(chat_id=chat_id, text=text)
await context.bot.send_photo(chat_id=chat_id, photo=open(path, "rb"), caption=caption)
await context.bot.send_media_group(chat_id=chat_id, media=media_group)
```

InlineKeyboardMarkup для кнопок:
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("✅ Одобрить", callback_data=f"approve:{post_id}")],
    [InlineKeyboardButton("✏️ Редактировать", callback_data=f"edit:{post_id}")],
    [InlineKeyboardButton("❌ Отклонить", callback_data=f"reject:{post_id}")],
]
reply_markup = InlineKeyboardMarkup(keyboard)
```

---

## Полезные ссылки

- Meta Graph API Docs: https://developers.facebook.com/docs/instagram-api
- HeyGen API Docs: https://docs.heygen.com/
- OpenRouter Docs: https://openrouter.ai/docs
- python-telegram-bot: https://docs.python-telegram-bot.org/
