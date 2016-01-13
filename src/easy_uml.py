class Class:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class Relations:
    def __init__(self):
        self.types = ['inheritance', 'composition']
        self.data = {'inheritance': [], 'composition': []}

    def add(self, ancestor, forebear, type):
        if type in self.types:
            self.data[type].append((ancestor, forebear))


class EasyUml:
    def __init__(self):
        self.classes = []
        self.relations = Relations()

    def parse_file(self, filename):
        with open(filename) as f:
            content = f.readlines()

        while len(content):
            line = content.pop(0)
            if 'class' in line:
                name = line.replace('class ', '').replace(':\n', '')
                line = content.pop(0)
                methods = []
                while len(content) and line != '' and line != '\n':
                    methods.append(line.replace('\n', ''))
                    line = content.pop(0) if len(content) else None
                self.classes.append(Class(name, methods))
            elif '->' in line:
                ancestor, forebear = line.replace(':\n', '').split('->')
                self.relations.add(ancestor, forebear, 'inheritance')
                line = content.pop(0) if len(content) else None
            elif '-<>' in line:
                ancestor, forebear = line.replace(':\n', '').split('-<>')
                self.relations.add(ancestor, forebear, 'composition')
                line = content.pop(0) if len(content) else None

        for i in xrange(len(self.classes)):
            print(self.classes[i].name)
            print(self.classes[i].methods)
        print(self.relations.data)


eu1 = EasyUml()

eu1.parse_file('class.1.txt')
