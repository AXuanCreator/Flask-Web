class Helper:
    @staticmethod
    def to_dict(orm):
        json = {key: value for key, value in orm.__dict__.items() if not key.startswith('_')}
        print('\033[35m[DEBUG]\033[0m | TO DICT : ', json)

        return json

    @staticmethod
    def to_dict_list(orm_list):
        return [Helper.to_dict(item) for item in orm_list]