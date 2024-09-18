#!/bin/bash

# Current date in YYYY-MM-DD-HHMMSS format for unique backup filenames
DATE=$(date +%F-%H%M%S)

# Backup directory on the host
BACKUP_DIR="/var/backups/database_backups"
mkdir -p $BACKUP_DIR

# Database credentials and details
DB_HOST="172.19.0.2"  # MySQL container IP address
DB_USER="testuser"
DB_PASSWORD="testpassword"
DB_NAME="testdb"
NETWORK="app-network"

# Docker image version of MySQL
MYSQL_IMAGE="mysql:8.0"

# Backup filename
BACKUP_FILENAME="$BACKUP_DIR/$DB_NAME-$DATE.sql"

# Run mysqldump within a new Docker container
docker run --rm --network $NETWORK $MYSQL_IMAGE \
  /usr/bin/mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILENAME

# Compress the backup file
gzip $BACKUP_FILENAME
