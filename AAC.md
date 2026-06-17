# Команды для управления `bot.py` на `VPS-сервере` на `Ubuntu 22.04`

###### [AAC] Alterra Administrator Commands // Команды администратора Альтерры

---

### Заход в конкретную папку
````ubuntu
cd ~/tspa
````

### Замена содержимого файла
````ubuntu
cat > bot.py
````

### Выход
````ubuntu
ctrl D
````

### Список файлов
````ubuntu
ls -la
````

### Запуск бота
````ubuntu
python3 bot.py
````

### Статус
````ubuntu
systemctl status tspa
````

###### Ожидаемый ответ `active (running)`

### Статус автозапуска
````ubuntu
systemctl is-enabled tspa
````
###### Ожидаемый ответ `enabled`

### Статус автозапуска
````ubuntu
systemctl is-active tspa
````
###### Ожидаемый ответ `active`

### Перегрузка
````ubuntu
systemctl restart tspa
````
### Остановка
````ubuntu
systemctl stop tspa
````

### Запуск
````ubuntu
systemctl start tspa
````

### Логи
````ubuntu
journalctl -u tspa -f
````

### Последние 50 строк логов
````ubuntu
journalctl -u tspa -n 50
````

---

###### Команды дополняются
