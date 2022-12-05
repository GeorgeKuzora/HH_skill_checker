# HH skill checker
HH skill checker это программа для поиска информации о необходимых навыках на сайте hh.ru.
## Алгоритм работы программы
Программа производит запросы к сайту на основании введенных пользователем данных о регионе поиска и ключевом слове для запроса. Программа производит веб-скрапинг полученных страниц и находит списки необходимых навыков указанных работодателями. После получения списков навыков программа подчитывает количество каждого навыка и заносит эти данные в файл.
## Особенности программы
- Программа производит веб-скрапинг веб страниц без использования API.
- Программа использует библиотеку Beautiful soup для парсинга html кода.
- Программа иcпользует библиотеку asyncio для неблокирующих запросов к сайту. Благодаря этому достигается увеличение скорости алгоритма.
## Требуемые библиотеки
- Python > 3.5
- asyncio = 3.4.3
- aiohttp = 3.8.3
- aiounittest = 1.4.2
- beautifulsoup4 = 4.11.1
- requests = 2.28.1
