-- DROP TABLE piggyData

-- CREATE TABLE piggyData(
--     Username TEXT,
--     Balance REAL,
--     MPS REAL,
--     MPC REAL,
-- )

-- INSERT INTO piggyData
-- VALUES ('Henrik', 500, 2, 6)

-- SELECT * FROM piggyData

-- SELECT Username, 
--     Balance AS [Balance],
--     MPS AS [MPS],
--     MPC AS [MPC]
-- FROM piggyData
-- FOR JSON PATH, ROOT('PlayerData');

SELECT Username, 
    Balance,
    MPS,
    MPC
FROM piggyData
FOR JSON PATH, ROOT('PlayerData');