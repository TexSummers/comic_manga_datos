import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.71 Safari/537.36'}

detail_link = []
manga_list = []
description_list = []


def getProducts(tag, limit, page):
    # A string that starts with "f" (formatted string literals) lets you write a Python expression between '{' and
    # '}' characters that can refer to variables or literal values.
    url = f"https://www.ovnipress.net/{tag}/?sort_by=created-descending&results_only=true&limit={limit}&page={page}&results_only=true"

    r = requests.get(url, headers=headers)

    # Should give 200
    # print(r.status_code)

    soup = BeautifulSoup(r.text, 'html.parser')

    # Prints page source code, can add extra stuff
    # print(soup)
    # print(soup.title.text)

    # Find every instance of the following element
    products = soup.find_all('div', {'class': 'item'})

    # Print the amount of the elements you want to find (recommended for testing)
    # print(len(mangas))

    # For loop used to find every instance of the desired element in the page
    for item in products:
        price = item.find('div', {'class': 'js-price-display price item-price'}).text
        title = item.find('h2', {'class': 'js-item-name item-name'}).text
        link = item.find('a')['href']
        # Creates a dictionary with keys and values
        manga_dict = {
            'Product': tag.title(),
            # variable = item.find(tag, {'attribute': 'attr_name'}).text (the ".text" shows you only the text part
            # after the attribute)
            'Title': title.title(),
            # Remove all unnecessary substrings from "price"
            'Price': int(price.replace("$", "").replace("\n", "").replace(" ", "").replace(".", "")),
            # You can add attributes from your element in square brackets
            # Won't use this image because it's too small
            # 'Image Url': item.find('img')['src'],
        }
        detail_link.append(link)
        # Print all of the titles, prices, image_urls
        # print(title + " || " + str(price_int) + " || " + img_url)
        # print(manga_dict)
        # Append our dictionary to a list for further use
        manga_list.append(manga_dict)

    for i in detail_link:
        url2 = i
        r2 = requests.get(url2, headers=headers)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        products2 = soup2.find_all('div', {'class': 'js-main-content main-content'})
        for item in products2:
            description = item.find('div', {'class': 'description user-content m-top'}).get_text()
            desc2 = (description[:description.index("ISBN")])
            img_url = item.find('a', {'class': 'js-desktop-zoom cloud-zoom'})['href']
            isbn = (description[description.index("ISBN"):]).replace(" ", "").replace("\n", "").replace("ISBN:", "")
            description_dict = {
                'Description': desc2,
                'Image Url': img_url,
                'ISBN': isbn,
            }
            description_list.append(description_dict)


# A for loop can be used to replace the function parameters
# for x in range(0, 2):
#    getProducts("manga", 3, x)

getProducts("manga", 3, 1)


# Merge two dictionaries with pandas
df1 = pd.DataFrame(manga_list)
df2 = pd.DataFrame(description_list)
df = df1.merge(df2, left_index=True, right_index=True)
df.to_excel('productlist.xlsx')
print("Done.")

