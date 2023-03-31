import docs_functions
import globals as G


class tree():
    def __init__(self, **properties):
        self.root = None
        self.tree_entry_list = []

    def add_root(self, payload=None):
        if len(self.tree_entry_list) == 0:
            new_entry = tree_entry('new_entry_L0_P0_root')
            new_entry.entry = new_entry
            new_entry.payload = payload
            new_entry.icon = 'closed'
            new_entry.is_root = True
            new_entry.root = new_entry
            new_entry.status_open = True
            new_entry.prev = None
            new_entry.next = None
            new_entry.last = new_entry
            new_entry.is_parent = False
            new_entry.is_child = False
            new_entry.parent = None
            new_entry.first_child = None
            new_entry.level = 0
            new_entry.row = 0
            new_entry.col = 0
            self.root = new_entry
            self.tree_entry_list.append([new_entry, None])

    def print_tree_list(self):
        for t in self.tree_entry_list:
            t.print()
        print('------')


class tree_entry():
    def __init__(self, name):
        self.name = name
        self.entry = None
        self.payload = None
        self.icon = 'closed'
        self.is_root = False,
        self.root = None
        self.status_open = False
        self.prev = None
        self.next = None
        self.last = None
        self.is_parent = False
        self.parent = None
        self.is_child = False
        self.first_child = None
        self.level = 0
        self.row = 0
        self.col = 0

    def print(self):
        for v in self.__dict__:
            print(v, "-->", self.__dict__.get(v))
        print('-------')

    def create_entry_same_level_after(self, name, payload):  # ee = existing

        if (self.next is None):  # I am the second on this level (either we have a root or firstchild!
            new_entry = tree_entry('{}'.format(name))
            new_entry.entry = new_entry
            new_entry.payload = payload
            new_entry.icon = 'closed'
            new_entry.is_root = False
            new_entry.root = self.root
            new_entry.status_open = False
            new_entry.prev = self
            self.next = new_entry
            new_entry.last = new_entry
            self.last = new_entry
            new_entry.is_parent = False
            new_entry.parent = self.parent  # either none or same parent as child
            new_entry.is_child = self.is_child  # either none or same parent as child
            new_entry.first_child = self.first_child
            new_entry.row = self.row + 1
            new_entry.col = self.col
        else:
            new_entry = tree_entry('{}'.format(name))
            new_entry.entry = new_entry
            new_entry.payload = payload
            new_entry.icon = 'closed'
            new_entry.is_root = False
            new_entry.root = self.root
            new_entry.status_open = False
            new_entry.prev = self  # der Aufrufer
            new_entry.next = self.next  # mein next wird Dein next bei einem insert
            self.next = new_entry  # ich werde dein next
            new_entry.next.prev = self  # und ich werde der Vorgänger des bestehenden nächsten elements
            new_entry.last = new_entry.next.last  # ich bin nicht letzer..
            self.last = self.last  # bleibt wo es ist
            new_entry.is_parent = False
            new_entry.parent = self.parent  # either none or same parent as child
            new_entry.is_child = self.is_child  # either none or same parent as child
            new_entry.first_child = self.first_child  # das übernehme ich
            new_entry.row = self.row + 1
            new_entry.col = self.col
        return new_entry

    def add_child(self, name, payload):
        if self.is_parent is False:  # it is the first child!
            new_entry = tree_entry('{}'.format(name))
            new_entry.entry = new_entry
            new_entry.payload = payload
            # print('add_child, payload:', new_entry.payload)
            new_entry.icon = 'closed'
            new_entry.is_root = False
            new_entry.root = self.root
            new_entry.status_open = False
            new_entry.prev = None
            new_entry.next = None
            new_entry.last = new_entry
            new_entry.is_parent = False
            new_entry.parent = self
            # print('---->add_parent in child', new_entry.parent.name, new_entry.parent)
            new_entry.is_child = True
            new_entry.first_child = new_entry
            new_entry.row = 0
            new_entry.col = self.col + 1

            self.icon = 'open'
            self.is_root = self.is_root
            self.root = self.root
            if self.is_root:
                self.status_open = True  # root offen lassen
            else:
                self.status_open = False
            self.prev = self.prev
            self.next = self.next
            self.is_parent = True
            self.parent = self.parent
            # print("++++++parent_parent",self.parent)
            self.is_child = self.is_child
            self.first_child = new_entry
            self.row = self.row
            self.col = self.col
            return new_entry
        else:  # hey, es gibt schon ein Kind!
            existing_last_child = self.first_child.last
            new_entry = existing_last_child.create_entry_same_level_after(name, payload)
            return new_entry

    def delete(self):
        if self.is_parent:
            msg = "remove_children_first!!!"
            print(msg)
        elif self.is_child:
            if self.first_child == self and self.next is None:  # it is the last item
                self.parent.is_parent = False
                self.parent.first_child = None
                self.parent.status_open = False
                t.tree_entry_list.remove(self)
                self = None

            elif self.first_child == self and self.next is not None:
                self.parent.first_child = self.next
                self.next.prev = None
                self.t.tree_entry_list.remove(self)
                self = None
            elif self.first_child is not self and self.next is not None:
                self.prev.next = self.next
                self.next.prev = self.prev
                self.t.tree_entry_list.remove(self)
                self = None
            elif self.first_child is not self and self.next is None:
                self.prev.next = None
                self.t.tree_entry_list.remove(self)
                self = None

    def print_tree_h(self):
        # self.print()
        global fld
        global fc
        # print(fld,"fld")
        # print(fc,'fc')
        if self.payload is None:
            # payload="---"
            charge = {'item': str(0), 'level': '0', 'desc': 'All Forms', 'form': 'None', 'tree_entry': self}
            fld.append(charge)
            fc = fc + 1
        else:
            # payload= """{}, {}, {}""".format(self.payload['dsd_id'],self.payload['dsd_name'],self.payload['dsd_domain'])
            desc = "{}".format(self.name) #change
            # print('print_tree_h: desc:',desc)
            charge = {'item': str(fc), 'level': str(self.level), 'desc': self.name, 'tree_entry': self}
            fld.append(charge)
            fc = fc + 1
        # print(self.name,payload)
        if self.is_parent:
            # print(self.status_open, self)
            if self.status_open is False:
                if self.next is None:
                    return
                else:
                    self.next.print_tree_h()
            else:
                self.first_child.print_tree_h()
                if self.next is None:
                    return
                else:
                    self.next.print_tree_h()
        elif self.next is not None:
            self.next.print_tree_h()
        else:
            return

    def print_tree_docs(self):
        print("self", self)
        global fld
        global fc
        print(fld, "fld")
        print(fc, 'fc')
        if self.payload is None:
            # payload="---"
            charge = {'item': str(0), 'level': '0', 'desc': 'All Forms', 'form': 'None', 'tree_entry': self}
            fld.append(charge)
            fc = fc + 1
        else:
            # payload= """{}, {}, {}""".format(self.payload['dsd_id'],self.payload['dsd_name'],self.payload['dsd_domain'])
            desc = "{} {}".format(self.payload['name'])
            print('print_tree_doc: desc:', desc)
            charge = {'item': str(fc), 'level': str(self.level), 'desc': self.name, 'tree_entry': self}
            fld.append(charge)
            fc = fc + 1
        print('fld:', fld)
        print(self.name, self.payload)
        if self.is_parent:
            print('entry:', self.status_open, self)
            if self.status_open is False:
                if self.next is None:
                    return
                else:
                    self.next.print_tree_h()
            else:
                print('first_child1', self.first_child.name, self.first_child.status_open)
                self.first_child.print_tree_h()
                print('first_child2', self.first_child.name, self.first_child.status_open)
                if self.next is None:
                    return
                else:
                    self.next.print_tree_h()
        elif self.next is not None:
            self.next.print_tree_h()
        else:
            return

    def tree_h(self):
        global fld
        global fc
        fld = []
        fc = 0
        # print('init fld_c',fc)
        self.print_tree_h()
        return fld

    def tree_doc_h(self):
        global fld
        global fc
        fld = []
        fc = 0
        # print('init fld_c',fc)
        self.print_tree_docs()
        return fld


G.l_register_and_setup_user('[344816,583548811]',1)
formlist = docs_functions.l_get_all_docs_required_for_client_id_by_form_year_modern('[344816,583548811]',210,1)
# print("formslist",formlist[0:3])

t = tree()
t.add_root()
root = t.root
last_at_level = {}
last_at_level[str(0)] = root
t.root.name = "All-Forms"
forms = []
level_previous = 0
L1p = None
L2p = None
L3p = None
L4p = None
L5p = None

for e in formlist:
    payload = e
    print('adfjöasdjf: payload', payload)
    if level_previous == 0:  # Build the initial tree after root, we have no headers...
        L1p = e['Level1']
        L2p = e['Level2']
        L3p = e['Level3']
        L4p = e['Level4']
        L5p = e['Level5']
        parent = last_at_level['0']

        name = e['Level1']
        level = '1'
        print('adfjöasdjf: payload', payload)
        ne = parent.add_child(name, payload)
        ne.level = level
        t.tree_entry_list.append([ne, e])
        last_at_level[str(level)] = ne
        level_previous = level
        L1p = name
        parent = ne

        name = e['Level2']
        level = '2'
        ne = parent.add_child(name, payload)
        ne.level = level
        t.tree_entry_list.append([ne, e])
        last_at_level[str(level)] = ne
        level_previous = level
        L2p = name
        parent = ne

        name = e['Level3']
        level = '3'
        ne = parent.add_child(name, payload)
        ne.level = level
        t.tree_entry_list.append([ne, e])
        last_at_level[str(level)] = ne
        level_previous = level
        L3p = name
        parent = ne

        name = e['Level4']
        level = '4'
        ne = parent.add_child(name, payload)
        ne.level = level
        t.tree_entry_list.append([ne, e])
        last_at_level[str(level)] = ne
        level_previous = level
        L4p = name
        parent = ne

        name = e['Level5']
        level = '5'
        ne = parent.add_child(name, payload)
        ne.level = level
        t.tree_entry_list.append([ne, e])
        last_at_level[str(level)] = ne
        level_previous = level
        L5p = name


    else:
        if e['Level4'] == L4p:  # neuer Eintrag, gleiche Section
            ds = e['Level5']
            payload = e
            level = '5'
            ne = last_at_level[str(5)].create_entry_same_level_after(ds, payload)
            ne.level = level
            t.tree_entry_list.append([ne, e])
            last_at_level[str(5)] = ne
            level_previous = '5'

        else:  # neue Section
            L4p = e['Level4']  # neue Section
            if e['Level3'] == L3p:  # neuer Eintrag, neue Section, gleiches Formular
                ds = e['Level4']  # neuer Sectionsknopf
                payload = e
                level = '4'
                ne = last_at_level[str(4)].create_entry_same_level_after(ds, payload)
                ne.level = level
                t.tree_entry_list.append([ne, e])
                last_at_level[str(4)] = ne
                level_previous = '4'
                parent = ne

                name = e['Level5']
                level = '5'
                ne = parent.add_child(name, payload)
                ne.level = level
                t.tree_entry_list.append([ne, e])
                last_at_level[str(level)] = ne
                level_previous = level
                L5p = name

            else:  # neues Formular
                L3p = e['Level3']  # neues Form
                if e['Level2'] == L2p:  # neuer Eintrag, neue Section, neues Formular, gleiches Jahr
                    ds = e['Level3']  # Form
                    payload = e
                    level = '3'
                    ne = last_at_level[str(3)].create_entry_same_level_after(ds, payload)
                    ne.level = level
                    t.tree_entry_list.append([ne, e])
                    last_at_level[str(3)] = ne
                    level_previous = '3'
                    parent = ne

                    name = e['Level4']
                    level = '4'
                    ne = parent.add_child(name, payload)
                    t.tree_entry_list.append([ne, e])
                    ne.level = level
                    last_at_level[str(level)] = ne
                    level_previous = level
                    L4p = name
                    parent = ne

                    name = e['Level5']
                    level = '5'
                    ne = parent.add_child(name, payload)
                    ne.level = level
                    t.tree_entry_list.append([ne, e])
                    last_at_level[str(level)] = ne
                    level_previous = level
                    L5p = name



                else:  # neues Jahr
                    L2p = e['Level2']  # neues Jahr
                    if e[
                        'Level1'] == L1p:  # neuer Eintrag, neue Section, neues Formular, neues Jahr, gleiche Domain
                        ds = e['Level2']  # neues Jahr
                        level = '2'
                        payload = e
                        ne = last_at_level[str(2)].create_entry_same_level_after(ds, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(2)] = ne
                        level_previous = '2'
                        parent = ne

                        name = e['Level3']
                        level = '3'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L3p = name
                        parent = ne

                        name = e['Level4']
                        level = '4'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L4p = name
                        parent = ne

                        name = e['Level5']
                        level = '5'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L5p = name


                    else:
                        ds = e['Level1']  # neue Domain
                        level = '1'
                        payload = e
                        ne = last_at_level[str(1)].create_entry_same_level_after(ds, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(1)] = ne
                        level_previous = '1'
                        parent = ne

                        name = e['Level2']
                        level = '2'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L2p = name
                        parent = ne

                        name = e['Level3']
                        level = '3'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L3p = name
                        parent = ne

                        name = e['Level4']
                        level = '4'
                        ne = parent.add_child(name, payload)
                        ne.level = level
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L4p = name
                        parent = ne

                        name = e['Level5']
                        level = '5'
                        ne.level = level
                        ne = parent.add_child(name, payload)
                        t.tree_entry_list.append([ne, e])
                        last_at_level[str(level)] = ne
                        level_previous = level
                        L5p = name

def print_nice(t):
    count = 0
    for e in t.tree_entry_list:

        if e[1] is None:
            print('root:', count, e[0].name)
            count = count + 1
        else:
            print('Level:', e[0].level, '   ' * int(e[0].level), e[0].name, e[0].status_open)
            count = count + 1


print(t.tree_entry_list)
print_nice(t)


a=t.root.tree_doc_h()
print('langes Resultat--->',[print(e) for e in a])
print('------------')
a[1]['tree_entry'].status_open=True #machen wir SO auf!
a=t.root.tree_doc_h()
print('langes Resultat--->',[print(e) for e in a])
print('------------')




