import os
from shutil import copyfile

import sqlalchemy
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session

from python_rules.rule_bank import rule_bank_withdraw  # FIXME design why required to avoid circular imports??
from python_rules.rule_bank import rule_bank_setup
from banking.banking_logic.banking_rules_bank import activate_basic_rules

from python_rules.util import prt

""" Initialization
1 - Connect
2 - Register listeners (either hand-coded ones above, or the logic-engine listeners).
"""

# Initialize Logging
import logging
import sys

logic_logger = logging.getLogger('logic_logger')  # for users
logic_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
handler.setFormatter(formatter)
logic_logger.addHandler(handler)

do_engine_logging = False  # TODO move to config file, reconsider level
engine_logger = logging.getLogger('engine_logger')  # for internals
if do_engine_logging:
    engine_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')
    handler.setFormatter(formatter)
    engine_logger.addHandler(handler)

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(basedir)

print("\n****************\n"
      "  IMPORTANT - create banking.db from banking-gold.db in " + basedir + "/db/" +
      "\n****************")

banking_loc = basedir + "/db/banking.db"
banking_source = basedir + "/db/banking-gold.db"
copyfile(src=banking_source, dst=banking_loc)

import banking as banking
conn_string = banking.conn_string  # "mysql://root:espresso_logic@127.0.0.1:3309/banking"
conn_string = "sqlite:///" + banking_loc
engine = sqlalchemy.create_engine(conn_string,
                                  pool_pre_ping= True,
                                  echo=True)  # sqlalchemy sqls...

session_maker = sqlalchemy.orm.sessionmaker()
session_maker.configure(bind=engine)
session = session_maker()

by_rules = True  # True => use rules, False => use hand code (for comparison)
rule_list = None
db = None
if by_rules:
    rule_bank_setup.setup(session, engine)
    activate_basic_rules()
    rule_bank_setup.validate(session, engine)  # checks for cycles, etc

print("\n" + prt("session created, listeners registered\n"))

