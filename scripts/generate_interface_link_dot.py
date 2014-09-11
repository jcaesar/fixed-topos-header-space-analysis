#!/usr/bin/python
#
# Old script:
# Reads the transfer function files generated by the cisco config parser
# Used to generate:
#  - a theory file with the hosts and host/port connections
# Generates
#  - A graphiz-file to mirror that
#
#  Runs on the old version of hassel
#  export PYTHONPATH=$PWD/hassel-public/hsa-python
#
#@author: Julius Michaelis
#'''
from examples.load_stanford_backbone import *

filename = "StanfordNetwork"
topos_path = "~/uni/ba/topoS/interface_abstraction"

(ports_nametoid,ports_idtoname) = load_stanford_backbone_port_to_id_map()

#opf = open("%s.thy"%filename, 'w')
opg = open("%s.dot"%filename, 'w')

# \<lparr> \<rparr>
#opf.write("theory StanfordNetwork\n")
#opf.write("imports \"{}/Network\" \"{}/Network_View\"\n".format(topos_path, topos_path))
#opf.write("begin\n\n")
#opf.write("\n")
opg.write("digraph generated_isab_network {\n")

#opf.write("definition \"stanford_network = \<lparr>\n")
# collect hostnames and ports
port_hosts = {}
for (rtr_name,pmap) in ports_nametoid.items():
	opg.write("subgraph %s {\ncolor=lightgrey; style=filled; %s [label=\"%s\"];\n"%(rtr_name, rtr_name, rtr_name))
	for (portname,portid) in pmap.items():
		if portid in port_hosts:
			print "Warning, duplicate port id {}, already present in {}, ignored {}".format(portid, port_hosts[portid], rtr_name)
		else:
			port_hosts[portid] = rtr_name
			opg.write("{} -> {} [dir=\"both\"]; {} [label=\"{} ({})\"];\n".format(rtr_name, portid, portid, portname, portid))
	opg.write("}\n")

# collect port links
ttf = load_stanford_backbone_ttf();
linkstrings = []
ifacestrings = []
linkbuild = []
def appendport(portid):
	s = "\<lparr> entity = Host ''{}'', port = Port {} \<rparr>".format(port_hosts[portid], portid)
	linkbuild.append(s)
	if s not in ifacestrings:
		ifacestrings.append("\t%s"%s)
for rule in ttf.rules:
	if rule['action'] == 'link':
		for in_port in rule['in_ports']:
			s_port = in_port / 100000 * 100000 + in_port % 10000 # the 10 000 place of the port number encodes its function - it is still the same port
			if not s_port in port_hosts:
				print "Warning, unknown source(?) port %d"%in_port
				continue
			for d_port in rule['out_ports']:
				if not d_port in port_hosts:
					print "Warning, unknown destination(?) port %d"%out_port
					continue
				linkbuild = []
				linkbuild.append("\t(")
				appendport(s_port);
				linkbuild.append(", ")
				appendport(d_port);
				linkbuild.append(")")
				linkstrings.append(''.join(linkbuild))
				opg.write("{} -> {};\n".format(s_port, d_port))
	else:
		print "Warning, TTF rule is not link."
print "%d links"%len(linkstrings)

#opf.write("interfaces = {\n")
#opf.write(",\n".join(ifacestrings))
#opf.write("},\n")

print "Forwarding function is a dummy"
#opf.write("forwarding = (\<lambda> e. (\<lambda> p (src,dst). {})),\n")

#opf.write("links = {\n")
#opf.write(",\n".join(linkstrings))
#opf.write("}\n")

#opf.write("\<rparr>\"\n")
#opf.write("\nend\n")
#opf.close()

opg.write("}\n")
opg.close()
