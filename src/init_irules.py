if __name__ == '__main__':
    import re
    import os
    from f5.bigip import ManagementRoot

    # Connect to the BigIP
    mgmt = ManagementRoot("10.0.0.11", "admin", "admin")

    # List all virtual servers
    vs_list = mgmt.tm.ltm.virtuals.get_collection()
    print "Here is the list of Virtual Server " + ":"
    vs_name_list = []
    for vs in vs_list:
        vs_name_list.append(vs.name)
    print vs_name_list


def init_irules(vs_name, irules_tmp_file):
    if not (os.path.isfile(irules_tmp_file)):
        print 'File ' + irules_tmp_file + ' does not exist !'
    else:
        irules_file = open(irules_tmp_file)
        try:
            irules_text = irules_file.read()
            strinfo = re.compile('ab_demo')
            irules_text = strinfo.sub(vs_name, irules_text)
        finally:
            irules_file.close()
        irules_ab = vs_name + '_irules_ab'
        if mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
            print irules_ab + ' already exists, updating ... '
            rule1 = mgmt.tm.ltm.rules.rule.load(name=irules_ab)
            rule1.apiAnonymous = irules_text
            rule1.update()
        else:
            print irules_ab + ' does not exist, creating ... '
            rule1 = mgmt.tm.ltm.rules.rule.create(name=irules_ab, partition='Common', apiAnonymous=irules_text)
            print rule1.name + ' created '
        rule1 = mgmt.tm.ltm.rules.rule.load(name=irules_ab)
        print rule1.name + ' created '
        print rule1.apiAnonymous

if __name__ == '__main__':
    init_irules('vs_http', 'irules_tmp.conf')
