import datetime
import json


def logger_path(path):

    def logger(function):
        all_log_list = []

        def new_function(*args, **kwargs):
            log_dict = {}
            result = function(*args, **kwargs)
            log_dict['date_time'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            log_dict['name'] = function.__name__
            log_dict['args'] = args
            log_dict['kwargs'] = kwargs
            log_dict['return'] = result
            all_log_list.append(log_dict)
            file = open(path, 'a', encoding='utf-8')
            json.dump(all_log_list, file, ensure_ascii=False)
            return result

        return new_function

    return logger
