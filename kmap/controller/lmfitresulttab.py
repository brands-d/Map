# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import QDir, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout

# Own Imports
from kmap import __directory__
from kmap.controller.lmfittab import LMFitBaseTab
from kmap.model.lmfittab_model import LMFitTabModel
from kmap.controller.lmfittree import LMFitResultTree
from kmap.controller.lmfitresult import LMFitResult

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittab.ui')
LMFitResultTab_UI, _ = uic.loadUiType(UI_file)


class LMFitResultTab(LMFitBaseTab, LMFitResultTab_UI):

    def __init__(self, results, other_parameter, sliced_data,
                 orbitals, region='all', inverted=False):

        self.model = LMFitTabModel(sliced_data, orbitals)
        self.other_parameter = other_parameter
        self.title = 'Results'

        # Setup GUI
        super(LMFitResultTab, self).__init__()
        self.setupUi(self)

        self._setup(results, region, inverted)
        self._connect()

        self.refresh_sliced_plot()
        self.refresh_selected_plot()
        self.refresh_sum_plot()

    def update_result_tree(self):

        index = self.slider.get_index()

        self.tree.update_result(self.result.get_index(index))

    def _get_parameters(self, ID):

        orbital_param = self.tree.get_orbital_parameters(ID)

        weight, E_kin, *orientation, alpha, beta = orbital_param
        Ak_type, polarization, symmetry, dk = self.other_parameter
        parameters = [weight, E_kin, dk, *orientation, Ak_type,
                      polarization, alpha, beta, 0, symmetry]

        return parameters

    def _setup(self, results, region, inverted):

        LMFitBaseTab._setup(self)

        self.result = LMFitResult(results)
        self.tree = LMFitResultTree(
            self.model.orbitals, self.result.get_index(0))

        layout = QVBoxLayout()
        self.scroll_area.widget().setLayout(layout)
        layout.insertWidget(0, self.slider)
        layout.insertWidget(2, self.colormap)
        layout.insertWidget(3, self.crosshair)

        self.layout.insertWidget(1, self.tree)

        self.lmfit.set_region(region, inverted)

    def _connect(self):

        self.slider.slice_changed.connect(self.update_result_tree)
        
        LMFitBaseTab._connect(self)