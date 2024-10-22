#!/bin/bash

# Define source and destination directories
SOURCE_DIR="/home/mahendra/Downloads/resume_corpus-master/resumes_corpus"
DEST_DIR="/home/mahendra/PycharmProjects/ProjectResume/Dataset/independent/"

# Check if the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Source directory does not exist."
  exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy up to 10 .txt files from the source to the destination directory
count=0
for file in "$SOURCE_DIR"/*.txt; do
  # Check if there are any .txt files
  if [ -e "$file" ]; then
    cp "$file" "$DEST_DIR"
    ((count++))
  fi
  
  # Break if we've copied 10 files
  if [ "$count" -ge 10 ]; then
    break
  fi
done

echo "Copied $count .txt files from $SOURCE_DIR to $DEST_DIR."
