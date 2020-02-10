# three_webtext.py

Pyhton 3 script to use the webtext service of Ireland's Three mobile network.

## Usage
From a python terminal in the directory of three_webtext.py run the following to import the file. Note make sure the 
file is in the current working directory.

``import three_webtext``

On initial use the user data (phone number and password) will be entered and saved in a csv file in the same directory as the three_webtext file.
The sensitive data (password) is encrypted so it is not identifiable when looking at the csv file. The following line of code can be used to generate the user data.

``three_webtext.create_user_data()``

Note: the above doesn't need to be called as it is always called when the main function is run.
If the 'user_data.csv' file already exists then the user won't need to enter credentials.

If the incorrect details are entered use the following command to delete the user data:

``three_webtext.delete_user_data()``


There are two options to send a message:
1. Save the message in a file called message.txt in the same directory as the three_webtext.py
2. Pass the message to the main file as a string

Examples of both:
``three_webtext.main(sent_to='0871234567')``
``three_webtext.main(sent_to='0871234567', 'This is my message!')``



## Requirements
* Python 3.X
* requests
* re
* bs4 
* csv
* os
* pyDes

### Further notes
Three do not have a dedicated api (that I know of) that let us easily send webtexts.
The code provided here has to log into the three webtext website similar as to what is done on a computer.


When three make changes to their website this may mean this code needs to be adapted/ updated to work with the 
updated website.



