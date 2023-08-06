
class Adder:
    @staticmethod
    def __normalize_text(_type):
        match _type:
            case "запрос":
                return input(f"Введите {_type}, или команду: ").lower().strip()
            case "ответ":
                return input(f"Введите {_type}, или команду: ").strip()


    # Сохранение в json. name - это meaning, а file принимает переменную-словарь,
    # path - относительный путь к файлу, но не более одной папки
    @staticmethod
    def __save(name, file, path='jsonComLab/'):
        from json import dump
        import os
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        with open(path + name + '.json', 'w') as add_info_file:
            dump(file, add_info_file)


    # сборка файла
    @staticmethod
    def __creator(meaning, request, response):
        dct = {
            meaning: {
                "request": request,
                "response": response,
            }
        }
        Adder.__save(meaning, dct)


    # заполнение листов, где _type - это "запрос", или "ответ".
    @staticmethod
    def __smart_input(_type):

        result = []
        key = True
        print('Для продолжения, введите "$$next". Чтобы узнать все команды - введите "$$help".')
        while key:
            input_text = Adder.__normalize_text(_type)
            # проверка на рабочие команды
            if "$$" in input_text:
                match input_text:
                    case "$$next":
                        key = False
                        break
                    case "$$del":
                        try:
                            result.pop()
                        except:
                            print(f"Данный {_type}-лист пуст.")
                    case "$$clear":
                        result = []
                    case "$$show":
                        print(f"{_type}-лист: {result}")
                    case "$$help":
                        print("$$del - удаляет последний добавленный элемент;\n"
                              "$$clear - очищает лист;\n"
                              "$$show - показывает лист добавленных значений;\n"
                              "$$next - заканчивает набор и переводит к следующему этапу;\n")
                    case _:
                        print("Команда написана неверно, либо отсутствует.")
            else:
                if input_text not in result:
                    result.append(input_text)

        return result

    @staticmethod
    def __inputs():

        meaning = input('Название meaning: ')
        request = Adder.__smart_input("запрос")
        response = Adder.__smart_input("ответ")

        return meaning, request, response

    @staticmethod
    def main():
        meaning, request, response = Adder.__inputs()
        Adder.__creator(meaning, request, response)


if __name__ == "__main__":
    Adder.main()
