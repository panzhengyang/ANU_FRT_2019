
The .tar.gz file has the spherical harmonic coefficients' anomaly at different time periods. 

tar -ztvf GRGS_anomaly.tar.gz 
is used to list all the file names in the .tar.gz file. The output also includes the details along with just the file names

tar -ztvf GRGS_anomaly.tar.gz > list.txt 
is used to save all the output from the previous command into a text file

the shell script extracts the file names from the output of previous command and saves them in another file called names.txt 
