import os
import requests
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse


def clean_url(url):
    """
    Removes the 'page=' parameter from a URL if it exists.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['page'] = ['1']  # Ensure the page parameter starts at 1
    new_query = urlencode(query_params, doseq=True)
    cleaned_url = parsed_url._replace(query=new_query)
    return urlunparse(cleaned_url)


def update_page_number(url, page_number):
    """
    Updates the 'page=' parameter in the URL to the specified page number.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['page'] = [str(page_number)]
    new_query = urlencode(query_params, doseq=True)
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)


def get_image_hash(image_url, headers):
    """
    Downloads an image and returns the MD5 hash of the image content.
    """
    try:
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()

        # Compute hash of the content
        image_hash = md5()
        for chunk in response.iter_content(1024):
            image_hash.update(chunk)

        return image_hash.hexdigest()
    
    except Exception as e:
        print(f"Failed to fetch image for hashing: {image_url} ({e})")
        return None


def save_image(image_url, output_dir, headers, seen_images_hashes):
    """
    Downloads and saves an image from a given URL.
    Checks if the image content is already downloaded using hashes.
    """
    try:
        image_hash = get_image_hash(image_url, headers)
        if image_hash is None:
            return

        # If the hash already exists, skip saving the image
        if image_hash in seen_images_hashes:
            print(f"Image already saved (duplicate content): {image_url}")
            return

        # Save the image content if it's unique
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()

        # Generate a unique filename using the hash
        filename = os.path.join(output_dir, f"{image_hash}.jpg")
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Saved image: {filename}")
        seen_images_hashes.add(image_hash)  # Track this image's hash
    
    except Exception as e:
        print(f"Failed to save image {image_url}: {e}")


def crawl_and_save_images(url, output_dir, headers, seen_images_hashes):
    """
    Crawls a URL, extracts image URLs, and saves them locally.
    It also tracks seen images by their content hash to avoid duplicates.
    """
    new_images_found = False
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            img_url = img.get('src')
            if img_url:
                # Handle relative URLs
                if not img_url.startswith(('http://', 'https://')):
                    img_url = requests.compat.urljoin(url, img_url)
                save_image(img_url, output_dir, headers, seen_images_hashes)
                new_images_found = True
        
        return new_images_found
    except Exception as e:
        print(f"Failed to crawl URL {url}: {e}")
        return False


def crawl_all_pages(base_url, output_dir, headers):
    """
    Iterates through all pages starting from the base URL and downloads images.
    Stops when no new images are found (non-repeating images).
    """
    page_number = 1
    seen_images_hashes = set()  # To keep track of unique image content hashes

    while True:
        current_url = update_page_number(base_url, page_number)
        print(f"Crawling URL: {current_url}")
        images_found = crawl_and_save_images(current_url, output_dir, headers, seen_images_hashes)

        if not images_found:
            print(f"No new images found on page {page_number}. Stopping.")
            break

        page_number += 1


def main():
    input_file = 'f.txt'
    output_dir = 'images'

    # User-Agent header to bypass access restrictions
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read URLs from the input file
    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return

    # Process each URL
    for url in urls:
        url = url.strip()
        if not url:
            continue
        cleaned_url = clean_url(url)
        print(f"Starting crawl for: {cleaned_url}")
        crawl_all_pages(cleaned_url, output_dir, headers)


if __name__ == '__main__':
    main()
