import requests
from bs4 import BeautifulSoup
import numpy as np

#Retrieve data from Google Doc

def retrieve_google_doc_data(url:str):
    # Validate URL
    if "docs.google.com/document/d" not in url:
        raise ValueError("The provided URL is not a valid Google Doc URL")

    try:
        #GET request
        response = requests.get(url)

        #exception if response unsuccessful
        response.raise_for_status()

        #parse document using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        #Extract text content
        document_content = soup.find('body').get_text(separator='\n')

        return document_content.strip()
    
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"An error occured while retrieving the document: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occured: {e}")

#Test

google_doc_url = 'https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub'
google_doc_content = retrieve_google_doc_data(google_doc_url)

# Create array from content
def create_array_from_content(content):
    numpy_arr = np.array((content).split('\n'))
    content_arr = numpy_arr.tolist()
    # Remove non-coordinate entries
    content_arr = [i for i in content_arr if len(i) <= 1 or i.isdigit()]
    return content_arr

content_arr = create_array_from_content(google_doc_content)

# Separate coordinates and unicodes
def separate_coordinates_and_unicodes(content_arr):
    coordinates = []
    unicodes = []
    for item in content_arr:
        if len(item) == 1 and item.isdigit():
            coordinates.append(int(item))
        elif len(item) == 1:
            unicodes.append(item)
        else:
            try:
                coord = int(item)
                coordinates.append(coord)
            except ValueError:
                continue
    coordinate_pairs = [coordinates[i:i+2] for i in range(0, len(coordinates), 2)]
    return coordinate_pairs, unicodes

coordinates, unicodes = separate_coordinates_and_unicodes(content_arr)
#print(coordinates)
#print(unicodes)


def draw_coordinates_on_grid(coordinates, unicodes):
    # Find grid size
    max_row = 0
    max_col = 0
    for pair in coordinates:
        if len(pair) == 2:
            col, row = pair 
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
    
    # Create grid
    grid = [[' ' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
    #print(max_col, max_row)

    for idx, pair in enumerate(coordinates):
        if len(pair) == 2 and idx < len(unicodes):
            col, row = pair  
            grid[row][col] = unicodes[idx] if idx < len(unicodes) else ' '

    # Print the grid
    i = len(grid)
    while i > 0:
        print(''.join(grid[i-1]))
        i -= 1

draw_coordinates_on_grid(coordinates, unicodes)