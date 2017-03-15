import time
import argparse
import win32net
import win32netcon
import win32security
from operator import itemgetter


parser = argparse.ArgumentParser()
parser.add_argument('--farsh', '-f', help='Farsh number')
parser.add_argument('--user', '-u', help='User', type=str)
parser.add_argument('--password', '-p', help='Password', type=str)
parser.add_argument('--domain', '-d', help='Domain', type=str)
args = parser.parse_args()

win32security.ImpersonateLoggedOnUser(win32security.LogonUser
                                      (args.user, args.domain,
                                       args.password, win32security.LOGON32_LOGON_NEW_CREDENTIALS,
                                       win32security.LOGON32_PROVIDER_WINNT50))

users, nusers, resume = win32net.NetUserEnum('vds{}.1cbit.ru'.format(args.farsh),
                                             2, win32netcon.FILTER_NORMAL_ACCOUNT)

sorted_users = sorted(users, key=itemgetter('name'))

#temp for inventory
with open('farsh-{}.txt'.format(args.farsh), "w") as ouf:
    for user in sorted_users:
        if user['name'].lower() not in 'администраторгостьrsyskrbtgt' :
            print(user['name'], 'последний раз заходил ' + time.strftime('%d.%m.%Y', time.localtime(int(user['last_logon']))), file=ouf)

#normal usage
#for user in sorted_users:
#    if user['name'].lower() not in 'администраторгостьrsyskrbtgt':
#        print(user['name'], 'последний раз заходил ' + time.strftime('%d.%m.%Y', time.localtime(int(user['last_logon']))))

#older month usage
#for user in sorted_users:
#    if user['name'].lower() not in 'администраторгостьrsyskrbtgt':
#        if time.time() - user['last_logon'] > 2592000:
#            print(user['name'], 'последний раз заходил ' + time.strftime('%d.%m.%Y', time.localtime(int(user['last_logon']))))
