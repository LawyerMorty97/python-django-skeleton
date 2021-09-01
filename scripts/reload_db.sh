# Clears db, reapplies all migrations, and loads test data

_CMD=$0

read -p "Are you sure you want to reset database to initial state? NB! Must only be run locally [y/N] " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Dropping database..."
    dropdb skeleton || exit

    echo "Creating database..."
    createdb skeleton  || exit

    echo "Making migrations..."
    python manage.py makemigrations  || exit

    echo "Migrating..."
    python manage.py migrate  || exit

    echo "Loading test data..."
    python scripts/loaddata.py || exit
fi