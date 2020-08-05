import logging
from PyQt5.QtWidgets import QWidget
from kmap.library.misc import get_ID_from_tab_text
from kmap.ui.orbitaldatatab_ui import OrbitalDataTabUI
from kmap.model.orbitaldatatab_model import OrbitalDataTabModel
from kmap.config.config import config


class OrbitalDataTab(OrbitalDataTabUI):

    def __init__(self):

        self.model = OrbitalDataTabModel(self)

        OrbitalDataTabUI.__init__(self)

    def add_orbital_from_filepath(self, path):

        orbital = self.model.load_data_from_path(path)

        self.table.add_orbital(orbital)

        self.refresh_plot()

    def refresh_plot(self):

        data = self.model.update_displayed_plot_data()

        self.plot_item.plot(data)

    def get_parameters(self, ID):

        # Hardcoded for now
        kinetic_energy = 30
        dk = 0.03

        parameters = self.table.get_parameters_by_ID(ID)
        deconvolution, *orientation = parameters
        polarization = self.polarization.get_parameters()

        return (deconvolution, kinetic_energy, dk,
                *orientation, *polarization)

    def crosshair_changed(self):

        data = self.model.displayed_plot_data
        self.crosshair.update_label()

    def polarization_changed(self):

        self.refresh_plot()

    def orbitals_changed(self):

        self.refresh_plot()

    def get_title(self):

        return 'Gas Phase Simulation'

    def remove_orbital_by_ID(self, ID):

        orbital = self.model.remove_orbital_by_ID(ID)

        self.refresh_plot()