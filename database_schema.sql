CREATE TABLE IF NOT EXISTS corec_usage (
    id INTEGER PRIMARY KEY,
     LocationId INTEGER, 
     TotalCapacity INTEGER,
     LocationName TEXT,
     LastUpdatedDateAndTime TEXT, 
     LastCount INTEGER, 
     FacilityId INTEGER, 
     IsClosed INTEGER,
     UNIQUE(LocationId, LastUpdatedDateAndTime, FacilityId)
     );