
__author__ = "David den Ouden"
__version__ = "01.11.2019 Final"

import rhinoscriptsyntax as rs
import math
import decimal
import random
import time
from math import sqrt

"""
Short description of the script:
    This script takes points as input and makes shop objects using the class Shop
    on all of those points. Then those shops are all empty except for the starting shops, 
    which are set to occupied and values for function, pollution, distance to nearest house, and noise are added
    with this as a starting position, a series of random input determine new shops that are added to the bazaar
    these new shops will be appointed 5 top locations from which one is selected
    these locations are found by computing the difference between the previously mentioned values of the new shop and all existing ones
    keep in mind that only the difference between neighbouring available slots (empty slots next to occupied slot) and new shops are taken into account
    Those differences are then multiplied by a factor determined by the admins (weigh factors)
    And also they are multiplied by a factor which is computed using the distances between the 2 shops
    One of the 5 locations is chosen and the new shop is set to occupied adn the values are added
    As a last step the distances for a shop to the nearest house are recomputed
    
    In a newer version the user also has the option to choose a size, small medium or large
    A large or medium shop will in essention 'just' fill multiple small slots
"""

class Shop:
    """This class will be used to make objects based on points, which are then;
    'shops' these shops have certain variables and can be either occupied or empty"""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.occupied = False
        self.house = False
        self.noise = None
        self.function = None
        self.pollution = None
        self.distance = None
        
    def get_point(self):
        """represent the point the shop is located as a list [x,y,z]"""
        self.point = [self.x, self.y, 0]
        return self.point
        
    def set_occupied(self):
        """make the shop actually real"""
        self.occupied = True

    def find_neighbour_points(self, gridsize, gridsize_2, point=None):
        """find all possible neighbour (using gridsizes) points 
            although some may be imaginary and return them as a list"""
        if point:
            point_1 = [(point[0]+gridsize),point[1],point[2]]
            point_2 = [(point[0]-gridsize),point[1],point[2]]
            point_3 = [point[0],(point[1]+gridsize),point[2]]
            point_4 = [point[0],(point[1]-gridsize),point[2]]
            point_5 = [(point[0]+gridsize_2),point[1],point[2]]
            point_6 = [(point[0]-gridsize_2),point[1],point[2]]
            point_7 = [point[0],(point[1]+gridsize_2),point[2]]
            point_8 = [point[0],(point[1]-gridsize_2),point[2]]
            possible_neighbours = []
            possible_neighbours.append(point_1)
            possible_neighbours.append(point_2)
            possible_neighbours.append(point_3)
            possible_neighbours.append(point_4)
            possible_neighbours.append(point_5)
            possible_neighbours.append(point_6)
            possible_neighbours.append(point_7)
            possible_neighbours.append(point_8)
            return possible_neighbours
        else:
            return None

    def find_neighbour_points_4(self, gridsize, gridsize_2, point=None):
        """find all possible direct neighbours (using gridsizes) 
            points although some may be imaginary and return them as a list"""
        if point:
            point_1 = [(point[0]+gridsize),point[1],point[2]]
            point_2 = [(point[0]-gridsize),point[1],point[2]]
            point_3 = [point[0],(point[1]+gridsize),point[2]]
            point_4 = [point[0],(point[1]-gridsize),point[2]]
            possible_neighbours = []
            possible_neighbours.append(point_1)
            possible_neighbours.append(point_2)
            possible_neighbours.append(point_3)
            possible_neighbours.append(point_4)
            return possible_neighbours
        else:
            return None

    def draw_shop(self, point, shop = None, xaxis = None):
        """visualize the shop by drawing the rectangle;
            this should also depend on wether its a junction or another type of shop"""
        z = (0,0,1)
        w = 2575
        if shop.type != "junction":
            if xaxis[1] == 1:
                point = (point[0]+1800, point[1]+w/2, 0)
                plane = rs.PlaneFromNormal(point, z, xaxis)
                w = -1 *w
                chosen_location = rs.AddRectangle( plane, w, 3600 ) 
            else:
                point[0] = point[0] -w/2
                point[1] = point[1] -1800
                plane = rs.PlaneFromNormal(point, z, xaxis)
                chosen_location = rs.AddRectangle( plane, w, 3600 )
        else:
            if xaxis == "dl":
                point = (point[0]-w/2, point[1]-w/2, 0)
                plane = rs.PlaneFromNormal(point, z)
                chosen_location = rs.AddRectangle( plane, 3087.5, 3087.5)
            elif xaxis == "ul":
                point = (point[0]-w/2, point[1]+w/2, 0)
                plane = rs.PlaneFromNormal(point, z)
                chosen_location = rs.AddRectangle( plane, 3087.5, -3087.5)
            elif xaxis == "ur":
                point = (point[0]+w/2, point[1]+w/2, 0)
                plane = rs.PlaneFromNormal(point, z)
                chosen_location = rs.AddRectangle( plane, -3087.5, -3087.5)
            else:
                point = (point[0]+w/2, point[1]-w/2, 0)
                plane = rs.PlaneFromNormal(point, z)
                chosen_location = rs.AddRectangle( plane, -3087.5, 3087.5)
        return chosen_location
        
    def add_values(self,noise,function,pollution,distance):
        """add the values of an existing shop"""
        self.noise = noise
        self.function = function
        self.pollution = pollution
        self.distance = distance
        
    def find_distances(self,points):
        """find the distances from a shop (wether empty or not) to a list of points"""
        distances = []
        for point in points:
            distance = sqrt(abs(self.x - point[0])*abs(self.x - point[0])+ abs(self.y - point[1])*abs(self.y - point[1]))
            distances.append(distance)
        return distances
        
    def set_house(self):
        """set an occupied shop to have a house on top"""
        self.house = True
    
    def find_xaxis(self,point, neighbourpoints, all_points, shop):
        """find the axis of the street the shop is on, this is different for a junction shop
            as they need to be oriented in two directions"""
        real_shops = []
        neighbourpoints_r = []
        for pnt in neighbourpoints[0:4]:
            if pnt in all_points:
                real_shops.append(pnt)
        if shop.type == "junction":
            if point[0] - real_shops[0][0] > 0 or point[0] - real_shops[1][0] > 0:
                if point[1] - real_shops[0][1] > 0 or point[1] - real_shops[1][1] > 0:
                    xaxis = "dl"
                else:
                    xaxis = "ul"
            else:
                if point[1] - real_shops[0][1] > 0 or point[1] - real_shops[1][1] > 0:
                    xaxis = "dr"
                else:
                    xaxis = "ur"
        elif point[0] - real_shops[0][0] == 0:
            xaxis = (0,1,0)
        else:
            xaxis = (1,0,0)
        return xaxis
        
def find_integers_nbs(points, shops):
    """if you have a point of a shop, this method finds the integer(s) of the corresponding shops"""
    shop_index = []
    if points:
        for point in points:
            for index, shop in enumerate(shops):
                if point[0] == shop.x and point[1] == shop.y:
                    shop_index.append(index)
                else:
                    pass
        return shop_index
    else:
        return None

def remap(list, high=100):
    """remap all numbers in a list to a maximum value, the default is 100"""
    remapped_nrs = []
    for item in list:
        remapped = ((item-min(list))/(max(list)-min(list))) *high
        remapped = int(round(remapped))
        remapped_nrs.append(remapped)
    return remapped_nrs


#make nice python lists
x_end = (x_end.split(","))
y_end = (y_end.split(","))
x_junction = x_junction.split(",")
y_junction = y_junction.split(",")
x_street = x_street.split(",")
y_street = y_street.split(",")
x_square = x_square.split(",")
y_square = y_square.split(",")


#make every lists integers
x_end = list(map(int, x_end))
y_end = list(map(int, y_end))
x_junction = list(map(int, x_junction))
y_junction = list(map(int, y_junction))
x_street = list(map(int, x_street))
y_street = list(map(int, y_street))
x_square = list(map(int,x_square))
y_square = list(map(int,y_square))
occupied = list(map(int, occupied))
noises = list(map(int, noises))
functions = list(map(int, functions))
pollutions = list(map(int, pollutions))
distances = list(map(int, distances))

#remap some of the functions to a range of 0-100
noises_r = remap(noises)
functions_r = remap(functions)
pollutions_r = remap(pollutions)
distances_r = remap(distances)

#make shops from class Shop and append them to empty list
shops = []
for i in range(len(x_street)):
    shop= Shop(x_street[i],y_street[i],"street")
    shops.append(shop)
for i in range(len(x_end)):
    shop= Shop(x_end[i],y_end[i],"end")
    shops.append(shop)
for i in range(len(x_junction)):
    shop= Shop(x_junction[i],y_junction[i],"junction")
    shops.append(shop)
for i in range(len(x_square)):
    shop= Shop(x_square[i],y_square[i],"square")
    shops.append(shop)

#import the shops that are already occupied
#assign all the remapped values (noise,pollution,function, distance) for the shops that are occupied
#also assign a house if the shop has one
for index, i in enumerate(occupied):
    shops[i].set_occupied()
    shops[i].add_values(noises_r[index],functions_r[index],pollutions_r[index],distances_r[index])
    if houses[index] == 'yes':
        shops[i].set_house()
    else:
        pass

#find all possible points in lists of [x,y,z] to be used later
all_shop_points = []
for shop in shops:
    pnt = shop.get_point()
    all_shop_points.append(pnt)


#draw existing shops
existing_shops___ =[]
for shop in shops:
    if shop.occupied:
        point = shop.get_point()
        nbpnts = shop.find_neighbour_points(gridsize, gridsize_2, point)
        xaxis = shop.find_xaxis(point, nbpnts, all_shop_points, shop)
        rectangle = shop.draw_shop(point,shop, xaxis)
        existing_shops___.append(rectangle)
    else:
        pass

#multiply the weighfactors 
#(for some reason the distance weight for social security outweighted all others)
wn = wn**2
wf = wf**2
wp = wp**2
wd = wd**0.25


#make a partition list and add the first 3 shops (which are already defined in the excel file)
partition_list = [1,1,1]

#now start a loop that generates the bazaar based on rng provided by a seperate python script
#this is to prevent the random numbers to be regenerated everytime the number of iterations is changed

#####################################################
### HERE STARTS THE FOR LOOP THAT GENERATES AUTO ####
#####################################################

if run:
    for nr in range(iterations):
        #checking the usershop size
        
        user_size = user_sizes[nr]
        
        #getting a random number to essentially choose from a catalogue
        random_nr = rng[nr]
        #teashop
        if random_nr == 0:
            user_noise = 40
            user_pollution = 30
            user_function = 0
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #restaurant
        elif random_nr == 1 or random_nr == 13:
            user_noise = 70
            user_pollution = 40
            user_function = 0
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #herb_store
        elif random_nr == 2:
            user_noise = 20
            user_pollution = 20
            user_function = 1
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #vegetable_store
        elif random_nr == 3:
            user_noise = 10
            user_pollution = 30
            user_function = 1
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #bakery
        elif random_nr == 4:
            user_noise = 40
            user_pollution = 30
            user_function = 1
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #butcher
        elif random_nr == 5:
            user_noise = 50
            user_pollution = 50
            user_function = 1
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #fabrics
        elif random_nr == 6:
            user_noise = 20
            user_pollution = 10
            user_function = 2
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #pharmacy
        elif random_nr == 7:
            user_noise = 10
            user_pollution = 40
            user_function = 2
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #phonestore
        elif random_nr == 8:
            user_noise = 20
            user_pollution = 0
            user_function = 2
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #coppersmith
        elif random_nr == 9:
            user_noise = 80
            user_pollution = 50
            user_function = 3
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #blacksmith
        elif random_nr == 10:
            user_noise = 100
            user_pollution = 70
            user_function = 3
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #furnature
        elif random_nr == 11:
            user_noise = 80
            user_pollution = 100
            user_function = 3
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'
        #pottery
        elif random_nr == 12:
            user_noise = 30
            user_pollution = 60
            user_function = 3
            user_choice = user_choise_rng[nr]
            house = house_rng[nr]
            if house == 0:
                user_house = 'yes'
            else:
                user_house = 'no'

        #remap the 'user'input
        user_noise_r = user_noise
        user_pollution_r = user_pollution
        user_function_r =  ((user_function-min(functions))/(max(functions)-min(functions))) *100
    
        
        
        #find all shops that are not occupied
        #check to see wether these open slots are actually adjecent to an already built shop = available
        occupied_points = []
        available_shops = [] 
        unoccupied_points = []
        possible_points_m = []
        possible_points_m_p = []
        possible_points_l = []
        m_points = []
        for o in occupied:
            occupied_points.append(shops[o].get_point())
        for ix,shop in enumerate(shops):
            if shop.occupied == False:
                point = shop.get_point()
                unoccupied_points.append(point)
                #find the neighbouring points of these points and see if any belong to an already built shop
                if user_size == "s":
                    nbs = shop.find_neighbour_points(gridsize,gridsize_2,point)
                    check = False
                    for neighbour in nbs:
                        if neighbour in occupied_points:
                            check = True
                    if check == True:
                        available_shops.append(ix)
                #so now the hard part, if the shopsize is not small, 
                #we should not append it to available shops directly but to a seperate list
                if user_size == "m" or user_size == "l":
                    nbs = shop.find_neighbour_points(gridsize,gridsize_2,point)
                    check = False
                    for neighbour in nbs:
                        if neighbour in occupied_points:
                            check =True
                    if check == True:
                        possible_points_m.append(ix)
                        m_point = shop.get_point()
                        possible_points_m_p.append(m_point)
                    
        #now we can run over the seperate list and check if they have an available neighbour
        if user_size == "m" or user_size == "l":
            for index in possible_points_m:
                pnt = shops[index].get_point()
                nbps = shops[index].find_neighbour_points_4(gridsize,gridsize_2,pnt)
                check_m = False
                
                for nb in nbps:
                    if nb in unoccupied_points:
                        check_m = True
                        possible_points_l.append(nb)
                        m_points.append(pnt)
                        if check_m == True:
                            break
                if user_size == "m":
                    if check_m == True:
                        available_shops.append(index)
                """
                if user_size == "l":
                    if check_m == True:
                        m_points.append(pnt)
                """

        #if the user size is large, the empty neighbour needs to have 2 more empty neighbours
        #to create a sequence of 4 empty slots where at least one is adjecent to an occupied slot
        #now it is also important to make sure that all these 4 slots are unique so its not a chain of 2 slots that are counted twice
        if user_size == "l":
            possible_shops_l = find_integers_nbs(possible_points_l, shops)
            m_shops = find_integers_nbs(m_points,shops)
            for middle,index,available in zip(m_points,possible_shops_l,m_shops):
                pnt = shops[index].get_point()
                nbps = shops[index].find_neighbour_points_4(gridsize,gridsize_2,pnt)
                middle_point = middle

                check_l = False
                for nb in nbps:
                    if nb in unoccupied_points and nb != middle_point:
                        check_l = True
                        l_point = nb
                        if check_l == True:
                            break
                l_shop = find_integers_nbs([l_point],shops)
                nbps_2 = shops[l_shop[0]].find_neighbour_points_4(gridsize,gridsize_2,l_point)
                check_l2 = False
                for nb_2 in nbps_2:
                    if nb_2 in unoccupied_points and nb_2 != pnt:
                        check_l2 = True
                if user_size == "l":
                    if check_l == True and check_l2 == True:
                        available_shops.append(available)
        
        
        
        #draw existing shops
        existing_shops =[]
        for shop in shops:
            if shop.occupied:
                available_points = []
                for indexx in available_shops:
                    pnt = shops[indexx].get_point()
                    available_points.append(pnt)
                point = shop.get_point()
                nbpnts = shop.find_neighbour_points(gridsize, gridsize_2, point)
                xaxis = shop.find_xaxis(point, nbpnts, all_shop_points, shop)
                rectangle = shop.draw_shop(point,shop, xaxis)
                existing_shops.append(rectangle)
            else:
                pass
        
        #now for every every element we should compute the distance to occupied slots as a list
        #(in a future version i would like to check only the distanes within a certain range, but for now this isnt necassary)
        #and then after immidiately check the most optimal spot based on the difference between noise function pollution and 
        #house distance and as a function of the previously computed distances between the new shop and all existing shops
        slot_qualifications = []
        flag = False
        length_loop = len(available_shops)

        for i in available_shops:
            distances_occupied = shops[i].find_distances(occupied_points)
            for index__,distance in enumerate(distances_occupied):
                if distance > 50000:
                    distances_occupied[index__] =50000
            d = remap(distances_occupied,10)
            for index_,distance in enumerate(d):
                d[index_] = (10 -distance)/10
            qualifications = []
            for j,x in enumerate(occupied):
                noise_difference = (abs(user_noise_r-shops[x].noise) * wn *d[j] )
                qualifications.append(noise_difference)
                function_difference = (abs(user_function_r-shops[x].function) *wf *d[j])
                qualifications.append(function_difference)
                pollution_difference = (abs(user_pollution_r-shops[x].pollution) * wp * d[j])
                qualifications.append(pollution_difference)
                if user_house == 'yes' and shops[x].house == False:
                    qualifications.append((shops[x].distance * wd*-1 *d[j]))
                elif user_house == 'yes' and shops[x].house == True:
                    qualifications.append((shops[x].distance * wd * d[j] ))
                elif user_house == 'no' and shops[x].house == True:
                    qualifications.append((shops[x].distance * wd*-1 *d[j]))
                else:
                    qualifications.append((shops[x].distance * wd * d[j] ))
                    
            qualifications = sum(map(float,qualifications))
            #now apply a bonus factor if a community shop [0] is going to occupy a junction
            #also apply a negative factor if any shop but community is going to occupy a junction
            if user_function == 0:
                if shops[i].type == 'junction':
                    qualifications = qualifications * 0.75
            else:
                if shops[i].type == 'junction':
                    qualifications = qualifications * 1.25
            #now apply a bonus factor if a community or workshop [0/3] is going to occupy a square
            #also apply a negative factor if any shop but community is going to occupy a square
            if user_function == 0 or user_function == 3:
                if shops[i].type == 'square':
                    qualifications = qualifications * 0.75
            else:
                if shops[i].type == 'square':
                    qualifications = qualifications * 1.25
            slot_qualifications.append(qualifications)

        #find the top 5 locations
        user_shop_integers = []
        user_shop_integer_1 = slot_qualifications.index(min(slot_qualifications))
        user_shop_integers.append(user_shop_integer_1)
        slot_qualifications[user_shop_integer_1] = 1000000000
        user_shop_integer_2 = slot_qualifications.index(min(slot_qualifications))
        user_shop_integers.append(user_shop_integer_2)
        slot_qualifications[user_shop_integer_2] = 1000000000
        user_shop_integer_3 = slot_qualifications.index(min(slot_qualifications))
        user_shop_integers.append(user_shop_integer_3)
        slot_qualifications[user_shop_integer_3] = 1000000000
        user_shop_integer_4 = slot_qualifications.index(min(slot_qualifications))
        user_shop_integers.append(user_shop_integer_4)
        slot_qualifications[user_shop_integer_4] = 1000000000
        user_shop_integer_5 = slot_qualifications.index(min(slot_qualifications))
        user_shop_integers.append(user_shop_integer_5)
        
        #visual feedback for the user to know which shop he is chosing
        #make all options visual
        shop_options = []
        shop_options_integers = []
        for k in user_shop_integers:
            rectangles = []
            shop_option_integer = available_shops[k]
            #if the user size isnt small 2 rectangles should be drawn
            if user_size == "m" or user_size == "l":
                mpoint = shops[shop_option_integer].get_point()
                mediumsizes = shops[shop_option_integer].find_neighbour_points_4(gridsize, gridsize_2, mpoint)
                m_real_points = []
                for m in mediumsizes:
                    if m in unoccupied_points:
                        m_real_points.append(m)
                m_real = find_integers_nbs(m_real_points, shops)
                if m_real:
                    point_2 = shops[m_real[0]].get_point()
                    nbpnts_2 = shops[m_real[0]].find_neighbour_points_4(gridsize, gridsize_2, point_2)
                    xaxis_2 = shops[m_real[0]].find_xaxis(point_2, nbpnts_2, all_shop_points, shops[m_real[0]])
                    rectangle_2 = shops[m_real[0]].draw_shop(point_2, shops[m_real[0]], xaxis_2)
                    rectangles.append(rectangle_2)
                    shop_options.append(rectangle_2)
            #if the usersize is large 4 rectangles should be drawn
            if user_size == "l":
                l_real_points = []
                l_point = shops[m_real[0]].get_point()
                m_point = shops[shop_option_integer].get_point()
                largesizes = shops[m_real[0]].find_neighbour_points_4(gridsize, gridsize_2, l_point)
                for l in largesizes:
                    if l in unoccupied_points and l != mpoint:
                        l_real_points.append(l)

                l_real = find_integers_nbs(l_real_points, shops)
                if l_real:
                    point_3 = shops[l_real[0]].get_point()
                    nbpnts_3 = shops[l_real[0]].find_neighbour_points_4(gridsize, gridsize_2, point_3)
                    xaxis_3 = shops[l_real[0]].find_xaxis(point_3, nbpnts_3, all_shop_points, shops[l_real[0]])
                    rectangle_3 = shops[l_real[0]].draw_shop(point_3, shops[l_real[0]], xaxis_3)
                    rectangles.append(rectangle_3)
                    shop_options.append(rectangle_3)
                    
                    l_real_points_2 = []
                    for l2 in nbpnts_3:
                        if l2 in unoccupied_points and l2 != l_point:
                            l_real_points_2.append(l2)
                    l_real_2 = find_integers_nbs(l_real_points_2,shops)
                    if l_real_2:
                        point_4 = shops[l_real_2[0]].get_point()
                        nbpnts_4 = shops[l_real_2[0]].find_neighbour_points_4(gridsize, gridsize_2, point_4)
                        xaxis_4 = shops[l_real_2[0]].find_xaxis(point_4, nbpnts_4, all_shop_points, shops[l_real_2[0]])
                        rectangle_4 = shops[l_real_2[0]].draw_shop(point_4, shops[l_real_2[0]], xaxis_4)
                        rectangles.append(rectangle_4)
                        shop_options.append(rectangle_4)
                
            point = shops[shop_option_integer].get_point()
            nbpnts = shops[shop_option_integer].find_neighbour_points_4(gridsize, gridsize_2, point)
            xaxis = shops[shop_option_integer].find_xaxis(point, nbpnts, all_shop_points, shops[shop_option_integer])
            rectangle = shops[shop_option_integer].draw_shop(point, shops[shop_option_integer], xaxis)
            
            rectangles.append(rectangle)
            shop_options.append(rectangle)
            shop_options_integers.append(shop_option_integer)
            
            
            
        #let the user see his current choice (same as visualising all choises but then only for one of the 5)
        #(iknow this could probably be done in the previous loop but ok)
        user_integer =user_shop_integers[int(user_choice)]
        user_shop = available_shops[user_integer]
        chosen_location = []
        if user_size == "m" or user_size == "l":
                mpoint = shops[user_shop].get_point()
                mediumsizes = shops[user_shop].find_neighbour_points_4(gridsize, gridsize_2, mpoint)
                m_real_points = []
                for m in mediumsizes:
                    if m in unoccupied_points:
                        m_real_points.append(m)
                m_real_u = find_integers_nbs(m_real_points, shops)
                if m_real_u:
                    point_2 = shops[m_real_u[0]].get_point()
                    nbpnts_2 = shops[m_real_u[0]].find_neighbour_points_4(gridsize, gridsize_2, point_2)
                    xaxis_2 = shops[m_real_u[0]].find_xaxis(point_2, nbpnts_2, all_shop_points, shops[m_real_u[0]])
                    rectangle_2 = shops[m_real_u[0]].draw_shop(point_2, shops[m_real_u[0]], xaxis_2)
                    rectangles.append(rectangle_2)
                    chosen_location.append(rectangle_2)
                    existing_shops___.append(rectangle_2)
                    
        if user_size == "l":
            l_real_points = []
            l_point = shops[m_real_u[0]].get_point()
            m_point = shops[user_shop].get_point()
            largesizes = shops[m_real_u[0]].find_neighbour_points_4(gridsize, gridsize_2, l_point)
            for l in largesizes:
                if l in unoccupied_points and l != mpoint:
                    l_real_points.append(l)

            l_real_u = find_integers_nbs(l_real_points, shops)
            if l_real_u:
                point_3 = shops[l_real_u[0]].get_point()
                nbpnts_3 = shops[l_real_u[0]].find_neighbour_points_4(gridsize, gridsize_2, point_3)
                xaxis_3 = shops[l_real_u[0]].find_xaxis(point_3, nbpnts_3, all_shop_points, shops[l_real_u[0]])
                rectangle_3 = shops[l_real_u[0]].draw_shop(point_3, shops[l_real_u[0]], xaxis_3)

                rectangles.append(rectangle_3)
                chosen_location.append(rectangle_3)
                existing_shops___.append(rectangle_3)
                
                l_real_points_2 = []
                for l2 in nbpnts_3:
                    if l2 in unoccupied_points and l2 != l_point:
                        l_real_points_2.append(l2)
                l_real_u2 = find_integers_nbs(l_real_points_2,shops)
                if l_real_2:
                    point_4 = shops[l_real_u2[0]].get_point()
                    nbpnts_4 = shops[l_real_u2[0]].find_neighbour_points_4(gridsize, gridsize_2, point_4)
                    xaxis_4 = shops[l_real_u2[0]].find_xaxis(point_4, nbpnts_4, all_shop_points, shops[l_real_u2[0]])
                    rectangle_4 = shops[l_real_u2[0]].draw_shop(point_4, shops[l_real_u2[0]], xaxis_4)
                    rectangles.append(rectangle_4)
                    chosen_location.append(rectangle_4)
                    existing_shops___.append(rectangle_4)
                
        point = shops[user_shop].get_point()
        nbpnts = shops[user_shop].find_neighbour_points_4(gridsize, gridsize_2, point)
        xaxis = shops[user_shop].find_xaxis(point, nbpnts, all_shop_points, shops[user_shop])
        rectangle = shops[user_shop].draw_shop(point, shops[user_shop], xaxis)
        chosen_location.append(rectangle)
        existing_shops___.append(rectangle)
        
        
       #This is an important step for the past processing, the partition list will help see which shops 
       #should be considered as one shop (as large and medium shops are build from multiple small ones)
        if user_size == "m":
            partition_list.append("2")
        elif user_size == "l":
            partition_list.append("4")
        else:
            partition_list.append("1")
        

        #set the chosen shop to occupied
        #if the user size is medium or large, set multiple shops to occupied
        shops[user_shop].set_occupied()
        occupied.append(user_shop)
        if user_size == "m" or user_size == "l":
            shops[m_real_u[0]].set_occupied()
            occupied.append(m_real_u[0])
        if user_size == "l" :
            shops[l_real_u[0]].set_occupied()
            occupied.append(l_real_u[0])
            shops[l_real_u2[0]].set_occupied()
            occupied.append(l_real_u2[0])
        
        #set the chosen shop to house if there is a house
        #if the user size is medium or large, set multiple houses
        if user_house == 'yes':
            shops[user_shop].set_house()
            if user_size == "m" or user_size == "l":
                shops[m_real_u[0]].set_house()
            if user_size == "l":
                shops[l_real_u[0]].set_house()
                shops[l_real_u2[0]].set_house()
        else:
            pass
        
        #although this is a legacy function, I might still need this in the future
        #append user values to excellist ouput
        #if shopsize is medium or large, append it multiple times
        noises.append(user_noise)
        functions.append(user_function)
        pollutions.append(user_pollution)
        if user_size == "m" or user_size == "l":
            noises.append(user_noise)
            functions.append(user_function)
            pollutions.append(user_pollution)
        if user_size == "l":
            noises.append(user_noise)
            functions.append(user_function)
            pollutions.append(user_pollution)
            noises.append(user_noise)
            functions.append(user_function)
            pollutions.append(user_pollution)
        
        #find a method to recalculate the housing distances and change the houses
        distances = []
        houses = []
        pnts = []
        for l in occupied:
            if shops[l].house == True:
                pnt = shops[l].get_point()
                pnts.append(pnt)
        for indx,value in enumerate(occupied):
            dstncs = shops[value].find_distances(pnts)
            distances.append(min(dstncs))
            if shops[value].house == True:
                houses.append('yes')
            else:
                houses.append('no')
        
        #add values to chosen shop
        #again, if the size is m or l, add values to multiple shops
        shops[user_shop].add_values(user_noise_r,user_function_r,user_pollution_r,distances[-1])
        if user_size == "m" or user_size == "l":
            shops[m_real_u[0]].add_values(user_noise_r,user_function_r,user_pollution_r,distances[-1])
        if user_size == "l":
            shops[l_real_u[0]].add_values(user_noise_r,user_function_r,user_pollution_r,distances[-1])
            shops[l_real_u2[0]].add_values(user_noise_r,user_function_r,user_pollution_r,distances[-1])
        distances = list(map(int, distances))


