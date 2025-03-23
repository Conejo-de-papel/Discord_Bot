# Project Documentation for Discord Bot

## Description

This project is a Discord bot that manages user roles and permissions on a server. The bot connects to an SQLite database to store role information.

## Installation and Setup

### Requirements

- Python 3.12.4 or higher
- `disnake` library
- `sqlite3` library

### Installing Dependencies

Use the `pip` command to install the required libraries:

```sh
pip install disnake
```

### Database Setup

Create an SQLite database and tables to store roles and user roles:

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

### Running the Bot

1. Replace `YOUR_BOT_TOKEN` in the code with your actual bot token.
2. Run the script:

```sh
Script.py
```

## Commands

### Role Management

#### `/role_add <role_name>`

Adds a new role to the database.

Example:
```
/role_add Moderator
```

#### `/role_list`

Lists all roles.

Example:
```
/role_list
```

#### `/role_get <role_name>`

Retrieves information about a role by its name.

Example:
```
/role_get Moderator
```

#### `/role_delete <role_name>`

Deletes a role from the database.

Example:
```
/role_delete Moderator
```

### User Role Management

#### `/rolemember_add <user> <role_name>`

Adds a role to a user.

Example:
```
/rolemember_add @user Moderator
```

#### `/rolemember_list <user>`

Lists the roles of a user.

Example:
```
/rolemember_list @user
```

#### `/rolemember_delete <user> <role_name>`

Removes a role from a user.

Example:
```
/rolemember_delete @user Moderator
```

### Database Connection Check

#### `/check_db_connection`

Checks the connection to the database.

Example:
```
/check_db_connection
```

## Error Handling

The bot includes basic checks and error messages for the following cases:

- Attempting to add an already existing role.
- Attempting to add a role to a user when the role does not exist.
- Attempting to remove a role from a user when the role is not assigned.
- Attempting to delete a non-existent role.

## Notes

1. Ensure your bot has the necessary permissions on the Discord server to execute commands (e.g., `Ban Members`, `Manage Roles`).
2. Use appropriate permissions for commands to restrict their usage to server administrators or moderators.
