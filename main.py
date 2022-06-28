from libgen_api import LibgenSearch
from rich import print
from rich.console import Console
from rich.table import Table
from time import sleep
import sys
import requests


console = Console()
bookList = []


def searchBook():
    print(
        "Welcome, [bold magenta]Don't forget to support the author if you enjoy the book[/bold magenta]!", ":books:", )
    # search_title()
    # enter the title of the book
    bookName = input("Enter the title of the book: ")
    Year = input("Enter the release year: ")
    Format = input("Enter the format of the book (epub, pdf) ")
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

    table = Table(show_header=True, header_style="bold magenta")
    # add id to the table
    table.add_column("ID", justify="left", style="cyan" + " bold")
    table.add_column("Publisher", justify="left")
    table.add_column("Title")
    table.add_column("Language", justify="right")
    table.add_column("Year", style="dim", justify="right")
    table.add_column("Pages", justify="right")

    for title in titles:
        table.add_row(
            # make a id number for each book
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
    for title in bookList:
        for book in title:
            # if the id of the book is the same as the user input then download the book
            if book['ID'] == selected:
                print("[bold green]Downloading the book...")
            else:
                print("[bold red]The book is not in the library...")
                sys.exit()


downloadBook()
