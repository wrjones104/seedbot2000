import sqlite3
import os
import datetime

# --- Configuration ---
OLD_DB_PATH = 'seeDBot_OLD.sqlite'
NEW_DB_PATH = 'seeDBot.sqlite'

# Allowed tables and columns for migration to prevent SQL injection
ALLOWED_SCHEMAS = {
    "presets": ["preset_name", "creator_id", "creator_name", "created_at", "flags", "description", "arguments", "official", "hidden", "gen_count"],
    "users": ["user_id", "bot_admin", "git_user", "race_admin"],
    "seedlist": ["creator_id", "creator_name", "seed_type", "share_url", "timestamp", "server_name", "server_id", "channel_name", "channel_id"]
}
# -------------------

def migrate_table(old_cursor, new_conn, new_cursor, table_name, column_names):
    if table_name not in ALLOWED_SCHEMAS:
        raise ValueError(f"Unauthorized table migration: {table_name}")

    for col in column_names:
        if col not in ALLOWED_SCHEMAS[table_name]:
            raise ValueError(f"Unauthorized column in table {table_name}: {col}")

    print(f"Migrating data for table: {table_name}...")
    
    # Use double quotes for identifiers to handle potential reserved words safely,
    # although they are already validated against the whitelist.
    quoted_table = f'"{table_name}"'
    quoted_columns = ", ".join([f'"{col}"' for col in column_names])

    old_cursor.execute(f"SELECT {quoted_columns} FROM {quoted_table}")
    all_rows = old_cursor.fetchall()
    
    if not all_rows:
        print(f"No data found in old '{table_name}' table. Skipping.")
        return

    # --- FIX: Handle potential NULL values in created_at for presets table ---
    if table_name == 'presets':
        processed_rows = []
        try:
            created_at_index = column_names.index("created_at")
            # created_at is the 4th column (index 3) in the standard list,
            # but we should use its index in column_names to be safe.
            for row in all_rows:
                row_list = list(row)
                if not row_list[created_at_index]: # If created_at is None or empty
                    row_list[created_at_index] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                processed_rows.append(tuple(row_list))
            all_rows = processed_rows
        except ValueError:
            # created_at not in column_names, skip fix
            pass
    # --- END FIX ---

    placeholders = ', '.join(['?'] * len(column_names))
    insert_sql = f"INSERT INTO {quoted_table} ({quoted_columns}) VALUES ({placeholders})"
    
    new_cursor.executemany(insert_sql, all_rows)
    new_conn.commit()
    
    print(f"Successfully migrated {len(all_rows)} rows to '{table_name}'.")


def main():
    if not os.path.exists(OLD_DB_PATH):
        print(f"Error: Old database file not found at '{OLD_DB_PATH}'")
        return

    if not os.path.exists(NEW_DB_PATH):
        print(f"Error: New database file not found at '{NEW_DB_PATH}'. Please run 'python manage.py migrate' first.")
        return
        
    old_conn = sqlite3.connect(OLD_DB_PATH)
    old_cursor = old_conn.cursor()
    new_conn = sqlite3.connect(NEW_DB_PATH)
    new_cursor = new_conn.cursor()

    try:
        for table_name, column_names in ALLOWED_SCHEMAS.items():
            migrate_table(old_cursor, new_conn, new_cursor, table_name, column_names)
        
        print("\nData migration complete!")

    except Exception as e:
        print(f"\nAn error occurred during migration: {e}")
    finally:
        old_conn.close()
        new_conn.close()

if __name__ == '__main__':
    main()
