from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
# print(excel.sheetnames)
sheet = excel.active
sheet.title = 'Top Rated Movies'
print(excel.sheetnames)
sheet.append(['Movie Rank', 'Movie Name', 'Year of Release', 'IMDB Ratings'])

try:
    source = requests.get('https://www.imdb.com/chart/top/')
    source.raise_for_status()
    
    soup = BeautifulSoup(source.text,'html.parser')
    ## print(soup.encode("utf-8")) ##
    movies = soup.find('tbody',class_="lister-list").find_all('tr')
    # print(len(movies))
    # print(movies)
    
    for movie in movies:
        
        # print(movie)
        
        name = movie.find('td', class_="titleColumn").a.text
        # print(name)
        
        rank = movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
        # print(rank)
        
        year = movie.find('td', class_="titleColumn").span.text.strip('( )')
        # print(year)
        
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text
        # print(rating)
        
        print(rank,name,year,rating)
        sheet.append([ rank,name,year,rating ])
        # break
    
except Exception as e:
    print(e)
    
excel.save('IMDB Movie Rating.xlsx')