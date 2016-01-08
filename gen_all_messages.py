import re
import glob
import os.path

from jinja2 import Environment, PackageLoader

from parse_proto import Parser

def gen_all_messages():
    parser = Parser()

    env = Environment(loader=PackageLoader('protobuf', 'templates'))

    for spec in glob.glob('messages/*.proto'):
        print("parsing %s" % spec)

        m, _ = os.path.splitext(os.path.basename(spec))
        name_pxd = "%s_proto.pxd" % m
        name_pyx = "%s_proto.pyx" % m

        msgdef = parser.parse_from_filename(spec)

        templ_pxd = env.get_template('proto_pxd.tmpl')
        templ_pyx = env.get_template('proto_pyx.tmpl')

        with open('out/' + name_pxd, 'w') as fp:
            fp.write(templ_pxd.render(msgdef))

        with open('out/' + name_pyx, 'w') as fp:
            fp.write(templ_pyx.render(msgdef))

if __name__ == "__main__":
    gen_all_messages()
