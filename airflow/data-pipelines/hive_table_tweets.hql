CREATE TABLE IF NOT EXISTS tweets ( 
    tweet String,
    dt Date,
    retweet_from String,
    before_clean_len int,
    after_clean_len int)
COMMENT 'tweets data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;