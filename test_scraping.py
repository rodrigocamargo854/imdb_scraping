from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import csv

url = "https://www.imdb.com/chart/top?ref_=nv_mv_250"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
request = Request(url, headers=headers)
page = urlopen(request)
html = BeautifulSoup(page.read(), "html.parser")

# Assuming the parent element contains all the required details
parent_elements = html.find_all("div", {"class": "ipc-metadata-list-summary-item sc-59b6048d-0 jemTre cli-parent"})

regexMovieYear = re.compile('(\d{4})')
regexUserRating = re.compile('\ ((\d{1,3})((\,|\.)\d{1,3})*)')

data = []

for element in parent_elements:
    movieTitle = element.find("a").text
    movieYear = re.search(regexMovieYear, element.find("span").text).group(0)
    
    rating_element = element.find(attrs={"aria-label": re.compile(r"IMDb rating:")})
    if rating_element:
        imdbRating = re.search(r"IMDb rating: (\d+\.\d+)", rating_element['aria-label']).group(1)
    else:
        imdbRating = "N/A"
    
    userRating_element = element.find("strong")
    if userRating_element:
        userRating = re.search(regexUserRating, userRating_element['title']).group(0)
    else:
        userRating = "N/A"
    
    print(movieTitle, movieYear, imdbRating, userRating)
    data.append([movieTitle, movieYear, imdbRating, userRating])

csvFilename = 'IMDTOP250.csv'

with open(csvFilename, 'w') as csvfile:
    fileWriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    fileWriter.writerow(['TITLE', 'YEAR', 'IMDB RATING', 'USER RATINGs'])
    
    for row in data:
        fileWriter.writerow(row)

    print('Arquivo', csvFilename, 'gerado com sucesso!')
