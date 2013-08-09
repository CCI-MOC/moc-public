#! /usr/bin/python
import sys, re, pexpect

sys.path.insert(0, '/etc/moc')
from mocutils import switch as cfg

def get_switch_state(switch_ip='192.168.0.1',user=cfg.user,passwd=cfg.pwd):
        p = pexpect.spawn('telnet '+switch_ip)
        p.expect('User:')
        p.sendline(user+'\r')
        p.expect('Password:')
        p.sendline(passwd+'\r')
        p.expect('TP-LINK')
        p.sendline('enable\r')
        p.expect('TP-LINK')
        p.sendline('configure\r')
        p.expect('TP-LINK')
        p.sendline('vlan database\r')
        p.expect('TP-LINK')
        f = open("log.txt","w+")
        p.logfile = f
        p.sendline('show vlan\r')
        p.expect('TP-LINK')
        p.sendline('exit\r')
        p.expect('TP-LINK')
        p.sendline('exit\r')
        p.expect('TP-LINK')
        p.sendline('exit\r')
        p.expect('TP-LINK')
        p.sendline('exit\r')
        p.expect('foreign host')
        p_3_entry=re.compile('[^\d]+(\d+)[^\d]+([\d,-]+)')
        p_4_entry=re.compile('[^\d]+(\d+)[^\d]+([\d,-]+)[^\d]+([\d,-]+)')
        #return a list of tuple ('100','16','1-2,4') or ('100','1-3'), the former with the tag-member in middle
        #the latter has no tag member
        vlan_list=[]
        #first try to match 4 entries, if failed, try to match 3 entries 
        for line in open("log.txt","r"):
                if p_4_entry.match(line):
                        vlan_list.append(p_4_entry.match(line).groups())
                elif p_3_entry.match(line):
                        vlan_list.append(p_3_entry.match(line).groups())
        print vlan_list
        return vlan_list

if __name__== "__main__":
        get_switch_state()
