from typing import Any, Callable, List
from idom import html, component, use_state
from components.layout import Column, Row
from components.pagination import PaginationBlock
import math

per_page_list = [
    2,
    4,
    6,
]


@component
def SimpleTable(rows: List[Any]):

    try:
        select_per_page, set_select_per_page = use_state(per_page_list[0])
        page_number, set_page_number = use_state(1)
        trs = []
        p = page_number
        m = p - 1
        number_of_visible_rows = int(select_per_page)
        a = m * number_of_visible_rows
        b = a + number_of_visible_rows
        qty_page = math.ceil(len(rows) / number_of_visible_rows)
        for row in rows[a:b]:
            tds = []
            for k in row:
                value = row[k]
                tds.append(html.td({"class": "p-4 w-full"}, value))
            trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

        ths = [html.th({"class": "p-4 w-full"}, header)
               for header in rows[0].keys()]
        thead = html.thead(
            {"class": "flex bg-secondary-400 text-white w-full"},
            html.tr({"class": "flex w-full mb-4"}, ths),
        )
        tbody = html.tbody(
            {
                "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
            },
            trs,
        )
        pages_total = math.ceil(len(rows) / number_of_visible_rows)
        pg_range = range(1, pages_total + 1)
        list_pages_nr = []
        for n in pg_range:
            list_pages_nr.append(n)
        table = html.table({"class": "text-left"}, thead, tbody)

        return html.div(
            {"class": "flex flex-col w-full space-y-2"},
            table,
            Row(
                PaginationBlock(set_page_number, qty_page,
                                set_select_per_page, per_page_list),
            ),
        )
    except TypeError:
        return False
    except IndexError:
        return False


@component
def SubmitTable(rows: List[Any]):
    trs = []
    for row in rows[-5:]:
        tds = []
        for k in row:
            value = row[k]
            tds.append(html.td({"class": "p-4 w-full"}, value))
        trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

    ths = [html.th({"class": "p-4 w-full"}, header)
           for header in rows[0].keys()]
    thead = html.thead(
        {"class": "flex bg-secondary-400 text-white w-full"},
        html.tr({"class": "flex w-full mb-4"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    table = html.table({"class": "text-left"}, thead, tbody)

    return html.div(
        {"class": "flex flex-col w-full space-y-2"},
        table,
    )


@component
def HiddenButton(is_hidden, set_is_hidden):
    text, set_text = use_state("hide table")

    def show_page(event):
        if is_hidden:
            set_is_hidden(False)
            set_text("hide table")
        else:
            set_is_hidden(True)
            set_text("show table")

    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": show_page,
        },
        text,
    )

    return btn
