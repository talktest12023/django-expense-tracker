#!/bin/bash

echo "⏳ Backing up SQLite database..."

# Define variables
LOCAL_DB_PATH="/opt/render/project/src/db.sqlite3"  # Production database path
BACKUP_FOLDER="gdrive1:SQLiteBackups"  # Google Drive folder where backups are stored

# Generate a timestamped filename
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="backup_$TIMESTAMP.sqlite3"

# Copy database to backup file
cp $LOCAL_DB_PATH $BACKUP_NAME
echo "✅ Database copied successfully: $BACKUP_NAME"

# Upload backup to Google Drive
rclone copy $BACKUP_NAME $BACKUP_FOLDER

echo "✅ Backup uploaded to Google Drive: $BACKUP_NAME"

# Cleanup local copy
rm $BACKUP_NAME
