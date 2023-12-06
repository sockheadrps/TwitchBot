from collections import namedtuple

Economy = namedtuple("Economy", "table_name sql") 
economy = Economy("economy",
                        """
						CREATE TABLE IF NOT EXISTS economy (
						UserName varchar(255) PRIMARY KEY,
						Points INTEGER DEFAULT 100
						);
						""")