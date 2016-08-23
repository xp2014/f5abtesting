# -*- coding:utf-8 -*-
if __name__ == '__main__':
    from f5.bigip import ManagementRoot

    bigip_ip = '10.0.0.11'
    bigip_username = 'admin'
    bigip_password = 'admin'

    # Connect to the BigIP
    mgmt = ManagementRoot(bigip_ip, bigip_username, bigip_password)

    # List all virtual servers
    vs_list = mgmt.tm.ltm.virtuals.get_collection()
    print "Here is the list of Virtual Server in " + bigip_ip + ":"
    vs_name_list = []
    for vs in vs_list:
        vs_name_list.append(vs.name)
    print vs_name_list


def pool_b_list(vs_name):
    pool_b_name = vs_name + '_pool_b'
    if mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
        pool_b = mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
        print 'Here is the member list of ' + pool_b_name
        for member in pool_b.members_s.get_collection():
            print 'member:'+ member.name + ' status:' + member.session
    else:
        print pool_b_name + ' does not exist...'


if __name__ == '__main__':
    pool_b_list('vs_http')