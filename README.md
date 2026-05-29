# VLESS Subscription Aggregator

Автоматический сборщик VLESS-конфигураций из популярных открытых источников. Собирает публичные прокси, удаляет дубликаты и сохраняет до 200 конфигураций. Обновляется каждые 6 часов.

---

## 🔗 Ссылки для VPN-клиентов

Вставьте одну из ссылок в ваш клиент (Hiddify, v2rayNG, Nekobox и др.):

**Base64 (рекомендуется для Hiddify):**
`https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_base64.txt`

**Plain Text:**
`https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_plain.txt`

---

## 📱 Как добавить в Hiddify

1. Скопируйте ссылку на `vless_base64.txt`
2. Откройте Hiddify → нажмите **+**
3. Выберите **Добавить подписку по URL**
4. Вставьте ссылку → **Сохранить**
5. Нажмите кнопку обновления

---

## 📦 Источники

| Источник | Репозиторий |
|----------|-------------|
| barry-far | github.com/barry-far/V2ray-Configs |
| soroushmirzaei | github.com/soroushmirzaei/telegram-configs-collector |
| sashalisk | github.com/sashalisk/VPN |
| ermaozi | github.com/ermaozi/get_subscribe |
| mheidari98 | github.com/mheidari98/.proxy |
| Epodonios | github.com/Epodonios/v2ray-configs |

---

## 🔄 Автоматизация

Работает через **GitHub Actions**:
- **По расписанию:** каждые 6 часов
- **Вручную:** Actions → Update Working Configs → Run workflow

---

## 📊 Статистика

Актуальная статистика последнего обновления:
`https://raw.githubusercontent.com/Rageru01/white-list/main/configs/stats.json`
