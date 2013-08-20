#!/usr/bin/python

import pkg_resources
import requests

def power_cycle(ip, port='16992', user='admin', pwd='MOC2123moc!!', time=3):
  url = 'http://' + ip + ':' + port + '/remoteform'

  # After version 0.8.2 the usage for http_digest changed to HTTPDigestAuth
  version = pkg_resources.get_distribution("requests").version
  if version < '0.8.3':
    AUTH    = ('digest', user, pwd)
  else:
    AUTH    = requests.auth.HTTPDigestAuth(user, pwd)

  # The form values for 'reboot' and 'normal start up'
  PARAMS = {'amt_html_rc_boot_special': '1', 'amt_html_rc_radio_group': '3'}
  try:
    requests.post(url, PARAMS, auth = AUTH, timeout = time)
    return 0
  except:
    print "Error on machine", ip, sys.exc_info()[0]
    return -1


if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    print "Must include list of machines to cycle."
    exit(1)

  for arg in sys.argv[1::]:
    if not len(arg.split('.')) == 4:
      print "Error, incorrect input for " + arg
      exit(1)
    # If there was a range of IPs specified
    # Only works if the range is the least significant term
    if '-' in arg:
      # Grab the beginning and end of the range
      parts = arg.split('.')[3].split('-')
      if not len(parts) == 2:
        print "Error for range " + arg
      # Loop from beginning to end of range
      for arg2 in range(int(parts[0]), int(parts[1])+1):
        power_cycle('.'.join(arg.split('.')[:3]) + '.'  + str(arg2))
    else:
      power_cycle(arg)
