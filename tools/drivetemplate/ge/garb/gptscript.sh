#!/bin/bash

# Path to the cleaned links file
input_file="cleaned_links.txt"

# Directory to save downloaded content
download_dir="downloaded_content"

# File to keep track of already crawled URLs
crawled_file="crawled_links.txt"

# Create the download directory if it doesn't exist
mkdir -p "$download_dir"

# Create the crawled_links.txt file if it doesn't exist
touch "$crawled_file"

# Loop through each URL in the cleaned_links.txt file
while IFS= read -r url; do
    # Check if the URL is not empty and does not contain "google.com"
    if [ -n "$url" ] && [[ ! "$url" =~ google\.com ]]; then
        # Check if the URL has already been crawled
        if grep -Fxq "$url" "$crawled_file"; then
            echo "Skipping $url (already crawled)"
        else
            # Sanitize the URL by replacing '?' with '_'
            sanitized_url=$(echo "$url" | sed 's/[?&=]/_/g')
            
            # Download the content with the sanitized URL
            echo "Downloading content from $sanitized_url..."

            # wget --user-agent="foo" --restrict-file-names=windows --adjust-extension -i in.txt
            
            wget2 --restrict-file-names=windows \
                 --adjust-extension \
                 --recursive \
                 --no-parent \
                 --wait=1 \
                 --limit-rate=100k \
                 --directory-prefix="$download_dir" \
                 "$url"
            
            # After downloading, add the URL to the crawled list
            echo "$url" >> "$crawled_file"
        fi
    else
        echo "Skipping $url (Google link)"
    fi
done < "$input_file"

echo "Download completed. All content saved in $download_dir."
