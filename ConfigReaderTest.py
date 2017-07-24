import BOF_ConfigReader
import unittest
import time


class Tester(unittest.TestCase):
    def test_read_dict0(self):
        string = '{1:1.0, a:b, date:2017-07-13, time:"10:45:00", ' \
                 'datetime:"2017-07-13 10:45:00", boolean:true, list:[12, 1.6, list]}'
        result, length = BOF_ConfigReader.ConfigReader.read_dict(string)
        self.assertEqual(result[1], 1.0)
        self.assertEqual(result["a"], "b")
        self.assertEqual(type(result["date"]), time.struct_time)
        self.assertEqual(type(result["time"]), time.struct_time)
        self.assertEqual(type(result["datetime"]), time.struct_time)
        self.assertEqual(result["boolean"], True)
        self.assertEqual(result["list"], [12, 1.6, "list"])
        self.assertEqual(length, len(string)-1)

    def test_read_dict1(self):
        input_str = '{d:{1:2, x:y, z:{1:2, x:y} }, e:{1:3, 2:[1,2]}}'
        result = BOF_ConfigReader.ConfigReader.read_dict(input_str)[0]
        self.assertEqual(result, {'d': {1: 2, 'x': 'y', 'z': {1: 2, 'x': 'y'}}, 'e': {1: 3, 2: [1, 2]}})

    def test_read_dict2(self):
        input_str = '{f: {g:{h:{i:"Hello"}}}}'
        result = BOF_ConfigReader.ConfigReader.read_dict(input_str)[0]
        self.assertEqual(result, {'f': {'g': {'h': {'i': 'Hello'}}}})

    def test_read_list(self):
        sample_list = '[12, 1.6, list, 2017-07-13 10:45:00, "ab,cd" , ab, "last"]'
        result = BOF_ConfigReader.ConfigReader.read_list(sample_list)
        self.assertEqual(result[0], 12)
        self.assertEqual(result[1], 1.6)
        self.assertEqual(result[2], "list")
        self.assertEqual(type(result[3]), time.struct_time)
        self.assertEqual(result[4], "ab,cd")
        self.assertEqual(result[5], 'ab')
        self.assertEqual(result[6], 'last')

    def test_get(self):
        config = BOF_ConfigReader.ConfigReader("SampleConfig")
        self.assertEqual(config.get_section("student").get_value("name"), "Yu Feng")
        self.assertEqual(config.get_section("student").get_value("dict1"),
                         {'a': 1, 1: 'x', 5: 6, 'c': ['x', 2, 3.5]})

    def test_write(self):
        BOF_ConfigReader.ConfigReader("SampleConfig").write()

if __name__ == '__main__':
    unittest.main()
