# -*- coding:Utf-8 -*-
class NicoTools (Workbench):
	MenuText = "NicoTools"
	ToolTip = "Petits outils generalistes"
	Icon = """
		/* XPM */
		static char * cone_small_xpm[] = {
		"40 52 26 1",
		" 	c None",
		".	c #010200",
		"+	c #301A03",
		"@	c #4D2A06",
		"#	c #663807",
		"$	c #804508",
		"%	c #904F09",
		"&	c #A65B0D",
		"*	c #B16006",
		"=	c #C46A0C",
		"-	c #B26E26",
		";	c #D5740D",
		">	c #C1813D",
		",	c #E47D11",
		"'	c #F38716",
		")	c #C19669",
		"!	c #F6952B",
		"~	c #C0A68C",
		"{	c #F3AC62",
		"]	c #BEB7AF",
		"^	c #C3C5C2",
		"/	c #F1C698",
		"(	c #D9DAD7",
		"_	c #FEE5C8",
		":	c #E8E9E6",
		"<	c #FBFDFA",
		"                                        ",
		"                                        ",
		"                                        ",
		"                  ;-==                  ",
		"                  ,=**                  ",
		"                 ,;=**                  ",
		"                 ';***&                 ",
		"                 !;***&                 ",
		"                ;!;****                 ",
		"                ,!=****                 ",
		"                '!=****&                ",
		"                !,=****-                ",
		"               <</>>>)]^                ",
		"               <<:(^^^^^                ",
		"               <<:(^^^^^]               ",
		"               <<:(^^^^^^               ",
		"              :<<:(^^^^^^               ",
		"              <<<:(^^^^^^               ",
		"              /<<:(^^^^^^-              ",
		"             ;'!/((^^^~>**              ",
		"             ,'!;==*******              ",
		"            ;''!;==*******%             ",
		"            ''',;==*******&             ",
		"            ''',;==********-            ",
		"            !'!;;==*******-~            ",
		"           :<_!;;==******)^^            ",
		"           <<<:{;==****&)^^^            ",
		"           <<<<::((^^^^^^^^^]           ",
		"           <<<<::((^^^^^^^^^^           ",
		"          :<<<<::((^^^^^^^^^^           ",
		"          _<<<<::((^^^^^^^^^^           ",
		"          !<<<::(((^^^^^^^^^~&          ",
		"        =,'!<<::(((^^^^^^^])**          ",
		"     ;,,;'',,,{_(((^^^^]~&****==        ",
		"   ,,,,;&'',,,;;==************&*;       ",
		"   ,,,;*%',,,;;;==************&%=;;     ",
		"   &,,;&*',,,;;;==*************%=;,;=   ",
		"   %&,;*%',,,;;;==************&%=;,,;;  ",
		"    #%;=%,,,;;;===************$&;;,,,&  ",
		"     %==&%,,;;;===***********&%*;;,,;#  ",
		"    ..$&=&$;;;;===**********%%=;;;&##   ",
		"     ..#&;=&$%====*******%$%*=;&###     ",
		"      ..@%,;==&%$$$$$$$%&*=;*###+..     ",
		"       ..+%,,,;;;;===;;;;%###+.....     ",
		"        ...%;,,,,,,,,,&###+.......      ",
		"         ...%%,,,,,*$##+........        ",
		"          ...@$$####@........           ",
		"           .....++........              ",
		"            ...........                 ",
		"              ......                    ",
		"                                        ",
		"                                        "};
	"""

	def Initialize(self):
		import NicoTools
		commandslistPr = ["M_Corniere","M_TubeCarreRectangle","M_TubeCarreRectangleDeco","M_ProfilIPN"]
		commandslistTo = ["M_ToleCorniere","M_ToleU","M_ToleBoite","M_ToleZ","M_ToleOmega"]
		commandslistMp = ["M_MAP"]
		commandslistTu = ["M_TurnX5Plus","M_TurnX5Moins","M_TurnY5Plus","M_TurnY5Moins","M_TurnZ5Plus","M_TurnZ5Moins"]
		commandslistOu = ["M_Extract","M_InfoVolMasse","M_OldFuse"]
		commandslistCalpinage = ["M_MCalpinage1D"]
		commandslistPoints = ["M_MPoints3D"]
		commandslistEurocode = ["M_PlatineEurocode"]
	
		
		self.appendToolbar("Profils",commandslistPr)
		self.appendToolbar("Toles",commandslistTo)
		self.appendToolbar("Mise en plan",commandslistMp)
		self.appendToolbar("Rotation Vue",commandslistTu)
		self.appendToolbar("Outils",commandslistOu)
		self.appendMenu(["Nico Tools","Profils"],commandslistPr)
		self.appendMenu(["Nico Tools","Toles"],commandslistTo)
		self.appendMenu(["Nico Tools","Mise en plan"],commandslistMp)
		self.appendMenu(["Nico Tools","Rotation Vue"],commandslistTu)
		self.appendMenu(["Nico Tools","Outils"],commandslistOu)
		
		self.appendMenu(["Calpinage"],commandslistCalpinage)
		self.appendMenu(["Points"],commandslistPoints)
		self.appendMenu(["Eurocode"],commandslistEurocode)
	
		
Gui.addWorkbench(NicoTools())
