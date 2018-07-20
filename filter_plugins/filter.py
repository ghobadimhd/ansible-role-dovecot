from ansible.errors import AnsibleError
from ansible.module_utils.six import string_types


def get_key(value):
    """ return key of single item mapping """
    if not isinstance(value, dict):
       raise AnsibleError(
           "input should be a dict, but was given a input of %s" % (type(value)))
    if len(value.items()) != 1:
       raise AnsibleError("dict most have only 1 item")
    item_key, item_value = [x for x in value.items()][0]
    return item_key


def get_value(value):
    """ return key of single item mapping"""
    if not isinstance(value, dict):
       raise AnsibleError("input should be a dict, but was given a input of ")
    if len(value.items()) != 1:
       raise AnsibleError("dict most have only 1 item")
    item_key, item_value = [x for x in value.items()][0]
    return item_value


def get_key_value(value):
    """ convert single item mapping to key, value"""
    if not isinstance(value, dict):
       raise AnsibleError("input should be a dict, but was given a input of ")
    if len(value.items()) != 1:
       raise AnsibleError("dict most have only 1 item")
    item_key, item_value = [x for x in value.items()][0]
    return (item_key, item_value)


def dictlist2items(value):
    """ convert list of single item mappings to list of key, values
    convert this:
        tags:
          - tag1: a
          - tag2: b
    to this:
        tags:
          - key: tag1
          - value: a
          - key: tag2
          - value: b
    this save order of tags
    """
    if not isinstance(value, list):
           raise AnsibleError(
           "input should be a list, but was given a input of %s" % type(value))
    new_value = [get_key_value(x) for x in value]
    return new_value


class FilterModule(object):
    """Filters for working with output mapping and list of mapping"""

    filter_map = {
        'get_key': get_key,
        'get_value': get_value,
        'dictlist2items': dictlist2items,
    }

    def filters(self):
        return self.filter_map
