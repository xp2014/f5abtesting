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


def region2b_remove(vs_name, region_name):
    dg_list = mgmt.tm.ltm.data_group.internals.get_collection()
    dg_name_list = []
    for dg in dg_list:
        dg_name_list.append(dg.name)
    print dg_name_list
    dg_region2b = vs_name + '_dg_region2b'
    dg_region2b_record = {'name': region_name}
    if dg_region2b in dg_name_list:
        print dg_region2b + ' exists,  removing ' + region_name + ' ...'
        dg_tmp = mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b)
        print dg_tmp.records
        dg_records = dg_tmp.records
        if dg_region2b_record in dg_records:
            if len(dg_records) > 1:
                dg_records.remove(dg_region2b_record)
                dg_tmp.update()
                print dg_region2b + ' updated ...'
            else:
                print 'The last region, remove the datagroup ' + dg_region2b
                dg_tmp.delete()
        else:
            print region_name + ' does not exist ...'
    else:
        print dg_region2b + ' does not exist ...'

if __name__ == '__main__':
    region2b_remove('vs_http', 'region12')
