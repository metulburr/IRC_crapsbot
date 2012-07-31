import sys
import socket
import string
import time, os
import random

argv_flag = {'-c':None, '-h':None, '-p':None, '-k':None}
flag_help = {'-c':'channel ',
             '-h':'host',
             '-p':'port',
             '-k':'character to call on bot'}
show_help = 'Icorrect argument, "{} -help" for help'.format(sys.argv[0])

def licks():
    filer = open('/home/metulburr/Documents/licks.txt')
    lines = filer.readlines()
    for line in lines:
        line1 = line
    
    line1 = int(line1) + 1
    filer.close()
    
    filer = open('/home/metulburr/Documents/licks.txt', 'w')
    filer.write(str(line1))
    filer.close()
    return line1

def botfight():
    filer = open('/home/metulburr/Documents/botfight.txt')
    lines = filer.readlines()
    say = random.choice(lines)
    return say
        

class IRC_bot:
    def __init__(self, h=None, p=None, c=None, k=None):
        if h is None:
            self.host = "irc.freenode.net"
        else:
            self.host = h
        if p is None:
            self.port = 6667
        else:
            self.port = p
        if c is None:
            self.channel = '#metulburr'
        else:
            if c[:1] != '#':
                c = '#'+c
            self.channel = c
        if k is None:
            self.contact = '|'
        else:
            self.contact = k
            
        self.nick = "Craps_Dealer"
        self.ident = "Craps_Dealer"
        self.realname = "Craps_Dealer"
        self.readbuffer=""
        self.list_cmds = ['help', 'op','lick', 'die', 'binary_solo', 'caller', 'robgraves',
                          'insult', 'rules','roll', 'bet','bank', 'join', 'players','print_table', 'shooter','rollhist','table','sex', 'give', 'point','points','coded', 'leave']
        
        self.sock = self.irc_conn()
        self.wait_event()
    def say(self, string):
        self.sock.send('PRIVMSG {0} :{1}\n'.format(self.channel, string).encode())
        
    def irc_conn(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting to "{0}/{1}"'.format(self.host, self.port))
        sock.connect((self.host, self.port))
        print('sending NICK "{}"'.format(self.nick))
        sock.send("NICK {0}\r\n".format(self.nick).encode())
        sock.send("USER {0} {0} bla :{0}\r\n".format(
            self.ident,self.host, self.realname).encode())
        print('joining {}'.format(self.channel))
        sock.send(str.encode('JOIN '+self.channel+'\n'))
        return sock
        
    def wait_event(self):
        time.sleep(10) #wait to connect before starting loop
        game = Craps()
        while True:
            data=self.sock.recv(1042) #recieve server messages
            #print('data is...', data) #server message is output
            #data = bytes.decode(data) #data decoded
            #data = data.decode('utf-8')
            data = data.decode()
            data = data.strip('\n\r') #data stripped
            try:
                operation = data.split()[1]
                command = data.split()[3][1:]
            except IndexError:
                pass
            print(data)
            print(time.asctime(time.localtime(time.time())))
            
            if data[:4] == 'PING':
                self.sock.send('PONG\r\n'.encode())# + data.split()[1] + '\r\n').encode()
                time.sleep(2)
            if data[-42:] == 'KICK #robgraves Craps_Dealer :Craps_Dealer':
                self.sock.send(str.encode('JOIN '+self.channel+'\n'))
                self.say('Don\'t kick me')
            #give ops
            #/op metulburr
            username = data[:data.find('!')][1:]
            OP = ['metulburr','Awesome-O', 'robgraves','corp769',
                  'metulburr1', 'robgravesny', 'Optichip', 'OptiWork', 'OptiMobile']
            
            if operation == 'JOIN':
                if username == self.nick:
                    pass
                else:
                    self.say('Hello, {0} My commands are listed in {1}help'.format(username, self.contact))
                if username in OP:
                    #for person in OP:
                    self.sock.send('MODE {0} +o {1}\r\n'.format(self.channel, username).encode())
                    
                    
                '''for num in OP:
                    if username == num:
                        self.say('/mode {0} +o {1}'.format(self.channel,username))'''
                        
            if operation == 'QUIT' or operation == 'PART':
                try:
                    if game.balance[username]:
                        self.say(game.remove_user(username))
                except KeyError:
                    pass
                    
                
            #cmd = self.get_cmd(data, self.contact)
            user = self.get_user(data)
            #usesrname = self.get_username(data)
            username = data[:data.find('!')][1:]
            '''
            if user == 'supybot': #start bot war with#####################################
                self.say(botfight())'''
                
            #if cmd != None:
            #if command[:1] == self.contact:
            #if data.split().pop()[1:2] == self.contact:
            try:
                if data.split()[3][1:2] == self.contact: 
                    if command[1:] in self.list_cmds:
                        cmd = command[1:]
                        for valid_cmd in self.list_cmds:
                            if cmd == valid_cmd:
                                self.commands(cmd, user, username, data, game, operation)
                                
                        #if cmd not in self.list_cmds: #no longer needed
                            #self.sock.send("PRIVMSG {0} :{1} \n".format(
                                #self.channel,'{} is not one of my commands'.format(cmd)).encode())
                        print()
            except IndexError:
                pass
    def commands(self, cmd , user, username, data, game, operation):
        user = data[:data.find('!')][1:]
        if operation == 'QUIT':
            game.remove_user(username)
#op
        if cmd == 'op':
            OPS = ['metulburr', 'Awesome-O', 'robgraves']
            for user in OPS:
                self.sock.send('MODE {0} +o {1}\r\n'.format(self.channel, user).encode())
#leave
        if cmd == 'leave':
            try:
                if game.balance[username]:
                    self.say(game.remove_user(username))
                elif game.balance[username] == 0:
                    self.say(game.remove_user(username))
            except KeyError:
                pass
#point
        if cmd == 'point':
            self.say('Point is: {}'.format(game.point))
#points
        if cmd == 'points':
            points = ['dont_comepoint4', 'dont_comepoint5','dont_comepoint6','dont_comepoint8',
                      'dont_comepoint9', 'dont_comepoint10', 'comepoint4', 'comepoint5',
                      'comepoint6','comepoint8', 'comepoint9', 'comepoint10']
            tmp = []
            for point in points:
                if game.table[point]:
                    tmp.append(point)

            self.say('Points: {}'.format(tmp))

                    
#coded
        if cmd == 'coded':
            self.say(
                'Current bet locations coded are: pass, dont_pass,all placewins, all placeloses, hard4, hard6, hard8, hard10, easy2, easy3, easy11, easy12, field, any7, anycraps, C, E, big6, big8')
#die
        if cmd == 'die' and user =='metulburr':
            sys.exit()
            #self.sock.send('PRIVMSG {0} :{1} \n'.format(self.channel, '/quit').encode())
        elif cmd == 'die':
            self.say('only metulburr or an OP has the power to kill me')
            
        
        '''if cmd == 'craps' and game.gameon is False:
            game.balance[username] = 1000
            game.shooter = username
            game.gameon = True

            self.say(
                '***Craps game started*** {0}join to join, starting shooter: {1}'
                .format(self.contact, game.shooter))
        elif cmd == 'craps' and game.gameon is True:
            self.say('{}: A game is already in progress'.format(username))'''
#sex
        if cmd == 'sex':
            if game.gameon is True:
                for loc in game.table:
                    try:
                        if game.table[loc][username]:
                            pass
                        else:
                            return
                            #del game.table[loc][username]
                    except KeyError:
                        pass
                try:
                    if game.balance[username] == 0:
                        game.balance[username] = 200
                        self.say('{} had sex on the street for 200 dollars'.format(username))
                    else:
                        self.say('{}: You cannot have sex for money, if you have money'.format(username))
                except KeyError:
                    self.say('{}: You are not in the game! |join to join game .'.format(user))
            else:
                self.say(game.no_game(username))
#give
        if cmd == 'give' and data.split().pop() == ':{}give'.format(self.contact):
            self.say('{0}: {1}give [username] [amount]'.format(username, self.contact))
#give username amount
        elif cmd == 'give' and type(data.split()[4]) is str and type(data.split()[5]) is str:
            #self.say('cmd is: give')
            #self.say('reviever is: {}'.format(data.split()[4]))
            #self.say('amount is: {}'.format(data.split()[5]))
            try:
                reciever = data.split()[4]
                amt = int(data.split()[5])
            except ValueError:
                return
            try:
                if game.balance[username] >= amt:
                    try:
                        if game.balance[reciever]:
                            game.balance[username] -= amt
                            game.balance[reciever] += amt
                            self.say('{0} gave {1} {2}'.format(username, reciever, amt))
                    except KeyError:
                        self.say('{0}: {1} is not in the game'.format(username, reciever))
                else:
                    self.say('{}: You do not have enough to give that much'.format(username))
            except KeyError:
                self.say('{}: You are not in the game'.format(username))
                
                #if cmd == 'bet' and data.split().pop() == ':{}bet'.format(self.contact):
#bet
        if cmd == 'bet' and data.split().pop() == ':{}bet'.format(self.contact):
            tmp = ['big8','big6','pass','dont_come','dont_pass',
                   'field','come', 'C', 'E', 'placewin4', 'placewin5',
                    'placewin6','placewin8','placewin9','placewin10',
                        'placelose4','placelose5','placelose6',
                            'placelose8','placelose9','placelose10',
                                'hard4','hard6','hard8','hard10',
                                    'any7','horn','easy2','easy3',
                                        'easy11','easy12','anycraps','oddspass', 'oddsdont_pass']
            if game.gameon is True:
                self.say(
                    '{0}bet [amount] [bet location]  --to place bet; bet locations = {1}'.format(
                        self.contact, sorted(tmp)))
            else:
                self.say(game.no_game(username))
            #self.say(game.all_bets())
#bet amount location
        elif cmd == 'bet' and type(data.split()[4]) is str and data.split()[5] in game.all_bets():
            #if data.split().pop() == cmd:
                #self.say(game.bet_location)
            #elif data.split()[:-1] in game.bet_location:
            loc = data.split()[-1:][0]
            amt = data.split()[-2:-1][0]
            #bet = game.place_bet(username, amt, loc)

            try: #check if user exists
                print(game.balance[user]) 
            except KeyError:
                self.say('{}: You are not in the game! |join to join game.'.format(user))
                return
            try: #not valid amt
                amt = int(amt)
            except ValueError:
                self.say('{} is not a valid bet'.format(amt))
                return
            if amt > game.balance[user]: #not enough money
                self.say('{}: You do not have enough in your balance to place that bet'.format(user))
                return
            if user in game.table[loc].keys(): #user already placed bet on location
                self.say('{0}: You have a bet already on {1}; table to view the bets on the table'.format(user, loc))
                return
            
            #check locations for comeout
            comeout_false_only = ['placewin4', 'placewin5', 'placewin6',
                                  'placewin8', 'placewin9', 'placewin10',
                                  'placelose4','placelose5','placelose6',
                                  'placelose8','placelose9','placelose10',
                                  'come', 'dont_come', 'hard4', 'hard6', 'hard8',
                                  'hard10', 'big6', 'big8']
            if game.comeout is True:
                if loc in comeout_false_only:
                    self.say('{0}: You can only place a {1} bet after the come out roll'.format(username, loc))
                    return
            
            no_bet = ['dont_comepoint4', 'dont_comepoint5','dont_comepoint6','dont_comepoint8',
                      'dont_comepoint9', 'dont_comepoint10', 'comepoint4', 'comepoint5',
                      'comepoint6','comepoint8', 'comepoint9', 'comepoint10']
            
            if loc in no_bet:
                self.say('{0}: You cannot bet on {1}. You need to bet on come/dont_come'.format(
                    username, loc))
                return
            
            odds_bet = ['oddspass',  'oddsdont_pass']
            if loc in odds_bet:
                bet_type = loc[4:]
                if game.comeout is False:
                    if username in game.table[bet_type]:
                        if amt <= game.balance[username]:
                            game.table[loc] = {username:amt} # put bet in
                            #game.balance[username] -= amt # subtract from bank
                            #bet_amt = game.table[loc][username] #*= 3
                        else:
                            self.say('{0}: You do not have enough money'.format(username))
                            return
                            #not enough money
                    else:   
                        self.say('{0}: You do not have a bet on {1}'.format(username, bet_type))
                        return
                        #you dont have a bet on pass
                else:
                    self.say('{0}: You cannot bet on {1} before the comeout roll and a bet on {2}'.format(username, loc, bet_type))
                    return
                    #cannot bet on comeout roll
                
                
                
            #users bet is valid
            game.balance[user] -= amt #subtract bet amount from user
            if loc in game.table.keys():
                game.table[loc][user] = amt #place user and his amount on table 
            
            self.say('{0} places bet: {1} on {2}'.format(user, amt, loc))
            #self.say(bet)
#roll
        if cmd == 'roll' and username == game.shooter:
            dicetup = game.roll_dice()
            self.say('{0} rolled {1}: {2}'.format(game.shooter, sum(dicetup),dicetup))
            game.rollhist.append(dicetup)
            points = [4,5,6,8,9,10]
            craps = [2,3,12]
            natural = [7,11]
            dice = sum(dicetup)
            game.win_loss(dicetup)
            #self.say('TEST: point:{0}, comeout:{1}, comepoint:{2}'.format(
                #game.point, game.comeout, game.comepoint))
            if dice in natural: #7,11
                if game.comeout is True:
                    self.say('{} rolled, shooter wins'.format(dice))
                    game.resetpoint()
                elif dice == 7:
                    self.say('{} rolled, shooter loses'.format(dice))
                    game.resetpoint()
                    game.new_shooter()
                    self.say('New Shooter : {}'.format(game.shooter))
            elif dice in craps:
                if game.comeout is True:
                    self.say('{} rolled, shooter loses'.format(dice))
                    game.resetpoint()
                    game.new_shooter()
                    self.say('New Shooter : {}'.format(game.shooter))
            elif dice in points:
                if game.comeout is True:
                    game.point = dice
                    self.say('Point is: {}'.format(dice))
                    game.comeout = False #shoot for point until 7
                elif dice == game.point:
                    self.say('Point {} rolled, shooter wins'.format(dice))
                    game.resetpoint()
#roll nonshooter
        elif cmd == 'roll':
            self.say('{}: Only the shooter can roll'.format(username))
#help
        if cmd == 'help':
            self.say(self.list_cmds)
#robgraves
        elif cmd == 'robgraves':
            self.say('http://www.youtube.com/user/TheRobGraves?feature=mhee')
#binary_solo
        elif cmd == 'binary_solo':
            self.say('{}'.format('http://www.youtube.com/watch?v=KbQGaH6v3EY'))
#caller
        elif cmd == 'caller':
            self.say('Don\'t talk to me: {}'.format(username))
#insult
        elif cmd == 'insult':
            self.say(botfight())
#lick
        elif cmd == 'lick':
            self.say('pussy has been licked {} times'.format(licks()))
#rollhist
        elif cmd == 'rollhist':
            if game.gameon is True:
                self.say(game.rollhist)
            else:
                self.say(game.no_game(username))
#bank
        elif cmd == 'bank':
            self.say( game.show_balance(username))
#table
        elif cmd == 'table':
            #game.table[loc][user]
            '''for location in game.table.keys():
                if game.table[location]: #if not emtpy
                    game.table[location] = game.table[location]'''
            #if not game.table:
                #self.say('No bets on table')
            #else:
            tmp = dict()
            for key, value in game.table.items(): #show only filled from game.table is printed
                if game.table[key]:
                    tmp.update({key:value})
            self.say('Bets on the table = {}'.format(tmp))      
                #self.say('Bets on the table = {}'.format(game.table))
#join
        elif cmd == 'join':
            if game.gameon is True:
                if username not in game.balance.keys() or user not in game.balance.keys():
                    if game.shooter is None:
                        self.shooter = username
                    game.balance[username] = 1000
                    self.say('{} has joined the game'.format(username))
                    
                else:
                    self.say('{}: Nice Try. You are already in the game'.format(user))
            else:
                game.balance[username] = 1000
                game.shooter = username
                game.gameon = True
    
                self.say(
                    '***Craps game started*** {0}join to join, starting shooter: {1}'
                    .format(self.contact, game.shooter))
#players
        elif cmd == 'players':
            if game.gameon is True:
                self.say(game.show_all())
            else:
                self.say(game.no_game(username))
#print_table
        elif cmd == 'print_table':
            table = game.print_table()
            for line in table:
                self.say('{}'.format(line))
#shooter
        elif cmd == 'shooter':
            if game.gameon is False:
                self.say(game.no_game(username))
            else:
                self.say('shooter is: {0}'.format(game.shooter))
#rules
        elif cmd == 'rules':
            self.say('http://www.intercasino.com/help/rules/craps.shtml')

    def get_cmd(self, stringer, responder):
        '''returns string of index responder(+1) to end of stringer,
        if no responder returns None'''
        lister = []
        for char in stringer[::-1]:#start from end
            if char == responder:
                return ''.join(lister[::-1]) #unreverse
            lister.append(char)
        return None
    def get_user(self, stringer):
        start = stringer.find('~')
        end = stringer.find('@')
        user = stringer[start +1:end]
        return user
    def get_username(self, stringer):
        start = stringer.find(':')
        end = stringer.find('!')
        username = stringer[start +1:end]
        return username




def cmd_arg():
    '''return IRC_bot object based on values supplied by sys.argv'''
    arguments = sys.argv
    #print(arguments)
    if len(sys.argv) == 1:
        connect = IRC_bot()
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-help':
            print('')
            for key in flag_help.keys():
                print('\t{0} -- {1}'.format(key, flag_help[key]))
            sys.exit()
        else:
            print(show_help)
    else:
        h, p, c , k = None, None, None, None
        for flag in argv_flag.keys():
            for user_flag in arguments:
                if flag == user_flag:
                    index = arguments.index(user_flag)
                    value = arguments[index + 1]
                    argv_flag[flag] = value
        #print(argv_flag)
        connect = IRC_bot(h=argv_flag['-h'], p=argv_flag['-p'], c=argv_flag['-c'],
                          k=argv_flag['-k'])
    return connect




class Craps:
    def __init__(self, user=None):
        self.username = user
        self.gameon = False
        self.comeout = True
        self.comepoint = None
        self.balance = {} #user:balance
        self.secure_join = {} #username/useraddress
        self.shooter = ''
        self.user_location = {} #user bet location
        self.rollhist = []
        self.point = None
        #self.table = {}
        self.table = {'big8':{},'big6':{},'pass':{},'dont_come':{},'dont_pass':{},
            'field':{},'come':{}, 'C':{}, 'E':{}, 'placewin4':{}, 'placewin5':{},
                'placewin6':{},'placewin8':{},'placewin9':{},'placewin10':{},
                    'placelose4':{},'placelose5':{},'placelose6':{},
                        'placelose8':{},'placelose9':{},'placelose10':{},
                            'hard4':{},'hard6':{},'hard8':{},'hard10':{},
                                'any7':{},'horn':{},'easy2':{},'easy3':{},
                                    'easy11':{},'easy12':{},'anycraps':{},
                                        'comepoint4':{}, 'comepoint5':{},
                                            'comepoint6':{}, 'comepoint8':{},
                                                'comepoint9':{}, 'comepoint10':{},
                                                    'dont_comepoint4':{},
                                                        'dont_comepoint5':{},
                                                            'dont_comepoint6':{},
                                                                'dont_comepoint8':{},
                                                                    'dont_comepoint9':{},
                                                                        'dont_comepoint10':{}, 'oddspass':{},'oddsdont_pass':{}}

    def get_table(self): # not used yet
        for location in self.table.keys():
            if self.table[location]: #if not emtpy
                self.table[location] = self.table[location]
        return self.table
        
        
    def info(self, user):
        return '{0} balance: {1}'.format(user, balance[user])
    def all_bets(self):
        list(self.table.keys())
            
        #return self.bet_location
        return sorted(list(self.table.keys()))
    def roll_dice(self):
        num1 = random.randint(1,6)
        num2 = random.randint(1,6)
        return (num1, num2)
    def rollhist(self):
        return rollhist
    def place_bet(self, user, amt, loc):
        try: #check if user exists
            print(self.balance[user]) 
        except KeyError:
            return '{}: You are not in the game! |join to join game.'.format(user)
        try: #not valid amt
            amt = int(amt)
        except ValueError:
            return '{} is not a valid bet'.format(amt)
        if amt > self.balance[user]: #not enough money
            return  '{}: You do not have enough in your balance to place that bet'.format(user)
        if user in self.table[loc].keys(): #user already placed bet on location
            return '{0}: You have a bet already on {1}; table to view the bets on the table'.format(user, loc)
            
        #users bet is valid
        self.balance[user] -= amt #subtract bet amount from user
        if loc in self.table.keys():
            self.table[loc][user] = amt #place user and his amount on table 
        
        return '{0} places bet: {1} on {2}'.format(user, amt, loc)
    
    def win_loss(self, dice):
        def payoff(loc, times):
            for user in self.table[loc]: #for every user with a bet in that location
                #winnings = self.table[loc][user] * times
                winnings = int(self.table[loc][user]/1 * times)
                self.balance[user] += winnings
            self.table[loc] = {}


        dicesum = sum(dice)
        for location in self.table.keys(): #for every location that has a bet
            if location == 'pass':
                if self.comeout is True:
                    if dicesum == 7 or dicesum == 11:
                        payoff(location, 2/1)
                    elif dicesum == 2 or dicesum ==3 or dicesum ==12:
                        self.table[location] = {}
                else:
                    if dicesum == self.point:
                        payoff(location, 2/1)
                    elif dicesum == 7:
                        self.table[location] = {}
            if location == 'oddspass':
                if self.comeout is True:
                    if dicesum == 7 or dicesum == 11:
                        payoff(location, 3/1)
                    elif dicesum == 2 or dicesum ==3 or dicesum ==12:
                        self.table[location] = {}
                else:
                    if dicesum == self.point:
                        payoff(location, 3/1)
                    elif dicesum == 7:
                        self.table[location] = {}
            if location ==  'dont_pass':
                if self.comeout is True:
                    if dicesum == 2 or dicesum == 3:
                        payoff(location, 2/1)
                    elif dicesum == 7 or dicesum == 11:
                        self.table[location] = {}
                    elif dicesum == 12:
                        payoff(location, 1/1)
                else:
                    if dicesum == 7:
                        payoff(location, 2/1)
                    elif dicesum == self.point:
                        self.table[location] = {}
            if location == 'oddsdont_pass':
                if self.comeout is True:
                    if dicesum == 2 or dicesum == 3:
                        payoff(location, 2/1)
                    elif dicesum == 7 or dicesum == 11:
                        self.table[location] = {}
                    elif dicesum == 12:
                        payoff(location, 1/1)
                else:
                    if dicesum == 7:
                        payoff(location, 2/1)
                    elif dicesum == self.point:
                        self.table[location] = {}
                        
            '''try:   
                if self.table['comepoint' + str(dicesum)] != {}:
                    #if dicesum == self.comepoint:
                    payoff('comepoint' + str(dicesum), 2/1)
                elif dicesum == 7:
                    self.table['comepoint' + str(dicesum)] = {}
            except KeyError:
                pass #no user on spot, so it does not exits'''
            if location == 'come':
                if self.comeout is False:
                    if dicesum == 7 or dicesum == 11:
                        payoff(location, 2/1)
                    elif dicesum == 2 or dicesum == 3 or dicesum == 12:
                        self.table[location] = {}
                    else:
                        for key, value in self.table[location].items():
                            self.table['comepoint' + str(dicesum)] = {key:value}
                        self.table[location] = {}

            if location == 'comepoint4':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 4:
                    payoff(location, 2/1)
            if location == 'comepoint5':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 5:
                    payoff(location, 2/1)
            if location == 'comepoint6':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 6:
                    payoff(location, 2/1)
            if location == 'comepoint8':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 8:
                    payoff(location, 2/1)
            if location == 'comepoint9':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 9:
                    payoff(location, 2/1)
            if location == 'comepoint10':
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == 10:
                    payoff(location, 2/1)

            if location == 'dont_come':
                if self.comeout is False:
                    if dicesum == 2 or dicesum == 3:
                        payoff(location, 2/1)
                    elif dicesum == 7 or dicesum == 11:
                        self.table[location] = {}
                    elif dicesum == 12:
                        payoff(location, 1/1)
                    else:
                        for key, value in self.table[location].items():
                            self.table['dont_comepoint' + str(dicesum)] = {key:value}
                        self.table[location] = {}
                        
            if location == 'dont_comepoint4':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 4:
                    self.table[location] = {}
            if location == 'dont_comepoint5':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 5:
                    self.table[location] = {}
            if location == 'dont_comepoint6':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 6:
                    self.table[location] = {}
            if location == 'dont_comepoint8':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 8:
                    self.table[location] = {}
            if location == 'dont_comepoint9':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 9:
                    self.table[location] = {}
            if location == 'dont_comepoint10':
                if dicesum == 7:
                    payoff(location, 2/1)
                elif dicesum == 10:
                    self.table[location] = {}
                    
                        
            if location == 'placewin9' or location == 'placewin5':
                place = int(location[-1:])
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == place:
                    payoff(location, 7/5)
            if location == 'placewin4' or location == 'placewin10':
                place = int(location[-1:])
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == place:
                    payoff(location, 9/5)
            if location == 'placewin6' or location == 'placewin8':
                place = int(location[-1:])
                if dicesum == 7:
                    self.table[location] = {}
                elif dicesum == place:
                    payoff(location, 7/6)
                    
            if location == 'placelose9' or location == 'placelose5':
                place = int(location[-1:])
                if dicesum == 7:
                    payoff(location, 8/5)
                elif dicesum == place:
                    self.table[location] = {}
            if location == 'placelose4' or location == 'placelose10':
                place = int(location[-1:])
                if dicesum == 7:
                    payoff(location, 11/5)
                elif dicesum == place:
                    self.table[location] = {}
            if location == 'placelose6' or location == 'placelose8':
                place = int(location[-1:])
                if dicesum == 7:
                    payoff(location, 5/4)
                elif dicesum == place:
                    self.table[location] = {}
                    
            if location == 'hard4':
                if dice == (2,2):
                    payoff(location, 7/1)
                elif dicesum == 4 or dicesum == 7:
                    self.table[location] = {}
            if location == 'hard6':
                if dice == (3,3):
                    payoff(location, 9/1)
                elif dicesum == 6 or dicesum == 7:
                    self.table[location] = {}
            if location == 'hard8':
                if dice == (4,4):
                    payoff(location, 9/1)
                elif dicesum == 8 or dicesum == 7:
                    self.table[location] = {}
            if location == 'hard10':
                if dice == (5,5):
                    payoff(location, 7/1)
                elif dicesum == 10 or dicesum == 7:
                    self.table[location] = {}
            
            if location == 'easy2':
                if dicesum == 2:
                    payoff(location, 30/1)
                else:
                    self.table[location] = {}
            if location == 'easy3':
                if dicesum == 3:
                    payoff(location, 15/1)
                else:
                    self.table[location] = {}
            if location == 'easy11':
                if dicesum == 11:
                    payoff(location, 15/1)
                else:
                    self.table[location] = {}
            if location == 'easy12':
                if dicesum == 12:
                    payoff(location, 30/1)
                else:
                    self.table[location] = {}
            
            if location == 'field':
                if dicesum == 2 or dicesum == 12:
                    payoff(location, 2/1)
                elif dicesum == 3 or dicesum == 4 or dicesum == 9 or dicesum == 10 or dicesum == 11:
                    payoff(location, 1/1)
                else:
                    self.table[location] = {}
                    
            if location == 'any7':
                if dicesum == 7:
                    payoff(location, 4/1)
                else:
                    self.table[location] = {}
                    
            if location == 'anycraps':
                if dicesum == 2 or dicesum == 3 or dicesum == 12:
                    payoff(location, 7/1)
                else:
                    self.table[location] = {}
                    
            if location == 'E':
                if dicesum == 11:
                    payoff(location, 7/1)
                elif dicesum == 2 or dicesum == 3 or dicesum == 12:
                    self.table[location] = {}
            if location == 'C':
                if dicesum == 2 or dicesum == 3 or dicesum == 12:
                    payoff(location, 15/1)
                elif dicesum == 11:
                    self.table[location] = {}
                    
            if location == 'big6':
                if self.comeout is False:
                    if dicesum  == 6:
                        payoff(location, 7/6)
                    elif dicesum == 7:
                        self.table[location] = {}
            if location == 'big8':
                if self.comeout is False:
                    if dicesum == 8:
                        payoff(location, 7/6)
                    elif dicesum == 7:
                        self.table[location] = {}
                

            
                
                
        
        
    def show_balance(self, user):
        try:
            return '{0} balance: {1}'.format(user, self.balance[user])
        except KeyError:
            return '{}: You are not in the game! |join to join game.'.format(user)
    def show_all(self):
        return self.balance
    def add_user(self, username, user):
        self.secure_join[username] = user
        if username in self.balance.keys() or user in self.balance.keys():
            return 'double'
        #if username not in self.balance.keys():
            #return True
        else:
            return False
    def remove_user(self, username):
            #game.balance[username] = 1000
            #game.shooter = username
            #game.gameon = True
        try:
            if username == self.shooter:
                if len(self.balance) > 1:
                    self.new_shooter()
                else:
                    self.shooter = None
                    self.resetpoint()
                    self.gameon = False
            if self.balance[username]:
                del self.balance[username]
                for loc in self.table:
                    try:
                        if self.table[loc][username]:
                            del self.table[loc][username]
                    except KeyError:
                        pass
            return'{} has left the game'.format(username)
        except KeyError:
            return
        
    def print_table(self):
        filer = open('/home/metulburr/Documents/crap_table.txt')
        return filer.readlines()
    def no_game(self, username):
        return '{0}: No Game in progress. join to start a game\n'.format(username)
    def dicesum(self, dice):
        no_point = [2,3,7,11,12]
        craps = [2,3,12]
        natural = [7,11]
        
        dice = sum(dice)
        if dice not in no_point:
            self.point = dice
            return 'point'
        elif dice in craps:
            return 'craps'
        elif dice in natural:
            return 'natural'
    def new_shooter(self):
        if len(self.balance.keys()) > 1: #if more than one player
            listusers = list(self.balance.keys())
            shooterindex = listusers.index(self.shooter)# - 1
            try:
                self.shooter =  listusers[shooterindex + 1]
            except IndexError:
                self.shooter =  listusers[0]
            #return 'New Shooter : {}'.format(new_shooter)
    def resetpoint(self):
        #resetround
        self.comeout = True
        self.comepoint = None
        self.point = None
        self.rollhist = []
        
        
        
        


if __name__ == '__main__':
    connect = cmd_arg()
    try:
        print('channel: ', connect.channel)
        print('port: ', connect.port)
        print('host: ', connect.host)
        print('contact: ', connect.contact)
    except NameError:
        print(show_help)