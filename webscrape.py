from bs4 import BeautifulSoup as soup
import requests 
import pandas as pd
import re

INPUT_FILE = 'urls.csv'
OUTPUT_FILE = 'ScrapeResultsNewest.csv'

def read_file(input_file):
    """Read input file into a pandas DataFrame.

    Args:
        input_file (str): Name of .csv file to be loaded.

    Returns:
        DataFrame: As loaded from input file.
    """
    try:
        with open(input_file, 'r') as data_file:
            df = pd.read_csv(data_file)
            return df
    except:
        print('Error opening file.')


def get_page_contents(url):
    """Get BeautifulSoup object from url request.

    Args:
        url (str): Website request will be sent to.

    Returns:
        BeautifulSoup object: Content from requested url using 'lxml parser.
        OR
        None: If url is invalid or request times out.
    """
    try:
        result = requests.get(url, headers={'User-Agent': "Mozilla/5.0"}, timeout=10)
        # requests.get returns a response object with attributes and functions
        # to provide information about the request context, so that the server can tailor the response
        if result.status_code != 200:
            print('url.status_code: ', result.status_code, url)
            return None
        return soup(result.content, 'lxml') # markup, Lane Xang Minerals Limited
        # Content in bytes translated to lxml
        # When doc loaded to Beautiful Soup, it’s  converted to Unicode
    except:
        print('Error accessing urls from input_file')

def get_heading(soup_obj):
    """Scrape name of page from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.

    Returns:
        str: Holds name of page.
    """
    try:
        heading = soup_obj.find('h1',{'id':'HEADING'})
        return heading.text.strip()

    except:
        return ''


def get_num_reviews(soup_obj):
    """Scrape the number of customer reviews from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.

    Returns:
        str: Holds number of customer reviews.
    """
    try:
        num_review = soup_obj.find('span',{'class':'hkxYU q Wi z Wc'})
        reviews = num_review.text.strip()
        return reviews.split(' ')[0] # First element in list
    except:
        return ''

def get_avg_score(soup_obj):
    """Scrape the average customer hotel rating from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.

    Returns:
        str: Holds average customer hotel rating.
    """
    try:
        score = soup_obj.find('span',{'class':'uwJeR P'})
        return score.text.strip()
    except:
        return ''

def get_rating_type_count(soup_obj, review_filter):
    """Scrape the count of the review_filter rating type from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.
        review_filter (str): Text used to find a count of a specfic customer rating. (1,2,3,4,5)

    Returns:
        str: Holds count of specified customer rating type. Excellent, Very Good, Average, Poor, Terrible)
    """
    try:
        rating_container = soup_obj.find('input',{'id':review_filter})
        review_count = rating_container.find_next_sibling('span',{'class':'NLuQa'}) #Looking a few siblings away to match span and class
        return review_count.text.strip()
    except:
        return ''

def get_star_rating(soup_obj):
    """Scrape the hotel rating (independent of customer reviews) from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.

    Returns:
        str: Holds hotel rating, as in star rating. (1,2,3,4,5)
    """
    try:
        stars = soup_obj.find('span',{'class':'S2'})
        star_rate = stars.svg['aria-label']
        # svg: Scalable Vector Graphics (filled in stars out of 5)
        # SVG has several methods for drawing paths, boxes, circles, text, and graphic images

        s_rate = star_rate.strip()
        rate = s_rate.split(' ', 1)[0] 
        return rate
    except:
        return ''

def get_num_rooms(soup_obj):
    """Scrape the number of guest rooms from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.

    Returns:
        str: Holds number of guest rooms at that hotel.
    """
    try:
        number_rooms = soup_obj.find(text='NUMBER OF ROOMS').next_element
        return number_rooms.text.strip()
    except:
        return ''

def get_price(soup_obj, index):
    """Scrape a price from the passed object.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.
        index (int): Price is a range in a form such as: $227 - $387
            An index of 0 will reference the lower price.
            An index of 2 will reference the upper price.

    Returns:
        str: Holds price extreme requested based on index passed. Symbols have been trimmed.
    """
    try:
        price = soup_obj.find(text='PRICE RANGE').next_element
        indexed_price = price.text.split(' ')[index]
        trimmed_price = re.sub('[^0-9]','',indexed_price)
        return trimmed_price
    except: 
        return ''

def get_data_elements(soup_obj, url):
    """Find and extract data elements.

    Args:
        soup_obj (BeautifulSoup object): Object to scrape from.
        acct_name (str): Name of account to be added to dictionary.
        url (str): url to be added to dictionary.

    Returns:
        dict: Dictionary of account name, url, and all other data scraped from the site.
        OR
        None: If anything fails and the dictionary can't be constructed.
    """
    excel_review_filter = 'ReviewRatingFilter_5'
    very_good_review_filter = 'ReviewRatingFilter_4'
    average_review_filter = 'ReviewRatingFilter_3'
    poor_review_filter = 'ReviewRatingFilter_2'
    terrible_review_filter = 'ReviewRatingFilter_1'
    low_price_index = 0
    high_price_index = 2
    try: 
        return {
            "acct_name": get_heading(soup_obj),
            "url": url,
            "num_reviews": get_num_reviews(soup_obj),
            "avg_score": get_avg_score(soup_obj),
            "excellent_rating": get_rating_type_count(soup_obj, excel_review_filter),
            "very_good_rating": get_rating_type_count(soup_obj, very_good_review_filter),
            "average_rating": get_rating_type_count(soup_obj, average_review_filter),
            "poor_rating": get_rating_type_count(soup_obj, poor_review_filter),
            "terrible_rating": get_rating_type_count(soup_obj, terrible_review_filter),
            "star_rank": get_star_rating(soup_obj),
            "num_rooms": get_num_rooms(soup_obj),
            "low_price": get_price(soup_obj, low_price_index),
            "high_price": get_price(soup_obj, high_price_index)
        }
    except:
        return None

def create_hotel_dataframe(data):
    """Create DataFrame from column headings and list of dictionaries.

    Args:
        data (List): List of dictionaries with uniform lengths to load to DataFrame.

    Returns:
        DataFrame: All scraped data and column headings.
        OR
        None: If anything fails and the DataFrame can't be constructed.
    """
    try:
        column_headings = [
            'Account Name',
            'URL',
            'Total Number of Reviews',
            'Average Review Score',
            'Number of Excellent Reviews',
            'Number of Very Good Reviews',
            'Number of Average Reviews',
            'Number of Poor Reviews',
            'Number of Terrible Reviews',
            'Star Rating',
            'Number of Rooms',
            'Lower Price Range',
            'Higher Price Range']

        df = pd.DataFrame.from_records(data)
        df.columns = column_headings
        return df
    except:
        return None

def print_dataframe_to_csv(hotel_df):
    """Export DataFrame to .csv file.

    Args:
        hotel_df (DataFrame): DataFrame to export.

    Returns:
        None: Output file will be simply be created in .csv format.
    """
    hotel_df.to_csv(OUTPUT_FILE)

def main():
    """When module values for INPUT_FILE and OUTPUT_FILE are set, this file will scrape websites for defined data.
    
    This program is intended for TripAdvisor webpages  designed as of 10-27-2022.
    The INPUT_FILE is read into a pandas DataFrame. Iterations of each row of the DataFrame will extract the desired
    data and store it in a dictionary. As each dictionary is constructed, it is added to a list. This list of dictionaries
    is loaded into a DataFrame, which is then exported to a .csv file.

    """
    error=False
    data_elements = []
    try:
        df = read_file(INPUT_FILE)
        for index, row in df.iterrows():           
            soup_obj = get_page_contents(row['tripadvisor_url'])
            if soup_obj: # soup object returned as hoped
                element = get_data_elements(soup_obj, row['tripadvisor_url']) 
                if element: # dict returned as hoped
                    data_elements.append(element) # add dict to list
        if len(data_elements)> 0:
            hotel_df = create_hotel_dataframe(data_elements)
            print_dataframe_to_csv(hotel_df)

    except Exception as e: 
        print(e)
        error=True
    if error:
        err_msg = 'Error in main'
        print(err_msg)

"""For execution."""
if __name__ == "__main__":
    main()