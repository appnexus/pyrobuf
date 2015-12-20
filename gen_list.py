from jinja2 import Environment, PackageLoader
import sys

def gen_list():
    env = Environment(loader=PackageLoader('protobuf', 'templates'))

    name_pyx = 'pyrobuf_list.pyx'
    name_pxd = 'pyrobuf_list.pxd'

    templ_pyx = env.get_template('pyrobuf_list_pyx.tmpl')
    templ_pxd = env.get_template('pyrobuf_list_pxd.tmpl')

    listdict = {
            'DoubleList':   'double',
            'FloatList':    'float',
            'IntList':      'int',
            'Int32List':    'int32_t',
            'Uint32List':   'uint32_t',
            'Int64List':    'int64_t',
            'Uint64List':   'uint64_t',
            'CharList':     'char'
    }

    with open('src/' + name_pyx, 'w') as fp:
        fp.write(templ_pyx.render({'def': listdict, 'version_major': sys.version_info.major}))

    with open('src/' + name_pxd, 'w') as fp:
        fp.write(templ_pxd.render({'def': listdict, 'version_major': sys.version_info.major}))

if __name__ == "__main__":
    gen_list()
