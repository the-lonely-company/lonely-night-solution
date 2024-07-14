from chains.general_chain import general_chain
from chains.suggestion_chain import suggestion_chain


def route(info):
    if "suggestion" in info["topic"].lower():
        return suggestion_chain
    else:
        return general_chain
