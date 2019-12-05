# -*- coding: utf-8 -*-
"""
Learnings:
    - tuple indexing/ np.arange
    - namedtuple
    - np.where
    - just use the most straightforward solution; More efficiency within inner loop only has a small effect (about x3)
    - get the index directions correct from the start, should also have added tests for .sum()
"""
import numpy as np
import unittest
from collections import namedtuple

CENTER = (10000, 10000) # (20,20) #
SIZE = 20000 # 40 #

class Test(unittest.TestCase):
    

    def test_1(self):
        data_1 = np.array(['R75','D30','R83','U83','L12','D49','R71','U7','L72'], dtype=np.str)
        data_2 = np.array(['U62','R66','U55','R34','D71','R55','D58','R83'], dtype=np.str)
        for b in (True, False):
            wire_1, ins_1 = parse_wire(data_1, None, b)
            wire_2, ins_2 = parse_wire(data_2, None, b)
            intersect = np.where(wire_1 & wire_2)
            dist = calc_closest(intersect)
            self.assertEqual(dist, 159)
            _, ins_dists_1 = parse_wire(data_1, wire_2.copy(), b) # do contain more...
            _, ins_dists_2 = parse_wire(data_2, wire_1.copy(), b) # actually contain only the intersect
            smallest_dist = calc_smallest_stepsum(ins_dists_1, ins_dists_2)
            self.assertEqual(smallest_dist, 610)

        
    def test_0(self):
        first = np.array(['R8','U5','L5','D3'])
        second = np.array(['U7','R6','D4','L4'])
        for b in (True, False):
            wire_1, ins_1 = parse_wire(first, None, b)
            wire_2, ins_2 = parse_wire(second, None, b)
            self.assertEqual(ins_1, {})
            self.assertEqual(ins_2, {})
            intersect = np.where(wire_1 & wire_2)
            dist = calc_closest(intersect)
            self.assertEqual(dist, 6)
            _, ins_dists_1 = parse_wire(first, wire_2, b)
            _, ins_dists_2 = parse_wire(second, wire_1, b)
            smallest_dist = calc_smallest_stepsum(ins_dists_1, ins_dists_2)
            self.assertEqual(smallest_dist, 30)


def calc_smallest_stepsum(dists_1, dists_2):
    smallest = 10000000000000000000
    real_intersections = dists_1.keys() & dists_2.keys()
    for key_tuple in real_intersections:
        total = dists_1[key_tuple] + dists_2[key_tuple]
        if total < smallest:
            smallest = total
    return smallest


def calc_closest(joint):
    closest = 10000000000000000000
    for i in range(0, len(joint[0])):
        if joint[0][i] == CENTER[0] and joint[1][i] == CENTER[1]:
            continue
        dist = np.abs(CENTER[0]-joint[0][i]) + np.abs(CENTER[1]-joint[1][i])
        if dist < closest:
            closest = dist
    return closest
        

def parse_wire(data: np.array, grid=None, use_numpy=True):
    """
    You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).
    find the intersection point closest to the central port. 
    Because the wires are on a grid, use the Manhattan distance for this measurement.
    Central point does not count.
    with array assignment:
    1. 49.8 ms ± 696 µs per loop
    2. 58.6 ms ± 500 µs per loop
    using the inner loop:
    1. 154 ms ± 5.19 ms per loop
    2. 160 ms ± 3.07 ms per loop 
    """
    if grid is None:
        grid = np.zeros((SIZE,SIZE), dtype=np.bool)
    grid[CENTER] = True
    intersections_to_dist = {}
    Position = namedtuple('Position', 'row col')
    dir_to_off = {'R': Position(0,1), 'L': Position(0,-1), 'U': Position(-1,0), 'D': Position(1,0)}
    prev = Position(*CENTER)
    dist=0
    
    for s in data:
        direction, step = s[0], int(s[1:])
        offset = dir_to_off[direction]
        
        if use_numpy:
            start = Position(prev.row+offset.row, prev.col+offset.col)
            row_step, col_step = 1,1
            if offset.row == 0:
                end = Position(start.row+1, start.col+offset.col*step)
                col_step = offset.col
            else:
                end = Position(start.row+offset.row*step, start.col+1)
                row_step = offset.row
            #print(f'S: {s}, prev: {prev}, offset: {offset} -> start: {start}, end: {end}')
            
            row_slice = np.arange(start.row,end.row,row_step)
            col_slice = np.arange(start.col,end.col,col_step)
            intersects = np.where(grid[row_slice, col_slice] == True)[0]
            for i in intersects:
                d_row, d_col = offset.row*i, offset.col*i
                key = Position(start.row+d_row, start.col+d_col)
                if grid[key] and key not in intersections_to_dist:
                    dist_from_start = dist + np.abs(d_row) + np.abs(d_col) + 1
                    # print(f'intersect: {i}, curr dist: {dist}, d_row: {d_row}, d_col: {d_col}, total: {dist_from_start}')
                    intersections_to_dist[key] = dist_from_start
                    
            grid[row_slice, col_slice] = True
            dist += step
            prev = Position(prev.row+offset.row*step, prev.col+offset.col*step)
        else:
            curr_row, curr_col = prev.row, prev.col
            for _ in range(step):
                curr_row += 1*offset.row
                curr_col += 1*offset.col
                curr_pos = Position(curr_row, curr_col)
                dist += 1
                if grid[curr_pos] and  curr_pos not in intersections_to_dist:
                    intersections_to_dist[curr_pos] = dist
                grid[curr_pos] = True
            prev = curr_pos
    return grid, intersections_to_dist
        

if __name__ == 'main':
    unittest.main()
    data_1 = np.array(['R1008','D256','L88','U390','R429','D828','R2','D452','L644','D942','R387','U221','L274','D837','R437','U664','R952','U126','L840','U425','L749','D199','L48','U394','L623','D562','L760','D856','L648','U666','R756','U396','L588','U217','R208','D492','L230','U60','L178','D211','L806','U423','L399','D159','L176','D555','R173','D946','L360','U415','L734','D441','L146','D332','R135','D529','L364','U742','L862','D790','L399','D392','R706','D740','L839','D950','R822','D27','R108','D873','L492','D465','L635','U771','L586','U66','R703','U943','R141','U396','R641','D339','R460','U295','L397','U799','R479','U963','L211','U933','R158','U248','R443','U807','R115','U885','R670','U116','L24','D980','R349','U363','L413','U444','L453','D497','L202','U300','L122','D895','L210','U218','R456','U293','L576','U968','L612','D225','L732','D34','R800','U925','R731','U520','R686','D181','L102','D824','R832','D527','L614','D624','R734','U552','L911','D352','R157','D70','R958','U317','L43','U902','R265','U986','R305','U264','L957','U888','R66','D413','L73','D642','R14','D559','R414','D985','R679','D965','R333','D332','L261','D446','L479','U430','L730','D37','L936','D615','L344','D215','R912','D95','L691','U383','L328','U560','R806','U711','R515','U448','R403','D109','L589','U458','L240','D375','L88','D479','R93','U794','L303','U783','L833','U500','R406','D589','L694','U504','L484','U695','R228','U813','R646','U768','L60','D326','L580','U840','L387','U147','L50','U155','L454','D574','L885','D705','R727','D827','R409','U335','L271','D388','R897','D563','L360','U70','R777','U903','R363','D202','R855','D159','R35','U585','L384','D540','R78','U13','R979','D702','L868','D868','R508','D552','L735','U923','R840','U133','L355','U282','R626','D699','L560','D26','R902','D873','L333','U492','L96','U461','R261','U784','L793','D723','R887','U836','R790','D400','L331','U389','L107','U534','L377','D831','R181','U325','L328','U778','L498','D109','L692','U185','R284','U930','R784','D843','L261','U119','L751','U313','R197','U911','L21','D201','L881','U119','R210','D700','R93','U208','R116'], 
                      dtype=np.str)
    data_2 = np.array(['L1009','D700','L634','U294','R898','D947','R650','U988','L623','D968','R761','U490','R525','U76','R633','D139','R348','D855','L983','U553','L454','D211','L240','D465','R260','U285','R653','D734','L346','U434','R813','U599','R98','D779','L58','D6','R309','U437','L712','U896','R262','U911','R400','D247','R297','U915','L223','D591','L755','D398','L980','U177','R186','U882','R418','U763','L741','D60','L942','U648','L430','D401','R30','D157','L901','D179','L615','U535','L586','D613','L606','U239','L133','D251','L549','D579','R612','U307','L127','D343','L43','D288','R245','U122','R352','D527','R476','U24','L805','U291','R953','D469','L941','U577','L384','U345','L463','D50','R311','D649','L746','D902','R644','U913','R147','D649','R848','D673','R93','U65','R363','U734','L289','U599','R738','U45','R128','D508','L93','D201','R51','U239','R17','D496','L661','D912','R165','U291','L207','D308','R241','D388','L910','D821','R714','D327','L605','U880','L682','D934','R334','D1','R602','D54','L51','D913','L575','U168','R614','D603','R452','U718','R689','D505','R83','D385','R636','D692','R424','D573','R686','D572','L467','D698','L21','U510','L497','U329','R286','U733','R584','U919','R499','U971','L558','U511','L565','D623','L502','U536','L483','U372','L686','D420','L900','U316','L37','U372','L915','D641','R165','D927','L137','U231','R813','U416','L131','D530','R486','U795','L507','U757','L208','U308','L521','U583','L758','U654','R554','D467','R381','U155','R47','U829','R92','D158','R54','D500','R17','D471','R748','U571','L194','D55','L921','U271','L730','U207','L204','U806','R19','D33','R218','D911','L106','U220','R551','U308','L268','U5','L374','U657','R639','U705','R294','U962','L927','U892','L477','U290','R378','D193','L154','U859','L618','D690','L769','D779','R752','D915','L693','D586','L558','D864','L523','U354','R386','U236','R888','U302','L75','U628','R132','D306','L939','U73','L687','D488','R21','D760','L856','U96','L116','U557','L639','U812','L389','D364','L807','U696','R781','D625','R565','U728','R134','D406','R785','U583','R60','D819','L939'],
                      dtype=np.str)
    wire_1, ins_1 = parse_wire(data_1)
    wire_2, ins_2 = parse_wire(data_2)
    intersect = np.where(wire_1 & wire_2)
    print('1)', calc_closest(intersect))
    
    _, ins_dists_1 = parse_wire(data_1, wire_2.copy())
    _, ins_dists_2 = parse_wire(data_2, wire_1.copy())
    # wtf - they have 159 in common, but 71 are only in 2 and 120 are only in 1??? -> self-crossings.
    smallest_dist = calc_smallest_stepsum(ins_dists_1, ins_dists_2)
    print('2)', smallest_dist)