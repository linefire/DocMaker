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

__version__ = '0.8.1'

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from sys import argv
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from os.path import join
from os.path import exists
from os.path import basename
from os.path import dirname
from os import makedirs
from re import search
from re import findall
from re import compile as re_compile
from datetime import datetime
from shutil import rmtree
from shutil import copytree

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
        self.doc: str = 'Опис відсутній'
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

        html = '<li class="caret"><a href="{}">{}</a></li>'.format(self.path, self.name)
        childs = self.get_childs()
        if childs:
            html += '<ul class="nested">'
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

    def get_alphabetical_index(self) -> str:
        """Метод віддає список імен у документації в html вигляді"""

        objects = self.get_all_childs()
        objects = sorted(objects, key=lambda o: o.name)

        html = ''
        for object_ in objects:
            if type(object_) is not _File:
                html += '<li><a href="{path}">{name}</a></li>'.format(
                    name=object_.name,
                    path=object_.path,
                )
        return html

    def get_all_childs(self) -> List['_TreeElement']:
        """Метод віддає список дітей і себе"""

        childs = []
        for child_ in self.get_childs():
            childs += child_.get_all_childs()
        childs.append(self)
        return childs

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

    def __init__(self, name: str, path: str, 
                 parent: Optional[_TreeElement] = None,
                 doc: str = None):
        """
        
        Parameters
        ----------
        name : str
            ім'я методу
        doc : str = 'Опис відсутній'
            Опис методу

        """

        super().__init__(name, path, parent)

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

        html = (
            '<li>Опис функції {doc}</li>'
            '<li id="{id}">fun {name}</li>'
        ).format(
            doc='',
            name=self.name,
            id=self.path.split('#')[1],
        )
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
    objects_pattern : re.Pattern
        Шаблон за яким знаходить об'єкти в коді

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію класу у html вигляді
    _get_objects(data):
        Метод знаходить об'єкти в коді

    """

    objects_pattern = re_compile(
        r'(\/\*[\s\S]*?\*\/|)'  # G1 Опис класу або нічого
        r'(\s+|)'               # G2 Пробіл або нічого
        r'(\w+|)'               # G3 Тип класу або нічого
        r'(\s+|)'               # G4 Пробіл або нічого
        r'(class)'              # G5 Слово class
        r'(\s+|)'               # G6 Пробіл або нічого
        r'(\w+)'                # G7 Ім'я класу
        r'(\s+|)'               # G8 Пробіл або нічого
        r'(\:|)'                # G9 Роздільник або нічого
        r'(\s+|)'               # G10 Пробіл або нічого
        r'(\w+\(.*?\)|)'        # G11 Ім'я класу родителя або нічого
        r'(\s+|)'               # G12 Пробіл або нічого
        r'(\{)'                 # G13 Відкриваюча скобка тіла класу
        r'|'                    # Далі йде патерн для функції
        r'(\/\*[\s\S]*?\*\/|)'  # G14 Опис функції або нічого
        r'(\s+|)'               # G15 Пробіл або нічого
        r'(\w+|)'               # G16 Тип функції або нічого
        r'( +|)'                # G17 Пробіл або нічого
        r'(fun)'                # G18 Слово fun
        r'(\s+|)'               # G19 Пробіл або нічого
        r'(\w+)'                # G20 Ім'я функції
        r'(\s+|)'               # G21 Пробіл або нічого
        r'(\(.*?\))'            # G22 Параметри функції
        r'(\s+|)'               # G23 Пробіл або нічого
        r'(\:|)'                # G24 Роздільник або нічого
        r'(\s+|)'               # G25 Пробіл або нічого
        r'(\w+|)'               # G26 Тип значення що повертається
        r'(\s+|)'               # G27 Пробіл або нічого
        r'(\{)'                 # G28 Відкриваюча скобка тіла класу
    )

    def __init__(self, data: str, name: str, path: str, 
                 parent: Optional[_TreeElement] = None,
                 doc: Optional[str] = None):
        """
        
        Parameters
        ----------
        data : str
            Строка в який передається інформація тільки класу.
        name : str
            Ім'я класу
        path : str
            Шлях до файлу у документації
        parent : _TreeElement
            Батько цього об'єкту
        doc : str
            Опис класу
        
        """

        super().__init__(name, path, parent)

        self.vars: List['_Var'] = []
        self.funcs: List['_Fun'] = []
        self.classes: List['_Class'] = []

        self._get_objects(data)

    def _get_objects(self, data: str):
        """Метод знаходить об'єкти в коді

        Метод шукає в коді об'єкти за регулярним вираженням
        Коли знаходить, создає новий об'єкт за інформацією
        Зтирає ділянок коду з цим об'єктом
        Шукає заново новий об'єкт
        Поки нічого не знайде

        Parameters
        ----------
        data : str
            Код
        
        """

        # Каталог для цього об'єкту
        doc_path = self.path
        if type(self) is _File:
            doc_path += '#'

        # Цикл який шукає об'єкти
        while True:
            # Знаходимо наступний об'єкт
            object_ = search(self.objects_pattern, data)
            # Якщо немає, виходимо з циклу
            if object_ is None:
                break
            
            if object_.group(5):
                # Позиції де починаєтся і закінчуєтся тіло класу
                start_pos_parentless = object_.start(13)
                end_pos_parentless = self._get_body(data, start_pos_parentless)
                
                # Создаємо клас та добавляємо у список класів
                class_ = _Class(
                    data[start_pos_parentless:end_pos_parentless], 
                    object_.group(7),
                    join(doc_path, object_.group(7)),
                    self,
                )
                self.classes.append(class_)
            if object_.group(18):
                # Позиції де починаєтся і закінчуєтся тіло функції
                start_pos_parentless = object_.start(28)
                end_pos_parentless = self._get_body(data, start_pos_parentless)
                
                # Создаємо клас та добавляємо у список функцій
                fun_ = _Fun( 
                    object_.group(20),
                    join(doc_path, object_.group(20)),
                    self,
                )
                self.funcs.append(fun_)

            # Зтираємо інформацію про цей об'єкт
            data = data[:object_.start()] + data[end_pos_parentless:]

    @staticmethod
    def _get_body(data: str, start_pos_parentless: int) -> int:
        """Метод визначає тіло об'єкту рахуючи скобки"""
        distance_from_start = 0
        count_parentless = 0
        # Цикл який знаходить тіло класу, рахуючі фігурні скобки 
        while True:
            current_char_pos = start_pos_parentless + distance_from_start
            if data[current_char_pos] == '{':
                count_parentless += 1
            if data[current_char_pos] == '}':
                count_parentless -= 1
            if count_parentless == 0:
                break
            distance_from_start += 1
        return current_char_pos
            
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

        if type(self) is _Class:
            id_ = self.path.split('#')[1]
            html = (
                '<p>Опис класу {doc}</p>'
                '<li id="{id}"><span>class {name}</span>'
                '<ul>{{class_childs}}</ul></li>'
            ).format(
                doc='',
                name=self.name,
                id=id_,
            )
        else:
            html = '{class_childs}'

        class_childs = ''
        for object_ in self.get_childs():
            class_childs += object_.get_content()
        html = html.format(class_childs=class_childs)

        return html
    

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

    def __init__(self, data: str, name: str, path: str,
                 parent: Optional[_TreeElement] = None):
        """
        
        Parameters
        ----------
        data : str
            Строка в який передається інформація тільки файлу.
        name : str
            Ім'я файлу
        path : str
            Шлях до файлу у документації
        parent : _TreeElement
            Батько об'єкту
        
        """

        super().__init__(data, name, path, parent)


        self.package = self._get_package(data)
        self.imports = self._get_imports(data)
        self.doc = self._get_doc(data)

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

        file_template = open(join('source', 'file_content_template.html'), 'r', 
                             encoding='utf-8').read()

        imports = ['<li>import {}</li>'.format(i) for i in self.imports]

        html = file_template.format(
            filename=self.name,
            doc=self.doc,
            package=self.package,
            imports=''.join(imports),
            content=super().get_content(),
        )
        return html

    @staticmethod
    def _get_doc(data: str) -> str:
        doc = search(r'([\s]+|)\/\*[\s\S]*?\*\/', data)
        if doc:
            doc = doc.group(0).strip()
        else:
            doc = 'Опис відсутній'
        doc = doc.replace('\n', '<br>')
        return doc

    @staticmethod
    def _get_package(data: str) -> str:
        """Метод аналізує данні та знаходить пакет файлу."""
        package = search(r'(?<=package).+', data).group(0).strip()
        return package

    @staticmethod
    def _get_imports(data: str) -> List[str]:
        """Метод аналізує данні та віддає список імпортів файлу."""
        imports = [i.strip() for i in findall(r'(?<=import).+', data)]
        return imports


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

    def __init__(self):
        self._root_element: Optional['_TreeElement'] = None

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

        Raises
        ------
        TypeError
            Файл не належить до язика програмування Kotlin
        FileNotFoundError
            Файл не знайдено
        
        """

        # Перевірка правильності шляху
        if path_to_file.split('.')[-1] != 'kt':
            raise TypeError('Файл не належить до '
                            'язика програмування Kotlin')

        if not exists(path_to_file):
            raise FileNotFoundError('Файл "{}" не'
                                    'знайдено.'.format(path_to_file))

        doc_path = basename(path_to_file).split('.')[0] + '.html'
        with open(path_to_file, 'r', encoding='utf-8') as file:
            self._root_element = _File(file.read(), 
                                       basename(path_to_file),
                                       doc_path,
                                       None,
            )


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

        # Перевірка на існування кінцевого каталогу, та предостереження юзера
        if exists(path_to_dir):
            while True:
                print(('Такий каталог "{}" вже існує, якщо продовжити' 
                      '- вся інформація в ньому буде знищена').format(path_to_dir))
                command = input('Продовжити? [Y(продовжити)\\N(відмінити)]'
                                ' - оберіть команду: ')
                if command.lower() == 'y':
                    break
                elif command.lower() == 'n':
                    exit()
                else:
                    print('Неправильна команда.')

            # Якщо юзер продовжив роботу програми, видаляємо папку
            rmtree(path_to_dir)  
        
        # Создаємо кінцеву папку в яку будемо зберігати документацію
        makedirs(path_to_dir)  

        copytree(join('source', 'css'), join(path_to_dir, 'css'))
        copytree(join('source', 'js'), join(path_to_dir, 'js'))

        page_template = open(join('source', 'page_template.html'), 'r', 
                             encoding='utf-8').read()
        
        page_template = page_template.format(
            project_name=self._root_element.name,
            date=datetime.now().strftime('%d.%m.%Y %H:%M'),
            version=__version__,
        )

        
        with open(join(path_to_dir, 'index.html'), 'w', 
                  encoding='utf-8') as file:
            file.write(page_template.format(
                page_content='',
                tree=self._root_element.get_tree_from_root(),
                alphabet=self._root_element.get_alphabetical_index(),
            ))

        for object_ in [self._root_element] + self._root_element.get_childs():

            if type(object_) is _File:
                makedirs(join(path_to_dir, dirname(object_.path)), 
                         exist_ok=True)

                with open(join(path_to_dir, object_.path), 'w', 
                          encoding='utf-8') as file:
                    file.write(
                        page_template.format(
                            page_content=object_.get_content(),
                            tree=self._root_element.get_tree_from_root(),
                            alphabet=self._root_element.get_alphabetical_index(),
                        ) 
                    )


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
