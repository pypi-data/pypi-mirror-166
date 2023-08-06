from pyosys import libyosys as ys
from collections import defaultdict
import re
from Classes.ModuleC import Module

class Design(ys.Design):
    def __init__(self, design = None, module = None, bit_to_cells = None):
        #Initialize the parent class
        super().__init__()
        #Create empty list for synPYosys Modules (Yosys Modules in self.modules_)
        self.synModules_ = {}
        #self.modules_ = 
    
    def set_var_py_modules_(self, dict):
        print("OVERRIDE")
        super().set_var_py_modules_(dict)
        return None

    def create(self, file_location):    #TODO see what modules are in there and pass them to the synPYosys moduleC
        #self.design = ys.Design
        ys.run_pass("read_verilog  " + file_location, self) 
        ys.run_pass("prep", self)
        print(self.modules_)
        self.synModules_ = self.get_ysmodules()
        #self.test_mods_ = self.get_ysmodules()
        #print("KLKL")
        #print(self.modules_)
        #self.get_ysmodules()
        #print("LKLKLKLKL")
        #for id, mod in self.modules_.items():
        #    print(type(mod))
        
    def get_ysmodules(self):   #TODO want it to return the module that I created - gets the yosys modules, pass each one to a new module
        ys_modules = {}
        for ysmodule in self.selected_whole_modules_warn():
            #print(ysmodule)
            #ys_modules.append(tmp_synModule)
            tmp_synModule = Module()
            #print("JKJK")
            #print(type(tmp_synModule))
            #ysmodule.cloneInto(tmp_synModule)
            #print(type(tmp_synModule))
            tmp_synModule.name = ys.IdString("\\TEST")
            tmp_synModule.design = ysmodule.design
            tmp_synModule.module = ysmodule
            ys_modules[tmp_synModule.name] = tmp_synModule #could result in design not updating
            #self.add(tmp_synModule)
        return ys_modules
    #is there a way to make the ys_modules list global? 

#should this be in the Module class
    def results(self):
        print("Checking Results of Wire Map")
        for module in self:
            cells = module.selected_cells()
            for cell in cells:
                print(f'CELL: {cell.name}')
                for conn_id, sig_spec in cell.connections_.items():
                    if(cell.output(conn_id)):
                        sig_bits = self.sigmap(sig_spec).to_sigbit_set()
                        for bit in sig_bits:
                            if not self.bit_to_cells[bit]:
                                print('\tNO CELL CONNECTIONS: PORT OUTPUT')
                                print(f'\tConnected to output wire {bit.wire}')
                            else:
                                print(f'\tConnected Cells: {self.bit_to_cells[bit]}')


        #not really sure if this should be placed here                            
    def short_names_map(self, file_name):
        shortened_names_map = {}
        for module in self.design.selected_modules():
            for cell in module.selected_cells():
                cell_sname = self.get_shortened_name(cell, file_name)
                shortened_names_map[cell.name] = cell_sname
        return shortened_names_map
    def get_shortened_name(self, cell, file_name):
        regrex_str = re.escape(cell.type.str()) + r'\$' + re.escape(file_name) + r':[\d]+([\\\$].*)'
        m = re.search(regrex_str, cell.name.str())
        if m:
            return m.group(1)
        return None