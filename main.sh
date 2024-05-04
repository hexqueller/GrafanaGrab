#!/bin/bash

# Check if config.ini exists and source it
if [ ! -f config.ini ]; then
    echo "config.ini not found!"
    exit 1
fi

# Read config.ini
URL=$(awk -F '=' '/url/{print $2}' config.ini)
KEY=$(awk -F '=' '/key/{print $2}' config.ini)
SAVE=$(awk -F '=' '/save/{print $2}' config.ini)

# Check if URL and KEY are set
if [ -z "$URL" ]; then
    echo "URL is not set in config.ini"
    exit 1
fi

if [ -z "$KEY" ]; then
    echo "KEY is not set in config.ini"
    exit 1
fi

# Create output folder
OUTPUT_FOLDER="/tmp/dashboards"
mkdir -p "$OUTPUT_FOLDER"

# Get dashboards
RESPONSE=$(curl -s -H "$HEADERS" -w "%{http_code}" -o /dev/null "$URL/api/search" -X GET)
if [ "$RESPONSE" != "200" ]; then
    echo "Failed to get dashboards: HTTP status code $RESPONSE"
    exit 1
fi

# Loop through dashboards and export them
UIDS=$(echo $RESPONSE | jq -r '.[] | .uid')
ERROR_COUNT=0
for DASHBOARD in $UIDS; do
    RESPONSE=$(curl -s -H "$HEADERS" "$URL/api/dashboards/uid/$DASHBOARD")
    if [ "$(echo $RESPONSE | jq -r '.status')" != "success" ]; then
        echo "Failed to export dashboard: $(echo $RESPONSE | jq -r '.message')"
        ERROR_COUNT=$((ERROR_COUNT+1))
        continue
    fi
    TITLE=$(echo $RESPONSE | jq -r '.dashboard.title')
    if [ -z "$TITLE" ]; then
        TITLE="dashboard"
        echo "Failed to get title for dashboard $DASHBOARD. Using default title."
    fi
    FILENAME="dashboard_$TITLE.json"
    echo $RESPONSE | jq -r '.dashboard | del(.id, .meta)' > "$OUTPUT_FOLDER/$FILENAME"
    echo "Dashboard $DASHBOARD successfully exported as $FILENAME."
done

echo -e "\nDashboards successfully exported!\nSuccessful: $(($UIDS-ERROR_COUNT))\nErrors: $ERROR_COUNT"

# Create archive
SCRIPT_DIR=$(dirname "$(realpath "$0")")
DATE_FORMAT=$(date +"%d-%m-%Y")
ARCHIVE_NAME="dashboards_$DATE_FORMAT.tar.gz"
if [ -z "$SAVE" ]; then
    SAVE="$SCRIPT_DIR/$ARCHIVE_NAME"
else
    SAVE="$SAVE/$ARCHIVE_NAME"
fi
tar -czf "$SAVE" -C "$OUTPUT_FOLDER" .
echo -e "\nArchive $SAVE successfully created."

# Clean up
rm -rf "$OUTPUT_FOLDER"
echo "Cleanup completed!"
