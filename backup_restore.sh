#!/bin/bash

# Define backup file location
BACKUP_DIR="/var/sqlite_backup"
BACKUP_FILE="$BACKUP_DIR/db_backup.sqlite3"
DB_FILE="/var/db.sqlite3"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

# Backup existing database before deployment
if [ -f "$DB_FILE" ]; then
    cp $DB_FILE $BACKUP_FILE
    echo "✅ Backup created: $BACKUP_FILE"
fi

# Restore database after deployment
if [ -f "$BACKUP_FILE" ]; then
    cp $BACKUP_FILE $DB_FILE
    echo "✅ Database restored from backup!"
fi
