import requests
from bs4 import BeautifulSoup
import json


def replace_html_entities(in_str):
    out_str = in_str
    out_str = out_str.replace("-", "%2D")
    out_str = out_str.replace(" ",  "%20")
    return out_str


def get_category_members(category):

    cat = replace_html_entities(category)

    url = "http://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmlimit=500&cmtitle=" \
        "Category:" + cat + "&format=json"
    page = requests.get(url)

    page_json = json.loads(page.content)

    formatted_page_json = json.dumps(page_json, indent=2)

    print(formatted_page_json)

    # cat_members = page_json["query"]["categorymembers"]

    # print(len(cat_members))

    # for mem in cat_members:
    #     print(mem["title"])


def get_cast_data():

    title = "Drishyam"

    url = "https://en.wikipedia.org/w/api.php?action=parse&page=" + title + \
          "&formatversion=2&format=json"

    page = requests.get(url)

    page_json = json.loads(page.content)

    formatted_page_json = json.dumps(page_json, indent=2)

    #soup = BeautifulSoup(page.content, "html.parser")

    # html = list(soup.children)[2]
    # body = list(html.children)[3]
    # print(page_json["parse"]["text"])
    page_text = page_json["parse"]["text"]
    soup = BeautifulSoup(page_text, "html.parser")

    cast_span = soup.find("span", id="Cast")
    cast_ul = soup.find("span", id="Cast").findNext("ul")
    cast_lis = list(cast_ul.find_all("li"))
#   print(cast_lis)

    for cast_li in cast_lis:
        print(extract_cast_json(cast_li))


def extract_cast_json(cast_item):

    cast_item_dict = {}
    cast_a = cast_item.find("a", href=True)

    if cast_a is not None:
        cast_item_dict["link"] = cast_a["href"]
        cast_item_dict["name"] = cast_a.contents[0]
        cast_item_dict["additional_text"] = cast_item.contents[1]
    else:
        cast_item_dict["link"] = None
        cast_item_contents = cast_item.contents[0]

        pos_as = cast_item_contents.find("as")

        if pos_as != -1:
            cast_item_dict["name"] = cast_item_contents[:pos_as - 1]
            cast_item_dict["additional_text"] = cast_item_contents[pos_as + 3:]
        else:
            cast_item_dict["name"] = cast_item.contents[0]
            cast_item_dict["additional_text"] = None

    return cast_item_dict


# get_category_members("Malayalam-language films")
get_cast_data()

