# api-script

A python script that creates multiple instances at a time testing different security zones with diferent OSnames and hostnames. 
the payload will stay the same with the exception of hostname, customer hostname, zonename.

## Details

OSname will vary (60% linux and 40% windows) we will use:
"osName": "Red Hat Enterprise 7.4",
"osName": "Windwos 2016 DE",

hostname will be same name with different ending numbers to tell instances apart 
ex. securityzonetest1, securityzonetest2, securityzonetest3, etc...

securityZone will be entered in the zoneNames array for every run. (we are in the process of optimizing this)

## Acceptance criteria
The script will successfully make multiple API calls to an API at a time with the above details and get different security zones tested.

## How to use

-Clone or Download api-script repository into local machine

-Make sure to have latest version of python with the required libraries (in this case: request, python-dotenv)

-Update the zoneNames array with the desired amount of zonenames

-run `Python3 httpScript.py`
