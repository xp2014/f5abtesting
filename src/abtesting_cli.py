# -*- coding:utf-8 -*-
from abtesting import *


# User raw_input the BIG-IP information
bigip_ip = raw_input('Please raw_input the IP address of the BIG-IP:')
bigip_username = raw_input('Please raw_input the BIG-IP username:')
bigip_password = raw_input('Please raw_input the BIG-IP password:')
# bigip_password = getpass.getpass('Password: ')

# Connect to the BigIP
mgmt = ManagementRoot(bigip_ip, bigip_username, bigip_password)

# List all virtual servers
vs_list = mgmt.tm.ltm.virtuals.get_collection()
print "Here is the list of Virtual Server in " + bigip_ip + ":"
vs_name_list = []
for vs in vs_list:
    vs_name_list.append(vs.name)

# Ask user raw_input vs_name
loop = True
vs_name = ''
while loop:
    for i in range(len(vs_name_list)):
        print vs_name_list[i]
    print 'Which virtual server do you want to do ab testing?'
    vs_name = raw_input(bigip_ip + '/>')
    if vs_name in vs_name_list:
        loop = False

commands = {'region2b_remove': '    remove region from B pool',
            'region2b_assign': '    assign region to B pool',
            'pool_b_mbr_add': '     add member into B pool',
            'pool_b_mbr_del': '     del member from B pool',
            'init_irules': '        create iRules for ab testing',
            'init_ip2region': '     load IP address to region mapping table into F5',
            'help': '               print this screen',
            'deploy': '             deploy f5abtesting for virtual server',
            'undeploy': '           undeploy f5abtesting for virtual server',
            'exit': '               exit script'}

print "Available commands:"
for (k, v) in commands.items():
    print "%s :" % k, v

# Loop waiting for user raw_input ...
loop = True
while loop:
    command_string = raw_input(bigip_ip + '/' + vs_name + '>')
    command_argvs = command_string.split()
    # print command_argvs
    if len(command_argvs) != 0:
        if command_argvs[0].lower() == 'init_irules':
            print 'init_irules'
            if len(command_argvs) > 1:
                init_irules(mgmt, vs_name, command_argvs[1])
            else:
                print 'Please input the file name '
        elif command_argvs[0].lower() == 'init_ip2region':
            print 'init_ip2region'
            if len(command_argvs) > 1:
                init_ip2region(mgmt, vs_name, command_argvs[1])
            else:
                print 'Please input the file name '
        elif command_argvs[0].lower() == 'region2b_remove':
            print 'region2b_remove'
            if len(command_argvs) > 1:
                region2b_remove(mgmt, vs_name, command_argvs[1])
            else:
                print 'Please input the region name '
        elif command_argvs[0].lower() == 'region2b_assign':
            print 'region2b_assign'
            if len(command_argvs) > 1:
                region2b_assign(mgmt, vs_name, command_argvs[1])
            else:
                print 'Please input the region name '
        elif command_argvs[0].lower() == 'pool_b_mbr_add':
            print 'pool_b_mbr_add'
            if len(command_argvs) > 1:
                if valid_pool_member(command_argvs[1]):
                    pool_b_mbr_add(mgmt, vs_name, command_argvs[1])
                else:
                    print command_argvs[1] + ' is not a valid pool member'
            else:
                print 'Please input the pool member address and port '
        elif command_argvs[0].lower() == 'pool_b_mbr_del':
            print 'pool_b_mbr_del'
            if len(command_argvs) > 1:
                if valid_pool_member(command_argvs[1]):
                    pool_b_mbr_del(mgmt, vs_name, command_argvs[1])
                else:
                    print command_argvs[1] + ' is not a valid pool member'
            else:
                print 'Please input the pool member address and port '
        elif command_argvs[0].lower() == 'help' or command_argvs[0].lower() == 'h' or command_argvs[0].lower() == '?':
            for (k, v) in commands.items():
                print "%s :" % k, v
        elif command_argvs[0].lower() == 'deploy':
            print 'deploy'
            deploy(mgmt,vs_name)
        elif command_argvs[0].lower() == 'undeploy':
            print 'undeploy'
            if len(command_argvs) > 1:
                undeploy(mgmt, vs_name, 'cleanup')
            else:
                undeploy(mgmt, vs_name, '')
        elif command_argvs[0].lower() == 'exit':
            break
        else:
            print 'command not found !'
