import win32net
import win32netcon
import time
import win32security
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--farsh', '-f', help='Farsh number')
parser.add_argument('--user', '-u', help='User', type=str)
parser.add_argument('--password', '-p', help='Password', type=str)
parser.add_argument('--domain', '-d', help='Domain', type=str)
args = parser.parse_args()

win32security.ImpersonateLoggedOnUser(win32security.LogonUser(args.user, args.domain, args.password, win32security.LOGON32_LOGON_NEW_CREDENTIALS, win32security.LOGON32_PROVIDER_WINNT50))

users, nusers, resume = win32net.NetUserEnum('vds{}.1cbit.ru'.format(args.farsh), 2, win32netcon.FILTER_NORMAL_ACCOUNT)
for user in users:
    if user['name'] != 'Администратор' and user['name'] != 'Гость' and user['name'] != 'rsys':
        print(user['name'], 'последний раз заходил ' + time.ctime(user['last_logon']))