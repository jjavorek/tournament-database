CREATE DATABASE tournament;
\c tournament;

-- TABLE players records players infor
CREATE TABLE players
(
player_id SERIAL PRIMARY KEY,
name VARCHAR(30) NOT NULL,
wins INTEGER DEFAULT 0,
matches INTEGER DEFAULT 0
);


-- TABLE matches records match record
CREATE TABLE matches
(
match_id SERIAL PRIMARY KEY,
winner_id INTEGER,
loser_id INTEGER,
FOREIGN KEY (winner_id) REFERENCES players(player_id),
FOREIGN KEY (loser_id) REFERENCES players(player_id)
);



