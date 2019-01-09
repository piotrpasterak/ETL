Architecture
============

In general whole application architecture mainly bases on ETL pattern:

.. image:: assets/UseDiagram.png

User interface architecture is hidden inside Kivy.
Kivy in general uses MVC (Model-View-Controller) architectural patten.
To be coherent with MVC idea also kivy language (files .kv) is in use for Views separation from logic.
