# Social AI Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](./pyproject.toml)
[![Status: Foundation](https://img.shields.io/badge/status-foundation-orange.svg)](./CHANGELOG.md)
[![Telegram Approval](https://img.shields.io/badge/approval-Telegram-2CA5E0?logo=telegram)](./docs/approval-workflow.md)

> Автопилот для Instagram, который не забывает о человеке за штурвалом.

---

## Что это

**Social AI Engine** — модульный AI-движок для автоматического ведения Instagram-аккаунтов.
Он планирует контент, генерирует посты, картинки и видео, отправляет их на одобрение в Telegram
и публикует через Meta Graph API. Всё управляется YAML-конфигами: новый проект или формат
добавляется одним файлом.

Для кого: эксперты, личные бренды, продуктовые команды и локальный бизнес, которым надоело
проводить вечера в соцсетях, но которые не готовы отдавать публикацию полностью чёрному ящику.

---

## Возможности

- 📅 **Планирование** — контент-план в `content-plan.yaml`, scheduler берёт темы по порядку.
- 🤖 **Генерация** — тексты через OpenRouter, изображения (DALL·E / Stable Diffusion), карусели и видеоаватары (HeyGen).
- ✈️ **Публикация** — Instagram через Meta Graph API и Telegram как backup / cross-post.
- ✅ **Telegram-одобрение** — кнопки «Одобрить / Изменить / Отклонить / Опубликовать сейчас».
- 🔄 **Аналитика и feedback loop** — собирает метрики постов и корректирует будущий контент.
- 🧩 **Расширяемость** — новый тип поста = интерфейс + шаблон + один файл генератора.

---

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone git@github.com:Shugar86/social-ai-engine.git
cd social-ai-engine

# 2. Создать виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt
pip install -e ".[dev]"

# 4. Подготовить переменные окружения
cp .env.example .env
# отредактируй .env и добавь свои токены

# 5. Создать новый проект
python scripts/init_project.py --name my_brand
# заполни projects/my_brand/config.yaml, brand-voice.md, content-plan.yaml
```

> **Статус:** фаза фундамента. Архитектура, интерфейсы, конфиги и документация готовы;
> реализация отдельных модулей ведётся итеративно.

---

## Архитектура

```text
┌─────────────────────────────────────────────┐
│  projects/          ← конфиги, бренд, планы  │
├─────────────────────────────────────────────┤
│  approvers/         ← Telegram-бот, UI       │
├─────────────────────────────────────────────┤
│  core/              ← scheduler, queue, state│
├─────────────────────────────────────────────┤
│  generators/        ← текст, картинка, аватар│
├─────────────────────────────────────────────┤
│  publishers/        ← Instagram, Telegram    │
├─────────────────────────────────────────────┤
│  analytics/         ← метрики, feedback loop │
└─────────────────────────────────────────────┘
```

Жизненный цикл поста:

```text
[ PLAN ] → [ GENERATE ] → [ QUEUE ] → [ APPROVE ] → [ PUBLISH ] → [ ANALYZE ]
    ↑___________________________________________________________↓
                              (feedback loop)
```

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| Язык | Python 3.11+ | Асинхронное ядро и генераторы |
| Конфиги | YAML | Проекты, планы, шаблоны prompt'ов |
| LLM | OpenRouter API | Генерация текстов и идей |
| Изображения | DALL·E 3 / Stable Diffusion | Посты и карусели |
| Аватар-видео | HeyGen API | Видео с цифровым двойником |
| Telegram | `python-telegram-bot` v20+ | Одобрение и уведомления |
| Instagram | Meta Graph API v21.0 | Публикация постов и Reels |
| Хранилище | SQLite + SQLAlchemy | Очередь постов и состояние |
| Линт / тесты | `ruff`, `mypy`, `pytest` | Качество кода |

Подробнее см. [docs/architecture.md](./docs/architecture.md).

---

## Структура репозитория

```text
social-ai-engine/
├── README.md                    # ты здесь
├── AGENTS.md                    # контракт для AI-агентов
├── LICENSE                      # MIT
├── CONTRIBUTING.md              # как участвовать
├── CHANGELOG.md                 # история изменений
├── .env.example                 # шаблон переменных окружения
├── pyproject.toml               # метаданные проекта и dev-зависимости
├── requirements.txt             # runtime-зависимости
├── docs/
│   ├── architecture.md          # детальная архитектура
│   ├── content-pillars.md       # контент-стратегия
│   ├── approval-workflow.md     # workflow одобрения
│   └── api-references.md        # шпаргалки по API
├── projects/
│   ├── _template/               # шаблон нового проекта
│   ├── doctor_yulia/            # проект: врач-косметолог
│   └── ai_stylist/              # проект: AI-стилист
├── core/                        # ядро: интерфейсы, scheduler, queue
├── generators/                  # генераторы контента
├── publishers/                  # паблишеры
├── approvers/                   # системы одобрения
├── analytics/                   # аналитика
├── scripts/                     # утилиты (init_project.py)
└── tests/                       # тесты
```

---

## Текущие проекты

| Проект | Описание | Особенности |
|--------|----------|-------------|
| `doctor_yulia` | Личный бренд врача-косметолога | Экспертный контент, медицинская этика, AI-аватар, DM → запись |
| `ai_stylist` | Продвижение приложения AI-стилиста | Reuse карточек `card_engine`, вирусные механики |

---

## 📍 С чего начать чтение

Чтобы разобраться в проекте за ~15 минут, читай в таком порядке:

1. **`core/interfaces.py`** — центральные контракты (ABC): `Post`, `ContentGenerator`, `Publisher`, `Approver`, `Queue`, `Scheduler`. Это «скелет» движка.
2. **`publishers/interfaces.py`** — контракт `Publisher` (`publish()` + `health_check()`): именно его реализуют конкретные публикаторы.
3. **`scripts/init_project.py`** — как заводится новый бренд/проект из YAML-конфига.

## Примеры

### Добавить новый проект

```bash
python scripts/init_project.py --name my_brand
```

Затем отредактируй:

- `projects/my_brand/config.yaml` — настройки публикации и генерации.
- `projects/my_brand/brand-voice.md` — тон, табу, аудитория.
- `projects/my_brand/content-plan.yaml` — темы и форматы постов.

### Добавить новый тип контента

1. Создать шаблон: `projects/<name>/templates/my_type.yaml`.
2. Создать генератор: `generators/my_type.py`, реализовав `ContentGenerator`.
3. Добавить тест: `tests/generators/test_my_type.py`.
4. Зарегистрировать в `generators/__init__.py`.

Не трогай соседние модули — только свой файл + регистрацию.

### Включить автопилот

В `projects/<name>/config.yaml`:

```yaml
approval:
  mode: "auto"          # "manual" | "auto"
  auto_publish_after: "24h"
```

При `auto` Telegram-бот не шлёт посты на одобрение, но уведомляет после публикации.

---

## Характер проекта

**Вайб:** `human-in-the-loop` — «автопилот, который не забывает о человеке за штурвалом».

1. **Последнее слово за человеком.** По умолчанию пост уходит на одобрение в Telegram, а не сразу в ленту.
2. **Не чёрный ящик.** Каждый пост виден до публикации; автопилот включается осознанно, через конфиг.
3. **Один файл — один шаг.** Новый формат добавляется генератором и шаблоном, без правок соседних модулей.

---

## Дорожная карта

См. [CHANGELOG.md](./CHANGELOG.md).

---

## Участие

См. [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Лицензия

[MIT](./LICENSE) © 2026 Shugar86.
