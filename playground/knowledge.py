
# class to model internal knowledge of pepper robot, used to interact with the 2D House simulator
class Knowledge():
	def __init__():
		self.name2predicate = self.getName2predicate()
		self.room2furniture = self.getRoom2Furniture()
		self.room2items 	= self.getRoom2items()


        # foyer living_room dining toilet studio bedroom kitchen outdoor          - room
        # d_foyer_outdoor d_foyer_living  d_toilet_living d_studio_living         - door
        # d_bedroom_living d_living_dining d_dining_kitchen                       - door
        # wl_foyer  wl_toilet wl_studio wl_bedroom wl_dining wl_kitchen           - window
        # wr_foyer  wr_toilet wr_studio wr_bedroom wr_dining wr_kitchen           - window
        # green_marker pen pencil plate_empty cup_coffee plate_oranges            - item
        # plate_apples orange1 orange2 orange3 apple1 apple2 smartphone           - item
        # red_notebook green_notebook glasses yellow_notebook cards pink_notebook - item
        # desk_studio pool_studio kitchenette table_kitchen bed cabinet_bedroom_l - furniture       ;_l -> left _r -> right
        # cabinet_bedroom_r tv_bedroom water tub sink cabinet_toilet              - furniture
        # tv_living sofa table_living armchair_l armchair_r table_dining          - furniture


	def getName2predicate(self)
		return = {
		# "foyer": "foyer",
		# "living room": "living_room"
		# "toiler":"toilet",
		# "studio": "studio",
		# "bedroom": "bedroom",
		# "kitchen": "kitchen",
		# "outdoor": "outdoor",

		# "" "d_foyer_outdoor"
		 d_foyer_outdoor d_foyer_living  d_toilet_living d_studio_living
		 wl_foyer  wl_toilet wl_studio wl_bedroom wl_dining wl_kitchen
		 wr_foyer  wr_toilet wr_studio wr_bedroom wr_dining wr_kitchen
		 green_marker pen pencil plate_empty cup_coffee plate_oranges
		 plate_apples orange1 orange2 orange3 apple1 apple2 smartphone
		 red_notebook green_notebook glasses yellow_notebook cards pink_notebook
		 desk_studio pool_studio kitchenette table_kitchen bed cabinet_bedroom_l
		 cabinet_bedroom_r tv_bedroom water tub sink cabinet_toilet
		 tv_living sofa table_living armchair_l armchair_r table_dining


		}


	# for modim application
	def getRoom2Furniture(self):
		return {


		}

	def getRoom2items(self):
		return {


		}
		


	# for acquiring new data
	def add(self, what, room, on_what):
		# edit room2items dictionary

		pass 

	def remove(self, object):   # we start without knowing of smartphone and glasses
		pass
