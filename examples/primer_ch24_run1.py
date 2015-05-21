
import Shadow

#
# initializa Shadow objects
#
source = Shadow.Source()
beam = Shadow.Beam()
oe = Shadow.OE()


flag_write_files = 1 #write shadow files

#number of rays
source.NPOINT  =  1000  
#seed
source.ISTAR1  =  10001 
#point source
source.FSOUR  =  0 
#flat distribution in divergences, and values
source.FDISTR  =  1  
source.HDIV1  =  0.05  
source.HDIV2  =  0.05  
source.VDIV1  =  0.01  
source.VDIV2  =  0.01  
#monochromatic: 0 eV
source.F_COLOR  =  1 
source.F_PHOT  =  0  
source.PH1  =  0.0  
source.POL_DEG  =  1.0 


if flag_write_files: source.write("start_py.00")
beam.genSource(source)
if flag_write_files: beam.write("begin.dat")



oe.T_INCIDENCE  =  20.0
oe.T_REFLECTION  =  20.0
oe.T_SOURCE  =  20.0
oe.T_IMAGE  =  40.0
#spherical mirror
oe.FMIRR  =  1
oe.F_EXT = 0
oe.F_DEFAULT = 1


if flag_write_files: oe.write("start.01")
beam.traceOE(oe,1)
if flag_write_files: oe.write("end.01")
if flag_write_files: beam.write("star.01")

Shadow.ShadowTools.plotxy(beam,1,3)


