from libgen_api import LibgenSearch
from rich import print
from rich.console import Console
from rich.table import Table
from rich.live import Live
from time import sleep
import sys
import requests
import re


console = Console()
bookList = []
linkList = []


def searchBook():
    print(
        "Welcome, [bold magenta]Don't forget to support the author if you enjoy the book[/bold magenta]!", ":books:", )
    # search_title()
    # enter the title of the book
    bookName = input("Enter the title of the book: ")
    Year = input("Enter the release year: ")
    Format = input("Enter the format of the book (epub, pdf) ")
    # format is global variable

    console.clear()

    tf = LibgenSearch()
    title_filters = {'Year': Year, 'Extension': Format}
    sleep(0.5)

    with console.status("[bold green]Searching for" + " " + bookName + " " + "in the library...",
                        spinner="monkey") as status:
        while True:
            sleep(2)
            status.update("[bold green]Pulling out relevant books from the shelf...",
                          spinner="monkey")
            titles = tf.search_title_filtered(
                bookName, title_filters, exact_match=True)
            if titles:
                break

    bookList.append(titles)

#update the 

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="left", style="cyan" + " bold")
    table.add_column("Publisher", justify="left")
    table.add_column("Title")
    table.add_column("Language", justify="right")
    table.add_column("Year", style="dim", justify="right")
    table.add_column("Pages", justify="right")

    for title in titles:
        table.add_row(
            title['ID'],
            title['Publisher'],
            title['Title'],
            title['Language'],
            title['Year'],
            title['Pages']
        )
    console.print(table)


def downloadBook():
    searchBook()
    selected = input("Enter the ID of the book you want to download: ")
    # url from the book [link] is https://libgen.io/harrypotter/sd342334553234.epub
    for book in bookList:
        for title in book:
            if selected == title['ID']:
                linkList.append(title['Mirror_1'])
                linkList.append(title['Mirror_2'])
                linkList.append(title['Mirror_3'])
                linkList.append(title['Mirror_4'])

            for link in linkList:
                # foreach link in the linkList test the url
                try:
                    r = requests.head(link)
                    if r.status_code == 200:
                        print("[bold green]Downloading the book...", ":books:")
                        # loading animation
                        with console.status("[bold green]Searching for" + " " + title['Title'] + " " + "in the library...", spinner="monkey") as status:
                            status.update("[bold green]Pulling out relevant books from the shelf...",
                                          spinner="monkey")
                        print("[bold green]Downloading to: " +
                              "./" + title['Title'] + "." + title['Extension'])
                        r = requests.get(link)
                        # automatically search for the download link

                        # inside the link search for the link to download the book

                        with open(title['Title'] + ".txt", 'wb') as f:
                            f.write(r.content)
                        print("[bold green]Download complete!",
                              ":thumbs_up:")
                        continue
                except requests.exceptions.RequestException as e:
                    print("[bold red]Download failed!")
                    print("Error: " + str(e))
                    continue

                # open the downloaded file and search for the link to download the book
                # if found, download the book
                # if not found, print error message
                # if error, try the next link
                # if all links are tested, print error message
                with open(title['Title'] + ".txt", 'r') as fh:
                    for line in fh:
                        # match every that has a href
                        match = re.search(r'href="(.*?)"', line)
                        if match:
                            # if the link is found, download the book
                            if match.group(1) == link:
                                print(
                                    "[bold green]Downloading the book...", ":books:")
                                # loading animation
                                with console.status("[bold green]Searching for" + " " + title['Title'] + " " + "in the library...", spinner="monkey") as status:
                                    status.update("[bold green]Pulling out relevant books from the shelf...",
                                                  spinner="monkey")
                                print("[bold green]Downloading to: " +
                                      "./" + title['Title'] + "." + title['Extension'])
                                r = requests.get(link)
                                # automatically search for the download link
                                with open(title['Title'] + "." + title['Extension'], 'wb') as f:
                                    f.write(r.content)
                                print("[bold green]Download complete!",
                                      ":thumbs_up:")
                                continue


downloadBook()
