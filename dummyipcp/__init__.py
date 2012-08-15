from __future__ import print_function

import re
import time

from starcluster import clustersetup, logger, spinner


class DummyIpCluster(clustersetup.ClusterSetup):
    def __init__(self, port=12345, profile_dir='~/.ipcluster'):
        self.port = port
        self.profile_dir = profile_dir
        self.json_conn = "%s/security/ipcontroller-client.json" % profile_dir
    
    def run(self, nodes, master, user, user_shell, volumes):
        logger.log.info("Running ipcluster plugin for dummies.")
        
        self.profile_dir = re.sub("^~/", "/home/%s/" % user, self.profile_dir)
        self.json_conn = re.sub("^~/", "/home/%s/" % user, self.json_conn)
        self.opts = " ".join(
            ("--profile-dir='%s'" % self.profile_dir, "--port=%d" % self.port,
             "--ip='*'", "--location=%s" % master.public_dns_name))
                
        self.start_controller(master, user)
        for node in nodes:
            self.start_engines(node, user)
    
    def controller_ready(self, node):
        return node.ssh.isfile(self.json_conn)
    
    def start_controller(self, node, user):
        logger.log.info("Starting ipython controller.")
        cmd = 'su -l %s -c "screen -d -m ipcontroller %s"' % (user, self.opts)
        node.ssh.execute(cmd)

        logger.log.info("Waiting for json connector files.")
        s = spinner.Spinner()
        s.start()
        while not self.controller_ready(node):
            time.sleep(1)
        s.stop()
    
    def start_engines(self, node, user):
        logger.log.info("Starting ipython engines on %s." % node.alias)        
        cmd = 'su -l %s -c "screen -d -m ipengine %s"' % (user, self.opts)
        for i in xrange(node.num_processors):
            node.ssh.execute(cmd)
