# VLESS Subscription Aggregator

Автоматический сборщик VLESS-конфигураций с упором на обход блокировок в России.  
Собирает из 50+ источников, убирает дубликаты, приоритизирует REALITY и российские серверы.  
Обновляется каждые 6 часов.

---

## 🔗 Подписки для VPN-клиентов

Вставьте нужную ссылку в Hiddify, v2rayNG, Nekobox, Streisand и др.

### Все конфиги (рекомендуется)
| Формат | Ссылка |
|--------|--------|
| Base64 | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_base64.txt` |
| Plain  | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_plain.txt` |

### Только российские серверы
| Формат | Ссылка |
|--------|--------|
| Base64 | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_russia_base64.txt` |
| Plain  | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_russia_plain.txt` |

### Только REALITY (лучший обход DPI)
| Формат | Ссылка |
|--------|--------|
| Base64 | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_reality_base64.txt` |
| Plain  | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_reality_plain.txt` |

### Только IPv6
| Формат | Ссылка |
|--------|--------|
| Base64 | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_ipv6_base64.txt` |
| Plain  | `https://raw.githubusercontent.com/Rageru01/white-list/main/configs/vless_ipv6_plain.txt` |

---

## 📱 Как добавить подписку

### Hiddify
1. Скопируйте ссылку на `vless_base64.txt` (любую из таблицы выше)
2. Откройте Hiddify → нажмите **+**
3. Выберите **Добавить подписку по URL**
4. Вставьте ссылку → **Сохранить**
5. Нажмите кнопку обновления

### v2rayNG
1. Главный экран → **☰** → **Subscription group**
2. Нажмите **+**, вставьте ссылку на `vless_base64.txt`
3. **OK** → главный экран → **☰** → **Update subscription**

### Nekobox / NekoRay
1. **Profiles** → **New group** → тип **Subscription**
2. Вставьте ссылку → **OK**
3. Правой кнопкой по группе → **Update**

---

## 📦 Источники

### 🇷🇺 Россия и СНГ
| Источник | Репозиторий |
|----------|-------------|
| soroushmirzaei (RU) | github.com/soroushmirzaei/telegram-configs-collector |
| Surfboardv2ray (RU) | github.com/Surfboardv2ray/Proxy-sorter |
| coldwater (RU) | github.com/coldwater-10/V2Hub |
| yebekhe (RU) | github.com/yebekhe/TVC |
| v2rayse (RU) | github.com/v2rayse/node-list |
| Proxifly (RU) | github.com/Proxifly/free-proxy-list |

### ✨ REALITY / TLS
| Источник | Репозиторий |
|----------|-------------|
| lagzian | github.com/lagzian/SS-Collector |
| coldwater | github.com/coldwater-10/V2rayCollector |
| SoliSpirit | github.com/SoliSpirit/v2ray-configs |
| Surfboardv2ray | github.com/Surfboardv2ray/Proxy-sorter |

### 🌐 Крупные агрегаторы
| Источник | Репозиторий |
|----------|-------------|
| barry-far | github.com/barry-far/V2ray-Configs |
| soroushmirzaei | github.com/soroushmirzaei/telegram-configs-collector |
| mahdibland | github.com/mahdibland/V2RayAggregator |
| MrMohebi | github.com/MrMohebi/xray-proxy-grabber-telegram |
| Epodonios | github.com/Epodonios/v2ray-configs |
| yebekhe | github.com/yebekhe/TVC |

---

## 🔄 Автоматизация

Работает через **GitHub Actions**:
- **По расписанию:** каждые 6 часов
- **Вручную:** Actions → *Update Working Configs* → **Run workflow**

При каждом запуске:
1. Загружает конфиги из всех источников
2. Декодирует base64 там, где нужно
3. Убирает дубликаты
4. Приоритизирует: Россия → REALITY → IPv6 → остальные
5. Сохраняет до 1000 конфигов и обновляет статистику

---

## 📊 Статистика последнего обновления
