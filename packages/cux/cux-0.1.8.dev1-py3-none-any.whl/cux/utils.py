def get_nlp_result_file(conversation_id: int):
    return "nlpcache/" + "%X" % (1631149749 + conversation_id) + "-1.json"
