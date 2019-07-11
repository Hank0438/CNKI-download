'''
import subprocess

subprocess.call(['C:\\Temp\\a b c\\Notepad.exe', 'C:\\test.txt'])
'''
import os, shutil

'''
if os.path.isdir('data'):
    #刪除資料夾
    shutil.rmtree('data')
#新增空資料夾
os.mkdir('data')
'''

f = open('patent', 'r', encoding='utf-8')

error_lines = []

for line in f.readlines()[:20]:
    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
    line = line.strip()
    print('下載: ', line)
    try:
        os.system("python main.py " + line)
    except OSError as e:
        print('OSError: ', e)
        error_lines.append(line)
    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')

eq = open('errorQuery', 'w', encoding='utf-8')
for err in error_lines:
    eq.write(err + '\n')