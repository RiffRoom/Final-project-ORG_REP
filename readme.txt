

-- ENVIRONMENT VARIABLE LAYOUT --

Create a .env file, it is already added to git ignore, then follow this layout for the declaration of your variables.

'DB_USER'=''
'DB_PASS'=''
'DB_HOST'=''
'DB_PORT'=''
'DB_NAME'=''

----------------------------------

-- AWS CREDENTIALS --

Put these in your .env file, it is very important that these keys are not lost, and not displayed to the public. 
You will prompted to download a .csv file with your keys, I recommend you do this, and store them in an encrypted folder on your computer
If you lose your keys, they are gone.

'AWS_ACCESS_KEY_ID'=''
'AWS_SECRET_ACCESS_KEY'=''
'AWS_SESSION_TOKEN'=''