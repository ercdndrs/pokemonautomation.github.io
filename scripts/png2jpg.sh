#!/bin/bash

# Check if argument provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <image.png>"
    exit 1
fi

# Get input file
input="$1"

# Check if file exists
if [ ! -f "$input" ]; then
    echo "Error: File '$input' not found"
    exit 1
fi

# Get basename without extension and create output filename
basename="${input%.png}"
output="${basename}.jpg"

# Convert using sips
sips -s format jpeg -s formatOptions 85 "$input" --out "$output"

# echo "Converted: $input -> $output"
