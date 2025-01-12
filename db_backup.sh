#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Exiting."
  exit 1
fi

# Current date in YYYY-MM-DD-HHMMSS format for unique backup filenames
DATE=$(date +%F-%H%M%S)

# Backup directory on the host
BACKUP_DIR="/var/backups/database_backups/carwash"
mkdir -p $BACKUP_DIR

# Ensure required environment variables are set
: "${DB_HOST:?DB_HOST is not set in .env file}"
: "${DB_USER:?DB_USER is not set in .env file}"
: "${MYSQL_ROOT_PASSWORD:?MYSQL_ROOT_PASSWORD is not set in .env file}"
: "${DB_NAME:?DB_NAME is not set in .env file}"
: "${NETWORK:?NETWORK is not set in .env file}"
: "${MYSQL_IMAGE:?MYSQL_IMAGE is not set in .env file}"

# Backup filename
BACKUP_FILENAME="$BACKUP_DIR/$DB_NAME-$DATE.sql"

# Run mysqldump within a new Docker container
docker run --rm --network $NETWORK $MYSQL_IMAGE \
  /usr/bin/mysqldump -h $DB_HOST -u "root" -p$MYSQL_ROOT_PASSWORD $DB_NAME > $BACKUP_FILENAME

# Compress the backup file
gzip $BACKUP_FILENAME