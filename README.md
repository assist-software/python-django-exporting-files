# python-django-exporting-files

This is a Python/Django app which displays how simple it is to export Excel and PDF files.

For creating Excel files we're using [XlsxWriter](http://xlsxwriter.readthedocs.org/) module. The code contains information on how to add data to the Excel file, how to resize columns and rows, and also how to add charts. For more details read this article: [How to export Excel files in a Python/Django application](http://assist-software.net/blog/how-export-excel-files-pythondjango-application).

For creating PDF files we're using [ReportLab](http://www.reportlab.com/documentation/) library. The code contains information on how to create PDF documents, how to add paragraphs, tables or charts. For more details read this article: [How to create PDF files in a Python/Django application using ReportLab](http://assist-software.net/blog/how-create-pdf-files-python-django-application-using-reportlab)

This application is developed by the awesome [ASSIST Software](http://assist-software.net/) team.

How to install the application
------------------------------

- Clone the code from git.
- Create an environment using [virtualenv](https://virtualenv.pypa.io/en/latest/) and activate it.
- Install the project dependencies with [pip](https://pip.pypa.io/en/latest/installing.html). Run this command: `pip install -r requirements.txt` while being in the folder with the `requirements.txt` file.
- Access mysql server using: `mysql -u root -p` and create the database: `CREATE DATABASE db_name;`
- Create a `local_settings.py` file in the same folder as `settings.py`. Change the name and user if needed and add the password.
```
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'weather',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '',
    'PORT': ''
    }
}
DEBUG = True
```
- Run `python manage.py migrate` to create the database.
- Run `python manage.py runserver` to actually run the application and explore its features.
