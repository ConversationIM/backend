LOCAL_USER=${MYSQL_USERNAME:='root'}
LOCAL_PASSWORD=${MYSQL_PASSWORD:=''}
LOCAL_HOST=${MYSQL_HOST:='localhost'}
LOCAL_PORT=${MYSQL_PORT:='3306'}
LOCAL_SCHEMA='conversationIM'

STAGING_USER=$OPENSHIFT_MYSQL_DB_USERNAME
STAGING_PASSWORD=$OPENSHIFT_MYSQL_DB_PASSWORD
STAGING_SCHEMA='staging'

LOCAL_CONNECTION="jdbc:mysql://${LOCAL_HOST}:${LOCAL_PORT}/${LOCAL_SCHEMA}"
STAGING_CONNECTION="jdbc:${OPENSHIFT_MYSQL_DB_URL}${STAGING_SCHEMA}"

SCRIPT_DIR=$(dirname $0)

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <flyway command> <target>"
    echo "Type 'flyway' for a list of available commands"
    echo "Available targets are 'local' and 'staging'"
    exit 2
fi

if [ "$2" = "local" ]; then
	flyway -user=$LOCAL_USER -password=$LOCAL_PASSWORD -url=$LOCAL_CONNECTION -locations=filesystem:$SCRIPT_DIR/migration -baselineOnMigrate=true -sqlMigrationSuffix=.sql $1
elif [ "$2" = "staging" ]; then
    if [ -z $STAGING_USER]; then
      echo "The requested target ($2) is not available"
      exit 2
    fi
	flyway -user=$STAGING_USER -password=$STAGING_PASSWORD -url=$STAGING_CONNECTION -locations=filesystem:$SCRIPT_DIR/migration -baselineOnMigrate=true -sqlMigrationSuffix=.sql $1
else
	echo "The requested target ($2) is not a valid"
fi
