SELECT "FirstName", "LastName", SUM("Cash_Amount")
FROM "CSV"
GROUP BY "FirstName", "LastName", "City", "State", "Zip", "PAC"
ORDER BY "sum" DESC;
