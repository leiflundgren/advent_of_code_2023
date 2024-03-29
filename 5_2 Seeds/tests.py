from math import exp
from os import access

import unittest
unittest.TestLoader.sortTestMethodsUsing = None

import range
from mapping import Mapping
from seed_map import SeedMap

def create_seed_map():
    seeds = Mapping("seeds") \
    .add_mapping(79, 79 ,14) \
    .add_mapping(55,55 ,13)

    seed_to_soil = Mapping("seed_to_soil")
    seed_to_soil.add_mapping( 50, 98, 2)
    seed_to_soil.add_mapping( 52, 50, 48)

    soil_to_fertilizer = Mapping("soil_to_fertilizer") \
    .add_mapping( 0, 15, 37)\
    .add_mapping( 37, 52, 2)\
    .add_mapping( 39, 0, 15)

    fertilizer_to_water = Mapping("fertilizer_to_water") \
    .add_mapping( 49, 53, 8) \
    .add_mapping( 0, 11, 42) \
    .add_mapping( 42, 0, 7) \
    .add_mapping( 57, 7, 4) 

    water_to_light = Mapping("water_to_light") \
    .add_mapping( 88, 18, 7) \
    .add_mapping( 18, 25, 70)

    light_to_temperature = Mapping("light_to_temperature") \
    .add_mapping( 45, 77, 23) \
    .add_mapping( 81, 45, 19) \
    .add_mapping( 68, 64, 13)

    temperature_to_humidity = Mapping("temperature_to_humidity") \
    .add_mapping( 0, 69, 1) \
    .add_mapping( 1, 0, 69)

    humidity_to_location = Mapping("humidity_to_location") \
    .add_mapping( 60, 56, 37) \
    .add_mapping( 56, 93, 4)

    return SeedMap(seeds, seed_to_soil, soil_to_fertilizer,fertilizer_to_water,water_to_light,light_to_temperature,                temperature_to_humidity,humidity_to_location ) 


seed_map = create_seed_map()
splitted_seed_map : SeedMap = None

# Function to print the matrix
def printMatrix(m):
    for line in m:
        for col in line:
            if isinstance(col, int):
                print('{:2d}'.format(col), end=' ')
            else:
                print(col, end=' ')
        print()


    
class Tests(unittest.TestCase):

        

    def test_mappings(self):
        m = Mapping('no-name')
        m.add_mapping(50, 98, 2)
        
        self.assertEqual(97, m.src_to_dst(97))
        self.assertEqual(50, m.src_to_dst(98))
        self.assertEqual(51, m.src_to_dst(99))
        self.assertEqual(100, m.src_to_dst(100))


        self.assertEqual(49, m.dst_to_src(49))
        self.assertEqual(98, m.dst_to_src(50))
        self.assertEqual(99, m.dst_to_src(51))
        self.assertEqual(52, m.dst_to_src(52))

    def test_split(self):
        seed_map = create_seed_map()
        # seed_map.add_missing_holes()
        print('---- split')
        print(str(seed_map.map_humidity_to_location))
        seed_map.split_mappings()
        print('---- split')
        print(str(seed_map.map_humidity_to_location))
        matrix = seed_map.create_debug_matrix(0, 99, True)
        # rotate90Clockwise(matrix)
        printMatrix(matrix)
        splitted_seed_map = seed_map

    # def test_find_change_points(self):
    #     points = seed_map.change_spots(0)
    #     expected = [15, 22, 26, 52, 59, 69, 70, 71, 98]
        
    #     self.assertListEqual(expected, points)

    # def test_walker(self):
    #     walker = seed_map.create_walkers()
        
    #     while True:
    #         try:
    #             nxt = walker.find_next_node()
    #             if nxt is None: break
    #             src_nxt = nxt.src
    #             src = nxt.translate_src_to_pre()
    #             nxt.next()
    #         except StopIteration:
    #             pass

    @unittest.skip('debug')
    def test_dump_matrix(self):
        def rotate90Clockwise(m):
            res = []
            for y in range(0, len(m)):
                for x in range(0, len(m[x])):
                    res[y, x] = m[x, y]
 


        matrix = seed_map.create_debug_matrix(0, 99, True)
        # rotate90Clockwise(matrix)
        printMatrix(matrix)
        # print(*matrix, sep='\n')
        


    def test_seed_soil(self):
        self.assertEqual(81, seed_map.seed_to_soil(79))

    def test_seed_location_lookup(self):
        self.assertEqual(82, seed_map.seed_to_loc(79))
        self.assertEqual(43, seed_map.seed_to_loc(14))
        self.assertEqual(86, seed_map.seed_to_loc(55))
        self.assertEqual(35, seed_map.seed_to_loc(13))
        
    # def test_zzz__seed_min_location(self):
    #     seed_map = create_seed_map()
    #     seed_map.split_mappings()
    #     self.assertEqual(46, seed_map.seed_with_lowest_location())
        
    def test_change_points(self):
        seed_map = create_seed_map()
        changes = seed_map.change_spots(0)
        self.assertLess(5, len(changes))
        self.assertEqual(0, changes[0])
        self.assertEqual(15, changes[1])
        lowest_all_points = seed_map.seed_with_lowest_location2(changes)
        
        changes_within = seed_map.map_seeds.points_within_some_range(changes)
        loweest_from_seeds = seed_map.seed_with_lowest_location2(changes_within)
        self.assertEqual(46, loweest_from_seeds)

if __name__ == '__main__':
    unittest.main()
    
