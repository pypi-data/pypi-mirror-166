

class JsonOperations:

    @staticmethod
    def read(name, path=''):
        """Возвращает значение JSON файла.
        Аргументы:
        path - путь каталога с JSON файлом (по умолчанию path=''),
        name - имя файла без указания формата."""
        from json import load
        with open(path + name + '.json') as json_import_data:
            data_file = load(json_import_data)
        return data_file

    @staticmethod
    def save(name, variable, path=''):
        """Сохраняет значение переменной в JSON файл.
        Аргументы: 
        path - путь каталога где будет сохранён JSON файл,
        name - имя файла без указания формата, 
        variable - экспортируемая переменная,
        значение которой сохраняется в JSON файл."""

        from json import dump
        with open(path + name + '.json', 'w') as add_info_file:
            dump(variable, add_info_file)

