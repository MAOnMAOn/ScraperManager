from copy import deepcopy
from urllib.parse import quote

from url_tools.core.config import (BASE_URL_KEY, BASE_URL_MAPPING, DEFAULT_PAGE_NUMBER, URL_KEY_ENCODING,
                                   URL_PARAM_MAPPING)


class UrlGenerator(object):
    def __init__(self, key_list):
        """
        self.param_dict: {page: [1, 2, 3, 4, 5,], city: ['Beijing', 'Shanghai']}
        :param key_list:
        """
        self.key_list = key_list
        self.base_url = BASE_URL_MAPPING[BASE_URL_KEY]
        self.param_dict = URL_PARAM_MAPPING[BASE_URL_KEY]
        self.page_num = DEFAULT_PAGE_NUMBER
        self.encoding = URL_KEY_ENCODING

    def get_url_param(self):
        """
        Get the initial constructor dictionary. The value of the dictionary can only be list
        :param
        :return:
        """
        if not self.param_dict:
            self.param_dict = dict()
        if self.page_num:
            page_num_dict = {'page_num': [i for i in range(1, int(self.page_num) + 1)]}
            self.param_dict.update(page_num_dict)
        keyword_dict = {'keyword': [quote(keyword, encoding=self.encoding)
                                    for keyword in self.key_list]}
        self.param_dict.update(keyword_dict)

    def change_param_struct(self):
        param_list = list()
        self.get_url_param()
        for i in self.param_dict:
            tmp_value = self.param_dict[i]
            if isinstance(tmp_value, int):
                tmp_value = str(tmp_value)
            for j in tmp_value:
                param_list.append({i: j})
        return param_list

    @staticmethod
    def change_dict(list_x):
        dict_list = []
        for i in list_x:
            for j in list_x:
                if i.keys() == j.keys():
                    break
                else:
                    item = deepcopy(i)
                    item.update(deepcopy(j))
                    if item not in dict_list:
                        dict_list.append(item)
        return dict_list

    def recursive(self, list_x, rec_times):
        my_dict = self.change_dict(list_x)

        n = rec_times - 1
        while True:
            if n < 1:
                break
            n = n - 1
            my_dict = self.change_dict(my_dict)
        return my_dict

    def get_param_array(self):
        rec_array = self.change_param_struct()
        param_length = len(self.param_dict)
        array = self.recursive(rec_array, rec_times=param_length - 1)
        param_array = [i for i in array if len(i) == param_length]
        if len(param_array) < 1:
            param_array = rec_array
        return param_array

    def get_link_set(self):
        """
        {keyword k} will treat the keyword argument as a dictionary kwargs,
        and will use the key of kwargs[k] to throw a KeyError
        :return:
        """
        link_set = [self.base_url.format(**i) for i in self.get_param_array()]
        return link_set

