from bs4 import BeautifulSoup
import requests
import csv

page = 'https://www.startech.com.bd/component/graphics-card'
csv_file = open('graphics_card_list_startech.csv', 'w',newline='', encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Description', 'Price', 'Status', 'video_link'])

while(page):

  fake_user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
  headers = {'User-Agent': fake_user }

  r = requests.get(page, headers, timeout=2).text
  soup = BeautifulSoup(r, 'lxml')

  for item in soup.find_all('div', class_='p-item'):
    name = item.h4.text.strip()
    link = item.h4.a.attrs['href']

    description = ""
    for des in item.find_all('li'):
      description = description + des.text +". "

    price = item.find("div", class_="p-item-price").span.text.replace("৳", "")
    if price == "0":
      price = "Not Set"

    status = item.find('div', class_='actions').span.text
    if(status == "shopping_cart Buy Now"):
      status = "Available"

    print(name)
    print(link)
    print(description)
    print(price)
    print(status)
    print("-------------------------------")

    csv_writer.writerow([name, description.strip() , price.strip(), status.strip(), link.strip()])

  pages = soup.find('ul', class_='pagination')
  try:
    page = pages.find(text = 'NEXT').parent.attrs['href']
  except Exception as e:
    page = None
csv_file.close()