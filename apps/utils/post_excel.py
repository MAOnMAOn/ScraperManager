import re

import pandas as pd


class PostExcel(object):
    def __init__(self, path):
        self.df = self.read_excel(path)

    def read_excel(self, path):
        return pd.read_excel(path).fillna(method='ffill')

    def rename_columns(self, model_instance):
        rename_dict = dict()
        for i in model_instance._meta.fields:  # 获取数据库模型所有的关键字字段
            extra_name = model_instance._meta.get_field(i.name).verbose_name  # 获取其verbose_name
            rename_dict.update({extra_name: i.name})
        self.df.rename(columns=rename_dict, inplace=True)

    def set_search_key(self, column_name):
        search_key_list = list()
        for item in self.df.loc[:, column_name]:
            if re.search('三级|3', str(item)):
                item = 3
            if re.search('二级|2', str(item)):
                item = 2
            if re.search('一级|1', str(item)):
                item = 1
            search_key_list.append(item)
        self.df.loc[:, column_name] = search_key_list
        return self.df

    def rename_foreignkey(self, foreign_key):
        for i in self.df.columns:
            if i == foreign_key:
                self.df.rename(columns={i: str(foreign_key) + '_id'}, inplace=True)

    def bulk_create(self, model_object):
        save_dict = self.df.T.to_dict(orient='dict')
        my_list = list()
        for e in save_dict.values():
            my_list.append(model_object(**e))
        model_object.objects.bulk_create(my_list)

    def save_model(self, model_object, foreign_object, foreign_key):
        value_list = list()
        frame = pd.DataFrame([i for i in foreign_object.objects.values()])
        try:
            for i in self.df.loc[:, foreign_key + '_id']:
                name_col = list(frame.loc[:, 'name'].str.strip())
                for j in name_col:
                    if re.search(str(i), j):
                        item = name_col.index(i.strip())
                        i = frame.loc[item, 'id']
                        value_list.append(float(i))
            self.df.loc[:, foreign_key + '_id'] = value_list
        except (ValueError, AttributeError):
            pass
        finally:
            self.bulk_create(model_object)
            del frame
            del self.df


"""


"""

