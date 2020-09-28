import sqlalchemy_utils

import nw.nw_logic.models as models
from python_rules.exec_row_logic.logic_row import LogicRow
from python_rules.util import row_prt, prt
from nw.nw_logic import session  # opens db, activates logic listener <--

cls = sqlalchemy_utils.functions.get_class_by_table(models.Base, "Product", data=None)

# Add Order - works
pre_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
session.expunge(pre_cust)

# First, try one to fail
bad_order = models.Order(AmountTotal=0, CustomerId="ALFKI", ShipCity="Richmond",
                         EmployeeId=6, Freight=1)
session.add(bad_order)

# OrderDetails - https://docs.sqlalchemy.org/en/13/orm/backref.html
bad_item1 = models.OrderDetail(ProductId=1, Amount=0,
                               Quantity=1, UnitPrice=18,
                               Discount=0)
bad_order.OrderDetailList.append(bad_item1)
bad_item2 = models.OrderDetail(ProductId=2, Amount=0,
                               Quantity=20000, UnitPrice=18,
                               Discount=0)
bad_order.OrderDetailList.append(bad_item2)
did_fail_as_expected = False
try:
    session.commit()
except:
    session.rollback()
    did_fail_as_expected = True

if not did_fail_as_expected:
    raise Exception("huge order expected to fail, but succeeded")
else:
    print("\n" + prt("huge order failed credit check as expected.  Now trying valid order, should succeed..."))

new_order = models.Order(AmountTotal=0, CustomerId="ALFKI", ShipCity="Richmond",
                         EmployeeId=6, Freight=1)
session.add(new_order)

# OrderDetails - https://docs.sqlalchemy.org/en/13/orm/backref.html
new_item1 = models.OrderDetail(ProductId=1, Amount=0,
                               Quantity=1, UnitPrice=18,
                               Discount=0)
new_order.OrderDetailList.append(new_item1)
new_item2 = models.OrderDetail(ProductId=2, Amount=0,
                               Quantity=2, UnitPrice=18,
                               Discount=0)
new_order.OrderDetailList.append(new_item2)
session.commit()

post_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()

print("\nadd_order, update completed\n\n")
row_prt(new_order, "\nnew Order Result")  # $18 + $38 = $56
if new_order.AmountTotal != 56:
    print ("==> ERROR - unexpected AmountTotal: " + str(new_order.AmountTotal) +
           "... expected 56")
row_prt(new_item1, "\nnew Order Detail 1 Result")  # 1 Chai  @ $18
row_prt(new_item2, "\nnew Order Detail 2 Result")  # 2 Chang @ $19 = $38

logic_row = LogicRow(row=post_cust, old_row=pre_cust, ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)
if post_cust.Balance == pre_cust.Balance + 56:
    logic_row.log("Correct adjusted Customer Result")
    assert True
else:
    logic_row.log("ERROR - incorrect adjusted Customer Result")
    print("\n--> probable cause: Order customer update not written")
    assert False
if post_cust.OrderCount == pre_cust.OrderCount + 1 and\
    post_cust.UnpaidOrderCount == pre_cust.UnpaidOrderCount + 1:
    pass
else:
    logic_row.log("Error - unexpected OrderCounts")
print("\nadd_order, ran to completion\n\n")


