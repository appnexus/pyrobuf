import sys
import re

from jinja2 import Environment, PackageLoader

from parse_proto import Parser

def gen_message(fname, direc=""):
    get_name = re.compile(r'([A-Za-z][A-Za-z0-9_]*).proto').match
    m = get_name(fname[fname.rfind('/')+1:])
    if m is None:
        print "not a .proto file"
        return

    name_pxd = "%s_proto.pxd" % m.group(1)
    name_pyx = "%s_proto.pyx" % m.group(1)

    parser = Parser()
    msgdef = parser.parse_from_filename(fname)

    env = Environment(loader=PackageLoader('protobuf', 'templates'))

    templ_pxd = env.get_template('proto_pxd.tmpl')
    templ_pyx = env.get_template('proto_pyx.tmpl')

    with open(direc.rstrip('/') + '/' + name_pxd, 'w') as fp:
        fp.write(templ_pxd.render(msgdef))

    with open(direc.rstrip('/') + '/' + name_pyx, 'w') as fp:
        fp.write(templ_pyx.render(msgdef))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "ERROR: no message supplied"

    elif len(sys.argv) == 2:
        gen_message(sys.argv[1])

    else:
        gen_message(sys.argv[1], sys.argv[2])
