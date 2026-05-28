# RU CIDR & SNI Collector

Автоматически собирает актуальные списки IP-диапазонов (CIDR) и доменов (SNI) российских сервисов из нескольких публичных источников, объединяет их и обновляет каждые 6 часов без участия пользователя.

## Что это и зачем

**CIDR** — список IP-диапазонов российских сетей (VK, Яндекс, CDN, провайдеры и др.)
**SNI** — список доменных имён российских сайтов

Используются в VPN-клиентах для **раздельной маршрутизации (split tunneling)**:
- Российские сайты открываются напрямую — быстро, без VPN
- Всё остальное идёт через VPN — безопасно

## Файлы

| Файл | Описание |
|------|----------|
| configs/CIDR-RU-all.txt | Объединённый список IP-диапазонов |
| configs/SNI-RU-all.txt | Объединённый список доменов |
| configs/stats.json | Статистика последнего обновления |

## Ссылки для VPN-клиента

CIDR (IP-диапазоны):
https://raw.githubusercontent.com/andreykorolev541-dotcom/vless/main/configs/CIDR-RU-all.txt

SNI (домены):
https://raw.githubusercontent.com/andreykorolev541-dotcom/vless/main/configs/SNI-RU-all.txt

## Как добавить в клиент

### v2rayNG (Android)
Настройки → Параметры маршрутизации → Добавить правило → вставить ссылку

### Hiddify (Android / iOS)
Настройки → Маршрутизация → Custom Rules → вставить ссылку

### v2rayN (Windows)
Настройки → Настройки маршрутизации → Добавить набор правил → вставить ссылку

### Clash / Clash Meta
Использовать CIDR-RU-all.txt как ip-cidr rule-set, SNI-RU-all.txt как domain rule-set

## Источники

### CIDR
- igareck/vpn-configs-for-russia
- antifilter.download
- 1andrevich/Re-filter-lists
- nicklvsa/russia-blocked
- zhongfly/runet-ip
- ipverse/rir-ip

### SNI
- igareck/vpn-configs-for-russia
- antifilter.download
- 1andrevich/Re-filter-lists
- nicklvsa/russia-blocked
- dartraiden/no-Russia-hosts
- zapret-info/z-i

## Обновление

Списки обновляются автоматически каждые 6 часов через GitHub Actions.
Для ручного обновления: вкладка Actions → Update Working Configs → Run workflow.

## Структура репозитория

scripts/
  check_configs.py       скрипт сбора и объединения списков
.github/workflows/
  update-config.yml      автоматический запуск по расписанию
configs/
  CIDR-RU-all.txt        результат (генерируется автоматически)
  SNI-RU-all.txt         результат (генерируется автоматически)
  stats.json             статистика (генерируется автоматически)
