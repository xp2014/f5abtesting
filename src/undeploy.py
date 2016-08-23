if __name__ == '__main__':
    from f5.bigip import ManagementRoot
    from pool_b_mbr_del import pool_b_mbr_del

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


def undeploy(vs_name, cleanup):
    pool_b_name = vs_name + '_pool_b'
    dg_region2b = vs_name + '_dg_region2b'
    dg_ip2region = vs_name + '_dg_ip2region'
    irules_ab = vs_name + '_irules_ab'
    irules_ab_fullpath = '/Common/' + irules_ab
    vs_tmp = mgmt.tm.ltm.virtuals.virtual.load(name='vs_http', partition='Common')
    vs_tmp_raw = vs_tmp.raw
    if 'rules' in vs_tmp_raw:
        print vs_tmp_raw['rules']
        if irules_ab_fullpath in vs_tmp_raw['rules']:
            print irules_ab + ' bound on ' + vs_name + ', unbind it'
            vs_tmp_irules = vs_tmp.rules
            vs_tmp_irules.remove(irules_ab_fullpath)
            print vs_tmp_irules
            vs_tmp.update()
            print irules_ab + ' unbound from ' + vs_name
        else:
            print irules_ab + ' is not bound on ' + vs_name
    else:
        print 'No iRules bound on ' + vs_name
    if cleanup == 'cleanup':
        print 'clean up f5abtesting configure for ' + vs_name
        if mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
            print 'deleting ' + irules_ab
            irules_tmp = mgmt.tm.ltm.rules.rule.load(name=irules_ab)
            irules_tmp.delete()
            print 'done'
        if mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
            print 'deleting ' + pool_b_name
            pool_tmp = mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
            for member in pool_tmp.members_s.get_collection():
                print member.name
                pool_b_mbr_del(vs_name,member.name)
            print 'done'
        if mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
            print 'deleting ' + dg_region2b
            datagroup_tmp = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b, partition='Common')
            datagroup_tmp.delete()
            print 'done'
        if mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_ip2region):
            print 'deleting ' + dg_ip2region
            datagroup_tmp = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region, partition='Common')
            datagroup_tmp.delete()
            print 'done'
        print 'clean up finished'


if __name__ == '__main__':
    undeploy('vs_http','cleanup')
