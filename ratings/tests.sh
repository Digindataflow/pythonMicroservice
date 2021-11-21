$Form = @{
    "isbn" = "4"
    "name" = "book4"
    "price" = "16"
} | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/ratings/ -Method POST -Body $Form -ContentType "application/json"