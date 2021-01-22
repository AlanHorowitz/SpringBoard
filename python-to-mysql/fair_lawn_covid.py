from bs4 import BeautifulSoup
import requests

def print_fl_covid_info():
    '''
    Read the www.fairlawn.org website for current active covid counts.
    Prints:
        Current Active Cases:
        Last Update date:
    or
        Error message if not able to parse the website
    '''
    fl_url = 'https://www.fairlawn.org/'
    resp = requests.get(fl_url)
    soup = BeautifulSoup(resp.text, features='lxml')

    # Find an <a> tag with href ending with covidupdates or with contents of 
    # "Corona Virus Alerts"
    a_tags = soup.find_all('a')
    href = ""
    for tag in a_tags:
        if tag.get('href'):
            if tag['href'].endswith('covidupdates'):
                href = tag['href']
                break
            elif tag.string == 'Corona Virus Alert':
                href = tag['href']
                
    if href != "":
        if href.startswith('http'):
            covid_url = href
        else:
            covid_url = fl_url + href
    else:
        print("Error: Couldn't find covid update link")
        return

    # read the covid info page
    resp = requests.get(covid_url)
    soup = BeautifulSoup(resp.text, features='lxml')

    marker_string = "Fair Lawn currently has"

    # Find the <P> with child content starting with the marker string.
    # Should be exactly one.
    p_tags = soup.find_all('p')
    p_children_tags = [p.contents for p in p_tags 
            if [ch for ch in p.children if str(ch).startswith(marker_string)]]

    if len(p_children_tags) != 1:
        if len(p_children_tags) == 0:
            print("No paragraphs found with marker string")
        else:
            print("found duplicate paragraphs with marker string")
        return

    # Data of interest is in the two <strong> tags.
    strong_tags = [s for s in p_children_tags[0] if s.name == 'strong']
    if len(strong_tags) != 2:
        print("Format of parargaph not as expected")
    else:
        print("Current Active Cases:", strong_tags[0].string.split()[1])
        print("Last Update date:", " ".join(strong_tags[1].string.split()[3:]))
    return

if __name__ == '__main__':
    print('+'*45)
    print_fl_covid_info()
    print('+'*45)



