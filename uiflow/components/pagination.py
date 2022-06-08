from idom import html, component

from .input import SelectPerPage
from .icons import arrow_left, arrow_right


class_str = """text-primary-500 placeholder-secondary-400 w-full px-4 py-2.5 mt-2 
                    text-base transition duration-500 ease-in-out transform 
                    border-transparent bg-secondary-300 focus:border-blueGray-500 
                    focus:bg-white dark:focus:bg-secondary-400 focus:outline-none 
                    focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2 
                    ring-gray-400"""

pageButtonClass = "w-8 h-8 mx-3 flex items-center justify-center cursor-pointer rounded-full hover:bg-pagination-hover hover:w-8 hover:h-8"
wrapperClass = "flex items-center w-full justify-center text-pagination md:justify-end"
currentPageStyle = {"font-weight": "bold", "color": "#1f1254"}


@component
def PaginationButton(set_page_number, number, page_number):
    def select_page_number(event):
        set_page_number(number)

    def condition():
        return currentPageStyle if page_number == number else {"color": "black"}

    pgn_btn = html.button(
        {"class": pageButtonClass, "onClick": select_page_number, "style": condition()},
        number,
    )

    return pgn_btn


@component
def PaginationBlock(
    set_page_number, qty_page, set_per_page, per_page_list, page_number
):
    pgn_block = (
        [
            PaginationButton(set_page_number, number + 1, page_number)
            for number in range(qty_page)
        ]
        if qty_page > 1
        else []
    )

    def next_page(event):
        if page_number >= qty_page:
            return
        else:
            set_page_number(page_number + 1)

    def previous_page(event):
        if page_number <= 1:
            return
        else:
            set_page_number(page_number - 1)

    return html.div(
        {"class": "flex justify-between w-full items-center"},
        SelectPerPage(set_per_page, per_page_list),
        html.div(
            {"class": wrapperClass},
            html.button(
                {"class": pageButtonClass, "onClick": previous_page},
                arrow_left,
            ),
            pgn_block,
            html.button({"class": pageButtonClass, "onClick": next_page}, arrow_right),
        ),
    )
