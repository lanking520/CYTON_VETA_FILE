
class packet:
	def __init__(self):
		self.packet_recv = []
		self.packet_lost = []
		self.packet_counter = 0
		self.packet_label = 0
		self.timer = 0
		self.time_delay = 0
		self.dead_packet = []

	def packet_record(self):
		self.packet_recv.append(self.packet_counter)
		self.packet_lost.append(self.dead_packet)
		self.packet_counter = 0
		self.dead_packet = 0
	
	def timer_probe(self, time_set):
		self.timer +=1 * time_set

	def label_probe(self, packet_label):
		self.dead_packet += packet_label - self.packet_label
		self.packet_label = packet_label

	def get_time_delay(self):
		current_time = self.timer
		self.timer = 0
		return current_time

	def drawer(self, canvas):
		canvas.draw_text('Packet Number: ' + str(self.packet_label), (10, 460), 20, 'White')
		canvas.draw_text('Packet Loss: ' + str(self.dead_packet), (10, 480), 20, 'White')
		canvas.draw_text('Packet Time Delay: '+ str(self.get_time_delay()), (10, 500), 20, 'White')

