from chains.general_chain import general_chain
from chains.suggestion_chain import suggestion_chain
from chains.db_chain import db_chain


def route(info):
    if "suggestion" in info["topic"].lower():
        return db_chain
    else:
        return general_chain