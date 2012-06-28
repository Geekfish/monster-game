Design Assumptions
==================

* Observing the structure of provided world data files, the parser assumes neighbouring cities are always provided in the following order: north, south, east, west.

* City names contain only letters and hyphens

* Multiple monsters can start on the same city

* If more than 2 monsters are occupying the same city, all monsters die and destroy the city.