%C80
"#############################################################################"
"                                                                             "
"  EGSnrc macros                                                              "
"  Copyright (C) 2015 National Research Council Canada                        "
"                                                                             "
"  This file is part of EGSnrc.                                               "
"                                                                             "
"  EGSnrc is free software: you can redistribute it and/or modify it under    "
"  the terms of the GNU Affero General Public License as published by the     "
"  Free Software Foundation, either version 3 of the License, or (at your     "
"  option) any later version.                                                 "
"                                                                             "
"  EGSnrc is distributed in the hope that it will be useful, but WITHOUT ANY  "
"  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS  "
"  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for   "
"  more details.                                                              "
"                                                                             "
"  You should have received a copy of the GNU Affero General Public License   "
"  along with EGSnrc. If not, see <http://www.gnu.org/licenses/>.             "
"                                                                             "
"#############################################################################"
"                                                                             "
"  Authors:         Iwan Kawrakow, 2000                                       "
"                   Dave Rogers, 2000                                         "
"                                                                             "
"  Contributors:    Blake Walters                                             "
"                   Ernesto Mainegra-Hing                                     "
"                   Frederic Tessier                                          "
"                   Reid Townson                                              "
"                   Victor Malkov                                             "
"                                                                             "
"#############################################################################"
"                                                                             "
"  Parts of the EGS code that originate from SLAC are distributed by NRC      "
"  under the terms of the AGPL 3.0 licence, in agreement with SLAC.           "
"                                                                             "
"  The contributors named above are only those who could be identified from   "
"  this file's revision history.                                              "
"                                                                             "
"  A large number of people have been involved with the development of EGS    "
"  over the years. Many details are in the manual. The authors want to point  "
"  out the central role of Ralph Nelson of SLAC in the development of EGS     "
"  over decades. We all owe Ralph a huge debt of gratitude.  Similarly, the   "
"  role of Alex Bielajew while he was at NRC was critical in many aspects of  "
"  code development. Hideo Hirayama was involved with the development of EGS4 "
"  while at SLAC and with Yosh Namito and Syuichi Ban at KEK has continued    "
"  developments on EGS4. As well many others and users from around the world  "
"  have assisted in developing and making available the code, in particular   "
"  Robert D. Stewart.                                                         "
"                                                                             "
"#############################################################################"


"Compiler directives"
"==================="
%Q1         "Automatically close comments at end of line
            "but this DOES NOT apply withing macro definitions!!
%C80        "Allow 80 columns of source/line (default is 72)
%L          "Turn on listing


"=================================================================="
" Macros to implement implicit data types                          "
"=================================================================="

REPLACE {$LOGICAL} WITH {;logical}
REPLACE {$REAL}    WITH {;real*8}
REPLACE {$INTEGER} WITH {;integer*4}
REPLACE {$LONG_INT} WITH {;integer*8} "change this to integer*4 for compilers"
                                      "that do not support integer*8"
REPLACE {$SHORT_INT} WITH {;integer*2} "change this to integer*4 for compilers"
                                      "that do not support integer*2"
"the above is not used in EGSnrc but is used in the NRC user codes,
"especially related to number of histories"
"Note that the HP compiler does not support *8 integers so the above"
" should be changed for HP"

REPLACE {$IMPLICIT-NONE;} WITH {;}
REPLACE {$IMPLICIT-NONE;} WITH {implicit none;}

"=================================================================="
"SELECT THE FORTRAN STANDARD TO BE USED (1966 OR 1977)             "
REPLACE {$FORTVER} WITH {1977}
"=================================================================="

"******************************************************************"
REPLACE {$TYPE} WITH {
  {SETR F=$FORTVER}
   [IF] {COPY F}=1977 [CHARACTER*4] [ELSE] [INTEGER*4]
  }
"******************************************************************"

"******************************************************************"
SPECIFY ALPHA    AS (0...$);
SPECIFY SYMBOL   AS (0...?);
SPECIFY NAME     AS LETTER(0,5)[ALPHA];
SPECIFY <COMMA>  AS [','|''];
SPECIFY <NAME>   AS [NAME|''];
SPECIFY LABEL    AS ':'NAME':';
SPECIFY <LABEL>  AS [LABEL|''];
SPECIFY <*>      AS ['*'|''];
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {NEWLABEL} WITH {@LG}
REPLACE {%'{ARB}'={<*>}'{ARB}'}
   WITH {[IF] '{P2}'='*' [APPEND'{P3}'TO'{P1}']
            [ELSE] [ REPLACE {{P1}}WITH{{P3}}]}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

    "RULES TO GENERALIZE MORTRAN'S INPUT AND OUTPUT"
REPLACE {;$UINPUT(#)#;}
   WITH {;{SETR A=NEWLABEL}
            READ({P1},{COPY A}){P2};{COPY A}FORMAT}

REPLACE {;$UOUTPUT(#)#;}
   WITH {;{SETR A=NEWLABEL}
            WRITE({P1},{COPY A}){P2};{COPY A}FORMAT}

REPLACE {;$ECHO#({NAME}{<COMMA>}#)#;}
 WITH {;{SETR X=NEWLABEL}
 WRITE(IUECHO,{COPY X});{COPY X}FORMAT(' ECHO {P1}:{P5}');
 [IF] {EXIST 3} [{P1}({P2},{P4}){P5};
 WRITE(IUECHO,{P4}){P5};]
 [ELSE] [{SETR Y=NEWLABEL}{P1}({P2},{COPY Y}){P4};
 WRITE(IUECHO,{COPY Y}){P5};{COPY Y}FORMAT]
 }
;  "---------- BUFFER FLUSH SEMICOLON ----------"
REPLACE {;IUECHO=#;} WITH { REPLACE {IUECHO} WITH {{P1}};}
"INITALIZE" ;IUECHO=6;

"MACRO TO SPLIT STRING INTO A LIST SEPARATED BY COMMAS"
REPLACE {$S'{SYMBOL}#'}
  WITH {'{P1}'[IF]{EXIST 2}[,$S'{P2}']}

"SOME DEBUGGING MACROS"
REPLACE {$LIST#/#/#;} WITH
   {;OUTPUT {P3};('LIST/{P2}/{P3}:'/(1X,{P1}));}
APPEND{;COMMON/QDEBUG/QDEBUG;LOGICAL QDEBUG;} TO {;COMIN/DEBUG/;}

REPLACE {$TRACE#;} WITH
  {REPLACE {;{P1}={WAIT {ARB}};}  WITH
  {{EMIT;{P1}}={WAIT {P1}};
  IF QDEBUG [OUTPUT{P1};
  (' {P1} ASSIGNED {WAIT {P1}} ',G25.18);] }; }
REPLACE {$S1TRACE#;} WITH
  {{SETR A=NEWLABEL}
    REPLACE {;{P1}({WAIT {ARB}})={WAIT {ARB}};}
       WITH {{EMIT ;{P1}({WAIT {P1}})}={WAIT {P2}};
           IF QDEBUG [I{COPY A}={WAIT {P1}};
                OUTPUT I{COPY A},{P1}(I{COPY A});
                    (' {P1}(',I6,') ASSIGNED {WAIT {P2}} ' ,
                       G25.18);] } ;}

REPLACE {$TRACE#,#;} WITH {$TRACE{P1};$TRACE{P2};}
REPLACE {$S1TRACE#,#;} WITH {$S1TRACE{P1};$S1TRACE{P2};}

SPECIFY DELIM AS ['('|';'];
REPLACE {$CALLTRACE;} WITH
  {REPLACE {;CALL{NAME}{DELIM}} WITH
  {;IF (QDEBUG)[OUTPUT;
    (' SUBROUTINE {WAIT {P1}} CALLED.');]
         {WAIT {EMIT CALL} {P1}{P2}} };}

REPLACE {$DUMP#,#;} WITH
    {;{SETR A=NEWLABEL}
         V{COPY A}={P1};OUTPUT V{COPY A};(' {P1}=',1PG15.7);
         [IF] {EXIST 2} [$DUMP{P2};] ;}
   "NOTICE: THE LIST OF VARIABLES MUST BE FOLLOWED BY A COMMA"
   "FOR EXAMPLE $DUMP S,T(U,V),W,; OR $DUMP A,;"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MORTRAN MACRO DEFINITIONS FOR EGS."

"FIRST SOME PARAMETERS"
REPLACE {PARAMETER #=#;} WITH
   { REPLACE {{P1}} WITH {{P2}}}

MXMED: int = 10  # MAX. NO. OF DIFFERENT MEDIA (EXCL. VAC.)
MXREG: int = 2000  # MAXIMUM NO. OF REGIONS ALLOCATED
MXSTACK: int = 40  # STACK SIZE
MXVRT1: int = 1000  # NO. OF REPRESENTATIVE ANGLES IN VERT1
FMXVRT1: float = 1000.  # FLOATING $MXVRT1
MXPWR2I: int = 50  # SIZE OF TABLE OF INVERSE POWERS OF TWO
MXJREFF: int = 200  # SIZE OF MULTIPLE SCATTERING JREFF MAP
MSSTEPS: int = 16  # NO. OF MULTIPLE SCATTERING STEP SIZES
MXVRT2: int = 100  # DISTRBTN OF NONOVERLAPPING PARTS OF VERT

;
"FOLLOWING DEFINE MAX. NO. OF INTERVALS FOR FIT TO FUNCTIONS"
MXSGE: int = 400  # GAMMA SMALL ENERGY INTERVALS
MXGE: int = 2000  # GAMMA MAPPED ENERGY INTERVALS
MXSEKE: int = 300  # ELECTRON SMALL ENERGY INTERVALS
MXEKE: int = 500  # ELECTRON MAPPED ENERGY INTERVALS
MXEL: int = 50  # MAXIMUM # OF ELEMENTS IN A MEDIUM
MXLEKE: int = 100  # ELECTRON ENERGY INTERVALS BELOW EKELIM
MXCMFP: int = 100  # CUMULATIVE ELECTRON MEAN-FREE-PATH
MXRANGE: int = 100  # ELECTRON RANGE
MXBLC: int = 20  # MOLIERE'S LOWER CASE B
MXRNTH: int = 20  # RANDOM NUMBER FOR SUBMEDIAN ANGLES
MXRNTHI: int = 20  # RANDOM NUMBER FOR SUPERMEDIAN ANGLES
MXRAYFF: int = 100  # RAYLEIGH ATOMIC FORM FACTOR
RAYCDFSIZE: int = 100  # CDF from RAYLEIGH FORM FACTOR SQUARED
MXSINC: int = 1002  # ANGLE INTERVALS IN (0,5*PI/2) FOR SINE
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"THE FOLLOWING ARE PARAMETERS FOR AUSGAB CALLS:"
MXAUS: int = 35  # CHANGE IF MORE AUSGAB CALLS ARE ADDED
MXAUSM5: int = 30  # SET THIS TO $MXAUS VALUE LESS 5

"FIRST FIVE AUSGAB CALLS BELOW TURNED ON IN BLOCK DATA (DEFAULT)"
TRANAUSB: int = 0  # BEFORE TRANSPORT
EGSCUTAUS: int = 1  # ENERGY BELOW ECUT OR PCUT
PEGSCUTAUS: int = 2  # ENERGY BELOW AE OR AP
USERDAUS: int = 3  # USER REQUESTED DISCARD
PHOTXAUS: int = 4  # FLUORESCENT PHOTON DISCARD

"THE REMAINING 23 ARE TURNED OFF IN BLOCK DATA (DEFAULT)"
TRANAUSA: int = 5  # AFTER TRANSPORT
BREMAUSB: int = 6  # BEFORE BREMS CALL
BREMAUSA: int = 7  # AFTER BREMS CALL
MOLLAUSB: int = 8  # BEFORE MOLLER CALL
MOLLAUSA: int = 9  # AFTER MOLLER CALL
BHABAUSB: int = 10  # BEFORE BHABHA CALL
BHABAUSA: int = 11  # AFTER BHABHA CALL
ANNIHFAUSB: int = 12  # BEFORE ANNIH CALL
ANNIHFAUSA: int = 13  # AFTER ANNIH CALL
ANNIHRAUSB: int = 28  # BEFORE POSITRON ANNIH AT REST
ANNIHRAUSA: int = 14  # POSITRON ANNIHILATED AT REST
PAIRAUSB: int = 15  # BEFORE PAIR CALL
PAIRAUSA: int = 16  # AFTER PAIR CALL
COMPAUSB: int = 17  # BEFORE COMPT CALL
COMPAUSA: int = 18  # AFTER COMPT CALL
PHOTOAUSB: int = 19  # BEFORE PHOTO CALL
PHOTOAUSA: int = 20  # AFTER PHOTO CALL
UPHIAUSB: int = 21  # ENTERED UPHI
UPHIAUSA: int = 22  # LEFT UPHI
RAYLAUSB: int = 23  # BEFORE RAYLEIGH EVENT
RAYLAUSA: int = 24  # AFTER RAYLEIGH EVENT
FLUORTRA: int = 25  # A fluorescent transition just occurred
COSKROTRA: int = 26  # A Coster-Kronig transition just occurred
AUGERTRA: int = 27  # An Auger transition just occurred
"Ali:photonuc, 2 lines"
" note that 28 is already used for positron annih at rest - see above"
PHOTONUCAUSB: int = 29  # BEFORE PHOTONUCLEAR EVENT
PHOTONUCAUSA: int = 30  # AFTER PHOTONUCLEAR EVENT
EIIB: int = 31  # Before EII
EIIA: int = 32  # After EII
SPHOTONA: int = 33  # After sub-threshold photon energy deposition
SELECTRONA: int = 34  # After sub-threshold electron energy deposition

;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {$AUSCALL(#);} WITH
   {IARG={P1} ;  IF (IAUSFL(IARG+1).NE.0) [CALL AUSGAB(IARG);]} ;
;  "---------- BUFFER FLUSH SEMICOLON ----------"
"TEMPORARY OVER-RIDES FOR SOME OF THE ABOVE"
MXSGE: int = 1
MXSEKE: int = 1
MXLEKE: int = 1
MXCMFP: int = 1
MXRANGE: int = 1
MXBLC: int = 1
MXRNTH: int = 1
MXRNTHI: int = 1
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"THE FOLLOWING DEFINE PRECISION USED IN ENERGY COMPUTATIONS"
"THE LATTER OF THE TWO WILL BE IN EFFECT"
REPLACE {$ENERGYPRECISION} WITH {;REAL }"SINGLE PRECISION"
REPLACE {$ENERGYPRECISION} WITH {;DOUBLE PRECISION }
REPLACE {$MAX_INT} WITH {2147483647} "2^31-1"
"^--- limits number of particles and hence phase space file size"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MACROS TO MAKE CHANGES IN THE DEGREE OF FIT EASIER"
"ALSO USEFUL FOR ABBREVIATING LISTS OF SUBSCRIPTED VARIABLES"
"$LGN STANDS FOR 'LIST GENERATOR'"
"$RSC MEANS THAT THE EXPANDED LIST SHOULD RESCANNED FOR FURTHER"
"OPERATIONS.  MACROS EXPECTING TO DO RESCANS SHOULD BE"
"DEFINED AFTER THE FOLLOWING MACRO"
REPLACE {$RSC(#)} WITH {{P1}}
"IF NOT MATCHED BY ANYTHING ELSE, REMOVE $RSC()"
REPLACE {$RSC(#),#$LSCALEBY#;} WITH
   {{P1}={P1}*{P3};{P2}$LSCALEBY{P3};}
REPLACE {$RSC(#)$LSCALEBY#;} WITH {{P1}={P1}*{P2};}
REPLACE {$LGN(#/#/)} WITH {$RSC({P1}{P2})}
REPLACE {$LGN(#(#)/#/)} WITH {$RSC({P1}{P3}({P2}))}
REPLACE {$LGN(#(#))} WITH {$RSC({P1}({P2}))}
REPLACE {$LGN(#/#,#/)} WITH
    {$LGN({P1}/{P2}/),$LGN({P1}/{P3}/)}
REPLACE {$LGN(#,#/#/)} WITH
    {$LGN({P1}/{P3}/),$LGN({P2}/{P3}/)}
REPLACE {$LGN(#(#)/#,#/)} WITH
    {$LGN({P1}({P2})/{P3}/),$LGN({P1}({P2})/{P4}/)}
REPLACE {$LGN(#,#(#)#)} WITH
    {$LGN({P1}({P3}){P4}),$LGN({P2}({P3}){P4})}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MACROS FOR SCALING REQUIRED BY CHANGE IN DISTANCE UNIT"
REPLACE {$SCALE# BY #;} WITH {{P1}={P1}*{P2};}
REPLACE {$SCALE#,# BY #;} WITH
    {{P1}={P1}*{P3};$SCALE{P2} BY {P3};}
REPLACE {$SCALE$LGN(#) BY #;} WITH
    {$LGN({P1})$LSCALE BY {P2};}
REPLACE {$SCALE$LGN(#),# BY #;} WITH
            {$LGN({P1})$LSCALE BY {P3};$SCALE{P2} BY {P3};}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"------------------------------------------------------------------
" Macros related to bit setting
"------------------------------------------------------------------
""
"Macro to set bit {P2} in {P1}  to 1
REPLACE {$IBSET(#,#);} WITH {ibset({P1},{P2});}

"Macro to set test bit {P2} in {P1}
"Note this may require a LOGICAL declaration wherever used
REPLACE {$BTEST(#,#)} WITH {btest({P1}, {P2})}

"Macro to set bit {P2} in {P1}  to 0
REPLACE {$IBCLR(#,#);} WITH {ibclr({P1},{P2});}
"Above used by RW_PH_SP routine - (read_write_phase_space for BEAM)


"COMMON BLOCK INSERTION MACROS"
REPLACE {;COMIN/#,#/;} WITH {;COMIN/{P1}/;COMIN/{P2}/;}

"NOW FOR SOME SPECIFIC COMMON BLOCKS"

"------------------------------------------------------------------"
"*** BOUNDS--CUTOFF ENERGIES & VACUUM TRANSPORT DISTANCE           "
"------------------------------------------------------------------"
REPLACE {;COMIN/BOUNDS/;} WITH
{
    ;COMMON/BOUNDS/ECUT($MXREG),PCUT($MXREG),VACDST;
     $REAL         ECUT,   "Minimum electron transport energy"
                   PCUT,   "Minimum photon transport energy"
                   VACDST; "Infinity (1E8)"
}

"------------------------------------------------------------------"
"*** BREMPR--BREMSSTRAHLUNG AND PAIR PRODUCTION DATA               "
"------------------------------------------------------------------"

;
REPLACE {$MXBREN} WITH {57}
REPLACE {$MXBRXX} WITH {54}
REPLACE {$MXBREL} WITH {100}
REPLACE {$MXGAUSS} WITH {64}
REPLACE {$MXBRES} WITH {100}
REPLACE {$MXBRXS} WITH {50}
REPLACE {$NIST-ENERGY-SCALE} WITH {1.0}

REPLACE {$NIST-DATA-UNIT} WITH {i_nist_data}
;

REPLACE {$COMIN-INIT-NIST-BREMS;} WITH {;
    ;COMIN/MEDIA,BREMPR,ELECIN,THRESH,USEFUL,NIST-BREMS,Spin-Data,EGS-IO/;
};

REPLACE {;COMIN/BREMPR/;} WITH
{
  ;COMMON/BREMPR/
             $LGN(DL(8,$MXMED)/1,2,3,4,5,6/),
             $LGN(ALPHI,BPAR,DELPOS(2,$MXMED)),
             $LGN(WA,PZ,ZELEM,RHOZ($MXMED,$MXEL)),
             PWR2I($MXPWR2I),
             $LGN(DELCM,ZBRANG,LZBRANG,NNE($MXMED)),
             IBRDST,IPRDST,ibr_nist,pair_nrc,itriplet,
             ASYM($MXMED,$MXEL,2);
   $TYPE     ASYM;
   $REAL     $LGN(DL/1,2,3,4,5,6/), "Parameter for the fit of the screening"
                                    "rejection function, eq. (2.7.14 and 15)"
             ALPHI,  "Prob. for the (1-BR)/BR part in BREMS, eq. (2.7.64)"
             BPAR,   "Prob. for the 12*(BR-1/2)**2 part in PAIR, eq. (2.7.105)"
             DELPOS, "maximum delta, eq. (2.7.31)"
             WA,     "atomic weight"
             PZ,     "atomic fraction of an element in a compound"
             ZELEM,  "Z for a given component"
             RHOZ,   "density of an element in a compound"
             PWR2I,  "powers of 1/2 (used for sampling (1-BR)/BR"
             DELCM,  "136*m*exp(Zg), eq. (2.7.51)"
             ZBRANG, "composite factor for angular distributions"
             LZBRANG;"-Log(ZBRANG)"
   $INTEGER  NNE,    "number of elements/compound"
             IBRDST, "flag to switch on bremsstrahlung angular distributions"
             IPRDST, "flag to switch on pair angular distributions"
             ibr_nist,  "use the NIST bremsstrahlung cross sections"
             itriplet,  "if set to 1, explicitely simulate triplet events"
             pair_nrc;  "=0 => use Bethe-Heitler pair cross sections"
                        "=1 => use the NRC pair cross sections"
};

REPLACE {;COMIN/NIST-BREMS/;} WITH {;

  common/nist_brems/ nb_fdata(0:$MXBRXS,$MXBRES,$MXMED),
                     nb_xdata(0:$MXBRXS,$MXBRES,$MXMED),
                     nb_wdata($MXBRXS,$MXBRES,$MXMED),
                     nb_idata($MXBRXS,$MXBRES,$MXMED),
                     nb_emin($MXMED),nb_emax($MXMED),
                     nb_lemin($MXMED),nb_lemax($MXMED),
                     nb_dle($MXMED),nb_dlei($MXMED),
                     log_ap($MXMED);
  $REAL    nb_fdata,nb_xdata,nb_wdata,nb_emin,nb_emax,nb_lemin,nb_lemax,
           nb_dle,nb_dlei,log_ap;
  $INTEGER nb_idata;
};

REPLACE {$NRC-PAIR-NXX} WITH {65};
REPLACE {$NRC-PAIR-NEE} WITH {84};
REPLACE {$NRC-PAIR-NX-1} WITH {64};
REPLACE {$NRC-PAIR-NE-1} WITH {83};

REPLACE {;COMIN/NRC-PAIR-DATA/;} WITH {;
    common/nrc_pair/ nrcp_fdata($NRC-PAIR-NXX,$NRC-PAIR-NEE,$MXMED),
                     nrcp_wdata($NRC-PAIR-NXX,$NRC-PAIR-NEE,$MXMED),
                     nrcp_idata($NRC-PAIR-NXX,$NRC-PAIR-NEE,$MXMED),
                     nrcp_xdata($NRC-PAIR-NXX),
                     nrcp_emin, nrcp_emax, nrcp_dle, nrcp_dlei;
    $REAL            nrcp_fdata,nrcp_wdata,nrcp_xdata,
                     nrcp_emin, nrcp_emax, nrcp_dle, nrcp_dlei;
    $INTEGER         nrcp_idata;
};

"------------------------------------------------------------------------"
"*** TRIPLET DATA                                                        "
"------------------------------------------------------------------------"
REPLACE {$MAX_TRIPLET} WITH {250}
REPLACE {;COMIN/TRIPLET-DATA/;} WITH {;
        common/triplet_data/ a_triplet($MAX_TRIPLET,$MXMED),
                             b_triplet($MAX_TRIPLET,$MXMED),
                             dl_triplet, dli_triplet, bli_triplet, log_4rm;
        $REAL                a_triplet,b_triplet,dl_triplet, dli_triplet,
                             bli_triplet, log_4rm;
};

"------------------------------------------------------------------------"
"*** COMPTON-DATA -- Incoherent scattering data                          "
"------------------------------------------------------------------------"
REPLACE {$MXTOTSH}   WITH {1538} "Total number of shells for Z=1..100    "
REPLACE {$MXMDSH}    WITH {200}   "Max. number of shells per medium       "
REPLACE {$INCOHUNIT} WITH {i_incoh}   "Unit number for compton data           "

REPLACE {;COMIN/COMPTON-DATA/;} WITH
{
  ;common/compton_data/ iz_array($MXTOTSH), "Atomic number for each shell"
                        be_array($MXTOTSH), "Shell binding energies      "
                        Jo_array($MXTOTSH), "Compton profile parameter   "
                        erfJo_array($MXTOTSH),"needed for the calculation"
                                            "of the incoherent scattering"
                                            "function                    "
                        ne_array($MXTOTSH), "Occupation number           "
                        shn_array($MXTOTSH),"shell type                  "
                                            "(=1     for K,              "
                                            " =2,3,4 for L1,L2,L3        "
                                            " =5     for M               "
                                            " =6     for N               "
                                            " =7     for all others      "
                        shell_array($MXMDSH,$MXMED),
                        eno_array($MXMDSH,$MXMED),
                        eno_atbin_array($MXMDSH,$MXMED),
                        n_shell($MXMED),
                        radc_flag,          "flag for radiative corrections"
                        ibcmp($MXREG);      "flag to turn on binding effects"
   $INTEGER             iz_array,ne_array,shn_array,eno_atbin_array,
                        shell_array,n_shell,radc_flag;
   $REAL                be_array,Jo_array,erfJo_array,eno_array;
   $SHORT_INT           ibcmp;
}


"------------------------------------------------------------------ "
"*** EDGE -- Containes binding energies for K,L1,L2,L3,             "
"             'average' M and 'average' N shells; photo-absorption  "
"             interaction probabilities with these shells;          "
"             + fluorescence, Auger, Coster-Kronig transition       "
"             probabilities                                         "
"             IEDGFL is a flag for turning on/off atomic relaxations"
"             IPHTER is a flag for turning on/off photo-lectron     "
"                    angular distribution                           "
"             both are left-overs from the previous coding          "
"             Have put now also data to calculate elemental PE      "
"             cross sections needed to sample the element the photon"
"             is interacting with.
"------------------------------------------------------------------ "
REPLACE {$MXELEMENT} WITH {100}  " Number of elements               "
REPLACE {$MXSHXSEC}  WITH {30}   " Number of shells available       "
REPLACE {$MXSHELL}   WITH {6}    " Number of shells treated         "
REPLACE {$MXINTER}   WITH {5}    " $MXSHELL-1                       "
REPLACE {$MXTRANS}   WITH {39}   " Number of possible transitions   "
REPLACE {$MXEDGE}    WITH {16}   " max. number of edges above 1 keV "
REPLACE {$PHOTOUNIT} WITH {i_photo_relax} " unit number for photo_relax.data "
REPLACE {$PHOCSUNIT} WITH {i_photo_cs}   " unit number for photo_cs.data    "

REPLACE {;COMIN/EDGE/;} WITH
{;
   COMMON/EDGE/binding_energies($MXSHXSEC,$MXELEMENT),
               interaction_prob($MXSHELL,$MXELEMENT),
               relaxation_prob($MXTRANS,$MXELEMENT),
               edge_energies($MXEDGE,$MXELEMENT),
               edge_number($MXELEMENT),
               edge_a($MXEDGE,$MXELEMENT),
               edge_b($MXEDGE,$MXELEMENT),
               edge_c($MXEDGE,$MXELEMENT),
               edge_d($MXEDGE,$MXELEMENT),
               IEDGFL($MXREG),IPHTER($MXREG);
   $REAL       binding_energies, " K,L1,L2,L3,M,N binding energies  "
               interaction_prob, " prob. for interaction with one of"
                                 " the above shells (provided photon"
                                 " energy is above be)              "
               relaxation_prob,  " relaxation probabilities         "
               edge_energies,    " photo-absorption edge energies   "
               edge_a,edge_b,edge_c,edge_d;
                                 " photo cross section fit parameters "
   $SHORT_INT  IEDGFL,  "flag for switching on fluorscent emission"
               IPHTER;  "flag for switching on photo-electron angular distr."
   $INTEGER    edge_number; " number of `edges' for each element"
}

"------------------------------------------------------------------"
"*** ELECIN--ELECTRON TRANSPORT INPUT                              "
"        MODIFIED 1989/12/19 TO INCLUDE IUNRST,EPSTFL AND IAPRIM   "
"        NRC DWOR                                                  "
"------------------------------------------------------------------"
REPLACE {;COMIN/ELECIN/;} WITH
{;
   COMMON/ELECIN/
   esig_e($MXMED),psig_e($MXMED),
   esige_max, psige_max,
   range_ep(0:1,$MXEKE,$MXMED),
   E_array($MXEKE,$MXMED),
   $LGN(etae_ms,etap_ms,q1ce_ms,q1cp_ms,q2ce_ms,q2cp_ms,
        blcce($MXEKE,$MXMED)/0,1/),
   $LGN(EKE($MXMED)/0,1/),
   $LGN(XR0,TEFF0,BLCC,XCC($MXMED)),
   $LGN(ESIG,PSIG,EDEDX,PDEDX,EBR1,PBR1,PBR2,TMXS($MXEKE,$MXMED)/0,1/),
   expeke1($MXMED),
   IUNRST($MXMED),EPSTFL($MXMED),IAPRIM($MXMED),
   sig_ismonotone(0:1,$MXMED);
   $REAL    esig_e,        "maximum electron cross section per energy loss"
                           "for each medium"
            psig_e,        "maximum positron cross section per energy loss"
                           "for each medium"
            esige_max,     "maximum electron cross section per energy loss"
            psige_max,     "maximum electron cross section per energy loss"
            range_ep,      "electron (0) or positron (1) range"
            E_array,       "table energies"
            etae_ms0,etae_ms1,
                           "for interpolation of screening parameter (e-)"
            etap_ms0,etap_ms1,
                           "for interpolation of screening parameter (e+)"
            q1ce_ms0,q1ce_ms1,
                          "for interpolation of q1 correction due to spin (e-)"
            q1cp_ms0,q1cp_ms1,
                          "for interpolation of q1 correction due to spin (e+)"
            q2ce_ms0,q2ce_ms1,
                          "for interpolation of q2 correction due to spin (e-)"
            q2cp_ms0,q2cp_ms1,
                          "for interpolation of q2 correction due to spin (e+)"
            blcce0,blcce1,"for interpolation of scattering power correction   "
                          "necessary to account for scattering already taken  "
                          "into account in discrete Moller/Bhabha             "
            expeke1,       "Exp(1/eke1)-1"
            $LGN(EKE/0,1/),"table for kinetic energy indexing"
            XR0,           "unused, but read in HATCH"
            TEFF0,         "unused, but read in HATCH"
            BLCC,          "b lower case sub c"
            XCC,           "chi sub-c-c"
            ESIG0,ESIG1,   "used for electron cross section interpolation"
            PSIG0,PSIG1,   "used for positron cross section interpolation"
            EDEDX0,EDEDX1, "used for electron dE/dx interpolation"
            PDEDX0,PDEDX1, "used for positron dE/dx interpolation"
            EBR10,EBR11,   "used for e- branching into brems interpolation"
            PBR10,PBR11,   "used for e+ branching into brems interpolation"
            PBR20,PBR21,   "used for e+ branching into Bhabha interpolation"
            TMXS0,TMXS1;   "used for maximum step-size interpolation"
   $INTEGER IUNRST,        "flag for type of stopping power (see PEGS4)"
            EPSTFL,        "flag for ICRU37 collision stopping powers"
            IAPRIM;        "flag for ICRU37 radiative stopping powers"
   $LOGICAL sig_ismonotone;"true, if cross section is an increasing function"
                           "of energy, false otherwise"
}

"***************************************************************************"
"                                                                           "
" ------------ common block for EII data -----------------                  "
"
" Added by Iwan Kawrakow, March 20 2004.
"                                                                           "
"****************************************************************************

REPLACE {$MAX_EII_SHELLS} WITH {40};  "Maximum number of shells participating"
                                      "in EII in a simulation                "
REPLACE {$N_EII_BINS} WITH {250};     "Number of bins for EII x-section      "
                                      "interpolations                        "
REPLACE {$MAX_EII_BINS} WITH {{COMPUTE $N_EII_BINS*$MAX_EII_SHELLS}};
"We store the EII x-section interpolation coefficients in 1D arrays  "
"The above is the dimension of these arrays required to hold the data"
REPLACE {;COMIN/EII-DATA/;} WITH {;
    common/eii_data/
        eii_xsection_a($MAX_EII_BINS), "EII x-section interpolation coeff."
        eii_xsection_b($MAX_EII_BINS), "EII x-section interpolation coeff."
        eii_cons($MXMED),
        eii_a($MAX_EII_SHELLS),        "energy grid coeff. for each shell "
        eii_b($MAX_EII_SHELLS),        "energy grid coeff. for each shell "
        eii_L_factor,                  "L-shell EII xsection scaling factor"
        eii_z($MAX_EII_SHELLS),        "Z of each shell                   "
        eii_sh($MAX_EII_SHELLS),       "shell type (1=K, 2=LI, eyc.)      "
        eii_nshells($MXELEMENT),       "No. of EII shells for each element"
        eii_nsh($MXMED),               "No. of EII shells for each medium "
        eii_first($MXMED,$MXEL),       "First EII shell in the list of shells"
        eii_no($MXMED,$MXEL),          "N. of EII shells                  "
        eii_flag;                      "EII flag                          "
                                       "         = 0 => no EII            "
                                       "         = 1 => simple EII        "
                                       "         > 1 => future use        "
    $REAL     eii_xsection_a,eii_xsection_b,eii_a,eii_b,eii_cons,eii_L_factor;
    $INTEGER  eii_z,eii_sh,eii_nshells;
    $INTEGER  eii_first,eii_no;
    $INTEGER  eii_elements,eii_flag,eii_nsh;
};

REPLACE {$COMIN-EII-SAMPLE;} WITH {
    ;COMIN/EPCONT,EII-DATA,EGS-VARIANCE-REDUCTION,RANDOM,STACK,THRESH,
           UPHIOT,USEFUL,EGS-IO,RELAX-DATA/;
};
REPLACE {$COMIN-EII-INIT;} WITH {
    ;COMIN/BREMPR,EDGE,EGS-IO,EII-DATA,ELECIN,MEDIA,THRESH,USEFUL/;
};

REPLACE {;COMIN/EMF-INPUTS/;} WITH {;
    common/emf_inputs/ExIN,EyIN,EzIN, "E field"
                     EMLMTIN,         "Ekin, u, E fractional maximum change"
                     BxIN, ByIN, BzIN,       "B field: initial region"
                     Bx, By, Bz,             "B field: current region"
                     Bx_new, By_new, Bz_new, "B field: in new region"
                     emfield_on;             "true if EM fields not null"

   $REAL    ExIN,EyIN,EzIN,
            EMLMTIN,
            BxIN,ByIN,BzIN,
            Bx,By,Bz,
            Bx_new,By_new,Bz_new;
   $LOGICAL emfield_on;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"
" The following common block is made available to the user so that  "
" he/she knows which shell was being relaxed when the call to ausgab"
" occured                                                           "
" Added by Iwan Kawrakow, March 22 2004.                            "

REPLACE {;COMIN/RELAX-USER/;} WITH {;
   common/user_relax/ u_relax,ish_relax,iZ_relax;
   $REAL              u_relax;
   $INTEGER           ish_relax, iZ_relax;
};


;  "---------- BUFFER FLUSH SEMICOLON ----------"
"***************************************************************************"
"                                                                           "
" ------------ common blocks for EADL relaxation data -----------------     "
"
" Added by Ernesto Mainegra, June 1st 2011.                                 "
"                                                                           "
"***************************************************************************"
"shell in one long list, avoiding repetition (i.e. if an element is present"
"in different materials, its shell structure and information will be stored"
"only once in the list). The array shell_eadl(Z,i) tells us the position of"
"the i'th shell of element Z in the long shell list.                       "
"***************************************************************************"

REPLACE {$MXESHLL} WITH {30}     "max. number of shells for an element"
REPLACE {$MAXSHELL} WITH {3000}  "max. number of shells"
REPLACE {$MAXRELAX} WITH {10000} "max. number of relaxations channels"
REPLACE {$MAXVAC} WITH {100}     "max. number of vacancies"
REPLACE {$MAXTRANS} WITH {300}   "max. number of transitions per element"
"============================================================"
" Set input key 'Atomic relaxations' to 'simple' to recover original
" implementation which allows photoelectric interactions with <M> and
" <N> shells. See below for details on the shells considered by different
" interactions depending on the value of eadl_relax:
"
"      Interaction        .false.             .true.
"      -----------------------------------------
"      Compton                all available shells
"      EII                K,L1..L3            K,L1..L3
"      Photoeffect        K,L1..L3,<M>,<N>    K,L1..L3
"      Shellwise
"      Photoeffect             N/A      All shells > $RELAX-CUTOFF
"      Relaxation
"        initial vacancy  K,L1..L3,<M>        K,L1..L3
"        (for new photoeffect)                K, L1..L3, M1..M5, N1..N4
"        final vacancy    L1..L3,<M>,<N>      L1..L3,M1..M5,N1..N7...
"
"============================================================"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {;COMIN/SHELL-DATA/;} WITH {;

  common/shell_data/
    shell_be($MAXSHELL),      "binding energies"
    shell_type($MAXSHELL),    "shell type according to EADL notation"
    shell_num($MAXSHELL),     "the shell position in the element"
    shell_Z($MAXSHELL),       "Z of the element the shell belongs to"
    shell_eadl($MXELEMENT,$MXESHLL), "global index for a shell of element Z"
    shell_ntot;               "total number of shells in the list"
  $REAL    shell_be;
  $INTEGER shell_type,shell_Z,shell_ntot,shell_num,shell_eadl;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {;COMIN/RELAX-DATA/;} WITH {;

  common/relax_data/
    relax_first($MAXSHELL),    "first transition"
    relax_ntran($MAXSHELL),    "number of transitions"
    relax_state($MAXRELAX),    "final state of the transition"
    relax_prob($MAXRELAX),     "probability"
    relax_atbin($MAXRELAX),    "used for alias sampling"
    relax_ntot;                "total number of transitions in the list"
  $REAL     relax_prob;
  $INTEGER  relax_first, relax_ntran, relax_state, relax_atbin, relax_ntot;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {;COMIN/RELAX-FOR-USER/;} WITH {;
    common/relax_for_user/
     rfu_E0, "binding energy of vacancy that initiated cascade"
     rfu_E,  "binding energy of current vacancy"
     rfu_Z,  "Atomic number of the element the relaxing shell belongs to"
     rfu_j0, "shell numb. of vacancy that initiated cascade in the list"
     rfu_n0, "same but number is shell number in the element"
     rfu_t0, "same but number is shell type according to EADL notation"
     rfu_j,  "shell number of current vacancy"
     rfu_n,  "same but number is shell number in the element"
     rfu_t;  "same but number is shell type according to EADL notation"
    $INTEGER rfu_Z,rfu_j0,rfu_n0,rfu_t0,rfu_j,rfu_n,rfu_t;
    $REAL    rfu_E0,rfu_E;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {$COMIN-RELAX-INIT;} WITH {
;COMIN/BREMPR,EDGE,EGS-IO,MEDIA,PHOTIN,THRESH,X-OPTIONS,USEFUL,
RELAX-DATA,SHELL-DATA/;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {$COMIN-RELAX-EADL;} WITH {
;COMIN/RELAX-DATA,RELAX-FOR-USER,SHELL-DATA,
STACK,THRESH,EPCONT,USEFUL,UPHIOT,RANDOM,BOUNDS,EGS-IO,MISC,MEDIA,
X-OPTIONS/;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"***************************************************************************"
"                                                                           "
" -------------- shell-wise photoelectric cross section data ------------   "
"
" Cross sections taken from Sabbatucci and Salvat,                          "
" Theory and calculation of the atomic photoeffect                          "
" Radiat. Phys. and Chem., Volume 121, April 2016, Pages 122-140            "
"                                                                           "
"***************************************************************************"
" Shell-wise photoelectric cross sections from 50 eV up to 1 GeV for elements
" from Z=1 up to Z=99. All K, L, M, and N shells are included. One can define
" a threshold energy separating inner from outer shells. By default this
" energy is set to 1 keV, but for accurate calculation of quantities that  "
" require knowledge of which particle deposited the energy, one might need to
" use the a lower threshold.
"***************************************************************************"
"============================================================"
REPLACE {$RELAX-CUTOFF} WITH {0.001"threshold energy for outer shells"}
REPLACE {$MXPESHELL} WITH {16} "K,L1..L3,M1..M5,N1..N7 + outer shell"
REPLACE {$MXNE} WITH {500}     "number of energy points per shell "
"============================================================"
REPLACE {;COMIN/PE-SHELL-DATA/;} WITH {;

  common/pe_shell_data/
    pe_xsection($MXNE,$MXELEMENT,0:$MXPESHELL),  "shellwise cross sections"
    pe_elem_prob($MXNE,$MXELEMENT,$MXMED), "prob. of interaction with an"
                                           "element of a medium"
    pe_energy($MXNE,$MXELEMENT),    "energy grid"
    pe_zsorted($MXELEMENT,$MXMED),"sorted array of Z for each medium"
    pe_be($MXELEMENT,$MXPESHELL),      "binding energies"
    pe_nshell($MXELEMENT),       "number of shells for each element"
    pe_zpos($MXELEMENT),       "position of each Z element"
    pe_nge($MXELEMENT),       "number of energy points for each element"
    pe_ne;                    "number of elements in the simulation"
  $REAL    pe_be, pe_energy, pe_xsection, pe_elem_prob;
  $INTEGER pe_zsorted, pe_nshell, pe_zpos, pe_nge, pe_ne;
};
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {$COMIN-SHELLWISE-PE-INIT;} WITH {
;COMIN/BREMPR,EDGE,EGS-IO,MEDIA,PHOTIN,THRESH,X-OPTIONS,USEFUL,
    PE-SHELL-DATA/;
};


;  "---------- BUFFER FLUSH SEMICOLON ----------"
" Some macros for C-style syntax in mortran "
" Unfortunately, /= doesn't work because of /v1,v2,...,vn/=value;"

REPLACE {;#+=#;} WITH { ;{P1} = {P1} + {P2}; }
REPLACE {[#+=#;} WITH { {P1} = {P1} + {P2}; }

REPLACE {;#-=#;} WITH { ;{P1} = {P1} - {P2}; }
REPLACE {[#-=#;} WITH { {P1} = {P1} - {P2}; }

REPLACE {;#*=#;} WITH { ;{P1} = {P1}*{P2}; }
REPLACE {[#*=#;} WITH { {P1} = {P1}*{P2}; }

;  "---------- BUFFER FLUSH SEMICOLON ----------"
"***************************************************************************"

REPLACE {;COMIN/ET-Control/;} WITH  "ET stands for Electron Transport"
{
  ;common/ET_control/
              smaxir($MXREG),estepe,ximax,
              "ximin_for_bca,"
              skindepth_for_bca,transport_algorithm,
              bca_algorithm,exact_bca,spin_effects;
    $REAL     smaxir,             "geom. step-size constrain for each region"
              estepe,             "global energy loss constrain"
              ximax,              "max. first GS moment per step"
                                  "(roughly half the average MS angle squared"
              "ximin_for_bca,"
                                  "min. first GS moment per step for boundary"
                                  "crossing in VMC mode"
              skindepth_for_bca;  "distance from a boundary (in elastic MFP)"
                                  "to switch to one of the BCAs "
    $INTEGER  transport_algorithm,"=$PRESTA-II or $PRESTA--I"
              bca_algorithm;      "will be used if other inexact BCAs"
                                  "implemented in the future"
    $LOGICAL  exact_bca,          "if .true. => BCA in single scattering mode"
              spin_effects;       "if .true. electron/positron spin effects"
                                  "are taken into account in the single and"
                                  "multiple elasting scattering routines"
}
;

" ======================== multiple scattering commons ================= "

" Screened Rutherford MS data "

REPLACE {$MAXL_MS}    WITH {63}
REPLACE {$MAXQ_MS}    WITH {7}
REPLACE {$MAXU_MS}    WITH {31}
REPLACE {$0-MAXL_MS}  WITH {0:63}
REPLACE {$0-MAXQ_MS}  WITH {0:7}
REPLACE {$0-MAXU_MS}  WITH {0:31}
REPLACE {$LAMBMIN_MS} WITH {1.}
REPLACE {$LAMBMAX_MS} WITH {1e5}
REPLACE {$QMIN_MS}    WITH {1e-3}
REPLACE {$QMAX_MS}    WITH {0.5}

REPLACE {COMIN/MS-Data/;} WITH {
  common/ms_data/
              ums_array($0-MAXL_MS,$0-MAXQ_MS,$0-MAXU_MS),
              fms_array($0-MAXL_MS,$0-MAXQ_MS,$0-MAXU_MS),
              wms_array($0-MAXL_MS,$0-MAXQ_MS,$0-MAXU_MS),
              ims_array($0-MAXL_MS,$0-MAXQ_MS,$0-MAXU_MS),
              llammin,llammax,dllamb,dllambi,dqms,dqmsi;
  real*4      ums_array,fms_array,wms_array,
              llammin,llammax,dllamb,dllambi,dqms,dqmsi;
  $SHORT_INT  ims_array;
}
;

" spin effect data used in an additional rejection loop "

REPLACE {$MAXE_SPIN}   WITH {15}
REPLACE {$MAXE_SPI1}   WITH {{COMPUTE 2*$MAXE_SPIN+1}}
REPLACE {$MAXQ_SPIN}   WITH {15}
REPLACE {$MAXU_SPIN}   WITH {31}
REPLACE {$0-MAXE_SPI1} WITH {0:$MAXE_SPI1}
REPLACE {$0-MAXQ_SPIN} WITH {0:$MAXQ_SPIN}
REPLACE {$0-MAXU_SPIN} WITH {0:$MAXU_SPIN}

REPLACE {COMIN/Spin-Data/;} WITH {
  common/spin_data/
              spin_rej($MXMED,0:1,$0-MAXE_SPI1,$0-MAXQ_SPIN,$0-MAXU_SPIN),
              espin_min,espin_max,espml,b2spin_min,b2spin_max,
              dbeta2,dbeta2i,dlener,dleneri,dqq1,dqq1i,
              fool_intel_optimizer;
  real*4      spin_rej,espin_min,espin_max,espml,b2spin_min,b2spin_max,
              dbeta2,dbeta2i,dlener,dleneri,dqq1,dqq1i;
  $LOGICAL    fool_intel_optimizer;
}
;

REPLACE {COMIN/CH-Steps/;} WITH
{
  common/CH_steps/ count_pII_steps,count_all_steps,is_ch_step;
  real*8           count_pII_steps,count_all_steps;
  $LOGICAL         is_ch_step;
}
;
"------------------------------------------------------------------"
"*** EPCONT--ELECTRON-PHOTON CONTROL VARIABLES                     "
"------------------------------------------------------------------"
REPLACE {;COMIN/EPCONT/;} WITH
{;
  COMMON/EPCONT/EDEP,EDEP_LOCAL,TSTEP,TUSTEP,USTEP,TVSTEP,VSTEP,
                RHOF,EOLD,ENEW,EKE,ELKE,GLE,E_RANGE,
                x_final,y_final,z_final,
                u_final,v_final,w_final,
                IDISC,IROLD,IRNEW,IAUSFL($MXAUS);
    $ENERGY PRECISION EDEP,   "energy deposition in MeV"
                      EDEP_LOCAL; "local energy deposition in MeV"
    $REAL             TSTEP,  "distance to a discrete interaction"
                      TUSTEP, "intended step length, befor check with geometry"
                      USTEP,  "transport distance calculated from TUSTEP"
                      VSTEP,  "transport distance after truncation by HOWFAR"
                      TVSTEP, "curved path-length calculated from TVSTEP"
                      RHOF,   "mass density ratio"
                      EOLD,   "energy before deduction of energy loss"
                      ENEW,   "energy after  deduction of energy loss"
                      EKE,    "kinetic energy"
                      ELKE,   "Log(EKE)"
                      GLE,    "Log(energy) in PHOTON"
                      E_RANGE,"range of electron before an iarg=0 ausgab call"
                      x_final,y_final,z_final, "position at end of step"
                      u_final,v_final,w_final; "direction at end of step"
                                               "only set (and relevant) "
                                               "for electrons"
    $INTEGER          IDISC,  "flag indicating user discard"
                      IROLD,  "region before transport"
                      IRNEW,  "region after transport"
                      IAUSFL; "flags for AUSGAB calls"
}

"------------------------------------------------------------------"
"*** MEDIA--NAMES OF MEDIA CURRENTLY BEING USED                    "
"------------------------------------------------------------------"
REPLACE {;COMIN/MEDIA/;} WITH
{;
   COMMON/MEDIA/
"Ali:photonuc, 4 lines (order matters because of padding issues)"
       $LGN(RLC,RLDU,RHO,MSGE,MGE,MSEKE,MEKE,MLEKE,MCMFP,MRANGE,
            IRAYLM,IPHOTONUCM($MXMED)),
            MEDIA(24,$MXMED), photon_xsections, comp_xsections,
            photonuc_xsections,eii_xfile,IPHOTONUC,NMED;
   $TYPE    MEDIA;"media names"
   $REAL    RLC,  "radiation length in centimeters for a given medium"
            RLDU, "radiation length after user scaling over-ride"
            RHO,  "mass density of a given medium"
            apx, upx;"new photon xsection data thresholds"
   $INTEGER MSGE, "??? "
            MGE,  "number of photon mapped energy intervals for a given medium"
            MSEKE,"??? "
            MEKE, "number of e mapped energy intervals for a given medium"
            MLEKE,"??? "
            MCMFP,"??? "
            MRANGE,"??? "
            IRAYLM,"Rayleigh switch for a given medium"
"Ali:photonuc, 2 lines"
            IPHOTONUCM,"photonuclear switch for a given medium"
            IPHOTONUC,"set to 1 if any IPHOTONUCM is set to 1"
            NMED;  "number of media"
   character*16 eii_xfile;
            "Defaults to eii_ik.data if On or Off options selected"
            "which is the EII implemented by Iwan for EGSnrc"
            "else, following options available: "
            "  eii_'casnati'.data    "
            "  eii_'kolbenstvedt'.data "
            "  eii_'gryzinski'.data"
            "these must be in $HEN_HOUSE/data"
   character*16 photon_xsections;
            "If photon_xsections is not empty, photon cross sections will be"
            "re-initialized using data files  "
            "  'photon_xsection'_photo.data   "
            "  'photon_xsection'_pair.data    "
            "  'photon_xsection'_triplet.data "
            "  'photon_xsection'_rayleigh.data"
            "that must be placed in $HEN_HOUSE/data"
   character*16 comp_xsections;
            "If comp_xsections is not empty or not set to 'default' and"
            "bound Compton scattering is On, then total Compton cross sections"
            "will be taken from 'comp_xsections'_compton.data"
            "instead of being computed from the theoretical expressions"
"Ali:photonuc, 5 lines"
   character*16 photonuc_xsections;
            "If photonuc_xsections is not empty or not set to 'default',"
            "the photonuclear cross sections will be taken from"
            "'photonuc_xsections'_photonuc.data instead of using the data"
            "in the default file iaea_photonuc.data."
}

"------------------------------------------------------------------"
"*** MISC--MISCELLANEOUS COMMON                                    "
"------------------------------------------------------------------"
REPLACE {;COMIN/MISC/;} WITH
{;
  COMMON/MISC/
"Ali:photonuc, 1 line"
           DUNIT,KMPI,KMPO,$LGN(RHOR,MED,IRAYLR,IPHOTONUCR($MXREG));
  $REAL    DUNIT,   "unit scaling factor"
           RHOR;    "density of a given region"
  $INTEGER KMPI,    "fortran unit number of the pegs4 datafile"
           KMPO;    "fortran unit number of pegs4 echo file"
  $SHORT_INT MED,   "medium number for a given region"
             IRAYLR,"Rayleigh switch for a given region"
"Ali:photonuc, 1 line"
             IPHOTONUCR;"photonuclear switch for a given region"
}
;

"------------------------------------------------------------------"
"*** PHOTIN--PHOTON TRANSPORT DATA                                 "
"------------------------------------------------------------------"
REPLACE {;COMIN/PHOTIN/;} WITH
{;
    COMMON/PHOTIN/
       EBINDA($MXMED),
       $LGN(GE($MXMED)/0,1/),
       $LGN(GMFP,GBR1,GBR2($MXGE,$MXMED)/0,1/),
       $LGN(RCO($MXMED)/0,1/),
       $LGN(RSCT($MXRAYFF,$MXMED)/0,1/),
       $LGN(COHE($MXGE,$MXMED)/0,1/),
"Ali:photonuc, 1 line"
       $LGN(PHOTONUC($MXGE,$MXMED)/0,1/),
       DPMFP,
       MPGEM($MXSGE,$MXMED),
       NGR($MXMED);
    $REAL
       EBINDA,      "energy of the K-edge for a given medium"
       GE0,GE1,     "used for indexing in logarithmic interpolations"
       GMFP0,GMFP1, "used for gamma MFP interpolation"
       GBR10,GBR11, "used for branching into pair interpolation"
       GBR20,GBR21, "used for branching into Compton interpolation"
       RCO0,RCO1,   "used for indexing in momentum trans. sampling in Rayleigh"
       RSCT0,RSCT1, "used for interpolation of momentum trans. func. in R"
       COHE0,COHE1, "used for Rayleigh modification interpolation"
"Ali:photonuc, 1 line"
       PHOTONUC0,PHOTONUC1, "used for photonuclear modification interpolation"
       DPMFP;       "number of MFP's to go to the next interaction"
    $INTEGER
       MPGEM,       "??? "
       NGR;         "array size for Rayleigh scattering data"
}
;

"------------------------------------------------------------------"
"*** RANDOM - DECLARATIONS FOR RANDOM NUMBER GENERATOR             "
"------------------------------------------------------------------"

" Note that the definition of the COMIN/RANDOM/ was taken out of   "
" the egsnrc.macros file. The current philosophy is that the user  "
" has to provide a random number generator in a separate file.     "
" Two commonly used RNGs are provided in separate files:           "
"  RANLUX: ranlux.macros and ranlux.mortran                        "
"  RANMAR: ranmar.macros and ranmar.mortran                        "


"------------------------------------------------------------------"
"*** STACK--INFORMATION KEPT ABOUT CURRENT PARTICLES               "
"------------------------------------------------------------------"
REPLACE {;COMIN/STACK/;} WITH
{;
   COMMON/STACK/
       $LGN(E,X,Y,Z,U,V,W,DNEAR,WT,IQ,IR,LATCH($MXSTACK)),
       LATCHI,NP,NPold;
   $ENERGY PRECISION
       E;     "total particle energy"
   $REAL
       X,Y,Z, "particle co-ordinates"
       U,V,W, "particle direction cosines"
       DNEAR, "perpendicular distance to nearest boundary"
       WT;    "particle weight"
   $INTEGER
       IQ,    "charge, -1 for electrons, 0 for photons, 1 for positrons"
       IR,    "current region"
       LATCH, "extra phase space variable"
       LATCHI,"needed because shower does not pass latch-BLOCK DATA sets 0"
       NP,    "stack pointer"
       NPold; "stack pointer before an interaction"
}

"------------------------------------------------------------------"
"*** THRESH--THRESHOLD (AND OTHER) ENERGIES                        "
"------------------------------------------------------------------"
REPLACE {;COMIN/THRESH/;} WITH
{;
   COMMON/THRESH/RMT2,RMSQ,
                 $LGN(AP,AE,UP,UE,TE,THMOLL($MXMED));
   $REAL         RMT2,  "2*electron mass in MeV"
                 RMSQ,  "electron mass squared in MeV**2"
                 AP,    "photon creation threshold energy"
                 AE,    "electron creation threshold energy (total)"
                 UP,    "upper photon energy in PEGS4 data set"
                 UE,    "upper electron energy in PEGS4 data set"
                 TE,    "electron creation threshold energy (kinetic)"
                 THMOLL;"Moller threshold = AE + TE"
}

"------------------------------------------------------------------"
"*** UPHIIN--SINE TABLES FOR UPHI                                  "
"------------------------------------------------------------------"
REPLACE {;COMIN/UPHIIN/;} WITH
{;
   COMMON/UPHIIN/SINC0,SINC1,$LGN(SIN($MXSINC)/0,1/);
   $REAL         SINC0,SINC1,SIN0,SIN1;
}

"------------------------------------------------------------------"
"*** UPHIOT--UPHI'S INPUT/OUTPUT WITH ITS USERS                    "
"------------------------------------------------------------------"
REPLACE {;COMIN/UPHIOT/;} WITH
{;
   COMMON/UPHIOT/THETA,SINTHE,COSTHE,SINPHI,
                 COSPHI,PI,TWOPI,PI5D2;
   $REAL         THETA,  "polar scattering angle"
                 SINTHE, "sin(THETA)"
                 COSTHE, "cos(THETA)"
                 SINPHI, "sine of the azimuthal scattering angle"
                 COSPHI, "cosine of the azimuthal scattering angle"
                 PI,TWOPI,PI5D2;
}

"------------------------------------------------------------------"
"*** USEFUL--HEAVILY USED VARIABLES                                "
"------------------------------------------------------------------"
REPLACE {;COMIN/USEFUL/;} WITH
{;
   COMMON/USEFUL/PZERO,PRM,PRMT2,RM,MEDIUM,MEDOLD;
   $ENERGY PRECISION PZERO,   "precise zero"
                     PRM,     "precise electron mass in MeV"
                     PRMT2;   "2*PRM"
   $REAL             RM;      "electron mass in MeV"
   $INTEGER          MEDIUM,  "medium index of current region"
                     MEDOLD;  "medium index of previous region"
   " The rest mass value is as recommended by CODATA 2014"
   " http://physics.nist.gov/cgi-bin/cuu/Value?mec2mev"
   DATA RM,PRM,PRMT2,PZERO/0.5109989461,0.5109989461,1.0219978922,0.D0/;
}

"------------------------------------------------------------------"
"*** USER--A COMMON FOR THE 'USER' TO 'USE'                        "
"------------------------------------------------------------------"
REPLACE {;COMIN/USER/;} WITH {
         ;}  "DEFAULT IS NULL"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {;COMIN/X-OPTIONS/;} WITH {
    ;
  common/x_options/eadl_relax,       "Use EADL relaxation"
                   mcdf_pe_xsections;"Use Sabbatucci and Salvat PE xsections"
  $LOGICAL  eadl_relax, mcdf_pe_xsections;
};

"------------------------------------------------------------------"
"*** MACROS TO DEFINE THE COMMONS USED IN EACH SUBPROGRAM.         "
"------------------------------------------------------------------"
REPLACE {$COMIN-ANNIH;} WITH {
     ;COMIN/DEBUG,STACK, UPHIOT,USEFUL,RANDOM,EGS-VARIANCE-REDUCTION,EGS-IO/;}
REPLACE {$COMIN-ANNIH-ATREST;} WITH {
    ;COMIN/DEBUG,STACK,RANDOM,USEFUL,EGS-VARIANCE-REDUCTION,EGS-IO/;}
REPLACE {$COMIN-BHABHA;} WITH {
    ;COMIN/DEBUG,STACK, THRESH,UPHIOT,USEFUL,RANDOM,EGS-VARIANCE-REDUCTION,
           EGS-IO/;}
REPLACE {$COMIN-BREMS;} WITH {
    ;COMIN/DEBUG,BREMPR,EPCONT,NIST-BREMS,STACK,THRESH,UPHIOT,USEFUL,RANDOM,
           EGS-VARIANCE-REDUCTION,EGS-IO/;}
REPLACE {$COMIN-COMPT;} WITH {
   ;COMIN/COMPTON-DATA,DEBUG,EPCONT,STACK,THRESH,UPHIOT,USEFUL,RANDOM,
          EGS-VARIANCE-REDUCTION,EGS-IO,RELAX-DATA/;}
REPLACE {$COMIN-ELECTR;} WITH {
;COMIN/DEBUG,BOUNDS,ELECIN,EPCONT,MEDIA,MISC,STACK,THRESH,
UPHIIN,UPHIOT,USEFUL,USER,RANDOM,ET-Control,CH-Steps,EGS-IO,
          EGS-VARIANCE-REDUCTION,EMF-INPUTS/;}
REPLACE {$COMIN-HATCH;} WITH {
;COMIN/DEBUG,BOUNDS,BREMPR,ELECIN,MEDIA,MISC,PHOTIN,STACK,THRESH,
UPHIIN,UPHIOT,USEFUL,USER,RANDOM,ET-Control,EGS-IO,X-OPTIONS,
          EGS-VARIANCE-REDUCTION/;}
REPLACE {$COMIN-MOLLER;} WITH {
   ;COMIN/DEBUG,STACK,THRESH,UPHIOT,USEFUL,RANDOM,EGS-IO,
          EGS-VARIANCE-REDUCTION/;}
REPLACE {$COMIN-PAIR;} WITH {
   ;COMIN/DEBUG,BREMPR,NRC-PAIR-DATA,STACK,THRESH,UPHIOT,USEFUL,RANDOM,
          EPCONT,TRIPLET-DATA,EGS-VARIANCE-REDUCTION,EGS-IO/;}
REPLACE {$COMIN-PHOTO;} WITH {
   ;COMIN/BOUNDS,BREMPR,DEBUG,EDGE,EPCONT,MEDIA,PHOTIN,RANDOM,
          STACK,UPHIOT,USEFUL,EGS-IO,X-OPTIONS,
          EGS-VARIANCE-REDUCTION,RELAX-DATA/;}
REPLACE {$COMIN-PHOTON;} WITH {
;COMIN/DEBUG,BOUNDS,MEDIA,MISC,EPCONT,PHOTIN,STACK,THRESH,UPHIOT,
USEFUL,USER,RANDOM,EGS-VARIANCE-REDUCTION,EGS-IO/;}
REPLACE {$COMIN-SHOWER;} WITH {
  ;COMIN/DEBUG,STACK,UPHIOT,RANDOM,EGS-IO/;}
REPLACE {$COMIN-UPHI;} WITH {
  ;COMIN/DEBUG,EPCONT,STACK,UPHIIN,UPHIOT,RANDOM,EGS-IO/;}
REPLACE {$COMIN-BLOCK;} WITH {
  ;COMIN/BOUNDS,BREMPR,COMPTON-DATA,EDGE,ELECIN,
  EPCONT,CH-Steps,ET-Control,MEDIA,MISC,PHOTIN,RANDOM,STACK,
  THRESH, UPHIIN,UPHIOT,USEFUL,EGS-VARIANCE-REDUCTION/;}
REPLACE {$COMIN-RELAX;} WITH {
  ;COMIN/EPCONT,STACK,BOUNDS,USEFUL,RANDOM,EDGE,EGS-IO,RELAX-DATA,X-OPTIONS/;}
REPLACE {$COMIN-SET-DEFAULTS;} WITH {
  ;COMIN/BOUNDS,BREMPR,COMPTON-DATA,EDGE,ELECIN,EPCONT,CH-Steps,ET-Control,
       MEDIA,MISC,PHOTIN,RANDOM,STACK,THRESH, UPHIIN,UPHIOT,USEFUL,
       EGS-VARIANCE-REDUCTION,EGS-IO,Spin-Data,EII-DATA,rayleigh_inputs,
       EMF-INPUTS,X-OPTIONS/;};
REPLACE {$COMIN-INIT-COMPT;} WITH {
  ;COMIN/COMPTON-DATA,BREMPR,EDGE,MEDIA,MISC,USEFUL,EGS-IO,X-OPTIONS/;};
REPLACE {$COMIN-MSCATI;} WITH {
  ;COMIN/BOUNDS,ELECIN,MEDIA,MISC,RANDOM,ET-Control,USEFUL,EGS-IO/;};
REPLACE {$COMIN-INIT-TRIPLET;} WITH {
  ;COMIN/BREMPR,EGS-IO,MEDIA,TRIPLET-DATA,USEFUL/;};
REPLACE {$COMIN-GET-TRANSPORTP;} WITH {
  ;COMIN/GetInput,BOUNDS,ET-Control,EDGE,COMPTON-DATA,MEDIA,MISC,
         BREMPR,EII-DATA,EGS-IO,rayleigh_inputs,EMF-INPUTS,X-OPTIONS/;};
"Ali:photonuc, 1 block"
REPLACE {$COMIN-PHOTONUC;} WITH {;COMIN/STACK,EPCONT,USEFUL/;};

;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {ILOG2(#)} WITH {
    IFIX(1.44269*LOG({P1}))} "1.44269=1/LN(2)"

REPLACE {$SETINTERVAL#,#;} WITH {
    [IF] '{P2}'=SNAME  [L{P1}={P2}1*{P1}+{P2}0;]
    [ELSE]  [L{P1}={P2}1(MEDIUM)*{P1}+{P2}0(MEDIUM);]}
"TWO ARGUMENT SET INTERVAL CALL (ABOVE) CURRENTLY MEANS"
"INTERVAL INDEX IS LINEAR FUNCTION OF THE LINEAR VARIABLE,"
"WITH NO MAPPING.  {P1} IS THE LINEAR VARIABLE AND {P2} IS"
"THE NAME OF THE INTERVAL(WHICH IS USED TO CONSTRUCT THE"
"COEFFICIENTS USED IN COMPUTING THE INTERVAL INDEX)."
"BUT, IF {P2} IS SINC OR BLC OR RTHR OR RTHRI, IT DOES"
"NOT DEPEND ON MEDIUM"

REPLACE {$EVALUATE#USING#(#);} WITH {
  [IF] '{P2}'=SNAME1
  [{P1}={P2}1(L{P3})*{P3}+{P2}0(L{P3});] [ELSE]
  [{P1}={P2}1(L{P3},MEDIUM)*{P3}+{P2}0(L{P3},MEDIUM);]}
"{P1} IS VARIABLE TO BE ASSIGNED VALUE."
"{P2} IS THE FUNCTION BEING APPROXIMATED."
"{P3} IS THE ARGUMENT OF THE FUNCTION. IN THE CURRENT"
"PWLF METHOD, THE ARGUMENT DETERMINES AN INTERVAL USING THE"
"$SET INTERVAL MACROS.   WITH IN THIS INTERVAL THE"
"FUNCTION IS APPROXIMATED AS A LINEAR FUNCTION OF"
"THE ARGUMENT. BUT"
"IF {P2}=SIN IT DOES NOT DEPEND ON MEDIUM"

REPLACE {$EVALUATE#USING#(#,#);} WITH {
  {P1}={P2}0(L{P3},L{P4})+{P2}1(L{P3},L{P4})*{P3}+
  {P2}2(L{P3},L{P4})*
  {P4};}"2-D APPROXIMATION INDEPENDENT OF MEDIUM"
SPECIFY SNAME AS ['sinc'|'blc'|'rthr'|'rthri'|'SINC'|'BLC'|'RTHR'|'RTHRI'];
SPECIFY SNAME1 AS ['sin'|'SIN'];

"The following circumvent the above table look up method for sin"
"functions.  Modern machines do sines very quickly so the large saving"
"in time from the above no longer exists for sines (was 40% on some"
"machines for the overall computing time! (for example it makes a
"20% effect on an SGI R4400)"
"To recover the use of tables, just comment out the following two"
"macros"

REPLACE {$EVALUATE#USING SIN(#);} WITH {{P1}=sin({P2});}
REPLACE {$SET INTERVAL#,SINC;} WITH {;}


"MACRO TO ALLOW USER TO ADD TO PROPERTIES THAT ARE"
"PASSED TO NEW PARTICLES"
REPLACE {$TRANSFERPROPERTIESTO#FROM#;} WITH {
    X{P1}=X{P2};Y{P1}=Y{P2};Z{P1}=Z{P2};IR{P1}=IR{P2};
    WT{P1}=WT{P2};DNEAR{P1}=DNEAR{P2};LATCH{P1}=LATCH{P2};}
   "IN THE USAGE OF THE ABOVE MACRO, '(IP)' WILL REFER TO THE"
   "PARTICLE WHOSE STACK INDEX IS 'IP'. 'NP' IS THE TOP OF THE STACK."
   "JUST PLAIN 'I' WILL REFER TO THE INITIAL VALUES SUPPLIED"
   "AS ARGUMENTS TO SHOWER, OR SUPPLIED IN COMMON BLOCKS OR"
   "DATA STATEMENTS IN SHOWER."

"Macro to check that the stack size is not exceeded"
REPLACE {$CHECK-STACK(#,#);} WITH {;
  IF( {P1} > $MXSTACK ) [
;  "---------- BUFFER FLUSH SEMICOLON ----------"
      $egs_fatal('(//,3a,/,2(a,i9),/,a)',' In subroutine ',{P2},
          ' stack size exceeded! ',' $MXSTACK = ',$MXSTACK,' np = ',{P1},
          ' Increase $MXSTACK and try again ');
  ]
};

/*
   Redefined to be able to use huge stack in C++ application after
   implementing new relaxation.
 */
REPLACE {$CHECK-STACK(#,#);} WITH {;
  IF( {P1} > $MXSTACK ) [
      $egs_fatal('(//,3a,/,2(a,i9))',' In subroutine ',{P2},
          ' stack size exceeded! ',' $MAXSTACK = ',$MXSTACK,' np = ',{P1});
  ]
};

"MACRO FOR RE-EVALUATING DEDX IN SUBROUTINE ELECTR"
REPLACE {$DEDX-RE-EVALUATION;} WITH {
;}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"THE FOLLOWING MACROS ARE USED IN SUBROUTINE ELECTR IN ORDER TO MAKE"
"PATH LENGTH CORRECTIONS AND RESTRICTIONS:"
REPLACE {$SET-USTEP;} WITH
{
  ekems = eke - 0.5*tustep*dedx; "Use mid-point energy to calculate"
                                  "energy dependent quantities"
  $CALCULATE-XI(tustep);
  IF ( xi < 0.1 )
    [
      ustep = tustep*(1 - xi*(0.5 - xi*0.166667));
    ]
    ELSE
    [
      ustep = tustep*(1 - Exp(-xi))/xi;
    ]
}
;

REPLACE {$CALCULATE-XI(#);} WITH
{
  p2 = ekems*(ekems+rmt2); beta2 = p2/(p2 + rmsq);
  chia2 = xccl/(4*blccl*p2);
                                "Note that our chia2 is Moliere chia2/4"
                                "Note also that xcc is now old egs xcc**2"
  xi = 0.5*xccl/p2/beta2*{P1};
  IF( spin_effects ) [
      elkems = Log(ekems);
      $SET INTERVAL elkems,eke;
      IF(lelec < 0) [
          $EVALUATE etap USING etae_ms(elkems);
          $EVALUATE xi_corr USING q1ce_ms(elkems);
      ]
      ELSE          [
          $EVALUATE etap USING etap_ms(elkems);
          $EVALUATE xi_corr USING q1cp_ms(elkems);
      ]
      chia2 = chia2*etap; xi = xi*xi_corr;
      $EVALUATE ms_corr USING blcce(elkems);
      blccl = blccl*ms_corr;
  ]
  ELSE [ xi_corr = 1; etap = 1; ]
  xi = xi*(Log(1+1./chia2)-1/(1+chia2));
}

REPLACE {$SET-TVSTEP;} WITH
"        ===========                 "
{
    ;IF ( vstep < ustep0 )
    [
      ekems = eke - 0.5*tustep*vstep/ustep0*dedx;
         "This estimates the energy loss to the boundary."
         "tustep was the intended curved path-length,"
         "ustep0 is the average transport distance in the initial direction"
         "       resulting from tustep"
         "vstep = ustep is the reduced average transport distance in the "
         "              initial direction due to boundary crossing"
      $CALCULATE-XI(vstep);
      IF ( xi < 0.1 )
      [
        tvstep = vstep*(1 + xi*(0.5 + xi*0.333333));
      ]
      ELSE
      [

        IF ( xi < 0.999999 )
        [
           tvstep = -vstep*Log(1 - xi)/xi;
        ]
        ELSE
        [
           "This is an error condition because the average transition "
           "in the initial direction of motion is always smaller than 1/Q1"
           $egs_info(*,' Stoped in SET-TVSTEP because xi > 1! ');
           $egs_info(*,' Medium: ',medium);
           $egs_info(*,' Initial energy: ',eke);
           $egs_info(*,' Average step energy: ',ekems);
           $egs_info(*,' tustep: ',tustep);
           $egs_info(*,' ustep0: ',ustep0);
           $egs_info(*,' vstep:  ',vstep);
           $egs_info(*,' ==> xi = ',xi);
           $egs_fatal(*,'This is a fatal error condition');
        ]
      ]
    ]
    ELSE
    [
      tvstep = tustep;
    ]
}
;

REPLACE {$ENEPS} WITH {0.0001}
            "DIFFERENCE BETWEEN ECUT AND END POINT ENERGY FOR"
            "RANGE CALCULATION"

REPLACE {$EPSEMFP} WITH {1.E-8}  "SMALLEST ELECTRON MFP VALUE"
REPLACE {$EPSGMFP} WITH {1.E-8}  "SMALLEST GAMMA MFP VALUE"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"THE FOLLOWING ARE UTILITY AND OTHER MACROS FOR THE USER"

"ETALY1---COMMON BLOCK FOR ENERGY CONSERVATION PURPOSES"
REPLACE {;COMIN/ETALY1/;} WITH {
    ;COMMON/ETALY1/ESUM(4,$MXREG,5);
    $ENERGY PRECISION ESUM;}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"NTALY1---COMMON BLOCK FOR KEEPING COUNT OF ETALY1-EVENTS"
REPLACE {;COMIN/NTALY1/;} WITH {
   ;COMMON/NTALY1/NSUM(4,$MXREG,5);
   $INTEGER NSUM;
}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MACRO TO ALLOW USER TO INITIALIZE IN SUBROUTINE HATCH"
REPLACE {$HATCH-USER-INPUT-INIT;} WITH {;
" $RNG-INITIALIZATION; "
" Have taken this out, (IK, Jan 2000). If the user does not initilize the"
" rng before the first call to shower, the rng will initialize itself    "
" using the default seed and the default luxury level (which is defined  "
" via $DEFAULT-LL).                                                      "

DO J=1,$MXREG [
  IF(SMAXIR(J)<=0.0) [SMAXIR(J)=1E10;]
]
;}

REPLACE {$KERMA-INSERT;} WITH {;}
            "USED IN KERMA CALCULATIONS---DEFAULT IS NULL"
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MACRO FOR CONTROLLING NEGATIVE USTEP"
REPLACE {$USER-CONTROLS-NEGATIVE-USTEP;} WITH {
"         ============================"
   ;IF(USTEP<-1.E-4)[ IERUST=IERUST+1;OUTPUT IERUST,USTEP,IR(NP),IRNEW,
   IROLD,X(NP),Y(NP),Z(NP),SQRT(X(NP)**2+Y(NP)**2);
   (I6,' NEGATIVE USTEP=',E14.6,' IR,IRNEW,IROLD=',3I4,' X,Y,Z,R=',
   4E14.6);
   IF(IERUST>10)[OUTPUT;(///'0STOP, TOO MANY USTEP ERRORS'///); STOP;]]
   USTEP=0.0;}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

REPLACE {$CHECK-NEGATIVE-USTEP;} WITH {;
    IF(ustep <= 0) [
        "Negative ustep---probable truncation problem at a"
        "boundary, which means we are not in the region we think"
        "we are in.  The default macro assumes that user has set"
        "irnew to the region we are really most likely to be"
        "in.  A message is written out whenever ustep is less than -1.e-4"
        IF(ustep < -1e-4) [
            ierust = ierust + 1;
            OUTPUT ierust,ustep,dedx,e(np)-prm,
                   ir(np),irnew,irold,x(np),y(np),z(np);
            (i4,' Negative ustep = ',e12.5,' dedx=',F8.4,' ke=',F8.4,
             ' ir,irnew,irold =',3i4,' x,y,z =',4e10.3);
            IF(ierust > 1000) [
                OUTPUT;(////' Called exit---too many ustep errors'///);
                $CALL_EXIT(1);
            ]
        ]
        ustep = 0;
    ]
};

"MACRO FOR INTRODUCING FLUCTUATIONS IN THE ENERGY LOSS BY"
"CHARGED PARTICLES (E.G., 'LANDAU FLUCTUATIONS')---DEFAULT IS NULL"
REPLACE {$DE-FLUCTUATION;} WITH {;}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"Macro for production of annihilation quanta whenever"
"the energy is greater than AE but less than or equal to ECUT."
"photons are always produced in EGSnrc."

REPLACE {$POSITRON-ECUT-DISCARD;} WITH {EDEP=PEIE-PRM;}
"NOTE: TO GET THE EGS3 VERSION SIMPLY USE EDEP=PEIE+PRM"
"      AS THE REPLACEMENT PART OF THE MACRO."
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"MACROS FOR PARTICLE SELECTION (E.G., LEADING PARTICLE,"
"SPLITTING, ETC.).  DEFAULT IS ULTIMATELY 'NULL'"
"     -----IN SUBROUTINE ELECTR-----                 "
REPLACE {$PARTICLE-SELECTION-ELECTR;} WITH {;}
REPLACE {$PARTICLE-SELECTION-ANNIH;} WITH {
         $PARTICLE-SELECTION-ELECTR;}
REPLACE {$PARTICLE-SELECTION-ANNIHREST;} WITH {
        $PARTICLE-SELECTION-ELECTR;}
REPLACE {$PARTICLE-SELECTION-BHABHA;} WITH {
        $PARTICLE-SELECTION-ELECTR;}
REPLACE {$PARTICLE-SELECTION-BREMS;} WITH {
        $PARTICLE-SELECTION-ELECTR;}
REPLACE {$PARTICLE-SELECTION-MOLLER;}
   WITH {$PARTICLE-SELECTION-ELECTR;}
"     -----IN SUBROUTINE PHOTON-----                 "
REPLACE {$PARTICLE-SELECTION-PHOTON;} WITH {;}
REPLACE {$PARTICLE-SELECTION-COMPT;} WITH {
        $PARTICLE-SELECTION-PHOTON;}
REPLACE {$PARTICLE-SELECTION-PAIR;} WITH {
        $PARTICLE-SELECTION-PHOTON;}
REPLACE {$PARTICLE-SELECTION-PHOTO;} WITH {
        $PARTICLE-SELECTION-PHOTON;}

"MACRO FOR SELECTION OF THE ELECTRON MEAN-FREE-PATH"
REPLACE {$SELECT-ELECTRON-MFP;} WITH {
        $RANDOMSET RNNE1; IF(RNNE1.EQ.0.0) [RNNE1=1.E-30;]
         DEMFP=MAX(-LOG(RNNE1),$EPSEMFP);}

"MACRO FOR SELECTION OF THE PHOTON MEAN-FREE-PATH"
REPLACE {$SELECT-PHOTON-MFP;} WITH {
       $RANDOMSET RNNO35; IF(RNNO35.EQ.0.0) [RNNO35=1.E-30;]
         DPMFP=-LOG(RNNO35);}

"MACRO to do range rejection on a region by region basis"
"      if the user requests it.  The variables e_max_rr and i_do_rr"
"      are in COMIN ET-CONTROL.  This macro is called immediately"
"      after $USER-RANGE-DISCARD in ELECTR and everytime called"
"      the electrons current range has been computed and stored in"
"      range and the distance to the nearest boundary has just been"
"      computed and is in tperp.  e_max_rr and i_do_rr are initialized"
"      to zero in BLOCK DATA so range rejection is not done unless"
"      Since option must be turned on by the user, it is considered a"
"      USER-ELECTRON-DISCARD."
"      Note this technique implies an approximation because the particle"
"      is not allowed to create a brem particle which might escape"
"      the region.  This is why  e_max_rr is used, to allow high"
"      energy electrons to be tracked in case they give off brem."

REPLACE {$RANGE-DISCARD;} WITH {
  ;IF( i_do_rr(irl) = 1 & e(np) < e_max_rr(irl) ) [
      IF(tperp >= range) ["particle cannot escape local region"
          idisc = 50 + 49*iq(np); "1 for electrons, 99 for positrons"
          go to :USER-ELECTRON-DISCARD: ;
      ]
  ]
};


"MACRO TO ALLOW USER TO DISCARD IF AT OR NEAR END OF RANGE"
REPLACE {$USER-RANGE-DISCARD;} WITH {;}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"RAYLEIGH (COHERENT) SCATTERING MACROS"

"custom form factor file names"
/*********************************************************
   For simplicity, molecular form factors are assumed to
   ALWAYS be given as FF/SQRT(MW). Current available mol.
   FF are given this way.

   One could devise a more complex scheme, where the user
   enters by input in which form the FF are given and then,
   depending on whether the medium is defined as compound or
   mixture, egsnrc must or not multiplicate the Rayleigh
   xsection with the molecular weight.

   In the current scheme, this is done automatically
   without needing input from the user.
**********************************************************/
REPLACE {COMIN/rayleigh_inputs/;} WITH
"        ================"
{
;COMMON/rayleigh_inputs/iray_ff_media($MXMED),iray_ff_file($MXMED);
;character*24 iray_ff_media;
;character*128 iray_ff_file;
}

REPLACE {COMIN/rayleigh_sampling/;} WITH
"        ================"
{;COMMON/rayleigh_sampling/xgrid($MXRAYFF,$MXMED),
                            fcum($MXRAYFF,$MXMED),
                           b_array($MXRAYFF,$MXMED),
                           c_array($MXRAYFF,$MXMED),
                           i_array($RAYCDFSIZE,$MXMED),
                           $LGN(pmax($MXGE,$MXMED)/0,1/);
$REAL xgrid, fcum, b_array, c_array,pmax0, pmax1;
$INTEGER i_array;
}

REPLACE {$RAYLEIGH-CORRECTION;} WITH {
     ;IF(IRAYLR(IRL).EQ.1) [$EVALUATE COHFAC USING COHE(GLE);
    GMFP=GMFP*COHFAC];}

REPLACE {$OLD_RAYLEIGH-SCATTERING;} WITH {
      ;IF(IRAYLR(IRL).EQ.1) [
   $RANDOMSET RNNO37;
   IF (RNNO37.LE.(1.0-COHFAC)) [
   $AUSCALL($RAYLAUSB);
   NPold = NP;
   :SAMPLING-LOOP: LOOP [$RANDOMSET XXX;
   $SET INTERVAL XXX,RCO; $EVALUATE X2 USING RSCT(XXX);
   Q2=X2*RMSQ/(20.60744*20.60744);
   COSTHE=1.-Q2/(2.*E(NP)*E(NP));
   IF (ABS(COSTHE).GT.1.0) GO TO :SAMPLING-LOOP:;
   CSQTHE=COSTHE*COSTHE;
   REJF=(1.0+CSQTHE)/2.0;
   $RANDOMSET RNNORJ;
   ] UNTIL (RNNORJ <= REJF);
   SINTHE=SQRT(1.0-CSQTHE); CALL UPHI(2,1);
   $AUSCALL($RAYLAUSA);
   GOTO :PNEWENERGY:;]]
  }
REPLACE {$RAYLEIGH-SCATTERING;} WITH {
   ;IF(IRAYLR(IRL).EQ.1) [
   $RANDOMSET RNNO37;
   IF (RNNO37.LE.(1.0-COHFAC)) [
   $AUSCALL($RAYLAUSB);
   NPold = NP;
   call egs_rayleigh_sampling(MEDIUM,E(NP),GLE,LGLE,COSTHE,SINTHE);
   CALL UPHI(2,1);
   $AUSCALL($RAYLAUSA);
   GOTO :PNEWENERGY:;]]
}

"Ali:photonuc, 2 blocks"
REPLACE {$PHOTONUC-CORRECTION;} WITH {
     ;IF(IPHOTONUCR(IRL).EQ.1) [$EVALUATE PHOTONUCFAC USING PHOTONUC(GLE);
    GMFP=GMFP*PHOTONUCFAC];}

REPLACE {$PHOTONUCLEAR;} WITH {
   ;IF(IPHOTONUCR(IRL).EQ.1) [
      $RANDOMSET RNNO39;
      IF (RNNO39.LE.(1.0-PHOTONUCFAC)) [
        $AUSCALL($PHOTONUCAUSB);
        call PHOTONUC;
        $AUSCALL($PHOTONUCAUSA);
        GOTO :PNEWENERGY:;
      ]
    ]
}

"DENSITY RATIO SCALING MACRO (TO OVER-RIDE DENSITY IN A PARTICULAR"
"REGION)  NOTE: THIS MACRO REPLACES SUBROUTINE RHOSET OF EGS3"

REPLACE {$SET-RHOF;} WITH {RHOF=RHOR(IRL)/RHO(MEDIUM);}  "DEFAULT"

"TEMPLATES FOR PERFORMING CHARGED PARTICLE TRANSPORT IN EM FIELD"
REPLACE {$SET-TUSTEP-EM-FIELD;} WITH {;}
REPLACE {$SET-USTEP-EM-FIELD;} WITH {;}
REPLACE {$VACUUM-ADD-WORK-EM-FIELD;} WITH {;}
REPLACE {$SET-ANGLES-EM-FIELD;} WITH {;}
REPLACE {$SET-TVSTEP-EM-FIELD;} WITH {;}
REPLACE {$ADD-WORK-EM-FIELD;} WITH {;}
REPLACE {$EMFIELD_INITIATE_SET_TUSTEP;} WITH {;}
REPLACE {;COMIN/EM/;} WITH {;}
REPLACE {$EMFIELD_PII;} WITH {;}
REPLACE{$EMFIELD_PI;}WITH{;}
REPLACE{$EM_FIELD_SS;}WITH{;}
REPLACE{$ADD_WORK_EM_FIELD;}WITH{;}
REPLACE{$EMFieldInVacuum;}WITH{;}
REPLACE{$EM_MACROS_ACTIVE}WITH{.false.}
;  "---------- BUFFER FLUSH SEMICOLON ----------"

"------------------------------------------------------------------"
"        EGS4/EGSnrc GEOMETRY MACROS: AN EXTENSION TO EGS MACROS   "
"------------------------------------------------------------------"

"   NOTE1: CYLNDR IS A NEW MACRO BY G.R.STEVENSON OF CERN"
"          (SEE HS-RP/TM/80-78, 25 NOV. 1980)"

"   NOTE2: CONE IS A NEW MACRO BY H.HIRAYAMA OF KEK. "
"          MACRO REPLACEMENT OF CERN VERSION SUBROUTINE CONE"
"          (SEE HS-RP/TM/81-30, 5 MAY 1981)"

"   NOTE3: SPHERE IS A NEW MACRO BY G.R.STEVENSON OF CERN"
"          (SEE HS-RP/TM/81-30, 5 MAY 1981)"

"   NOTE4: $PLAN2X AND $PLAN2P ARE TWO NEW MACROS BY W.R.NELSON."
"          $PLAN2P WAS FORMERLY CALLED $PLANE2 AND IS STILL THE"
"          SAME (CALLS TO $PLANE2 WILL AUTOMATICALLY DEFAULT TO"
"          TO $PLAN2P).  $PLAN2X, HOWEVER, WILL CORRECTLY HANDLE"
"          THE CASE OF TWO, NON-PARALLEL PLANES."

"------------------------------------------------------------------"
"        MACRO-ROUTINES FOR PLANE GEOMETRY  (SLAC VERSION)         "
"------------------------------------------------------------------"
;
MXPLNS: int = 100  # MAX. NO. OF PLANES

"PLADTA---COMMON BLOCK FOR $PLANE1 AND $PLANE2 MACROS"
REPLACE {;COMIN/PLADTA/;} WITH {
      ;COMMON/PLADTA/PCOORD(3,$MXPLNS),PNORM(3,$MXPLNS);
      $REAL PCOORD, PNORM;
}

"$PLANE1---MACRO REPLACEMENT FOR SUBROUTINE PLANE1"
REPLACE {$PLANE1(#,#,#,#);} WITH {
 UDOTA=PNORM(1,{P1})*U(NP)+PNORM(2,{P1})*
 V(NP)+PNORM(3,{P1})*W(NP); UDOTAP={P2}*UDOTA;
 IF(UDOTA.EQ.0.0)[{P3}=2;]ELSEIF(UDOTAP.LT.0.0)
 [{P3}=0;] ELSE [{P3}=1;{P4}=(PNORM(1,{P1})*
 (PCOORD(1,{P1})-X(NP))+ PNORM(2,{P1})*
 (PCOORD(2,{P1})-Y(NP))+PNORM(3,{P1})*
 (PCOORD(3,{P1})-Z(NP)))/UDOTA;]}
"NOTE:   EVERYWHERE $PLANE1 IS USED ONE MUST"
"        INCLUDE COMIN/PLADTA,STACK/"

"------------------------------------------------------------------"

"$PLANE2---MACRO REPLACEMENT FOR SUBROUTINE PLANE2"
"          NOTE: $PLANE2 HAS BEEN SUPERCEDED BY $PLAN2P (BELOW),"
"                WHICH IS AUTOMATICALLY TAKEN CARE OF BY THE"
"                FOLLOWING MACRO STATEMENT."
REPLACE {$PLANE2} WITH {$PLAN2P}

"------------------------------------------------------------------"

"$PLAN2P---MACRO REPLACEMENT FOR SUBROUTINE PLAN2P (OR $PLANE2)"
"          (I.E., TWO PARALLEL PLANES)"
REPLACE {$PLAN2P(#,#,#,#,#,#);} WITH {
  $PLANE1({P1},{P3},IHIT,TVAL); IF(IHIT.EQ.1)
 [ $CHGTR(TVAL,{P2});] ELSEIF(IHIT.EQ.0)
 [$PLANE1({P4},{P6},IHIT,TVAL);$CHGTR(TVAL,{P5});]}
"NOTE:   EVERYWHERE $PLAN2P ($PLANE2) IS USED ONE MUST"
"        INCLUDE COMIN/EPCONT,PLADTA,STACK/"

"------------------------------------------------------------------"

"$PLAN2X---MACRO REPLACEMENT FOR SUBROUTINE PLAN2X"
"          (I.E., TWO, NON-PARALLEL (CROSSING) PLANES)"
REPLACE {$PLAN2X(#,#,#,#,#,#);} WITH {
    $PLANE1({P1},{P3},IHIT,TVAL); IF(IHIT.EQ.1) [
   $CHGTR(TVAL,{P2});]   $PLANE1({P4},{P6},IHIT,TVAL);
   IF(IHIT.EQ.1) [$CHGTR(TVAL,{P5});]}
"NOTE:   EVERYWHERE $PLAN2X IS USED ONE MUST"
"        INCLUDE COMIN/EPCONT,PLADTA,STACK/"

"------------------------------------------------------------------"
"      MACRO-ROUTINE FOR CYLINRICAL GEOMETRY  (CERN VERSION)       "
"------------------------------------------------------------------"

MXCYLS: int = 75  # MAX. NO. OF CYLINDERS
PARAMETER $DELCYL=1.0E-04; "CLOSEST ALLOWABLE DISTANCE TO SURFACE"

"CYLDTA---COMMON BLOCK FOR $CYLNDR MACRO"
REPLACE {;COMIN/CYLDTA/;} WITH {
   ;COMMON/CYLDTA/CYRAD2($MXCYLS);
   $REAL CYRAD2;
}

"$CYLNDR---MACRO REPLACEMENT FOR SUB CYLNDR GRS VERSION 14 11 80"
REPLACE {$CYLNDR(#,#,#,#);} WITH {
   {P3}=1;{P4}=0.0;ACYL=SQRT(U(NP)*U(NP)+V(NP)*V(NP));
   IF(ACYL.EQ.0.0)[{P3}=0;]  ELSE [
   BCYL=(X(NP)*U(NP)+Y(NP)*V(NP))/ACYL;CCYL=X(NP)*X(NP)+Y(NP)*Y(NP)
   -CYRAD2({P1});  ARGCY=BCYL*BCYL-CCYL;
   IF(ARGCY.LT.0.0) [{P3}=0;]   ELSE [
   IF(ABS(CCYL).LT.$DELCYL.AND.{P2}.EQ.0.AND.BCYL.GE.0.0)[{P3}=0;]
   ELSEIF(ABS(CCYL).LT.$DELCYL.AND.{P2}.EQ.1.AND.BCYL.LT.0.0)[
   {P4}=-2.0*BCYL/ACYL;]
   ELSE [ IF({P2}.EQ.1.AND.CCYL.GE.0.0)[{P3}=1;{P4}=$DELCYL;]
   ELSEIF({P2}.EQ.0.AND.CCYL.LE.0.0)[{P3}=1;{P4}=$DELCYL;]
   ELSE  [  ROOTCY=SQRT(ARGCY); IF(CCYL.LT.0.0)
   [{P4}=(-BCYL+ROOTCY)/ACYL;]
   ELSEIF(BCYL.LT.0.0) [{P4}=(-BCYL-ROOTCY)/ACYL;]
   ELSE [{P3}=0;]]]]]}
"NOTE:   EVERYWHERE $CYLNDR IS USED ONE MUST"
"         INCLUDE COMIN/CYLDTA,STACK/"

"$CYL2--MACRO EQUIVALENT FOR CYLNDR OF $PLANE2  GRS 17.11.80"
REPLACE {$CYL2(#,#,#,#);} WITH {
 $CYLNDR({P1},0,IHIT,TCYL);IF(IHIT.EQ.1)[
 $CHGTR(TCYL,{P2});]ELSE[$CYLNDR({P3},1,IHIT,TCYL);
 IF(IHIT.EQ.1)[ $CHGTR(TCYL,{P4});]]}
"NOTE:   EVERYWHERE $CYL2 IS USED ONE MUST
"         INCLUDE COMIN/CYLDTA,STACK/"

;  "---------- BUFFER FLUSH SEMICOLON ----------"

"------------------------------------------------------------------"
"     MACRO-ROUTINE FOR CERN CONICAL GEOMETRY  (SLAC VERSION)      "
"------------------------------------------------------------------"

MXCONES: int = 75  # MAXIMUM NUMBER OF CONES
PARAMETER $DELCON=1.0E-04; "CLOSEST ALLOWABLE DISTANCE TO SURFACE"

"CONDTA---COMMON BLOCK FOR $CONE MACRO"
REPLACE {;COMIN/CONDTA/;} WITH {
   ;COMMON/CONDTA/COTAL2($MXCONES),SMALLL($MXCONES);
   $REAL COTAL2, SMALLL;
}

"$CONE---MACRO REPLACEMENT FOR CERN VERSION SUBROUTINE CONE"
REPLACE {$CONE(#,#,#,#);} WITH {
   {P3}=0;ITWOPR=0;CPCON=COTAL2({P1});SGNCON=SIGN(1.0,CPCON);
   CPCON=ABS(CPCON);ZNP=SGNCON*(Z(NP)-SMALLL({P1}));
   WNP=SGNCON*W(NP);CPCON1=1.0+CPCON;
   CPCON2=SQRT(CPCON1);DCON1=X(NP)*X(NP)+Y(NP)*Y(NP);
   DCON2=SQRT(DCON1); IF((ZNP.GE.0.0).OR.(WNP.GE.0.0)) [
   ACON=(U(NP)*U(NP)+V(NP)*V(NP))*CPCON-WNP*WNP;
   BCON1=(X(NP)*U(NP)+Y(NP)*V(NP))*CPCON;BCON=BCON1-ZNP*WNP;
   CCON=DCON1*CPCON-ZNP*ZNP;
   IF(ACON.EQ.0.0)[IF(BCON.NE.0.0)
   [IF(ABS(CCON).LT.$DELCON.AND.ZNP.GE.0.0)[
   IF(({P2}.EQ.1.AND.BCON.GE.0.0).OR.({P2}.EQ.0.AND.BCON.LE.0.0))[
   TCON1=-CCON/(2*BCON);IF(TCON1.GE.0.0)[IF((ZNP+TCON1*WNP).GE.0.0)
   [{P4}=TCON1;{P3}=1;]]]]]
   ELSE[TCON1=CPCON2*ZNP*SIGN(1.0,-WNP);
   IF(TCON1.GE.0.0)[{P4}=TCON1;{P3}=1;]]]
   ELSEIF((ABS(CCON).LT.$DELCON).AND.(ZNP.GE.0.0))
   [BPRIM=BCON1-WNP*DCON2;
   IF({P2}.EQ.1.AND.BPRIM.LT.0.0)[TCON1=-2*BCON/ACON;
   IF(TCON1.GE.0.0) [{P4}=TCON1;{P3}=1;]]]
   ELSEIF({P2}.EQ.1.AND.CCON.GT.0.0) [{P4}=$DELCON;{P3}=1;]
   ELSEIF({P2}.EQ.0.AND.CCON.LT.0.0.AND.ZNP.GE.0.0)
   [{P4}=$DELCON;{P3}=1;] ELSE[CCON1=BCON*BCON-ACON*CCON;
   IF(CCON1.GE.0.0)[ROOT=SQRT(CCON1);
   IF(BCON.GT.0.0)[TCON11=-(BCON+ROOT)/ACON;]
   ELSE[TCON11=-CCON/(BCON-ROOT);]
   IF(BCON.LT.0.0)[TCON22=-(BCON-ROOT)/ACON;]
   ELSE[TCON22=-CCON/(BCON+ROOT);]
   IF((TCON11.GE.0.0).OR.(TCON22.GE.0.0))[
   IF(TCON11.LT.0.0)[TCON1=TCON22;]
   ELSE[IF(TCON22.LT.0.0)[TCON1=TCON11;] ELSE[ITWOPR=1;
   TCON1=min(TCON11,TCON22);TCON2=max(TCON11,TCON22);]]
   IF((ZNP+TCON1*WNP).GE.0.0)[{P4}=TCON1;{P3}=1;]
   ELSEIF((ITWOPR.EQ.1).AND.((ZNP+TCON2*WNP).GE.0.0))
   [{P4}=TCON2;{P3}=1;]]]]]}
"NOTE:   EVERYWHERE $CONE IS USED ONE MUST
"         INCLUDE COMIN/CONDTA,STACK/"

"$CON2--MACRO EQUIVALENT FOR CONE OF $PLANE2            "
REPLACE {$CON2(#,#,#,#);} WITH {
   $CONE({P1},0,IHIT,TCON);IF(IHIT.EQ.1)[
   $CHGTR(TCON,{P2});]ELSE[$CONE({P3},1,IHIT,TCON);IF(IHIT.EQ.1)[
   $CHGTR(TCON,{P4});]]}

"$CON21--MACRO EQUIVALENT FOR CONE OF $PLANE2 (IN THE CASE  "
"OF OUTSIDE TWO CONE SURFACE)                               "
REPLACE {$CON21(#,#,#,#);} WITH {
   $CONE({P1},0,IHIT,TCON);IF(IHIT.EQ.1)[
   $CHGTR(TCON,{P2});]ELSE[$CONE({P3},0,IHIT,TCON);IF(IHIT.EQ.1)[
   $CHGTR(TCON,{P4});]]}

;  "---------- BUFFER FLUSH SEMICOLON ----------"

"------------------------------------------------------------------"
"        MACRO-ROUTINE FOR SPHERICAL GEOMETRY  (CERN VERSION)      "
"------------------------------------------------------------------"

MXSPHE: int = 75  # MAX. NO. OF SPHERES
PARAMETER $DELSPH=1.0E-04; "CLOSEST ALLOWABLE DISTANCE TO SURFACE"

"SPHDTA------COMMON BLOCK FOR $SPHERE MACRO"
REPLACE {;COMIN/SPHDTA/;} WITH {
   ;COMMON/SPHDTA/SPRAD2($MXSPHE);
   $REAL SPRAD2;
}

"$SPHERE---MACRO REPLACEMENT FOR SUB SPHERE GRS VERSION 08 12 80"
REPLACE {$SPHERE(#,#,#,#);} WITH {
   {P3}=1;{P4}=0.0;ASPH=1.0;
   BSPH=(X(NP)*U(NP)+Y(NP)*V(NP)+Z(NP)*W(NP))/ASPH;CSPH=X(NP)*X(NP)
   +Y(NP)*Y(NP)+Z(NP)*Z(NP)  -SPRAD2({P1});  ARGSP=BSPH*BSPH-CSPH;
   IF(ARGSP.LT.0.0) [{P3}=0;]   ELSE [
   IF(ABS(CSPH).LT.$DELSPH.AND.{P2}.EQ.0.AND.BSPH.GE.0.0)[{P3}=0;]
   ELSEIF(ABS(CSPH).LT.$DELSPH.AND.{P2}.EQ.1.AND.BSPH.LT.0.0)[
   {P4}=-2.0*BSPH/ASPH;]
   ELSE [ IF({P2}.EQ.1.AND.CSPH.GE.0.0)[{P3}=1;{P4}=$DELSPH;]
   ELSEIF({P2}.EQ.0.AND.CSPH.LE.0.0)[{P3}=1;{P4}=$DELSPH;]
   ELSE [ROOTSP=SQRT(ARGSP); IF(CSPH.LT.0.0)
   [{P4}=(-BSPH+ROOTSP)/ASPH;] ELSEIF(BSPH.LT.0.0)
   [{P4}=(-BSPH-ROOTSP)/ASPH;] ELSE [{P3}=0;]]]]}
"NOTE:   EVERYWHERE $SPHERE IS USED ONE MUST
"         INCLUDE COMIN/SPHDTA,STACK/"

"$SPH2--MACRO EQUIVALENT FOR SPHERE OF $PLANE2  GRS 08.12.80"
REPLACE {$SPH2(#,#,#,#);} WITH {
 $SPHERE({P1},0,IHIT,TSPH);IF(IHIT.EQ.1)[
 $CHGTR(TSPH,{P2});]ELSE[$SPHERE({P3},1,IHIT,TSPH);
 IF(IHIT.EQ.1)[ $CHGTR(TSPH,{P4});]]}
"NOTE:   EVERYWHERE $SPH2 IS USED ONE MUST
"         INCLUDE COMIN/SPHDTA,STACK/"

;  "---------- BUFFER FLUSH SEMICOLON ----------"

"------------------------------------------------------------------"
"        MACRO-ROUTINE FOR CHANGING REGIONS  (SLAC VERSION)        "
"------------------------------------------------------------------"

"$CHGTR---MACRO REPLACEMENT FOR SUBROUTINE CHGTR"
REPLACE {$CHGTR(#,#);} WITH {
    ;IF({P1}.LE.USTEP) [USTEP={P1}; IRNEW={P2};]}
"NOTE:   EVERYWHERE $CHGTR IS USED ONE MUST
"         INCLUDE COMIN/EPCONT/"

"------------------------------------------------------------------"
"     MACRO-ROUTINE TO OBTAIN FINAL COORDINATES (SLAC VERSION)     "
"------------------------------------------------------------------"

"$FINVAL---MACRO REPLACEMENT FOR SUBROUTINE FINVAL"
REPLACE {$FINVAL(#,#,#,#);} WITH {
   {P2}=X(NP)+{P1}*U(NP); {P3}=Y(NP)+{P1}*V(NP);
   {P4}=Z(NP)+{P1}*W(NP);}
"NOTE:   EVERYWHERE $FINVAL IS USED ONE MUST
"         INCLUDE COMIN/STACK/"

"------------------------------------------------------------------"
"                 END OF GEMOETRY MACRO EXTENSION                  "
"------------------------------------------------------------------"

"******************************************************************"
"                                                                  "
"                    NRC EXTENSIONS                                "
"                                                                  "
"******************************************************************"

; "BUFFER FLUSH"
"--------------------------------------------------------------"
"                                                              "
"           PHOTOELECTRON ANGLE SELECTION                      "
"           =============================                      "
"                                                              "
"--------------------------------------------------------------"
"This macro can be used to select the photoelectron direction  "

REPLACE {$SELECT-PHOTOELECTRON-DIRECTION;} WITH {
"        ================================"
;IF(IPHTER(IR(NP)).EQ.1)[
  EELEC=E(NP);
  IF(EELEC.GT.ECUT(IR(NP)))[
    BETA=SQRT((EELEC-RM)*(EELEC+RM))/EELEC;
    GAMMA=EELEC/RM;
    ALPHA=0.5*GAMMA-0.5+1./GAMMA;
    RATIO=BETA/ALPHA;
    LOOP[
      $RANDOMSET RNPHT;RNPHT=2.*RNPHT-1.;
      IF(RATIO.LE.0.2)[
        FKAPPA=RNPHT+0.5*RATIO*(1.-RNPHT)*(1.+RNPHT);
        IF( gamma < 100 ) [
            COSTHE=(BETA+FKAPPA)/(1.+BETA*FKAPPA);
        ]
        ELSE [
            IF( fkappa > 0 ) [
                costhe = 1 - (1-fkappa)*(gamma-3)/(2*(1+fkappa)*(gamma-1)**3);
            ]
            ELSE [ COSTHE=(BETA+FKAPPA)/(1.+BETA*FKAPPA); ]
        ]
        "XI=1./(1.-BETA*COSTHE); <-- this numerically problematic "
        "                            at high energies, IK"
        xi = (1+beta*fkappa)*gamma*gamma;
      ]
      ELSE[
        XI=GAMMA*GAMMA*(1.+ALPHA*(SQRT(1.+RATIO*(2.*RNPHT+RATIO))-1.));
        COSTHE=(1.-1./XI)/BETA;
      ]
      SINTH2=MAX(0.,(1.-COSTHE)*(1.+COSTHE));
      $RANDOMSET RNPHT2;
      ]WHILE(RNPHT2.GT.0.5*(1.+GAMMA)*SINTH2*XI/GAMMA);
    SINTHE=SQRT(SINTH2);
    CALL UPHI(2,1);]]
}

; "BUFFER FLUSH"

"--------------------------------------------------------------"
"                                                              "
"           TSTEP RECURSION IN ELECTR                          "
"           =========================                          "
"                                                              "
"--------------------------------------------------------------"
"This macro can be used to control TSTEP recursion in ELECTR   "

REPLACE {$USER_CONTROLS_TSTEP_RECURSION;} WITH {;}

; "BUFFER FLUSH"

%C80
"------------------------------------------------------------------"
"  BREMSSTRAHLUNG ANGLE SELECTION MACROS                           "
"------------------------------------------------------------------"


"These macros are explained in NRCC REPORT #PIRS0203"
"by Bielajew, Mohan and Chui                        "

"Macro to initialize data for bremsstrahlung production               "
"The quantity ZBRANG is ( (1/111)*Zeff**(1/3) )**2                    "
"where Zeff is defined in equation (7) OF PIRS0203                    "
"This macro goes in SUBROUTINE HATCH                                  "
"                                                                     "
REPLACE {$INITIALIZE-BREMS-ANGLE;} WITH {
; IF(IBRDST.EQ.1)[
        DO IM=1,NMED[
            ZBRANG(IM)=0.0;PZNORM=0.0;
            DO IE=1,NNE(IM)[
                ZBRANG(IM)=
                  ZBRANG(IM)+PZ(IM,IE)*ZELEM(IM,IE)*(ZELEM(IM,IE)+1.0);
                PZNORM=PZNORM+PZ(IM,IE);
                ]
                ZBRANG(IM)=(8.116224E-05)*(ZBRANG(IM)/PZNORM)**(1./3.);
                LZBRANG(IM)=-log(ZBRANG(IM));
            ]
        ]
}
;

;

" Following is associated with the selection of bremsstrahlung photon"
" angle.  This has been implemented directly into the BREMS subroutine"
" and changed slightly. Nonetheless, this macro is still used."

"This is the function G(X) of PIRS0203               "
"The result is returned in {P1} as a function of {P2}"
"i.e. {P1}=G({P2}) where {P2}=X                      "
"                                                    "
REPLACE {$SET-BREM-REJECTION-FUNCTION(#,#);} WITH {
; Y2TST1=(1.+{P2})**2;
{P1}= (4.+LOG(RJARG3+ZTARG/Y2TST1))*(4.*ESEDEI*{P2}/Y2TST1-RJARG1)+RJARG2;
}
;

"------------------------------------------------------------------"
"  PAIR ANGLE SELECTION MACROS                                     "
"------------------------------------------------------------------"

"These macros are explained in NRCC REPORT # PIRS0287 by Bielajew     "

;
"Macro to initialize data for PAIR PRODUCTION                         "
"THE QUANTITY ZBRANG IS ( (1/111)*Zeff**(1/3) )**2                    "
"WHERE Zeff IS DEFINED IN EQUATION (7) OF PIRS0287                    "
"THIS MACRO GOES IN SUBROUTINE HATCH                                  "
"THIS MACRO IS IDENTICAL TO THE $INITIALIZE-BREMS-ANGLE DEFINED ABOVE "
"                                                                     "
REPLACE {$INITIALIZE-PAIR-ANGLE;} WITH {
;    IF(IPRDST.GT.0)[
        DO IM=1,NMED[
            ZBRANG(IM)=0.0;PZNORM=0.0;
            DO IE=1,NNE(IM)[
                ZBRANG(IM)=
                  ZBRANG(IM)+PZ(IM,IE)*ZELEM(IM,IE)*(ZELEM(IM,IE)+1.0);
                PZNORM=PZNORM+PZ(IM,IE);
                ]
                ZBRANG(IM)=(8.116224E-05)*(ZBRANG(IM)/PZNORM)**(1./3.);
            ]
        ]
}
;
"THRESHOLD BELOW WHICH ONLY LOWEST ORDER ANGULAR DISTRIBUTION OF THE  "
"PAIR ANGLE IS EMPLOYED. SCALE IS ENERGY (MeV).                       "
"USERS MAY OVERRIDE THIS WITH A HIGHER VALUE BUT A LOWER VALUE WILL   "
"CAUSE NON-PHYSICAL SAMPLING                                          "
"                                                                     "
REPLACE {$BHPAIR} WITH {4.14}
;
"THIS MACRO ENABLES VERY SMALL ANGLE SAMPLING TO BE     "
"ACCUMULATED. THE LIMIT OF 1.0E-10 BREAKS DOWN AROUND   "
"50 GEV OR SO (THETA=RM/E, FOR BOTH PAIR AND BREM).     "
"THIS MACRO REPLACES CODE IN UPHI AND IN THE PRESTA     "
"MACROS FOR THE LATERAL CORRELATION PART $PRESTA-LCDV.  "
;
REPLACE {(SINPS2.LT.1.0E-10)} WITH {(SINPS2.LT.1.0E-20)}
;
"THE FOLLOWING REPLACES THE EGS4 DEFAULT $SET-PAIR-ANGLE MACRO    "
"IT'S USE REQUIRES AN ASSOCIATE MACRO $SET-PAIR-REJECTION-FUNCTION"
"DEFINED BELOW                                                    "
"                                                                 "
"USAGE: IPRDST=0 => EGS4 DEFAULT ANGLE SELECTION                  "
"       IPRDST=1 => LOWEST ORDER ANGULAR DISTRIBUTION             "
"                                                                 "
"              d(Probability)            sin(theta)               "
"              -------------- = -------------------------------   "
"                 d(theta)      2*P*[E_total - P*cos(theta)]**2   "
"                                                                 "
"       IPRDST=2 => MOTZ, OLSEN AND KOCH (1969) EQ. 3D-2003       "
"                   IF IPRDST IS NON-ZERO AND E_PHOTON < $BHPAIR  "
"                   THE IPRDST=1 DISTRIBUTION IS USED             "
"                                                                 "
REPLACE {$SET-PAIR-ANGLE;} WITH {;
    IF( iprdst > 0 ) [
        IF( iprdst = 4 ) [
            $RANDOMSET rtest;
            "gbeta = (1-rmt2/eig)**8;"
            gbeta = PESE1/(PESE1+10);
            IF( rtest < gbeta ) [ iprdst_use = 1; ]
            ELSE [ iprdst_use = 4; ]
        ]
        ELSEIF ( iprdst = 2 & eig < $BHPAIR ) [ iprdst_use = 1; ]
        ELSE [ iprdst_use = iprdst; ]
        DO ichrg = 1,2 [
            IF(ICHRG.EQ.1)[ESE=PESE1;]ELSE[
                ESE=ESE2;
                IF( iprdst = 4 ) [
                    gbeta = ESE/(ESE+10);
                    $RANDOMSET rtest;
                    IF( rtest < gbeta ) [ iprdst_use = 1; ]
                    ELSE [ iprdst_use = 4; ]
                ]
            ]
            IF( iprdst_use = 1 ) [
                PSE=SQRT(MAX(0.0,(ESE-RM)*(ESE+RM)));
                $RANDOMSET COSTHE;COSTHE=1.0-2.0*COSTHE;
                SINTHE=RM*SQRT((1.0-COSTHE)*(1.0+COSTHE))/(PSE*COSTHE+ESE);
                COSTHE=(ESE*COSTHE+PSE)/(PSE*COSTHE+ESE);
            ]
            ELSE IF( iprdst_use = 2 ) [
                "ZBRANG=( (1/111)*Zeff**(1/3) )**2"
                ZTARG=ZBRANG(MEDIUM);
                "TTEIG=TOTAL INITIAL PHOTON ENERGY IN ELECTRON REST MASS UNITS"
                TTEIG=EIG/RM;
                "TTESE=TOTAL FINAL ELECTRON ENERGY IN ELECTRON REST MASS UNITS"
                TTESE=ESE/RM;
                "TTPSE=TOTAL FINAL ELECTRON MOMENTUM IN rm UNITS"
                TTPSE=SQRT((TTESE-1.0)*(TTESE+1.0));
                "THIS IS THE RATIO (r IN PIRS0287)"
                ESEDEI=TTESE/(TTEIG-TTESE);
                ESEDER=1.0/ESEDEI;
                "DETERMINE THE NORMALIZATION "
                XIMIN=1.0/(1.0+(3.141593*TTESE)**2);
                $SET-PAIR-REJECTION-FUNCTION(REJMIN,XIMIN);
                YA=(2.0/TTEIG)**2;
                XITRY=MAX(0.01,MAX(XIMIN,MIN(0.5,SQRT(YA/ZTARG))));
                GALPHA=1.0+0.25*LOG(YA+ZTARG*XITRY**2);
                GBETA=0.5*ZTARG*XITRY/(YA+ZTARG*XITRY**2);
                GALPHA=GALPHA-GBETA*(XITRY-0.5);
                XIMID=GALPHA/(3.0*GBETA);
                IF(GALPHA.GE.0.0)[
                    XIMID=0.5-XIMID+SQRT(XIMID**2+0.25);
                ]
                ELSE[
                    XIMID=0.5-XIMID-SQRT(XIMID**2+0.25);
                ]
                XIMID=MAX(0.01,MAX(XIMIN,MIN(0.5,XIMID)));
                $SET-PAIR-REJECTION-FUNCTION(REJMID,XIMID);
                "ESTIMATE MAXIMUM OF THE REJECTION FUNCTION"
                "FOR LATER USE BY THE REJECTION TECHNIQUE  "
                REJTOP=1.02*MAX(REJMIN,REJMID);
                LOOP[
                    $RANDOMSET XITST;
                    $SET-PAIR-REJECTION-FUNCTION(REJTST,XITST);
                    $RANDOMSET RTEST;
                    "CONVERT THE SUCCESSFUL CANDIDATE XITST TO AN ANGLE"
                    THETA=SQRT(1.0/XITST-1.0)/TTESE;
                    "LOOP UNTIL REJECTION TECHNIQUE ACCEPTS XITST"
                    REJTST_on_REJTOP   = REJTST/REJTOP;
                ]UNTIL((RTEST <= REJTST_on_REJTOP) & (THETA < PI) );
                SINTHE=SIN(THETA);COSTHE=COS(THETA);
            ]
            ELSE IF( iprdst_use = 3 ) [
                $RANDOMSET COSTHE;COSTHE=1.0-2.0*COSTHE;
                sinthe=(1-costhe)*(1+costhe);
                IF( sinthe > 0 ) [ sinthe = sqrt(sinthe); ] ELSE [ sinthe = 0; ]
            ]
            ELSE [
                "PSE=SQRT(MAX(1e-10,(ESE-RM)*(ESE+RM)));"
                "$RANDOMSET costhe;"
                "costhe=(ese-(ese+pse)*exp(-2*costhe*log((ese+pse)/rm)))/pse;"
                $RANDOMSET costhe;
                costhe=1-2*sqrt(costhe);
                sinthe=(1-costhe)*(1+costhe);
                IF( sinthe > 0 ) [ sinthe=sqrt(sinthe); ] ELSE [ sinthe=0; ]
            ]
            IF( ichrg = 1 ) [CALL UPHI(2,1);]
            ELSE [ sinthe=-sinthe; NP=NP+1; CALL UPHI(3,2); ]
        ]
        iq(np) = iq2; iq(np-1) = iq1; return;
    ]
    ELSE[
        THETA=0; "THETA=RM/EIG; "
    ]
}
;
"THIS IS THE FUNCTION d[G(XI)]/(d XI) OF PIRS0287    "
"THE RESULT IS RETURNED IN {P1} AS A FUNCTION OF {P2}"
"I.E. {P1}=G({P2}) WHERE {P2}=XI                     "
"                                                    "
REPLACE {$SET-PAIR-REJECTION-FUNCTION(#,#);} WITH {
; {P1} = 2.0+3.0*(ESEDEI+ESEDER) -
        4.00*(ESEDEI+ESEDER+1.0-4.0*({P2}-0.5)**2)*(
            1.0+0.25*LOG(
                ((1.0+ESEDER)*(1.0+ESEDEI)/(2.*TTEIG))**2+ZTARG*{P2}**2
                )
            )
        ;
}
;

REPLACE {$SELECT-LOW-ENERGY-PAIR-PRODICTION;} WITH
{
  $RANDOMSET RNNO30; $RANDOMSET rnno34;
  PESE2 = PRM + 0.5*RNNO30*(PEIG-2*PRM); PESE1 = PEIG - PESE2;
  IF( rnno34 < 0.5 ) [ iq1 = -1; iq2 = 1; ] ELSE [ iq1 = 1; iq2 = -1; ]
}
" IK introduced this macro because uniform energy distribution"
" is probably a better approximation than a zero energy 'electron'"
" for low energy pair production"

;

"THIS MACRO EXCHANGES TWO POSITIONS ON THE STACK"
"NB: LATCH IS A NON-STANDARD STACK VARIABLE     "
"    REMOVE IT IF IT CAUSES PROBLEMS            "
"                                               "
REPLACE {$EXCHANGE-STACK(#,#);} WITH {
;
FDUMMY = U({P2});     U({P2})     = U({P1});     U({P1})     = FDUMMY;
FDUMMY = V({P2});     V({P2})     = V({P1});     V({P1})     = FDUMMY;
FDUMMY = W({P2});     W({P2})     = W({P1});     W({P1})     = FDUMMY;
FDUMMY = E({P2});     E({P2})     = E({P1});     E({P1})     = FDUMMY;
FDUMMY = WT({P2});    WT({P2})    = WT({P1});    WT({P1})    = FDUMMY;
IDUMMY = IQ({P2});    IQ({P2})    = IQ({P1});    IQ({P1})    = IDUMMY;
"LATCH IS NOW STANDARD"
IDUMMY = LATCH({P2}); LATCH({P2}) = LATCH({P1}); LATCH({P1}) = IDUMMY;
}
;

REPLACE {;OUTPUT61#;#;} WITH {
"       ==============="
;{SETR A=@LG}
WRITE(6,{COPY A}){P1};WRITE(1,{COPY A}){P1};{COPY A}FORMAT{P2};}
;

" The following macro provides a second order evaluation of the   "
" stopping power. The parameter is half of the initial estimate of"
" the energy loss fraction. IK Oct 97                             "
REPLACE {$RE-EVALUATE-DEDX(#);} WITH
{
;
  elktmp = elke + Log(1 - {P1});
  $SET INTERVAL elktmp,eke;
  lelktmp = max(1,lelktmp);
  IF(lelec < 0)[$EVALUATE dedxmid USING ededx(elktmp);]
  ELSE         [$EVALUATE dedxmid USING pdedx(elktmp);]
  dedx = rhof*dedxmid*(1+0.17408298*({P1}/(1-{P1})/(eke+PRM))**2);
                   "0.17408298 is 2/3*m**2"
  {P1} = 2*{P1};
}

; "BUFFER FLUSH"


%E    "egsnrc.macros"
"******************************************************************"
"                                                                  "
"       transport algorithm related stuff                          "
"                                                                  "
"******************************************************************"

"Macros to denote the various transport algorithms"
"These numbers just have to be distinct"
"Note that the distributed version of EGSnrc does not include the VMC option"
REPLACE {$PRESTA-II} WITH {0}
REPLACE {$PRESTA--I} WITH {1}
REPLACE {$VMC}       WITH {2}

REPLACE {$CALL-USER-ELECTRON} WITH {;}

;
REPLACE {$MSCAT-DATAFILE} WITH {i_mscat}
  "Fortran unit number used to read in new MS"
;
REPLACE {$RANDOMIZE-TUSTEP} WITH {.false.}
  "Switches tustep randomization off"
;
REPLACE {$SKIN-DEPTH-FOR-BCA} WITH {3}
;
REPLACE {$PRESTA-DEBUG} WITH {.false.}
;
REPLACE {$EXACT-BCA-XIMAX} WITH {0.5}
;
REPLACE {$INEXACT-BCA-XIMAX} WITH {0.5} "this is not realy neccessary, "
                                        "it remained from Alex's coding"
;
REPLACE {$MAX-ELOSS} WITH {0.25}
;
REPLACE {$SUBSTEP-ELOSS-EVALUATION} WITH {.false.}
;
REPLACE {$MAX-SMAX} WITH {1e10}
;
REPLACE {$GLOBAL-ECUT} WITH {0.}
;
REPLACE {$GLOBAL-PCUT} WITH {0.}
;
REPLACE {$IBRDST-DEFAULT} WITH {1}
;
REPLACE {$IBR-NIST-DEFAULT} WITH {0}
;
REPLACE {$PAIR-NRC-DEFAULT} WITH {0}
;
REPLACE {$TRIPLET-DEFAULT} WITH {0}
;
REPLACE {$IPRDST-DEFAULT} WITH {1}
;
REPLACE {$IBCMP-DEFAULT} WITH {3} "set to norej"
;
REPLACE {$IEDGFL-DEFAULT} WITH {1}
;
REPLACE {$IPHTER-DEFAULT} WITH {1}
;
REPLACE {$TRANSPORT-ALGORITHM-DEFAULT} WITH {$PRESTA-II}
;
REPLACE {$BCA-ALGORITHM-DEFAULT} WITH {0}
;
REPLACE {$EXACT-BCA-DEFAULT} WITH {.true.}
;
REPLACE {$SPIN-EFFECTS-DEFAULT} WITH {.true.}
;
REPLACE {$IRAYLR-DEFAULT} WITH {1}
;
REPLACE {$AP-DEFAULT} WITH {-1}
;
REPLACE {$UP-DEFAULT} WITH {-1}
;
REPLACE {$XSEC-DEFAULT} WITH {0}
;
REPLACE {$XDATA-DEFAULT} WITH {'xcom'}
;
REPLACE {$COMP-XDATA-DEFAULT} WITH {'default'}
;
"EADL relaxation is now the default"
REPLACE {$EADL-RELAX-DEFAULT} WITH {.true.}
;
"Sabbatucci and Salvat PE xsections not the default yet"
REPLACE {$MCDF-PE-DEFAULT} WITH {.false.}
;
"Ali:photonuc, 2 lines"
REPLACE {$IPHOTONUCR-DEFAULT} WITH {0}
;
REPLACE {$PHOTONUC-XDATA-DEFAULT} WITH {'default'}
;
"EMH:emf, 7 lines"
REPLACE {$ExDEF} WITH {0}
;
REPLACE {$EyDEF} WITH {0}
;
REPLACE {$EzDEF} WITH {0}
;
REPLACE {$BxDEF} WITH {0}
;
REPLACE {$ByDEF} WITH {0}
;
REPLACE {$BzDEF} WITH {0}
;
REPLACE {$EMLMTDEF} WITH {0.02}
;

            "This macro sets the minimum step size for a condensed"
            "history (CH) step. When the exact BCA is used, the minimum"
            "CH step is determined by efficiency considerations only"
            "At about 3 elastic MFP's single scattering becomes more"
            "efficient than CH and so the algorithm switches off CH"
            "If one of the various inexact BCA's is invoked, this macro"
            "provides a simple way to include more sophisticated"
            "decisions about the maximum acceptable approximated CH step"

"The parameters passed to the macro in ELECTR are  eke and elke "

REPLACE {$SET-SKINDEPTH(#,#);} WITH
"        =================                  "
{
   $CALCULATE-ELASTIC-SCATTERING-MFP(ssmfp,{P1},{P2});
   skindepth = skindepth_for_bca*ssmfp;
}
;

"This macro calculates the elastic scattering MFP"
"If spin_effects is .false., the screened Rutherford cross section"
"is used, else the the elastic MFP is based on PWA cross sections"

REPLACE {$CALCULATE-ELASTIC-SCATTERING-MFP(#,#,#);} WITH
"        =======================================           "
{
    blccl = rhof*blcc(medium);
    xccl  = rhof*xcc(medium);
    p2 = {P2}*({P2}+rmt2); beta2 = p2/(p2 + rmsq);
    IF ( spin_effects ) [
      IF(lelec < 0) [ $EVALUATE etap USING etae_ms({P3}); ]
      ELSE          [ $EVALUATE etap USING etap_ms({P3}); ]
      $EVALUATE ms_corr USING blcce({P3});
      blccl = blccl/etap/(1+0.25*etap*xccl/blccl/p2)*ms_corr;
    ]
    {P1}=beta2/blccl;
}
;

REPLACE {$SINGLE-SCATTERING(#);} WITH
"        ======================                     "
{
    $SET-SCREENING-ANGLE({P1});
    call sscat(chia2,costhe,sinthe);
}
;

"The following macro will allow the use of better single scattering"
"cross sections (PWA) and/or to take into account double counting  "
"of the contribution of atomic electrons to the scattering power   "

REPLACE {$SET-SCREENING-ANGLE(#);} WITH
"        ========================                   "
{
    chia2   = xcc(medium)/(4*{P1}*({P1} + rmt2)*blcc(medium));
}
;

REPLACE {$HARD-SCATTERING;} WITH {;}
;

REPLACE {$TURN_OFF_SCATTERING} WITH {;}
;
"If the above is redefined in a user code or uncommented here                 "
"REPLACE {$TURN_OFF_SCATTERING} WITH {;cost = 1.000; sint = 0.000; return;}   "
"this will turn off all single and multiple scattering                        "
"DR April 2012   see corresponding 2 additions to egsnrc,mortran in           "
"                subroutines sscat and mscat

%E "egsnrc.macros"

REPLACE {$CALL-HOWFAR-IN-ELECTR;} WITH {;
  IF(callhowfar | wt(np) <= 0) [ call howfar; ]
};

REPLACE {$CALL-HOWFAR-IN-PHOTON;} WITH {;
  IF( ustep > dnear(np) | wt(np) <= 0 ) [ call howfar; ]
};

REPLACE {$CALL-HOWNEAR(#);} WITH
{
    OUTPUT 35; "35 in decimal is ascii code for the pound sign"
    (
        ' '/
        ' '/
        ' ***************************************************************'/
        ' ***************************************************************'/
        ' '/
        ' PRESTA-II is aborting execution because you have not defined   '/
        ' the HOWNEAR macro for your geometry.                           '/
        ' '/
        ' You MUST either do so or employ a limited form of PRESTA-II    '/
        ' which does not attempt the refined boundary crossing or lateral'/
        ' correlation features of the algorithm.                         '/
        ' '/
        ' If you include the following macro in your usercode:           '/
        ' '/
        ' REPLACE {$CALL-HOWNEAR(',a,');} WITH {;}                       '/
        ' '/
        ' you can choose between single scattering mode (very slow) and  '/
        ' standard EGS4 mode (no PRESTA enhancments) by the appropriate  '/
        ' choice of the parameters in your input file (see the PRESTA-II '/
        ' manual)                                                        '/
        ' '/
        ' ***************************************************************'/
        ' ***************************************************************'/
        ' '/
        ' '/
    );
    stop;
}

"For compability with user codes with PRESTA-I implemented"
REPLACE {$PRESTA-INPUT-SUMMARY;} WITH {;}
REPLACE {$PRESTA-INPUTS;}        WITH {;}

"If you want to read P-II inputs using the get_input() routine by "
"A. Merovitz and D.W.O.R. you need to either place the following  "
"three macros at the top of your user code, or after the default"
"definitions given below"

;

REPLACE {$USE-GET-INPUTS} WITH {.true.} "To not use get_input replace this "
                                        "with .false.                      "

"The following are the ones used by default"


REPLACE {$USE-GET-INPUTS} WITH {.false.}


;
%E    "egsnrc.macros"

"Macro for azimuthal angle selection
"using a sampling within a box method
"Choose a point randomly within a box such that
"-1 <= x <= 1 and 0 <= y < = 1
"Reject the set if it lies without the inscribed unit semicircle centered
"at (x,y) = (0,0)
"once out of the loop, use the trigonimetric relations (TeX notation)
"\cos 2\phi = (x^2 - y^2)/(x^2 + y^2)
"\sin 2\phi = 2xy/(x^2 + y^2)
REPLACE {$SELECT-AZIMUTHAL-ANGLE(#,#);} WITH
{
;
LOOP
[
    $RANDOMSET xphi;
    xphi  = 2*xphi - 1;
    xphi2 = xphi*xphi;
    $RANDOMSET yphi;
    yphi2  = yphi*yphi;
    rhophi2 = xphi2 + yphi2;
]WHILE(rhophi2 > 1);
rhophi2 = 1/rhophi2;
{P1}  = (xphi2 - yphi2)*rhophi2;
{P2}  = 2*xphi*yphi*rhophi2;
}
;

REPLACE {$DEFINE-VARIABLES-FOR-SELECT-AZIMUTHAL-ANGLE;} WITH {;
  $REAL xphi,xphi2,yphi,yphi2,rhophi2;
};

%E     "egsnrc.macros"
"************************************************************************"
"                                                                        "
"                 Definitions of local variables                         "
"                                                                        "
"************************************************************************"

REPLACE {$DEFINE-LOCAL-VARIABLES-ANNIH;} WITH
{;
"Local variables in order of appearance"
$ENERGY PRECISION
      PAVIP,    "precise total energy in the laboratory frame"
      PESG1,    "precise energy of 1st annihilation photon"
      PESG2;    "precise energy of 2nd annihilation photon"
$REAL AVIP,     "total energy in the laboratory frame"
      A,        "total energy in units of the electron's rest energy"
      G,T,P,    "energy, kinetic energy and momentum in units of RM"
      POT,      "P/T"
      EP0,      "minimum fractional energy"
      WSAMP,    "to avoid un-necessary calc. of Log((1-ep0)/ep0)"
      RNNO01,   "random numbers"
      RNNO02,
      EP,       "fractional energy of the more energetic photon"
      REJF,     "rejection function"
      ESG1,     "energy of the more energetic photon"
      ESG2,     "energy of the less energetic photon"
      aa,bb,cc,sinpsi,sindel,cosdel,us,vs,cphi,sphi;
                "for inline rotations"
$INTEGER
      ibr;
$DEFINE-VARIABLES-FOR-SELECT-AZIMUTHAL-ANGLE;
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-BHABHA;} WITH
{;
"Local variables in order of appearance"
$ENERGY PRECISION
      PEIP,     "precise total energy of incident positron"
      PEKIN,    "precise kinetic energy of incident positron"
      PEKSE2,   "precise kinetic energy of second 'electron'"
      PESE1,    "precise total energy of first 'electron'"
      PESE2,    "precise total energy of second 'electron'"
      H1,       "used in direction cosine calculations"
      DCOSTH;   "polar scattering angle for more energetic 'electron'"
$REAL EIP,      "total energy of incident positron"
      EKIN,     "kinetic energy of incident positron"
      T0,       "kinetic energy of incident positron in units of RM"
      E0,       "total energy of incident positron in units of RM"
      E02,      "E0**2"
      YY,       "1/(T0+2)"
      Y2,YP,YP2,"various functions of YY"
      BETA2,    "incident positron velocity in units of c"
      EP0,      "minimum fractional energy of a secondary 'electron'"
      EP0C,     "1-EP0"
      B1,B2,B3,B4,  "used in rejection function calculation"
      RNNO03,RNNO04,"random numbers"
      BR,       "kinetic energy fraction of the 2nd 'electron'"
      REJF2,    "rejection function"
      ESE1,     "total energy of 1st 'electron'"
      ESE2;     "total energy of 2nd 'electron'"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-BREMS;} WITH
{;
"Local variables in order of appearance"
$ENERGY PRECISION
  PEIE,   "precise incident electron energy"
  PESG,   "presice energy of emitted photon"
  PESE;   "precise total energy of scattered electron"
$REAL
  EIE,    "total incident electron energy"
  EKIN,   "kinetic incident energy"
  brmin,  " ap(medium)/ekin"
  waux,   "for faster sampling of 1/br"
  aux,    "ese/eie"
  r1,     "a random number"
  ajj,    "for energy bin determination if alias sampling is employed"
  alias_sample1,
  RNNO06, "random number"
  RNNO07, "random number"
  BR,     "energy fraction of secondary photon"
  ESG,    "energy of secondary photon"
  ESE,    "total energy of secondary electron"
  DELTA,  "scaled momentum transfer"
  phi1,   "screening function"
  phi2,   "screening function"
  REJF;   "screening rejection function"

"Brems angle selection variables"
$REAL
  a,b,c,  "direction cosines of incident `electron'"
  sinpsi, sindel, cosdel, us, vs,
          "all used for rotations"
  ztarg,  "(Zeff**1/3/111)**2, used for 2BS angle sampling"
  tteie,  "total energy in units of rest energy"
  beta,   "electron velocity in units of speed of light"
  y2max,  "maximum possible scaled angle"
  y2maxi, "inverse of the above"
  ttese,  "new electron energy in units of rm"
  rjarg1,rjarg2,rjarg3,rejmin,rejmid,rejmax,rejtop,rejtst,
          "all of them used for angle rejection function calcs"
  esedei, "new total energy over old total energy"
  y2tst,  "scaled angle, costhe = 1 - 2*y2tst/y2max"
  y2tst1,
  rtest,  "random number for rejection"
  xphi,yphi,xphi2,yphi2,rhophi2,cphi,sphi;
          "all of the above is for azimuthal angle sampling"

$INTEGER
  L,L1,ibr,jj,j;

}
;

REPLACE {$DEFINE-VARIABLES-FOR-SET-BREMS-ANGLE;} WITH
{;
"Local variables for photon angle selection"
$REAL ZTARG,  "( (1/111)*Zeff**(1/3) )**2"
      TTEIE,  "total incident electron energy in units of RM"
      TTESE,  "total scattered electron energy in units of RM"
      ESEDEI, "TTESE/TTEIE"
      beta,   "electron speed in units of c"
      Y2MAX,  "maximum value of the scaled angle"
      RJARG1,RJARG2,RJARG3,
              "arguments for which the rejection function is calculated"
      REJMIN,REJMID,REJMAX,
              "corresponding values of the rejection function"
      REJTOP, "max(REJMIN,REJMID,REJMAX)"
      Y2TST,  "random number and candidate for a scaled angle"
      REJTST, "rejection function at Y2TST"
      Y2TST1, "aux. variable for rejection function calculation"
      REJTST_on_REJTOP  ,  "ratio for rejection test"
      RTEST;  "random number for rejection"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-COMPT;} WITH
{;
"Local COMPT variables in order of appearance"
$ENERGY PRECISION
      PEIG,   "precise energy of incident photon"
      PESG,   "precise energy of scattered photon"
      PESE;   "precise total energy of compton electron"
$REAL ko,     "energy of incident photon in units of RM"
      broi,   "1+2*ko"
      broi2,  "broi*broi"
      bro,    "1/broi"
      bro1,   "1-bro"
      alph1,  "probability for the 1/BR part"
      alph2,  "probability for the BR part"
      alpha,  "alpha1/(alph1+alph2)"
      rnno15,rnno16,rnno17,rnno18,rnno19,
              "random numbers"
      br,     "scattered photon energy fraction"
      temp,   "aux. variable for polar angle calculation"
      rejf3,  "rejection function"
      rejmax, "max. of rejf3 in thge case of uniform sampling"
      Uj,     "binding energy of the selected shell"
      Jo,     "the Compton profile parameter"
      br2,    "br*br"
      fpz,fpz1,"used for limited pz-range rejection"
      qc,     "momentum transfer corresponding to the Compton line energy"
      qc2,    "qc squared"
      af,     "for calculating F"
      Fmax,   "maximum of F"
      frej,   "used for F-rejection"
      eta_incoh, eta, "random numbers"
      aux,aux1,aux2,aux3,aux4, "aux. variables"
      pzmax,  "max. possible z-component of the initial electron momentum"
      pz,     "initial electron momentum projection"
      pz2,    "pz*pz"
      rnno_RR;"for playing Russian Roulette"
$INTEGER
      irl,    "local region number"
      i,      "loop variable for shell sampling (and then shell sampled)"
      j,      "pointer to the shell in the shell data list"
      iarg,   "argument for ausgab call"
      ip;     "a loop variable"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-COMPT-old;} WITH
{;
"Local COMPT variables in order of appearance"
$ENERGY PRECISION
      PEIG,   "precise energy of incident photon"
      PESG,   "precise energy of scattered photon"
      PESE;   "precise total energy of compton electron"
$REAL ko,     "energy of incident photon in units of RM"
      broi,   "1+2*ko"
      broi2,  "broi*broi"
      bro,    "1/broi"
      bro1,   "1-bro"
      alph1,  "probability for the 1/BR part"
      alph2,  "probability for the BR part"
      alpha,  "alpha1/(alph1+alph2)"
      rnno15,rnno16,rnno17,rnno18,rnno19,
              "random numbers"
      br,     "scattered photon energy fraction"
      temp,   "aux. variable for polar angle calculation"
      rejf3,  "rejection function"
      rejmax, "max. of rejf3 in thge case of uniform sampling"
      Uj,     "binding energy of the selected shell"
      br2,    "br*br"
      aux,aux1,aux2,"aux. variables"
      pzmax2, "max. possible momentum transfer squared"
      pz,     "momentum transfer prejection"
      pz2,    "pz*pz"
      rnno_RR;"for playing Russian Roulette"
$INTEGER
      irl,    "local region number"
      i,      "loop variable for shell sampling (and then shell sampled)"
      j,      "pointer to the shell in the shell data list"
      iarg,   "argument for ausgab call"
      ip;     "a loop variable"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-ELECTR;} WITH
{;
" Local ELECTR variables"
$ENERGY PRECISION "($ENERGY PRECISION means double precision)"
    demfp,        "differential electron mean free path"
    peie,         "precise energy of incident electron"
    total_tstep,  "total path-length to next discrete interaction"
    total_de      "total energy loss to next discrete interaction"
;
$REAL
    ekems,      "kinetic energy used to sample MS angle (normally midpoint)"
    elkems,     "Log(ekems)"
    chia2,      "Multiple scattering screening angle"
    etap,       "correction to Moliere screening angle from PWA cross sections"
    lambda,     "number of mean free paths (elastic scattering cross section)"
    blccl,      "blcc(medium)*rhof"
    xccl,       "xcc(medium)*rhof"
    xi,         "used for PLC calculations (first GS moment times path-length)"
    xi_corr,    "correction to xi due to spin effects"
    ms_corr,
    p2,         "electron momentum times c, squared"
    beta2,      "electron speed in units of c, squared"
    de,         "energy loss to dedx"
    save_de,    "de saved before $DE-FLUCTUATION"
    dedx,       "stopping power after density scaling"
    dedx0,      "stopping power before density scaling"
    dedxmid,    "stopping power at mid-step before density scaling"
    ekei,       "used in $CALCULATE-TSTEP-FROM-DEMFP;"
    elkei,      "Log(ekei), used in $CALCULATE-TSTEP-FROM-DEMFP;"
    aux,        "aux. variable"
    ebr1,       "e- branching ratio into brem"
    eie,        "energy of incident electron"
    ekef,       "kinetic energy after a step"
    elkef,      "Log(ekef)"
    ekeold,     "kinetic energy before a step"
    eketmp,     "used to evaluate average kinetic energy of a step"
    elktmp,     "log(eketmp)"
    fedep,      "fractional energy loss used in stopping power calculation"
    tuss,       "sampled path-length to a single scattering event"
    pbr1,       "e+ branching ratio into brem"
    pbr2,       "e+ branching ratio into brem or Bhabha"
    range,      "electron range"
    rfict,      "rejection function for fictitious cross section"
    rnne1,      "random number"
    rnno24,     "random number"
    rnno25,     "random number"
    rnnotu,     "random number"
    rnnoss,     "random number"
    sig,        "cross section after density scaling but before a step"
    sig0,       "cross section before density scaling but before a step"
    sigf,       "cross section before density scaling but after a step"
    skindepth,  "skin depth employed for PRESTA-II boundary crossing"
    ssmfp,      "distance of one single elastic scattering mean free path"
    tmxs,       "electron step-size restriction"
    tperp,      "perpendicular distance to the closest boundary"
    ustep0,     "temporary storage for ustep"
    uscat,      "x-axis direction cosine for scattering"
    vscat,      "y-axis direction cosine for scattering"
    wscat,      "z-axis direction cosine for scattering"
    xtrans,     "final x-axis position after transport"
    ytrans,     "final y-axis position after transport"
    ztrans,     "final z-axis position after transport"
    cphi,sphi;  "for azimuthal angle selection for annih at rest"

$DEFINE-VARIABLES-FOR-SELECT-AZIMUTHAL-ANGLE;

$INTEGER
    iarg,      "calling code for ausgab"
    idr,       "calling code for ausgab"
    ierust,    "error counter for negative ustep errors"
    irl,       "region number"
    lelec,     "charge of electron"
    qel,       " = 0 for electrons, = 1 for positrons "
    lelke,     "index into the energy grid of tabulated functions"
    lelkems,   "index into the energy grid of tabulated functions"
    lelkef,    "index into the energy grid of tabulated functions"
    lelktmp,   "index into the energy grid of tabulated functions"
    ibr;       "a loop variable"

$LOGICAL
    "BCA = boundary crossing algorithm"
    callhowfar, "= .true.  => BCA requires a call to howfar"
                "= .false. => BCA does not require a call to howfar"
    domultiple, "= .true.  => inexact BCA requires multiple scattering"
    dosingle,   "= .true.  => exact BCA requires single scattering"
                "= .false. => exact BCA requires no single scattering"
    callmsdist, "= .true.  => normal condensed-history transport"
                "= .false. => one of the BCA's will be invoked"
    findindex,  "used for mscat"
    spin_index, "used for mscat with spin effects"
    compute_tstep
;
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-HATCH;} WITH
{;
"Local HATCH variables in alphabetical order"

$TYPE MBUF(72),MDLABL(8);

$REAL
    ACD   , "used to test goodness of sine-table look-up"
    ADEV  , "absolute deviation in sine-table look-up"
    ASD   , "used to test goodness of sine-table look-up"
    COST  , "cos(theta) from instrinsic library function"
    CTHET , "use to calculate cos(theta) according to look-up tables"
    DEL   , "leat squares delta for sine-table look-up"
    DFACT , "converts rl to dunits"
    DFACTI, "converts rl**-1 to dunits**-1"
    DUNITO, "units scaling varable"
    DUNITR, "saved value of dunit"
    FNSSS , "real form of integer nsinss"
    P     , "counter used in the pwr2i(i) = 1/2**(i - 1) construction"
    PZNORM, "used in $INITIALIZE-BREMS-ANGLE"
    RDEV  , "relative deviation in sine-table look-up"
    S2C2  , "sinthe**2 + costhe**2, used to test look-up table"
    S2C2MN, "min(s2c2)"
    S2C2MX, "max(s2c2)"
    SINT  , "sin(theta) from instrinsic library function"
    SX    , "sum of angles for least squared analysis of look-up table errors"
    SXX   , "sum**2 of angles for least square analysis of look-up table errors"
    SXY   , "sum of angle*sin(angle) for least squared analysis of look-up"
            "table errors"
    SY    , "sum of sin(angle) for least squared analysis of look-up table "
            "errors"
    WID   , "width of sine-table mesh sub-interval (sine-table algorithm)"
    XS    , "angle value in a sub-sub-interval (sine-table algorithm)"
    XS0   , "lower limit of a sub-sub-interval (sine-table algorithm)"
    XS1   , "upwer limit of a sub-sub-interval (sine-table algorithm)"
    XSI   , "beginning angle of a sun-interval (sine-table algorithm)"
    WSS   , "width of a sub-sub-interval (sine-table algorithm)"
    YS    , "sin(angle) for least squared analysis of look-up table errors"
    ZEROS(3); "zeros of sine, 0,pi,twopi"

$INTEGER
    I     , "generic do-loop variable"
    I1ST  , "flag = 0 on first pass"
    IB    , "do-loop variable used for reading the medium type"
    ID    , "integer value of -dunit, when dunit is negative"
    IE    , "do-loop variable for reading over elements in a compound/mixture"
    IL    , "do-loop variable used for reading the medium type"
    IM    , "do-loop variable looping over nmed, number of media"
    IRAYL , "Rayleigh switch read in from PEGS"
    IRN   , "do-loop variable over random set of sine-table look-ups"
    ISTEST, "flag that switches on test of sine function fit"
    ISUB  , "do-loop variable over sub-intervals of the sine look-up table"
    ISS   , "do-loop variable over sub-sub-intervals of the sine look-up table"
    IZ    , "used to locate an exact zero of a sun-interval mesh point in the"
            "sine-table look-up"
    IZZ   , "do-loop variable over the exact zeros of the sine-table look-up"
    J     , "do-loop variable looping over nmed, number of media"
    JR    , "do-loop variable looping over number of regions"
    LCTHET, "$SET INTERVAL index for cos(theta) from look-up table"
    LMDL  , "character width of medium header ' MEDIUM='"
    LMDN  , "character width of medium description"
    LTHETA, "$SET INTERVAL index for sin(theta) from look-up table"
    MD    , "temporary storage for the medium number"
    MXSINC, "number of intervals approximating the sine function"
    NCMFP , "array size input from PEGS. Currently 0, but probably intended"
            "to be cumulative electron mean free path. Presently unused."
    NEKE  , "array size input from PEGS."
            "Number of electron mapped energy intervals."
    NGE   , "array size input from PEGS."
            "Number of photon mapped energy intervals."
    NGRIM , "Rayleigh cross section array size."
    NISUB , "mxsinc - 2. Size of array with endpoints removed."
    NLEKE , "array size input from PEGS. Currently 0, but probably intended"
            "to be number of electron energy intervals below threshold."
            "Presently unused."
    NM    , "number of media found in the "
    NRANGE, "array size input from PEGS. Currently 0, but probably intended"
            "to be number of intervals in an array giving the electron range."
            "Presently unused."
    NRNA  , "number of random angles testing sine function fit"
    NSEKE , "array size input from PEGS. Currently 0, but probably intended"
            "to be number of electron small energy intervals. Presently unused."
    NSGE  , "array size input from PEGS. Currently 0, but probably intended"
            "to be number of gamma small energy intervals. Presently unused."
    NSINSS, "number of sub-intervals for each sine function interval"
    LOK($MXMED); "flag indicating that medium has been found in the PEGS "
                 "datafile"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-MOLLER;} WITH
{;
"Local MOLLER variables in order of their appearance"

$ENERGY PRECISION
     PEIE,   "precise total energy of incident electron"
     PEKSE2, "precise kinetic energy of 2nd secondary electron"
     PESE1,  "precise total energy of 1st secondary electron"
     PESE2,  "precise total energy of 2nd secondary electron"
     PEKIN,  "precise kinetic energy of incident electron"
     H1,     "used for polar scattering angle calculation"
     DCOSTH; "polar scattering angle squared"
$REAL EIE,    "total energy of incident electron"
     EKIN,   "kinetic energy of incident electron"
     T0,     "kinetic energy of incident electron in units of RM"
     E0,     "total energy of incident electron in units of RM"
     EXTRAE, "energy above the Moller threshold"
     E02,    "E0**2"
     EP0,    "minimum alowed kinetic energy fraction"
     G2,G3,  "used for rejection function calculation"
     GMAX,   "maximum value of the rejection function"
     BR,     "kinetic energy fraction to lowew energy electron"
     R,      "(1-BR)/BR"
     REJF4,  "rejection function"
     RNNO27, "random number for BR sampling"
     RNNO28, "random number for rejection"
     ESE1,   "energy of 1st secondary electron"
     ESE2;   "energy of 2nd secondary electron"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-PAIR;} WITH
{;
"Local PAIR variables in order of their appearance"
$ENERGY PRECISION
      PEIG,      "precise energy of incident photon"
      PESE1,     "precise energy of 1st 'electron'"
      PESE2;     "precise energy of 2nd 'electron'"

$REAL EIG,       "energy of incident photon"
      ESE2,      "total energy of lower energy 'electron'"
      RNNO30,RNNO31,rnno32,rnno33,rnno34,
                 "random numbers"
      DELTA,     "scaled momentum transfer"
      REJF,      "screening rejection function"
      rejmax,    "the maximum of rejf"
      aux1,aux2, "auxilary variables"
      Amax,      "Maximum of the screening function used with (br-1/2)**2"
      Bmax,      "Maximum of the screening function used with the uniform part"
      del0,      "delcm*eig"
      br,        "fraction of the available energy (eig-rmt2) going to the"
                 "lower energy `electron'"
      Eminus,Eplus,Eavail,rnno_RR;

$INTEGER
      L,L1;  "flags for high/low energy distributions"
}
;

REPLACE {$DEFINE-VARIABLES-FOR-SET-PAIR-ANGLE;} WITH
{;
$REAL ESE,   "total energy of one of the 'electrons'"
      PSE,   "momentum corresponding to ESE"
      ZTARG, "( (1/111)*Zeff**(1/3) )**2"
      TTEIG, "incident photon energy in units of RM"
      TTESE, "energy of one of the 'electrons' in units of RM"
      TTPSE, "momentum of one of the 'electrons' in units of RM"
      ESEDEI,"TTESE/(TTEIG-TTESE) = ratio of secondary electron energies"
      ESEDER,"1/ESEDEI"
      XIMIN, "1st argument where rejection function might have a maximum"
      XIMID, "2nd argument where rejection function might have a maximum"
      REJMIN,"rejection function at XIMIN"
      REJMID,"rejection function at XIMID"
      REJTOP,"max(REJMIN,REJMID)"
      YA,XITRY,GALPHA,GBETA,
             "aux. variables for XIMID calculation"
      XITST, "random number for pair angle sampling"
      REJTST_on_REJTOP  ,  "ratio for rejection test"
      REJTST,"rejection function at XITST"
      RTEST; "random number for rejection"
$INTEGER
      ICHRG; "loop variable"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-PHOTO;} WITH
{;
"Local PHOTO variables in order of their appearance"

$ENERGY PRECISION
      PEIG;         "precise energy of incident photon"
$REAL BR,           "random number"
      sigma,        "elemental cross section"
      aux,aux1,     "aux. variables"
      probs($MXEL), "probability for an interaction with a given element"
      sigtot,       "total cross section"
      e_vac,        "shell binding energy"
      rnno_RR;      "for playing Russian Roulette"
$INTEGER
      IARG,         "AUSGAB calling switch"
      iZ,           "Atomic number of the element the photon is "
                    "interactiong with"
      irl,          "local region number"
      ints($MXEL),  "energy interval number for a given element"
      j,ip,         "loop variables"
      n_warning,    "a warning counter"
      k;            "shell number"

$LOGICAL
      do_relax;
save  n_warning;
}
;

REPLACE {$DEFINE-VARIABLES-FOR-SELECT-PHOTOELECTRON-DIRECTION;} WITH
{;
"Photo-electron angle selection variables"
$REAL EELEC, "total energy of photo-electron"
      BETA,  "velocity of electron in units of c"
      GAMMA, "total energy of photo-electron in units of RM"
      ALPHA, "kinematic factor"
      RATIO, "=BETA/ALPHA"
      RNPHT, "random number"
      FKAPPA,"aux. variable for COSTHE calculation"
      XI,    "used in rejection function calculation"
      SINTH2,"SINTHE**2"
      RNPHT2;"random number for rejection"
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-EDGSET;} WITH
{;
"Local EDGSET variables in order of their appearance"
$REAL EALF(100),EBET(100),OMEG(100),PHOTOK(100),PKA(100);
      "see the data statements in EDGSETfor definition of these arrays"
$INTEGER JJ,IZ,IMED,I;
}
;

REPLACE {$DEFINE-LOCAL-VARIABLES-PHOTON;} WITH
{;
"Local PHOTON variables in order of their appearance"
$ENERGY PRECISION
    PEIG;   "precise photon energy"
;
$REAL
    EIG,    "photon energy"
    RNNO35, "random number for default MFP selection"
    GMFPR0, "photon MFP before density scaling and coherent correction"
    GMFP,   "photon MFP after density scaling"
    COHFAC, "Rayleigh scattering correction"
    RNNO37, "random number for Rayleigh scattering selection"
    XXX,    "random number for momentum transfer sampling in Rayleigh"
    X2,     "scaled momentum transfer in Rayleigh scattering event"
    Q2,     "momentum transfer squared in Rayleigh scattering event"
    CSQTHE, "COSTHE**2"
    REJF,   "Rayleigh scattering rejection function"
    RNNORJ, "random number for rejection in Rayleigh scattering"
    RNNO36, "random number for interaction branching"
    GBR1,   "probability for pair production"
    GBR2,   "probability for pair + compton"
    T,      "used for particle exchange on the stack"
"Ali:photonuc, 2 lines"
    PHOTONUCFAC, "photonuclear correction"
    RNNO39; "random number for photonuclear selection (RNNO38 is taken)"
;
$INTEGER
    IARG,   "parameter for AUSGAB"
    IDR,    "parameter for AUSGAB"
    IRL,    "region number"
    LGLE,   "index for GMFP interpolation"
    LXXX;   "index for Rayleigh scattering cummulative distribution int."
}
;

"Ali:photonuc, 1 block"
REPLACE {$DEFINE-LOCAL-VARIABLES-PHOTONUC;} WITH {;}
;

" Handling track-ends "
" By default, just call AUSGAB and drop energy on the spot"

REPLACE {$ELECTRON-TRACK-END;} WITH {; $AUSCALL(idr); }
REPLACE {$PHOTON-TRACK-END;}   WITH {; $AUSCALL(IDR); }
;

" Macros for the fictitious method  "
"==================================="

" The following version uses sub-threshold energy loss "
" as a measure of path-length => cross section is actual "
" cross section divided by restricted stopping power "
" The global maximum of this quantity called esig_e (electrons) or "
" psig_e (positrons) and is determined in HATCH "

REPLACE {$EVALUATE-SIG0;} WITH
"        ==============="
{;
   IF( sig_ismonotone(qel,medium) ) [
       $EVALUATE-SIGF; sig0 = sigf;
   ]
   ELSE [
       IF( lelec < 0 ) [sig0 = esig_e(medium);]
       ELSE            [sig0 = psig_e(medium);]
   ]
}

REPLACE {$EVALUATE-SIGF;} WITH
"        ==============="
{;
  IF(lelec < 0)
  [
      $EVALUATE sigf USING esig(elke);
      $EVALUATE dedx0 USING ededx(elke);
      sigf = sigf/dedx0;
  ]
  ELSE
  [
      $EVALUATE sigf USING psig(elke);
      $EVALUATE dedx0 USING pdedx(elke);
      sigf = sigf/dedx0;
  ]
}
;

REPLACE {$EVALUATE-EBREM-FRACTION;} WITH {
    $EVALUATE ebr1 USING ebr1(elke);
};
REPLACE {$EVALUATE-PBREM-FRACTION;} WITH {
    $EVALUATE pbr1 USING pbr1(elke);
};
REPLACE {$EVALUATE-BHABHA-FRACTION;} WITH {
    $EVALUATE pbr2 USING pbr2(elke);
};


" Because the cross section is interactions per energy loss, no "
" rhof-scaling is required "
REPLACE {$SCALE-SIG0;} WITH
"        ============"
{
   sig = sig0;
}
;

" Once the sub-threshold processes energy loss to the next discrete "
" interaction is determined, the corresponding path-length has to be"
" calculated. This is done by the macro below. This macro           "
" assumes the energy at the begining to be eke, the logarithm of it "
" elke, lelke - the corresponding interpolation index and makes     "
" use of $COMPUTE-DRANGE(#,#,#,#,#,#)                               "

REPLACE {$CALCULATE-TSTEP-FROM-DEMFP;} WITH
"        ============================"
{;
  IF( compute_tstep ) [
    total_de = demfp/sig; fedep = total_de;
    ekef  = eke - fedep;
    IF( ekef <= E_array(1,medium) ) [ tstep = vacdst; ]
    ELSE
    [
      elkef = Log(ekef);
      $SET INTERVAL elkef,eke;
      IF( lelkef = lelke )
      [       " initial and final energy are in the same interpolation bin "
          $COMPUTE-DRANGE(eke,ekef,lelke,elke,elkef,tstep);
      ]
      ELSE
      [   " initial and final energy are in different interpolation bins, "
          " calc range from ekef to E(lelkef+1) and from E(lelke) to eke  "
          " and add the pre-calculated range from E(lelkef+1) to E(lelke) "
          ekei = E_array(lelke,medium);
          elkei = (lelke - eke0(medium))/eke1(medium);
          $COMPUTE-DRANGE(eke,ekei,lelke,elke,elkei,tuss);
          ekei = E_array(lelkef+1,medium);
          elkei = (lelkef + 1 - eke0(medium))/eke1(medium);
          $COMPUTE-DRANGE(ekei,ekef,lelkef,elkei,elkef,tstep);
          tstep=tstep+tuss+
                  range_ep(qel,lelke,medium)-range_ep(qel,lelkef+1,medium);
      ]
    ]
    total_tstep = tstep;
    compute_tstep = .false.;
  ]
  tstep = total_tstep/rhof;  " non-default density scaling "
}
;

" The following macro computes the path-length traveled while going from  "
" energy {P1} to energy {P2}, both energies being in the same             "
" interpolation bin, given by {P3}. {P4} and {P5} are the logarithms of   "
" {P1} and {P2}. The expression is based on logarithmic interpolation as  "
" used in EGSnrc (i.e. dedx = a + b*Log(E) ) and a power series expansion "
" of the ExpIntegralEi function that is the result of the integration.    "
" The result is returned in {P6}.                                         "

REPLACE {$COMPUTE-DRANGE(#,#,#,#,#,#);} WITH
"        ============================="
{
  fedep = 1 - {P2}/{P1};
  elktmp = 0.5*({P4}+{P5}+0.25*fedep*fedep*(1+fedep*(1+0.875*fedep)));
           " the above evaluates the logarithm of the midpoint energy"
  lelktmp = {P3};
  IF(lelec < 0) [
      $EVALUATE dedxmid USING ededx(elktmp);
      dedxmid = 1/dedxmid;
      aux = ededx1(lelktmp,medium)*dedxmid;
      "aux = ededx1(lelktmp,medium)/dedxmid;"
  ]
  ELSE [
      $EVALUATE dedxmid USING pdedx(elktmp);
      dedxmid = 1/dedxmid;
      aux = pdedx1(lelktmp,medium)*dedxmid;
      "aux = pdedx1(lelktmp,medium)/dedxmid;"
  ]
  aux = aux*(1+2*aux)*(fedep/(2-fedep))**2/6;
  "{P6} = fedep*{P1}/dedxmid*(1+aux);"
  {P6} = fedep*{P1}*dedxmid*(1+aux);
}
;

" The following macro computes the range to the minimum table energy "
" It uses $COMPUTE-DRANGE                                            "
" Note that range_ep array is precomputed in subroutine mscati and   "
" gives the range from the energy interval end points to AE for each "
" medium.

REPLACE {$COMPUTE-RANGE;} WITH
"        ==============="
{
;
  ekei = E_array(lelke,medium);
  elkei = (lelke - eke0(medium))/eke1(medium);
  $COMPUTE-DRANGE(eke,ekei,lelke,elke,elkei,range);
  range = (range + range_ep(qel,lelke,medium))/rhof;
}
;

/******* trying to save evaluation of range.
REPLACE {$COMPUTE-RANGE;} WITH {;
"        ==============="
  IF( do_range ) [
      ekei = E_array(lelke,medium);
      elkei = (lelke - eke0(medium))/eke1(medium);
      $COMPUTE-DRANGE(eke,ekei,lelke,elke,elkei,range);
      the_range = range + range_ep(qel,lelke,medium);
      do_range = .false.;
  ]
  range = the_range/rhof;
};
******************/

" The following macro updates demfp. As energy loss is used as the  "
" 'path-length' variable (see above), it just substracts the energy "
" loss for the step.                                                "
REPLACE {$UPDATE-DEMFP;} WITH
"        =============="
{
  demfp = demfp - save_de*sig;
  total_de = total_de - save_de;
  total_tstep = total_tstep - tvstep*rhof;
  IF( total_tstep < 1e-9 ) [ demfp = 0; ]
}
;

" The following macro computes the energy loss due to sub-threshold "
" processes for a path-length {P1}. The energy at the beginning of  "
" the step is {P2}, {P3}=Log({P2}), {P4} is the interpolation index "
" The formulae are based on the logarithmic interpolation for dedx  "
" used in EGSnrc. The result is returned in {P5}. Assumes that      "
" initial and final energy are in the same interpolation bin.       "

REPLACE {$COMPUTE-ELOSS(#,#,#,#,#);} WITH
"        =========================="
{;
  IF( lelec < 0 ) [
      $EVALUATE dedxmid USING ededx({P3});
      aux = ededx1({P4},medium)/dedxmid;
  ]
  ELSE [
      $EVALUATE dedxmid USING pdedx({P3});
      aux = pdedx1({P4},medium)/dedxmid;
  ]
  /*
  {P5} = dedxmid*{P1};  " Energy loss using stopping power at the beginning "
  */
  {P5} = dedxmid*{P1}*rhof; "IK: rhof scaling bug, June 9 2006"
                            "rhof scaling must be done here and NOT in "
                            "$COMPUTE-ELOSS-G below!"
  fedep = {P5}/{P2};
  {P5} = {P5}*(1-0.5*fedep*aux*(1-0.333333*fedep*(aux-1-
             0.25*fedep*(2-aux*(4-aux)))));
}
;

" The following is a generalized version of $COMPUTE-ELOSS.        "

REPLACE {$COMPUTE-ELOSS-G(#,#,#,#,#);} WITH
"        ============================"
{
  tuss = range - range_ep(qel,{P4},medium)/rhof;
    " here tuss is the range between the initial energy and the next lower "
    " energy on the interpolation grid "
  IF( tuss >= {P1} ) [  " Final energy is in the same interpolation bin "
      $COMPUTE-ELOSS({P1},{P2},{P3},{P4},{P5});
      /* {P5} = {P5}*rhof; "IK, rhof bug"  */
      "IK: rhof scaling bug, June 9 2006. rhof scaling is done in "
      "    $COMPUTE-ELOSS above!                                  "
  ]
  ELSE [ " Must find first the table index where the step ends using "
         " pre-calculated ranges                                     "
      lelktmp = {P4};
      tuss = (range - {P1})*rhof;
         " now tuss is the range of the final energy electron "
         " scaled to the default mass density from PEGS4      "
      IF( tuss <= 0 ) [ {P5} = {P2} - TE(medium)*0.99; ]
        " i.e., if the step we intend to take is longer than the particle "
        " range, the particle energy goes down to the threshold "
        "({P2} is the initial particle energy)  "
        "originally the entire energy was lost, but msdist_xxx is not prepared"
        "to deal with such large eloss fractions => changed July 2005."
      ELSE [
          WHILE ( tuss < range_ep(qel,lelktmp,medium) ) [
              lelktmp = lelktmp - 1; ]
          elktmp = (lelktmp+1-eke0(medium))/eke1(medium);
          eketmp = E_array(lelktmp+1,medium);
          "tuss = range_ep(qel,lelktmp+1,medium) - tuss;"
          "IK: rhof scaling bug, June 9 2006: because of the change in "
          "    $COMPUTE-ELOSS above, we must scale tuss by rhof        "
          tuss = (range_ep(qel,lelktmp+1,medium) - tuss)/rhof;
          $COMPUTE-ELOSS(tuss,eketmp,elktmp,lelktmp,{P5});
          {P5} = {P5} + {P2} - eketmp;
      ]
  ]
}
;
%E  "egsnrc.macros"
"============================================================================"
"
"   The following is related to use of the NRC auxilliary get_inputs
"   routine which is part of the standard NRC user-codes.
"
"   It is not an essential part of EGSnrc but is most easily defined here.
"
"============================================================================"
"
" Input stuff for the get_inputs() routine.                                  "
" As the expirience has shown that get_inputs() is frequently used in several"
" subroutines, I changed the parameter passed to get_inputs() to a common    "
" block. Otherwise, the parameters have to be defined in each subroutine using"
" get_inputs() and, with static variables, this lead to a memory use         "
" explosion (e.g. 8 MB for CAVRZ vs. 0.8 MB without get_inputs()!)           "
" IK, Dec. 1998                                                              "

REPLACE {$NMAX} WITH {100};
REPLACE {$NVALUE} WITH {100};
REPLACE {$STRING80} WITH {80};
REPLACE {$STRING32} WITH {64};
REPLACE {$STRING40} WITH {40};
REPLACE {$STRING256} WITH {256};
REPLACE {$MXALINP} WITH {5};

REPLACE {COMIN/GetInput/;} WITH
"        ================"
{
  ;COMMON/GetInput/
        ALLOWED_INPUTS($NMAX,0:$MXALINP), "Associates a name with each second "
                                   "array index(0:4) for a value sought"
        VALUES_SOUGHT($NMAX),      "Name of each input                 "
        CHAR_VALUE($NMAX,$NVALUE), "For returning character inputs     "
        VALUE($NMAX,$NVALUE),      "For returning int. or real inputs  "
        DEFAULT($NMAX),            "Default value, only for type 0 & 1 "
        VALUE_MIN($NMAX),          "Min and max value defining         "
        VALUE_MAX($NMAX),          "the acceptable input range         "
        NVALUE($NMAX),             "Number of values per value sought  "
        TYPE($NMAX),               "Type of the value sought           "
                                   "0 for integer                      "
                                   "1 for real                         "
                                   "2 for character                    "
                                   "3 for character with allowed_inputs"
        ERROR_FLAGS($NMAX),        "An error flag for each of the      "
                                   "attempted inputs                   "
        i_errors,                  "Unit no. for .errors output file   "
        NMIN, NMAX,                "Minimum and maximum index number of"
                                   "the values sought                  "
        ERROR_FLAG,                "0 for no errors, 1 for errors      "
        DELIMETER;                 "Name of the delimeter              "
   character ALLOWED_INPUTS*$STRING32,VALUES_SOUGHT*$STRING32,
             CHAR_VALUE*$STRING256,DELIMETER*$STRING32;
   $REAL     VALUE,DEFAULT,VALUE_MIN,VALUE_MAX;
   $INTEGER  NVALUE,TYPE,NMIN,NMAX,ERROR_FLAG,ERROR_FLAGS,i_errors;
}
;

REPLACE {$GET_INPUT(#);} WITH { NMIN = {P1}; NMAX = {P1}; CALL GET_INPUT; }
;

REPLACE {$GET_INPUTS(#,#);} WITH { NMIN = {P1}; NMAX = {P2}; CALL GET_INPUT; }
;

"The following macro is used in the egs_init1 subroutine (in the file
"egs_utilities.mortran.  Here it is replaced by null so that we insist that
"the .egsinp file be opened with unit=5 (standard input) and the .egslog
"file (if required) be opened with unit=6 (standard output).  This is
"replaced by a search for available units in beamnrc_lib.mortran to avoid
"unit collisions with BEAM shared library sources

REPLACE {$AVAILABLE_UNIT(#,#)} WITH {;}

" The following two macros are defined so that if the nrcaux.mortran file
" is included in the configuration file these are defined at least.
" If the NRC statistics routine  SIGMA is to be used these must have realistic
" definitions in the user-code.

REPLACE {$MXDATA} WITH {1};
REPLACE {$STAT} WITH {2};

%E  "egsnrc.macros"
"============================================================================"
"   The following is related to use of the NRC auxilliary
"   routine xvgrplot which is called from some of the standard
"   NRC user-codes.
"
"   It is not an essential part of EGSnrc but is most easily defined here.
"============================================================================"
REPLACE{$PLTDIM} WITH {300};"Unique array dimension for XVGRPLOT and PLOTSN"
                        "Suppresses warnings from Intel compiler on Windows"
                   "when arrays have different dimensions in diff. routines"

%E   "egsnrc.macros"
"***************************************************************************"
"                                                                           "
"         EGSnrc internal Variance Reduction Macros                         "
"                                                                           "
"***************************************************************************"

REPLACE {;COMIN/EGS-VARIANCE-REDUCTION/;} WITH {;

  common/egs_vr/
    e_max_rr($MXREG), "max energy at which to do range rejection (RR)"
    prob_RR,          "probability for survival in R. Roulette"
    nbr_split,        "do brems splitting if > 1"
    i_play_RR,        "0=>don't play Russian Roulette,1=>play Russian Roulette"
    i_survived_RR,    "0=> all particles survive RR, n=> n partilces were"
                      "eliminated by RR in this interaction"
    n_RR_warning,     "a counter for user errors"
    i_do_rr($MXREG);  "0=>no RR, region by region, 1=>there is RR"
  $REAL          e_max_rr,prob_RR;
  $INTEGER       nbr_split,i_play_RR,i_survived_RR,n_RR_warning;
  $SHORT_INT     i_do_rr;
};

REPLACE {$MAX-RR-WARNING} WITH {50}

"This macro implements Russian Roulette (most useful  with brems splitting)"
"It is more efficient than having the user do it via AUSGAB since it avoids"
"considerable handling of the particles by ELECTR"
"The user must set i_play_RR (defaults to 0) and prob_RR"
"Both are in COMIN EGS-VARIANCE-REDUCTION"
""
"Note that this macro is called as $PLAY RUSSIAN ROULETTE WITH ELECTRONS..."
"Note also that subroutine pair has its own, internal version"

REPLACE {$PLAYRUSSIANROULETTEWITHELECTRONSFROM#;} WITH {;

  i_survived_RR = 0;   "flag all survive"
  ;IF( i_play_RR = 1 ) [
      IF( prob_RR <= 0 ) [
          IF( n_RR_warning < $MAX-RR-WARNING ) [
            n_RR_warning = n_RR_warning + 1;
            OUTPUT prob_RR;
  ('**** Warning, attempt to play Roussian Roulette with prob_RR<=0! ',g14.6);
          ]
      ]
      ELSE [
          ip = {P1};
          LOOP [     "handle all particles from p1 to np"
              IF( iq(ip) ~= 0 ) [   "i.e. charged particles"
                  $RANDOMSET rnno_RR;
                  IF( rnno_RR < prob_RR ) [ "particle survives"
                      wt(ip) = wt(ip)/prob_RR;
                      ip = ip + 1; "increase local pointer"
                  ]
                  ELSE [                    "particle killed"
                      ;i_survived_RR = i_survived_RR + 1;
                      ;IF(ip < np) [
                          "=>replace it with last particle on stack"
                          e(ip) = e(np); iq(ip) = iq(np); wt(ip) = wt(np);
                          u(ip) = u(np); v(ip) = v(np); w(ip) = w(np);
                      ]
                      np = np-1; "reduce stack by one=> particle gone"
                  ] "end of kill particle block"
              ] ELSE [ "this is a photon, leave it. Change pointer" ip = ip+1; ]
          ] UNTIL (ip > np);
          "loops until either np is decreased to ip, or ip increased to np"
          IF( np = 0 ) [ " we need at least one particle on the stack "
                         " so that the transport routines can exit properly"
              np = 1; e(np) = 0; iq(np) = 0; wt(np) = 0;
          ]
      ] "end of russian roulette block"
  ] "end of flag set block"
};

"*********************************************************************"
"  Stuff related to radiative corrections for Compton scattering      "
"                                                                     "
"  For now we exclude such corrections by default. They can be        "
"  included by adding the file rad_compton.mortran to the list of     "
"  files used to build EGSnrc just before egsnrc.mortran              "
"  The reason is that there is a fairly large amount of data needed   "
"  and this would be wasteful if the effect turns out to be small     "
"*********************************************************************"

REPLACE {$RADC_CHECK;} WITH {;}
REPLACE {$RADC_REJECTION;} WITH {;}
REPLACE {$RADC_WARNING;} WITH {;
    IF( radc_flag = 1 ) [
        $egs_warning(*,'You are trying to use radiative Compton corrections');
        $egs_info(*,'without having included rad_compton1.mortran');
        $egs_info('(a//)','Turning radiative Compton corrections OFF ...');
        radc_flag = 0;
    ]
};
REPLACE {$RADC_HATCH;} WITH {$RADC_WARNING;}
REPLACE {$COMIN-RADC-INIT;} WITH {
        ;COMIN/RAD_COMPTON,EGS-IO,COMPTON-DATA,MEDIA,PHOTIN,USEFUL/;
};
REPLACE {$COMIN-RADC-SAMPLE;} WITH {
        ;COMIN/RAD_COMPTON,RANDOM,STACK,USEFUL,EGS-IO/;
};


"*********************************************************************"
"  I/O, parallel processing, string manipulations, etc.
"*********************************************************************"

"how many chunks do we want to split the parallel run into
REPLACE {$N_CHUNKS} WITH {10};

" String manipulations, error messages, etc. "
REPLACE {$cstring(#)} WITH {{P1}(:lnblnk1({P1}))};
REPLACE {$set_string(#,#);} WITH {;
  DO i=1,len({P1}) [ {P1}(i:i) = {P2}; ] ;
};

REPLACE {$egs_debug(#,#);} WITH { write(i_log,{P1}) {P2}; };
REPLACE {$egs_fatal(#,#,#);} WITH {
  $warning('(/a)','***************** Error: ');
  $warning({P1},{P2});
  $warning('(/a)','***************** Quiting now.');
  $CALL_EXIT({P3});
};
REPLACE {$egs_fatal(#,#);} WITH {
  $warning('(/a)','***************** Error: ');
  $warning({P1},{P2});
  $warning('(/a)','***************** Quiting now.');
  $CALL_EXIT(1);
};
REPLACE {$egs_warning(#,#);} WITH {
  $warning('(/a)','***************** Warning: ');
  $warning({P1},{P2});
};
REPLACE {$warning(#,#);} WITH { write(i_log,{P1}) {P2}; };
REPLACE {$egs_info(#,#);} WITH { write(i_log,{P1}) {P2}; };
REPLACE {$declare_write_buffer;} WITH {;};


" Common block containing various directories, file names, etc. "
REPLACE {$mx_units} WITH {20};
REPLACE {$max_extension_length} WITH {10};
REPLACE {;COMIN/EGS-IO/;} WITH {;
  common /egs_io/ file_extensions($mx_units),
                  file_units($mx_units),
                  user_code,  "The name of the user code"
                  input_file, "The input file name with path but no extension"
                  output_file,"Same as above but for output"
                  pegs_file,  "The pegs file name with path and extension"
                  hen_house,  "The HEN_HOUSE directory"
                  egs_home,   "The EGS_HOME directory"
                  work_dir,   "The working directory within the user code dir."
                  host_name,  "The name of the host"
                  n_parallel, "if >0, number of parallel jobs"
                  i_parallel, "if >0, parallel job number"
                  first_parallel,"first parallel job (default is 1)"
                  n_max_parallel,"if parallel run, max. number of running jobs"
                  n_chunk,    "Histories per calculation chunk"
                  n_files,
                  i_input,    "unit no. for .egsinp if required"
                  i_log,      "unit no. for .egslog if required"
                  i_incoh,    "unit no. for Compton data"
                  i_nist_data, "unit no. for NIST data"
                  i_mscat,     "unit no. for multiple scattering data"
                  i_photo_cs,  "unit no. for photon cross-section data"
                  i_photo_relax, "unit no. for photon relaxation data"
                  xsec_out,     "switches on/off xsection file output"
                  is_batch,   "True for batch mode"
                  is_pegsless; "true if you are running without pegs file"
  character input_file*256, output_file*256, pegs_file*256,
            file_extensions*$max_extension_length,
            hen_house*128, egs_home*128, work_dir*128, user_code*64,
            host_name*64;
  $INTEGER  n_parallel, i_parallel, first_parallel,n_max_parallel,
            n_chunk, file_units, n_files,i_input,i_log,i_incoh,
            i_nist_data,i_mscat,i_photo_cs,i_photo_relax, xsec_out;
  $LOGICAL  is_batch,is_pegsless;
};

"The following macro sets the EGS_HOME directory               "
"The defualt implementation is to use the environment variable "
"EGS_HOME. But at the NRC EGS_HOME is set using the macro      "
"$EGS_HOME defined in machine.macros.                          "
REPLACE {$set_egs_home;} WITH {;
  $set_string(egs_home,' ');
  call getenv('EGS_HOME',egs_home);
};


" Initialization of various variables on a region-by-region basis "
" This is made a macro so that it can be replaced with a different "
" version for the C/C++ interface                                 "
REPLACE {$set-region-by-region-defaults;} WITH {;
DO i=1,$MXREG [
    ecut(i) = $GLOBAL-ECUT; pcut(i) = $GLOBAL-PCUT; "cut-off energies"
    ibcmp(i) = $IBCMP-DEFAULT;    "Compton "
    iedgfl(i) = $IEDGFL-DEFAULT;  "Relaxations"
    iphter(i) = $IPHTER-DEFAULT;  "photo-electron angular distribution"
    smaxir(i) = $MAX-SMAX;        "maximum step size"
    i_do_rr(i) = 0;               "range rejection flag"
    e_max_rr(i) = 0;              "`save' energy for range rejection"
    med(i) = 1;                   "default medium"
    rhor(i) = 0;                  "default mass density"
    iraylr(i) = $IRAYLR-DEFAULT;  "Rayleigh flag"
"Ali:photonuc, 1 line"
    iphotonucr(i) = $IPHOTONUCR-DEFAULT;  "photonuclear flag per region"]
};

" Make sure ecut and pcut are at least ae/ap and set default densities "
" This is made a macro so that it can be replaced with a different "
" version for the C/C++ interface                                 "
REPLACE {$adjust_rhor_ecut_pcut;} WITH {;
DO JR=1,$MXREG [
    MD=MED(JR);
    IF ((MD.GE.1).AND.(MD.LE.NMED))["IT IS LEGAL NON-VACUUM MEDIUM."
        ECUT(JR)=max(ECUT(JR),AE(MD));
        PCUT(JR)=max(PCUT(JR),AP(MD));
        "   USE STANDARD DENSITY FOR REGIONS NOT SPECIALLY SET UP"
        IF (RHOR(JR).EQ.0.0)[RHOR(JR)=RHO(MD);]
    ]
]
};

REPLACE {$adjust_pcut;} WITH {;
DO JR=1,$MXREG [
    MD=MED(JR);
    IF ((MD.GE.1).AND.(MD.LE.NMED))["IT IS LEGAL NON-VACUUM MEDIUM."
        PCUT(JR)=max(PCUT(JR),AP(MD));
    ]
]
};

REPLACE {$start_new_particle;} WITH { medium = med(irl); };

REPLACE {$electron_region_change;} WITH {
    ir(np) = irnew; irl = irnew; medium = med(irl);
};
REPLACE {$photon_region_change;} WITH { $electron_region_change; }

REPLACE {$declare_max_medium;} WITH {;};

REPLACE {$need_bound_compton_data(#);} WITH {
  {P1} = .false.;
  DO j=1,$MXREG [
      medium = med(j);
      IF( medium > 0 & medium <= nmed) [
          IF( ibcmp(j) > 0 ) [ {P1} = .true.; EXIT; ]
      ]
  ]
};

REPLACE {$need_relaxation_data(#);} WITH {
  {P1} = .false.;
  DO j=1,$MXREG [
      IF( iedgfl(j) > 0 & iedgfl(j) <= $MXELEMENT ) [ {P1} = .true.; EXIT; ]
  ]
};

REPLACE {$need_rayleigh_data;} WITH {;
DO J=1,NMED [
:LOOP-OVER-REGIONS:  DO I=1,$MXREG [
IF(IRAYLR(I).EQ.1.AND.MED(I).EQ.J) [
"REGION I = MEDIUM J AND WE WANT RAYLEIGH SCATTERING, SO"
"SET FLAG TO PICK UP DATA FOR MEDIUM J AND TRY NEXT MEDIUM."
IRAYLM(J)=1; EXIT :LOOP-OVER-REGIONS:;]
"END OF REGION-LOOP"]
"END OF MEDIA-LOOP"]
};

"Ali:photonuc, 1 block"
REPLACE {$need_photonuc_data;} WITH {;
IPHOTONUC=0;
DO J=1,NMED [
:LOOP-OVER-REGIONS-PHOTONUC: DO I=1,$MXREG [
IF(IPHOTONUCR(I).EQ.1.AND.MED(I).EQ.J) [
"REGION I = MEDIUM J AND WE WANT PHOTONUCLEAR, SO"
"SET FLAG TO PICK UP DATA FOR MEDIUM J AND TRY NEXT MEDIUM."
IPHOTONUCM(J)=1; IPHOTONUC=1; EXIT :LOOP-OVER-REGIONS-PHOTONUC:;]
"END OF REGION-LOOP"]
"END OF MEDIA-LOOP"]
};

REPLACE {$set_ecutmn;} WITH {
  ecutmn = 1e30;
  DO i=1,$MXREG [
      IF( med(i) > 0 & med(i) <= nmed ) [
                ecutmn = Min(ecutmn,ecut(i));
      ]
  ]
};

" default numer of media. "
REPLACE {$default_nmed} WITH {1}

REPLACE {$GET-PEGSLESS-XSECTIONS;} WITH {;
$egs_fatal('(a/a)',' Code cannot be run in pegsless mode.',
' Compile with required files and try again.');
;
}

REPLACE {$INIT-PEGS4-VARIABLES;} WITH {;}

REPLACE {$DECLARE-PEGS4-COMMON-BLOCKS;} WITH {;}

" The following macro is defined to fool the Intel Fortran compiler "
" version 8.0, which miscompiles init_spin when certain optimizations"
" are turned on and the code is run on an Athlon CPU. "
REPLACE {$FOOL-INTEL-OPTIMIZER(#) #;} WITH {;
    IF( fool_intel_optimizer ) [ write({P1},*) {P2}; ]
}
;