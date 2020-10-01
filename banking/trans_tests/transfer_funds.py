import datetime
import os
import sqlalchemy
import banking.banking_logic.models as models
from banking.banking_logic import session  # opens db, activates logic listener <--

trans_date = datetime.datetime(2020, 10, 1)
deposit = models.CHECKINGTRANS(TransId=1,CustNum=1, AcctNum=1,
                               DepositAmt=100, WithdrawlAmt=0, TransDate=trans_date)
print("\n\n - Deposit $100 to CHECKINGTRANS: " + str(deposit))
session.add(deposit)

trasfer = models.TRANSFERFUND(TransId=1,FromCustNum=1, FromAcct=1,ToCustNum=1, ToAcct=1,TransferAmt=10, TransDate=trans_date)
session.add(trasfer)

print("\n\n - Transfer 10 from checking to savings")

session.commit()

verify_cust = session.query(models.CUSTOMER).filter(models.CUSTOMER.CustNum ==12).one()

print("\ncust should have 10 in savings completed: " + str(verify_cust) + "\n\n")