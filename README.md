# RU CIDR & SNI — White List для обхода блокировок

Автоматически собирает IP-диапазоны (CIDR) и домены (SNI) российских сервисов
из открытых источников. Включает IP адреса VK Cloud, Яндекс, Mail.ru (MAX),
Сбер, Тинькофф, Госуслуги и сводные списки Роскомнадзора.
Обновляется каждые 6 часов автоматически.

## Ссылки для VPN-клиента

CIDR (IP-диапазоны российских сервисов):
https://raw.githubusercontent.com/Rageru01/white-list/main/configs/CIDR-RU-all.txt

SNI (домены российских сервисов):
https://raw.githubusercontent.com/Rageru01/white-list/main/configs/SNI-RU-all.txt

## Как добавить в VPN клиент

v2rayNG (Android):
Настройки → Параметры маршрутизации → добавить правило → вставить ссылку

Hiddify (Android / iOS):
Настройки → Маршрутизация → Custom Rules → вставить ссылку

v2rayN (Windows):
Настройки → Настройки маршрутизации → Добавить правило → вставить ссылку

Используй как "прямой" маршрут — российские сайты пойдут мимо VPN (быстро),
всё остальное через VPN.

## Источники CIDR

Платформенные IP (Ground-Zerro/DomainMapper):
- VK / ВКонтакте
- Яндекс
- Mail.ru / MAX
- Сбер
- Тинькофф
- Госуслуги
- Одноклассники

Сводные списки:
- igareck/vpn-configs-for-russia (WHITE-CIDR-RU)
- antifilter.download
- 1andrevich/Re-filter-lists
- zhongfly/runet-ip
- ipverse/rir-ip (RU IPv4)
- nicklvsa/russia-blocked

## Источники SNI

- igareck/vpn-configs-for-russia (WHITE-SNI-RU)
- antifilter.download
- 1andrevich/Re-filter-lists
- Ground-Zerro/DomainMapper (VK, Яндекс, Mail.ru домены)
- dartraiden/no-Russia-hosts
- nicklvsa/russia-blocked

## Обновление

Автоматически каждые 6 часов через GitHub Actions.
Ручной запуск: Actions → Update Working Configs → Run workflow.

## Файлы

configs/CIDR-RU-all.txt   — IP-диапазоны (генерируется автоматически)
configs/SNI-RU-all.txt    — домены (генерируется автоматически)
configs/stats.json        — статистика последней проверки
