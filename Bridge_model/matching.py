class matching:
    def __init__(self):
	self.target_pressure = 0.15
	self.current_pressure = 0.15
	self.matched = True

    def matching(self):
	self.matched =  abs(self.target_pressure - self.current_pressure) <= 0.2 
	if !self.matched:
		return self.target_pressure - self.current_pressure

    def get_match(self):
	return self.matched
		
