
def format_number(phone):
    if phone == "":
        return ""
    return "+234{}".format(phone[1:])