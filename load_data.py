import sqlite3
import csv
from pathlib import Path 

class loader:

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def clean(value):
        if value is None:
            return None
        value = value.strip()
        return value if value else None

    def iso_date(v):
        v = loader.clean(v)
        if v and len(v) == 8 and v.isdigit():
            return f"{v[:4]}-{v[4:6]}-{v[6:]}"
        return v

    def atp_match_loader(file_path: str, conn: sqlite3.Connection):

        # tourney_id, -> tourney_id
        # tourney_name,
        # surface,
        # draw_size,
        # tourney_level,
        # indoor,
        # tourney_date,
        # match_num, -> match_num
        # winner_id,  -> wid
        # winner_seed, -> wseed
        # winner_entry,
        # winner_name, -> wname
        # winner_hand,
        # winner_ht,
        # winner_ioc,
        # winner_age,
        # winner_rank, -> wrank
        # winner_rank_points, -> wrank_points
        # loser_id, -> lid
        # loser_seed, -> lseed
        # loser_entry,
        # loser_name, -> lname
        # loser_hand,
        # loser_ht,
        # loser_ioc,
        # loser_age,
        # loser_rank, -> lrank
        # loser_rank_points, -> lrank_points
        # score, -> score
        # best_of, -> best_of
        # round, -> round
        # minutes, -> minutes
        # w_ace, -> w_ace
        # w_df, -> w_df
        # w_svpt, -> w_svpt
        # w_1stIn, -> w_1stIn
        # w_1stWon, -> w_1stWon
        # w_2ndWon, -> w_2ndWon
        # w_SvGms, -> w_SvGms
        # w_bpSaved, -> w_bpSaved
        # w_bpFaced, -> w_bpFaced
        # l_ace, -> l_ace
        # l_df, -> l_df
        # l_svpt, -> l_svpt
        # l_1stIn, -> l_1stIn
        # l_1stWon, -> l_1stWon
        # l_2ndWon, -> l_2ndWon
        # l_SvGms, -> l_SvGms
        # l_bpSaved, -> l_bpSaved
        # l_bpFaced -> l_bpFaced

        print(f"loading from {file_path}")

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                values = [loader.clean(row.get(col)) for col in [
                    'tourney_id', 'match_num', 'winner_id', 'winner_seed', 'winner_name', 'winner_rank',
                    'winner_rank_points', 'loser_id', 'loser_seed', 'loser_name', 'loser_rank', 'loser_rank_points',
                    'score', 'best_of', 'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon',
                    'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn',
                    'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
                ]]

                cursor.execute(
                    """
                    insert or ignore into ATPMatches (tourney_id, match_num, wid, wseed, wname, wrank,
                    wrank_points, lid, lseed, lname, lrank, lrank_points, score, best_of, round, minutes,
                    w_ace, w_df, w_svpt, w_1stIn, w_1stWon, w_2ndWon, w_SvGms, w_bpSaved, w_bpFaced, l_ace,
                    l_df, l_svpt, l_1stIn, l_1stWon, l_2ndWon, l_SvGms, l_bpSaved, l_bpFaced)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    values)

                loaded_count += cursor.rowcount

                

        conn.commit()

        loaded_count += loader.tournament_loader(file_path, "atp", conn)

        return loaded_count

    def wta_match_loader(file_path: str, conn: sqlite3.Connection):

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                values = [loader.clean(row.get(col)) for col in [
                    'tourney_id', 'match_num', 'winner_id', 'winner_seed', 'winner_name', 'winner_rank',
                    'winner_rank_points', 'loser_id', 'loser_seed', 'loser_name', 'loser_rank', 'loser_rank_points',
                    'score', 'best_of', 'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon',
                    'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn',
                    'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
                ]]

                cursor.execute(
                    """
                    insert or ignore into WTAMatches (tourney_id, match_num, wid, wseed, wname, wrank,
                    wrank_points, lid, lseed, lname, lrank, lrank_points, score, best_of, round, minutes,
                    w_ace, w_df, w_svpt, w_1stIn, w_1stWon, w_2ndWon, w_SvGms, w_bpSaved, w_bpFaced, l_ace,
                    l_df, l_svpt, l_1stIn, l_1stWon, l_2ndWon, l_SvGms, l_bpSaved, l_bpFaced)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    values)

                loaded_count += cursor.rowcount

        conn.commit()

        loaded_count += loader.tournament_loader(file_path, "wta", conn)

        return loaded_count

    def ranking_loader(file_path: str, conn: sqlite3.Connection):

        # playerId -> pid
        # rank -> rank
        # points -> points
        # date??

        print(f"loading from {file_path}")

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    """
                    insert or ignore into rankings (pid, rank, points, date)
                    values(?, ?, ?, ?)""", (loader.clean(row.get('playerId')), loader.clean(row.get('rank')),
                    loader.clean(row.get('points')), Path(file_path).stem.split("_")[-1]))

                loaded_count += cursor.rowcount

            conn.commit()

            return loaded_count

    def tournament_loader(file_path: str, tour: str, conn: sqlite3.Connection):

        # tourney_id, -> tid
        # tour_input -> tour
        # tourney_name -> tname
        # surface -> surface
        # draw_size -> draw_size
        # tourney_level -> tlevel
        # indoor, -> indoor
        # tourney_date -> date

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tid = loader.clean(row.get('tourney_id'))
                name = loader.clean(row.get('tourney_name'))
                surface = loader.clean(row.get('surface'))
                draw_size = loader.clean(row.get('draw_size'))
                t_level = loader.clean(row.get('tourney_level'))
                indoor = loader.clean(row.get('indoor'))
                date = loader.iso_date(row.get('tourney_date'))

                cursor.execute(
                    """
                    insert or ignore into tournaments (tid, tour, name, surface, draw_size, tourney_level, indoor, date)
                    values(?, ?, ?, ?, ?, ?, ?, ?)""", (tid, tour, name, surface, draw_size, t_level, indoor, date))

                loaded_count += cursor.rowcount

        conn.commit()

        return loaded_count

    def player_loader(file_path: str, conn: sqlite3.Connection):

        # "id" -> pid
        # "player"
        # "atpname" -> name
        # "birthdate" -> birthdate
        # "weight" 
        # "height" -> height
        # "turnedpro" -> turned_pro
        # "birthplace" -> birthplace
        # "coaches" -> coaches
        # "hand" -> dominant_hand
        # "backhand" -> backhand
        # "ioc" -> nationality

        print(f"loading from {file_path}")

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Clean and convert fields
                pid = loader.clean(row.get('id'))
                name = loader.clean(row.get('atpname'))
                birthdate = loader.iso_date(row.get('birthdate'))
                height_raw = loader.clean(row.get('height'))
                height = int(height_raw) if height_raw else None
                turned_pro_raw = loader.clean(row.get('turnedpro'))
                turned_pro = int(turned_pro_raw) if turned_pro_raw else None
                birthplace = loader.clean(row.get('birthplace'))
                coaches = loader.clean(row.get('coaches'))
                hand = loader.clean(row.get('hand'))
                backhand = loader.clean(row.get('backhand'))
                ioc = loader.clean(row.get('ioc'))

                cursor.execute(
                    """
                    insert or ignore into players (pid, name, birthdate, height, turned_pro, birthplace, coaches,
                    dominant_hand, backhand, nationality) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (pid, name, birthdate, height, turned_pro, birthplace, coaches, hand, backhand, ioc))

                loaded_count += cursor.rowcount

        conn.commit()

        return loaded_count



    

            
            
