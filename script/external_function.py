
from uitest.uihelper.common import get_state_as_dict
import time

DEFAULT_SLEEP = 0.05

# TODO: add visible view of the results
def time_record(item, test_time):
    with open('test_result.txt', 'a') as file:
        file.write('{0}\t{1:.3f}\n'.format(item, test_time))

def trim_average(list_item):

    max_value = max(list_item)
    list_item.remove(max_value)

    min_value = min(list_item)
    list_item.remove(min_value)

    return sum(list_item)/len(list_item)

# arithmatic average
def ari_average(list_item):
    return sum(list_item)/len(list_item)
    

# An opposite implement of wait_until_property_is_updated
def wait_until_property_is_updated_custom(element, propertyName, value):
    while True:
        if get_state_as_dict(element)[propertyName] != value:
            return
        else:
            time.sleep(DEFAULT_SLEEP)