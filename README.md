# Скрипт "Cisco Statistic Port"
## Данный скрипт работает следующими моделями Cisco:
1. *WS-C3560G-48PS*
2. *WS-C2960S-48FPS-L*
3. *WS-C2960S-48LPS-L*
4. *WS-C3560X-48P*
5. *WS-C2960G-24TC-L*
6. *WS-C3560X-48P*
7. *WS-C2960G-24TC-L*

### Работа скрипта.
1. Открыть файл *ipaddress.json*
    - добавить нужные ip адреса сетевых устр-в в том-же формате.
2. Открыть файл *main.py*
    - найти строку *auth_user*, установить *login* и *password* для авторизации на сетевом устройстве.
3. Запускаем скрипт!

### Вывод файла будет сохранен в файл *data.json*:
```
{
  "ASW-STK-15-1": [
    {
      "IP-address": "10.2.0.1",
      "Model device": "WS-C3560G-48PS",
      "Vendor": "Cisco",
      "Port RJ45": 48,
      "Port SFP": 4,
      "Location": "Hall 1",
      "Count port": 52,
      "Busy port": 4,
      "Free port": 48
    }
  ],
  "ASW-STK-15-2": [
    {
      "IP-address": "10.2.0.2",
      "Model device": "WS-C3560G-48PS",
      "Vendor": "Cisco",
      "Port RJ45": 48,
      "Port SFP": 4,
      "Location": "Hall 2",
      "Count port": 52,
      "Busy port": 1,
      "Free port": 51
    }
  ],
  "ASW-STK-15-3": [
    {
      "IP-address": "10.2.0.3",
      "Model device": "WS-C3560G-48PS",
      "Vendor": "Cisco",
      "Port RJ45": 48,
      "Port SFP": 4,
      "Location": "Hall 3",
      "Count port": 52,
      "Busy port": 3,
      "Free port": 49
    }
  ]
}
```
