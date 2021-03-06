# -*- coding: utf-8 -*-

import unohelper


class Shortcuts():
    
    def __init__(self,mb):
        if mb.debug: log(inspect.stack)
        
        self.mb = mb
        
    
        AZ = [chr(i).upper() for i in range(ord('a'), ord('z')+1)]
        F1F12 = ['F'+str(i) for i in range(1,13)]
        numbers = [i for i in range(10)]
        
        self.keycodes = {}
        
        for a in AZ:
            co = uno.getConstantByName( "com.sun.star.awt.Key.{}".format(a) )
            self.keycodes.update({co:a.lower()})
        for a in numbers:
            co = uno.getConstantByName( "com.sun.star.awt.Key.NUM{}".format(a) )
            self.keycodes.update({co:a})
        for a in ['DOWN','UP','LEFT','RIGHT']:
            co = uno.getConstantByName( "com.sun.star.awt.Key.{}".format(a) )
            self.keycodes.update({co:a})
        for a in F1F12:
            co = uno.getConstantByName( "com.sun.star.awt.Key.{}".format(a) )
            self.keycodes.update({co:a})
        
        
        self.moegliche_shortcuts = AZ + numbers + F1F12 + ['DOWN','UP','LEFT','RIGHT']
        
        self.shortcuts = self.mb.settings_orga['shortcuts']
        self.writer_shortcuts = self.mb.class_Funktionen.get_writer_shortcuts()
        

        self.shortcuts_befehle = {
                         'TRENNE_TEXT' : self.teile_text,
                         'INSERT_DOC' : self.erzeuge_neue_Datei,
                         'INSERT_DIR' : self.erzeuge_neuen_Ordner,
                         'IN_PAPIERKORB_VERSCHIEBEN' : self.in_Papierkorb_einfuegen,
                         'CLEAR_RECYCLE_BIN' : self.leere_Papierkorb,
                         'NEUER_TAB' : self.starte_neuen_Tab,
                         'SCHLIESSE_TAB' : self.schliesse_Tab,
                         'BACKUP' : self.erzeuge_Backup,
                         'OEFFNE_ORGANIZER' : self.oeffne_Organizer,
                         'SHOW_TAG1' : self.toggle_tag1,
                         'SHOW_TAG2' : self.toggle_tag2,
                         'GLIEDERUNG' : self.toggle_tag3,
                         'BAUMANSICHT_HOCH' : self.tv_up,
                         'BAUMANSICHT_RUNTER' : self.tv_down,
                         'BENENNE_DATEI_UM' : self.datei_umbenennen,
                         'DATEIEN_VEREINEN' :  self.mb.class_Funktionen.vereine_dateien,   
                         'KONSOLENAUSGABE' :  self.toggle_logging,   
                          }


        
    def shortcut_ausfuehren(self,code,mods):
        if self.mb.debug: log(inspect.stack)
        
        try:
            if code in self.keycodes:
                keychar = self.keycodes[code]
            else:
                return False
            
            if isinstance(keychar, int):
                taste = keychar
            else:
                taste = keychar.upper()
            
            if taste in self.shortcuts[str(mods)]:
                cmd = self.shortcuts[str(mods)][taste]
                self.shortcuts_befehle[cmd]()
                return True
            return False
        except:
            log(inspect.stack,tb())
            return False
    
    def teile_text(self):
        if self.mb.debug: log(inspect.stack)

        if T.AB != 'ORGANON': return
        self.mb.class_Funktionen.teile_text()
        
    def erzeuge_neue_Datei(self):
        if self.mb.debug: log(inspect.stack)
        
        if T.AB != 'ORGANON': return
        self.mb.class_Baumansicht.erzeuge_neue_Zeile('Dokument')
    
    def erzeuge_neuen_Ordner(self):
        if self.mb.debug: log(inspect.stack)
        
        if T.AB != 'ORGANON': return
        self.mb.class_Baumansicht.erzeuge_neue_Zeile('Ordner')
        
    def vereine_dateien(self):
        if self.mb.debug: log(inspect.stack)
        
        if T.AB != 'ORGANON': return
        self.mb.class_Funktionen.vereine_dateien()
        
    def in_Papierkorb_einfuegen(self):
        if self.mb.debug: log(inspect.stack)
        
        ordinal = self.mb.props[T.AB].selektierte_zeile
        self.mb.class_Baumansicht.in_Papierkorb_einfuegen(ordinal)
                
    def leere_Papierkorb(self):
        if self.mb.debug: log(inspect.stack)
        self.mb.class_Baumansicht.leere_Papierkorb()  
        
    def starte_neuen_Tab(self):
        if self.mb.debug: log(inspect.stack)
        self.mb.class_Tabs.start(False)
        
    def schliesse_Tab(self):
        if self.mb.debug: log(inspect.stack)
        self.mb.tabsX.schliesse_Tab()
        
    def erzeuge_Backup(self):
        if self.mb.debug: log(inspect.stack)
        self.mb.erzeuge_Backup()
        
    def oeffne_Organizer(self):
        if self.mb.debug: log(inspect.stack)
        self.mb.class_Organizer.run()
        
    def toggle_tag1(self):
        if self.mb.debug: log(inspect.stack)
        
        sett = self.mb.settings_proj
        nummer = 1
        tag = 'tag%s'%nummer
        sett[tag] = not sett[tag]
        
        self.mb.class_Funktionen.mache_tag_sichtbar(sett[tag],tag)
        
        self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)  
        
    def toggle_tag2(self):
        if self.mb.debug: log(inspect.stack)
        
        if not self.mb.class_Funktionen.pruefe_galerie_eintrag():
            return
        
        sett = self.mb.settings_proj
        nummer = 2
        tag = 'tag%s'%nummer
        sett[tag] = not sett[tag]
        
        self.mb.class_Funktionen.mache_tag_sichtbar(sett[tag],tag)
        
        self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)  
        
    def toggle_tag3(self):
        if self.mb.debug: log(inspect.stack)
        
        sett = self.mb.settings_proj
        nummer = 3
        tag = 'tag%s'%nummer
        sett[tag] = not sett[tag]
        
        self.mb.class_Funktionen.mache_tag_sichtbar(sett[tag],tag)
        
        self.mb.speicher_settings("project_settings.txt", self.mb.settings_proj)  
        
    def toggle_logging(self):
        if self.mb.debug: log(inspect.stack)
        
        new_state = int(not self.mb.debug)
        
        self.mb.class_Log.output_console = new_state
        self.mb.settings_orga['log_config']['output_console'] = new_state
        self.mb.schreibe_settings_orga()
        self.mb.debug = new_state
        
        Popup(self.mb, zeit=1).text = '{0}: {1}'.format(LANG.KONSOLENAUSGABE, new_state)
        
    def tv_up(self):
        if self.mb.debug: log(inspect.stack)
        
        vorgaenger = self.mb.class_XML.finde_nachfolger_oder_vorgaenger('vorgaenger',True) 
        if vorgaenger != None:
            self.mb.class_Baumansicht.selektiere_zeile(vorgaenger)
        
    def tv_down(self):
        if self.mb.debug: log(inspect.stack)

        nachfolger = self.mb.class_XML.finde_nachfolger_oder_vorgaenger('nachfolger',True)    
        if nachfolger != None:
            self.mb.class_Baumansicht.selektiere_zeile(nachfolger)
            
    def datei_umbenennen(self):
        if self.mb.debug: log(inspect.stack)
        
        sel = self.mb.props[T.AB].selektierte_zeile
        props = self.mb.props[T.AB]
        
        ctrl_zeile = props.Hauptfeld.getControl(sel)
        ctrl_txt = ctrl_zeile.getControl('textfeld')
        
        txt = ctrl_txt.Text
        
        p = ctrl_txt.AccessibleContext.LocationOnScreen
        x,y = p.X,p.Y
        x = x + ctrl_txt.AccessibleContext.Size.Width
        
        posSize = x,y,400,50
        win,cont = self.mb.class_Fenster.erzeuge_Dialog_Container(posSize)
        
        ctrl, model = self.mb.createControl(self.mb.ctx, "Edit", 10, 10, 380, 30, (), ())   
        ctrl.Text = txt
        
        cont.addControl('txt',ctrl)
        
        listener = Datei_Umbenennen_Listener(self.mb,sel,win)
        ctrl.addKeyListener(listener)


    def get_mods(self,cmd,ctrls):
        if self.mb.debug: log(inspect.stack)
        # 0 = keine Modifikation
        # 1 = Shift
        # 2 = Strg
        # 3 = Shift + Strg
        # 4 = Alt
        # 5 = Shift + Alt
        # 6 = Strg + Alt
        # 7 = Shift + Strg + Alt
                        
        shift = ctrls['_Shift'+cmd].State
        alt = ctrls['_Alt'+cmd].State
        ctrl = ctrls['_Ctrl'+cmd].State
        
        mods = 0
        
        if shift: mods += 1
        if alt: mods += 4
        if ctrl: mods += 2
        mods = shift*1 + ctrl*2 + alt*4
        return mods
    
    def get_moegliche_shortcuts(self,mods,use_settings = True):
        if self.mb.debug: log(inspect.stack)
        
        moegliche = self.mb.class_Shortcuts.moegliche_shortcuts
        
        if mods < 2:
            return ('-',)
        
        if use_settings:
            in_settings = self.mb.settings_orga['shortcuts'][str(mods)]
        else:
            in_settings = []
                                                                
        uebrige = [str(m) for m in moegliche if str(m) not in self.writer_shortcuts[mods] and
                                           str(m) not in in_settings
                   ]
        uebrige.insert(0, '-')
        uebrige = tuple(uebrige)
        
        return uebrige
        
    
        
from com.sun.star.awt import XKeyListener
class Datei_Umbenennen_Listener (unohelper.Base, XKeyListener):
    def __init__(self,mb,sel,win):
        self.mb = mb
        self.sel = sel
        self.win = win
       
    def keyPressed(self,ev): pass
    
    def keyReleased(self,ev):
        if ev.KeyCode != 1280:
            return
        # Nur nach einer Eingabe (=1280) loggen
        if self.mb.debug: log(inspect.stack)
        
        try:
            txt = ev.Source.Text.strip()
            self.mb.class_Zeilen_Listener.aendere_datei_namen(self.sel,txt)
            self.win.dispose()
        except:
            log(inspect.stack,tb())
            
        
    def disposing(self,ev):
        return False





