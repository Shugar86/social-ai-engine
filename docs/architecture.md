# Архитектура Social AI Engine

## Принципы

1. **Модульность.** Каждый компонент заменяем. Хочешь вместо Telegram-бота сделать Web-UI — реализуешь `Approver` и всё.
2. **Конфиг-ориентированность.** Поведение проекта определяется YAML, не кодом.
3. **Прозрачность.** Любой пост можно отследить от генерации до публикации.
4. **Расширяемость.** Новый тип контента = новый файл генератора + шаблон.

## Компоненты

### Core (ядро)

| Компонент | Ответственность |
|-----------|-----------------|
| `Scheduler` | По расписанию или внешнему триггеру запускает генерацию |
| `Queue` | Хранит посты в статусах: pending, waiting_approval, approved, rejected, published, failed |
| `StateManager` | Знает текущее состояние каждого проекта: что в очереди, когда последний пост |
| `Orchestrator` | Склеивает всё: берёт тему → вызывает генератор → кладёт в очередь → ждёт одобрения → публикует → анализирует |

### Generators (генераторы)

| Генератор | Выход | Описание |
|-----------|-------|----------|
| `TextGenerator` | `text: str, caption: str` | LLM через OpenRouter |
| `ImageGenerator` | `image_url: str` | DALL-E 3 / Stable Diffusion |
| `AvatarVideoGenerator` | `video_url: str` | HeyGen API, цифровой двойник |
| `CarouselGenerator` | `images: list[str]` | Несколько картинок + unified caption |

Каждый генератор читает шаблон из `projects/<name>/templates/<type>.yaml`.

### Publishers (паблишеры)

| Паблишер | Назначение |
|----------|------------|
| `InstagramPublisher` | Посты, Reels, Stories через Meta Graph API |
| `TelegramPublisher` | Копия поста в канал/группу (backup, cross-post) |

### Approvers (одобрение)

| Компонент | Роль |
|-----------|------|
| `TelegramApprover` | Бот шлёт превью, принимает ✅ ✏️ ❌ |
| `AutoApprover` | Фейковый компонент, сразу одобряет (режим autopilot) |

### Analytics (аналитика)

| Компонент | Роль |
|-----------|------|
| `MetricsCollector` | Забирает лайки, комменты, охват из Meta API |
| `FeedbackLoop` | Корректирует генераторы на основе топовых постов |

## State machine поста

```
┌─────────┐     generate      ┌─────────────────┐
│  PLAN   │ ─────────────────→│  PENDING        │
└─────────┘                   └─────────────────┘
                                       │
                                       │ queue
                                       ▼
                              ┌─────────────────┐
                              │ WAITING_APPROVAL│◄──────┐
                              └─────────────────┘       │
                                │  │  │                 │
                                ▼  ▼  ▼                 │
                           ┌────┐┌───┐┌────┐           │
                           │ ✅ ││ ✏️││ ❌ │           │
                           └─┬─┘└─┬─┘└─┬─┘           │
                             │    │    │               │
                             ▼    │    ▼               │
                        ┌────────┐│ ┌─────────┐        │
                        │APPROVED││ │REJECTED │        │
                        └───┬────┘│ └─────────┘        │
                            │     │                    │
                            ▼     └────────────────────┘
                     ┌──────────┐
                     │PUBLISHING│
                     └────┬─────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌────────┐  ┌────────┐  ┌────────┐
        │PUBLISHED│  │FAILED  │  │SCHEDULED│
        └────┬───┘  └────────┘  └────────┘
             │
             ▼
     ┌───────────────┐
     │ ANALYZED      │
     └───────────────┘
```

## Поток данных (подробно)

### 1. Планирование

`Scheduler` смотрит `projects/<name>/content-plan.yaml`:

```yaml
plan:
  - date: "2025-06-01"
    topic: "Почему коллаген не работает в кремах"
    type: "educational"
    format: "carousel"
  - date: "2025-06-01"
    topic: "Утренняя рутина ухода"
    type: "tip_of_day"
    format: "avatar_video"
```

Если `type` и `format` не указаны — берутся случайно из доступных.

### 2. Генерация

`Orchestrator` выбирает генераторы по `format`:
- `carousel` → `TextGenerator` + `CarouselGenerator`
- `avatar_video` → `TextGenerator` + `AvatarVideoGenerator`

Генераторы читают `projects/<name>/templates/<type>.yaml`:

```yaml
template: educational
system_prompt: |
  Ты — профессиональный косметолог с 10-летним опытом.
  Тон: дружелюбный, но экспертный. Без паникёрства.
  Запрещено: давать медицинские диагнозы, назначать лечение.
structure:
  - hook: "Миф, который вредит вашей коже"
  - body: "3–5 абзацев с фактами"
  - cta: "Вопрос к аудитории или призыв записаться"
hashtags: ["скincare", "косметология", "уходзакожей"]
```

Результат — объект `Post`:

```python
@dataclass
class Post:
    id: str                      # uuid
    project: str                 # "doctor_yulia"
    type: str                    # "educational"
    format: str                  # "carousel"
    status: PostStatus           # enum
    text: str                    # полный текст
    caption: str                 # caption для Instagram (с хэштегами)
    media: list[MediaAsset]      # картинки/видео
    scheduled_at: datetime
    created_at: datetime
    approved_at: datetime | None
    published_at: datetime | None
    published_url: str | None
    analytics: Analytics | None
```

### 3. Очередь

`Queue` (SQLite) хранит `Post`. Главный индекс — `(project, status, scheduled_at)`.

### 4. Одобрение

`TelegramApprover` шлёт сообщение:

```
📋 Проект: doctor_yulia
📝 Тип: educational / carousel
📅 Запланировано: 01.06 09:00

─── Превью ───
[картинка 1] [картинка 2] [картинка 3]

Caption:
Миф: коллаген в креме восстанавливает кожу.
Факт: молекула коллагена слишком велика...

#skincare #косметология

[✅ Одобрить] [✏️ Редактировать] [❌ Отклонить] [🚀 Сразу]
```

**Кнопка ✏️ Редактировать:**
Бот переходит в режим ожидания текста. Юзер присылает новый caption → Post обновляется → бот показывает превью снова.

**Кнопка 🚀 Сразу:**
Публикует моментально, игнорируя `scheduled_at`.

### 5. Публикация

`InstagramPublisher` работает через Meta Graph API:

```
POST /{ig-user-id}/media           → creation_id (для Reels/каруселей: upload + configure)
GET  /{creation_id}?fields=status_code  → ждём "FINISHED"
POST /{ig-user-id}/media_publish    → опубликовано
```

После успеха: `status = PUBLISHED`, `published_url = https://instagram.com/p/...`

### 6. Аналитика

Через 24ч после публикации `MetricsCollector` забирает:
- impressions, reach, engagement, likes, comments, shares, saves

`FeedbackLoop` анализирует: если `saves > threshold` → тема похожа на "сохраняемый" контент → повышаем приоритет похожих тем в плане.

## Расширяемость

### Новый тип контента

1. `projects/<name>/templates/my_thing.yaml` — prompt, структура, ограничения
2. `generators/my_thing.py` — класс, реализующий `ContentGenerator`
3. `tests/generators/test_my_thing.py` — моки, тест генерации
4. Регистрация в `generators/registry.py` (одна строка)

### Новый проект

1. `cp -r projects/_template projects/my_brand`
2. Заполнить `config.yaml`, `brand-voice.md`, `content-plan.yaml`
3. Добавить секреты в `.env`
4. Готово — scheduler начнёт работу по расписанию

### Новый канал публикации

1. `publishers/my_channel.py` — класс, реализующий `Publisher`
2. Регистрация в `publishers/registry.py`
3. В `config.yaml` проекта добавить `publish_to: ["instagram", "my_channel"]`
