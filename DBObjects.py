class Salon:

    def __init__(self, room_id, code, capacity, building_name, building_id):
        
        self.id = room_id
        self.code = code
        self.capacity = capacity
        self.building_name = building_name
        self.building_id = building_id
    
    def update_capacity(self, capacity):

        if capacity > self.capacity:
            self.capacity = capacity