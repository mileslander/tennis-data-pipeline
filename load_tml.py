from pathlib import Path
import sqlite3
from load_data import loader

def load_tml():
    if not Path("./tml-data").exists:
        raise("tml-data directory does not exist")
    if not Path("./tml-data").is_dir:
        raise("tml-data directory does not exist")

    data_directory = Path("./tml-data")

    conn = sqlite3.connect("tennis_data.db")


    for path in data_directory.iterdir():
        if "laver" in path.name:
            continue
        if "amateur" in path.name:
            continue
        elif "wta" in path.name:
            loader.wta_match_loader(path, conn)
        elif "Database" in path.name:
            loader.player_loader(path, conn)
        elif "rankings" in path.name:
            loader.ranking_loader(str(path), conn)
        else:
            loader.atp_match_loader(path, conn)
    
if __name__ == "__main__":
    load_tml()
