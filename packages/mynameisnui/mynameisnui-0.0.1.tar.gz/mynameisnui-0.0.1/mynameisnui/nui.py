class NuiZiLLa:
	"""
	คลาส NuiZiLLa คือ
	ข้อมูลที่เกี่ยวข้อง กับ กะเทยแดง
	ประกอบด้วย ชื่อเพจ ก็ไม่มีอะ
	ชื่อช่องยูทูป ยิ่งไม่มีใหญ่

	Example
	# ------------------------
	nui = NuiZiLLa()
	nui.show_name()
	nui.show_youtube()
	nui.about()
	nui.show_art()
	# ------------------------

	"""

	def __init__(self):
		self.name = 'กะเทยแดง'
		self.page = 'https://www.facebook.com/nuizilla'

	def show_name(self):
		print('สัสดี ฉันชื่อ{}' .format(self.name))

	def show_youtube(self):
		print('https://youtube.com/nuizilla')

	def about(self):
		text = '''

		สัสดีจย้าาาา ขี้เกียจจะพิมพ์อะไรเยอะแยะ
		สามารถติดตามได้ ที่ไหนก็ไม่รู้แหละนะ

		'''
		print(text)

	def show_art(self):
		text = '''

		    .-  -.        .-====-.      ,-------.      .-=<>=-.
		   /_-\'''/-_\\      / / '' \\\\     |,-----.|   /__----__\
		  |/  o) (o  \\|    | | ')(' | |   /,'-----'.\\   |/ (')(') \\|
		   \\   ._.   /      \\ \\    / /   {_/(') (')\\_}   \\   __   /
		   ,>-_,,,_-<.       >'=jf='<     `.   _   .'    ,'--__--'.
		 /      .      \\    /        \\     /'-___-'\\    /    :|    \
		(_)     .     (_)  /          \\   /         \\  (_)   :|   (_)
		 \\_-----'____--/  (_)        (_) (_)_______(_)   |___:|____|
		  \\___________/     |________|     \\_______/     |_________|

		'''
		print(text)


if __name__ == '__main__':
	nui = NuiZiLLa()
	nui.show_name()
	nui.show_youtube()
	nui.about()
	nui.show_art()