from idom import component

from uiflow.components.table import BillingTable


@component
def page():

    return BillingTable()