class Supply:
    def __init__(self, name: str, count: int, best_before: int = 'Not specified', price: int = 0, unit: str = 'piece(s)', restriction: str = 'No restrictions', notes: str = 'No notes'):
        self.__name = name
        self.__count = count
        self.__unit = unit # unit is one of the following : "kg", "g", "mg", "l", "ml", "unit", "piece(s)"
        self.__best_before = best_before # best_before date is in seconds counted since epoch
        self.__price = price
        self.__restriction = restriction
        self.__notes = notes
        
    def get_name(self):
        return self.__name
    
    def get_count(self):
        return self.__count
    
    def get_unit(self):
        return self.__unit
    
    def get_best_before(self):
        return self.__best_before
    
    def get_price(self):
        return self.__price
    
    def get_restriction(self):
        return self.__restriction
    
    def get_notes(self):
        return self.__notes
    
    def add_count(self, count: int):
        try:
            if count < 0:
                return "Error : Supply.add_count() error, Invalid count"
            self.__count += count
            return "Success : Count added"
        except:
            return "Error : Supply.add_count() error"
    
    def del_count(self, count):
        try:
            if count < 0:
                return "Error : Supply.del_count() error, Invalid count"
            if self.__count - count < 0:
                return "Error : Not enough supply"
            self.__count -= count
            return "Success : Count deleted"
        except:
            return "Error : Supply.del_count() error"
        
    def chg_count(self, count):
        try:
            if count < 0:
                return "Error : Supply.chg_count() error, Invalid count"
            self.__count = count
            return "Success : Count changed"
        except:
            return "Error : Supply.chg_count() error"
        
    def chg_unit(self, unit):
        try:
            if not unit in ["kg", "g", "mg", "l", "ml", "unit", "piece(s)"]:
                return "Error : Supply.chg_unit() error, Invalid unit"
            self.__unit = unit
            return "Success : Unit changed"
        except:
            return "Error : Supply.chg_unit() error"
        
    def chg_best_before(self, best_before):
        try:
            if not best_before > time.time():
                return "Error : Supply.chg_best_before() error, Invalid best before date"
            self.__best_before = best_before
            return "Success : Best before date changed"
        except:
            return "Error : Supply.chg_best_before() error"
        
    def chg_price(self, price):
        try:
            if price < 0:
                return "Error : Supply.chg_price() error, Invalid price"
            self.__price = price
            return "Success : Price changed"
        except:
            return "Error : Supply.chg_price() error"
        
    def chg_restriction(self, restriction):
        try:
            self.__restriction = restriction
            return "Success : Restriction changed"
        except:
            return "Error : Supply.chg_restriction() error"
        
    def chg_notes(self, notes):
        try:
            self.__notes = notes
            return "Success : Notes changed"
        except:
            return "Error : Supply.chg_notes() error"