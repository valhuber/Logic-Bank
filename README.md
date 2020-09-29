Use Logic Bank to govern SQLAlchemy
update transaction logic - multi-table derivations, constraints,
and actions such as sending mail or messages. Logic consists of:

* **Rules - 40X** more concise
using a spreadsheet-like paradigm, and

* **Python - control and extensibility,**
using standard functions and event handlers


Features
--------

Logic Bank is:

- **Extensible:** logic consists of rules (see below), plus standard Python code

- **Multi-table:** rules like `sum` automate multi-table transactions

- **Scalable:** rules are automatically pruned and optimized; for example, sums are processed as *1 row adjustment updates,* rather than expensive SQL aggregate queries

- **Manageable:** develop and debug your rules in IDEs, manage it in SCS systems (such as `git`) using existing procedures


For more information, [**see the Logic Bank Overview**](../../wiki/Home).

Skeptical?  You should be.  Taking a rule-based approach to
logic has serious implications for performance, quality and manageability.
Unlike familiar rules engines, Logic Bank rules are specifically
designed to be **scalable and extensible**
[as explained here.](../../wiki/Rules-Engines)


## Architecture
<figure><img src="images/architecture.png" width="500"><figcaption>Architecture</figcaption></figure>


 1. **Declare** logic as Python functions (see example below).

 2. Your application makes calls on `sqlalchemy` for inserts, updates and deletes.

    - By bundling transaction logic into sqlalchemy data access, your logic
  is automatically shared, whether for hand-written code (Flask apps, APIs)
  or via generators such as Flask AppBuilder.

 3. The **Logic Bank** engine handles sqlalchemy `before_flush` events on
`Mapped Tables`

 4. The logic engine operates much like a spreadsheet:
* **watch** for changes at the attribute level
* **react** by running rules that referenced changed attributes,
which can
* **chain** to still other attributes that refer to
_those_ changes.  Note these might be in different tables,
providing automation for _multi-table logic_.

Logic does not apply to updates outside SQLAlchemy,
nor to SQLAlchemy batch updates or unmapped sql updates.


## Declaring Logic as Spreadsheet-like Rules
To illustrate, let's use an adaption
of the Northwind database,
with a few rollup columns added.
For those not familiar, this is basically
Customers, Orders, OrderDetails and Products,
as shown in the diagrams below.

##### Declare rules using Python
Logic is declared as spreadsheet-like rules as shown below
from  [`nw/nw_logic/nw_rules_bank.py`](nw/nw_logic/nw_rules_bank.py),
which implements the *check credit* requirement:
```python
def activate_basic_check_credit_rules():
    """ Check Credit Requirement:
        * the balance must not exceed the credit limit,
        * where the balance is the sum of the unshipped order totals
        * which is the rollup of OrderDetail Price * Quantities:
    """

    Rule.constraint(validate=Customer, as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
    Rule.sum(derive=Customer.Balance, as_sum_of=Order.AmountTotal,
             where=lambda row: row.ShippedDate is None)  # *not* a sql select sum
    
    Rule.sum(derive=Order.AmountTotal, as_sum_of=OrderDetail.Amount)
   
    Rule.formula(derive=OrderDetail.Amount, as_expression=lambda row: row.UnitPrice * row.Quantity)
    Rule.copy(derive=OrderDetail.UnitPrice, from_parent=Product.UnitPrice)
```

The specification is fully executable, and governs around a
dozen transactions.  Let's look at **Add Order (Check Credit) -**
enter an Order / OrderDetails,
and rollup to AmountTotal / Balance to check CreditLimit.

This representatively complex transaction illustrates
common logic execution patterns, described below.

##### Activate Rules
To test our rules, we use
[`nw/trans_tests/add_order.py`](nw/trans_tests/add_order.py).
It activates the rules using this import:
```python
from nw.nw_logic import session  # opens db, activates logic listener <--
```
 
This executes [`nw/nw_logic/__init__.py`](nw/nw_logic/__init__.py),
which sets up the rule engine:
```python
by_rules = True  # True => use rules, False => use hand code (for comparison)
if by_rules:
    rule_bank_setup.setup(session, engine)     # setup rules engine
    activate_basic_check_credit_rules()        # loads rules above
    rule_bank_setup.validate(session, engine)  # checks for cycles, etc
else:
    # ... conventional after_flush listeners (to see rules/code contrast)
```
This is what replaces 200 lines of conventional code.  Let's see how it operates.

## Logic Execution: Watch, React, Chain
The engine operates much as you might imagine a spreadsheet:

* **Watch** - for inserts, deletes, and updates at the *attribute* level

* **React** - derivation rules referencing changes are (re)executed
(forward chaining *rule inference*); unreferenced rules are pruned.

* **Chain** - if recomputed values are referenced by still other rules,
*these* are re-executed.  Note this can be in other tables, thus
automating multi-table transaction logic.
   
[Click here](../../wiki/Multi-Table-Logic-Execution)

## An Agile Perspective
The core tenant of agile is _working software,_
driving _collaboration,_ for _rapid iterations._
Here's how rules can help.

##### Working Software _Now_
The examples above illustrate how just a few rules can replace 
[pages of code](../../wiki/by-code).

##### Collaboration - Running Screens

Certainly business users are more easily able to
read rules than code.  But honestly, rules are
pretty abstract.

Business users relate best to actual working pages -
_their_ intepretation of working software.
The [fab-quick-start](https://github.com/valhuber/fab-quick-start/wiki)
project enables you to build a basic web app in minutes.

This project has already generated such an app, which you can run like this:

```
cd nw_app
export FLASK_APP=app
flask run
```

Login: user = admin, password = p

##### Iteration - Automatic Ordering
Rules are _self-organizing_ - they recognize their interdependencies,
and order their execution and database access (pruning, adjustments etc)
accordingly.  This means:

* order is independent - you can state the rules in any order
and get the same result

* maintenance is simple - just make changes, additions and deletions,
the engine will reorganize execution order and database access, automatically


## Installation

#### Contents
This is the development project for `python-rules`:
* Explore project contents [here](../../wiki/Explore-Logic-Bank)
* This project also includes a sample application
used to test and illustrate rules.  Importantly,
it inclues comparisons of Business logic, both
[by-code](../../wiki/by-code) and
[by-rules,](../../wiki/by-rules)

Stand-alone projects illustrating how to _use_
`python-rules` can be found
[here](https://github.com/valhuber/python-rules-examples).
These more closely resemble your use of `python-logic`,
including usage of the `pip` mechanism to install.

#### Installation Procedure
To get started, you will need:

* Python3.8 (Relies on `from __future__ import annotations`, so requires Python 3.8)

   * Run the windows installer; on mac/Unix, consider [using brew](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)
   
* virtualenv - see [here](https://www.google.com/url?q=https%3A%2F%2Fpackaging.python.org%2Fguides%2Finstalling-using-pip-and-virtual-environments%2F%23creating-a-virtual-environment&sa=D&sntz=1&usg=AFQjCNEu-ZbYfqRMjNQ0D0DqU1mhFpDYmw)  (e.g.,  `pip install virtualenv`)

* An IDE - any will do (I've used [PyCharm](https://www.jetbrains.com/pycharm/download) and [VSCode](https://code.visualstudio.com), install notes [here](https://github.com/valhuber/fab-quick-start/wiki/IDE-Setup)) - ide will do, though different install / generate / run instructions apply for running programs

Issues?  [Try here](https://github.com/valhuber/fab-quick-start/wiki/Mac-Python-Install-Issues).

Using your IDE or command line: 
```
cd your-project
virtualenv venv
source venv/bin/activate
```

#### Testing
You can run the .py files under `nw/trans_tests`, and/or
run the FAB application as described above.

## Status: Running, Under Development
Essential functions running on 9/6/2020:
multi-table transactions -
key paths of copy, formula, constraint, sum and event rules. 

Not complete, under active development.

Ready to explore and provide feedback
on general value, and features.
