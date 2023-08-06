from pickle import TRUE
import string
from pyosys import libyosys as ys
import matplotlib.pyplot as plt
from collections import defaultdict
from enum import Enum, auto
from typing import Union

class CellType(Enum):
    AND = auto()
    NOT = auto()
    OR = auto()

class ModuleType(Enum):
    YOSYS_RTLIL = auto()

class Module():
    def __init__(self, module: Union[ys.Module, None] = None, bit_to_cells: defaultdict = None):
        self.name = None
        self.module_type = ModuleType.YOSYS_RTLIL
        self.module = None
        self.bit_to_cells = defaultdict(list) if bit_to_cells is None else bit_to_cells
        self.sigmap = ys.SigMap(module) if module else None
    
    def update_map(self, changed_cell): 
        if not self.sigmap:
            self.sigmap = ys.SigMap(self.module)

        for conn_id, sig_spec in changed_cell.connections_.items():
            if(changed_cell.input(conn_id)):
                sig_bits = self.sigmap(sig_spec).to_sigbit_set()
                for bit in sig_bits:
                    #print(self.bit_to_cells[bit])
                    # need to call .hash() to get same id for SigBits
                    self.bit_to_cells[bit.hash()].append(changed_cell)
        return self.bit_to_cells 

    def update_map_removed_cells(self, removed_cell):
        if not self.sigmap:
            self.sigmap = ys.SigMap(self.module)

        for conn_id, sig_spec in removed_cell.connections_.items():
            if(removed_cell.input(conn_id)):
                sig_bits = sig_spec.to_sigbit_set()
                for bit in sig_bits:
                    for cell in self.bit_to_cells[bit.hash()]:
                        if cell.hash() == removed_cell.hash():
                            self.bit_to_cells[bit.hash()].remove(cell)
                        else:
                            print("Error: Cell does not exist in dictionary, deletion not possible")
                            break
  
    def create_map(self):    #populates the bit_to_cells in the module class        
        if not self.sigmap:
            self.sigmap = ys.SigMap(self.module)

        for cell in self.module.selected_cells():          
            for conn_id, sig_spec in cell.connections_.items():
                if(cell.input(conn_id)):
                    sig_bits = self.sigmap(sig_spec).to_sigbit_set()
                    for bit in sig_bits:
                        #print(bit.hash())
                        #need to call .hash() to get same id for SigBits
                        self.bit_to_cells[bit.hash()].append(cell) #updates the bit2cells

    def cell_id_str(self, id_name):
        new_id_str = ys.IdString(id_name)
        return new_id_str

    def cell_test(self, name: string):
        print(name)

    def new_wire(self, id_name, bit_width, port_output = None, port_input = None):
        id_str = self.cell_id_str(id_name)
        wire = self.module.addWire(id_str, bit_width)
        if port_input == True:
            self.wire.port_input = True
        elif port_output == True:
            self.wire.port_output = True
        return wire
    
    def add_and(self, id_name, input1, input2, output):
        id_str = self.cell_id_str(id_name)
        new_cell = self.module.addAnd(id_str, input1, input2, output)
        self.update_map(new_cell)
        return new_cell

    def add_or(self, id_name, input1, input2, output):
        id_str = self.cell_id_str(id_name)
        new_cell = self.module.addOr(id_str, input1, input2, output)
        self.update_map(new_cell)
        return new_cell

    def add_not(self, id_name, input, output):
        # id_str = self.cell_id_str(id_name)
        new_cell = self.module.addNot(id_name, input, output)
        self.update_map(new_cell)
        return new_cell

    # def add_cell(self, gate_type: CellType, module: ys.Module, cell_id_str, input_sigs = None, output_sigs = None): #TODO - module: ys.Module should not need to be there
    #     if gate_type == CellType.NOT: #what is the cell type class?? - Adds cell to module and creates a cell in the background - updates module in the background so design is updated
    #         gate_type = module.addNot(cell_id_str, input_sigs, output_sigs)
    #     elif gate_type == CellType.AND:
    #         gate_type = module.addAnd(cell_id_str, input_sigs, output_sigs)
    #     elif gate_type == CellType.NOT:
    #         gate_type = module.addOr(cell_id_str, input_sigs, output_sigs)
    #     else:
    #         print(f"Invalid Cell Type: {gate_type}")
    #     self.update_map()  

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
        if cell_name == str:   
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


