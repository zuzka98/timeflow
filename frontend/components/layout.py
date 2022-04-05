from typing import Any, Callable, List
from idom import html, component


def Container(*args: html):
    return html.div({"class": "container"}, args)


def FlexContainer(*args: html):
    return html.div({"class": "flex w-full xl:ml-60 xl:w-auto"}, args)


def Column(*args: html, width: str = "full"):
    return html.div(
        {"class": f"flex flex-col w-{width} space-y-2 pl-2 mt-2"}, args
    )


@component
def Row(*args: html, justify: str = None):
    return html.div({"class": f"flex flex-col px-2 md:flex-row {justify} space-x-4"}, args)
