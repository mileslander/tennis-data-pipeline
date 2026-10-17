import sqlite3
import csv

class loader:

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def load_all_data(match_path: str, ranking_path: str, tournament_path: str, player_path: str, conn: sqlite3.Connection):

        loader.atp_match_loader(match_path, conn)

        loader.wta_match_loader(match_path, conn)

        loader.ranking_loader(ranking_path, conn)

        loader.tournament_loader(tournament_path, conn)

        loader.player_loader(player_path, conn)

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
                cursor.execute(
                    """
                    insert or ignore into ATPMatches (tourney_id, match_num, wid, wseed, wname, wrank, 
                    wrank_points, lid, lseed, lname, lrank, lrank_points, score, best_of, round, minutes,
                    w_ace, w_df, w_svpt, w_1stIn, w_1stWon, w_2ndWon, w_SvGms, w_bpSaved, w_bpFaced, l_ace,
                    l_df, l_svpt, l_1stIn, l_1stWon, l_2ndWon, l_SvGms, l_bpSaved, l_bpFaced) 
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row['tourney_id'], row['match_num'], row['winner_id'], row['winner_seed'], row['winner_name'], row['winner_rank'], 
                    row['winner_rank_points'], row['loser_id'], row['loser_seed'], row['loser_name'], row['loser_rank'], row['loser_rank_points'], 
                    row['score'], row['best_of'], row['round'], row['minutes'], row['w_ace'], row['w_df'], row['w_svpt'], row['w_1stIn'], row['w_1stWon'], 
                    row['w_2ndWon'], row['w_SvGms'], row['w_bpSaved'], row['w_bpFaced'], row['l_ace'], row['l_df'], row['l_svpt'], row['l_1stIn'], 
                    row['l_1stWon'], row['l_2ndWon'], row['l_SvGms'], row['l_bpSaved'], row['l_bpFaced']))

                loaded_count += 1

        conn.commit()

        print(f"Loaded {loaded_count} atp matches from {file_path}")

    def wta_match_loader(file_path: str, conn: sqlite3.Connection):

        cursor = conn.cursor()

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    """
                    insert or ignore into WTAMatches (tourney_id, match_num, wid, wseed, wname, wrank, 
                    wrank_points, lid, lseed, lname, lrank, lrank_points, score, best_of, round, minutes,
                    w_ace, w_df, w_svpt, w_1stIn, w_1stWon, w_2ndWon, w_SvGms, w_bpSaved, w_bpFaced, l_ace,
                    l_df, l_svpt, l_1stIn, l_1stWon, l_2ndWon, l_SvGms, l_bpSaved, l_bpFaced) 
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row['tourney_id'], row['match_num'], row['winner_id'], row['winner_seed'], row['winner_name'], row['winner_rank'], 
                    row['winner_rank_points'], row['loser_id'], row['loser_seed'], row['loser_name'], row['loser_rank'], row['loser_rank_points'], 
                    row['score'], row['best_of'], row['round'], row['minutes'], row['w_ace'], row['w_df'], row['w_svpt'], row['w_1stIn'], row['w_1stWon'], 
                    row['w_2ndWon'], row['w_SvGms'], row['w_bpSaved'], row['w_bpFaced'], row['l_ace'], row['l_df'], row['l_svpt'], row['l_1stIn'], 
                    row['l_1stWon'], row['l_2ndWon'], row['l_SvGms'], row['l_bpSaved'], row['l_bpFaced']))

                loaded_count += 1

        conn.commit()

        print(f"Loaded {loaded_count} wta matches from {file_path}")

    def ranking_loader(file_path: str, conn: sqlite3.Connection):

        # playerId -> pid
        # rank -> rank
        # points -> points
        # date??

        print(f"Loading from {file_path}")

        cursor = conn.cursor()

        spilt_file_name = file_path.split("_")

        ranking_date = spilt_file_name[2]

        loaded_count = 0

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    """
                    insert or ignore into rankings (pid, rank, points, date)
                    values(?, ?, ?, ?)""", (row['playerId'], row['rank'], row['points'], ranking_date))

                loaded_count += 1

            conn.commit()

            print(f"loaded {loaded_count} atp rankings from {file_path}")

    def tournament_loader(file_path: str, conn: sqlite3.Connection):

        # tourney_id, -> tid
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
                cursor.execute(
                    """
                    insert or ignore into tournaments (tid, tname, surface, draw_size, tlevel, indoor, date)
                    values(?, ?, ?, ?, ?, ?, ?)""", (row['tourney_id'], row['tname'], row['surface'], row['draw_size'],
                    row['tourney_level'], row['indoor'], row['tourney_date']))

                loaded_count += 1

        conn.commit()

        print(f"loaded {loaded_count} tournaments from {file_path}")

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
                # Convert empty strings to None for integer columns
                height = int(row['height']) if row['height'].strip() else None
                turned_pro = int(row['turnedpro']) if row['turnedpro'].strip() else None

                cursor.execute(
                    """
                    insert or ignore into players (pid, name, birthdate, height, turned_pro, birthplace, coaches,
                    dominant_hand, backhand, nationality) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row['id'], row['atpname'], row['birthdate'], height, turned_pro, row['birthplace'],
                     row['coaches'], row['hand'], row['backhand'], row['ioc']))

                loaded_count += 1

        conn.commit()

        print(f"loaded {loaded_count} player profiles from {file_path}")



    

            
            
