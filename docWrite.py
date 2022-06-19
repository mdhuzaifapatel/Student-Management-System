# By Code Fellas
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import os

# Take info from user
# TODO - later we will take the info from database
name = input('Enter your Name: ').title()
# father = input('Enter your Father''s Name: ').title()
# clg = input('Enter your College: ').title()
# degree = input('Enter your Degree: ').upper()
# branch = input('Enter your Branch: ').upper()
# usn = input('Enter your USN: ').upper()
# dob = input('Enter your Date of Birth: ')

# Define the templates - assumes they are in the same directory as the code
bonafideTemplate = "Documents/bonafide.docx"

bonafide = MailMerge(bonafideTemplate)
print("Bonafide generated successfully")

# Info to be replaced
bonafide.merge(
    name=name,
    # clg=clg,
    # branch=branch,
    # usn=usn,
    # father=father,
    # degree=degree,
    # dob=dob,
    date='{:%d-%b-%Y}'.format(date.today()),
)

# Save the document
bonafide.write(f'StudentDocs\{name}_Bonafide.docx')


# Print the document
# win32api.ShellExecute(0, 'print', filename, None, '.', 0)

# printChoice = input('\nDo you want to print the document (Y/N):')
# if(printChoice == 'Y' or 'y'):
#     filename = f'D:\Learning\PROJECTS\Mini Project\Student Management System\StudentDocs\{name}_Bonafide.docx'
#     os.startfile(filename, "print")
# else:
#     exit()
