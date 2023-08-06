import pickle, os
from time import sleep
import webbrowser
import sys
import time
import random
import pyfiglet
#from licensing.models import *
#from licensing.methods import Key, Helpers
from colorama import init, Fore
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError, ChatAdminRequiredError
from telethon.errors.rpcerrorlist import ChatWriteForbiddenError, UserBannedInChannelError, UserAlreadyParticipantError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import UserStatusRecently
#from telethon.sessions import StringSession

if not os.path.exists('./sessions'):
    os.mkdir('./sessions')

try:
  from lolpython import lol_py 
  import pyfiglet
except:
  os.system("pip install lolpython")
  os.system("pip install pyfiglet")
init()

n = Fore.RESET
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = lg + '[' + w + 'i' + lg + ']' + rs
error = lg + '[' + r + '!' + lg + ']' + rs
success = w + '[' + lg + '*' + w + ']' + rs
INPUT = lg + '[' + cy + '~' + lg + ']' + rs
plus = w + '[' + lg + '+' + w + ']' + rs
minus = w + '[' + lg + '-' + w + ']' + rs

re="\033[1;31m"
gr="\033[1;32m"
wi="\033[1,35m"

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

def banner():

  os.system("clear")

  result = pyfiglet.figlet_format("    Ramex ", font = "slant"  )#chintoo
  lol_py(result) 
  lol_py('         Version: 1.3 | Author: @Annex_xD\n')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    banner()
    print(lg+'[1] Add new accounts'+n)
    print(lg+'[2] Member Adder'+n)
    print(lg+'[3] Filter all banned accounts'+n)
    print(lg+'[4] Delete specific accounts'+n)
    print(lg+'[5] Subscribe To TrickyAbhi'+n)
    print(lg+'[6] Group Spam'+n)
    print(lg+'[7] Exit'+n)
    a = int(input('\nEnter your choice: '))
    if a == 1:
        new_accs = []
        with open('vars.txt', 'ab') as g:
            number_to_add = int(input(f'\n{lg} [~] Enter number of accounts to add: {r}'))
            for i in range(number_to_add):
                phone_number = str(input(f'\n{lg} [~] Enter Phone Number: {r}'))
                parsed_number = ''.join(phone_number.split())
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)
            print(f'\n{lg} [i] Saved all accounts in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                c = TelegramClient(f'sessions/{number}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
                c.start(number)
                c(JoinChannelRequest('@The_Hacking_Zone'))
                time.sleep(2)
                c(JoinChannelRequest('@Techno_Trickop'))
                c.disconnect()
            print(f'{lg}[+] Login successful')
            input(f'\n Press enter to goto main menu...')

        g.close()
    elif a == 2:
        accounts = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break

# create sessions(if any) and check for any banned accounts
# TODO: Remove code input(just to check if an account is banned)
        print('\n' + info + lg + ' Checking for banned accounts...' + rs)
        for a in accounts:
            phn = a[0]
            print(f'{plus}{grey} Checking {lg}{phn}')
            clnt = TelegramClient(f'sessions/{phn}', 3910389, '86f861352f0ab76a251866059a6adbd6')
            clnt.connect()
            banned = []
            if not clnt.is_user_authorized():
                try:
                    clnt.send_code_request(phn)
                    print('OK')
                except PhoneNumberBannedError:
                    print(f'{error} {w}{phn} {r}is banned!{rs}')
                    banned.append(a)
            for z in banned:
                accounts.remove(z)
                print(info+lg+' Banned account removed[Remove permanently using manager.py]'+rs)
            time.sleep(0.5)
            clnt.disconnect()


        print(info+' Sessions created!')
        clr()
        banner()
# func to log scraping details(link of the grp to scrape
# and current index) in order to resume later
        def log_status(scraped, index):
            with open('status.dat', 'wb') as f:
                pickle.dump([scraped, int(index)], f)
                f.close()
            print(f'{info}{lg} Session stored in {w}status.dat{lg}')
    

        def exit_window():
            input(f'\n{cy} Press enter to exit...')
            clr()
            banner()
            sys.exit()

# read user details
        try:
    # rquest to resume adding
            with open('status.dat', 'rb') as f:
                status = pickle.load(f)
                f.close()
                lol = input(f'{INPUT}{cy} Resume scraping members from {w}{status[0]}{lg}? [y/n]: {r}')
                if 'y' in lol:
                    scraped_grp = status[0] ; index = int(status[1])
                else:
                    if os.name == 'nt': 
                        os.system('del status.dat')
                    else: 
                        os.system('rm status.dat')
                    scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
                    index = 0
        except:
            scraped_grp = input(f'{INPUT}{cy} Public/Private group link to scrape members: {r}')
            index = 0
# load all the accounts(phonenumbers)
        accounts = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break

        print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
        number_of_accs = int(input(f'{INPUT}{cy} Enter number of accounts to use: {r}'))
        print(f'{info}{cy} Choose an option{lg}')
        print(f'{cy}[0]{lg} Add to public group')
        print(f'{cy}[1]{lg} Add to private group')
        choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
        if choice == 0:
            target = str(input(f'{INPUT}{cy} Enter public group link: {r}'))
        else:
            target = str(input(f'{INPUT}{cy} Enter private group link: {r}'))
        print(f'{grey}_'*50)
#status_choice = str(input(f'{INPUT}{cy} Do you wanna add active members?[y/n]: {r}'))
        to_use = [x for x in accounts[:number_of_accs]]
        for l in to_use: accounts.remove(l)
        with open('vars.txt', 'wb') as f:
            for a in accounts:
                pickle.dump(a, f)
            for ab in to_use:
                pickle.dump(ab, f)
            f.close()
        sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None{w}]: {r}'))
#print(f'{info}{lg} Joining group from {w}{number_of_accs} accounts...')
#print(f'{grey}-'*50)
        print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')
        adding_status = 0
        approx_members_count = 0
        for acc in to_use:
            stop = index + 60
            c = TelegramClient(f'sessions/{acc[0]}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
            print(f'{plus}{grey} User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
            c.start(acc[0])
            acc_name = c.get_me().first_name
            try:
                if '/joinchat/' in scraped_grp:
                    g_hash = scraped_grp.split('/joinchat/')[1]
                    try:
                        c(ImportChatInviteRequest(g_hash))
                        print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
                    except UserAlreadyParticipantError:
                        pass 
                else:
                    c(JoinChannelRequest(scraped_grp))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
                scraped_grp_entity = c.get_entity(scraped_grp)
                if choice == 0:
                    c(JoinChannelRequest(target))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                    target_entity = c.get_entity(target)
                    target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
                else:
                    try:
                        grp_hash = target.split('/joinchat/')[1]
                        c(ImportChatInviteRequest(grp_hash))
                        print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                    except UserAlreadyParticipantError:
                        pass
                    target_entity = c.get_entity(target)
                    target_details = target_entity
            except Exception as e:
                print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group')
                print(f'{error} {r}{e}')
                continue
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
    #c.get_dialogs()
            try:
                members = []
                while_condition = True
                my_filter = ChannelParticipantsSearch('')
                offset = 0
                i = 1
                while while_condition:
                    participants = c(GetParticipantsRequest(channel=scraped_grp,  offset= offset, filter = my_filter, limit=200, hash=0))
                    members.extend(participants.users)
                    offset += len(participants.users)
                    members += (participants.users)
                    if len(participants.users) < 1 :
                        while_condition = False
            except Exception as e:
                print(f'{error}{r} Couldn\'t scrape members')
                print(f'{error}{r} {e}')
                continue
            approx_members_count = len(members)
            assert approx_members_count != 0
            if index >= approx_members_count:
                print(f'{error}{lg} No members to add!')
                continue
            print(f'{info}{lg} Start: {w}{index}')
    #adding_status = 0
            peer_flood_status = 0
            for user in members[index:stop]:
                index += 1
                if peer_flood_status == 10:
                    print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
                    break
                try:
                    if choice == 0:
                        c(InviteToChannelRequest(target_details, [user]))
                    else:
                        c(AddChatUserRequest(target_details.id, user, 42))
                    user_id = user.first_name
                    target_title = target_entity.title
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
            #print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep 1 second')
                    adding_status += 1
                    print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
                    time.sleep(sleep_time)
                except UserPrivacyRestrictedError:
                    print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted Error')
                    continue
                except PeerFloodError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
                    peer_flood_status += 1
                    continue
                except ChatWriteForbiddenError:
                    print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
                    if index < approx_members_count:
                        log_status(scraped_grp, index)
                    exit_window()
                except UserBannedInChannelError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
                    break
                except ChatAdminRequiredError:
                    print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
                    continue
                except UserAlreadyParticipantError:
                    print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User is already a participant')
                    continue
                except FloodWaitError as e:
                    print(f'{error}{r} {e}')
                    break
                except ValueError:
                    print(f'{error}{r} Error in Entity')
                    continue
                except KeyboardInterrupt:
                    print(f'{error}{r} ---- Adding Terminated ----')
                    if index < len(members):
                        log_status(scraped_grp, index)
                    exit_window()
                except Exception as e:
                    print(f'{error} {e}')
                    continue
#global adding_status, approx_members_count
        if adding_status != 0:
            print(f"\n{info}{lg} Adding session ended")
        try:
            if index < approx_members_count:
                log_status(scraped_grp, index)
                exit_window()
        except:
            exit_window()
    elif a == 3:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r+'[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                phone = str(account[0])
                client = TelegramClient(f'sessions/{phone}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        #client.sign_in(phone, input('[+] Enter the code: '))
                        print(f'{lg}[+] {phone} is not banned{n}')
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' is banned!'+n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg+'Congrats! No banned accounts')
                input('\nPress enter to goto main menu...')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Phone = a[0]
                        pickle.dump([Phone], k)
                k.close()
                print(lg+'[i] All banned accounts removed'+n)
                input('\nPress enter to goto main menu...')

    elif a == 4:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choose an account to delete\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[0]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        phone = str(accs[index][0])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Account Deleted{n}')
        input(f'\nPress enter to goto main menu...')
        f.close()
    elif a == 5:
        # thanks to github.com/th3unkn0n for the snippet below
        url = 'https://youtube.com/c/TrickyAbhi'
        brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
        cmd = brw % url
        os.system(cmd)
        print('opened by command:', repr(cmd), end='\n\n')
        
    elif a == 6:
     usernameset = str(input(f'{cy} Your Group Username {r}'))
     sendmsg = str(input(f'{cy} What Message you Want to Send {r}'))
     repeatg = int(input(f'{cy} How many times you want to Send Message {r}'))
     sleepss = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None{w}]: {r}'))
     times_to_repeat = repeatg
     while times_to_repeat > 0:
        accounts = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break

# create sessions(if any) and check for any banned accounts
# TODO: Remove code input(just to check if an account is banned)
        for a in accounts:
            phn = a[0]
            print(f'{plus}{grey} Sending Message from {lg}{phn}')
            clnt = TelegramClient(f'sessions/{phn}', 3910389, '86f861352f0ab76a251866059a6adbd6')
            clnt.connect()
            clnt(JoinChannelRequest(usernameset))
            clnt.send_message(usernameset, sendmsg)
            clnt.disconnect()
            time.sleep(sleepss)
            times_to_repeat -= 1

    elif a == 7:
        clr()
        banner()
        exit()
