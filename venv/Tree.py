import doc_set_definition
import globals as G

class tree():
  def __init__(self,**properties):
    self.root=None
    self.tree_entry_list=[]

  def add_root(self,payload=None):
    if len(self.tree_entry_list)==0:
        new_entry = tree_entry('new_entry_L0_P0_root')
        new_entry.entry = new_entry
        new_entry.payload = payload
        new_entry.icon = 'closed'
        new_entry.is_root = True
        new_entry.root = new_entry
        new_entry.status_open = False
        new_entry.prev = None
        new_entry.next = None
        new_entry.last = new_entry
        new_entry.is_parent = False
        new_entry.is_child = False
        new_entry.parent = None
        new_entry.first_child = None
        new_entry.level=0
        new_entry.row = 0
        new_entry.col = 0
        self.root=new_entry
        self.tree_entry_list.append([new_entry,None])


  # def add_tree_entry(self,position, icon, row,xs_col,x_width,is_root,is_parent,pt_first_child,is_child,pt_parent):
  #   new_tree_entry=tree_entry(icon, row,xs_col,x_width,is_root,is_parent,pt_first_child,is_child,pt_parent)
  #   self.tree_entry_list.append(new_tree_entry)
  #
  # def add_child_entry( self,position, icon, row,xs_col,x_width,is_root,is_parent,pt_first_child,is_child,pt_parent):
  #   pass

  def print_tree_list(self):
     for t in self.tree_entry_list:
        t.print()
     print('------')








class tree_entry():

  def __init__(self,name):
      self.name=name
      self.entry=None
      self.payload=None
      self.icon='closed'
      self.is_root=False,
      self.root=None
      self.status_open=True
      self.prev=None
      self.next = None
      self.last = None
      self.is_parent= False
      self.parent= None
      self.is_child= False
      self.first_child=None
      self.level=0
      self.row=0
      self.col=0

  def print(self):
      for v in self.__dict__:
          print(v,"-->",self.__dict__.get(v))
      print('-------')

  def create_entry_same_level_after(self,name,payload): #ee = existing

      if(self.next is None): #I am the second on this level (either we have a root or firstchild!
          new_entry=tree_entry('{}'.format(name))
          new_entry.entry =new_entry
          new_entry.payload = payload
          new_entry.icon='closed'
          new_entry.is_root=False
          new_entry.root=self.root
          new_entry.status_open = True
          new_entry.prev=self
          self.next=new_entry
          new_entry.last=new_entry
          self.last=new_entry
          new_entry.is_parent= False
          new_entry.parent= self.parent         #either none or same parent as child
          new_entry.is_child= self.is_child     #either none or same parent as child
          new_entry.first_child=self.first_child
          new_entry.row=self.row+1
          new_entry.col=self.col
      else:
          new_entry=tree_entry('{}'.format(name))
          new_entry.entry =new_entry
          new_entry.payload = payload
          new_entry.icon='closed'
          new_entry.is_root=False
          new_entry.root=self.root
          new_entry.status_open = True
          new_entry.prev=self #der Aufrufer
          new_entry.next=self.next #mein next wird Dein next bei einem insert
          self.next=new_entry #ich werde dein next
          new_entry.next.prev=self #und ich werde der Vorgänger des bestehenden nächsten elements
          new_entry.last=new_entry.next.last #ich bin nicht letzer..
          self.last=self.last #bleibt wo es ist
          new_entry.is_parent= False
          new_entry.parent= self.parent         #either none or same parent as child
          new_entry.is_child= self.is_child     #either none or same parent as child
          new_entry.first_child=self.first_child #das übernehme ich
          new_entry.row=self.row+1
          new_entry.col=self.col
      return new_entry

  def add_child(self,name,payload):
      if self.is_parent is False: #it is the first child!
          new_entry = tree_entry('{}'.format(name))
          new_entry.entry = new_entry
          new_entry.payload = payload
          new_entry.icon = 'closed'
          new_entry.is_root = False
          new_entry.root = self.root
          new_entry.status_open = True
          new_entry.prev = None
          new_entry.next = None
          new_entry.last = new_entry
          new_entry.is_parent= False
          new_entry.parent= self
          # print('---->add_parent in child', new_entry.parent.name, new_entry.parent)
          new_entry.is_child= True
          new_entry.first_child=new_entry
          new_entry.row=0
          new_entry.col=self.col+1

          self.icon='Open'
          self.is_root=self.is_root
          self.root=self.root
          self.status_open=True
          self.prev=self.prev
          self.next = self.next
          self.is_parent= True
          self.parent= self.parent
          # print("++++++parent_parent",self.parent)
          self.is_child= self.is_child
          self.first_child=new_entry
          self.row=self.row
          self.col=self.col
          return new_entry
      else: #hey, es gibt schon ein Kind!
          existing_last_child = self.first_child.last
          new_entry = existing_last_child.create_entry_same_level_after(name)
          return new_entry

  def delete(self):
     if self.is_parent:
        msg="remove_children_first!!!"
        print(msg)
     elif self.is_child:
         if self.first_child==self and self.next is None: #it is the last item
             self.parent.is_parent=False
             self.parent.first_child=None
             self.parent.status_open=False
             t.tree_entry_list.remove(self)
             self=None

         elif self.first_child==self and self.next is not None:
             self.parent.first_child=self.next
             self.next.prev=None
             t.tree_entry_list.remove(self)
             self=None
         elif self.first_child is not self and self.next is not None:
             self.prev.next= self.next
             self.next.prev = self.prev
             t.tree_entry_list.remove(self)
             self=None
         elif self.first_child is not self and self.next is None:
             self.prev.next = None
             t.tree_entry_list.remove(self)
             self = None




  def print_tree_h(self):
      #self.print()
      if self.payload is None:
          payload="---"
      else:
          payload= """{}, {}, {}""".format(self.payload['dsd_id'],self.payload['dsd_name'],self.payload['dsd_domain'])

      print(self.name,payload)
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





#
# #--main---
# t= tree()
# t.add_root()
# # t.root.print()
#
# nte=t.root.add_child('L1_P0')
# t.tree_entry_list.append(nte)
# # nte.print()
#
# nt2=nte.create_entry_same_level_after('L1_P1')
# t.tree_entry_list.append(nt2)
# # nt2.print()
#
# ch1=nte.add_child('L1_P0_L2_P0')
# t.tree_entry_list.append(ch1)
# # ch1.print()
#
# ch4=nte.add_child('L1_P0_L2_P2')
# t.tree_entry_list.append(ch4)
#
#
# ch2=ch1.create_entry_same_level_after('L1_P0_L2_P1')
# t.tree_entry_list.append(ch2)
# # ch2.print()
#
#
# ch1_1=ch1.add_child('L1_P0_L2_P0_L3_P0')
# t.tree_entry_list.append(ch1_1)
#
# ch1_1_1=ch1_1.add_child('L1_P0_L2_P0_L3_P0_L4_P0')
# t.tree_entry_list.append(ch1_1_1)
#
# ch1_1_2=ch1_1_1.create_entry_same_level_after('L1_P0_L2_P0_L3_P0_L4_P1_alt')
# t.tree_entry_list.append(ch1_1_2)
#
# ch1_1_3=ch1_1_1.create_entry_same_level_after('L1_P0_L2_P0_L3_P0_L4_P1_neu')
# t.tree_entry_list.append(ch1_1_3)
#
# ch3=t.root.add_child('L1_P2')
# t.tree_entry_list.append(ch3)


#------------------------------

G.l_register_and_setup_user('[344816,583548811]',1)
formlist=doc_set_definition.l_get_forms_in_sequence_modern('[344816,583548811]')
t = tree()
t.add_root()
root=t.root
last_at_level = {}
last_at_level[str(0)]=root
t.root.name="All-Forms"


forms=[]
level_previous = 0
for e in formlist:
    print(e['doc_set_structure'],e['dsd_desc'])
    ds=e['doc_set_structure']
    payload=e
    level=ds.count('.')+1
    if level > level_previous: #we go deeper
        parent=last_at_level[str(level-1)]
        ne=parent.add_child(ds,payload)
        t.tree_entry_list.append([ne,e])
        last_at_level[str(level)]=ne
        level_previous=level
    elif level==level_previous:
        ne=last_at_level[str(level)].create_entry_same_level_after(ds,payload)
        t.tree_entry_list.append([ne,e])
        last_at_level[str(level)] = ne
        level_previous = level
    elif level < level_previous:
        ne=last_at_level[str(level)].create_entry_same_level_after(ds,payload)
        t.tree_entry_list.append([ne,e])
        last_at_level[str(level)] = ne
        level_previous = level


count=0
for e in t.tree_entry_list:

    if e[1] is None:
        print('root',count)
        count=count+1
    else:
        print(e[0].name,count, e[1]['dsd_desc'])
        count=count+1

# print('------')
# print('Länge der Liste', len(t.tree_entry_list))
# print('------')
# print(t.tree_entry_list)
# print('------')
# [print(e.name) for e in t.tree_entry_list]
# for e in t.tree_entry_list:
#     print(e.name)
# print("------------")
# t.root.status_open = True
# nt2.status_open = False
# nte.status_open = False

t.tree_entry_list[2][0].status_open=False
t.tree_entry_list[20][0].status_open=False
t.root.print_tree_h()
print('--------')
# print(len(t.tree_entry_list))
# # ch1_1_3.delete()
# print(len(t.tree_entry_list))

# t.root.print_tree_h()
# nte= tree_entry('nte')
#
#
#

# nte.entry=nte
# nte.root=te
# nte.prev=te
# te.next=nte
#
#
# te.print()
# nte.print()


