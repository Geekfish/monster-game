Monster Game
============

Usage
-----

Example usage::
  
	# usage: game.py [-h] [-f DATAFILE] monsters

	# Runs the game with 50 monsters defaulting to the small world map
	python game.py 50

	# Runs the game with 200 monsters specifying a world map file
	python game.py 200 --datafile data/world_map_medium.txt


Please run `python game.py -h` for argument description.


Docs
----

Assumptions are contained in docs/assumptions.rst


Tests
-----

Running tests require the packages contained in `test_requirements.txt`
