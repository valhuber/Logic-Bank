import datetime
import banking.banking_logic.models as models
from banking.banking_logic import session
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.rule import Rule
from banking.banking_logic.models import CUSTOMER, CHECKING, CHECKINGTRANS, SAVING, SAVINGSTRANS, TRANSFERFUND

def activate_basic_rules():
    def transferFunds(row: TRANSFERFUND, old_row: TRANSFERFUND, logic_row: LogicRow):
        if logic_row.ins_upd_dlt == "ins" or True:  # logic engine fills parents for insert
            print("Transfer from source to target")
            fromCustNum = row.FromCustNum
            toCustNum = row.ToCustNum
            acctNum = row.FromAcct
            trans_date = datetime.datetime(2020, 10, 1)
            transferAmt = row.TransferAmt
            transID = row.TransId
            withdrawl = models.SAVINGSTRANS(TransId=transID, CustNum=toCustNum, AcctNum=acctNum, DepositAmt=transferAmt, WithdrawlAmt=0,
                                            TransDate=trans_date)
            logic_row.insert(" from savings", withdrawl)
            deposit = models.CHECKINGTRANS(TransId=transID, CustNum=fromCustNum, AcctNum=acctNum,
                                           DepositAmt=0, WithdrawlAmt=transferAmt, TransDate=trans_date)
            print("\n\n - withdraw from CHECKINGTRANS: " + str(deposit))
            logic_row.insert("to checking", deposit)

    Rule.sum(derive=CHECKING.Deposits, as_sum_of=CHECKINGTRANS.DepositAmt)
    Rule.sum(derive=CHECKING.Withdrawls, as_sum_of=CHECKINGTRANS.WithdrawlAmt)
    Rule.formula(derive=CHECKING.AvailableBalance, as_expression=lambda  row: row.Deposits - row.Withdrawls)
    Rule.count(derive=CHECKING.ItemCount, as_count_of=CHECKINGTRANS)

    Rule.sum(derive=CUSTOMER.CheckingAcctBal, as_sum_of=CHECKING.AvailableBalance)
    Rule.sum(derive=CUSTOMER.SavingsAcctBal, as_sum_of=SAVING.AvailableBalance)
    Rule.formula(derive=CUSTOMER.TotalBalance, as_expression=lambda row: row.CheckingAcctBal + row.SavingsAcctBal)
    Rule.constraint(validate=CUSTOMER,
                    as_condition=lambda row: row.TotalBalance >= 0,
                    error_msg="Your balance of ({row.TotalBalance}) is less than 0)")

    Rule.sum(derive=SAVING.Withdrawls, as_sum_of=SAVINGSTRANS.WithdrawlAmt)
    Rule.sum(derive=SAVING.Deposits, as_sum_of=SAVINGSTRANS.DepositAmt)
    Rule.formula(derive=SAVING.AvailableBalance, as_expression=lambda row: row.Deposits - row.Withdrawls)
    Rule.count(derive=SAVING.ItemCount, as_count_of=SAVINGSTRANS)

    Rule.formula(derive=CHECKINGTRANS.Total, as_expression=lambda row: row.DepositAmt - row.WithdrawlAmt)
    Rule.formula(derive=SAVINGSTRANS.Total, as_expression=lambda row: row.DepositAmt - row.WithdrawlAmt)

    Rule.commit_row_event(on_class=TRANSFERFUND, calling=transferFunds)

