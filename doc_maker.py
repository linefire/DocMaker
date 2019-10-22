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
        DocMaker.parse(DocMaker.parse_file, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з каталогу:
        DocMaker.parse(DocMaker.parse_dir, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з каталогу та його підкаталогів:
        DocMaker.parse(DocMaker.parse_recursive, "path\\\\to\\\\file")
    Якщо потрібно документовати файли з git репозиторія:
        DocMaker.parse(DocMaker.parse_git, "path\\\\to\\\\file")
    
    Якщо потрібно зберегти документацію у окреме місце:
        DocMaker.parse(DocMaker.parse_file, "path\\\\to\\\\file", "path\\\\to\\\\dir")

"""

__version__ = '0.2'

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from sys import argv

# TODO 1.0 Збір інформації з файлу
# TODO 2.0 Збір інформації з файлів каталогу
# TODO 3.0 Збір інформації з файлів каталогу та підкаталогів
# TODO 4.0 Збір інформації з git репозиторію
# TODO <1.0 Генерування документації у html вигляді
# TODO <1.0 Підключити bootstrap 4.3.x
# TODO 5.0 Дизайн документації


"""TODO 0.5 _TreeElement
    Так як всі об'єкти будуть належати дереву об'єктів, треба зробити
    базовий клас для всіх таких об'єктів"""
"""TODO 0.5.1 _Class(_TreeElement)
    Клас який описує класи Kotlin"""
"""TODO 0.5.2 _File(_Class)
    Клас який доповнює _Class тому що, файл містить в собі все те 
    що містить простий клас Kotlin але не може містити в собі:
    імпорти, інформацію пакету, та ім'я файлу."""
"""TODO 0.5.3 _Fun(_TreeElement) 
    Клас який описує методи класів Kotlin"""
"""TODO 0.5.4 _Var(_TreeElement)
    Клас який описує змінні класів Kotlin"""
"""TODO >0.5.4 
    інші класи які описують методи класів Kotlin
    такі як interface тощо."""



class DocMaker:
    """Головний клас модуля який опрацьовує та генерує документацію.
    
    Attributes
    ----------
    parse_file : int
        Парсинг інформації з одного файлу.
    parse_dir : int
        Парсинг інформації з файлів каталогу.
    parse_recusive : int
        Парсинг інформації з файлів каталогу та його підкаталогів.
    parse_git : int
        Парсинг інформації з файлів git репозиторія.

    Methods
    -------
    parse()
        Клас метод - вхідна точка роботи класу.
        Робить обробку файлів з вхідної інформації.
    _parse_file()
        Обробка файлу
    _parse_dir()
        Пошук файлів з вхідного каталогу.
    _parse_recursive()
        Рекурсивний пошук файлів з 
        вхідного каталогу та його підкаталогів.
    _parse_git()
        Пошук файлів з git репозиторія.
    _write_doc()
        Запис документації у html форматі.

    """

    parse_file: int = 0
    parse_dir: int = 1
    parse_recusive: int = 2
    parse_git: int = 3

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
        
        """

        # TODO 0.4 Обробка файлів з вхідної інформації
        pass

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
        help=('НЕОБОВ\'ЯЗКОВО '
              'Шлях до каталогу, де буде записано документацію.'
              'Якщо не вказано, документацію буде записано рядом з модулем'),
    )

    arguments = argument_parser.parse_args(argv[1:])
    # TODO 0.3 продовжити роботу програми за вказаними аргументами
