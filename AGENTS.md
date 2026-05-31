# AGENTS.md — Social AI Engine

## Стек

- **Python 3.11+**
- **HTTP-клиент:** `httpx` (async)
- **База данных:** SQLite (MVP), миграции через `alembic` (если понадобится)
- **Telegram:** `python-telegram-bot` v20+ (async)
- **API:** Meta Graph API v21.0, HeyGen API, OpenRouter API
- **Конфиги:** YAML
- **Scheduler:** `APScheduler` или `celery` (решится при имплементации)

## Правила для AI-кодера

1. **Интерфейсы священны.** Любой новый модуль реализует существующий интерфейс из `*/interfaces.py`. Не меняй интерфейс без согласования.
2. **Конфиг-ориентированность.** Всё, что может быть в YAML — должно быть в YAML. Код читает конфиг, не хардкодит.
3. **Один проект = одна папка.** Все ассеты, шаблоны, токены проекта — в `projects/<name>/`. Не смешивать.
4. **Минимальные изменения.** Добавляешь фичу — добавляешь один файл. Не рефакторь соседний код.
5. **Тесты.** Каждый генератор и паблишер покрыт unit-тестом с моками API.
6. **No secrets in git.** Токены — только в `.env`. Конфиги проектов — в git, но без секретов.

## Как работать с этой кодовой базой

### Добавить генератор

```python
# generators/my_thing.py
from generators.interfaces import ContentGenerator, Post

class MyThingGenerator(ContentGenerator):
    async def generate(self, topic: str, project_config: dict) -> Post:
        # implementation
        pass
```

### Добавить паблишер

```python
# publishers/telegram_channel.py
from publishers.interfaces import Publisher, Post

class TelegramPublisher(Publisher):
    async def publish(self, post: Post, credentials: dict) -> str:
        # returns post_id
        pass
```

### Добавить новый проект

Скопировать `projects/_template/` → `projects/my_new/`, заменить значения. Не создавать новые структуры папок.

## Важные пути

- `core/interfaces.py` — все контракты системы
- `projects/<name>/config.yaml` — единая точка конфигурации проекта
- `projects/<name>/templates/*.yaml` — шаблоны постов с prompt'ами

## Контекст бизнеса

Движок обслуживает два принципиально разных кейса:
1. **Личный бренд эксперта** — требует медицинской этики, одобрения каждого поста, AI-аватара реального человека.
2. **Продуктовый аккаунт** — вирусные механики, reuse существующих ассетов приложения, меньше ограничений.

При добавлении фичи проверяй: она работает для обоих кейсов или только для одного? Если только для одного — выноси в project-specific конфиг.
