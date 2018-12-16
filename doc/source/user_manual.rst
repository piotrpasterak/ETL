============
User Manual
============

Installation
^^^^^^^^^^^^^^^^^^^^^
    Application requires Python environment in version 3.6+. Firefox 63.0+ web browser is             also required, in case of malfunction (exceptions about lack of access to this binary), please add firefox.exe binary path to system PATH.

    For environment in which application can work additional python package (see appendix) are required.

    However, by execute dependecy_installer.py script all necessary packages shall be automatically downloaded and installed.

Features description
^^^^^^^^^^^^^^^^^^^^^
- How to start application:
    Application is started as Python application by following command::

        py <path to etl>etl.py

    In result such main window shall appear:

    .. image:: assets/main.png

- Setup city for searching:
    First, enter of chosen city is necessary:

    .. image:: assets/city_text_box.png

    Next, push button "Enter":

    .. image:: assets/city_enter.png

- Hotel choosing:
    If city name has been correctly entered, then list of no more then 10 most commented hotels appears.
    One of them shall be selected.

- Extract
    When hotel has been chosen then extract of review data is possible:

    .. image:: assets/extract.png

    During this process, modal dialog is visible, and after processing "OK" button is active.

    .. image:: assets/modal_extract.png

- Transform

    .. image:: assets/transform.png

    During this process, modal dialog is visible, and after processing, "OK" button is active (as above).

- Load

    .. image:: assets/load.png

    During this process, modal dialog is visible, and after processing, "OK" button is active (as above).

- Whole process

    .. image:: assets/whole.png

    During this process, modal dialog is visible, and after processing, "OK" button is active (as above).

- Display database content:

    .. image:: assets/show_database.png

    When button "Show Database" is clicked than, in dialog, after hotel choose,
    content of database for given hotel is shown. Also there is button "Clear" by which database can be cleared.