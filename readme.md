# Converting "Ishmael" log files to .csv tables

With this python script you can convert the .ipf log files that the audio analysis software ISHMAEL (http://www.bioacoustics.us/ishmael.html) spits out, into an actually useful .csv table with timestamps and a column for each label. The .ipf file is structurd like this:

```
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_144000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:24:18.
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_154000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:24:29.
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_164000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:25:31.
Fin
Baleen
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_174000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:26:15.
Fin
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_184000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:26:44.
Fin
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_194000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:27:05.
Fin
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_204000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:27:10.
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_214000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:27:18.
StartFile: inputFile='D:\msc_project\Orkney2_data\2017\04_2017\170412_224000_AU_SO02.wav' localTimeNow=2021 Sep  7 15:27:42.
Humpback
```

For each of the logged sound files, any label that was added by the analyst is appended behind the filename and time of the edit.  What we want instead is a table with time in one column and the presence (1) or absence (0) of different call types (labels) as additional columns, such as this example:

| Time|Fin|Baleen|100-200Hz Upsweeps|Humpback|Minke|Check|40-Fin|Odontocetes|100-30Hz|Southern Rigth Whale|
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 2017-04-01  00:40:00|0|0|0| 0        |0| 0     | 0      | 0           |0 |0|
| 2017-04-01  06:40:00| 0    | 1      |0|0| 1     |0| 0      | 0           |0|0 |

This script converts any .ipf file into a .csv file, where each label gets its own column. To convert the .ipf file of your choice, change the "listlocation" string to the path/filename of your file and adjust the "timekey" string as indicated below:

```python

import numpy as np
import pandas as pd

listlocation=r"linn_filelist\Orkney_april17.ipf"
timekey='%y%m%d_%H%M%S_AU_SO02.wav'

df=pd.read_csv(listlocation,delimiter=' ',header=None)
df_oneline=pd.read_csv(listlocation,header=None)

ix_categories= np.where( df.iloc[:,0]!='StartFile:' )[0]
categories=pd.unique(df_oneline.iloc[ix_categories,0])

annotations=pd.DataFrame(columns=[ np.append('Time',categories) ])
ix_timestamp= np.where( df.iloc[:,0]=='StartFile:' )[0]

b= df.iloc[ix_timestamp,1].str.replace("'",'').str.split('\\',expand=True)
annotations['Time']=  pd.to_datetime( b.iloc[:,-1].values,format=timekey )

annotations.iloc[:,1:]=np.zeros([ annotations.shape[0] , annotations.shape[1]-1 ])

for i_cat in range(len(categories)):
    cat=categories[i_cat]
    ix=np.where( df_oneline.iloc[:,0]==cat )[0]
    for ixx in ix:
        c=ixx-ix_timestamp
        c[c<0]=999999
        ix_t=ix_timestamp[ np.argmin(c) ]
        timestamp=pd.to_datetime( df.iloc[ix_t,1].replace("'",'').split('\\')[-1]  ,format=timekey )
        ix_time=np.where( annotations['Time']==timestamp )[0]
        
        annotations.iloc[ix_time,i_cat+1]=1
        
annotations.to_csv(  listlocation[:-4]+'.csv',index=False)   
```

Adjust the "timekey" string so that the program recognizes the correct time-stamp. For example: `aural_%Y_%m_%d_%H_%M_%S.wav` or `%y%m%d_%H%M%S_AU_SO02.wav` Where %Y is year, %m is month, %d is day and so on.   Here is a list of the format strings:

| **Directive** | **Meaning**                                                  | **Example**              |
| ------------- | ------------------------------------------------------------ | ------------------------ |
| `%a`          | Abbreviated weekday name.                                    | Sun, Mon, ...            |
| `%A`          | Full weekday name.                                           | Sunday, Monday, ...      |
| `%w`          | Weekday as a decimal number.                                 | 0, 1, ..., 6             |
| `%d`          | Day of the month as a zero-padded decimal.                   | 01, 02, ..., 31          |
| `%-d`         | Day of the month as a decimal number.                        | 1, 2, ..., 30            |
| `%b`          | Abbreviated month name.                                      | Jan, Feb, ..., Dec       |
| `%B`          | Full month name.                                             | January, February, ...   |
| `%m`          | Month as a zero-padded decimal number.                       | 01, 02, ..., 12          |
| `%-m`         | Month as a decimal number.                                   | 1, 2, ..., 12            |
| `%y`          | Year without century as a zero-padded decimal number.        | 00, 01, ..., 99          |
| `%-y`         | Year without century as a decimal number.                    | 0, 1, ..., 99            |
| `%Y`          | Year with century as a decimal number.                       | 2013, 2019 etc.          |
| `%H`          | Hour (24-hour clock) as a zero-padded decimal number.        | 00, 01, ..., 23          |
| `%-H`         | Hour (24-hour clock) as a decimal number.                    | 0, 1, ..., 23            |
| `%I`          | Hour (12-hour clock) as a zero-padded decimal number.        | 01, 02, ..., 12          |
| `%-I`         | Hour (12-hour clock) as a decimal number.                    | 1, 2, ... 12             |
| `%p`          | Locale’s AM or PM.                                           | AM, PM                   |
| `%M`          | Minute as a zero-padded decimal number.                      | 00, 01, ..., 59          |
| `%-M`         | Minute as a decimal number.                                  | 0, 1, ..., 59            |
| `%S`          | Second as a zero-padded decimal number.                      | 00, 01, ..., 59          |
| `%-S`         | Second as a decimal number.                                  | 0, 1, ..., 59            |
| `%f`          | Microsecond as a decimal number, zero-padded on the left.    | 000000 - 999999          |
| `%z`          | UTC offset in the form +HHMM or -HHMM.                       |                          |
| `%Z`          | Time zone name.                                              |                          |
| `%j`          | Day of the year as a zero-padded decimal number.             | 001, 002, ..., 366       |
| `%-j`         | Day of the year as a decimal number.                         | 1, 2, ..., 366           |
| `%U`          | Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, ..., 53          |
| `%W`          | Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0. | 00, 01, ..., 53          |
| `%c`          | Locale’s appropriate date and time representation.           | Mon Sep 30 07:06:05 2013 |
| `%x`          | Locale’s appropriate date representation.                    | 09/30/13                 |
| `%X`          | Locale’s appropriate time representation.                    | 07:06:05                 |
| `%%`          | A literal '%' character.                                     | %                        |

 
