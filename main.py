import sys
import re
import requests
from libgen_api import LibgenSearch
from rich import print
from rich.console import Console
from rich.table import Table
from rich.live import Live
from time import sleep

def search_book():
    print(
        "Welcome, [bold magenta]Don't forget to support the author if you enjoy the book[/bold magenta]!", ":books:", )
    
    # enter the title of the book
    book_name = input("Enter the title of the book: ")
    author_name = input("Enter the name of the author: ")
    year = input("Enter the release year: ")
    format = input("Enter the format of the book (epub, pdf) ")
    
    tf = LibgenSearch()
    title_filters = {'Author': author_name, 'Year': year, 'Extension': format}

    with Console().status("[bold green]Searching for" + " " + book_name + " " + "in the library...", spinner="monkey"):
        titles = tf.search_title_filtered(book_name, title_filters, exact_match=True)
    
    return titles

def download_book(titles):
    selected = input("Enter the ID of the book you want to download: ")
    # url from the book [link] is https://libgen.io/harrypotter/sd342334553234.epub
    found = False
    for title in titles:
        if selected == title['ID']:
            link_list = [title['Mirror_1'], title['Mirror_2'], title['Mirror_3'], title['Mirror_4']]
            found = True
    
    if not found:
        print("[bold red]Invalid book ID!")
        return
    
    for link in link_list:
        # foreach link in the linkList test the url
        try:
            r = requests.head(link)
            if r.status_code == 200:
                print("[bold green]Downloading the book...", ":books:")
                # loading animation
                with Console().status("[bold green]Searching for" + " " + title['Title'] + " " + "in the library...", spinner="monkey"):
                    pass
                print("[bold green]Downloading to: " + "./" + title['Title'] + "." + title['Extension'])
                r = requests.get(link)
                # automatically search for the download link

                # inside the link search for the link to download the book

                with open(title['Title'] + "." + title['Extension'], 'wb') as f:
                    f.write(r.content)
                print("[bold green]Download complete!", ":thumbs_up:")
                break
        except requests.exceptions.RequestException as e:
            print("[bold red]Download failed!")
            print("Error: " + str(e))
            continue

def main():
    titles = search_book()
    
    table = Table(show_header=True, header_
