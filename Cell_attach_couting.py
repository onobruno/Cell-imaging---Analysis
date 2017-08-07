'''
Created on 2 Aug 2017

@author: brunoandradeono
'''

import pandas as pd
import os
import xlrd
import csv
import numpy 
import numpy as np
from pandas.io.parsers import read_csv
import matplotlib.pyplot as plt
import xlsxwriter

plt.rcdefaults()
import os
import platform
import subprocess

import subprocess

from subprocess import call

from subprocess import call


" This programm were made thinking in pre-processing of imageJ. It is not previously necessary to create the file on the path"


def cels_per_image(path):
    # This function returns an array with number of cells per image and cell density per image.
    
    Nbr_memb = int(raw_input('Enter the number of membranes: '))
    # Number of membranes to be analyzed
        
    cell_number_list = []
    cell_density_list = []
    mean_area_list = []
    std_area_list = []
        
    for y in range(1,Nbr_memb+1):
        for x in range(1,6):
        
            x = str(x) 
        
            y = str(y)
        
            newFile1 = pd.read_csv( path + "Processed images/Processed_m"+ y +"."+ x +".tif.csv")
            # This will read the csv file - Make sure to name it with some pattern
    
            cell_number = newFile1["Area"].count()
                    
            cell_number_list  = cell_number_list  + [cell_number]
            #This will count how many cells there is
                    
            cell_density = cell_number/0.009709037
                    
            cell_density_list = cell_density_list + [cell_density]
            # This gives cell density (Cells/cm2)
                
            mean_area = newFile1["Area"].mean()
                    
            mean_area_list = mean_area_list + [mean_area]
            # This will give the mean area of the column
                    
            std_area = newFile1["Area"].std()
                    
            std_area_list = std_area_list + [std_area]
            # This will give the standard deviation
    
                
        a = {'Cells number':cell_number_list, 'Cell Density':cell_density_list}
        
        cell_per_image = pd.DataFrame(a)
        
        cell_per_image = cell_per_image[['Cells number', 'Cell Density']]
        # the sort of the columns
        #print cell_per_image.tail(5) 
        #check up step
        
    return cell_per_image
    
      

def cels_per_membrane(df1):
    
    list = df1['Cell Density']
    # Make a list with all cell densities of all images

    Nbr_images_per_membrane = int(raw_input('Enter the number of images per membranes: '))
    
    Nbr_images_per_membrane = len(list)
    
    avg_memb_list = []
    
    std_memb_list = []
    
    per_cem_list = []
    
    for x in range(0,Nbr_images_per_membrane,5):
        
        # The range run the 5 in 5 because we have 5 images from each sample
        memb_array = numpy.array([list[x+0],list[x+1],list[x+2],list[x+3],list[x+4]])
        # This make a array for the 
        #print list[x+0],list[x+1],list[x+2],list[x+3],list[x+4],list[x+5]
        
        avg_memb = numpy.mean(memb_array)
        # This return the average cell density of each membrane
        
        avg_memb_list = avg_memb_list + [avg_memb]
        # This add the mean to a list
        
        std_memb = numpy.std(memb_array,ddof=1)
        # This adds the standard deviation of cell density of each membrane
        
        std_memb_list = std_memb_list + [std_memb]
        # This return the list of average cell density of each membrane
        
        per_cem = (std_memb/avg_memb)*100
        # how much this represent compared to mean
        
        per_cem_list = per_cem_list + [per_cem]
        
    a = {'Cell Density per membrane (cells/cm2)':avg_memb_list,'Std deviation per membrane':std_memb_list, 'Std/cell density (%)':per_cem_list}
    #print a 
    
    cell_per_memb = pd.DataFrame(a)
    #print cell_per_memb.head()    
        
    cels_per_membrane = pd.concat([df1,cell_per_memb], axis=1)
    # This function will join the new columns
    #print df2.tail()
    #print df2.head()
    
    return cels_per_membrane

# print cels_per_membrane(cels_per_image()).head()

def CD_per_condition(df2):
    
    cd_memb = df2["Cell Density per membrane (cells/cm2)"]
    # Make a list with all cell densities of all images
    # print cd_memb
    
    cd_memb_std = df2["Std deviation per membrane"]
    
    cd_memb_rel_error = df2["Std/cell density (%)"] 
    
    Nbr_memb = len(cd_memb)
    
    avg_membS_list = []
    
    std_membS_list = []
    
    cd_membraneS_std_list = [] 
    
    std_error_membS_list = []
    
    mean_of_std_list = []
    
    rel_error_list = []
    
    for x in range(0,Nbr_memb,6):
    
        cd_membraneS = numpy.array([cd_memb[x+0],cd_memb[x+1],cd_memb[x+2],cd_memb[x+3],cd_memb[x+4],cd_memb[x+5]])
        cd_membraneS_std = numpy.array([cd_memb_std[x+0],cd_memb_std[x+1],cd_memb_std[x+2],cd_memb_std[x+3],cd_memb_std[x+4],cd_memb_std[x+5]])
        cd_membraneS_rel_error = numpy.array([cd_memb_rel_error[x+0],cd_memb_rel_error[x+1],cd_memb_rel_error[x+2],cd_memb_rel_error[x+3],cd_memb_rel_error[x+4],cd_memb_rel_error[x+5]])
        # Group of means, std and relative error
        
        cd_membraneS_std1 = (numpy.sqrt(sum(numpy.square(cd_membraneS_std))))/len(cd_membraneS_std)
        cd_membraneS_std_list = cd_membraneS_std_list + [cd_membraneS_std1]
        # Error propagation 
                          
        avg_membS = numpy.mean(cd_membraneS,0)
        avg_membS_list = avg_membS_list + [avg_membS]
        # This return avg_membranes from 6 samples
        
        std_membS = numpy.std(cd_membraneS,0)
        std_membS_list = std_membS_list + [std_membS]
        # This return the std of the mean from 6 samples
        
        std_error_membS = numpy.std(cd_membraneS,0)/numpy.sqrt(len(cd_membraneS))
        std_error_membS_list = std_error_membS_list + [std_error_membS]
        # This return the std error from 6 samples
        
        mean_of_std = numpy.mean(numpy.array([cd_memb_std[x+0],cd_memb_std[x+1],cd_memb_std[x+2],cd_memb_std[x+3],cd_memb_std[x+4],cd_memb_std[x+5]]))
        mean_of_std_list = mean_of_std_list + [mean_of_std]
        # This return the mean of the std from 6 samples
        
        rel_error_membS = numpy.mean(cd_membraneS_rel_error,0)
        rel_error_list = rel_error_list + [rel_error_membS]
        # This return the mean of the rel_error from 6 samples
        
    a = {'Average Cell Density (cells/cm2)':avg_membS_list,'Std deviation of the averages':std_membS_list,'Average of the std':mean_of_std_list, 'Error propagation':cd_membraneS_std_list, 'Std error': std_error_membS_list, 'Relative error (%)': rel_error_list}
    
    cell_per_cond = pd.DataFrame(a)
    #print cell_per_memb.head()    
    
    cell_per_cond = cell_per_cond[['Average Cell Density (cells/cm2)', 'Std deviation of the averages','Std error','Average of the std', 'Error propagation', 'Relative error (%)']]
            
    cels_per_condition = pd.concat([df2,cell_per_cond], axis=1)
    # This function will join the new columns
   
    #print df2.tail()
    #print df2.head()
    
    return cels_per_condition

   
def cell_attach_percent(df3):
    
    "Cell Attachment (%)"
    
    
    avg_cd = df3["Average Cell Density (cells/cm2)"]

    percent_cd = ( avg_cd/avg_cd[0]) *100
    
    " Cell attachment (%) + and -"

    percent_cd_list = []
    
    for s in range(0,len(avg_cd),2):
   
        a = (avg_cd[s]/avg_cd[0])*100
        b = (avg_cd[s+1])/avg_cd[1]*100
        percent_cd_list = percent_cd_list + [a] + [b]
    
    #percentage of cell attachment
    
    "Standard deviation (SD) of the averages"
    
    std_cd = df3["Std deviation of the averages"]
    #print std_cd
    
    error_bar_sd = []
    
    for x in range(0, len(std_cd)):
        
        a = (std_cd[x]/avg_cd[0])*100
        error_bar_sd = error_bar_sd +[a]
        
    " Standard Error (SE) (%) "
    
    std_error = df3['Std error']
    
    error_bar_se = []
    # error related of standard error deviation 
    
    for y in range(0,len(std_cd)):
        
        a = (std_error[y]/avg_cd[0])*100
        error_bar_se = error_bar_se +[a]
    
    " Error propagation (%) "
    
    error_ppg = df3['Error propagation']
    
    error_ppg_list =[]
        
    for z in range(0,len(std_cd)):
        
        a = (error_ppg[z]/avg_cd[0])*100
        error_ppg_list = error_ppg_list +[a]    
        
    "Mean of stds (%)"
    
    avg_std = df3['Average of the std'] 
    
    avg_std_list = []
    
    for t in range(0,len(avg_std),2):
   
        a = (avg_std[t]/avg_cd[0])*100
        b = (avg_std[t+1])/avg_cd[1]*100
        avg_std_list = avg_std_list + [a] + [b]
   
    
    a = {'Cell attachment (%)': percent_cd, 'Cell attachment (%) + and -':percent_cd_list,'Std deviation (%)':error_bar_sd,'Std error (%)':error_bar_se, 'Error propagation (%)':error_ppg_list, 'Mean of stds (%)':avg_std_list}
    #print a
    
    cell_percent = pd.DataFrame(a)

    cell_percent = cell_percent[['Cell attachment (%)','Std deviation (%)','Std error (%)','Cell attachment (%) + and -', 'Mean of stds (%)','Error propagation (%)' ]]
        
    cels_attach_percent = pd.concat([df3,cell_percent], axis=1)
    
    #exc_name = str(raw_input("Type here the name of the excel file:"))
    
    return cels_attach_percent

path = "/users/brunoandradeono/desktop/Cell Attachment/Rep 5 - 30.04.17/"
df_final = cell_attach_percent(CD_per_condition(cels_per_membrane(cels_per_image(path))))
df_final.to_excel(path + "Condition/All columns.xlsx")


