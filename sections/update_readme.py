# importing libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# ---------------------------------

def get_daily_papers(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize lists to store data
    data = {'Title': [], 'Paper_Link': [], 'Image': []}

    # Find all article elements
    articles = soup.find_all('article', class_ = "flex flex-col overflow-hidden rounded-xl border")

    # Iterate over each article
    for article in articles:
        # Extract image source if available
        img_tag = article.find('img')
        image = img_tag.get('src') if img_tag else None

        # Extract title text
        title = article.find('h3').text.strip()

        # Extract link
        link = "https://huggingface.co" + article.find('a').get('href')

        # Append data to lists
        data['Image'].append(image)
        data['Title'].append(title)
        data['Paper_Link'].append(link)

    df = pd.DataFrame(data)    
    return df

def update_readme(url):

    # Fetch today's date
    today_date = datetime.today().strftime('%d %b %Y')

    # Read existing README file
    with open(r'C:\Users\prana\Jupyter Codes\Project\Latest Papers\Notes\README.md', 'r', encoding='utf-8') as file:
        readme_content = file.read()

    upper_section, lower_section = readme_content.split('## Papers')

    # Append today's data to README content
    today_data = f"### {today_date}\n"

    # Create a DataFrame to store paper data
    df = get_daily_papers(url)

    # Add papers to today's data
    for index, row in df.iterrows():
        
        today_data += f"{index + 1}. [{row['Title']}]({row['Paper_Link']})\n"
    

    updated_readme = upper_section + "## Papers\n" + today_data + lower_section

    # Write back to README file
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_readme)




if __name__ == '__main__':
    url = 'https://huggingface.co/papers'
    update_readme(url)
    