library("dplyr")                                                  # Load dplyr package
library("plyr")                                                   # Load plyr package
library("readr")                                                  # Load readr package

years <- seq(from = 2019, to = 1980, by = -1)
datasets <- c("box_score_plus_", "game_summaries_", "total_officals_")
path = "/Users/alexanderxiong/Documents/stat405/nba_analysis/data/"
box_store_call <- rep(list(0), times = 40)
summary_store_call <- rep(list(0), times = 40)
officials_store_call <- rep(list(0), times = 40)

for (idx in 1:40) {
  box_store_call[[idx]] = read.csv(paste0(path, datasets[1], as.character(years[idx]), ".csv"), header = TRUE)
  summary_store_call[[idx]] = read.csv(paste0(path, datasets[2], as.character(years[idx]), ".csv"), header = TRUE)
  officials_store_call[[idx]] = read.csv(paste0(path, datasets[3], as.character(years[idx]), ".csv"), header = TRUE)
  
  box_store_call[[idx]]$Year = years[idx]
  box_store_call[[idx]]$MIN = as.integer(box_store_call[[idx]]$MIN)
  summary_store_call[[idx]]$Year = years[idx]
  if (years[idx] > 1995){
    officials_store_call[[idx]]$Year = years[idx]
  }
}

# c(GAME_ID, TEAM_ID, TEAM_ABBREVIATION, TEAM_CITY,
#   PLAYER_ID, PLAYER_NAME, START_POSITION, COMMENT,
#   MIN, FGM, FGA, FG_PCT, FG3A, FG3M, FG3_PCT,
#   FTA, FTM, FT_PCT,  DREB, OREB, REB,
#   AST, STL, BLK, TO, PF, PTS, PLUS_MINUS)

# c(GAME_ID, TEAM_ID, TEAM_ABBREVIATION, TEAM_CITY,
#   PLAYER_ID, PLAYER_NAME, START_POSITION, COMMENT,
#   MIN, FGM, FGA, FG_PCT, FG3A, FG3M, FG3_PCT,
#   FTA, FTM, FT_PCT,  DREB, OREB, REB,
#   AST, STL, BLK, TO, PF, PTS, PLUS_MINUS,
#   EFG_PCT, FTA_RATE, OPP_EFG_PCT, OPP_FTA_RATE, 
#   OPP_OREB_PCT, OPP_TOV_PCT, OREB_PCT, TM_TOV_PCT,
#   BLKA, OPP_PTS_2ND_CHANCE,
#   OPP_PTS_FB, OPP_PTS_OFF_TOV, OPP_PTS_PAINT, PFD,
#   PTS_2ND_CHANCE, PTS_FB, PTS_OFF_TOV, PTS_PAINT)

select_box_store_call <- rep(list(0), times = 40)
super_box_store_call <- rep(list(0), times = 24)
super_officials_store_call <- rep(list(0), times = 24)
for (idx in 1:40) {
  ### Append for only the box score data
  select_box_store_call[[idx]] <- select(box_store_call[[idx]], GAME_ID, TEAM_ID, TEAM_ABBREVIATION, TEAM_CITY,
                                         PLAYER_ID, PLAYER_NAME, START_POSITION, COMMENT,
                                         MIN, FGM, FGA, FG_PCT, FG3A, FG3M, FG3_PCT,
                                         FTA, FTM, FT_PCT,  DREB, OREB, REB,
                                         AST, STL, BLK, TO, PF, PTS, PLUS_MINUS, Year)
  ### Append for the super data
  if (years[idx] > 1995) {
    super_box_store_call[[idx]] <- box_store_call[[idx]]
    super_officials_store_call[[idx]] <- officials_store_call[[idx]]
  }
}

basic_box_score <- bind_rows(select_box_store_call)
super_box_score <- bind_rows(super_box_store_call)
total_summary <- bind_rows(summary_store_call)
super_officials <- bind_rows(super_officials_store_call)

nrow(basic_box_score)
nrow(super_box_score)
nrow(total_summary)
nrow(super_officials)

write.csv(basic_box_score, paste0(path, "basic_box_score_1980_2019.csv"))
write.csv(super_box_score, paste0(path, "super_box_score_1980_2019.csv"))
write.csv(total_summary, paste0(path, "total_summary_1980_2019.csv"))
write.csv(super_officials, paste0(path, "super_officials_1980_2019.csv"))

          
          
          
          
          
          