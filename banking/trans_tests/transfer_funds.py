import datetime
import os
import sqlalchemy
import banking.banking_logic.models as models
from banking.banking_logic import session  # opens db, activates logic listener <--

trans_date = datetime.datetime(2020, 10, 1)
withdrawl = models.SAVINGSTRANS(TransId=101, CustNum=2, AcctNum=3, DepositAmt=10, WithdrawlAmt=0, TransDate=trans_date)
print("\n\n - withdraw funds from checking trans: " + str(withdrawl))
session.add(withdrawl)

deposit = models.CHECKINGTRANS(TransId=101,CustNum=2, AcctNum=2,
                               DepositAmt=0, WithdrawlAmt=10, TransDate=trans_date)
print("\n\n - deposit to savings trans: " + str(deposit))
session.add(deposit)

session.commit()

