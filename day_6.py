# -*- coding: utf-8 -*-
import networkx as nx
import unittest

class OrbitTest(unittest.TestCase):
    
    def test_1(self):
        orbit = nx.parse_edgelist(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'], 
                                  delimiter=')')
        self.assertEqual(total_orbit_count(orbit), 42)
        

    def test_2(self):
        orbit = nx.parse_edgelist(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN'],
                                  delimiter=')')
        self.assertEqual(shortest_orbit_transfer(orbit), 4)
        
    
def total_orbit_count(G: nx.Graph):
    return sum(nx.single_source_shortest_path_length(G, 'COM').values())


def shortest_orbit_transfer(G: nx.Graph):
    return nx.shortest_path_length(G, source='YOU', target='SAN') - 2
    

if __name__ == '__main__':
    
    unittest.main()
    G = nx.read_edgelist('day_6_input.csv', delimiter=')')
    print('\n1.)', total_orbit_count(G))
    print('2.)', shortest_orbit_transfer(G))
    
