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
    d) Файли з git репозиторію. - у розробці до верії 4.0
5.Модуль генерує документацію у вигляді html сторінок.
6.Модуль генерує html сторінки з використанням технології bootstrap.

Примери застосування модуля:
Запуск модуля:
    Якщо потрібно документовати файл:
        python doc_maker.py -f "path\\\\to\\\\file"
    Якщо потрібно документовати файли з каталогу:
        python doc_maker.py -d "path\\\\to\\\\dir"
    Якщо потрібно документовати файли з каталогу та його підкаталогів:
        python doc_maker.py -r "path\\\\to\\\\dir"
    Якщо потрібно документовати файли git репозиторію:
        python doc_maker.py -g "path\\\\to\\\\git"
    
    Якщо потрібно зберегти документацію у окреме місце:
        python doc_maker.py -g "path\\\\to\\\\git" -o "path\\\\to\\\\dir"

"""

__version__ = '0.1'

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

"""TODO 0.2 Добавити головний клас який буде 
опрацьвовати та генерувати докуентацію""" 


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
        help=('Шлях до git репозиторію, '
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
