"""Модуль який робить документацію для язика програмування 'Kotlin'.

УВАГА: Модуль у розробці, окремі функції не працюють.

1.Модуль робить документацію з програмних кодів 
язика програмування 'Kotlin'.
2.Модуль можна імпортувати або запустити.
3.Модуль не потребує сторонніх бібліотек.
4.Модуль може опрацювати:
    a) Окремий файл.
    b) Файли каталогу.
    с) Файли каталогу та підкаталогів.
    d) Файли з git репозиторія.
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

__version__ = '5.0'

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
from os.path import isfile
from os.path import split
from os import walk
from os import listdir
from os import makedirs
from os import system
from os import access
from os import chmod
from os import W_OK
from stat import S_IWUSR
from re import search
from re import findall
from re import sub
from re import compile as re_compile
from datetime import datetime
from shutil import rmtree
from shutil import copytree


def remove_error(func, path, exc_info):
    # Якщо не видалився файл пробуємо змінити його права
    if not access(path, W_OK):
        chmod(path, S_IWUSR)
        func(path)


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
    doc : str
        Опис об'єкту

    Methods
    -------
    get_tree_from_root()
        Вертає дерево дітей у html форматі відносно кореневого елементу
    get_tree()
        Вертає дерево дітей у html форматі
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію об'єкту у html вигляді
    get_name_with_type(object_: '_TreeElement')
        Вертає тип + ім'я об'єкту відносно типу
    get_alphabetical_index()
        Вертає алфавітний показчик
    get_all_childs()
        Вертає список всых дытей цього об'єкту
    
    """

    def __init__(self, name: str, path: str,
                 parent: Optional['_TreeElement'] = None,
                 level: int = 0):
        """Конструктор класу _TreeElement

        Parameters
        ----------
        name : str
            Ім'я яке буде відображено у дереві документації
        path : str
            Відносний шлях до об'єкту у документації
        parent : Optional['_TreeElement']
            Батько об'єкту
        level : int
            Рівень вкладеності об'єкта у документації
        
        """

        self.name: str = name
        self.doc: str = 'Опис відсутній'
        self.path: str = path
        self.parent: Optional['_TreeElement'] = parent

        if parent and not level:
            self.level = parent.level
        else:
            self.level = level

    def get_tree_from_root(self, level: int = 0) -> str:
        """Вертає дерево у html форматі відносно кореневого елементу

        Метод знаходить корневий eлемент дерева, та вертає html
        сторінку з метода get_tree.

        Parameters
        ----------
        level : int
            Рівень вкладеності файлу у документації

        Returns
        -------
        self.get_tree : str
            Вертає дерево у вигляді html коду відносно корeневого 
            елементу.

        """

        if self.parent:
            return self.parent.get_tree_from_root(level)
        else:
            return self.get_tree(level)

    def get_tree(self, level: int = 0) -> str:
        """Вертає дерево своїх дітей у html форматі

        Метод рекурсивно вертає дерево змісту у html форматі.

        Parameters
        ----------
        level : int = 0
            Рівень вкладеності файлу у документації

        Returns
        -------
        html : str
            Вертає html код дерева змісту себе та своїх дітей.
        
        """
 
        childs = self.get_childs()
        if childs:
            html = ('<li>'
                    '<span class="caret">'
                    '<a class="tree-item" href="{}{}">{}</a>'
                    '</span>'
                   ).format(
                        '../' * level,
                        self.path, 
                        self.get_name_with_type(self),
                   )
            html += '<ul class="nested">'
            for child in childs:
                html += child.get_tree(level)
            html += '</ul></li>'
        else:
            html = (
                '<li><a class="tree-item" href="{}{}">{}</a></li>'
            ).format(
                '../' * level,
                self.path, 
                self.get_name_with_type(self),
            )
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

    @staticmethod
    def get_name_with_type(object_: '_TreeElement') -> str:
        """Модуль віддає тип обє'кту + ім'я відносно типу"""
        if type(object_) is _File:
            name = 'file {}'.format(object_.name)
        if type(object_) is _Class:
            name = 'class {}'.format(object_.name)
        if type(object_) is _Fun:
            name = 'fun {}'.format(object_.name)
        if type(object_) is _Var:
            if object_.fullname.__contains__(' var '):
                var_type = 'var'
            else:
                var_type = 'val' 
            name = '{} {}'.format(var_type, object_.name)
        if type(object_) is _Dir:
            name = 'dir {}'.format(object_.name)
        return name

    def get_alphabetical_index(self, level: int = 0) -> str:
        """Метод віддає список імен у документації в html вигляді"""

        objects = self.get_all_childs()
        objects = sorted(objects, key=lambda o: o.name.lower())

        html = ''
        for object_ in objects:
            name = self.get_name_with_type(object_)
            if type(object_) not in [_File, _Dir]:
                html += ('<li><a class="tree-item" href="{level}{path}">'
                         '{name}</a></li>'
                ).format(
                    level='../' * level,
                    name=name,
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
    fullname : str
        Повна інформація змінної

    Methods
    -------
    get_childs()
        Вертає список дітей цього об'єкту
    get_content()
        Вертає інформацію змінної у html вигляді
    
    """

    def __init__(self, name: str, path: str, fullname: str = '',
                 parent: _TreeElement = None,
                 doc: str = 'Опис відсутній'):
        """
        
        Parameters
        ----------
        name : str
            Ім'я змінної
        path : str
            Шлях до об'єкту у документації
        fullname : str = ''
            Повна інформація змінної
        parent : _TreeElement = None
            Батько об'єкту
        doc : str = 'Опис відсутній'
            Опис змінної

        """

        super().__init__(name, path, parent)
        
        self.fullname: str = fullname
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
        html = '<p id={id}>{doc}<br>{name}</p>'.format(
            name=self.fullname,
            doc=self.doc,
            id=self.path.split('#')[1],
        )
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

    def __init__(self, name: str, path: str, fullname: str = '',
                 parent: Optional[_TreeElement] = None,
                 doc: str = 'Опис відсутній'):
        """
        
        Parameters
        ----------
        name : str
            Скорочене ім'я методу
        fullname : str
            Повне ім'я методу
        parent : _TreeElement
            Батько об'єкту
        doc : str = 'Опис відсутній'
            Опис методу

        """

        super().__init__(name, path, parent)

        self.fullname = fullname
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
            '<li id="{id}"><span>{name}</span></li>'
            '<ul>{doc}</ul><br>'
        ).format(
            doc=self.doc,
            name=self.fullname,
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
        r'( +|)'                # G4 Пробіл або нічого
        r'(class)'              # G5 Слово class
        r'(\s+|)'               # G6 Пробіл або нічого
        r'(\w+)'                # G7 Ім'я класу
        r'(\s+|)'               # G8 Пробіл або нічого
        r'(\:|)'                # G9 Роздільник або нічого
        r'(\s+|)'               # G10 Пробіл або нічого
        r'(\w+|)'               # G11 Ім'я класу родителя або нічого
        r'(\(.*?\)|)'           # G12 Параметри класу родителя
        r'(\s+|)'               # G13 Пробіл або нічого
        r'(\{)'                 # G14 Відкриваюча скобка тіла класу
        r'|'                    # Далі йде патерн для функції
        r'(\/\*[\s\S]*?\*\/|)'  # G15 Опис функції або нічого
        r'(\s+|)'               # G16 Пробіл або нічого
        r'(\w+|)'               # G17 Тип функції або нічого
        r'( +|)'                # G18 Пробіл або нічого
        r'(fun|constructor)'    # G19 Слово fun або constructor
        r'(\s+|)'               # G20 Пробіл або нічого
        r'(\w+)'                # G21 Ім'я функції
        r'(\s+|)'               # G22 Пробіл або нічого
        r'(\(.*?\))'            # G23 Параметри функції
        r'(\s+|)'               # G24 Пробіл або нічого
        r'(\:|)'                # G25 Роздільник або нічого
        r'(\s+|)'               # G26 Пробіл або нічого
        r'(\w+|)'               # G27 Тип значення що повертається
        r'(\s+|)'               # G28 Пробіл або нічого
        r'(\{)'                 # G29 Відкриваюча скобка тіла класу
        r'|'                    # Далі йде патерн для змінних
        r'(\/\*[\s\S]*?\*\/|)'  # G30 Опис функції або нічого
        r'(\s+|)'               # G31 Пробіл або нічого
        r'(\w+|)'               # G32 Тип змінної або нічого
        r'( +|)'                # G33 Пробіл або нічого
        r'(val|var)'            # G34 Слово var або val
        r'(\s+|)'               # G35 Пробіл або нічого
        r'(\w+)'                # G36 Ім'я змінної
        r'(\s+|)'               # G37 Пробіл або нічого
        r'(\:|)'                # G38 Роздільник або нічого
        r'(\s+|)'               # G39 Пробіл або нічого
        r'(\w+|)'               # G40 Тип змінної
        r'(\s+|)'               # G41 Пробіл або нічого
        r'(\=|)'                # G42 Дорівнює або нічого
        r'(.+|)'                # G43 Значення змінної або нічого
    )

    def __init__(self, data: str, name: str, path: str, fullname: str = '', 
                 parent: Optional[_TreeElement] = None, 
                 doc: Optional[str] = None,
                 level: int = 0):
        """
        
        Parameters
        ----------
        data : str
            Строка в який передається інформація тільки класу.
        name : str
            Скорочене ім'я класу
        fullname : str
            Повне ім'я класу
        path : str
            Шлях до файлу у документації
        parent : _TreeElement
            Батько цього об'єкту
        doc : str
            Опис класу
        
        """

        super().__init__(name, path, parent, level)

        self.fullname = fullname
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
                start_pos_parentless = object_.start(14)
                end_pos_parentless = self._get_body(data, start_pos_parentless)
                
                fullname = ' '.join([
                    object_.group(3), object_.group(5), object_.group(7), 
                    object_.group(9), object_.group(11) + object_.group(12),
                ])
                # Создаємо клас та добавляємо у список класів
                class_ = _Class(
                    data[start_pos_parentless:end_pos_parentless], 
                    object_.group(7),
                    join(doc_path, object_.group(7)),
                    fullname,
                    self,
                )
                self.classes.append(class_)
            if object_.group(19):
                # Позиції де починаєтся і закінчуєтся тіло функції
                start_pos_parentless = object_.start(29)
                end_pos_parentless = self._get_body(data, start_pos_parentless)
                
                fullname = ' '.join([
                    object_.group(17), object_.group(19), 
                    object_.group(21) + object_.group(23), 
                    object_.group(25), object_.group(27),
                ])
                # Создаємо клас та добавляємо у список функцій
                fun_ = _Fun( 
                    object_.group(21),
                    join(doc_path, object_.group(21)),
                    fullname,
                    self,
                )
                self.funcs.append(fun_)
            if object_.group(34):
                end_pos_parentless = object_.end()

                fullname = ' '.join([
                    object_.group(32), object_.group(34), 
                    object_.group(36), object_.group(38), 
                    object_.group(40), object_.group(42),
                    object_.group(43),
                ])
                var_ = _Var( 
                    object_.group(36),
                    join(doc_path, object_.group(36)),
                    fullname,
                    self,
                )
                self.vars.append(var_)

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
        
        return self.classes + self.vars + self.funcs 

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
                '<li id="{id}"><span>{name}</span>'
                '<ul><p>{doc}</p><br>{{class_childs}}</ul>'
            ).format(
                doc=self.doc,
                name=self.fullname,
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
                 parent: Optional[_TreeElement] = None,
                 level: int = 0):
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

        super().__init__(data, name, path, '', parent, '', level)

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

        file_template = open(join('source', 'file_content_template.html'), 
                             'r', encoding='utf-8').read()

        imports = []
        for import_ in self.imports:
            imports.append(('<li><b style="color: darkred;">'
                            'import</b> {}</li>').format(import_))

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
        doc = search(r'^([\s]+|)\/\*[\s\S]*?\*\/', data)
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


class _Dir(_TreeElement):
    """Класс який описує каталог коду
    
    """

    def __init__(self, name: str, path: str, 
                 parent: Optional['_TreeElement'] = None,
                 level: int = 0):
        
        super().__init__(name, path, parent, level)

        self.files: List[_File] = []
        self.dirs: List['_Dir'] = []

    def get_childs(self):
        return self.dirs + self.files

    def get_content(self):
        html = '<h1>Каталог {}</h1>'.format(basename(self.name))
        html += '<h3>Каталоги</h3>'
        html += '<ul>'
        for dir_ in self.dirs:
            html += '<li><a href="{level}{link}">dir {name}</a></li>'.format(
                name=dir_.name, 
                link=dir_.path,
                level='../' * self.level,
            )
        html += '</ul>'
        html += '<h3>Файли</h3>'
        html += '<ul>'
        for file_ in self.files:
            html += '<li><a href="{level}{link}">file {name}</a></li>'.format(
                name=file_.name, 
                link=file_.path,
                level='../' * self.level,
            )
        html += '</ul>'
        return html

    def add_file(self, name: str, path: str, data: str):
        for dir_ in self.dirs:
            if path.__contains__(dir_.path.split('.')[0]):
                dir_.add_file(name, path, data)
                break
        else:
            self.files.append(_File(
                data,
                name,
                path,
                self,
                self.level + 1,
            ))

    def add_dir(self, path: str, name: str, level: int = 0):
        for dir_ in self.dirs:
            if path.__contains__(dir_.path.split('.')[0]):
                dir_.add_dir(path, name)
                break
        else:
            self.dirs.append(_Dir(
                name,
                path,
                self,
                self.level + 1,
            ))

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
    _root_element : Optional[_TreeElement]
        Корневий елемент дерева об'єктів

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
        elif method == doc_maker.dir:
            doc_maker._parse_dir(input_path)
        elif method == doc_maker.recursive:
            doc_maker._parse_recursive(input_path)
        elif method == doc_maker.git:
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

        dir_ = _Dir(
            basename(path_to_dir),
            basename(path_to_dir) + '.html',
        )
        self._root_element = dir_

        for object_ in listdir(path_to_dir):
            if (isfile(join(path_to_dir, object_)) and 
                object_.split('.')[1] == 'kt'):

                doc_path = join(
                    basename(path_to_dir), 
                    object_.split('.')[0] + '.html',
                )
                with open(join(path_to_dir, object_), 
                          'r', encoding='utf-8') as file:
                    name = basename(join(path_to_dir, object_))
                    self._root_element.add_file(
                                            name,
                                            doc_path,
                                            file.read(),
                    )

        
    def _parse_recursive(self, path_to_dir: str):
        """Рекурсивний пошук файлів
        
        Метод рекурсивно шукає файли з каталогів та підкаталогів та 
        передає їх методу _parse_file.

        Parameters
        ----------
        path_to_dir : str
            Шлях до вхідного каталогу.
        
        """

        dir_ = _Dir(
            basename(path_to_dir),
            basename(path_to_dir) + '.html',
        )
        self._root_element = dir_

        path_to_delete, _ = split(path_to_dir)
        for root, dirs, files in walk(path_to_dir):
            relative_path = root.replace(path_to_delete, '')[1:]
            for dir_ in dirs:
                if dir_.__contains__('.'):
                    continue
                self._root_element.add_dir(
                    join(relative_path, dir_ + '.html'), 
                    dir_,
                )
            for file_ in files:
                try:
                    if file_.split('.')[1] != 'kt':
                        continue
                except IndexError:
                    continue

                with open(join(root, file_), 'r', encoding='utf-8') as file:
                    self._root_element.add_file(
                        file_,
                        join(relative_path, file_.split('.')[0] + '.html'),
                        file.read(),
                    )
        
        # Видаляємо непотрібні каталоги
        for object_ in self._root_element.get_all_childs():
            if type(object_) is _Dir:
                if not object_.get_childs():
                    object_.parent.dirs.remove(object_)
                elif len(object_.get_childs()) == 1:
                    dir_ = object_.get_childs()[0]
                    if type(dir_) is not _Dir:
                        continue
                    
                    if object_.parent:
                        object_.parent.dirs.remove(object_)
                        object_.parent.dirs.append(dir_)
                        dir_.name = join(object_.name, dir_.name)

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

        name = basename(path_to_git).split('.')[0]

        system('git clone {}'.format(path_to_git))

        self._parse_recursive(name)
        
        rmtree(name, onerror=remove_error)

    def _write_doc(self, path_to_dir: str):
        """Генерує зібрану інформацію у HTML форматі.
        
        Parameters
        ----------
        path_to_dir : str
            Шлях де буде збережено документацію.
        
        """

        if not path_to_dir:
            path_to_dir = 'documentions'

        name = self._root_element.name.split('.')[0]
        path_to_dir = join(path_to_dir, name)

        # Перевірка на існування кінцевого каталогу, та предостереження юзера
        if exists(path_to_dir):
            while True:
                print(('Такий каталог "{}" вже існує, якщо продовжити' 
                      '- вся інформація в ньому буде знищена'
                      ).format(path_to_dir))
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

        index_content = """
        <div class="row d-flex align-self-center">
            <div class="col-12">
                <h1>{project_name}</h1>
                <h1>Згенеровано {date}</h1>
                <h1>Завдяки DocMaker {version}</h1>
            </div>
        </div>""".format(
            project_name=self._root_element.name,
            date=datetime.now().strftime('%d.%m.%Y %H:%M'),
            version=__version__,
        )
        
        with open(join(path_to_dir, 'index.html'), 'w', 
                  encoding='utf-8') as file:
            file.write(page_template.format(
                level='',
                page_content=index_content,
                tree=self._root_element.get_tree_from_root(0),
                alphabet=self._root_element.get_alphabetical_index(),
            ))

        for object_ in self._root_element.get_all_childs():

            if type(object_) is _File or type(object_) is _Dir:
                try:
                    makedirs(join(path_to_dir, dirname(object_.path)), 
                            exist_ok=True)
                except FileExistsError:
                    pass

                with open(join(path_to_dir, object_.path), 'w', 
                          encoding='utf-8') as file:
                    re = self._root_element
                    html = page_template.format(
                        level='../' * object_.level,
                        page_content=object_.get_content(),
                        tree=re.get_tree_from_root(object_.level),
                        alphabet=re.get_alphabetical_index(object_.level),
                    )
                    html = self.get_style(html)
                    file.write(html)

    @staticmethod
    def get_style(html: str) -> str:
        """Добавляє стилі по відведеним крітеріям в HTML"""

        html = sub(
            (
                r'(?<!\w)'
                r'(class|fun|override|inner|var|dir|file|val|open)'
                r'(?!=\w|\=)'
            ),
                '<b style="color: darkred;">\g<1></b>',
                html,
        )
        html = sub(
            r'(Опис відсутній)',
            '<small style="color: lightgray;">\g<1></small>',
            html,
        )
        return html


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
