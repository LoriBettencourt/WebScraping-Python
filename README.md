# Data Analysis-Hotel Data

## Scenario
Take a list of urls and scrape information from each page on number of each type of review, average review, star rating, number of rooms, and price ranges. Use the scraped data to determine if there are any interesting findings.

## Analysis
Data analysis for the scraped data can be found at [DataAnalysis.docx](/DataAnalysis.docx)

## Process
I carefully examined the urls.csv file. Some of the URLs looked incomplete compared to the others, so I knew that was something to keep in mind. I inspected some TripAdvisor webpages and then did some research on which python library/tools would be best for this task. I looked at scrapy, requests, urllib, beautifulsoup, selenium, and pandas. (See ‘Findings on Python web-scraping tools – Summary’ below). Since it appeared by looking at TripAdvisor that I did not need to be concerned about JavaScript, I chose to use requests and beautifulsoup over selenium.

I started with a simple python script to begin trying to scrape information for just one of the pages. Almost immediately I realized that there was an issue because my requests were hanging up. I did a quick search and saw that some websites require some finessing because they have anti-scaping measures in place. Bot web scrapers are often detected because they  don’t define a user agent. I added ‘headers={'User-Agent': "Mozilla/5.0"}, timeout=10)’ to my requests.get call. 

Also, I wrote a quick script get the page information from one TripAdvisor page, prettified and wrote the html to a text file for reference. As I started writing code to scrape, I relied on this prettified file and on Chrome’s View/Developer/Inspect Elements to search for html tags. These resources helped me to write some skeletal code to get and store each of the 13 elements for my initial page.

Now that I had was familiar with the page HTML structure and had one site scraped, I performed a requests.get() for the complete list of URLs from the tripadvisor_data.csv file and received a 404 status code for almost half of the sites. I now recalled how so many of the URLs in the input file had inconsistent web addresses. 58 of the 100 URLs looked incomplete and 46 of them were causing the 404 error. Looking closer, most of the links in the format http://www.tripadvisor.com/ShowUserReviews-g946468-d597500 were bad links, and those working consistently looked like https://www.tripadvisor.com.ph/Hotel_Review-g295424-d1737457-Reviews-Grand_BelleVue-Dubai_Emirate_of_Dubai.html. Also, Waka Hotels and resorts had a longer URL with ‘ShowReviews’ in the string. Since this URL did not launch a valid account page, I manipulated the URL to the same format as the others I had modified (with and without the region) but these links failed to launch a valid Waka lodging account.

I had cleaned and trimmed the .csv data in Excel and confirmed there were no duplicates. Now I went about changing the strings for the web addresses.
•	Replaced ShowUserReviews with Hotel_Reviews  
•	Added ‘-Reviews-‘ after the string of numbers  
•	Changed spaces between the words in the account name to underscores and added this at the end of the above  
•	Finally, tacked ‘.html’ on the end   
Not all working links had a geographical location after the name, so this was worth a shot.
I saved the account names and updated URLs to a new .csv file. This eliminated all 404 status.codes and only 200s were returned. Still, some links were not valid for this analysis.  They led to restaurants, clubs, attractions, or were redirected to a different TripAdvisor page altogether. I checked to see if any of the links I modified worked before the modification but that was not the case. 18 URLs were deleted from the .csv input file used in my script, leaving 82 sites to be scraped.

I worked on scraping one element at a time with data from 10 websites. As I was able to get functionality consistent, I polished up the method I was using for the current element. When everything looked good for collecting that piece of data, I tested it on all 82.  I placed the results for this element in a dictionary.

I commented out the code for the previous element being scraped and repeated the process for the next to save time when running the script. When it came to star ratings and price ranges, some sites were missing values for these, and an empty string was placed in the corresponding dictionary value for that element. 

Once I had scraping functionality for all 13 pieces of data, I added 3 of the 13 dictionaries to a list, created column headings and a data frame for just these 3. I wrote the data frame output to my TripAdvisorScrapeResults.csv file. Once that was behaving as I hoped, I added all dictionaries to a list for the data frame and finalized my output file. I then opened it in Excel to get a visualization of the results. I went back over my code to comment and review my algorithms, styling, etc.

## Findings on Python web-scraping tools - Summary
*scrapy* - spiders; big-scale web scraping or automate multiple tests  
*requests* - fetch and clean well-organized API responses; lets you integrate your Python programs with web services  
*urllib* - more complicated than Requests but offers more control; able to open and parse information from HTTP or FTP protocols. Urllib offers some functionality to deal with and open URLs.  
* urllib.request: opens and reads URLs.
* urllib.error: catches the exceptions raised by urllib.request.
* urllib.parse: parses URLs.
* urllib.robotparser: parses robots.txt files.  

*beautifulsoup* - designed to make screen-scraping get done quickly; good for beginner; perfect choice for unstructured docs; difficult to maintain for large or growing projects.  
*selenium* - beginner-friendly; low learning curve; allows the code to mimic human behavior; extendable and flexible; excellent choice if you want to scrape a few pages, yet the information you need is within JavaScript.  
*pandas* - uses lxml html5lib beautifulsoup4; easy to scrape a table (<table> tag) on a web page and save as a DataFrame and do various processing and save it as an Excel file or csv file.

## Resources
[Choose the Best Python Web Scraping Library for Your Application](https://towardsdatascience.com/choose-the-best-python-web-scraping-library-for-your-application-91a68bc81c4f) (data scraping method selection)  
[How To Work with Web Data Using Requests and Beautiful Soup with Python 3](https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3)   
[Cannot Web Scraping Tripadvisor](https://stackoverflow.com/questions/71181932/cannot-web-scraping-tripadvisor) (addressing issues with scraping TripAdvisor)  
[Beautiful Soup Nested Tag Search](https://stackoverflow.com/questions/46510966/beautiful-soup-nested-tag-search) (handling nested tags you want to scrape)  
