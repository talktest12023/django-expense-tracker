#!/bin/bash

echo "⏳ Restoring SQLite database from Google Drive..."

# Define variables
BACKUP_FOLDER="gdrive1:SQLiteBackups"  # Google Drive folder where backups are stored
LOCAL_DB_PATH="/opt/render/project/src/db.sqlite3"  # SQLite path in Render

# Find the latest backup in Google Drive
LATEST_BACKUP=$(rclone lsf $BACKUP_FOLDER | sort | tail -n 1)

# Check if backup exists
if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ No backup found!"
    exit 1
fi

echo "✅ Latest backup found: $LATEST_BACKUP"

# Download the latest backup to Render's database path
rclone copy "$BACKUP_FOLDER/$LATEST_BACKUP" "/opt/render/project/src"

echo "✅ Database restored successfully!"
