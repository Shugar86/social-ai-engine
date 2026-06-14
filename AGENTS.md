# Social AI Engine — контракт для агента

**Версия:** 0.1.0 · **Вайб:** professional — надёжный AI-ассистент за кулисами соцсетей.

---

## 0. Режим работы

- **Pair-programmer**, не автономный продакт. Пользователь задаёт приоритеты; ты исполняешь, проверяешь, сужаешь неопределённость.
- **Язык:** русский — продукт ориентирован на русскоязычные Telegram/Instagram-каналы.
- **Тон:** professional — спокойный, уважительный, экспертный. Без хайпа, паники и пустых обещаний.

---

## 1. Продукт

**Social AI Engine** — модульный AI-движок для автоматического ведения Instagram-аккаунтов.
Генерирует контент, отправляет на одобрение через Telegram, публикует через Meta Graph API.
Работает для личных брендов (врач-косметолог) и продуктовых аккаунтов (AI-стилист).

Ключевые ценности:

- Контроль человека на каждом этапе.
- Медицинская и профессиональная этика.
- Минимальная рутина и максимальная ясность.

---

## 2. Вайб продукта

- **Тон:** professional — спокойный, уважительный, экспертный.
- **3 правила:**
  1. Экспертный и уважительный тон: без хайпа, паники и пустых обещаний.
  2. Человек всегда на контроле: одобрение, редактирование, этика — прежде автопилота.
  3. Минимум воды, максимум ясности: чёткие команды, прозрачные статусы, минимальный diff.

---

## 3. Стек и архитектура

| Область | Технология |
|---------|------------|
| Язык | Python 3.11+ |
| HTTP-клиент | `httpx` (async) |
| База данных | SQLite (MVP), миграции через `alembic` при необходимости |
| Telegram | `python-telegram-bot` v20+ (async) |
| Планировщик | `APScheduler` |
| Конфиги | YAML |
| LLM | OpenRouter API |
| Изображения | DALL·E 3 / Stable Diffusion |
| Аватар-видео | HeyGen API |
| Публикация | Meta Graph API v21.0 (Instagram), Telegram |
| Линт / тесты | `ruff`, `mypy`, `pytest`, `pytest-asyncio` |

Архитектура слоёв:

```text
projects/  →  approvers/  →  core/  →  generators/  →  publishers/  →  analytics/
```

Жизненный цикл поста:

```text
[ PLAN ] → [ GENERATE ] → [ QUEUE ] → [ APPROVE ] → [ PUBLISH ] → [ ANALYZE ]
    ↑___________________________________________________________↓
```

---

## 4. Инженерная дисциплина

- **KISS / минимальный diff / YAGNI.** Добавляешь фичу — добавляешь один файл.
- **Интерфейсы священны.** Любой новый модуль реализует существующий интерфейс из `*/interfaces.py`. Не меняй интерфейс без согласования.
- **Конфиг-ориентированность.** Всё, что может быть в YAML — должно быть в YAML. Код читает конфиг, не хардкодит.
- **Один проект = одна папка.** Все ассеты, шаблоны, токены проекта — в `projects/<name>/`. Не смешивать.
- **Тесты.** Каждый генератор и паблишер покрыт unit-тестом с моками внешних API.
- **No secrets in git.** Токены — только в `.env`. Конфиги проектов — в git, но без секретов.
- **Не ломай:** сомневаешься — спроси, не делай предположений.

---

## 5. Git workflow

- Коммить результат задачи — часть работы.
- Пушь, если пользователь просил или задача требует публикации.
- **Текущая ветка:** `main`.
- **Remotes:**
  - `origin` — `git@github.com:Shugar86/social-ai-engine.git`

Проверь актуальный список:

```bash
git remote -v
git branch --show-current
```

---

## 6. Definition of Done

1. Изменения соответствуют существующим интерфейсам.
2. Добавлены/пройдены релевантные тесты и lint (`ruff`, `mypy`).
3. Конфиги вынесены в YAML, секреты не попали в git.
4. Отчёт: что изменилось, что запускал, риски.
5. Документация и примеры обновлены при необходимости.
6. Соответствие вайбу продукта: professional, человек в центре.

---

## 7. Эскалация

Спроси пользователя, если:

- Нужно добавить или использовать секреты/токены.
- Два равных архитектурных пути и выбор влияет на несколько проектов.
- Изменение касается prod-деплоя, публикации от имени клиента или медицинской этики.

---

## 8. Как работать с кодовой базой

### Добавить генератор

```python
# generators/my_thing.py
from __future__ import annotations

from typing import Any

from core.interfaces import ContentGenerator, Post


class MyThingGenerator(ContentGenerator):
    async def generate(
        self,
        topic: str,
        content_type: str,
        project_config: dict[str, Any],
    ) -> Post:
        # Реализация: вызов LLM/API, сборка Post
        ...
```

### Добавить паблишер

```python
# publishers/my_channel.py
from __future__ import annotations

from typing import Any

from core.interfaces import Post, Publisher


class MyChannelPublisher(Publisher):
    async def publish(self, post: Post, credentials: dict[str, Any]) -> str:
        # returns post_id или permalink
        ...

    async def health_check(self, credentials: dict[str, Any]) -> bool:
        # Проверка валидности credentials
        ...
```

### Добавить новый проект

```bash
python scripts/init_project.py --name my_new_brand
```

Затем заполни:

- `projects/my_new_brand/config.yaml`
- `projects/my_new_brand/brand-voice.md`
- `projects/my_new_brand/content-plan.yaml`

---

## 9. Важные пути

- `core/interfaces.py` — все контракты системы.
- `projects/<name>/config.yaml` — единая точка конфигурации проекта.
- `projects/<name>/templates/*.yaml` — шаблоны постов с prompt'ами.
- `docs/architecture.md` — подробная архитектура.
- `README.md` — человеческое введение.
- `CONTRIBUTING.md` — правила участия.
- `CHANGELOG.md` — история изменений.

---

## 10. Запрещено

- Не коммить `.env`, `*.pem`, токены, ключи, пароли, `github_pat_*`.
- Не публиковать URL remote, содержащие токены.
- Не добавлять в репозиторий сгенерированный контент, логи, `__pycache__/`, `node_modules/`.
