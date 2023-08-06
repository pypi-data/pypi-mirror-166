## An Example of using LineFinder Package

# imprt the package(s)
from pykea.LineFinder import LineFinder

# instantiate an object
lf = LineFinder(hsv_v_max=20, 
                display_contour=True, 
                h_start=380,
                h_end=480,
                w_start=0,
                w_end=640,
                min_area=500,
                max_area=90000)

# start processing
lf.process

# get cam data
lf.line_center_xy()
lf.line_angle()
lf.line_area()


