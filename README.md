# Интеллектуальный ассистент для CRM

## Установка тестовой среды
Крайне рекомендуется использовать VSCode, т.к. в комплекте идут файлы с настройками

Из корневой папки проекта запускаем `./setup_env.sh`

При необходимости дебаггинга бота там же, в корневой директории, создаём файлик `.env` со следующим содержанием:

```
TOKEN=###############
```

Где указываем вместо решёток токен телеграм-бота из botfather.

После этого в VSCode нажимаем Ctrl+Shift+P, либо View => Command Pallette, далее Python:Select Interpreter, после чего выбираем .venv/bin/python3

## Рекомендации по отладке

Не рекомендуется пользоваться pip install, лучше добавить нужный пакет в requirements в соответствующей папке, затем снова выполнить `./setup_env.sh`

## Сборка Docker-контейнеров

Локальный запуск Docker выполняется с помощью Docker-Compose: `docker-compose up`

Автоматически собранные контейнеры, готовые к использованию, лежат в registry проекта:

```
gitlab.com/vitalymegabyte/crmhack/bot_master
gitlab.com/vitalymegabyte/crmhack/backend_master
```
