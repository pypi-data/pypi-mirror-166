# scrapeTiger

scrapeTiger is an python package for web scraping. 

* `requires-python = ">=3.7"`

# example of scraping multiple page
```
from scrapeTiger import multi_page,details_page

multi_page(url="https://quotes.toscrape.com/page/",start_page=1,end_page=3,css_selector= ".quote span a")

details_page(field_one_css='.author-title')
```

Let explain how this two function working. First we are scraping link of each items from page 1 to page 2 with the help of multi_page function then we are scraping author name from datils page of each item with the help of details_page function.  

# example of scraping single page
```
from scrapeTiger import single_page,details_page

single_page(url="https://quotes.toscrape.com/",css_selector= ".quote span a")

details_page(field_one_css='.author-title')
```

# How to install

`pip install scrapeTiger`

# dependency packages
install selenium and webdriver-manager for run this package properly.

* `pip install selenium`
* `pip install webdriver-manager`

# Output Result
___

It will generate csv file after scraping.

# multi_page 

`multi_page(url,start_page,end_page,css_selector,wait_second=2)`
* url (string, required)
* start_page(integer, required) 
* end_page(integer, required)
* css_selector(string, required)
* wait_second(integer, optional)  
defult 2 second


# single_page
 `single_page(url,css_selector,wait_second=2)`

* url (string, required)
* css_selector(string, required)
* wait_second(integer, optional)


# details_page
___
 `
 details_page(wait_second=2,field_one_css=None,field_one_html=False,main_image_css=None,img_attribute='src',gallary_image_css=None,gallary_image_attribute='src',header_added=False)
 `

 * wait_second(integer, optional)  
 defult 2 second
  
 * field_one_css(string, optional)
 * field_one_html(boolean, optional)
  
   defult flase. If you want to get html then make it true otherwise you will get text value.
* You can aslo use field_two_css,field_three_css,field_four_css same like field_one_css.

* You can aslo use field_two_html, field_three_html,field_four_html same like field_one_html.

* maximum four fields 

* main_image_css(string, optional)

* img_attribute(string, optional)
  
  defult img_attribute is `src` for main_image_css. 

* gallary_image_css(string, optional)

* gallary_image_attribute(string, optional)

   defult img_attribute is `src` for gallary_image_css. 

* header_added(boolean, optional)

  defult flase. If you don't want to write csv header then make to true.

* details_page() function support maximum four fields.
 example: `details_page(field_one_css=None,field_one_html=False,field_two_css=None,field_two_html=False,field_three_css=None,field_three_html=False,field_four_css=None,field_four_html=False,)`





[Github link](https://github.com/MDFARHYN/scrapeTiger)

[report issue](https://github.com/MDFARHYN/scrapeTiger/issues)






