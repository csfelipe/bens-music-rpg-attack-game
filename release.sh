#!/bin/bash

# Check if version argument is provided
if [ -z "$1" ]; then
    # No version provided, bump minor version
    CURRENT_VERSION=$(cat version | tr -d '[:space:]')
    IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
    MAJOR=${VERSION_PARTS[0]}
    MINOR=${VERSION_PARTS[1]}
    PATCH=${VERSION_PARTS[2]}
    NEW_MINOR=$((MINOR + 1))
    RELEASE_VERSION="${MAJOR}.${NEW_MINOR}.0"
    echo "No version provided, bumping minor version: ${CURRENT_VERSION} -> ${RELEASE_VERSION}"
else
    # Use provided version
    RELEASE_VERSION="$1"
fi

# Get current date/time in ISO format
RELEASE_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S")
RELEASE_DATE_PST=$(TZ='America/Los_Angeles' date +"%Y-%m-%dT%H:%M:%S PST")

# Update version file
echo "$RELEASE_VERSION" > version

# Add release entry to the top of release_history
{
    echo "${RELEASE_VERSION} - ${RELEASE_DATE}"
    cat release_history
} > release_history.tmp && mv release_history.tmp release_history

# Stage the changes
git add .

# Create commit
COMMIT_MESSAGE="Release v${RELEASE_VERSION} - ${RELEASE_DATE_PST}"
git commit -m "$COMMIT_MESSAGE"

# Push to main
git push origin main

echo "Release v${RELEASE_VERSION} completed successfully!"

