LOCAL_USER=${MYSQL_USERNAME:='root'}
LOCAL_PASSWORD=${MYSQL_PASSWORD:=''}
LOCAL_HOST=${MYSQL_HOST:='localhost'}
LOCAL_PORT=${MYSQL_PORT:='3306'}

STAGING_USER=$STAGING_MYSQL_USERNAME
STAGING_PASSWORD=$STAGING_MYSQL_PASSWORD

SCHEMA='conversationIM'

LOCAL_CONNECTION="jdbc:mysql://${LOCAL_HOST}:${LOCAL_PORT}/${SCHEMA}"
STAGING_CONNECTION="jdbc:mysql://localhost:3306/${SCHEMA}"

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
  read -r -p "Is port-forwarding enabled? [y/N] " response
  case $response in
    [yY][eE][sS]|[yY]) 
        flyway -user=$STAGING_USER -password=$STAGING_PASSWORD -url=$STAGING_CONNECTION -locations=filesystem:$SCRIPT_DIR/migration -baselineOnMigrate=true -sqlMigrationSuffix=.sql $1
        ;;
    *)
        echo "Run 'rhc port-forward staging'"
  esac
else
	echo "The requested target ($2) is not a valid"
fi
