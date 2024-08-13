--
-- gamenum.sql
--
-- Created: 2024.08.12
-- Copyright: Steven E. Pav, 2024
-- Author: Steven E. Pav <steven@gilgamath.com>
-- Comments: Steven E. Pav

CREATE OR REPLACE TABLE bigjoin AS (
WITH 
indat AS (
  SELECT * 
  FROM read_csv('stacked_antichess.csv',
    DELIM=',',
    HEADER = true,
    IGNORE_ERRORS = true,
    COLUMNS = {
    'site': 'VARCHAR',
    'datetime': 'DATETIME',
    'time_control' : 'VARCHAR',
    'termination': 'VARCHAR',
    'outcome': 'DOUBLE',
    'nply': 'INT2',
    'move1': 'VARCHAR',
    'move2': 'VARCHAR',
    'move3': 'VARCHAR',
    'move4': 'VARCHAR',
    'move5': 'VARCHAR',
    'move6': 'VARCHAR',
    'move7': 'VARCHAR',
    'move8': 'VARCHAR',
    'move9': 'VARCHAR',
    'move10': 'VARCHAR',
    'moves': 'VARCHAR',
    'white': 'VARCHAR',
    'black': 'VARCHAR',
    'white_elo': 'BIGINT',
    'black_elo': 'BIGINT',
    'white_elo_diff': 'VARCHAR',
    'black_elo_diff': 'VARCHAR',
    'rr_ply': 'INT2',
    't1_ply': 'INT2',
    't2_ply': 'INT2',
    't3_ply': 'INT2',
    'l1_dpawn': 'VARCHAR',
    'l1_dknight': 'VARCHAR',
    'l1_dbishop': 'VARCHAR',
    'l1_drook': 'VARCHAR',
    'l1_dqueen': 'VARCHAR',
    'l1_dking': 'VARCHAR',
    'rr_dpawn': 'INT1',
    'rr_dknight': 'INT1',
    'rr_dbishop': 'INT1',
    'rr_drook': 'INT1',
    'rr_dqueen': 'INT1',
    'rr_dking': 'INT1',
    't1_dpawn': 'INT1',
    't1_dknight': 'INT1',
    't1_dbishop': 'INT1',
    't1_drook': 'INT1',
    't1_dqueen': 'INT1',
    't1_dking': 'INT1',
    't2_dpawn': 'INT1',
    't2_dknight': 'INT1',
    't2_dbishop': 'INT1',
    't2_drook': 'INT1',
    't2_dqueen': 'INT1',
    't2_dking': 'INT1',
    't3_dpawn': 'INT1',
    't3_dknight': 'INT1',
    't3_dbishop': 'INT1',
    't3_drook': 'INT1',
    't3_dqueen': 'INT1',
    't3_dking': 'INT1',
    })
),
all_play AS (
  SELECT site, datetime, white AS pid
  FROM indat

  UNION ALL

  SELECT site, datetime, black AS pid
  FROM indat
),
dist_play AS (
  SELECT DISTINCT site, datetime, pid
  FROM all_play
),
add_rows AS (
  SELECT site, pid, ROW_NUMBER() OVER (PARTITION BY pid ORDER BY datetime ASC) AS gamenum
  FROM dist_play
),
attached AS (
  SELECT 
  ind.*,
  war.gamenum AS white_gamenum,
  bar.gamenum AS black_gamenum
FROM
  indat AS ind
LEFT JOIN
  add_rows AS war
ON
  ind.site = war.site
AND
  ind.white = war.pid
LEFT JOIN
  add_rows AS bar
ON
  ind.site = bar.site
AND
  ind.black = bar.pid
)
SELECT * FROM attached ORDER BY datetime, site
);

COPY bigjoin TO 'uni_out.csv' (HEADER);

--for vim modeline: (do not edit)
-- vim:ts=2:sw=2:tw=129:expandtab:fdm=indent:cms=--%s:syn=mysql:ft=mysql:ai:si:cin:nu:fo=croql:cino=p0t0c5(0:
