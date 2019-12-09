# script for spinning up new db server and running tests logged into a log file
Set-Location "C:\Users\jma\Documents\PSQL11\bin"

Write-Output "Stopping current DB instance"
./pg_ctl -D "C:/Users/jma/Documents/PSQLDB" stop

Write-Output "Stopping test DB instance"
./pg_ctl -D "C:/Users/jma/Documents/PSQLDB-test" stop

Write-Output "Removing Old test database"
Remove-Item -Path "C:/Users/jma/Documents/PSQLDB-test" -Recurse

Write-Output "Creating New test database"
./pg_ctl initdb -D "C:/Users/jma/Documents/PSQLDB-test"
./pg_ctl -D "C:/Users/jma/Documents/PSQLDB-test" -l logfile start
./createuser --superuser --interactive postgres

Write-Output "Migrating Django schema"
Set-Location "C:\Users\jma\Documents\tw-front-back\django"
python manage.py migrate

Write-Output "Press Enter to run tests"
pause

Write-Output "Running Tests"
python manage.py test > "C:\Users\jma\Documents\tw-front-back\django\scripts\test.log"

Write-Output "Finished Tests"
Write-Output "Press Enter to Close Test Server & Exit"
pause
Set-Location "C:\Users\jma\Documents\PSQL11\bin"
./pg_ctl -D "C:/Users/jma/Documents/PSQLDB-test" stop