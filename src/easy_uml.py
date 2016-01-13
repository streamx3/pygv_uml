#!/usr/bin/env python

import sys


class Class:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class Relations:
    types = {'-|>':  'onormal',
             '-<>':  'diamond',
             '-<o>': 'odiamond',
             '-->':  'vee',
             '---':  'none',
             '--<':  'invempty'}

    def __init__(self):
        self.data = {}
        for typ in self.types:
            self.data[typ] = []

    def add(self, obj_a, obj_b, _type, dashed=False):
        if _type in self.types:
            self.data[_type].append((obj_a, obj_b, dashed))


class EasyUml:
    def __init__(self):
        self.classes = []
        self.relations = Relations()
        self.input_filename = ''
        self.template = {
            'header': 'digraph G {\n\t\tfontname = "Ubuntu Mono"\n\t\tfontsize = 12\n\n'
            '\t\tnode [\n\t\t\t\tfontname = "Ubuntu Mono"\n\t\t\t\tfontsize = 12\n'
            '\t\t\t\tshape = "record"\n\t\t]\n\n\t\tedge [\n'
            '\t\t\t\tfontname = "Ubuntu Mono"\n\t\t\t\tfontsize = 12\n\t\t]\n',
            'relation': '\t\tedge [\n\t\t\t\tarrowhead = "%s"\n\t\t]\n\n'
        }

    def parse_file(self, input_filename):
        self.input_filename = input_filename
        with open(input_filename) as f:
            content = f.readlines()

        while len(content):
            line = content.pop(0) if len(content) else None
            if 'class' in line:
                name = line.replace('class ', '').replace(':\n', '')
                line = content.pop(0)
                methods = []
                while len(content) and line != '' and line != '\n':
                    methods.append(line.replace('\n', ''))
                    line = content.pop(0) if len(content) else None
                self.classes.append(Class(name, methods))
            else:
                for rel in Relations.types:
                    dashed = False
                    if rel in line:
                        if '- ' in line:
                            dashed = True
                            line = line.replace('- ', '')
                        a, b = line.replace('\n', '').split(rel)
                        self.relations.add(a, b, rel, dashed)
        # for i in xrange(len(self.classes)):
        #     print(self.classes[i].name)
        #     print(self.classes[i].methods)
        # print(self.relations.data)

    def gen_dot(self, output_filename=None):
        def add_rel(rel_name):
            loc_rv = ''
            for rel in self.relations.data[rel_name]:
                loc_rv += '\t\t' + rel[0] + '->' + rel[1]
                if rel[2]:
                    loc_rv += ' [style="dashed"];'
                loc_rv += '\n'
            return loc_rv + '\n'

        retval = self.template['header']

        for t_class in self.classes:
            retval += '\t\t' + t_class.name + ' [\n\t\t\t\tlabel = "{' + t_class.name + '|'
            for meth in t_class.methods:
                retval += meth + '\l'
            retval += '}"\n\t\t]\n\n'

        for rel in self.relations.data:
            if len(self.relations.data[rel]):
                retval += self.template['relation'].replace('%s', Relations.types[rel])
                retval += add_rel(rel)

        retval += '}'

        if output_filename and output_filename != self.input_filename:
            with open(output_filename, 'w') as output_file:
                output_file.write(retval)
        else:
            print(retval)


eu1 = EasyUml()

if len(sys.argv) == 3:
    eu1.parse_file(sys.argv[1])
    eu1.gen_dot(sys.argv[2])

else:
    print('\nUsage:\n\t' + sys.argv[0] + ' input_file output_file\n')
