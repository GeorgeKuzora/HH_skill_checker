def page_with_links():
    page = '''
<!doctype html>
<html class="no-js" lang="">

<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Untitled</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <!-- Place favicon.ico in the root directory -->

</head>

<body>
    <!--[if lt IE 8]>
            <p class="browserupgrade">
            You are using an <strong>outdated</strong> browser. Please
            <a href="http://browsehappy.com/">upgrade your browser</a> to improve
            your experience.
            </p>
        <![endif]-->
    <span data-page-analytics-event="vacancy_search_suitable_item">
    <a class="serp-item__title" data-qa="serp-item__title" target="_blank" href="https://spb.hh.ru/vacancy/72685558?from=vacancy_search_list&amp;hhtmFrom=vacancy_search_list&amp;query=python">Python - разработчик</a>
    </span>

</body>

</html>
    '''
    return page

def page_without_links():
    page = '''
<!doctype html>
<html class="no-js" lang="">

<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Untitled</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <!-- Place favicon.ico in the root directory -->

</head>

<body>
    <!--[if lt IE 8]>
            <p class="browserupgrade">
            You are using an <strong>outdated</strong> browser. Please
            <a href="http://browsehappy.com/">upgrade your browser</a> to improve
            your experience.
            </p>
        <![endif]-->

</body>

</html>
    '''
    return page

def page_with_skills():
    page = '''
<!doctype html>
<html class="no-js" lang="">

<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Untitled</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <!-- Place favicon.ico in the root directory -->

</head>

<body>
    <div>
        <div class="bloko-tag-list">
            <div class="bloko-tag bloko-tag_inline" data-qa="bloko-tag bloko-tag_inline skills-element">
                <span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">Python</span>
            </div>
            <div class="bloko-tag bloko-tag_inline" data-qa="bloko-tag bloko-tag_inline skills-element">
                <span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">Git</span>
            </div>
            <div class="bloko-tag bloko-tag_inline" data-qa="bloko-tag bloko-tag_inline skills-element">
                <span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">Django Framework</span>
            </div>
            <div class="bloko-tag bloko-tag_inline" data-qa="bloko-tag bloko-tag_inline skills-element">
                <span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">PostgreSQL</span>
            </div>
            <div class="bloko-tag bloko-tag_inline" data-qa="bloko-tag bloko-tag_inline skills-element">
                <span class="bloko-tag__section bloko-tag__section_text" data-qa="bloko-tag__text">Docker</span>
            </div>
        </div>
    </div>
</body>

</html>
    '''
    return page
