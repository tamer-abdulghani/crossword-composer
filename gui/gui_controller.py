
from PyQt5.QtWidgets import QApplication, QWidget
from gui.gui import *
from helpers.dictionary import DictionaryCollection
from resources.samplegrids import *
from helpers.gridbuilder import *
from algorithms.a_star import *
from algorithms.csp import *

class Gui_controller(QWidget):
    def __init__(self, app, parent=None):
        super(Gui_controller, self).__init__(parent)
        self.app = app
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_my_componenets()
        self.buildMyGrid(GRID_11_11)
        self.active_grid = GRID_11_11
        self.gb = GridBuilder(self.active_grid)
        self.gb.build_as_words_list()
        self.collection = None
        self.backtraking_nb = 0

    def init_my_componenets(self):
        list_of_grids = ['GRID_11_11','GRID_7_7','GRID_5_6']
        self.ui.gridDropDown.addItems(list_of_grids)
        self.ui.gridDropDown.currentIndexChanged['int'].connect(self.init_gui_grid)

        list_of_solvers = ['LeastPossibilities', 'MostIntersects']
        self.ui.solverList.addItems(list_of_solvers)

        list_of_renders = ['100', '1000', '10000']
        self.ui.nbsolutionsList.addItems(list_of_renders)

        self.ui.loadDictionaryBtn.clicked.connect(self.load_dictioanry)
        self.ui.solveProblem_Btn.clicked.connect(self.solve_the_problem)

        self.init_gui_grid()

    def init_gui_grid(self):
        grid_name = str(self.ui.gridDropDown.currentText())

        if grid_name == 'GRID_5_6':
            self.active_grid = GRID_5_6
        elif grid_name == 'GRID_7_7':
            self.active_grid = GRID_7_7
        else:
            self.active_grid = GRID_11_11


        self.gb = GridBuilder(self.active_grid)
        self.gb.build_as_words_list()
        self.draw_grid()
        self.collection = None

    def draw_grid(self):
        self.gb.init_words()
        self.buildMyGrid(self.active_grid)

    def buildMyGrid(self, GRID):
        step = 29

        #Hiding old elements
        for i in range(0, 11):
            for j in range(0, 11):
                for widget in self.app.allWidgets():
                    if isinstance(widget, QtWidgets.QLineEdit):
                        # widget.clear()
                        if widget.objectName() == "textEdit_{}_{}".format(i, j):
                            widget.setParent(None)
                            #widget.del_()

        for i, val in enumerate(GRID):
            for j, val1 in enumerate(val):
                self.ui.textEdit = QtWidgets.QLineEdit(self.ui.frame)
                self.ui.textEdit.setGeometry(QtCore.QRect(40+j * step, i * step-15 + step, step, step))
                self.ui.textEdit.setObjectName("textEdit_{}_{}".format(i, j))
                self.ui.textEdit.setText('')
                if val1 == 0:
                    pal = QtGui.QPalette()
                    bgc = QtGui.QColor(0, 0, 0)
                    pal.setColor(QtGui.QPalette.Base, bgc)
                    textc = QtGui.QColor(255, 255, 255)
                    pal.setColor(QtGui.QPalette.Text, textc)
                    self.ui.textEdit.setPalette(pal)
                    self.ui.textEdit.setAutoFillBackground(False)

                self.ui.textEdit.raise_()
                self.ui.textEdit.show()

    def load_dictioanry(self):
        dicName = self.ui.dicNameText.text()
        print(dicName)

        from pathlib import Path
        my_file = Path("resources/"+dicName)
        if my_file.is_file():
            self.collection = DictionaryCollection("resources/"+dicName)
            self.collection.load(self.gb.words_list)
            self.ui.logWidget.addItem('Dictionary Loaded Successfully!!!')
        else:
            self.ui.logWidget.addItem(dicName+  ' not exist in the ::resources:: folder')
            self.ui.logWidget.addItem('Enter a valid file name please!')
        self.ui.logWidget.addItem('----------------')
        self.re_initialize()

    def solve_the_problem(self):
        if self.re_initialize():
            algorithm = 'astar'
            if self.ui.csp_radioButton.isChecked():
                algorithm = 'csp'

            if algorithm == 'astar':
                self.ui.logWidget.addItem('A* algorithm started, please wait!')
                self.ui.logWidget.addItem('LOADING .... ')
                text = str(self.ui.solverList.currentText())
                starting_solver = StartingSolver.LeastPossibilites
                process_solver = ProcessSolver.LeastPossibilitesAnotherWord
                if text == 'MostIntersects':
                    starting_solver = StartingSolver.MostIntersects
                    process_solver = ProcessSolver.MostIntersectsAnotherWord

                print('test1')
                alg = A_Star(self.gb,self.collection)
                print('test2')
                alg.guicontroller = self
                alg.starting_solver = starting_solver
                alg.process_solver = process_solver
                print("I started")
                time, solution = alg.solve()
                if solution:
                    self.render_grid_in_gui(solution)
                    self.ui.logWidget.addItem('Solution Found in: ' +str(time) + ' seconds')
                    self.ui.logWidget.addItem('Nb of Backtracks: '+ str(self.backtraking_nb))
                    self.ui.logWidget.addItem('----------------')

                else:
                    result_text = 'No solution found, duration is: ' + str(time) + ' seconds'
                    self.ui.logWidget.addItem(result_text)
                    self.ui.logWidget.addItem('----------------')
            else:
                self.ui.logWidget.addItem('CSP method started')
                self.ui.logWidget.addItem('LOADING .... ')
                nb = str(self.ui.nbsolutionsList.currentText())
                alg = csp(self.gb.words_list,self.collection)
                alg.create_variables()
                alg.create_constraints()
                print('test')
                time, solutions = alg.get_solutions(int(nb))

                result_text = nb + ' solution(s) found in: ' + str(time) + ' seconds'
                self.ui.logWidget.addItem(result_text)
                self.ui.logWidget.addItem('----------------')

                from time import sleep
                for s in solutions:
                    solution_as_grid = self.gb.fill_solution(s)
                    self.render_grid_in_gui(solution_as_grid)
                    sleep(0.1)


    def re_initialize(self):
        if self.collection is None:
            self.ui.logWidget.addItem("Please load dictionary first!!!")
            self.ui.logWidget.addItem('----------------')
            return False

        if self.gb is None:
            self.ui.logWidget.addItem("wrong grid loaded")
            self.ui.logWidget.addItem('----------------')
            return False

        self.draw_grid()
        self.backtraking_nb = 0

        return True



    def render_grid_in_gui(self, grid):
        #new_grid = self.gb.fill_solution(grid)
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                for widget in self.app.allWidgets():
                    if isinstance(widget, QtWidgets.QLineEdit):
                        # widget.clear()
                        if widget.objectName() == "textEdit_{}_{}".format(i, j):
                            # either empty cells (0,1) and newcells (0, 1 or letter) OR filled cells (1 or letter) and new cells (1 or letter)
                            if widget.text() != '' and widget.text() != '1' and widget.text() != '0' and str(val) != '0' and str(val) != '' and widget.text() != str(val):
                                pal = QtGui.QPalette()
                                bgc = QtGui.QColor(163, 234, 169)
                                pal.setColor(QtGui.QPalette.Base, bgc)
                                widget.setPalette(pal)
                                self.backtraking_nb+=1

                            if str(val) != '0':
                                widget.setText(str(val))

        self.app.processEvents()








