

def AUSGAB(IARG):
    pass


# IMPORTS -------
import numpy as np

# EMPTY CALLBACKS ----



# CALLBACKS ---- 


# %C80
# #############################################################################
#                                                                              
#   EGSnrc tutor1 application                                                  
#   Copyright (C) 2015 National Research Council Canada                        
#                                                                              
#   This file is part of EGSnrc.                                               
#                                                                              
#   EGSnrc is free software: you can redistribute it and/or modify it under    
#   the terms of the GNU Affero General Public License as published by the     
#   Free Software Foundation, either version 3 of the License, or (at your     
#   option) any later version.                                                 
#                                                                              
#   EGSnrc is distributed in the hope that it will be useful, but WITHOUT ANY  
#   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS  
#   FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for   
#   more details.                                                              
#                                                                              
#   You should have received a copy of the GNU Affero General Public License   
#   along with EGSnrc. If not, see <http://www.gnu.org/licenses/>.             
#                                                                              
# #############################################################################
#                                                                              
#   Author:          Dave Roger, 1985                                          
#                                                                              
#   Contributors:    Iwan Kawrakow                                             
#                    Frederic Tessier                                          
#                    Reid Townson                                              
#                                                                              
# #############################################################################
#                                                                              
#   An EGSnrc user code. It lists the particles escaping from the back of a    
#   1 mm tantalum plate when a pencil beam of 20 MeV electrons is incident on  
#   it normally.                                                               
#                                                                              
#   The following units are used: unit 6  for (terminal) output, and unit 12   
#   is PEGS cross section file                                                 
#                                                                              
#   Iwan Kawrakow, 2003: Adapted to new EGSnrc MP system by adding call        
#   egs_init at the beginning and call egs_finish at the end.                  
#                                                                              
# #############################################################################


# %L
# %E
# !INDENT M 4 # indent each mortran nesting level by 4
# !INDENT F 2 # indent each fortran nesting level by 2
# --- Inline replace: ; -----
implicit none
# -------------------------------------------
                        # default is IMPLICIT NONE
I: np.int32
IQIN: np.int32
IRIN                  #  defaults to INTEGER*4: np.int32
XIN: np.float64
YIN: np.float64
ZIN: np.float64
EIN: np.float64
WTIN: np.float64
UIN: np.float64
VIN: np.float64
WIN#  defaults to REAL*4: np.float64
# ---------------------------------------------------------------------
# STEP 1:  USER-OVERRIDE-OF-EGSnrc-MACROS                              
# ---------------------------------------------------------------------
REPLACE {MXMED} WITH {1}   # only 1 medium in the problem(default 10)
REPLACE {MXREG} WITH {3}   # only 3 geometric regions (default 2000)
REPLACE {MXSTACK} WITH {15}# less than 15 particles on stack at once

# define a common to pass information to the geometry routine HOWFAR
REPLACE {;COMIN/GEOM/;} WITH {;COMMON/GEOM/ZBOUND;$REAL ZBOUND;}
REPLACE {$CALL_HOWNEAR(#);} WITH {
  ;CALL HOWNEAR({P1},x[np],y[np],z[np],IRL)
}


;COMIN/BOUNDS,GEOM,MEDIA,MISC,THRESH,USEFUL/ # Note  ; before COMIN
#        The above expands into a series of COMMON statements
#        BOUNDS contains ECUT and PCUT
#        GEOM passes info to our HOWFAR routine
#        MEDIA contains the array MEDIA
#        MISC contains MED
#        THRESH contains AE and AP
#        USEFUL contains PRM

# ---------------------------------------------------------------------
# STEP 2 PRE-HATCH-CALL-INITIALIZATION                                 
# ---------------------------------------------------------------------
CHARACTER*4 MEDARR(24)
DATA  MEDARR /$S'TA',22*' '/ # place medium name in an array
#                             $S is a MORTRAN macro to expand strings

# ---------------------------------------------------------------------
#  STEP 0:  Initialize EGSnrc system. Must be the first executable stmt
# ---------------------------------------------------------------------
call egs_init

# STEP 2 cont
DO I=1,24[
   MEDIA(I,1)=MEDARR(I)
]# this is to avoid a DATA STATEMENT for
#                                     a variable in COMMON
# NMED and DUNIT default to 1, i.e. one medium and we work in cm

/MED(1),MED(3)/=0;MED(2)=1 # vacuum in regions 1 and 3, Ta in region 2

# %E  # tutor1.mortran
ECUT(2)=1.5 #    terminate electron histories at 1.5 MeV in the plate
PCUT(2)=0.1 #    terminate   photon histories at 0.1 MeV in the plate
#                only needed for region 2 since no transport elsewhere
#                ECUT is total energy = 0.989   MeV kinetic energy

# ---------------------------------------------------------------------
# STEP 3   HATCH-CALL                                                  
# ---------------------------------------------------------------------

;OUTPUT;('\f  Start tutor1'//' CALL HATCH to get cross-section data'/)
CALL HATCH #     pick up cross section data for TA
#                data file must be assigned to unit 12

;OUTPUT AE(1)-PRM, AP(1)
(/' knock-on electrons can be created and any electron followed down to'
  /T40,F8.3,' MeV kinetic energy'/
' brem photons can be created and any photon followed down to      ',
  /T40,F8.3,' MeV ')
# Compton events can create electrons and photons below these cutoffs

# ---------------------------------------------------------------------
# STEP 4  INITIALIZATION-FOR-HOWFAR and HOWNEAR                        
# ---------------------------------------------------------------------
ZBOUND=0.1 #      plate is 1 mm thick

# ---------------------------------------------------------------------
# STEP 5  INITIALIZATION-FOR-AUSGAB                                    
# ---------------------------------------------------------------------
# Print header for output - which is all AUSGAB does in this case
;OUTPUT;(/T19,'Kinetic Energy(MeV)',T40,'charge',T48,
'angle w.r.t. Z axis-degrees')

# ---------------------------------------------------------------------
# STEP 6   DETERMINATION-OF-INICIDENT-PARTICLE-PARAMETERS              
# ---------------------------------------------------------------------
# Define initial variables for 20 MeV beam of electrons incident
# perpendicular to the slab

IQIN=-1 #                incident charge - electrons
EIN=20.5109989461 #             20 MeV kinetic energy
/XIN,YIN,ZIN/=0.0 #      incident at origin
/UIN,VIN/=0.0;WIN=1.0 #  moving along Z axis
IRIN=2 #                 starts in region 2, could be 1
WTIN=1.0 #               weight = 1 since no variance reduction used
# ---------------------------------------------------------------------
# STEP 7   SHOWER-CALL                                                 
# ---------------------------------------------------------------------
# initiate the shower 10 times
DO I=1,10[
   OUTPUT I;(' Start history',I4)
   CALL SHOWER(IQIN,EIN,XIN,YIN,ZIN,UIN,VIN,WIN,IRIN,WTIN)

# -----------------------------------------------------------------
# STEP 8   OUTPUT-OF-RESULTS                                       
# -----------------------------------------------------------------
# note output is at the end of each history in subroutine ausgab

# -----------------------------------------------------------------
# STEP 9   finish run                                              
# -----------------------------------------------------------------
call egs_finish


STOP;END

# %E  # tutor1.mortran
# ********************************************************************
#                                                                     
def AUSGAB(IARG):
#                                                                     
#   In general, AUSGAB is a routine which is called under a series    
#   of well defined conditions specified by the value of IARG (see the
#   EGSnrc manual for the list). This is a particularily simple AUSGAB
#   Whenever this routine is called with IARG=3 , a particle has      
#   been discarded by the user in HOWFAR                              
#   We get AUSGAB to print the required information at that point     
#                                                                     
# ********************************************************************
# --- Inline replace: ; -----
implicit none
# -------------------------------------------

IARG: np.int32
EKINE: np.float64
ANGLE: np.float64

COMIN/STACK/

if IARG == 3:

ANGLE=ACOS(w[np])*180./3.14159 # angle w.r.t. Z axis in degrees

if iq[np] == 0:

    EKINE=e[np]
else:
    EKINE=e[np]-0.510998946131;# get kinetic energy
OUTPUT EKINE,iq[np],ANGLE;(T21,F10.3,T33,I10,T49,F10.1);]
RETURN;END # END OF AUSGAB

# %E  # tutor1.mortran
# *********************************************************************
#                                                                      
def HOWFAR:
#                                                                      
#  The following is a general specification of HOWFAR                  
#    Given a particle at (X,Y,Z) in region IR and going in direction   
#    (U,V,W), this routine answers the question, can the particle go   
#    a distance USTEP without crossing a boundary?                     
#            If yes, it merely returns                                 
#            If no, it sets USTEP=distance to boundary in the current  
#            direction and sets IRNEW to the region number   on the    
#            far side of the boundary (this can be messy in general!)  
#                                                                      
#    The user can terminate a history by setting IDISC>0. Here we      
#    terminate all histories which enter region 3 or are going         
#    backwards in region 1                                             
#                                                                      
#                    or               or                                 
#    REGION 1        or   REGION 2    or       REGION 3                  
#                    or               or                                 
#    e- =========>   or               or e- or photon ====>              
#                    or               or                                 
#    vacuum          or     Ta        or       vacuum                    
#                                                                      
# *********************************************************************
# --- Inline replace: ; -----
implicit none
# -------------------------------------------

TVAL: np.float64
COMIN/STACK,EPCONT,GEOM/
#        COMMON STACK contains X,Y,Z,U,V,W,IR and NP(stack pointer)
#        COMMON EPCONT contains IRNEW, USTEP and IDISC
#        COMMON GEOM contains ZBOUND

if ir[np] == 3:

   IDISC = 1;RETURN # terminate this history: it is past the plate
else:

   if w[np] > 0.0:

      # going forward - consider first since  most frequent
      TVAL= (ZBOUND - z[np])/w[np] # TVAL is dist to boundary
      #                           in this direction
      if TVAL > USTEP:
          RETURN # can take currently requested step
      else:
          USTEP = TVAL; IRNEW=3; RETURN;
   ]# END OF w[np]>0 CASE

   else:
      TVAL = -z[np]/w[np] # distance to plane at origin
      if TVAL > USTEP:
          RETURN # can take currently requested step
      else:
          USTEP = TVAL; IRNEW = 1; RETURN;
   ]# END w[np]<0 CASE

   else:

       # cannot hit boundaryRETURN;
]# end of region 2 case

else:
   if w[np] >  0.0:
       [# this must be a source particle on z=0 boundary
      USTEP = 0.0;IRNEW = 2;RETURN
   else:
      IDISC=1;RETURN

]# end region 1 case

END # END OF def HOWFAR:

# %E  # tutor1.mortran
# *********************************************************************
#                                                                      
def HOWNEAR(tperp, x, y, z, irl):
#                                                                      
#  The following is a general specification of HOWNEAR                 
#    Given a particle at (x,y,z) in region irl, HOWNEAR answers the    
#    question, What is the distance tperp to the closest boundary?     
#                                                                      
#   In general this can be a complex subroutine.                       
#                                                                      
# *********************************************************************
# --- Inline replace: ; -----
implicit none
# -------------------------------------------

tperp: np.float64
x: np.float64
y: np.float64
z: np.float64
irl: np.int32

;COMIN/GEOM/ #        COMMON GEOM contains ZBOUND

if irl == 3:

    OUTPUT;('Called HOWNEAR in region 3'); RETURN

else:
    tperp = min(z,  (ZBOUND - z))
else:
    OUTPUT;('Called HOWNEAR in region 1'); RETURN;

END # end of subroutine HOWNEAR
# ============================end of tutor1.mortran=================