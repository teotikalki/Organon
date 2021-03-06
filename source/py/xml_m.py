# -*- coding: utf-8 -*-
  
class XML_Methoden():
    
    def __init__(self,mb):
                
        self.ctx = mb.ctx
        self.mb = mb  
             
        self.selbstaufruf = False  
               
    def get_tree_info(self,elem,eintr,index=0,parent = 'root'):
        
        if not self.selbstaufruf:
            if self.mb.debug: log(inspect.stack)
            self.selbstaufruf = True
            
            
        if elem.attrib['Name'] != 'root':
            eintr.append((elem.tag,parent,elem.attrib['Name'],str(index-1),elem.attrib['Art'],
                          elem.attrib['Zustand'],elem.attrib['Sicht'],elem.attrib['Tag1'],elem.attrib['Tag2'],elem.attrib['Tag3']))
            #print('-    '*index,elem.tag,parent,elem.attrib['Name'],index-1,elem.attrib['Art'])
        for child in elem:
            self.get_tree_info(child,eintr,index+1,elem.tag)
    
    
    def get_parents(self,ordinal):
        #if self.mb.debug: log(inspect.stack)
        props = self.mb.props[T.AB]
        tree = props.xml_tree
        root = tree.getroot()
        
        parents = []
        try:     
            while ordinal not in ('ORGANON','Tabs'):
                el = root.find('.//{0}/..'.format(ordinal))
                if el.tag not in ['nr0','ORGANON','Tabs']:
                    ordinal = el.tag
                    parents.append([ordinal,el])
                else:
                    break
        except:
            log(inspect.stack,tb())
            
        return parents
             
    
    def erzeuge_XML_Eintrag(self,eintrag):
        if self.mb.debug: log(inspect.stack)

        # erzeugt den XML Eintrag fuer ein neues Standard Dokument
        tree = self.mb.props[T.AB].xml_tree 
        root = tree.getroot()
        et = ElementTree            
        ordinal,parent,name,lvl,art,zustand,sicht,tag1,tag2,tag3 = eintrag

        if parent == 'root':
            par = root
        else:
            par = root.find('.//'+parent)

        el = et.SubElement(par,ordinal)
        el.attrib['Parent'] = parent
        el.attrib['Name'] = name
        el.attrib['Art'] = art
        el.attrib['Lvl'] = str(lvl)
        el.attrib['Zustand'] = zustand
        el.attrib['Sicht'] = sicht
        el.attrib['Tag1'] = tag1
        el.attrib['Tag2'] = tag2
        el.attrib['Tag3'] = tag3
                    
        self.mb.props[T.AB].kommender_Eintrag += 1
        root.attrib['kommender_Eintrag'] = str(self.mb.props[T.AB].kommender_Eintrag)
       
       

          
    def in_Ordner_einfuegen(self,source,target):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()        
        # wird zum ersten Eintrag im Ordner
        source = root.find('.//'+source)
        target = root.find('.//'+target)
        # Parent Source/Target
        par_source = root.find('.//'+source.tag+'/..')
        par_target = root.find('.//'+target.tag+'/..')
        # Source im Parent loeschen
        par_source.remove(source)
        #Source als Subelement einfuegen
        target.insert(0,source)

        self.xmlLevel_und_hfPosition_anpassen(root,source)
        
     
    def drueber_einfuegen(self,source,target):
        if self.mb.debug: log(inspect.stack)
        
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()        
        # nur fuer das allererste Element
        source = root.find('.//'+source)
        target = root.find('.//'+target)
        # Parent Source/Target
        par_source = root.find('.//'+source.tag+'/..')
        par_target = root
        # Source im Parent loeschen
        par_source.remove(source)
        # Source hinter Target einfuegen
        par_target.insert(0,source)
        
        self.xmlLevel_und_hfPosition_anpassen(root,source)
        
     
    def vor_Nachfolger_einfuegen(self,source,nachfolger):  
        if self.mb.debug: log(inspect.stack)
  
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()        
        source = root.find('.//'+source)
        nachfolger = root.find('.//'+nachfolger)
        # Parent Source/Target
        par_source = root.find('.//'+source.tag+'/..')
        par_target = root.find('.//'+nachfolger.tag+'/..')
        # Source im Parent loeschen
        par_source.remove(source)
        # Index des Target im Parent
        index_target = list(par_target).index(nachfolger)
        # Source hinter Target einfuegen
        par_target.insert(index_target,source)

        self.xmlLevel_und_hfPosition_anpassen(root,source)

             
    def drunter_einfuegen(self,source,target):
        if self.mb.debug: log(inspect.stack)
            
        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()       
        source = root.find('.//'+source)
        target = root.find('.//'+target)
        # Parent Source/Target
        par_source = root.find('.//'+source.tag+'/..')
        par_target = root.find('.//'+target.tag+'/..')
        # Source im Parent loeschen
        par_source.remove(source)
        # Index des Target im Parent
        index_target = list(par_target).index(target)
        # Source hinter Target einfuegen
        par_target.insert(index_target+1,source)   
        
        self.xmlLevel_und_hfPosition_anpassen(root,source)
        
            
    def in_Papierkorb_einfuegen(self,source,target):
        if self.mb.debug: log(inspect.stack)

        tree = self.mb.props[T.AB].xml_tree
        root = tree.getroot()        
        # wird zum ersten Eintrag im Ordner
        source = root.find('.//'+source)
        target = root.find('.//'+target)
        # Parent Source/Target
        par_source = root.find('.//'+source.tag+'/..')
        #par_target = root.find('.//'+target.tag+'/..')
        # Source im Parent loeschen
        par_source.remove(source)
        #Source als Subelement einfuegen
        target.append(source)
        
        self.xmlLevel_und_hfPosition_anpassen(root,source)
        

    def xmlLevel_und_hfPosition_anpassen(self,root,source):
        if self.mb.debug: log(inspect.stack)
         
        eintr = []
        self.get_tree_info(root,eintr)
        
        sett = self.mb.settings_proj
        tags = sett['tag1'],sett['tag2'],sett['tag3']
        
        
        zeilen = []
        
        for eintrag in eintr:
            # Attribut 'Lvl' in xml datei setzen
            ordinal,parent,text,lvl,art,zustand,sicht,tag1,tag2,tag3 = eintrag
            
            if ordinal == self.mb.props[T.AB].Papierkorb:
                continue
            
            elem = root.find('.//'+ordinal)
            elem.attrib['Lvl'] = str(lvl)  
            lvl2 = int(lvl)
            
            par = root.find( './/{0}/..'.format(ordinal) )

            if par.attrib['Name'] == 'root':
                elem.attrib['Parent'] = 'root'
            else:
                elem.attrib['Parent'] = par.tag

            # Alle Zeilen X neu positionieren
            contr_zeile = self.mb.props[T.AB].Hauptfeld.getControl(ordinal)
            icon = contr_zeile.getControl('icon')
            x = 16+lvl2*16
            if icon.PosSize.X != x:
                icon.setPosSize(x,0,0,0,1)
                
            zeilen.append(contr_zeile)
                
                
        gliederung  = None
        if sett['tag3']:
            tree = self.mb.props[T.AB].xml_tree
            gliederung = self.mb.class_Gliederung.rechne(tree)    
                
        for contr_zeile in zeilen:       
            self.mb.class_Baumansicht.positioniere_icons_in_zeile(contr_zeile,tags,gliederung)
            
            
    def finde_nachfolger_oder_vorgaenger(self,nachbar,nur_sichtbaren_waehlen=False):
        
        try:
            selektierte_zeile = self.mb.props[T.AB].selektierte_zeile_alt
            props = self.mb.props[T.AB]
            
            tree = self.mb.props[T.AB].xml_tree
            root = tree.getroot()        
            source = root.find('.//'+selektierte_zeile)            
            
            eintr = []
            self.mb.class_XML.get_tree_info(root,eintr)
            
            gesuchter = None
            
            def nachf(value):
                return value < len(eintr)-1
            def vorg(value):
                return value > 0
            
            if nachbar == 'nachfolger':
                rechnung = nachf
                x = 1
            else:
                rechnung = vorg
                x = -1
            
            for e in eintr:
                if e[0] == selektierte_zeile:
                    index = eintr.index(e)
                    
                    if rechnung(index):
                        
                        if not nur_sichtbaren_waehlen:
                            
                            gesuchter = eintr[index+x][0]
                            return gesuchter
                        
                        else:
                            
                            sichtbare = [props.dict_zeilen_posY[s][0] for s in props.dict_zeilen_posY]
                            
                            gesuchter = eintr[index+x][0]
                            helfer = 0
                            
                            while gesuchter not in sichtbare:
                                
                                if nachbar == 'nachfolger':
                                    helfer += 1
                                else:
                                    helfer -= 1
                                
                                gesuchter = eintr[index + x + helfer][0]
                                
                            return gesuchter

            return gesuchter
        except:
            log(inspect.stack,tb())
            return None
        
        
        
    def get_papierkorb_inhalt(self):
        if self.mb.debug: log(inspect.stack)
        
        props = self.mb.props[T.AB]
        tree = props.xml_tree
        root = tree.getroot()
        
        papierkorb = root.find('.//' + props.Papierkorb)
        papierkorb_inhalt = [p.tag for p in papierkorb.findall('.//')]
        papierkorb_inhalt.append(props.Papierkorb)
        
        return papierkorb_inhalt
        
        
        
        