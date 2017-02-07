# For each cylinder in the scan, find its cartesian coordinates,
# in the scanner's coordinate system.
# Write the result to a file which contains all cylinders, for all scans.
# 03_d_find_cylinders_cartesian
# Claus Brenner, 09 NOV 2012
from lego_robot import *
from math import sin, cos

# Find the derivative in scan data, ignoring invalid measurements.
def compute_derivative(scan, min_dist):
    jumps = [ 0 ]
    for i in xrange(1, len(scan) - 1):
        l = scan[i-1]
        r = scan[i+1]
        if l > min_dist and r > min_dist:
            derivative = (r - l) / 2.0
            jumps.append(derivative)
        else:
            jumps.append(0)
    jumps.append(0)
    return jumps

# For each area between a left falling edge and a right rising edge,
# determine the average ray number and the average depth.
def find_cylinders(scan, scan_derivative, jump, min_dist):
    cylinder_list = []
    on_cylinder = False
    sum_ray, sum_depth, rays = 0.0, 0.0, 0

    # --->>> Insert here your previous solution from find_cylinders_question.py.
    
    for i in xrange(len(scan_derivative)):
        # --->>> Insert your cylinder code here.
        # Whenever you find a cylinder, add a tuple
        # (average_ray, average_depth) to the cylinder_list.
        # Just for fun, I'll output some cylinders.
        # Replace this by your code.
        #if scan[i] > min_dist:
        if scan_derivative[i] < -100:
            on_cylinder = True
            current = "l"
        if scan_derivative[i] < -100 and current == "l":
            rays = 0
            sum_ray = 0
            sum_depth = 0
        if on_cylinder:
            if scan[i] > min_dist:
                rays = rays + 1
                sum_ray = sum_ray + i
                sum_depth = sum_depth + scan[i]
            else:
                rays = rays
                sum_ray = sum_ray
                sum_depth = sum_depth
        if scan_derivative[i] >= 100 and on_cylinder:
            on_cylinder = False
            current = "r"
            i = sum_ray/rays
            lst = list(scan)
            lst[i] = sum_depth/rays
            scan = tuple(lst)
            cylinder_list.append( (i, scan[i]) )
    return cylinder_list

def compute_cartesian_coordinates(cylinders, cylinder_offset):
    result = []
    #print cylinders # for debugging
    Cylinder_lst = list(cylinders)
    #print Cylinder_lst # for debugging
    for c in cylinders:
        # --->>> Insert here the conversion from polar to Cartesian coordinates.
        # c is a tuple (beam_index, range).
        # For converting the beam index to an angle, use
        # LegoLogfile.beam_index_to_angle(beam_index)
        beam_index,beam_range = c
        #print "beam_index is: ",beam_index
        angle = LegoLogfile.beam_index_to_angle(beam_index)
        #print "angle is: ",angle
        x = (beam_range + cylinder_offset) * cos(angle)
        y = (beam_range + cylinder_offset) * sin(angle)
        #print (x,y)
        result.append( (x,y) ) 
    return result
        

if __name__ == '__main__':

    minimum_valid_distance = 20.0
    depth_jump = 100.0
    cylinder_offset = 90.0

    # Read the logfile which contains all scans.
    logfile = LegoLogfile()
    logfile.read("robot4_scan.txt")

    # Write a result file containing all cylinder records.
    # Format is: D C x[in mm] y[in mm] ...
    # With zero or more points.
    # Note "D C" is also written for otherwise empty lines (no
    # cylinders in scan)
    out_file = file("cylinders.txt", "w")
    for scan in logfile.scan_data:
        # Find cylinders.
        der = compute_derivative(scan, minimum_valid_distance)
        cylinders = find_cylinders(scan, der, depth_jump,
                                   minimum_valid_distance)
        cartesian_cylinders = compute_cartesian_coordinates(cylinders,
                                                            cylinder_offset)
        # Write to file.
        print >> out_file, "D C",
        for c in cartesian_cylinders:
            print >> out_file, "%.1f %.1f" % c,
        print >> out_file
    out_file.close()
