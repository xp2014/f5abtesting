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

def region2b_list(vs_name):
    dg_region2b = vs_name + '_dg_region2b'
    if mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
        dg_tmp = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b)
        print 'Here is the record of ' + dg_region2b
        dg_records = dg_tmp.records
        for record in dg_records:
            for (k,v) in record.items():
                print v
    else:
        print dg_region2b + ' does not exist ...'


if __name__ == '__main__':
    region2b_list('vs_http')