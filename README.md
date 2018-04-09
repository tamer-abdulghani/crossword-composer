# Crossword Composer

This project contains implementation of Crossword Composer problem in Python. 
For a given grid and specific dictionary which contains list of words in English, the software trys to fill all the white cells in the grid with letters where each columns or row are formed by a word in the dictionary.

## Project main structure: 
1. algorithms folder: 
	- contains two main files, a_star.py and csp.py.
    - a_star.py is the a* algorithm implementation. 
    - csp.py contains a wrapper class that use a library: python-constrait
2. gui folder:
	- GUI.py is the ui python file generated from command line using "pyuic5" which convert gui.ui (drawed by QtDesigner) into .py extension.
	- gui_controller: contains custom method that control the ui form.
3. helpers:
	- dictionary: contains implementation of all helper methods and indexing needed by the algorithms
	- gridBuilder: contains methods of building grids arrays, wordslist and convertions between them.
4. models:
	- word: the basic object of a word of the grid.
	- node: represnet the node or state in A* algorithm
	- position: represent the x,y coordinates in the grid.
	- direction: has two values: Across/Down.
5. resources:
	- samplegrids: contains three main grids: GRID_11_11,GRID_7_7, GRID_5_6
	- words(2)(_small).txt:  are the dictionaries.
