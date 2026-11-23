from pathlib import Path
import sqlite3
from load_data import loader
import os
from datetime import timezone, datetime

# Get most recent tournament date from tennis_data.db
def get_last_tournament(conn: sqlite3.Connection) -> str:
    cursor = conn.execute("SELECT MAX(date) FROM Tournaments")

    return cursor.fetchone()[0]

# Get schema from tennis_data.db
def get_schema(conn: sqlite3.Connection) -> str:
    cursor = conn.execute("PRAGMA user_version;")

    return cursor.fetchone()[0]

# Get table counts from tennis_data.db
def populate_table_counts(conn: sqlite3.Connection):
    tables = [name for (name,) in conn.execute(
        "select name from sqlite_schema where type='table' "
        "and name not in ('Metadata', 'TableCounts')")]

    for name in tables:
        (count,) = conn.execute(f"select count(*) from {name}").fetchone()
        conn.execute("insert into TableCounts values (?, ?)", (name, count))

    conn.commit()

# Verify that old count < new count < 101% * old count
def compare_counts(old_conn: sqlite3.Connection, new_conn: sqlite3.Connection):
    old = dict(old_conn.execute("select table_name, row_count from TableCounts where table_name != 'Rankings'"))
    new = dict(new_conn.execute("select table_name, row_count from TableCounts where table_name != 'Rankings'"))

    for table, old_count in old.items():
        if table not in new:
            raise ValueError(f"{table} missing from new build")
        if new[table] < old_count:
            raise ValueError(f"{table} shrank: {old_count} -> {new[table]}") 
        if new[table] > old_count * 1.01:  
            raise ValueError(f"{table} grew greater than 1%: {old_count} -> {new[table]}") 

def populate_metadata(new_conn):

    new_schema = get_schema(new_conn)
    populate_table_counts(new_conn)

    new_conn.execute(
        "insert into Metadata (built_at, schema_version, last_tournament_date) values (?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), new_schema, get_last_tournament(new_conn)))
    new_conn.commit()

    old_path = Path("tennis_data.db")
    if not old_path.exists():
        return
    
    old_conn = sqlite3.connect(f"file:{old_path}?mode=ro", uri=True)

    try:
        old_schema = get_schema(old_conn)

        has_counts = old_conn.execute(
            "select 1 from sqlite_schema where name='TableCounts'").fetchone()
        
        if new_schema < old_schema:
            raise ValueError(f"Schema version went backwards: {old_schema} -> {new_schema}")
        
        if new_schema == old_schema and has_counts:
            compare_counts(old_conn, new_conn)

    finally:
        old_conn.close()

def load_tml():
    if not Path("./tml-data").exists():
        raise FileNotFoundError("tml-data directory does not exist")
    if not Path("./tml-data").is_dir():
        raise FileNotFoundError("tml-data directory does not exist")

    data_directory = Path("./tml-data")

    tmp = Path("tennis_data.db.tmp")
    tmp.unlink(missing_ok=True)

    new_conn = sqlite3.connect(tmp)
    new_conn.executescript(Path("tennis_schema.sql").read_text())

    loaded_count = 0

    for path in data_directory.iterdir():
        if "laver" in path.name:
            continue
        if "amateur" in path.name:
            continue
        elif "wta" in path.name:
            loaded_count += loader.wta_match_loader(path, new_conn)
        elif "Database" in path.name:
            loaded_count += loader.player_loader(path, new_conn)
        elif "rankings" in path.name:
            loaded_count += loader.ranking_loader(str(path), new_conn)
        else:
            loaded_count += loader.atp_match_loader(path, new_conn)

    print(f"Loaded {loaded_count} match and player records")

    populate_metadata(new_conn)

    new_conn.close()
    os.replace(tmp, "tennis_data.db")
    
if __name__ == "__main__":
    load_tml()
