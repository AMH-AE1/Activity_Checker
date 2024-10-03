import os ;from os import system
import subprocess, time, re; from colorama import Fore

clear = lambda: system("cls")
clear()
print ("""
 █████╗ ███╗   ███╗██╗  ██╗         █████╗ ███████╗
██╔══██╗████╗ ████║██║  ██║        ██╔══██╗██╔════╝
███████║██╔████╔██║███████║        ███████║█████╗  
██╔══██║██║╚██╔╝██║██╔══██║        ██╔══██║██╔══╝  
██║  ██║██║ ╚═╝ ██║██║  ██║███████╗██║  ██║███████╗
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
""")

system('title Activity Checker')

ques = '['+Fore.MAGENTA+'?'+Fore.WHITE+'] '
cc = '['+Fore.CYAN+'*'+Fore.WHITE+'] '
era = '['+Fore.YELLOW+'!'+Fore.WHITE+'] '

print(f'                                     Coded by {Fore.RED}https://www.instagram.com/amh_ae_{Fore.WHITE}')


print (f'\n{cc}1. To gather System activities, Last logins, Start-Up programs/files and the users on this PC.')
print (f'{cc}2. To create a new user.')
print (f'{cc}3. To delete an exisitng user.')
user_choice1 = str(input('\nChoose the operation >> '))

# Get the username of the current user
username = os.getlogin()
# gets the working directory
working_dir = os.getcwd()

paths = (
    "C:\\Windows\\System32",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Windows",
    f"C:\\Users\\{username}\\Downloads"
)
def location_check():
    for path in paths:
        if working_dir.startswith(paths):
            print ('This is a restricted working directory, please change the directory and try again')
            exit()
        if working_dir == f"C:\\Users\\{username}\\Desktop":
            print ('Please change the directory, this program cant run on Desktop! ')
            exit()
location_check()

def activity_retriever():
    ret = r'''
    @echo off

    REM Set the directory for the output files
    set "output_dir=%CD%\txt files"

    REM Create the directory if it doesn't exist
    if not exist "%output_dir%" (
        mkdir "%output_dir%"
    )

    REM Overwrite the output files if they exist
    echo. > "%output_dir%\output.txt"
    echo. > "%output_dir%\task scheduler.txt"
    echo. > "%output_dir%\login_events.txt"

    REM Export the registry key to a temporary file
    reg export "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" "%output_dir%\temp_output.txt"

    REM Append the user list to the output file, overwriting if necessary
    net user >> "%output_dir%\output.txt"
    REM Append the message to the output.txt file
    echo *****THESE ARE THE USERS ON THIS PC***** >> "%output_dir%\output.txt"
    echo -------------------------------------------------------------------------------------------------------------------- >> "%output_dir%\output.txt"
    echo. >> "%output_dir%\output.txt"
    REM Creates a new blank line

    REM Append the contents of the temp registry export to the final output file, overwriting if necessary
    type "%output_dir%\temp_output.txt" >> "%output_dir%\output.txt"
    REM Append the message to the output.txt file
    echo *****THESE ARE THE PROCESSES THAT START AUTOMATICALLY WHEN THE WINDOWS BOOTS***** >> "%output_dir%\output.txt"
    echo -------------------------------------------------------------------------------------------------------------------- >> "%output_dir%\output.txt"
    echo. >> "%output_dir%\output.txt"
    REM Creates a new blank line

    REM Clean up the temporary file
    del "%output_dir%\temp_output.txt"

    REM Append the output of the PowerShell command to the same output file
    powershell -command "Get-LocalUser | Select-Object Name, @{Name='LastLogon';Expression={($_.LastLogon -as [datetime]).ToLocalTime()}} | Format-Table -AutoSize | Out-File -Append '%output_dir%\output.txt'"
    REM Append the message to the output.txt file
    echo *****THIS IS THE LOGIN DATES AND TIME***** >> "%output_dir%\output.txt"
    echo -------------------------------------------------------------------------------------------------------------------- >> "%output_dir%\output.txt"
    echo. >> "%output_dir%\output.txt"
    REM Creates a new blank line

    echo The output has been saved to "%output_dir%\output.txt"

    REM Exports the tasks schedule so you can analyze it, overwriting if necessary
    schtasks /query /fo table /v > "%output_dir%\task scheduler.txt"
    echo The task scheduler has been saved to "%output_dir%\task scheduler.txt"

    REM Exports the login activity (excluding default users) using XML filter for Event ID 4624 (Logon successes)
    powershell -Command "Start-Process powershell -ArgumentList '-Command $XmlFilter = ''<QueryList><Query><Select Path=''Security''>*[System[(EventID=4624) and (EventData[Data[@Name=''TargetUserName''] != ''Administrator'' and Data[@Name=''TargetUserName''] != ''DefaultAccount'' and Data[@Name=''TargetUserName''] != ''Guest'' and Data[@Name=''TargetUserName''] != ''WDAGUtilityAccount'')]]</Select></Query></QueryList>''; Get-WinEvent -FilterXml $XmlFilter | Select-Object -Property TimeCreated, @{Name=''UserName'';Expression={$.Properties[5].Value}} | Out-File -Force ''%output_dir%\login_events.txt'' ' -WindowStyle Hidden"

    REM Append the message to the login_events.txt file
    echo *****IF YOU SEE THIS EMPTY THEN THERE IS NO SUSPICIOUS LOGINS ON YOUR PC***** >> "%output_dir%\login_events.txt"

    echo The login events (excluding default users) have been saved to "%output_dir%\login_events.txt"
    REM Self-delete section
    echo Delayed deletion...
    timeout /t 10 >nul
    start "" cmd /c del "%~f0"
    exit
    '''
    with open('Activity Retriever.bat','w') as reg:
        reg.write(ret)
    batch_file = 'Activity Retriever.bat'
    subprocess.run([batch_file], check=True, capture_output=True, text=True)

    


def output_organizer():
    global users
    try:    
        result_file = 'result.txt'
        
        with open(f"{working_dir}\\txt files\\output.txt", "r") as file:
            content = file.readlines()

        users = []
        capture = False
        pattern = r'\s{2,}'


        # Loop through lines to extract user accounts
        for line in content:
            # Check if we are in the relevant section by detecting the start line
            if "User accounts for" in line:
                capture = True
                continue

            # When we reach the dashed separator, start capturing usernames
            if "-------------------------------------------------------------------------------" in line:
                capture = True
                continue

            # Stop capturing when we encounter the end of the user accounts section
            if "The command completed successfully." in line:
                break

            # Capture usernames in the relevant section
            if capture and line.strip():
                # Split the line by two or more spaces to separate usernames
                parts = re.split(pattern, line.strip())
                users.extend(parts)  # Add all parts as usernames

        
        # Write the result to result.txt
        with open(f"{working_dir}\\txt files\\result.txt", "w") as result_file:
            result_file.write("\n".join(users))

        print(f"Extracted users: {users}")
    except Exception as e:
        print (e)

def user_remover():
            response = input ('\n*****WARNING : IF YOU DELETED THE MAIN USER YOU CANT GET IT BACK AND ALL DATA WILL BE LOST!!!*****\nAre you sure you want to continue? (y/n) >> ').lower()
            if response == 'y':
                user_to_delete = input('\nEnter the username you want to delete (please make sure you type it correctly) >> ')
                if user_to_delete not in users:
                    print ('The username you have entered does not exist! ')
                else:
                        print('\nPrepairing Removing File ...')

                        # Specify the username to delete
                        username_to_delete = user_to_delete  # Replace with the actual username

                        
                        batch_content = f"""
                        
                        :: BatchGotAdmin
                        :-------------------------------------
                        REM  --> Check for permissions
                        IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
                            >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
                        ) ELSE (
                            >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
                        )

                        REM --> If error flag set, we do not have admin.
                        if '%errorlevel%' NEQ '0' (
                            echo Requesting administrative privileges...
                            goto UACPrompt
                        ) else ( goto gotAdmin )

                        :UACPrompt
                            echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
                            set params= %*
                            echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

                            "%temp%\getadmin.vbs"
                            del "%temp%\getadmin.vbs"
                            exit /B

                        :gotAdmin
                            pushd "%CD%"
                            CD /D "%~dp0"
                        :--------------------------------------

                        REM Delete the user account
                        set "username={username_to_delete}"  
                        net user "%username%" /delete

                        echo User account "%username%" has been deleted.
                        REM Self-delete section
                        echo Delayed deletion...
                        timeout /t 2 >nul
                        start "" cmd /c del "%~f0"
                        exit
                        """

                        # Specify the file name
                        batch_file_path = 'USER DELETE.bat'

                        # Create and write to the batch file
                        with open(batch_file_path, 'w') as file:
                            file.write(batch_content)
            elif response == 'n':
                exit()
            else:
                print('Please enter \'y\' for yes or \'n\' for no.')       

def user_creator():
    new_username = input('Enter a name for the new user >> ') 

    password_check = input(f'\n{ques}Do you want to set a Password to the new user? (y/n) >> ').lower()
    if password_check == 'y':
        password = input('Please enter a password for the new user >> ')
        batch_content = f"""
        :: BatchGotAdmin
        :-------------------------------------
        REM  --> Check for permissions
        IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
            >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
        ) ELSE (
            >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
        )

        REM --> If error flag set, we do not have admin.
        if '%errorlevel%' NEQ '0' (
            echo Requesting administrative privileges...
            goto UACPrompt
        ) else ( goto gotAdmin )

        :UACPrompt
            echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
            set params= %*
            echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

            "%temp%\getadmin.vbs"
            del "%temp%\getadmin.vbs"
            exit /B

        :gotAdmin
            pushd "%CD%"
            CD /D "%~dp0"
        :--------------------------------------

        REM Create users
        net user {new_username} {password} /add

        echo User {new_username} has been created.
        REM Self-delete section
        echo Delayed deletion...
        timeout /t 2 >nul
        start "" cmd /c del "%~f0"
        exit
        """
    elif password_check == 'n':

        batch_content = f"""
        :: BatchGotAdmin
        :-------------------------------------
        REM  --> Check for permissions
        IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
            >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
        ) ELSE (
            >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
        )

        REM --> If error flag set, we do not have admin.
        if '%errorlevel%' NEQ '0' (
            echo Requesting administrative privileges...
            goto UACPrompt
        ) else ( goto gotAdmin )

        :UACPrompt
            echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
            set params= %*
            echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

            "%temp%\getadmin.vbs"
            del "%temp%\getadmin.vbs"
            exit /B

        :gotAdmin
            pushd "%CD%"
            CD /D "%~dp0"
        :--------------------------------------

        REM Create users
        net user {new_username} /add

        echo User {new_username} has been created.
        REM Self-delete section
        echo Delayed deletion...
        timeout /t 2 >nul
        start "" cmd /c del "%~f0"
        exit
        """

    # Specify the file name
    batch_file_path = 'USER CREATOR.bat'

    # Create and write to the batch file
    with open(batch_file_path, 'w') as file:
        file.write(batch_content)

def temporary_users():
    global users
    batch_temp = '''
    net user >> temp.txt
    '''
    with open('temp.bat','w') as temp:
        temp.write(batch_temp)
    batch_file = 'temp.bat'
    subprocess.run([batch_file], check=True, capture_output=True, text=True)
    time.sleep(5)
    with open("temp.txt", "r") as file:
        content = file.readlines()

        users = []
        capture = False
        pattern = r'\s{2,}'


        # Loop through lines to extract user accounts
        for line in content:
            # Check if we are in the relevant section by detecting the start line
            if "User accounts for" in line:
                capture = True
                continue

            # When we reach the dashed separator, start capturing usernames
            if "-------------------------------------------------------------------------------" in line:
                capture = True
                continue

            # Stop capturing when we encounter the end of the user accounts section
            if "The command completed successfully." in line:
                break

            # Capture usernames in the relevant section
            if capture and line.strip():
                # Split the line by two or more spaces to separate usernames
                parts = re.split(pattern, line.strip())
                users.extend(parts)  # Add all parts as usernames

        
        # Write the result to result.txt
        with open("temp_file.txt", "w") as result_file:
            result_file.write("\n".join(users))

        print(f"\nExtracted users: {users}")
    

# End of the script to keep the terminal open
def main():
    if user_choice1 == '1':
        print('Gathering ...')
        try:
            activity_retriever()
            output_organizer()
            print('Done! Check the same directory for the txt files!')
        except Exception as a:
            print(f'There is an error, {a}')
            exit()
    elif user_choice1 == '2':
        try:
            user_creator()
            print('Creating File ...')
            time.sleep(3)
            print('User Creating File Is Ready! Double click the USER CREATOR.bat (you might need to restart your PC to take effect).')
        except Exception as a:
            print(f'There is an error, {a}')
            exit()
    elif user_choice1 == '3':
        try:
            temporary_users()
            user_remover()
            time.sleep(3)
            print('\nUser Removing File Is Ready! Double click the USER DELETE.bat (you might need to restart your PC to take effect).')
            time.sleep(1)
            print ('Deleting Temporary Files ...')
            os.remove('temp.txt')
            os.remove('temp_file.txt')
            os.remove('temp.bat')
        except Exception as a:
            print(f'There is an error, {a}')
            exit()

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")  # Keeps the terminal open
