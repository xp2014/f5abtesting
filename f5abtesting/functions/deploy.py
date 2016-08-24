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


def deploy(vs_name):
    pool_b_name = vs_name + '_pool_b'
    dg_region2b = vs_name + '_dg_region2b'
    dg_ip2region = vs_name + '_dg_ip2region'
    irules_ab = vs_name + '_irules_ab'
    irules_ab_fullpath = '/Common/' + irules_ab
    if not mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
        print pool_b_name + ' does not exist, use pool_b_mbr_add to create and add member into it.'
    elif not mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
        print dg_region2b + ' does not exist, use region2b_assign to create and add record into it.'
    elif not mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_ip2region):
        print dg_ip2region + ' does not exist, use init_ip2region to create it.'
    elif not mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
        print irules_ab + ' does not exist, use init_irules to create it.'
    else:
        vs_tmp = mgmt.tm.ltm.virtuals.virtual.load(name='vs_http', partition='Common')
        vs_tmp_raw = vs_tmp.raw
        if 'rules' in vs_tmp_raw:
            print vs_tmp_raw['rules']
            if irules_ab_fullpath in vs_tmp_raw['rules']:
                print irules_ab + ' already bound on ' + vs_name
            else:
                vs_tmp_irules = vs_tmp.rules
                irules_record_file = vs_name + '_irules_records.bak'
                f = open(irules_record_file, 'w')
                for s in vs_tmp_irules:
                    f.write(s + '\n')
                f.close()
                vs_tmp_irules.insert(0, irules_ab_fullpath)
                vs_tmp.update()
                print irules_ab + ' prepended on vs ' + vs_name
        else:
            print 'No iRules bound on ' + vs_name + ', binding ' + irules_ab
            vs_tmp.rules = [irules_ab_fullpath]
            vs_tmp.update()
            print irules_ab + ' bound on ' + vs_name

if __name__ == '__main__':
    deploy('vs_http')





