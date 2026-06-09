# Docker Compose

Лабораторный проект с двумя compose-стеками:

- `flask_redis` - Flask-приложение с Redis.
- `monitoring` - Prometheus, Grafana и Blackbox Exporter для мониторинга приложения.

## Структура

```text
docker-compose/
├── flask_redis/
│   ├── app.py
│   ├── compose.yml
│   ├── dockerfile
│   └── requirements.txt
├── monitoring/
│   ├── compose.yml
│   ├── grafana/
│   │   └── datasource.yml
│   └── prometheus/
│       └── prometheus.yml
└── text_outputs/
    ├── docker_compose_ps_flask.txt
    └── docker_compose_ps_mon.txt
```

## Flask + Redis

Папка: `flask_redis`.

Сервисы:

- `web` - Flask-приложение, собирается из локального `dockerfile`.
- `redis` - Redis из образа `redis:alpine`.

Порт приложения:

```text
http://localhost:8000
```

Внутри контейнера Flask слушает порт `5000`, а наружу проброшен порт `8000`:

```yaml
ports:
  - '8000:5000'
```

Приложение подключается к Redis по имени сервиса `redis` и увеличивает счетчик посещений.

Запуск:

```bash
cd flask_redis
docker compose up -d
```

Остановка:

```bash
docker compose down
```

## Monitoring

Папка: `monitoring`.

Сервисы:

- `prometheus` - собирает метрики.
- `grafana` - показывает dashboards и графики.
- `blackbox` - проверяет доступность HTTP-сервисов снаружи.

Доступные URL:

```text
Prometheus:       http://localhost:9090
Grafana:          http://localhost:3000
Blackbox Exporter http://localhost:9115
```

Логин Grafana:

```text
admin / grafana
```

Запуск:

```bash
cd monitoring
docker compose up -d
```

Остановка:

```bash
docker compose down
```

## Prometheus

Конфиг: `monitoring/prometheus/prometheus.yml`.

Prometheus собирает:

- метрики самого Prometheus с `localhost:9090/metrics`;
- нативные метрики Flask-приложения с `host.docker.internal:8000/metrics`;
- HTTP-проверку Flask-приложения через Blackbox Exporter.

`host.docker.internal` используется, чтобы контейнеры могли обращаться к сервисам, опубликованным на хосте.

## Grafana

Конфиг datasource: `monitoring/grafana/datasource.yml`.

Grafana автоматически подключает Prometheus как datasource:

```text
http://prometheus:9090
```

Это внутренний адрес Docker Compose. Контейнер Grafana обращается к контейнеру Prometheus по имени сервиса `prometheus`.

## Volumes

В `monitoring/compose.yml` используются named volumes:

- `prom_data` - данные Prometheus: временные ряды, WAL, служебное состояние.
- `grafana_data` - данные Grafana: настройки, dashboards, плагины, локальная база.

Обычный `docker compose down` не удаляет эти volumes. Команда ниже удалит контейнеры вместе с данными:

```bash
docker compose down -v
```

## Text Outputs

Папка `text_outputs` содержит сохраненные выводы команд `docker compose ps` для двух стеков. Это справочные снимки текущего состояния контейнеров.
