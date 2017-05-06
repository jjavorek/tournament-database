import psycopg2


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def registerPlayer(name):
    """Adds a player to the tournament database."""
    query = 'INSERT INTO players (name) VALUES (%s);'
    conn = connect()
    c = conn.cursor()
    c.execute(query, (name,))
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    remove_matches_query = "DELETE FROM matches;"
    remove_players_query = 'DELETE FROM players;'
    conn = connect()
    c = conn.cursor()
    c.execute(remove_matches_query)
    c.execute(remove_players_query)
    conn.commit()
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    set_wins_to_zero_query = "UPDATE players SET wins = 0;"
    set_matches_to_zero_query = "UPDATE players SET matches = 0;"
    remove_matches_query = "DELETE FROM matches;"
    conn = connect()
    c = conn.cursor()
    c.execute(set_wins_to_zero_query)
    c.execute(set_matches_to_zero_query)
    c.execute(remove_matches_query)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    query = 'SELECT COUNT(player_id) as NUM FROM players;'
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    result = int(c.fetchone()[0])
    conn.commit()
    conn.close()
    return result

def playerStandings():
    """Returns a list of the players and their records of wins, this is sorted by wins."""
    query = 'SELECT * FROM players ORDER BY wins DESC;'
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""
    add_match_query = 'INSERT INTO matches (winner_id, loser_id) VALUES ({0}, {1});'.format(winner, loser)
    add_winner_query = 'UPDATE players SET matches=matches+1, wins=wins+1 WHERE player_id = {0};'.format(winner)
    add_loser_query = 'UPDATE players SET matches=matches+1 WHERE player_id = {0};'.format(loser)
    conn = connect()
    c = conn.cursor()
    c.execute(add_match_query)
    c.execute(add_winner_query)
    c.execute(add_loser_query)
    conn.commit()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""
    pairings = []
    players = playerStandings()
    if len(players) < 2:
        raise KeyError("Not enough players.")
    for i in range(0, len(players), 2):
        pairings.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1]))
    return pairings
