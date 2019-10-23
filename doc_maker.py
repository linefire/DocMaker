"""Модуль який робить документацію для язика програмування 'Kotlin'.

УВАГА: Модуль у розробці, окремі функції не працюють.

1.Модуль робить документацію з програмних кодів 
язика програмування 'Kotlin'.
2.Модуль можна імпортувати або запустити.
3.Модуль не потребує сторонніх бібліотек.
4.Модуль може опрацювати:
    a) Окремий файл. - у розробці до верії 1.0
    b) Файли каталогу. - у розробці до верії 2.0
    с) Файли каталогу та підкаталогів. - у розробці до верії 3.0
    d) Файли з git репозиторія. - у розробці до верії 4.0
5.Модуль генерує документацію у вигляді html сторінок.
6.Модуль генерує html сторінки з використанням технології bootstrap.

Приклади застосування модуля:
Запуск модуля:
    Якщо потрібно документовати файл:
        python doc_maker.py -f "path\\\\to\\\\file"
    Якщо потрібно документовати файли з каталогу:
        python doc_maker.py -d "path\\\\to\\\\dir"
    Якщо потрібно документовати файли з каталогу та його підкаталогів:
        python doc_maker.py -r "path\\\\to\\\\dir"
    Якщо потрібно документовати файли git репозиторія:
        python doc_maker.py -g "path\\\\to\\\\git"
    
    Якщо потрібно зберегти документацію у окреме місце:
        python doc_maker.py -g "path\\\\to\\\\git" -o "path\\\\to\\\\dir"
Імпорт модуля:
    from doc_maker import DocMaker

    Якщо потрібно документовати файл:
        DocMaker.parse(DocMaker.file, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з каталогу:
        DocMaker.parse(DocMaker.dir, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з каталогу та його підкаталогів:
        DocMaker.parse(DocMaker.recursive, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з git репозиторія:
        DocMaker.parse(DocMaker.git, "path\\\\to\\\\file")
    
    Якщо потрібно зберегти документацію у окреме місце:
        DocMaker.parse(DocMaker.file, "path\\\\to\\\\file", "path\\\\to\\\\dir")

"""

__version__ = '0.5.4'

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from sys import argv
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

# TODO 1.0 Збір інформації з файлу
# TODO 2.0 Збір інформації з файлів каталогу
# TODO 3.0 Збір інформації з файлів каталогу та підкаталогів
# TODO 4.0 Збір інформації з git репозиторію
# TODO <1.0 Генерування документації у html вигляді
# TODO <1.0 Підключити bootstrap 4.3.x
# TODO 5.0 Дизайн документації


class _TreeElement(ABC):
    """Базовий клас для всіх об'єктів в дереві об'єктів
    
    Attributes
    ----------
    name : str
        Ім'я яке буде відображено у дереві документації
    path : str
        Відносний шлях до об'єкту у документації
    parent : Optional['_TreeElement']
        Батько об'єкту

    Methods
    -------
    get_tree_from_root()
        Вертає дерево дітей у html форматі відносно кореневого елементу
    get_tree()
        Вертає дерево дітей у html форматі
    get_childs()
        Вертає список дітей цього об'єкту
    
    """

    def __init__(self, name: str, path: str, 
                 parent: Optional['_TreeElement'] = None):
        """Конструктор класу _TreeElement

        Parameters
        ----------
        name : str
            Ім'я яке буде відображено у дереві документації
        path : str
            Відносний шлях до об'єкту у документації
        parent : Optional['_TreeElement']
            Батько об'єкту
        
        """

        self.name: str = name
        self.path: str = path
        self.parent: Optional['_TreeElement'] = parent

    def get_tree_from_root(self) -> str:
        """Вертає дерево у html форматі відносно кореневого елементу

        Метод знаходить корневий eлемент дерева, та вертає html
        сторінку з метода get_tree.

        Returns
        -------
        self.get_tree : str
            Вертає дерево у вигляді html коду відносно корeневого 
            елементу.
        
        """

        if self.parent:
            return self.parent.get_tree_from_root()
        else:
            return self.get_tree()

    def get_tree(self) -> str:
        """Вертає дерево своїх дітей у html форматі

        Метод рекурсивно вертає дерево змісту у html форматі.

        Returns
        -------
        html : str
            Вертає html код дерева змісту себе та своїх дітей.
        
        """

        html = '<li>{}</li>'.format(self.name)
        childs = self.get_childs()
        if childs:
            html += '<ul>'
            for child in childs:
                html += child.get_tree()
            html += '</ul>'
        return html

    @abstractmethod
    def get_childs(self) -> List['_TreeElements']:
        """Абстрактний метод який вертає дітей цього елементу
        
        Так як наслідники цього класу мають різні типи дітей, вони 
        повинні по різному визначатися.

        Returns
        -------
        : List['_TreeElements']
            Список дітей цього об'єкту

        """

        pass

    @abstractmethod
    def get_content(self) -> str:
        """Абстрактний метод вертає інформацію об'єкта у вигляді HTML
        
        Так як наслідники цього класу мають різні типи інформації, вони
        повинні по різному визначатися.

        Returns
        -------
        : str
            Інформація у html вигляді

        """

        pass


class _Var(_TreeElement):
    """Клас який описує змінні класів Kotlin
    
    Attributes
    ----------
    name : str
        Ім'я змінної
    doc : str
        Опис змінної

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію змінної у html вигляді
    
    """

    def __init__(self, name: str, doc: str = 'Опис відсутній'):
        """
        
        Parameters
        ----------
        name : str
            ім'я змінної
        doc : str = 'Опис відсутній'
            Опис змінної

        """

        self.name: str = name
        self.doc: str = doc

    def get_childs(self) -> List['_TreeElements']:
        """Метод який вертає дітеї цього об'єкту
        
        У цього об'єкту не може бути дітей, тому він вертає пустий 
        список.
        
        """

        return []

    def get_content(self) -> str:
        """Метод який вертає інформацію змінної у html вигляді
        
        Returns
        -------
        html : str
            Інформація змінної у html вигляді
        
        """
        html = ('<p>{doc}</p>'
                '<p>{name}</p>')
        return html


class _Fun(_TreeElement):
    """Клас який описує методи класів Kotlin
    
    Attributes
    ----------
    name : str
        Ім'я методу
    doc : str
        Опис методу

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію методу у html вигляді
    
    """

    def __init__(self, name: str, doc: str = 'Опис відсутній'):
        """
        
        Parameters
        ----------
        name : str
            ім'я методу
        doc : str = 'Опис відсутній'
            Опис методу

        """

        self.name: str = name
        self.doc: str = doc

    def get_childs(self) -> List['_TreeElements']:
        """Метод який вертає дітеї цього об'єкту
        
        У цього об'єкту не може бути дітей, тому він вертає пустий 
        список.
        
        """

        return []

    def get_content(self) -> str:
        """Метод який вертає інформацію методу у html вигляді
        
        Returns
        -------
        html : str
            Інформація методу у html вигляді
        
        """
        html = ('<p>{doc}</p>'
                '<p>{name}</p>')
        return html


"""TODO x.x 
    інші класи які описують методи класів Kotlin
    такі як interface тощо. добавлю якщо побачу їх при тестуванні 
    модуля"""


class _Class(_TreeElement):
    """Клас який описує класи Kotlin

    Attributes
    ----------
    vars : List['_Var']
        Список змінних класу
    funcs : List['_Fun']
        Список методів класу
    classes : List['_Class']
        Список класів класу

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію класу у html вигляді

    """

    def __init__(self, data: str):
        """
        
        Parameters
        ----------
        data : str
            Строка в який передається інформація тільки класу.
        
        """
        self.vars: List['_Var'] = []
        self.funcs: List['_Fun'] = []
        self.classes: List['_Class'] = []
        # TODO >0.6 обробка інформації з змінної data

    def get_childs(self) -> List['_TreeElements']:
        """Метод який вертає дітеї цього об'єкту
        
        Returns
        -------
        : List['_TreeElements']
            Вертає дітей цього об'єкту
        
        """

        return self.classes + self.funcs + self.vars

    def get_content(self) -> str:
        """Метод який вертає інформацію класу у html вигляді
        
        Returns
        -------
        html : str
            Інформація методу у html вигляді
        
        """
        # TODO >0.6 Генерування html коду
        return ''
    

class _File(_Class):
    """Клас який описує файли Kotlin

    Attributes
    ----------
    vars : List['_Var']
        Список змінних класу
    funcs : List['_Fun']
        Список методів класу
    classes : List['_Class']
        Список класів класу

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію класу у html вигляді

    """

    def __init__(self, data: str):
        """
        
        Parameters
        ----------
        data : str
            Строка в який передається інформація тільки файлу.
        
        """
        self.package = ''
        # TODO >0.6 обробка інформації з змінної data

    def get_childs(self) -> List['_TreeElements']:
        """Метод який вертає дітеї цього об'єкту
        
        Returns
        -------
        : List['_TreeElements']
            Вертає дітей цього об'єкту
        
        """

        return super().get_childs()

    def get_content(self) -> str:
        """Метод який вертає інформацію файлу у html вигляді
        
        Returns
        -------
        html : str
            Інформація методу у html вигляді
        
        """
        # TODO >0.6 Генерування html коду
        return ''


class DocMaker:
    """Головний клас модуля який опрацьовує та генерує документацію.
    
    Attributes
    ----------
    file : int
        Парсинг інформації з одного файлу.
    dir : int
        Парсинг інформації з файлів каталогу.
    recursive : int
        Парсинг інформації з файлів каталогу та його підкаталогів.
    git : int
        Парсинг інформації з файлів git репозиторія.

    Methods
    -------
    parse(method: int, input_path: str, output_path: str = '')
        Клас метод - вхідна точка роботи класу.
        Робить обробку файлів з вхідної інформації.
    _parse_file(path_to_file: str)
        Обробка файлу
    _parse_dir(path_to_dir: str)
        Пошук файлів з вхідного каталогу.
    _parse_recursive(path_to_dir: str)
        Рекурсивний пошук файлів з 
        вхідного каталогу та його підкаталогів.
    _parse_git(path_to_git: str)
        Пошук файлів з git репозиторія.
    _write_doc(path_to_dir: str)
        Запис документації у html форматі.

    """

    file: int = 0
    dir: int = 1
    recursive: int = 2
    git: int = 3

    @classmethod
    def parse(cls, method: int, input_path: str, output_path: str = ''):
        """Обробка вхідної інформації
        
        Метод обробляє вхідну інформацію та передає інформацію 
        відповідним методам для подальшої роботи програми.

        Parameters
        ----------
        method : int
            Метод збору інформації.
        input_path : str
            Шлях вхідної точки для збору інформацію.
        output_path : str = ''
            Шлях збереження документації.

        Raises
        ------
        ValueError
            Якщо method не вірно вказан
        TypeError
            Якщо method, input_path, output_path мають неправильний тип.
        
        """

        # Перевірка правильності вхідних данних
        try:
            if not 0 <= method <= 3:
                raise ValueError('method повинен бути в діапазоні [0, 3]')
        except TypeError:
            raise TypeError('method повинен бути типу int')

        if type(input_path) != str:
            raise TypeError('input_path повинен бути типу str')

        if type(output_path) != str:
            raise TypeError('output_path повинен бути типу str')
        
        # Передача інформації для подальшої обробки
        doc_maker = cls()

        if method == doc_maker.file:
            doc_maker._parse_file(input_path)
        elif method == doc_maker.file:
            doc_maker._parse_dir(input_path)
        elif method == doc_maker.file:
            doc_maker._parse_recursive(input_path)
        elif method == doc_maker.file:
            doc_maker._parse_git(input_path)

        doc_maker._write_doc(output_path)

    def _parse_file(self, path_to_file: str):
        """Обробляє файли
        
        Метод відкриває файл та передає його на обробку класу _File.

        Parameters
        ----------
        path_to_dir : str
            Шлях до вхідного каталогу.
        
        """

        # TODO 0.6 Обробка файлу
        pass

    def _parse_dir(self, path_to_dir: str):
        """Пошук файлів з каталогу
        
        Метод шукає файли з каталогу та 
        передає їх методу _parse_file.

        Parameters
        ----------
        path_to_dir : str
            Шлях до вхідного каталогу.
        
        """

        # TODO >1.0 Збір файлів з каталогу
        pass

    def _parse_recursive(self, path_to_dir: str):
        """Рекурсивний пошук файлів
        
        Метод рекурсивно шукає файли з каталогів та підкаталогів та 
        передає їх методу _parse_file.

        Parameters
        ----------
        path_to_dir : str
            Шлях до вхідного каталогу.
        
        """

        # TODO >2.0 Збір файлів з каталогу
        pass

    def _parse_git(self, path_to_git: str):
        """Обробка git репозиторія
        
        Метод завантажує git репозиторій.
        Передає папку з репозиторієм методу _parse_recursive.
        Видаляє папку з репозиторієм.

        Parameters
        ----------
        path_to_git : str
            Шлях до git репозиторія.
        
        """

        # TODO >3.0 Збір файлів з git репозиторія
        pass

    def _write_doc(self, path_to_dir: str):
        """Генерує зібрану інформацію у HTML форматі.
        
        

        Parameters
        ----------
        path_to_dir : str
            Шлях де буде збережено документацію.
        
        """

        # TODO <1.0 Генерація документації
        pass


if __name__ == "__main__":
    argument_parser = ArgumentParser(
        description=__doc__, 
        formatter_class=RawDescriptionHelpFormatter,
        epilog='%(prog)s {}'.format(__version__),
    )
    
    argument_parser.add_argument(
        '-v', 
        '--version', 
        action='version',
        version='%(prog)s {}'.format(__version__),
        help='Відобразити версію програми.',
    )
    
    launch_group = argument_parser.add_mutually_exclusive_group(required=True)
    launch_group.add_argument(
        '-f',
        '--file',
        metavar='PATH',
        help=('Шлях до файлу, '
              'за якого потрібно зробити документацію.'),
    )
    launch_group.add_argument(
        '-d',
        '--dir',
        metavar='PATH',
        help=('Шлях до каталогу, '
              'з файлів якого потрібно зробити документацію.'),
    )
    launch_group.add_argument(
        '-r',
        '--recursive',
        metavar='PATH',
        help=('Шлях до каталогу, '
              'з файлів підкаталогів якого потрібно зробити документацію.'),
    )
    launch_group.add_argument(
        '-g',
        '--git',
        metavar='PATH',
        help=('Шлях до git репозиторія, '
              'з файлів підкаталогів якого потрібно зробити документацію.'),
    )

    argument_parser.add_argument(
        '-o',
        '--output',
        metavar='PATH',
        default='',
        help=('НЕОБОВ\'ЯЗКОВО '
              'Шлях до каталогу, де буде записано документацію.'
              'Якщо не вказано, документацію буде записано рядом з модулем'),
    )

    arguments = argument_parser.parse_args(argv[1:])
    
    if arguments.file:
        DocMaker.parse(DocMaker.file, arguments.file, arguments.output)
    elif arguments.dir:
        DocMaker.parse(DocMaker.dir, arguments.dir, arguments.output)
    elif arguments.recursive:
        DocMaker.parse(DocMaker.recursive, arguments.recursive, arguments.output)
    elif arguments.git:
        DocMaker.parse(DocMaker.git, arguments.git, arguments.output)
