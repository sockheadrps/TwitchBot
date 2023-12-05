schema_econ = {
    "table_name": "economy",
    "sql": """
			CREATE TABLE IF NOT EXISTS economy (
			UserName varchar(255) PRIMARY KEY,
			Credits INTEGER DEFAULT 100
		);
		"""
}