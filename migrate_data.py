import sqlite3
import os
import datetime

# --- Configuration ---
OLD_DB_PATH = 'seeDBot_OLD.sqlite'
NEW_DB_PATH = 'seeDBot.sqlite'
# -------------------

def migrate_table(old_cursor, new_conn, new_cursor, table_name, column_names):
    print(f"Migrating data for table: {table_name}...")
    
    old_cursor.execute(f"SELECT {', '.join(column_names)} FROM {table_name}")
    all_rows = old_cursor.fetchall()
    
    if not all_rows:
        print(f"No data found in old '{table_name}' table. Skipping.")
        return

    # --- FIX: Handle potential NULL values in created_at for presets table ---
    if table_name == 'presets':
        processed_rows = []
        # created_at is the 4th column (index 3)
        for row in all_rows:
            row_list = list(row)
            if not row_list[3]: # If created_at is None or empty
                row_list[3] = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
            processed_rows.append(tuple(row_list))
        all_rows = processed_rows
    # --- END FIX ---

    placeholders = ', '.join(['?'] * len(column_names))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
    
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
        preset_cols = ["preset_name", "creator_id", "creator_name", "created_at", "flags", "description", "arguments", "official", "hidden", "gen_count"]
        migrate_table(old_cursor, new_conn, new_cursor, "presets", preset_cols)

        user_cols = ["user_id", "bot_admin", "git_user", "race_admin"]
        migrate_table(old_cursor, new_conn, new_cursor, "users", user_cols)

        seedlist_cols = ["creator_id", "creator_name", "seed_type", "share_url", "timestamp", "server_name", "server_id", "channel_name", "channel_id"]
        migrate_table(old_cursor, new_conn, new_cursor, "seedlist", seedlist_cols)
        
        print("\nData migration complete!")

    except Exception as e:
        print(f"\nAn error occurred during migration: {e}")
    finally:
        old_conn.close()
        new_conn.close()

if __name__ == '__main__':
    main()