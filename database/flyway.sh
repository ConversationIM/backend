USER=${MYSQL_USERNAME:='root'}
PASSWORD=${MYSQL_PASSWORD:=''}
HOST=${MYSQL_HOST:='localhost'}
PORT=${MYSQL_PORT:='3306'}
SCHEMA='conversationIM'

SCRIPT_DIR=$(dirname $0)

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flyway command>"
    echo "Type 'flyway' for a list of available commands"
    exit 2
fi

flyway -user=$USER -password=$PASSWORD  -url=jdbc:mysql://$HOST:$PORT/$SCHEMA -locations=filesystem:$SCRIPT_DIR/migration -baselineOnMigrate=true -sqlMigrationSuffix=.sql $1
