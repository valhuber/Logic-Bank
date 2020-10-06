import os
import sys
from datetime import datetime

cwd = os.getcwd()   # eg, /Users/val/python/pycharm/logic-bank/nw/tests
required_path_python_rules = cwd  # seeking /Users/val/python/pycharm/Logic-Bank
required_path_python_rules = required_path_python_rules.replace("/banking/tests", "")
required_path_python_rules = required_path_python_rules.replace("\banking\tests", "")

sys_path = ""
required_path_present = False
for each_node in sys.path:
    sys_path += each_node + "\n"
    if each_node == required_path_python_rules:
        required_path_present = True

if not required_path_present:
    print("Fixing path (so can run from terminal)")
    sys.path.append(required_path_python_rules)
else:
    pass
    print("NOT Fixing path (default PyCharm, set in VSC Launch Config)")

run_environment_info = "Run Environment info...\n\n"
run_environment_info += " Current Working Directory: " + cwd + "\n\n"
run_environment_info += "sys.path: (Python imports)\n" + sys_path + "\n"
run_environment_info += "From: " + sys.argv[0] + "\n\n"
run_environment_info += "Using Python: " + sys.version + "\n\n"
run_environment_info += "At: " + str(datetime.now()) + "\n\n"

print("\n" + run_environment_info + "\n\n")

import datetime
import banking.db.models as models
from banking.logic import session  # opens db, activates logic listener <--

delete_deposit = session.query(models.CHECKINGTRANS).filter(models.CHECKINGTRANS.TransId == 100).one()
print("\ndelete checking trans, deleting row: " + str(delete_deposit) )

delete_deposit = session.query(models.CHECKINGTRANS).filter(models.CHECKINGTRANS.TransId == 100).delete()
print("\ndelete checking trans, affected: " + str(delete_deposit) + " rows")
session.commit()

trans_date = datetime.datetime(2020, 10, 1)
deposit = models.CHECKINGTRANS(TransId=100, CustNum=2, AcctNum=2, DepositAmt=1000, WithdrawlAmt=0, TransDate=trans_date)
print("\n\n - deposit checking trans: " + str(deposit))
session.add(deposit)
session.commit()

verify_deposit = session.query(models.CHECKINGTRANS).filter(models.CHECKINGTRANS.TransId == 100).one()

print("\nverify_deposit, completed: " + str(verify_deposit) + "\n\n")