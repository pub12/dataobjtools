import unittest
import os

import sys
sys.path.insert(0, '../dataobjtools/')


from selector import Selector

class TestSelector(unittest.TestCase):
	data1 = { "id":"abc", "value":123 }
	data2 = [ 	{ "id":"abc", "value":123, "tag":"monday" }, 
				{ "id":"xyz", "value":123 , "tag":"tuesday" }, 
				{ "id":"ijk", "value":456 , "tag":"wednesday" }, 
				{ "id":"abc", "value":456 , "tag":"thursday" } ]
	
	data3 = { 
				"monday":{
							"morning":[	{"time":"9am", "appointee":"john", "location":"city"},
										{"time":"10am", "appointee":"sally", "location":"city"},
										{"time":"11am", "appointee":"alex", "location":"city"}],
							"afternon":[{"time":"2pm", "appointee":"bill", "location":"city"},
										{"time":"3pm", "appointee":"harry", "location":"waverly"},
										{"time":"6am", "appointee":"nancy", "location":"eastwood"}],
							"evening":[	{"time":"7pm", "appointee":"clarice", "location":"perth"},
										{"time":"8pm", "appointee":"harvey", "location":"ryde"},
										{"time":"9pm", "appointee":"zoe", "location":"clayton"}],
				},

				"tuesday":{
							"morning":[	{"time":"9am", "appointee":"john", "location":"city"},
										{"time":"10am", "appointee":"sally", "location":"city"},
										{"time":"11am", "appointee":"alex", "location":"city"}]
				},

				"wednesday":{
							"morning":[	{"time":"9am", "appointee":"john", "location":"city"},
										{"time":"11am", "appointee":"alex", "location":"city"}],

							"evening":[	{"time":"7pm", "appointee":"clarice", "location":"perth"},
										{"time":"9pm", "appointee":"zoe", "location":"clayton"}],
				},
	}

	## Data1
	def test_selector_flat_positive_match(self):
		match = { "id":"abc", "value":123 }
		results = Selector().dict_search( self.data1, {"id":"abc"} ) 
		self.assertEqual( match, results)


	def test_selector_flat_negative_match(self):
		match = None
		results = Selector().dict_search( self.data1, {"id":"abc2"} ) 
		self.assertEqual( match, results)
 

	def test_selector_flat_positive_multi_match(self):
		match = { "id":"abc", "value":123 }
		results = Selector().dict_search( self.data1, {"id":"abc", "value":123} ) 
		self.assertEqual( match, results)

	def test_selector_flat_negative_multi_partial_match(self):
		match = None
		results = Selector().dict_search( self.data1, {"id":"abc2", "value":123} ) 
		self.assertEqual( match, results)
	
	###Data2

	def test_selector_array_positive_match(self):
		match = { "id":"abc", "value":123, "tag":"monday" }
		results = Selector().dict_search( self.data2, {"id":"abc"} ) 
		self.assertEqual( match, results)


	def test_selector_array_negative_match(self):
		match = None
		results = Selector().dict_search( self.data2, {"id":"abc2"} ) 
		self.assertEqual( match, results)
 

	def test_selector_array_positive_multi_match(self):
		match = { "id":"xyz", "value":123, "tag":"tuesday" }
		results = Selector().dict_search( self.data2, {"id":"xyz", "value":123} ) 
		self.assertEqual( match, results)

	def test_selector_array_negative_multi_partial_match(self):
		match = None
		results = Selector().dict_search( self.data2, {"id":"abc2", "value":123} ) 
		self.assertEqual( match, results)
 
 	###Data3

	def test_selector_complex_positive_match(self):
		match = {"time":"9am", "appointee":"john", "location":"city" }
		results = Selector().dict_search( self.data3, {"monday":{"morning":{"time":"9am"}}} ) 
		self.assertEqual( match, results)


	def test_selector_complex_negative_match(self):
		match = None
		results = Selector().dict_search( self.data3, {"monday":{"morning":{"time":"930am"}}}) 
		self.assertEqual( match, results)


	def test_selector_complex_positive_multi_match1(self):
		match = {"time":"9am", "appointee":"john", "location":"city" }
		results = Selector().dict_search( self.data3, {"monday":{"morning":{"time":"9am","appointee":"john" }}} ) 
		self.assertEqual( match, results)


	def test_selector_complex_positive_multi_match2(self):
		match = {"time":"9am", "appointee":"john", "location":"city" }
		results = Selector().dict_search( self.data3, {"tuesday":{"morning":{"time":"9am","appointee":"john" }}} ) 
		self.assertEqual( match, results)


	def test_selector_complex_positive_multi_match3(self):
		match = {"time":"7pm", "appointee":"clarice", "location":"perth" }
		results = Selector().dict_search( self.data3, {"wednesday":{"evening":{"time":"7pm","appointee":"clarice" }}}  ) 
		self.assertEqual( match, results)

 
	def test_selector_complex_negative_multi_match1(self):
		match = None
		results = Selector().dict_search( self.data3, {"monday":{"evening":{"time":"9am","appointee":"john" }}} ) 
		self.assertEqual( match, results)


	def test_selector_complex_negative_multi_match2(self):
		match = None
		results = Selector().dict_search( self.data3, {"tuesday":{"morning":{"time":"11am","appointee":"alice" }}} ) 
		self.assertEqual( match, results)


	def test_selector_complex_negative_multi_match3(self):
		match = None
		results = Selector().dict_search( self.data3, {"wednesday":{"evening":{"time":"7pm","appointee":"john" }}}, loc_debug=True ) 
		self.assertEqual( match, results)


if __name__ == '__main__':
    unittest.main()