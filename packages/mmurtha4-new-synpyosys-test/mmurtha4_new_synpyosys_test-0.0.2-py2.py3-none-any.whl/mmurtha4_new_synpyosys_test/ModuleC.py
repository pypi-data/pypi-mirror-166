from shutil import which
from unittest.util import strclass
from pyosys import libyosys as ys
import matplotlib.pyplot as plt
from collections import defaultdict
from enum import Enum, auto
from typing import Union

class CellType(Enum):
    AND = auto()
    NOT = auto()
    OR = auto()
class Module(ys.Module):
    def __init__(self, module = None, bit_to_cells = None):
        self.bit_to_cells = defaultdict(list) if bit_to_cells is None else bit_to_cells #incorporating bit_to_cells back into the class - does this make sense?
        #self.module = ys.Module() if module is None else module #need to have the mapping (bit2cells)
        super().__init__() #does this refer to the ys.Module class
        if module:
            self = module.cloneInto(self) #what's this do? cloneInto function? 
        self.sigmap = ys.SigMap(self)


    #def sigmap(self, module = None): 
        #self.module = ys.SigMap(module)
     #add a sigmap to the module itself - instead of self.sigmap - self.module.sigmap - can this be run like i.e. design1.sigmap(module_number)
    
    def update_map(self, changed_cell):  #for added cells
        for conn_id, sig_spec in changed_cell.connections_.items():
            if(changed_cell.input(conn_id)):
                sig_bits = self.sigmap(sig_spec).to_sigbit_set()
                for bit in sig_bits:
                    self.bit_to_cells[bit].append(changed_cell) #this is not appending properly - prints none??
        return self.bit_to_cells #can do .values[] forms a list of cells
    def update_map_removed_cells(self, removed_cell):
        del self.bit_to_cells[removed_cell]
        return self.bit_to_cells

    def create_map(self):    #populates the bit_to_cells in the module class        
        for cell in self.selected_cells():          #this means that it does it for one specific module - .selected_cells not working
            for conn_id, sig_spec in cell.connections_.items():
                if(cell.input(conn_id)):
                    sig_bits = self.sigmap(sig_spec).to_sigbit_set()
                    #my_cell = sig_spec
                    print(sig_spec)
                    for bit in sig_bits:
                        self.bit_to_cells[bit].append(cell) #updates the bit2cells

    def add_cell(self, gate_type: CellType, module: ys.Module, cell_id_str, input_sigs = None, output_sigs = None): #TODO - module: ys.Module should not need to be there
        if gate_type == CellType.NOT: #what is the cell type class?? - Adds cell to module and creates a cell in the background - updates module in the background so design is updated
            gate_type = module.addNot(cell_id_str, input_sigs, output_sigs)
        elif gate_type == CellType.AND:
            gate_type = module.addAnd(cell_id_str, input_sigs, output_sigs)
        elif gate_type == CellType.NOT:
            gate_type = module.addOr(cell_id_str, input_sigs, output_sigs)
        else:
            print(f"Invalid Cell Type: {gate_type}")
        self.update_map()  

    def add_and(self, module: ys.Module, cell_id: Union[str, ys.IdString], input_sigs = None, output_sigs = None): #incorporate add_and at the bottom
        input_wires = []
        for input_sig in input_sigs:
            input_wire = module.wires_[ys.IdString("\\G18")]
            if input_wire is None:
                input_wires.append(module.addWire(ys.IdString("\\G18"), 1))
            #wire.port_output = False
        for output_sig in output_sigs:
            wire.append(module.addWire(ys.IdString("\\G18"), 1))
            wire = module.wires_[ys.IdString("\\G18")]
            #wire.port_output = True

    # def add_single_cell_info(self, cell):       #for adding single cell information
    #     for conn_id, sig_spec in cell.connections_.items():
    #          if(cell.input(conn_id)):
    #             sig_bits = self.sigmap(sig_spec).to_sigbit_set()
    #             my_cell = sig_spec
    #             print(sig_spec)
    #             for bit in sig_bits:
    #                 if cell not in self.bit_to_cells[bit]:
    #                     self.bit_to_cells[bit].append(cell)






    def cell_id_str(self, cell_name):
        if cell_name == str:    #saw something about .isalnum, but not sure if it would work with $
            ys.IdString(cell_name) #need to somehow check if cell_name is a string
        else:
            print("Error: Input a string")
    def create_wire(self, wire_name, bit, which_module, is_wire_output): #is_wire_output could be cleaner
        new_wire = which_module.addWire(ys.IdString("\\"+wire_name), bit) #where bit is the width of the wire? 
        if is_wire_output == 'Output':
            new_wire.port_output = True
        elif is_wire_output == 'Input':
            new_wire.port_input = True
        else:
            None
        #TODO - make it easier to create wires/cells/sigspecs - next week? - don't worry about the functions below for right now
        #TODO remove function - then a connected mapping function in the bit_to_cells that updates this
        #TODO an add function for the different types of gates

