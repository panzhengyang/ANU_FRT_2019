import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

# Only data in this intervel will be considered
Tmax = 2011.33333333
Tmin = 2001.0

if len(sys.argv) < 3 :
    print('No enough input aurguments')
    print('Example usage is ')
    print('python3 -W ignore this_file_name.py grace_time_series_data gps_time_series_data')     # ignore warnings
    sys.exit()

grace_data_file_name = sys.argv[1]
gps_data_file_name = sys.argv[2]

min_data_points = 3

try:
    '''
    grace_data = np.genfromtxt(grace_data_file_name , 
            delimiter = ' ' ,
            skip_header = 1)    # skipping one line because the time stamp for first line has error
    #'''
    #print(grace_data.shape)
    '''
    gps_data = np.genfromtxt(gps_data_file_name ,
            skip_header = 1 ,
            delimiter = None) 
    # The data has variable number of spaces seperating columns
    # None is the default setting which means any white space is taken as delimiter which include single space, many spaces, tab or many tab etc
    #'''
    #print(gps_data.shape)
    #'''
    grace_data = pd.read_csv(grace_data_file_name,
            delimiter=' ',
            header=None,
            skiprows=0)
            #dtype=float)
    grace_data = np.asarray(grace_data)
    #'''
    
    #''' For NGL
    gps_data = pd.read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=1)
    gps_data = np.asarray(gps_data)

    Tgps , EIgps , EFgps , NIgps , NFgps , UIgps , UFgps , ESgps , NSgps , USgps = gps_data[:,2].astype(float) , gps_data[:,7].astype(float) , gps_data[:,8].astype(float) , gps_data[:,9].astype(float) , gps_data[:,10].astype(float) , gps_data[:,11].astype(float) , gps_data[:,12].astype(float) , gps_data[:,14].astype(float) , gps_data[:,15].astype(float) , gps_data[:,16].astype(float) 

    Egps = EIgps.astype(float) + EFgps.astype(float)
    Ngps = NIgps.astype(float) + NFgps.astype(float)
    Ugps = UIgps.astype(float) + UFgps.astype(float)

    # Converting units m to mm
    Egps , Ngps , Ugps = Egps*1000 , Ngps*1000 , Ugps*1000 
    #'''

    ''' For MIT

    gps_data = pd.read_csv(gps_data_file_name,
            delimiter='\s+',
            header=None,
            skiprows=0)
    gps_data = np.asarray(gps_data)
    #print(gps_data.shape)

    Tgps , Elon , Nlat , Ugps , ESgps , NSgps , USgps = gps_data[:,0].astype(float) , gps_data[:,18].astype(float) , gps_data[:,17].astype(float) , gps_data[:,19].astype(float) , gps_data[:,24].astype(float) , gps_data[:,23].astype(float) , gps_data[:,25].astype(float)  

    Earth_radius = 6.3781*10**6     # meters
    # Converting units mm
    Egps , Ngps , Ugps = Earth_radius*np.sin(Nlat*np.pi/180)*(Elon-Elon[0])*1000 , Earth_radius*((Nlat-Nlat[0])*np.pi/180.)*1000 , Ugps*1000 

    #'''


    # time north north_sigma east east_sigma up up_sigma 
    Tgrace , Ngrace , NSgrace , Egrace , ESgrace , Ugrace , USgrace = grace_data[:,0].astype(float) , grace_data[:,1].astype(float) , grace_data[:,2].astype(float) , grace_data[:,3].astype(float), grace_data[:,4].astype(float) , grace_data[:,5].astype(float) , grace_data[:,6].astype(float)
    
    # Selecting the GRACE data which is only in a particular time intervel 
    grace_select_flag = np.logical_and((Tgrace > Tmin),(Tgrace < Tmax))
    
    Tgrace = Tgrace[grace_select_flag]
    Ngrace = Ngrace[grace_select_flag]
    NSgrace = NSgrace[grace_select_flag]
    Egrace = Egrace[grace_select_flag]
    ESgrace = ESgrace[grace_select_flag]
    Ugrace = Ugrace[grace_select_flag]
    USgrace = USgrace[grace_select_flag]

    # DTgrace is the difference of consecutive elements in Tgrace
    DTgrace = np.diff(Tgrace)       # length of DTgrace is one less than Tgrace

    # Forward Tgrace and Backward Tgrace are the time bounds(upper and lower) of at each Tgrace for taking mean of GPS data at each GRACE data
    # DTgrace is padded since it is one element less than Tgrace
    FTgrace = Tgrace + np.pad(DTgrace,(0,1),'constant',constant_values = (0,0)) / 2          
    BTgrace = Tgrace - np.pad(DTgrace,(1,0),'constant',constant_values = (0,0)) / 2

    # I don't know how to avoid this loop

    ReTgps = Tgrace
    ReNgps = Ngrace * 0
    ReEgps = Egrace * 0
    ReUgps = Ugrace * 0
    ReNSgps = NSgrace * 0
    ReESgps = ESgrace * 0
    ReUSgps = USgrace * 0
    data_flag = (Tgrace * 0).astype(bool)

    for i in range(np.size(Tgrace)):
        
        selection_flag = np.logical_and( Tgps <= FTgrace[i] , Tgps > BTgrace[i] ) 
        data_flag[i] = selection_flag.sum()     # gets boolean elements, not integers 
        
        #print(selection_flag.sum())
        #print(data_flag[i])

        ReNgps[i] = Ngps[ selection_flag ].mean()
        ReEgps[i] = Egps[ selection_flag ].mean()
        ReUgps[i] = Ugps[ selection_flag ].mean()
        
        ReNSgps[i] = NSgps[ selection_flag ].mean()
        ReESgps[i] = ESgps[ selection_flag ].mean()
        ReUSgps[i] = USgps[ selection_flag ].mean()


    if data_flag.sum() > min_data_points :
        # selecting data only when both GRACE and GPS are simultaniously available
        ReTgps = ReTgps[data_flag]
        ReNgps = ReNgps[data_flag]
        ReEgps = ReEgps[data_flag]
        ReUgps = ReUgps[data_flag]
        ReNSgps = ReNSgps[data_flag]
        ReESgps = ReESgps[data_flag]
        ReUSgps = ReUSgps[data_flag]

        ReTgrace = Tgrace[data_flag]
        ReNgrace = Ngrace[data_flag]
        ReEgrace = Egrace[data_flag]
        ReUgrace = Ugrace[data_flag]
        ReNSgrace = NSgrace[data_flag]
        ReESgrace = ESgrace[data_flag]
        ReUSgrace = USgrace[data_flag]

        # Removing mean value from GPS data
        # This process should not be done initially as mean should be calculated based on data when GRACE data is not present
        # This needs further inspection
        ReNgps = ReNgps - ReNgps.mean()
        ReEgps = ReEgps - ReEgps.mean()
        ReUgps = ReUgps - ReUgps.mean()

        # Removing mean value from GRACE data
        # This process is already done for the data but the mean is for all the original data and now not all the initial data is being used
        # This needs further inspection
        ReNgrace = ReNgrace - ReNgrace.mean()
        ReEgrace = ReEgrace - ReEgrace.mean()
        ReUgrace = ReUgrace - ReUgrace.mean()

        # Calculating the RMS values  
        rms_gps = np.sqrt(np.mean((ReUgps)**2))
        rms_grace = np.sqrt(np.mean((ReUgrace)**2))
        Udiff = ReUgrace - ReUgps
        rms_diff = np.sqrt(np.mean((Udiff)**2))

        # Calcualting the slope of time series which can be helpful to study Glacial Isostatic Adjustments
        slope_gps = ( ( ReTgps-ReTgps.mean() ).dot( ReUgps-ReUgps.mean() ) )/( ( ReTgps-ReTgps.mean() ).dot( ReTgps-ReTgps.mean() ) )
        slope_grace = ( ( ReTgrace-ReTgrace.mean() ).dot( ReUgrace-ReUgrace.mean() ) )/( ( ReTgrace-ReTgrace.mean() ).dot( ReTgrace-ReTgrace.mean() ) )
        slope_diff = ( ( ReTgps-ReTgps.mean() ).dot( Udiff-Udiff.mean() ) )/( ( ReTgps-ReTgps.mean() ).dot( ReTgps-ReTgps.mean() ) )

        corr_coeff = np.corrcoef(ReUgps,ReUgrace)[1,0]      # corrcoef function gives 2*2 matrix and any element except diagonal ones are equal to corr coef
        
        print(data_flag.sum(),'\t',"{0:.6f}".format(rms_gps),'\t',"{0:.6f}".format(rms_grace),'\t',"{0:.6f}".format(rms_diff),'\t',"{0:.6f}".format(slope_gps),'\t',"{0:.6f}".format(slope_grace),'\t',"{0:.6f}".format(slope_diff),'\t',"{0:.6f}".format(corr_coeff),'\t','0')

    else : 
        #print('no sufficient data available')
        print(data_flag.sum(),'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',2.0,'\t','1')
except:
    print(-1.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',0.0,'\t',3.0,'\t','2')
