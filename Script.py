import disnake
from disnake.ext import commands
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('bot_database.db')
c = conn.cursor()

# Создание таблиц
c.execute('''CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT UNIQUE NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS user_roles (
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )''')

conn.commit()

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Команды для работы с ролями
@bot.slash_command(description="Add a new role")
async def role_add(ctx, role_name: str):
    try:
        c.execute('INSERT INTO roles (role_name) VALUES (?)', (role_name,))
        conn.commit()
        await ctx.send(f'Role "{role_name}" added.')
    except sqlite3.IntegrityError:
        await ctx.send(f'Role "{role_name}" already exists.')

@bot.slash_command(description="List all roles")
async def role_list(ctx):
    c.execute('SELECT role_name FROM roles')
    roles = c.fetchall()
    if roles:
        await ctx.send("Roles: " + ", ".join(role[0] for role in roles))
    else:
        await ctx.send("No roles found.")

@bot.slash_command(description="Get a role by name")
async def role_get(ctx, role_name: str):
    c.execute('SELECT id, role_name FROM roles WHERE role_name = ?', (role_name,))
    role = c.fetchone()
    if role:
        await ctx.send(f'Role ID: {role[0]}, Role Name: {role[1]}')
    else:
        await ctx.send(f'Role "{role_name}" not found.')

@bot.slash_command(description="Delete a role")
async def role_delete(ctx, role_name: str):
    c.execute('DELETE FROM roles WHERE role_name = ?', (role_name,))
    conn.commit()
    if c.rowcount:
        await ctx.send(f'Role "{role_name}" deleted.')
    else:
        await ctx.send(f'Role "{role_name}" not found.')

# Команды для работы с ролями пользователей
@bot.slash_command(description="Add a role to a user")
async def rolemember_add(ctx, user: disnake.User, role_name: str):
    c.execute('SELECT id FROM roles WHERE role_name = ?', (role_name,))
    role = c.fetchone()
    if role:
        c.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)', (user.id, role[0]))
        conn.commit()
        await ctx.send(f'Role "{role_name}" added to user {user.name}.')
    else:
        await ctx.send(f'Role "{role_name}" not found.')

@bot.slash_command(description="List roles of a user")
async def rolemember_list(ctx, user: disnake.User):
    c.execute('''SELECT r.role_name FROM roles r
                 JOIN user_roles ur ON r.id = ur.role_id
                 WHERE ur.user_id = ?''', (user.id,))
    roles = c.fetchall()
    if roles:
        await ctx.send(f'Roles for user {user.name}: ' + ", ".join(role[0] for role in roles))
    else:
        await ctx.send(f'User {user.name} has no roles.')

@bot.slash_command(description="Delete a role from a user")
async def rolemember_delete(ctx, user: disnake.User, role_name: str):
    c.execute('SELECT id FROM roles WHERE role_name = ?', (role_name,))
    role = c.fetchone()
    if role:
        c.execute('DELETE FROM user_roles WHERE user_id = ? AND role_id = ?', (user.id, role[0]))
        conn.commit()
        if c.rowcount:
            await ctx.send(f'Role "{role_name}" removed from user {user.name}.')
        else:
            await ctx.send(f'User {user.name} does not have role "{role_name}".')
    else:
        await ctx.send(f'Role "{role_name}" not found.')
 
@bot.slash_command(description="Check database connection")
async def check_db_connection(ctx):
    try:
        c.execute('SELECT 1')
        conn.commit()
        await ctx.send("Database connection is active.")
    except sqlite3.Error as e:
        await ctx.send(f"Database connection failed: {e}")


bot.run('YOUR_BOT_TOKEN')
   
