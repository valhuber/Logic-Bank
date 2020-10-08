from sqlalchemy.orm import session

from logic_bank.rule_bank.rule_bank_setup import setup, validate


def activate(session: session, activator: callable):
    """
    load rules - executed on commit

    raises exception if cycles detected

    :param session: SQLAlchemy session
    :param activator: function that declares rules (e.g., Rule.sum...)
    :return:
    """
    engine = session.bind.engine
    setup(session, engine)
    activator()
    validate(session, engine)