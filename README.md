# Social AI Engine

Полностью модульный AI-движок для автоматического ведения Instagram-аккаунтов. 
Генерация контента, одобрение через Telegram, публикация через Meta Graph API — всё конфигурируется через YAML и расширяется новыми модулями.

## Два текущих кейса

| Проект | Описание | Особенности |
|--------|----------|-------------|
| `doctor_yulia` | Личный бренд врача-косметолога | AI-аватар (HeyGen), экспертный контент, DM → запись на приём |
| `ai_stylist` | Продвижение приложения AI-стилиста | Reuse готовых карточек `card_engine`, вирусные механики |

## Архитектура: 5 слоёв

```
┌─────────────────────────────────────────────┐
│  projects/          ← конфиги, бренд, столпы │
├─────────────────────────────────────────────┤
│  approvers/         ← Telegram-бот, UI       │
├─────────────────────────────────────────────┤
│  core/              ← scheduler, queue, state│
├─────────────────────────────────────────────┤
│  generators/        ← текст, картинка, аватар│
├─────────────────────────────────────────────┤
│  publishers/        ← Instagram, Stories, TG │
├─────────────────────────────────────────────┤
│  analytics/         ← метрики, feedback loop │
└─────────────────────────────────────────────┘
```

## Жизненный цикл поста

```
[ PLAN ] → [ GENERATE ] → [ QUEUE ] → [ APPROVE ] → [ PUBLISH ] → [ ANALYZE ]
    ↑___________________________________________________________↓
                              (feedback loop)
```

## Структура репозитория

```
social-ai-engine/
├── README.md
├── AGENTS.md                    # правила для AI-кодера
├── docs/
│   ├── architecture.md          # детальная архитектура
│   ├── content-pillars.md       # контент-стратегия
│   ├── approval-workflow.md     # workflow одобрения
│   └── api-references.md        # шпаргалки по API
├── projects/
│   ├── doctor_yulia/            # проект: врач
│   └── ai_stylist/              # проект: ai-stylist
├── core/                        # ядро (интерфейсы + реализация)
├── generators/                  # генераторы контента
├── publishers/                  # паблишеры
├── approvers/                   # системы одобрения
├── analytics/                   # аналитика
├── scripts/                     # утилиты
├── tests/                       # тесты
├── pyproject.toml
├── requirements.txt
└── .env.example
```

## Как добавить новый проект

```bash
python scripts/init_project.py --name my_new_brand
```

Скрипт создаст папку в `projects/my_new_brand/` с шаблоном конфига, brand-voice и примером content-plan.

## Как добавить новый тип контента (для AI-кодера)

1. Создать шаблон в `projects/<name>/templates/my_type.yaml`
2. Создать генератор в `generators/my_type.py`, реализовав `ContentGenerator`
3. Добавить тест в `tests/generators/test_my_type.py`
4. Не трогать соседние модули — только свой файл + регистрацию в `generators/__init__.py`

## Как включить автопилот

В `projects/<name>/config.yaml`:

```yaml
approval:
  mode: "auto"          # "manual" | "auto"
  auto_publish_after: "24h"
```

## Статус

Фаза: **фундамент**. Структура, интерфейсы, документация — готовы. Реализация модулей — в очереди.
