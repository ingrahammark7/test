from bs4 import BeautifulSoup

# Paths to input and output files
input_file = "your_file.html"
output_file = "extracted_links.txt"

# Read and parse the file
with open(input_file, "r", encoding="ascii", errors="ignore") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract links
links = [a.get("href") for a in soup.find_all("a", href=True)]

# Save to a text file
with open(output_file, "w", encoding="ascii") as file:
    for link in links:
        file.write(link + "\n")


# Path to the extracted links file
input_file_path = "extracted_links.txt"
output_file_path = "cleaned_links.txt"

# Read the links from the file
with open(input_file_path, "r", encoding="ascii") as file:
    links = file.readlines()

# Clean URLs by removing Google tracking and extra parameters
cleaned_links = []
for link in links:
    # Remove the Google tracking part
    if link.startswith("https://www.google.com/url?q="):
        link = link.split("https://www.google.com/url?q=")[-1]  # Remove prefix
        link = link.split("&")[0]  # Remove any trailing parameters like "&usg="
    cleaned_links.append(link.strip())

# Write the cleaned links to a new file
with open(output_file_path, "w", encoding="utf-8") as file:
    for link in cleaned_links:
        file.write(link + "\n")

print(f"Cleaned links have been saved to {output_file_path}")
