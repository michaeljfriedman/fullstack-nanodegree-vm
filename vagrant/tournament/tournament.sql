-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--------------------------------
-- Drop everything, start fresh
--------------------------------
drop view if exists player_stats;
drop view if exists player_matches;
drop view if exists player_losses;
drop view if exists player_wins;
drop table if exists matches;
drop table if exists players;


--------------------------------
-- Create tables
--------------------------------

-- Players
create table players(
	id serial primary key,
	name text
);

-- Matches
create table matches(
	id serial primary key,
	winner_id serial references players (id),
	loser_id serial references players (id)
);

--------------------------------
-- Create helper views
--------------------------------

-- Players and their wins
create view player_wins as
	select players.id, count(matches.winner_id) as num_wins from
	(players left join matches on players.id = matches.winner_id)
	group by players.id;

-- Players and their losses
create view player_losses as
	select players.id, count(matches.loser_id) as num_losses from
	(players left join matches on players.id = matches.loser_id)
	group by players.id;

-- Players and the number of matches they played
create view player_matches as
	select player_wins.id, sum(num_wins) + sum(num_losses) as num_matches from
	(player_wins join player_losses on player_wins.id = player_losses.id)
	group by player_wins.id;

-- Player ids, player names, number of wins, and number of matches played
create view player_stats as
	select players.id, name, num_wins, num_matches from players, player_wins,
	player_matches where players.id = player_wins.id and players.id = player_matches.id
	order by num_wins desc;