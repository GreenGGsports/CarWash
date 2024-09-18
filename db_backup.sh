#!/bin/bash

# Current date in YYYY-MM-DD-HHMMSS format for unique backup filenames
DATE=$(date +%F-%H%M%S)

# Backup directory on the host
BACKUP_DIR="/var/backups/database_backups"
mkdir -p $BACKUP_DIR

# Database credentials and details
DB_HOST="db"  # Docker service name of the MySQL container in your Compose file
DB_USER="testuser"  # From the Compose file
DB_PASSWORD="testpassword"  # From the Compose file
DB_NAME="testdb"  # From the Compose file
NETWORK="app-network"  # Custom network defined in the Compose file

# Docker image version of MySQL
MYSQL_IMAGE="mysql:8.0"

# Backup filename
BACKUP_FILENAME="$BACKUP_DIR/$DB_NAME-$DATE.sql"

# Run mysqldump within a new Docker container
docker run --rm --network $NETWORK $MYSQL_IMAGE \
  /usr/bin/mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILENAME

# Compress the backup file
gzip $BACKUP_FILENAME
