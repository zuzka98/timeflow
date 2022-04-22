from typing import Any, Callable, List
from idom import html, component, use_effect, use_state
from .layout import Column, Container, Row
from .pagination import PaginationBlock
import math

from .input import Checkbox
from .tablebatch_row import TablebatchRow

per_page_list = [
    5,
    10,
    15,
]
thClass = "w-[176px] text-left text-text-table-head uppercase py-1 leading-5"
trClass = "border-b-[1px] border-border-table"
tdClassActive = "w-[176px] pt-4 pb-3"
tdClass = 'w-[176px] pt-4 pb-3'


@component
def SimpleTable(rows: List[Any]):
    checked, set_checked = use_state({})
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
        count = 0
        for row in rows[a:b]:
            tds = []
            count += 1

            for k in row:
                value = row[k]
                tds.append(html.td({"class": tdClassActive}, value))

            trs.append(TablebatchRow(count, tds, checked, set_checked))

        ths = [html.th({"class": thClass}, header) for header in rows[0].keys()]
        thead = html.thead(
            {},
            html.tr({"class": "bg-table-head"}, html.th({"class": "w-6"}), ths),
        )
        tbody = html.tbody(
            {},
            trs,
        )
        pages_total = math.ceil(len(rows) / number_of_visible_rows)
        pg_range = range(1, pages_total + 1)
        list_pages_nr = []
        for n in pg_range:
            list_pages_nr.append(n)
        table = html.div(
            {"class": "overflow-auto py-6 text-xs"},
            html.table({"class": "w-[905px] mx-auto xl:w-full"}, thead, tbody),
        )

        return html.div(
            {"class": "flex flex-col w-full space-y-2"},
            table,
            Row(
                PaginationBlock(
                    set_page_number, qty_page, set_select_per_page, per_page_list
                ),
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

    ths = [html.th({"class": thClass}, header) for header in rows[0].keys()]
    thead = html.thead(
        {"class": ""},
        html.tr({"class": "bg-table-head"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    table = html.table({"class": "w-[905px] mx-auto xl:w-full"}, thead, tbody)

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

data = {
    "Client": ["client_a", "client_a", "client_a", "client_a", "client_a", "client_a"],
    "Epic":["epic_a", "epic_a", "epic_a", "epic_a", "epic_b", "epic_b"],
    "Username":["user_a", "user_b", "user_c", "user_d", "user_b", "user_c"],
    "Forecasted Days":  ["(...)", "(...)", "(...)","(...)","(...)","(...)"],
    "Billings": ["(...)", "(...)", "(...)","(...)","(...)","(...)"],
    "Timelogs Days" :  ["(...)", "(...)", "(...)","(...)","(...)","(...)"],
    "Billings":  ["(...)", "(...)", "(...)","(...)","(...)","(...)"]
    }


@component
def BillingTable():

    ths = [html.th({"class": thClass}, key)
           for key, value in data.items()]
    thead = html.thead(
        {},
        html.tr(
            {"class": "bg-table-head"},
            ths),
    )          
      
    tds = []
    data_trs = []
    clientResult = []
    changeEpic = []
   
    for key, array in data.items():
        rowspan = 1
        startRowspanIndex = []
        for index, item in enumerate(array):
            if key == 'Client':
                if (index < len(array) - 1) and item == array[index + 1] :
                    rowspan += 1
                    startRowspanIndex.append(index)
                    tds.append([])
                else:
                    for epic_index, epic in enumerate(data['Epic']):
                        if (epic_index < index) and epic == data['Epic'][epic_index+1]:
                            continue
                        else:
                            changeEpic.append(epic_index)
                    tds.append([])
                    rowspan = rowspan + len(changeEpic)
                    tds[startRowspanIndex[0]].append(html.td({'class': tdClass, 'rowspan': rowspan},item))
                    rowspan = 1
                    clientResult.append(index + len(changeEpic))
                    startRowspanIndex = []
                    changeEpic = []
                
                
            elif key == 'Epic':
                if (index < len(array) - 1) and item == array[index + 1]:
                    rowspan += 1
                    startRowspanIndex.append(index)
                else:
                    tds[startRowspanIndex[0]].append(html.td({'class': tdClass, 'rowspan': rowspan},item))
                    rowspan = 1
                    changeEpic.append(index)
                    startRowspanIndex = []
            else: 
                tds[index].append(html.td({'class': tdClass}, item))
                
    for item in tds:
        data_trs.append(html.tr({'class': 'border-b-[1px] border-border-table'}, item))
    
    for index, epicIndex in enumerate(changeEpic):
        data_trs.insert(epicIndex + 1 + index, html.tr(
                        {'class': 'border-b-[1px] border-border-table bg-table-head'},
                        html.th(
                            {'colspan': '2', 'class': 'text-left'},
                            'Epic total'
                        ),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                    ))
    
    for index, clientIndex in enumerate(clientResult):
        data_trs.insert(clientIndex + 1 + index, html.tr(
                        {'class': 'border-b-[1px] border-border-table bg-table-head'},
                        html.th(
                            {'colspan': '3', 'class': 'text-left'},
                            'Client total'
                        ),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                    ))
    
    return Container(
        html.div(
            {'class': 'overflow-auto py-6 text-xs'},
            html.table(
                {
                    'class': 'w-[905px] mx-auto xl:w-full'
                },
                thead,
                html.tbody(
                    {},
                    data_trs,
                    html.tr(
                        {'class': 'border-b-[1px] border-border-table bg-table-head'},
                        html.th(
                            {'colspan': '3', 'class': 'text-left '},
                            'Grand total'
                        ),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                    ),
                    html.tr(
                        {'class': 'border-b-[1px] border-border-table bg-table-head'},
                        html.th(
                            {'colspan': '3', 'class': 'text-left '},
                            'Country total'
                        ),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                        html.td({'class': tdClass}, 'sum'),
                    )
                )
            )
        )

    )
