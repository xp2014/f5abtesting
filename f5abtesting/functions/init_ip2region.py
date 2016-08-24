if __name__ == '__main__':
    import os
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


def init_ip2region(vs_name, ip2region_file):
    dg_records = []
    if not (os.path.isfile(ip2region_file)):
        print 'File ' + ip2region_file + ' does not exist !'
    else:
        for line in open(ip2region_file):
            dg_str = line.split()
            dg_record = {'data': dg_str[0], 'name': dg_str[1]}
            dg_records.append(dg_record)
        print dg_records
        dg_list = mgmt.tm.ltm.data_group.internals.get_collection()
        dg_name_list = []
        for dg in dg_list:
            dg_name_list.append(dg.name)
        print dg_name_list
        dg_ip2region = vs_name + '_dg_ip2region'
        if dg_ip2region in dg_name_list:
            print dg_ip2region + ' already exists, deleting ...'
            dg_tmp = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region)
            dg_tmp.delete()
            print dg_ip2region + ' deleted'
            print ' creating a new version ...'
            dg_new = mgmt.tm.ltm.data_group.internals.internal.create(name=dg_ip2region, type='ip', records=dg_records)
            print 'Datagroup ' + dg_new.name + ' created'
        else:
            print dg_ip2region + ' does not exist, creating ...'
            dg_new = mgmt.tm.ltm.data_group.internals.internal.create(name=dg_ip2region, type='ip', records=dg_records)
            print 'Datagroup ' + dg_new.name + ' created'

        dg_new = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region)
        print dg_new.records

if __name__ == '__main__':
    init_ip2region('vs_http', 'ip2region.conf')
