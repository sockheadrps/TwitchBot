from collections import namedtuple

User = namedtuple("User", "table_name sql") 
user = User("users",
                        """
						CREATE TABLE IF NOT EXISTS users (
						UserName varchar(255) PRIMARY KEY,
						Credits INTEGER DEFAULT 100,
						Points INTEGER DEFAULT 100
						);
						""")