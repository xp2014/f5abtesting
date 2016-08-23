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


def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def valid_pool_member(pool_member):
    pool_member_parts = pool_member.split(':')
    if len(pool_member_parts) != 2:
        return False
    if validIP(pool_member_parts[0]) and (0 <= int(pool_member_parts[1])  <= 65535):
        return True
    else:
        return False


def pool_b_mbr_del(vs_name, pool_b_member):
    pool_b_name = vs_name + '_pool_b'
    if mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
        pool_b = mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
        if pool_b.members_s.members.exists(name=pool_b_member, partition='Common'):
            pool_b_members = pool_b.members_s.get_collection()
            if len(pool_b_members) > 1:
                pool_b_member_tmp = pool_b.members_s.members.load(name=pool_b_member, partition='Common')
                pool_b_member_tmp.delete()
                print pool_b_member + ' removed from ' + pool_b_name
            else:
                pool_b.delete()
                print pool_b_member + ' is the last member, delete ' + pool_b_name
            # check pool_b_member is in pool_a
            vs_tmp = mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
            vs_tmp_raw = vs_tmp.raw
            pool_a_s = vs_tmp_raw['pool'].split('/')
            pool_a = mgmt.tm.ltm.pools.pool.load(name=pool_a_s[2], partition=pool_a_s[1])
            for pool_a_member in pool_a.members_s.get_collection():
                # print pool_a_member.raw
                # Retrieve full path of the pool member, as the name could be different from IP:port
                pool_a_member_path = pool_a_member.fullPath
                # check if the IP:port already in pool_a's member list, enable it if exists
                if pool_a_member_path.split('/')[2] == pool_b_member:
                    print pool_b_member + ' is also in ' + pool_a.name + ', enable it ...'
                    pool_a_member_tmp = pool_a.members_s.members.load(name=pool_a_member.name, partition=pool_a_s[1])
                    pool_a_member_tmp.session = 'user-enabled'
                    pool_a_member_tmp.update()
                    print pool_b_member + ' enabled in ' + pool_a.name
        else:
            print pool_b_member + ' does not in ' + pool_b_name

if __name__ == '__main__':
    pool_b_mbr_del('vs_http', '10.10.1.43:80')