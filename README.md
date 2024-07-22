# Discord_Bot

# Документация к проекту Discord Bot

## Описание

Этот проект представляет собой Discord-бота, который управляет ролями и правами пользователей на сервере. Бот подключается к базе данных SQLite для хранения информации о ролях.

## Установка и запуск

### Требования

- Python 3.12.4 или выше
- Библиотека `disnake`
- Библиотека `sqlite3`

### Установка зависимостей

Используйте команду `pip` для установки необходимых библиотек:

```sh
pip install disnake
```

### Настройка базы данных

Создайте базу данных SQLite и таблицы для хранения ролей и пользовательских ролей:

```sql
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles (id),
    PRIMARY KEY (user_id, role_id)
);
```

### Запуск бота

1. Замените `YOUR_BOT_TOKEN` в коде на ваш фактический токен бота.
2. Запустите скрипт:

```sh
python bot.py
```

## Команды

### Управление ролями

#### `/role_add <role_name>`

Добавляет новую роль в базу данных.

Пример:
```
/role_add Moderator
```

#### `/role_list`

Список всех ролей.

Пример:
```
/role_list
```

#### `/role_get <role_name>`

Получить информацию о роли по имени.

Пример:
```
/role_get Moderator
```

#### `/role_delete <role_name>`

Удалить роль из базы данных.

Пример:
```
/role_delete Moderator
```

### Управление пользовательскими ролями

#### `/rolemember_add <user> <role_name>`

Добавляет роль пользователю.

Пример:
```
/rolemember_add @user Moderator
```

#### `/rolemember_list <user>`

Список ролей пользователя.

Пример:
```
/rolemember_list @user
```

#### `/rolemember_delete <user> <role_name>`

Удаляет роль у пользователя.

Пример:
```
/rolemember_delete @user Moderator
```

### Проверка подключения к базе данных

#### `/check_db_connection`

Проверяет соединение с базой данных.

Пример:
```
/check_db_connection
```

## Обработка ошибок

Бот включает базовые проверки и сообщения об ошибках для следующих случаев:

- Попытка добавить уже существующую роль.
- Попытка добавить роль пользователю, когда роль не существует.
- Попытка удалить роль у пользователя, когда роль не назначена.
- Попытка удалить несуществующую роль.

## Примечания

1. Убедитесь, что ваш бот имеет необходимые разрешения на сервере Discord для выполнения команд (например, `Ban Members`, `Manage Roles`).
2. Используйте подходящие права доступа для команд, чтобы ограничить их использование только администраторами или модераторами сервера.
