# -*- coding:Utf-8 -*-
#############################################################
# Programme Python type                     				#
# Auteur : Nicolas Tuffereau, 2011							#
# Licence : GPL												#
# Ateliers de petits outils généraux			            #
# 												            #
#############################################################

#####################################
# Importation de fonctions externes :

import FreeCAD, FreeCADGui, Part, math, os, time, FreeCADTools, Draft
import Chemin
from FreeCAD import Base
from pivy import coin
App=FreeCAD
Gui=FreeCADGui




#
#	maths
#

def Arrondi(x,n):
	if n==0:
		val=1
	if n==1:
		val=10.0
	if n==2:
		val=100.0
	arrondi=int(x*val)/val
	return arrondi

def moyenne(list):
	moyenne=sum(list)/len(list)
	return moyenne


#
# Profilés
#

class Corniere():
	"Construction d'un profil de corniere"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","L1","Corniere","Largeur 1").L1=20.0
		obj.addProperty("App::PropertyDistance","L2","Corniere","Largeur 2").L2=20.0
		obj.addProperty("App::PropertyDistance","e1","Corniere","Epaisseur 1").e1=2.0
		#obj.addProperty("App::PropertyDistance","e2","Corniere","Epaisseur 2").e2=2.0
		obj.addProperty("App::PropertyDistance","Longueur","Corniere","Longueur").Longueur=200.0
		obj.addProperty("App::PropertyIntegerList","Chx","Corniere","Choix Autonome ou lié").Chx=[0]#0 pour Autonome et 1 pour lié
		obj.addProperty("App::PropertyLink","ParamCorn","Corniere","Paramètres Cornières").ParamCorn#Trouver le moyen possédant uniquement des paramètres et pas de shapes...
		obj.Proxy = self
		
	def onChanged(self, fp, prop):
		if prop == "L1" or prop == "L2" or prop == "e1" or prop == "Longueur":
			self.execute(fp)
		
	def execute(self, fp):
		pl=fp.Placement
		if fp.Chx[0]==1:
			L1=fp.ParamCorn.Param[0]
			L2=fp.ParamCorn.Param[1]
			e1=fp.ParamCorn.Param[2]
			Longueur=fp.ParamCorn.Param[3]
		elif fp.Chx[0]==0:
			L1=fp.L1.Value
			L2=fp.L2.Value
			e1=fp.e1.Value
			Longueur=fp.Longueur.Value
		P1=Base.Vector(e1,e1,0)
		S1=Part.makeBox(L1,L2,Longueur)
		S1=S1.makeThickness([S1.Faces[1],S1.Faces[3],S1.Faces[4],S1.Faces[5]],-e1,.01)
		fp.Shape=S1
		fp.Placement=pl

class TubeCarreRectangle:
	"Construction d'un profil Tubulaire carré ou rectangulaire"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","L1","TubeCarreRectangle","L1").L1=40.0
		obj.addProperty("App::PropertyDistance","L2","TubeCarreRectangle","L2").L2=40.0
		obj.addProperty("App::PropertyDistance","Epaisseur","TubeCarreRectangle","Epaisseur").Epaisseur=2.0
		obj.addProperty("App::PropertyDistance","Longueur","TubeCarreRectangle","Longueur").Longueur=200.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "L1" or prop == "L2" or prop == "Epaisseur" or prop == "Longueur":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		if fp.L1.Value == fp.Longueur.Value:
			print "Problème : L1 ne peut pas être égale à la longueur... Limitation du programme !!"
			fp.Longueur.Value=fp.L1.Value+0.1
		if fp.L2.Value == fp.Longueur.Value:
			print "Problème : L2 ne peut pas être égale à la longueur... Limitation du programme !!"
			fp.Longueur.Value=fp.L2.Value+0.1
		
		P1=Base.Vector(-fp.L1.Value/2,-fp.L2.Value/2,0)
		S1=Part.makeBox(fp.L1.Value,fp.L2.Value,fp.Longueur.Value,P1)
		
		goodedges = []
		for edge in S1.Edges:
		    l = (edge.Vertexes[-1].Point.sub(edge.Vertexes[0].Point)).Length
		    if l == fp.Longueur.Value:
		        goodedges.append(edge)		
		S1=S1.makeFillet(2*fp.Epaisseur.Value,goodedges)
		S1=S1.makeThickness([S1.Faces[1],S1.Faces[4]],-fp.Epaisseur.Value,.01)
		fp.Shape=S1
		fp.Placement=pl

class TubeCarreRectangleDeco:
	"Construction d'un profil Tubulaire carré ou rectangulaire"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","L1","TubeCarreRectangleDeco","L1").L1=40.0
		obj.addProperty("App::PropertyDistance","L2","TubeCarreRectangleDeco","L2").L2=40.0
		obj.addProperty("App::PropertyDistance","Epaisseur","TubeCarreRectangleDeco","Epaisseur").Epaisseur=2.0
		obj.addProperty("App::PropertyDistance","Longueur","TubeCarreRectangleDeco","Longueur").Longueur=200.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "L1" or prop == "L2" or prop == "Epaisseur" or prop == "Longueur":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		if fp.L1.Value == fp.Longueur.Value:
			print "Problème : L1 ne peut pas être égale à la longueur... Limitation du programme !!"
			fp.Longueur.Value=fp.L1.Value+0.1
		if fp.L2.Value == fp.Longueur.Value:
			print "Problème : L2 ne peut pas être égale à la longueur... Limitation du programme !!"
			fp.Longueur.Value=fp.L2.Value+0.1
		
		P1=Base.Vector(-fp.L1.Value/2,-fp.L2.Value/2,0)
		S1=Part.makeBox(fp.L1.Value,fp.L2.Value,fp.Longueur.Value,P1)
		
		goodedges = []
		for edge in S1.Edges:
		    l = (edge.Vertexes[-1].Point.sub(edge.Vertexes[0].Point)).Length
		    if l == fp.Longueur.Value:
		        goodedges.append(edge)		
		# S1=S1.makeFillet(2*fp.Epaisseur.Value,goodedges)
		S1=S1.makeThickness([S1.Faces[4],S1.Faces[5]],-fp.Epaisseur.Value,.01)
		fp.Shape=S1
		fp.Placement=pl
	
class ProfilIPN:
	def __init__(self, obj):
		obj.addProperty("App::PropertyEnumeration","IPN","ProfilIPN","IPN")
		obj.IPN = ['80','100','120','140','160','180','200','220','240','260','280','300','320','340','360','380','400','450','500','550','600']
		# obj.addProperty("App::PropertyDistance","h","ProfilIPN","h").h=80.0
		# obj.addProperty("App::PropertyDistance","b","ProfilIPN","b").b=42.0
		# obj.addProperty("App::PropertyDistance","tw","ProfilIPN","tw").tw=3.9
		# obj.addProperty("App::PropertyDistance","tf","ProfilIPN","tf").tf=5.9
		# obj.addProperty("App::PropertyDistance","r1","ProfilIPN","r1").r1=3.9
		# obj.addProperty("App::PropertyDistance","r2","ProfilIPN","r2").r2=2.3
		obj.addProperty("App::PropertyDistance","Longueur","ProfilIPN","Longueur").Longueur=1000.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "IPN" :
			self.execute(fp)

	def execute(self, fp):
		dimIPN=[]
		dimIPN.append([80.0,42.0,3.9,5.9,3.9,2.3])
		dimIPN.append([100.0,50.0,4.5,6.8,4.5,2.7])
		dimIPN.append([120.0,58.0,5.1,7.7,5.1,3.1])
		dimIPN.append([140.0,66.0,5.7,8.6,5.7,3.4])
		dimIPN.append([160.0,74.0,6.3,9.5,6.3,3.8])
		dimIPN.append([180.0,82.0,6.9,10.4,6.9,4.1])
		dimIPN.append([200.0,90.0,7.5,11.3,7.5,4.5])
		dimIPN.append([220.0,98.0,8.1,12.2,8.1,4.9])
		dimIPN.append([240.0,106.0,8.7,13.1,8.7,5.2])
		dimIPN.append([260.0,113.0,9.4,14.1,9.4,5.6])
		dimIPN.append([280.0,119.0,10.1,15.2,10.1,6.1])
		dimIPN.append([300.0,125.0,10.8,16.2,10.8,6.5])
		dimIPN.append([320.0,131.0,11.5,17.3,11.5,6.9])
		dimIPN.append([340.0,137.0,12.2,18.3,12.2,7.3])
		dimIPN.append([360.0,143.0,13.0,19.5,13.0,7.8])
		dimIPN.append([380.0,149.0,13.7,20.5,13.7,8.2])
		dimIPN.append([400.0,155.0,14.4,21.6,14.4,8.6])
		dimIPN.append([450.0,170.0,16.2,24.3,16.2,9.7])
		dimIPN.append([500.0,185.0,18.0,27.0,18.0,10.8])
		dimIPN.append([550.0,200.0,19.0,30.0,19.0,11.9])
		dimIPN.append([600.0,215.0,21.6,32.4,21.6,13.0])
		
		for dim in dimIPN:
			if float(fp.IPN)==dim[0]:
				ipn=dim[:]
				
		h=ipn[0]
		b=ipn[1]
		tw=ipn[2]
		tf=ipn[3]
		r1=ipn[4]
		r2=ipn[5]
		
		pl=fp.Placement
		F1=Part.makePlane(b/2,h/2)
		P1=Base.Vector(b/2,h/2-tf+14*(b/2)/200,0.0)
		P2=Base.Vector(tw/2,h/2-tf-14*(b/4-tw/2)/100,0.0)
		P3=Base.Vector(tw/2,0.0,0.0)
		P4=Base.Vector(b/2,0.0,0.0)
		L1=Part.Line(P1,P2)
		L2=Part.Line(P2,P3)
		L3=Part.Line(P3,P4)
		L4=Part.Line(P4,P1)
		F2=Part.Shape([L1,L2,L3,L4])
		F2=Part.Wire(F2.Edges)
		F2=Part.Face(F2)
		S1=F1.cut(F2)
		V1=Base.Vector(0.0,0.0,fp.Longueur.Value)
		S1=S1.extrude(V1)
		for edge in S1.Edges:
			if -0.1<edge.Vertexes[-1].X-P1.x<0.1 and -0.1<edge.Vertexes[0].X-P1.x<0.1:
				if -0.1<edge.Vertexes[-1].Y-P1.y<0.1 and -0.1<edge.Vertexes[0].Y-P1.y<0.1:
					goodedge=edge
		S1=S1.makeFillet(r2,[goodedge])
		for edge in S1.Edges:
			if -0.1<edge.Vertexes[-1].X-P2.x<0.1 and -0.1<edge.Vertexes[0].X-P2.x<0.1:
				if -0.1<edge.Vertexes[-1].Y-P2.y<0.1 and -0.1<edge.Vertexes[0].Y-P2.y<0.1:
					goodedge=edge
		S1=S1.makeFillet(r1,[goodedge])
		M0=Base.Vector(0.0,0.0,0.0)
		M1=Base.Vector(1.0,0.0,0.0)
		M2=Base.Vector(0.0,1.0,0.0)
		Sm1=S1.mirror(M0,M1)
		S1=S1.oldFuse(Sm1)
		Sm2=S1.mirror(M0,M2)
		S1=S1.oldFuse(Sm2)
		fp.Shape=S1
		fp.Placement=pl
	
#
# Tôles
#

class ToleCorniere:
	"Construction d'une tôle plié en équerre"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","Longueur","ToleCorniere","Longueur").Longueur=50.0
		obj.addProperty("App::PropertyDistance","Largeur","ToleCorniere","Largeur").Largeur=20.0
		obj.addProperty("App::PropertyDistance","Hauteur","ToleCorniere","Hauteur").Hauteur=20.0
		obj.addProperty("App::PropertyDistance","Epaisseur","ToleCorniere","Epaisseur").Epaisseur=1.0
		obj.addProperty("App::PropertyDistance","RayonPliage","ToleCorniere","Rayon de pliage").RayonPliage=2.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "Longueur" or prop == "Largeur" or prop == "Hauteur" or prop == "Epaisseur" or prop == "RayonPliage":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		P1=Base.Vector(fp.Epaisseur.Value,fp.Epaisseur.Value,0)
		
		S1=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value,fp.Longueur.Value)
		S1=S1.makeFillet(fp.RayonPliage.Value+fp.Epaisseur.Value,[S1.Edges[0]])
		
		S2=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value,fp.Longueur.Value,P1)
		S2=S2.makeFillet(fp.RayonPliage.Value,[S2.Edges[0]])
		
		fp.Shape=S1.cut(S2)	
		fp.Placement=pl

class ToleCorniereDev:
	"Développé de la tôle plié en l'équerre"
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","Source" ,"ToleCorniereDev","Source shape").Source=None
		obj.addProperty("App::PropertyDistance","PertePli","ToleCorniereDev","Perte au Pli").PertePli=2.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "Source" or prop == "PertePli":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		dev=fp.Source.Largeur.Value+fp.Source.Hauteur.Value-fp.PertePli.Value
		print "Longueur développée : ",dev
		
		P1=Base.Vector(-fp.Source.Hauteur.Value+fp.PertePli.Value,0,0)

		S1=Part.makeBox(dev,fp.Source.Epaisseur.Value,fp.Source.Longueur.Value,P1)
		
		fp.Shape=S1
		fp.Placement=pl

class ToleU:
	"Construction d'une tôle plié en U"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","Longueur","ToleU","Longueur").Longueur=100.0
		obj.addProperty("App::PropertyDistance","Largeur","ToleU","Largeur").Largeur=100.0
		obj.addProperty("App::PropertyDistance","Hauteur","ToleU","Hauteur").Hauteur=30.0
		obj.addProperty("App::PropertyDistance","Epaisseur","ToleU","Epaisseur").Epaisseur=1.0
		obj.addProperty("App::PropertyDistance","RayonPliage","ToleU","Rayon de pliage").RayonPliage=2.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "Longueur" or prop == "Largeur" or prop == "Hauteur" or prop == "Epaisseur" or prop == "RayonPliage":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		P1=Base.Vector(-fp.Largeur.Value/2,0,0)
		S1=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value,fp.Longueur.Value,P1)
				
		S1=S1.makeFillet(fp.RayonPliage.Value+fp.Epaisseur.Value,[S1.Edges[4],S1.Edges[0]])
		
		S1=S1.makeThickness([S1.Faces[1],S1.Faces[3],S1.Faces[4]],-fp.Epaisseur.Value,.01)
		
		fp.Shape=S1
		fp.Placement=pl

class ToleUDev:
	"Développé de la tôle plié en U"
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","Source" ,"ToleUDev","Source shape").Source=None
		obj.addProperty("App::PropertyDistance","PertePli","ToleUDev","Perte au Pli").PertePli=2.0
		obj.addProperty("App::PropertyFloatList","RetRapport","ToleUDev","Liste pour rapport").RetRapport
		#fp.RetRapport=[devX,devY]
		obj.Proxy = self
	def onChanged(self, fp, prop):
		if prop == "Source" or prop == "PertePli":
			self.execute(fp)
	def execute(self, fp):
		pl=fp.Placement
		dev=fp.Source.Largeur.Value+2*fp.Source.Hauteur.Value-2*fp.PertePli.Value
		print "Longueur développée : ",dev
		fp.RetRapport=[dev,fp.Source.Largeur.Value]
		P1=Base.Vector(-dev/2,0,0)#-fp.Source.Hauteur+fp.PertePli.Value-fp.Source.Longueur/2)
		S1=Part.makeBox(dev,fp.Source.Epaisseur.Value,fp.Source.Longueur.Value,P1)
		fp.Shape=S1
		fp.Placement=pl

class ToleBoite:
	"Construction d'une tôle plié en boite"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","Longueur","ToleBoite","Longueur").Longueur=200.0
		obj.addProperty("App::PropertyDistance","Largeur","ToleBoite","Largeur").Largeur=200.0
		obj.addProperty("App::PropertyDistance","Hauteur","ToleBoite","Hauteur").Hauteur=30.0
		obj.addProperty("App::PropertyDistance","Epaisseur","ToleBoite","Epaisseur").Epaisseur=1.0
		obj.addProperty("App::PropertyDistance","RayonPliage","ToleBoite","Rayon de pliage").RayonPliage=0.5
		obj.addProperty("App::PropertyEnumeration","TrouCentral","ToleBoiteFonction","Trou central")
		obj.TrouCentral = ['Sans Trou central','Avec Trou Central']
		obj.addProperty("App::PropertyDistance","DiametrePercageCentral","ToleBoiteFonction","Diametre percage central").DiametrePercageCentral=50.0
		obj.Proxy = self
	def onChanged(self, fp, prop):
		if prop == "Longueur" or prop == "Largeur" or prop == "Hauteur" or prop == "Epaisseur" or prop == "RayonPliage":
			self.execute(fp)
	def execute(self, fp):
		pl=fp.Placement
		P1=Base.Vector(-fp.Longueur.Value/2,-fp.Largeur.Value/2,0)
		P2=Base.Vector(-fp.Longueur.Value/2+fp.Epaisseur.Value,-fp.Largeur.Value/2+fp.Epaisseur.Value,fp.Epaisseur.Value)
		S1=Part.makeBox(fp.Longueur.Value/2,fp.Largeur.Value/2,fp.Hauteur.Value,P1)
		S1=S1.makeFillet(fp.RayonPliage.Value+fp.Epaisseur.Value,[S1.Edges[3],S1.Edges[8]])#,S1.Edges[7],S1.Edges[10]])
		S2=Part.makeBox(fp.Longueur.Value/2-fp.Epaisseur.Value,fp.Largeur.Value/2-fp.Epaisseur.Value,fp.Hauteur.Value-fp.Epaisseur.Value,P2)
		S2=S2.makeFillet(fp.RayonPliage.Value,[S2.Edges[3],S2.Edges[8]])#,S2.Edges[7],S2.Edges[10]])
		P3=Base.Vector(-fp.Longueur.Value/2,-fp.Largeur.Value/2,0)
		S3=Part.makeBox(fp.Epaisseur.Value,fp.Epaisseur.Value,fp.Hauteur.Value,P3)
		S4=Part.makeBox(fp.Epaisseur.Value+fp.RayonPliage.Value,fp.Epaisseur.Value+fp.RayonPliage.Value,fp.Epaisseur.Value+fp.RayonPliage.Value,P3)
		S1=S1.cut(S2)
		S1=S1.cut(S3)
		S1=S1.cut(S4)
		P1=Base.Vector(0,0,0)
		P2=Base.Vector(1,0,0)
		P3=Base.Vector(0,1,0)
		Sm1=S1.mirror(P1,P2)
		S1=S1.oldFuse(Sm1)
		Sm2=S1.mirror(P1,P3)
		S1=S1.oldFuse(Sm2)
		if fp.TrouCentral=="Avec Trou Central":
			Trou=Part.makeCylinder(fp.DiametrePercageCentral.Value/2,fp.Epaisseur.Value)
			S1=S1.cut(Trou)
		fp.Shape=S1
		fp.Placement=pl

class ToleBoiteDev:
	"Développé de la tôle plié en boite"
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","Source" ,"ToleBoiteDev","Source shape").Source=None
		obj.addProperty("App::PropertyDistance","PertePli","ToleBoiteDev","Perte au Pli").PertePli=2.0
		obj.addProperty("App::PropertyFloatList","RetRapport","ToleBoiteDev","Liste pour rapport").RetRapport
		#fp.RetRapport=[devX,devY]
		obj.Proxy = self
	def onChanged(self, fp, prop):
		if prop == "Source" or prop == "PertePli":
			self.execute(fp)
	def execute(self, fp):
		pl=fp.Placement
		devX=2*fp.Source.Hauteur.Value-2*fp.PertePli.Value+fp.Source.Longueur.Value
		devY=fp.Source.Largeur.Value-2*fp.PertePli.Value+2*fp.Source.Hauteur.Value
		print "Longueur développée suivant X : ",devX
		print "Longueur développée suivant Y : ",devY
		fp.RetRapport=[devX,devY]
		P1=Base.Vector(-devX/2,-fp.Source.Largeur.Value/2+fp.Source.Epaisseur.Value,0)
		P2=Base.Vector(fp.Source.Epaisseur.Value-fp.Source.Longueur.Value/2,-devY/2,0)
		P3=Base.Vector(0,0,fp.Source.Epaisseur.Value)
		S1=Part.makePlane(devX,fp.Source.Largeur.Value-2*fp.Source.Epaisseur.Value,P1,P3)
		S1=S1.extrude(P3)
		S2=Part.makePlane(fp.Source.Longueur.Value-2*fp.Source.Epaisseur.Value,devY,P2,P3)
		S2=S2.extrude(P3)
		S1=S1.oldFuse(S2)
		fp.Shape=S1
		fp.Placement=pl
		
class ToleZ:
	"Tôle plié en Z"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","Largeur","ToleZ","Largeur").Largeur=50.0
		obj.addProperty("App::PropertyDistance","L1","ToleZ","L1").L1=25.0
		obj.addProperty("App::PropertyDistance","Hauteur","ToleZ","Hauteur").Hauteur=100.0
		obj.addProperty("App::PropertyDistance","Epaisseur","ToleZ","Epaisseur").Epaisseur=1.0
		obj.addProperty("App::PropertyDistance","Rayon","ToleZ","Rayon de Pliage").Rayon=2.0
		obj.addProperty("App::PropertyDistance","Longueur","ToleZ","Longueur").Longueur=20.0

		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "Largeur" or prop == "L1" or prop == "Hauteur" or prop == "Epaisseur" or prop == "Rayon" or prop == "Longueur":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		if fp.L1.Value>=fp.Largeur.Value-fp.Epaisseur.Value-fp.Rayon.Value-1:
			print "Cote L1 trop grande !!!!!!!!!!!!!!"
			S1=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value,fp.Longueur.Value)
		else :
			S1=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value,fp.Longueur.Value)
			P2=Base.Vector(0,fp.Epaisseur.Value,0)
			S2=Part.makeBox(fp.L1.Value-fp.Epaisseur.Value,fp.Hauteur.Value,fp.Longueur.Value,P2)
			P3=Base.Vector(fp.L1.Value,0,0)
			S3=Part.makeBox(fp.Largeur.Value,fp.Hauteur.Value-fp.Epaisseur.Value,fp.Longueur.Value,P3)
			S1=S1.cut(S2)
			S1=S1.cut(S3)
			#Rayon intérieure de pliage
			goodedge=[]
			for edge in S1.Edges:
				if -0.1<edge.Vertexes[-1].X-fp.L1.Value+fp.Epaisseur.Value<0.1 and -0.1<edge.Vertexes[0].X-fp.L1.Value+fp.Epaisseur.Value<0.1:
					if -0.1<edge.Vertexes[-1].Y-fp.Epaisseur.Value<0.1 and -0.1<edge.Vertexes[0].Y-fp.Epaisseur.Value<0.1:
						goodedge.append(edge)
			for edge in S1.Edges:
				if -0.1<edge.Vertexes[-1].X-fp.L1.Value<0.1 and -0.1<edge.Vertexes[0].X-fp.L1.Value<0.1:
					if -0.1<edge.Vertexes[-1].Y-fp.Hauteur.Value+fp.Epaisseur.Value<0.1 and -0.1<edge.Vertexes[0].Y-fp.Hauteur.Value+fp.Epaisseur.Value<0.1:
						goodedge.append(edge)
			S1=S1.makeFillet(fp.Rayon.Value,goodedge)
			#Rayon extérieure de pliage
			goodedge=[]
			for edge in S1.Edges:
				if -0.1<edge.Vertexes[-1].X-fp.L1.Value<0.1 and -0.1<edge.Vertexes[0].X-fp.L1.Value<0.1:
					if -0.1<edge.Vertexes[-1].Y<0.1 and -0.1<edge.Vertexes[0].Y<0.1:
						goodedge.append(edge)
			for edge in S1.Edges:
				if -0.1<edge.Vertexes[-1].X-fp.L1.Value+fp.Epaisseur.Value<0.1 and -0.1<edge.Vertexes[0].X-fp.L1.Value+fp.Epaisseur.Value<0.1:
					if -0.1<edge.Vertexes[-1].Y-fp.Hauteur.Value<0.1 and -0.1<edge.Vertexes[0].Y-fp.Hauteur.Value<0.1:
						goodedge.append(edge)
			S1=S1.makeFillet(fp.Rayon.Value+fp.Epaisseur.Value,goodedge)
		fp.Shape=S1
		fp.Placement=pl
		
class ToleZDev:
	"Développé de la tôle plié en Z"
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","Source" ,"ToleZDev","Source shape").Source=None
		obj.addProperty("App::PropertyDistance","PertePli","ToleZDev","Perte au Pli").PertePli=2.0
		obj.Proxy = self

	def onChanged(self, fp, prop):
		if prop == "Source" or prop == "PertePli":
			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		dev=fp.Source.L1.Value+fp.Source.Hauteur.Value+fp.Source.Largeur.Value-fp.Source.L1.Value+fp.Source.Epaisseur.Value-2*fp.PertePli.Value
		print "Longueur développée : ",dev
		S1=Part.makeBox(dev,fp.Source.Epaisseur.Value,fp.Source.Longueur.Value)
		fp.Shape=S1
		fp.Placement=pl

class ToleOmega:
	"Tôle plié en Omega"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","Largeur","ToleOmega","Largeur").Largeur=150.0
		obj.addProperty("App::PropertyDistance","L1","ToleOmega","L1").L1=25.0
		obj.addProperty("App::PropertyDistance","L2","ToleOmega","L2").L2=25.0
		obj.addProperty("App::PropertyDistance","H1","ToleOmega","H1").H1=30.0
		obj.addProperty("App::PropertyDistance","H2","ToleOmega","H2").H2=40.0
		obj.addProperty("App::PropertyDistance","Epaisseur","ToleOmega","Epaisseur").Epaisseur=1.0
		obj.addProperty("App::PropertyDistance","Rayon","ToleOmega","Rayon").Rayon=2.0
		obj.addProperty("App::PropertyDistance","Longueur","ToleOmega","Longueur").Longueur=150.0
		obj.addProperty("App::PropertyDistance","LAppuiTheorique","ToleOmega","Longueur Appui Théorique").LAppuiTheorique
		obj.Proxy = self

#	def onChanged(self, fp, prop):
#		if prop == "Largeur" or prop == "L1" or prop == "L2" or prop == "H1" or prop == "H2" or prop == "Epaisseur" or prop == "Rayon" or prop == "Longueur":
#			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		if fp.L1.Value>=fp.Largeur.Value-fp.L2.Value-2*fp.Rayon.Value-1:
			print "Cote L1 trop grande !!!!!!!!!!!!!!"
			S1=Part.makeBox(fp.Largeur.Value,max(fp.H1.Value,fp.H2.Value),fp.Longueur.Value)
			
		elif fp.L2.Value>=fp.Largeur.Value-fp.L1.Value-2*fp.Rayon.Value-1:
			print "Cote L2 trop grande !!!!!!!!!!!!!!"
			S1=Part.makeBox(fp.Largeur.Value,max(fp.H1.Value,fp.H2.Value),fp.Longueur.Value)

		else :

			P1=Base.Vector(0,fp.Epaisseur.Value,0)
			P2=Base.Vector(fp.L1.Value-fp.Epaisseur.Value,fp.Epaisseur.Value,0)
			P3=Base.Vector(fp.L1.Value-fp.Epaisseur.Value,fp.H1.Value,0)
			P4=Base.Vector(fp.Largeur.Value-fp.L2.Value+fp.Epaisseur.Value,fp.H2.Value,0)
			P5=Base.Vector(fp.Largeur.Value-fp.L2.Value+fp.Epaisseur.Value,fp.Epaisseur.Value,0)
			P6=Base.Vector(fp.Largeur.Value,fp.Epaisseur.Value,0)
			P7=Base.Vector(fp.Largeur.Value,-10*fp.Epaisseur.Value,0)
			P8=Base.Vector(0,-10*fp.Epaisseur.Value,0)

			L1=Part.Line(P1,P2)
			L2=Part.Line(P2,P3)
			L3=Part.Line(P3,P4)
			L4=Part.Line(P4,P5)
			L5=Part.Line(P5,P6)
			L6=Part.Line(P6,P7)
			L7=Part.Line(P7,P8)
			L8=Part.Line(P8,P1)
			
			S1=Part.Shape([L1,L2,L3,L4,L5,L6,L7,L8])
			S1=Part.Wire(S1.Edges)
			S1=Part.Face(S1)
			S1=S1.extrude(Base.Vector(0,0,fp.Longueur.Value))

			S1=S1.makeFillet(fp.Rayon.Value,[S1.Edges[1],S1.Edges[13]])
			S1=S1.makeFillet(fp.Rayon.Value+fp.Epaisseur.Value,[S1.Edges[24],S1.Edges[26]])

			S1=S1.makeThickness([S1.Faces[0],S1.Faces[7],S1.Faces[9],S1.Faces[11],S1.Faces[13]],-fp.Epaisseur.Value,.01)

			A=fp.Largeur.Value-fp.L1.Value-fp.L2.Value+2*fp.Epaisseur.Value
			B=abs(fp.H2.Value-fp.H1.Value)

			if fp.H1.Value==fp.H2.Value:
				Alpha=math.pi/2
				Beta=math.pi/2
				X1=(fp.Rayon.Value+fp.Epaisseur.Value)/(math.tan((Beta)/2))
				X2=X1
			else :			
				Alpha=math.atan(B/A)
				Beta=math.atan(A/B)
				X1=(fp.Rayon.Value+fp.Epaisseur.Value)/(math.tan((Beta)/2))
				X2=abs((fp.Rayon.Value+fp.Epaisseur.Value)/(math.tan((Alpha+(math.pi)/2)/2)))
	
			
			LappuiT=math.sqrt(math.pow(A,2)+math.pow(B,2))
			Lappui=LappuiT-X1-X2

			fp.LAppuiTheorique.Value=LappuiT
			
			print "----------------------------------------------------------"
			print "Nouvelle pièce"
			print "Largeur de l'appui théorique : ",FreeCADTools.Arrondi(LappuiT,1)," mm"
			print "Largeur de l'appui haut : ",FreeCADTools.Arrondi(Lappui,1)," mm"
			print "Alpha : ",FreeCADTools.Arrondi(math.degrees(Alpha),1)," °"
			print "Beta : ",FreeCADTools.Arrondi(math.degrees(Beta),1)," °"

		fp.Shape=S1
		fp.Placement=pl
		
class ToleOmegaDev:
	"Développé de la tôle plié en Omega"
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","Source" ,"ToleOmegaDev","Source shape").Source=None
		obj.addProperty("App::PropertyDistance","PertePli","ToleOmegaDev","Perte au Pli").PertePli=2.0
		obj.Proxy = self

#	def onChanged(self, fp, prop):
#		if prop == "Source" or prop == "PertePli":
#			self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		Dev=fp.Source.L1.Value+fp.Source.H1.Value+fp.Source.H2.Value+fp.Source.L2.Value+fp.Source.LAppuiTheorique.Value-4*fp.PertePli.Value

		S1=Part.makeBox(Dev,fp.Source.Epaisseur.Value,fp.Source.Longueur.Value)

		print "Largeur developpée : ", FreeCADTools.Arrondi(Dev,1)," mm"

		fp.Shape=S1
		fp.Placement=pl

class PlatineEurocode:
	"Construction d'une platine Eurocode"
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","p1","Parametres Eurocode","p1").p1=200.0
		obj.addProperty("App::PropertyDistance","e1","Parametres Eurocode","e1").e1=20.0
		obj.addProperty("App::PropertyDistance","p2","Parametres Eurocode","p2").p2=250.0
		obj.addProperty("App::PropertyDistance","e2","Parametres Eurocode","e2").e2=20.0
		obj.addProperty("App::PropertyDistance","t","Parametres Eurocode","t").t=10.0
		obj.addProperty("App::PropertyDistance","d0","Parametres Eurocode","d0").d0=14.0
		obj.addProperty("App::PropertyDistance","rp","Autres parametres","rp").rp=5.0
		obj.addProperty("App::PropertyInteger","NbTrousp1","Autres parametres","NbTrousp1").NbTrousp1=2
		obj.addProperty("App::PropertyInteger","NbTrousp2","Autres parametres","NbTrousp2").NbTrousp2=2
		obj.Proxy = self

	#def onChanged(self, fp, prop):
		#if prop == "p1" or prop == "e1" or prop == "p2" or prop == "e2" or prop == "t" or prop == "d0" or prop == "rp" or prop == "NbTrousp1" or prop == "NbTrousp2":
			#self.execute(fp)

	def execute(self, fp):
		pl=fp.Placement
		LongueurPlatineSousCharge=fp.e1.Value*2+fp.p1.Value*(fp.NbTrousp1-1.0)
		LargeurPlatine=fp.e2.Value*2+fp.p2.Value*(fp.NbTrousp2-1)
		V1=Base.Vector(-LongueurPlatineSousCharge/2,-LargeurPlatine/2,0)
		S1=Part.makeBox(LongueurPlatineSousCharge,LargeurPlatine,fp.t.Value,V1)
		#Rayon 
		goodedges=[]
		for edge in S1.Edges:
		    l = (edge.Vertexes[-1].Point.sub(edge.Vertexes[0].Point)).Length
		    if l == fp.t.Value:
		        goodedges.append(edge)		
		S1=S1.makeFillet(fp.rp.Value,goodedges)
		#Percages
		X=[]
		X.append(-LongueurPlatineSousCharge/2+fp.e1.Value)
		Y=[]
		Y.append(-LargeurPlatine/2+fp.e2.Value)
		pers=[]
		for x in range(fp.NbTrousp1-1):
			X.append(X[x]+fp.p1.Value)
		for y in range(fp.NbTrousp2-1):
			Y.append(Y[y]+fp.p2.Value)
		for x in X:
			for y in Y:
				pers.append(Base.Vector(x,y,0))
		for per in pers:
			Per=Part.makeCylinder(fp.d0.Value/2,fp.t.Value,per)
			S1=S1.cut(Per)
		fp.Shape=S1
		fp.Placement=pl

class RapportPlatineEurocode:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","PlatineSource","Rapport","PlatineSource").PlatineSource=None
		obj.Proxy = self
	#def onChanged(self, fp, prop):
		#if prop == "PlatineSource":
			#self.execute(fp)
	def execute(self, fp):
		p1=fp.PlatineSource.p1.Value
		e1=fp.PlatineSource.e1.Value
		p2=fp.PlatineSource.p2.Value
		e2=fp.PlatineSource.e2.Value
		d0=fp.PlatineSource.d0.Value
		print "p1 	"+str(p1)
		print ""
		print "e1 	"+str(e1)
		print ""
		print "p2 	"+str(p2)
		print ""
		print "e2 	"+str(e2)
		print ""
		print "d0 	"+str(d0)
		print ""
		#Vérification e1=e2=1,5d0
		if e1==e2 and e1==1.5*d0 and e2==1.5*d0:
			print "pratique courante e1=e2=1,5d0 OK"
			print ""
		elif e1!=e2:
			print "e1 est différent de e2 :"
			print "e1="+str(e1)+" et e2="+str(e2)
			print ""
		elif e1!=1.5*d0:
			print "e1 est différent de 1,5d0 :"
			print "e1="+str(e1)+" et 1,5d0="+str(1.5*d0)
			print ""
		elif e2!=1.5*d0:
			print "e2 est différent de 1,5d0 :"
			print "e1="+str(e2)+" et 1,5d0="+str(1.5*d0)
			print ""
		#Vérification p1=p2=3d0
		if p1==p2 and p1==3*d0 and p2==3*d0:
			print "pratique courante p1=p2=3d0 OK"
		elif p1!=p2:
			print "p1 est différent de p2 :"
			print "p1="+str(p1)+" et p2="+str(p2)
			print ""
		elif p1!=3*d0:
			print "p1 est différent de 3d0 :"
			print "p1="+str(p1)+" et 3d0="+str(3*d0)
			print ""
		elif p2!=3*d0:
			print "e2 est différent de 3d0 :"
			print "e1="+str(e2)+" et 3d0="+str(3*d0)
			print ""

#
# Outils
#
		
def turnX(X):
	cam = Gui.ActiveDocument.ActiveView.getCameraNode()
	rot = coin.SbRotation()
	rot.setValue(coin.SbVec3f(1,0,0),X)
	nrot = cam.orientation.getValue() * rot
	cam.orientation = nrot

def turnY(Y):
	cam = Gui.ActiveDocument.ActiveView.getCameraNode()
	rot = coin.SbRotation()
	rot.setValue(coin.SbVec3f(0,1,0),Y)
	nrot = cam.orientation.getValue() * rot
	cam.orientation = nrot

def turnZ(Z):
	cam = Gui.ActiveDocument.ActiveView.getCameraNode()
	rot = coin.SbRotation()
	rot.setValue(coin.SbVec3f(0,0,1),Z)
	nrot = cam.orientation.getValue() * rot
	cam.orientation = nrot

def makeExtract(basesel=None,NoFace=None,NoEdge=None,NoVertex=None,name=None):
	if NoFace!= None:
		name="Extraction Face"
	elif NoEdge!= None:
		name="Extraction Edge"
	elif NoVertex!= None:
		name="Extraction Vertex"
	obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
	Extract(obj)
	obj.Components=[basesel]
	r=85.0/255.0
	g=85.0/255.0
	b=125.0/255.0
	obj.ViewObject.ShapeColor = (r,g,b,1.0)
	ViewProviderExtract(obj.ViewObject)
	if NoFace!= None:
		obj.NoFace = NoFace
	elif NoEdge!= None:
		obj.NoEdge = NoEdge
	elif NoVertex!= None:
		obj.NoVertex = NoVertex
	for comp in obj.Components:
		comp.ViewObject.hide()
	return obj

class Extract:
	"The Extract object"
	def __init__(self,obj):
		obj.addProperty("App::PropertyLinkList","Components","Base","Les objets originaux")
		obj.addProperty("App::PropertyInteger","NoFace","Base","Numero Face").NoFace=0
		obj.addProperty("App::PropertyInteger","NoEdge","Base","Numero Edge").NoEdge=0
		obj.addProperty("App::PropertyInteger","NoVertex","Base","Numero Vertex").NoVertex=0
		obj.Proxy = self
		self.Type = "Exraction"
	def execute(self,obj):
		self.createGeometry(obj)
	def onChanged(self,obj,prop):
		if prop in ["Base","NoFace","NoEdge","NoVertex"]:
			self.createGeometry(obj)
	def createGeometry(self,obj):
		if obj.Components:
			components = obj.Components[:]
			base=components[0].Shape.copy()
			# Part.show(base)
			if obj.NoFace != 0:
				if obj.NoFace <= 0:
					print "Premiere Face"
					obj.NoFace=1
				elif obj.NoFace > len(base.Faces):
					print "Derniere Face"
					obj.NoFace=len(base.Faces)
				print base
				base=base.Faces[obj.NoFace-1]
			elif obj.NoEdge != 0:
				if obj.NoEdge <= 0:
					print "Premiere Arrête"
					obj.NoEdge=1
				elif obj.NoEdge > len(base.Edges):
					print "Derniere Arrête"
					obj.NoEdge=len(base.Edges)
				base=base.Edges[obj.NoEdge-1]
			elif obj.NoVertex != 0:
				if obj.NoVertex <= 0:
					print "Premier Point"
					obj.NoVertex=1
				elif obj.NoVertex > len(base.Vertexes):
					print "Dernier Point"
					obj.NoVertex=len(base.Vertexes)
				base=base.Vertexes[obj.NoVertex-1]
			obj.Shape = base

class ViewProviderExtract:
	"A View Provider for the Wall object"
	def __init__(self,vobj):
		vobj.Proxy = self
		self.Object = vobj.Object
	def getIcon(self):
		return """
			/* XPM */
			static char * Extraction Elements_xpm[] = {
			"16 16 9 1",
			" 	c None",
			".	c #047503",
			"+	c #009E0E",
			"@	c #338498",
			"#	c #4D8D6A",
			"$	c #0ABC00",
			"%	c #46A65C",
			"&	c #6A9AA5",
			"*	c #46ADC9",
			"                ",
			"                ",
			"                ",
			"    &&&&&&      ",
			"  @@&&***&&&#.  ",
			"  ****@&#%+$$$  ",
			"  *****&%$$$$$  ",
			"  *****&%$$$$$  ",
			"  *****&%$$$$$  ",
			"  *****&%$$$$$  ",
			"  *****&%$$$$$  ",
			"  *****&%$$$$$  ",
			"    @@@&%$++.   ",
			"                ",
			"                ",
			"                "};
		"""
	def updateData(self,obj,prop):
		return

	def onChanged(self,vobj,prop):
		return

	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return

	def getDisplayModes(self,obj):
		modes=[]
		return modes

	def setDisplayMode(self,mode):
		return mode

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None 

	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return

def makeInfoVolMasse(objectslist):
	name="InfoVolMasse"
	obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
	InfoVolMasse(obj)
	ViewProviderInfoVolMasse(obj.ViewObject)
	obj.Components = objectslist
	r=85.0/255.0
	g=170.0/255.0
	b=255.0/255.0
	obj.ViewObject.ShapeColor = (r,g,b,1.0)
	obj.ViewObject.Transparency = 50
	return obj

class InfoVolMasse:
	"The Info Vol Masse object"
	def __init__(self,obj):
		obj.addProperty("App::PropertyLinkList","Components","Base","Les objets a peser")
		obj.addProperty("App::PropertyFloat","DensiteR","Base","DensiteR").DensiteR=0
		obj.addProperty("App::PropertyFloat","Masse","Base","Derniere masse calculee en kg").Masse
		obj.addProperty("App::PropertyEnumeration","Densite","Base","Densite")
		obj.Densite = ['Acier','Aluminium','Inox','Reglable']
		obj.addProperty("App::PropertyEnumeration","UniteVol","Base","UniteVol")
		obj.UniteVol = ['mm','cm','dm','m']
		obj.addProperty("App::PropertyEnumeration","UniteMasse","Base","UniteMasse")
		obj.UniteMasse = ['kg','g','Tonnes']
		obj.Proxy = self
		self.Type = "InfoVolMasse"
	def execute(self,obj):
		self.createGeometry(obj)
	def createGeometry(self,obj):
		if obj.Components:
			components = obj.Components[:]
			Vol=0
			for comp in components:
				for sol in comp.Shape.Solids:
					Vol=sol.Volume+Vol
			print "----------------------------------------------------------"
			print ""
			CDGX=[]
			CDGY=[]
			CDGZ=[]
			for comp in components:
				for sol in comp.Shape.Solids:
					CDGX.append(sol.CenterOfMass.x)
					CDGY.append(sol.CenterOfMass.y)
					CDGZ.append(sol.CenterOfMass.z)
			cdgx=moyenne(CDGX)
			cdgy=moyenne(CDGY)
			cdgz=moyenne(CDGZ)
			print "Coordonnées centre de gravité des objets suivants : (Densité identique pour tous)"
			print ""
			for comp in components:
				print "	",comp.Label
			print ""
			print "Suivant X : ",Arrondi(cdgx,2)," mm"
			print "Suivant Y : ",Arrondi(cdgy,2)," mm"
			print "Suivant Z : ",Arrondi(cdgz,2)," mm"
			print ""
			if obj.UniteVol=="mm":
				print "Volume : ", Arrondi(Vol,2), " mm^3"
			if obj.UniteVol=="cm":
				Rap=1000
				print "Volume : ", Arrondi(Vol/Rap,2), " cm^3"
			if obj.UniteVol=="dm":
				Rap=1000000				
				print "Volume : ", Arrondi(Vol/Rap,2), " dm^3"
			if obj.UniteVol=="m":
				Rap=1000000000
				print "Volume : ", Arrondi(Vol/Rap,2), " m^3"
			if obj.Densite=="Reglable":
				densite=obj.DensiteR
			elif obj.Densite=="Acier":
				densite=7.88
				obj.DensiteR=densite
			elif obj.Densite=="Aluminium":
				densite=2.7
				obj.DensiteR=densite
			elif obj.Densite=="Inox":
				densite=8.0
				obj.DensiteR=densite
			if obj.UniteMasse=="g":
				Rap=1000
				print "Masse : ", Arrondi(Vol*densite/Rap,2), " g"
			if obj.UniteMasse=="kg":
				Rap=1000000
				print "Masse : ", Arrondi(Vol*densite/Rap,2), " kg"
			if obj.UniteMasse=="Tonnes":
				Rap=1000000000
				print "Masse : ", Arrondi(Vol*densite/Rap,2), " Tonnes"
			print ""
			print "----------------------------------------------------------"
			obj.Masse=Arrondi(Vol*densite/1000000,2)
			V1=Base.Vector(cdgx,cdgy,cdgz)
			pas=10.0
			Bv1=Base.Vector(-pas/2,-pas/2,-pas/2)
			B1=Part.makeBox(pas/2,pas/2,pas/2,Bv1)
			B2=B1.copy()
			Bv2=Base.Vector(pas/2,0.0,pas/2)
			B2.translate(Bv2)
			B3=B2.copy()
			Bv3=Base.Vector(-pas/2,pas/2,0.0)
			B3.translate(Bv3)
			B4=B3.copy()
			Bv4=Base.Vector(pas/2,0.0,-pas/2)
			B4.translate(Bv4)
			S1=Part.makeSphere(pas/2)
			S1=S1.cut(B1).cut(B2).cut(B3).cut(B4)
			obj.Shape =S1
			obj.Placement.Base.x=cdgx
			obj.Placement.Base.y=cdgy
			obj.Placement.Base.z=cdgz
       
class ViewProviderInfoVolMasse:
	"A View Provider for the Face Decalage object"
	def __init__(self,vobj):
		vobj.Proxy = self
		self.Object = vobj.Object
	def getIcon(self):
		return """
			/* XPM */
			static char * Info Vol Masse_xpm[] = {
			"16 16 9 1",
			" 	c None",
			".	c #685E3C",
			"+	c #9B8733",
			"@	c #AA8900",
			"#	c #C09C04",
			"$	c #D4AE0D",
			"%	c #CAAE45",
			"&	c #C9BA7A",
			"*	c #FFCC06",
			"                ",
			"      %%%       ",
			"     %%%%%+     ",
			"     +%%%%      ",
			"    &%$$$%&.    ",
			"    $$##$$$@    ",
			"    *******#    ",
			"    *******#    ",
			"    *******#    ",
			"    *******#    ",
			"    *******#    ",
			"    *******#    ",
			"    *******#    ",
			"    *******@    ",
			"     @###@      ",
			"                "};
			"""
	def updateData(self,obj,prop):
		return

	def onChanged(self,vobj,prop):
		return

	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return

	def getDisplayModes(self,obj):
		modes=[]
		return modes

	def setDisplayMode(self,mode):
		return mode

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None 
 
	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return

def makeOldFuse(objectslist):
	name="OldFuse"
	obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
	OldFuse(obj)
	ViewProviderOldFuse(obj.ViewObject)
	obj.Components = objectslist
	for comp in obj.Components:
		comp.ViewObject.hide()
	return obj

class OldFuse:
	"The Old Fuse object"
	def __init__(self,obj):
		obj.addProperty("App::PropertyLinkList","Components","Base","Les objets a fusionner")
		self.Type = "OldFuse"
		obj.Proxy = self
	def execute(self,obj):
		self.createGeometry(obj)
	def createGeometry(self,obj):
		if obj.Components:
			components = obj.Components[:]
			base=components[0].Shape.copy()
			for n in range(len(components)-1):
					base=base.oldFuse(components[n+1].Shape)
			obj.Shape = base
       
class ViewProviderOldFuse:
	"A View Provider for the OldFuse object"
	def __init__(self,vobj):
		vobj.Proxy = self
		self.Object = vobj.Object
	def getIcon(self):
		return """
			/* XPM */
			static char * OldFuse_xpm[] = {
			"16 16 9 1",
			" 	c None",
			".	c #12282E",
			"+	c #234149",
			"@	c #3A606C",
			"#	c #9B7381",
			"$	c #498B9F",
			"%	c #3CAAC7",
			"&	c #A5909F",
			"*	c #84CBDA",
			"                ",
			"          .     ",
			"        +**$    ",
			"       $*****@  ",
			"     @********* ",
			"   +**********+ ",
			"  @**&#*****@   ",
			"   @&%%$#*$     ",
			"  +%%%%%%@.     ",
			" $%%%%%%%%%@    ",
			" +%%%%%%%%%%%.  ",
			"   @%%%%%%%%$.  ",
			"    .$%%%%%+    ",
			"      +%%@      ",
			"                ",
			"                "};
		"""
	def updateData(self,obj,prop):
		return

	def onChanged(self,vobj,prop):
		return

	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return

	def getDisplayModes(self,obj):
		modes=[]
		return modes

	def setDisplayMode(self,mode):
		return mode

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None 
 
	def claimChildren(self):
		return self.Object.Components

	def attach(self,vobj):
		self.Object = vobj.Object
		return		

#
#	Calpinage
#

def LectureFichier():
	PiecesACouper=[]
	BarresBrutes=[]
	Chutes=[]
	os.chdir(Chemin.CheminEchange(1))
	try:
		obFichier = open('Coupes Barre.txt','r')
	except:
		print "Le fichier", 'Coupes Barre.txt', "est introuvable"
	n=0
	test=0
	for ligne in obFichier.readlines():
		if n==1:
			text = ligne.split()
			if text != []:
				if ligne[0] != '#' :
					if len(text)==3:
						if text[1] == "x":
							Qte=[int(text[0])]
							Longueur=[float(text[2])]
							PiecesACouper.append((Qte[0],Longueur[0]))
					else:
						PiecesACouper.append((1,float(text[0])))
		elif n==2:
			text = ligne.split()
			if text != []:
				if ligne[0] != '#' :
					if len(text)==3:
						if text[1] == "x":
							Qte=[int(text[0])]
							Longueur=[float(text[2])]
							Chutes.append((Qte[0],Longueur[0]))
					else:
						Chutes.append((1,float(text[0])))
		if ligne[0] == '#':
			n=n+1
		
	obFichier.close
	return [PiecesACouper,Chutes]		

def Tri(Liste,Croissant):
	if len(Liste)==0:
		listetrie=Liste[:]
	else :
		if type(Liste[0])==tuple:
			Liste.sort(lambda a,b: cmp(a[1],b[1]),reverse=Croissant)
			listetrie=Liste[:]
		else:
			Liste.sort(reverse=Croissant)
			listetrie=Liste[:]
	return	listetrie
	
class Calpinage1D:
	def __init__(self, obj):
		obj.addProperty("App::PropertyDistance","EpBarreBrute","Representation","Epaisseur Barre Brute").EpBarreBrute=50.0
		obj.addProperty("App::PropertyDistance","EspaceBarresBrute","Representation","Espace entre les barres brutes").EspaceBarresBrute=50.0
		obj.addProperty("App::PropertyDistance","EpTraitCoupe","Parametres","Epaisseur Trait de coupe").EpTraitCoupe=3.0
		obj.addProperty("App::PropertyDistance","LongueurBarreBruteR","Parametres","Longueur Barre Brute").LongueurBarreBruteR=6000.0
		obj.addProperty("App::PropertyEnumeration","LongueurBarreBrute","Parametres","Choix du tri de la liste des pieces")
		obj.LongueurBarreBrute = ['6000','3000','2500','5410 (poteaux Fermod)','5800 (echelons Fermod)','6730 (echelons Fermod)','Longueur reglable']
		obj.addProperty("App::PropertyEnumeration","PiecesACouper","Tri","Choix du tri de la liste des pieces")
		obj.PiecesACouper = ['Croissant','Decroissant','Original']
		obj.addProperty("App::PropertyFloatList","PiecesACouperCroissant","Parametres","Longueurs Pieces").PiecesACouperCroissant
		obj.addProperty("App::PropertyFloatList","PiecesACouperDecroissant","Parametres","Longueurs Pieces").PiecesACouperDecroissant
		obj.addProperty("App::PropertyFloatList","PiecesACouperOriginale","Parametres","Longueurs Pieces").PiecesACouperOriginale
		obj.addProperty("App::PropertyFloatList","PiecesACouperChoix","Parametres","Longueurs Pieces").PiecesACouperChoix
		obj.addProperty("App::PropertyEnumeration","Chutes","Tri","Choix du tri de la liste des Chutes")
		obj.Chutes = ['Croissant','Decroissant','Original']
		obj.addProperty("App::PropertyFloatList","ChutesCroissant","Parametres","Longueur Chutes dispo").ChutesCroissant
		obj.addProperty("App::PropertyFloatList","ChutesDecroissant","Parametres","Longueur Chutes dispo").ChutesDecroissant
		obj.addProperty("App::PropertyFloatList","ChutesOriginal","Parametres","Longueur Chutes dispo").ChutesOriginal
		obj.addProperty("App::PropertyFloatList","ChutesChoix","Parametres","Longueur Chutes dispo").ChutesChoix
		obj.addProperty("App::PropertyFloatList","PosXPiece","Parametres","Position ne X des pieces").PosXPiece
		obj.addProperty("App::PropertyFloatList","PosYPiece","Parametres","Position ne Y des pieces").PosYPiece
		obj.addProperty("App::PropertyIntegerList","OrdreDessinPiece","Parametres","Ordre de dessin des pieces").OrdreDessinPiece
		obj.addProperty("App::PropertyIntegerList","InfoBarreBrute","Parametres","Ordre de dessin des pieces").InfoBarreBrute
		#[NbBarresBrutes]
		obj.Proxy = self

	def execute(self, fp):
		TestLMax=0
		if fp.LongueurBarreBrute=='Longueur reglable':
			longueurBarreBrute=fp.LongueurBarreBruteR
		else :
			longueurBarreBrute=float(fp.LongueurBarreBrute[0:4])
			fp.LongueurBarreBruteR=longueurBarreBrute
		if max(fp.PiecesACouperOriginale)>longueurBarreBrute:
			print "Probleme une des piece est trop longue!!!"
			TestLMax=1
		if TestLMax==0:
			if fp.PiecesACouper=='Croissant':
				pieces=fp.PiecesACouperCroissant[:]
			elif fp.PiecesACouper=='Decroissant':
				pieces=fp.PiecesACouperDecroissant[:]
			elif fp.PiecesACouper=='Original':
				pieces=fp.PiecesACouperOriginale[:]
			if fp.Chutes=='Croissant':
				chutes=fp.ChutesCroissant
			if fp.Chutes=='Decroissant':
				chutes=fp.ChutesDecroissant
			if fp.Chutes=='Original':
				chutes=fp.ChutesOriginal
			fp.PiecesACouperChoix=pieces[:]
			fp.ChutesChoix=chutes[:]
			ListRectangleChute=[]
			posXPiece=[]
			posYPiece=[]
			ordreDessinPiece=[]
			PosY=fp.EspaceBarresBrute.Value
			if len(chutes)!=0:
				for chute in chutes:
					PosX=0.0
					PosY=PosY-fp.EpBarreBrute.Value-fp.EspaceBarresBrute.Value
					V1=Base.Vector(PosX,PosY,0)
					B1=Part.makeBox(chute,fp.EpBarreBrute.Value,1.0,V1)
					ListRectangleChute.append(B1)
					for n in range(len(pieces)):
						test=0
						for no in ordreDessinPiece:
							if n==no:
								test=1
						if PosX+pieces[n] <= chute and test==0 :
							posXPiece.append(PosX)
							PosX=PosX+pieces[n]+fp.EpTraitCoupe.Value
							posYPiece.append(PosY)
							ordreDessinPiece.append(n)
			if len(pieces) < len(ordreDessinPiece):
				print "Les chutes suffisent a couper les pieces"
			else :
				if len(chutes)!=0:
					PosY=PosY-2*fp.EspaceBarresBrute.Value
				test=False
				NbBarresBrutes=0
				while test==False:
					PosX=0.0
					PosY=PosY-fp.EpBarreBrute.Value-fp.EspaceBarresBrute.Value
					V1=Base.Vector(PosX,PosY,0)
					B1=Part.makeBox(longueurBarreBrute,fp.EpBarreBrute.Value,1.0,V1)
					ListRectangleChute.append(B1)
					NbBarresBrutes=NbBarresBrutes+1
					for n in range(len(pieces)):
						test=0
						for no in ordreDessinPiece:
							if n==no:
								test=1
						if PosX+pieces[n] <= longueurBarreBrute and test==0:
							posXPiece.append(PosX)
							PosX=PosX+pieces[n]+fp.EpTraitCoupe.Value
							posYPiece.append(PosY)
							ordreDessinPiece.append(n)
					if len(pieces) > len(ordreDessinPiece):
						test=False
					else:
						test=True
			fp.PosXPiece=posXPiece[:]
			fp.PosYPiece=posYPiece[:]
			fp.OrdreDessinPiece=ordreDessinPiece[:]
			fp.InfoBarreBrute=[NbBarresBrutes]
			fp.Shape=Part.makeCompound(ListRectangleChute)

class MasterTracerPieces:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","InfosCalpinage","MasterTracerPieces","Infos Calpinage").InfosCalpinage=None
		obj.Proxy = self
	def execute(self, fp):
		ListeANettoyer=App.ActiveDocument.Objects
		for n in range(len(ListeANettoyer)):
			if ListeANettoyer[n].Name[0:2]=="Ra":
				# print "Rapport : ",ListeANettoyer[n].Name
				FreeCAD.ActiveDocument.removeObject(ListeANettoyer[n].Name)
			elif ListeANettoyer[n].Name[0:2]=="Pi":
				# print "Piece : ",ListeANettoyer[n].Name
				FreeCAD.ActiveDocument.removeObject(ListeANettoyer[n].Name)
		
		rapport=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Rapport")
		RapportCalpinage1D(rapport)
		rapport.InfosCalpinage=fp.InfosCalpinage
		pieces=[]
		PiecesC=fp.InfosCalpinage.PiecesACouperChoix[:]
		for n in range(len(fp.InfosCalpinage.OrdreDessinPiece)):
			lPiece=PiecesC[fp.InfosCalpinage.OrdreDessinPiece[n]]
			Npiece="PieceNo"+str(n+1)+"_"+str(int(lPiece))+"mm"
			pieces.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython",Npiece))
			SlaveTracerPieces(pieces[n])
			col1=100.0/255.0
			col2=10.0/255.0
			col3=250.0/255.0
			Gui.ActiveDocument.ActiveObject.ShapeColor=(col1,col2,col3)
			pieces[n].PosX=fp.InfosCalpinage.PosXPiece[n]
			pieces[n].PosY=fp.InfosCalpinage.PosYPiece[n]
			pieces[n].LPiece=lPiece
			pieces[n].HPiece=fp.InfosCalpinage.EpBarreBrute
			pieces[n].ViewObject.Proxy=0
		
class SlaveTracerPieces:			
	def __init__(self, obj):
		obj.addProperty("App::PropertyFloat","PosX","SlaveTracerPieces","Position ne X des pieces").PosX
		obj.addProperty("App::PropertyFloat","PosY","SlaveTracerPieces","Position ne Y des pieces").PosY
		obj.addProperty("App::PropertyDistance","LPiece","SlaveTracerPieces","Longueurs des pieces").LPiece
		obj.addProperty("App::PropertyDistance","HPiece","SlaveTracerPieces","Hauteur des pieces").HPiece
		obj.Proxy = self
	def execute(self, fp):
		V1=Base.Vector(fp.PosX,fp.PosY,1.0)
		P1=Part.makeBox(fp.LPiece.Value,fp.HPiece.Value,1.0,V1)
		fp.Shape=P1
		
class RapportCalpinage1D:
	def __init__(self, obj):
		obj.addProperty("App::PropertyLink","InfosCalpinage","Rapport","Infos Calpinage").InfosCalpinage=None
		obj.Proxy = self
	def execute(self, fp):
		#Calculs
		sommeLPieces=0
		for lpie in fp.InfosCalpinage.PiecesACouperChoix:
			sommeLPieces=sommeLPieces+lpie
		sommeLChutes=0
		for lcht in fp.InfosCalpinage.ChutesChoix:
			sommeLChutes=sommeLChutes+lcht
		nbBarreBrute=fp.InfosCalpinage.InfoBarreBrute[0]
		sommeLChutes=sommeLChutes+nbBarreBrute*fp.InfosCalpinage.LongueurBarreBruteR.Value
		
		Pertes=FreeCADTools.Arrondi(100.0-sommeLPieces*100.0/sommeLChutes,1)
		Pertesmm=FreeCADTools.Arrondi(sommeLChutes-sommeLPieces,1)
		longByLine=[]
		Line=[]
		n=0
		posprec=0
		for pos in fp.InfosCalpinage.PosYPiece:
			if pos==-fp.InfosCalpinage.EpBarreBrute:
				Line.append(fp.InfosCalpinage.PiecesACouperChoix[fp.InfosCalpinage.OrdreDessinPiece[n]])
			elif pos==posprec:
				Line.append(fp.InfosCalpinage.PiecesACouperChoix[fp.InfosCalpinage.OrdreDessinPiece[n]])
			else:
				longByLine.append(Line)
				Line=[]
				Line.append(fp.InfosCalpinage.PiecesACouperChoix[fp.InfosCalpinage.OrdreDessinPiece[n]])
			posprec=pos
			n=n+1
		longByLine.append(Line)
		#Ecriture fichier
		os.chdir(Chemin.CheminEchange(1))
		obFichier = open('Rapport Calpinage Barres.txt','w')
		obFichier.write("\n")
		obFichier.write("Rapport Calpinage Barres :\n")
		obFichier.write("\n")
		datEtHeure=time.strftime('%d/%m/%y %H:%M',time.localtime())
		obFichier.write("("+datEtHeure+")""\n")
		obFichier.write("\n")
		obFichier.write("--------------------------------------------------------------------------------\n")
		def rapPertes():
			obFichier.write("\n")
			obFichier.write("Total des pertes : \n")
			obFichier.write("\n")
			obFichier.write("	"+str(Pertesmm)+" mm ("+str(Pertes)+" %)\n")
			obFichier.write("\n")
		def rapConclusion():
			obFichier.write("\n")
			obFichier.write("Commande : \n")
			obFichier.write("\n")
			if nbBarreBrute==0:
				obFichier.write("	Les chutes suffisent, pas de barre neuve à commander\n")
			else :
				if nbBarreBrute==1:
					Barresss="barre neuve"
				else :
					Barresss="barres neuves"
				obFichier.write("	"+str(nbBarreBrute)+" "+Barresss+" de "+str(FreeCADTools.Arrondi(fp.InfosCalpinage.LongueurBarreBruteR.Value,0))+" mm à commander\n")
			obFichier.write("\n")
		def rapParLigne():
			obFichier.write("\n")
			obFichier.write("Rapport par barre : \n")
			obFichier.write("\n")
			obFichier.write("	Coupes dans les chutes : \n")
			obFichier.write("\n")
			inc=0
			def analyseListePiece(inc):
				somme=0
				nbpie=1
				lq=[]
				ll=[]
				for n in range(len(longByLine[inc])):
					if n==len(longByLine[inc])-1:
						lq.append(nbpie)
						ll.append(longByLine[inc][n])
					else :
						if longByLine[inc][n]==longByLine[inc][n+1]:
							nbpie=nbpie+1
						else :
							lq.append(nbpie)
							ll.append(longByLine[inc][n])
							nbpie=1
					somme=somme+longByLine[inc][n]
				for n in range(len(lq)):
					if lq[n]>1:
						PC=" pièces"
					else:
						PC=" pièce"
					obFichier.write("			"+str(lq[n])+PC+" de : "+str(FreeCADTools.Arrondi(ll[n],1))+" mm\n")
				return somme
			for chts in range(len(fp.InfosCalpinage.ChutesChoix)):
				obFichier.write("\n")
				obFichier.write("		Chute N° "+str(chts+1)+" - "+str(FreeCADTools.Arrondi(fp.InfosCalpinage.ChutesChoix[chts],1))+" mm :\n")
				obFichier.write("\n")
				somme=analyseListePiece(inc)
				reste=fp.InfosCalpinage.ChutesChoix[chts]-somme-len(longByLine[inc])*fp.InfosCalpinage.EpTraitCoupe.Value
				if reste < 0:
					reste=0.0
				obFichier.write("			reste : "+str(FreeCADTools.Arrondi(reste,1))+" mm ("+str(FreeCADTools.Arrondi(100.0*reste/(somme+reste),1))+"%)\n")
				inc=inc+1
			obFichier.write("\n")
			
		
			for pie in range(nbBarreBrute):
				obFichier.write("\n")
				
				
				obFichier.write("		Barre N° "+str(pie+1)+" - "+str(FreeCADTools.Arrondi(fp.InfosCalpinage.LongueurBarreBruteR.Value,1))+" mm :\n")
				obFichier.write("\n")
				somme=analyseListePiece(inc)
				reste=fp.InfosCalpinage.LongueurBarreBruteR.Value-somme-len(longByLine[inc])*fp.InfosCalpinage.EpTraitCoupe.Value
				if reste < 0:
					reste=0.0
				obFichier.write("			reste : "+str(FreeCADTools.Arrondi(reste,1))+" mm ("+str(FreeCADTools.Arrondi(100.0*reste/(somme+reste),1))+"%)\n")
				
				inc=inc+1
		
		rapParLigne()
		
		rapPertes()
		rapConclusion()
		
		obFichier.write("\n")
		obFichier.write("--------------------------------------------------------------------------------\n")
		obFichier.close()

#
#	Points 3D
#
		
def LectureFichierPoints3D():
	ListePoints=[]
	os.chdir(Chemin.CheminEchange(1))
	try:
		obFichier = open('Points3D.txt','r')
		for ligne in obFichier.readlines():
			text = ligne.split(",")
			if text != []:
				if ligne[0] != '#' :
					if len(text)==4:
						Labels=text[0]
						X=float(text[1])
						Y=float(text[2])
						Z=float(text[3])
						ListePoints.append([Labels,X,Y,Z])
	except:
		print "Le fichier ", 'Points3D.txt', " est introuvable"
	obFichier.close
	return ListePoints	
	
#
#	Pièces diverses
#

class Palette:
	"Palette type Eur"
	def __init__(self, obj):
		obj.Proxy = self
	# def onChanged(self, fp, prop):
		# if prop == "L1" or prop == "L2":
			# self.execute(fp)

	def execute(self, fp):
		Longueur=1200.0
		Largeur=800.0
		EpPlanche=22.0
		EpBois=100.0
		LaPlanche1=100.0
		LongBois=145.0
		Ec1=227.5
		Ec2=382.5
		Ec3=40.0
		LaBois=145.0
		LaPlanche2=LaBois
		LaPlanche3=LaPlanche1
		Chanfrein=25.0
		#Structure
		B1=Part.makeBox(Longueur,LaPlanche1,EpPlanche)
		S1=B1.copy()
		V2=Base.Vector(0,0,EpPlanche)
		B2=Part.makeBox(LongBois,LaPlanche1,EpBois,V2)
		V3=Base.Vector(0,0,EpPlanche+EpBois)
		B3=Part.makeBox(LongBois,Largeur,EpPlanche,V3)
		B4=B1.copy()
		B5=B2.copy()
		V4=Base.Vector(0,Largeur-LaPlanche1,0)
		B4.translate(V4)
		B5.translate(V4)
		S1=S1.fuse(B4)
		V6=Base.Vector(0,LaPlanche1+Ec1,0)
		B6=Part.makeBox(Longueur,LaBois,EpPlanche,V6)
		S1=S1.fuse(B6)
		V7=Base.Vector(0,LaPlanche1+Ec1,EpPlanche)
		B7=Part.makeBox(LongBois,LaBois,EpBois,V7)
		B7=B7.fuse(B5)
		B7=B7.fuse(B2)
		B7=B7.fuse(B3)
		S1=S1.fuse(B7)
		V8=Base.Vector(LongBois+Ec2,0,0)
		B8=B7.copy()
		B8.translate(V8)
		S1=S1.fuse(B8)
		V9=Base.Vector(2*(LongBois+Ec2),0,0)
		B9=B7.copy()
		B9.translate(V9)
		S1=S1.fuse(B9)
		#Plancher
		V10=Base.Vector(0,0,EpBois+2*EpPlanche)
		B10=Part.makeBox(Longueur,LaPlanche2,EpPlanche,V10)
		B11=B10.copy()
		B11.translate(V6)
		V12=Base.Vector(0,Largeur-LaPlanche2,0)
		B12=B10.copy()
		B12.translate(V12)
		S1=S1.fuse(B10).fuse(B11).fuse(B12)
		V13=Base.Vector(0,LaPlanche1+Ec1-Ec3-LaPlanche3,EpBois+2*EpPlanche)
		B13=Part.makeBox(Longueur,LaPlanche3,EpPlanche,V13)
		V14=Base.Vector(0,LaPlanche3+2*Ec3+LaBois,0)
		B14=B13.copy()
		B14.translate(V14)
		S1=S1.fuse(B13).fuse(B14)
		#S1=S1.makeChamfer(Chanfrein,[S1.Edges[4],S1.Edges[13],S1.Edges[245],S1.Edges[298]])
		fp.Shape=S1

		
		
#----------------------------------------------------
#	Menus

#	Profilés

class MCorniere:
	"Creation profil de corniere"
	def Activated(self): 
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("Corniere")

		oldDocumentObjects=App.ActiveDocument.Objects

		cor=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Corniere")
		Corniere(cor)
		cor.ViewObject.Proxy=0

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
	def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/Corniere.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Corniere', 'ToolTip': 'Creation profil de corniere'} 
		
class MTubeCarreRectangle:
	"Creation profil carre ou rectangulaire"
	def Activated(self): 
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("Tube")

		oldDocumentObjects=App.ActiveDocument.Objects

		tube=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Tube")
		TubeCarreRectangle(tube)
		tube.ViewObject.Proxy=0

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/Tube.svg" 	
		return {'Pixmap' : IconPath, 'MenuText': 'Tube', 'ToolTip': 'Creation profil de tube carre ou rectangulaire'}    

class MTubeCarreRectangleDeco:
	"Creation profil carre ou rectangulaire"
	def Activated(self): 
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("Tube")

		oldDocumentObjects=App.ActiveDocument.Objects

		tube=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Tube")
		TubeCarreRectangleDeco(tube)
		tube.ViewObject.Proxy=0

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/TubeDeco.svg" 	
		return {'Pixmap' : IconPath, 'MenuText': 'Tube', 'ToolTip': 'Creation profil de tube carre ou rectangulaire decoration'}    

class MProfilIPN:
	"Creation profil IPN"
	def Activated(self): 
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("IPN")
	
		oldDocumentObjects=App.ActiveDocument.Objects

		ipn=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","IPN")
		ProfilIPN(ipn)
		ipn.ViewObject.Proxy=0

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/IPN.svg" 	
		return {'Pixmap' : IconPath, 'MenuText': 'IPN', 'ToolTip': 'Creation profil IPN'}    

		

#	Tôles 
#

class MToleCorniere:
	"Creation de tole pliee en corniere"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("ToleCorniere")

		oldDocumentObjects=App.ActiveDocument.Objects

		tole=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleCorniere")
		ToleCorniere(tole)
		tole.ViewObject.Proxy=0

		toleDev=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleCorniereDev")
		ToleCorniereDev(toleDev)
		toleDev.Source=tole
		toleDev.ViewObject.Proxy=0

		Gui.activeDocument().ToleCorniereDev.Visibility=False
	
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/ToleCorniere.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Tole Corniere', 'ToolTip': 'Creation tole plie en corniere'}    
		
class MToleU:
	"Creation de tole pliee en U"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("ToleU")

		oldDocumentObjects=App.ActiveDocument.Objects

		tole=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleU")
		ToleU(tole)
		tole.ViewObject.Proxy=0

		toleDev=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleUDev")
		ToleUDev(toleDev)
		toleDev.Source=tole
		toleDev.ViewObject.Proxy=0

		Gui.activeDocument().ToleUDev.Visibility=False
	
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/ToleU.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Tole U', 'ToolTip': 'Creation tole plie en U'}    

class MToleBoite:
	"Creation de tole pliee en boite"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("ToleBoite")

		oldDocumentObjects=App.ActiveDocument.Objects

		tole=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleBoite")
		ToleBoite(tole)
		tole.ViewObject.Proxy=0

		toleDev=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleBoiteDev")
		ToleBoiteDev(toleDev)
		toleDev.Source=tole
		toleDev.ViewObject.Proxy=0

		Gui.activeDocument().ToleBoiteDev.Visibility=False
	
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/ToleBoite.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Tole boite', 'ToolTip': 'Creation tole plie en boite'}    


class MToleZ:
	"Creation de tole pliee en Z"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("ToleZ")

		oldDocumentObjects=App.ActiveDocument.Objects

		tole=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleZ")
		ToleZ(tole)
		tole.ViewObject.Proxy=0

		toleDev=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleZDev")
		ToleZDev(toleDev)
		toleDev.Source=tole
		toleDev.ViewObject.Proxy=0

		Gui.activeDocument().ToleZDev.Visibility=False
	
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/ToleZ.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Tole Z', 'ToolTip': 'Creation tole plie en Z'}    

class MToleOmega:
	"Creation de tole pliee en Omega"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("ToleOmega")

		oldDocumentObjects=App.ActiveDocument.Objects

		tole=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleOmega")
		ToleOmega(tole)
		tole.ViewObject.Proxy=0

		toleDev=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","ToleOmegaDev")
		ToleOmegaDev(toleDev)
		toleDev.Source=tole
		toleDev.ViewObject.Proxy=0

		Gui.activeDocument().ToleOmegaDev.Visibility=False
	
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/ToleOmega.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Tole Omega', 'ToolTip': 'Creation tole plie en Omega'}    

class MPlatineEurocode:
	"Creation de platine conforme Eurocode"
	def Activated(self): 
	
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("Platine")

		oldDocumentObjects=App.ActiveDocument.Objects
		
		platineEurocode=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","PlatineEurocode")
		PlatineEurocode(platineEurocode)
		platineEurocode.ViewObject.Proxy=0
		col1=0.0/255.0
		col2=128.0/255.0
		col3=255.0/255.0
		Gui.ActiveDocument.ActiveObject.ShapeColor=(col1,col2,col3)
		rapport=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Rapport")
		RapportPlatineEurocode(rapport)
		rapport.PlatineSource=platineEurocode
		

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
		
	def GetResources(self):
		return {'MenuText': 'Platine', 'ToolTip': 'Creation de platine conforme Eurocode'}    


#	Mise en Plan
#

def planche(Obj,nameFile):

	Echelle=3.543307

	TailleX=Obj.Object.Shape.BoundBox.XLength
	TailleY=Obj.Object.Shape.BoundBox.YLength
	TailleZ=Obj.Object.Shape.BoundBox.ZLength
	XMax=Obj.Object.Shape.BoundBox.XMax
	YMax=Obj.Object.Shape.BoundBox.YMax
	ZMax=Obj.Object.Shape.BoundBox.ZMax
	XMin=Obj.Object.Shape.BoundBox.XMin
	YMin=Obj.Object.Shape.BoundBox.YMin
	ZMin=Obj.Object.Shape.BoundBox.ZMin
	
	XCentrePiece=XMax-XMin
	YCentrePiece=YMax-YMin
	ZCentrePiece=ZMax-ZMin
	
	EspaceEntreVues=min(TailleX,TailleY,TailleZ)
	
	XCentreVueXY=2*EspaceEntreVues+TailleZ-XMin
	YCentreVueXY=2*EspaceEntreVues+TailleZ-YMin

	XCentreVueYZG=EspaceEntreVues+ZMax
	YCentreVueYZG=YCentreVueXY

	XCentreVueXZDessous=XCentreVueXY
	YCentreVueXZDessous=EspaceEntreVues+ZMax

	XCentreVueYZD=3*EspaceEntreVues+TailleZ+TailleX-ZMin
	YCentreVueYZD=YCentreVueXY

	XCentreVueXZDessus=XCentreVueXY
	YCentreVueXZDessus=3*EspaceEntreVues+TailleZ+TailleY-ZMin



	page=App.activeDocument().addObject('Drawing::FeaturePage','Page')
	page.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_Simple.svg'		
	VueXY=App.activeDocument().addObject('Drawing::FeatureViewPart','VueXY')
	VueXY.Source = Obj.Object
	VueXY.Direction = (0.0,0.0,1.0)
	VueXY.ShowHiddenLines = True
	VueXY.Scale = Echelle
	VueXY.X = XCentreVueXY*Echelle
	VueXY.Y = YCentreVueXY*Echelle
	page.addObject(VueXY)

	VueYZG=App.activeDocument().addObject('Drawing::FeatureViewPart','VueYZG')
	VueYZG.Source = Obj.Object
	VueYZG.Direction = (1.0,0.0,0.0)
	VueYZG.ShowHiddenLines = True
	VueYZG.Scale = Echelle
	VueYZG.Rotation = 180.0
	VueYZG.X = XCentreVueYZG*Echelle
	VueYZG.Y = YCentreVueYZG*Echelle
	page.addObject(VueYZG)

	VueXZDessous=App.activeDocument().addObject('Drawing::FeatureViewPart','VueXZDessous')
	VueXZDessous.Source = Obj.Object
	VueXZDessous.Direction = (0.0,1.0,0.0)
	VueXZDessous.ShowHiddenLines = True
	VueXZDessous.Scale = Echelle
	VueXZDessous.Rotation = -90.0
	VueXZDessous.X = XCentreVueXZDessous*Echelle
	VueXZDessous.Y = YCentreVueXZDessous*Echelle
	page.addObject(VueXZDessous)

	VueYZD=App.activeDocument().addObject('Drawing::FeatureViewPart','VueYZD')
	VueYZD.Source = Obj.Object
	VueYZD.Direction = (-1.0,0.0,0.0)
	VueYZD.ShowHiddenLines = True
	VueYZD.Scale = Echelle
	VueYZD.Rotation = 180
	VueYZD.X = XCentreVueYZD*Echelle
	VueYZD.Y = YCentreVueYZD*Echelle
	page.addObject(VueYZD)

	VueXZDessus=App.activeDocument().addObject('Drawing::FeatureViewPart','VueXZDessus')
	VueXZDessus.Source = Obj.Object
	VueXZDessus.Direction = (0.0,-1.0,0.0)
	VueXZDessus.ShowHiddenLines = True
	VueXZDessus.Scale = Echelle
	VueXZDessus.Rotation = -90.0
	VueXZDessus.X = XCentreVueXZDessus*Echelle
	VueXZDessus.Y = YCentreVueXZDessus*Echelle
	page.addObject(VueXZDessus)

	#Vue ISO XY Sol

	EspaceEntreVuesIso=max(TailleX,TailleY,TailleZ)*2.2

	XCentreVueIso1=XCentreVueXY
	YCentreVueIso1=YCentreVueXZDessus+EspaceEntreVuesIso

	XCentreVueIso2=XCentreVueIso1
	YCentreVueIso2=YCentreVueIso1+EspaceEntreVuesIso

	XCentreVueIso3=XCentreVueIso1+EspaceEntreVuesIso
	YCentreVueIso3=YCentreVueIso1

	XCentreVueIso4=XCentreVueIso3
	YCentreVueIso4=YCentreVueIso2

	VueIso1=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso1')
	VueIso1.Source = Obj.Object
	VueIso1.Direction = (-1.0,-1.0,0.3)
	VueIso1.Scale = Echelle
	VueIso1.ShowSmoothLines = True
	VueIso1.X = XCentreVueIso1*Echelle
	VueIso1.Y = YCentreVueIso1*Echelle
	page.addObject(VueIso1)

	VueIso2=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso2')
	VueIso2.Source = Obj.Object
	VueIso2.Direction = (-1.0,1.0,0.3)
	VueIso2.Scale = Echelle
	VueIso2.ShowSmoothLines = True
	VueIso2.X = XCentreVueIso2*Echelle
	VueIso2.Y = YCentreVueIso2*Echelle
	page.addObject(VueIso2)

	VueIso3=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso3')
	VueIso3.Source = Obj.Object
	VueIso3.Direction = (1.0,-1.0,0.3)
	VueIso3.Scale = Echelle
	VueIso3.ShowSmoothLines = True
	VueIso3.X = XCentreVueIso3*Echelle
	VueIso3.Y = YCentreVueIso3*Echelle
	page.addObject(VueIso3)

	VueIso4=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso4')
	VueIso4.Source = Obj.Object
	VueIso4.Direction = (1.0,1.0,0.3)
	VueIso4.Scale = Echelle
	VueIso4.ShowSmoothLines = True
	VueIso4.X = XCentreVueIso4*Echelle
	VueIso4.Y = YCentreVueIso4*Echelle
	page.addObject(VueIso4)
	
	#Vue ISO XZ Sol

	XCentreVueIso5=XCentreVueXY
	YCentreVueIso5=YCentreVueIso2+EspaceEntreVuesIso

	XCentreVueIso6=XCentreVueIso5
	YCentreVueIso6=YCentreVueIso5+EspaceEntreVuesIso

	XCentreVueIso7=XCentreVueIso5+EspaceEntreVuesIso
	YCentreVueIso7=YCentreVueIso5

	XCentreVueIso8=XCentreVueIso7
	YCentreVueIso8=YCentreVueIso6

	VueIso5=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso5')
	VueIso5.Source = Obj.Object
	VueIso5.Direction = (-1.0,-0.3,-1.0)
	VueIso5.Scale = Echelle
	VueIso5.ShowSmoothLines = True
	VueIso5.X = XCentreVueIso5*Echelle
	VueIso5.Y = YCentreVueIso5*Echelle
	page.addObject(VueIso5)

	VueIso6=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso6')
	VueIso6.Source = Obj.Object
	VueIso6.Direction = (-1.0,-0.3,1.0)
	VueIso6.Scale = Echelle
	VueIso6.ShowSmoothLines = True
	VueIso6.X = XCentreVueIso6*Echelle
	VueIso6.Y = YCentreVueIso6*Echelle
	page.addObject(VueIso6)

	VueIso7=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso7')
	VueIso7.Source = Obj.Object
	VueIso7.Direction = (1.0,-0.3,-1.0)
	VueIso7.Scale = Echelle
	VueIso7.ShowSmoothLines = True
	VueIso7.X = XCentreVueIso7*Echelle
	VueIso7.Y = YCentreVueIso7*Echelle
	page.addObject(VueIso7)

	VueIso8=App.activeDocument().addObject('Drawing::FeatureViewPart','VueIso8')
	VueIso8.Source = Obj.Object
	VueIso8.Direction = (1.0,-0.3,1.0)
	VueIso8.Scale = Echelle
	VueIso8.ShowSmoothLines = True
	VueIso8.X = XCentreVueIso8*Echelle
	VueIso8.Y = YCentreVueIso8*Echelle
	page.addObject(VueIso8)

	App.activeDocument().recompute()

	PageFile = open(page.PageResult,'r')
	OutFile = open(Chemin.CheminEchange(1)+nameFile+'.dxf','w')
	OutFile.write(PageFile.read())
	del OutFile,PageFile

class MAP:
	"Creation de plusieurs vues de la piece selectionnee"
	def Activated(self): 
		Pieces=Gui.Selection.getSelectionEx()
		Liste=Pieces[:]
		if len(Liste)==0:
			print "Selectionner au moins une piece"
		else :
			n=0
			for piece in Liste:
				n=n+1
				planche(piece,"Piece"+str(n))
		
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/MAP.svg" 
		return {'Pixmap' : IconPath, 'MenuText': 'Mise en plan', 'ToolTip': 'Creation de plusieurs vues de la piece selectionnee'} 


#	Rotation piece on screen
#

class TurnX5Plus: 
   def Activated(self): 
		"Tourner suivant X de 5 Degres"
		RotX=5*math.pi/180
		turnX(RotX)
   def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/TurnX5Plus.svg"   
		return {'Pixmap' : IconPath, 'MenuText': 'TurnX5Plus', 'ToolTip': 'Tourner suivant X de 5 Degres'} 

class TurnX5Moins: 
   def Activated(self): 
		"Tourner suivant X de -5 Degres"
		RotX=5*math.pi/180
		turnX(-RotX)
   def GetResources(self):
		IconPath = Chemin.iconsPath() + "/TurnX5Moins.svg"   
		return {'Pixmap' : IconPath, 'MenuText': 'TurnX5Moins', 'ToolTip': 'Tourner suivant X de -5 Degres'} 

class TurnY5Plus: 
   def Activated(self): 
		"Tourner suivant Y de 5 Degres"
		RotY=5*math.pi/180
		turnY(RotY)
   def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/TurnY5Plus.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'TurnY5Plus', 'ToolTip': 'Tourner suivant Y de 5 Degres'} 

class TurnY5Moins: 
   def Activated(self): 
		"Tourner suivant Y de -5 Degres"
		RotY=5*math.pi/180
		turnY(-RotY)
   def GetResources(self): 
		IconPath = Chemin.iconsPath() + "/TurnY5Moins.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'TurnY5Moins', 'ToolTip': 'Tourner suivant Y de -5 Degres'} 

	   
class TurnZ5Plus: 
   def Activated(self): 
		"Tourner suivant Z de 5 Degres"
		RotZ=5*math.pi/180
		turnZ(RotZ)
   def GetResources(self):
		IconPath = Chemin.iconsPath() + "/TurnZ5Plus.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'TurnZ5Plus', 'ToolTip': 'Tourner suivant Z de 5 Degres'} 

	   
class TurnZ5Moins: 
   def Activated(self): 
		"Tourner suivant Z de -5 Degres"
		RotZ=5*math.pi/180
		turnZ(-RotZ)
   def GetResources(self):
		IconPath = Chemin.iconsPath() + "/TurnZ5Moins.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'TurnZ5Moins', 'ToolTip': 'Tourner suivant Z de -5 Degres'} 
		
class MExtract:
	def Activated(self): 
		"Extrait les elements selectionnes de leur shape respectives"
		sel=Gui.Selection.getSelectionEx()
		ListeCache=[]
		if sel:
			FreeCAD.ActiveDocument.openTransaction("Extraction")
			for elts in sel:
				obj=elts.Object
				subname=elts.SubElementNames[:]
				for name in subname:
					noFace = 0
					noEdge = 0
					noVertex = 0
					if name[0:4]=="Face":
						noFace=int(name[4:7])
						makeExtract(obj,noFace,None,None)
						print "Surface : "+(str(float(int(obj.Shape.Area*100+0.49))/100))+" mm2"
					elif name[0:4]=="Edge":
						noEdge=int(name[4:7])
						makeExtract(obj,None,noEdge,None)
						print "Longueur arrête : "+(str(float(int(base.Shape.Length*100+0.49))/100))+" mm"
					elif name[0:6]=="Vertex":
						noVertex=int(name[6:9])
						makeExtract(obj,None,None,noVertex)
			App.ActiveDocument.recompute()
			FreeCAD.ActiveDocument.commitTransaction()
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/Extraction Elements.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'Extract', 'ToolTip': 'Extrait les elements selectionnes de leur shape respectives'} 

class MInfoVolMasse:
	def Activated(self): 
		"Donne le volume et la masse d'une shape"
		sel=FreeCADGui.Selection.getSelection()
		if sel:
			FreeCAD.ActiveDocument.openTransaction("Extraction")
			makeInfoVolMasse(sel)
			App.ActiveDocument.recompute()
			FreeCAD.ActiveDocument.commitTransaction()
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/Info Vol Masse.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'InfoVolMasse', 'ToolTip': 'Donne le volume et la masse d une shape'} 

class MOldFuse:
	def Activated(self): 
		"Old Fuse"
		sel=FreeCADGui.Selection.getSelection()
		if sel:
			FreeCAD.ActiveDocument.openTransaction("OldFuse")
			makeOldFuse(sel)
			App.ActiveDocument.recompute()
			FreeCAD.ActiveDocument.commitTransaction()
	def GetResources(self):
		IconPath = Chemin.iconsPath() + "/OldFuse.svg"
		return {'Pixmap' : IconPath, 'MenuText': 'OldFuse', 'ToolTip': 'Old Fuse'} 
		
class MCalpinage1D:
	def Activated(self): 
		"Calpinage 1D"
		RetourFichier=LectureFichier()
		PiecesACouper=RetourFichier[0][:]
		Chutes=RetourFichier[1][:]
		PiecesACouperOriginale=PiecesACouper[:]
		ChutesOriginal=Chutes[:]

		PiecesACouperCroissant=Tri(PiecesACouper,True)
		PiecesACouperDecroissant=Tri(PiecesACouper,False)
		ChutesCroissant=Tri(Chutes,True)
		ChutesDecroissant=Tri(Chutes,False)

		piecesACouperCroissant=[]
		for pcs in PiecesACouperCroissant:
			for n in range(pcs[0]):
				piecesACouperCroissant.append(pcs[1])
				
		piecesACouperDecroissant=[]
		for pcs in PiecesACouperDecroissant:
			for n in range(pcs[0]):
				piecesACouperDecroissant.append(pcs[1])
				
		piecesACouperOriginale=[]
		for pcs in PiecesACouperOriginale:
			for n in range(pcs[0]):
				piecesACouperOriginale.append(pcs[1])
				
		chutesCroissant=[]
		for pcs in ChutesCroissant:
			for n in range(pcs[0]):
				chutesCroissant.append(pcs[1])

		chutesDecroissant=[]
		for pcs in ChutesDecroissant:
			for n in range(pcs[0]):
				chutesDecroissant.append(pcs[1])

		chutesOriginal=[]
		for pcs in ChutesOriginal:
			for n in range(pcs[0]):
				chutesOriginal.append(pcs[1])
				
		FreeCAD.newDocument("Calpinage1D")
		col1=220.0/255.0
		col2=220.0/255.0
		col3=127.0/255.0
		calpinage=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Barres")
		Calpinage1D(calpinage)
		calpinage.PiecesACouperCroissant=piecesACouperCroissant
		calpinage.PiecesACouperDecroissant=piecesACouperDecroissant
		calpinage.PiecesACouperOriginale=piecesACouperOriginale
		calpinage.ChutesCroissant=chutesCroissant
		calpinage.ChutesDecroissant=chutesDecroissant
		calpinage.ChutesOriginal=chutesOriginal
		Gui.ActiveDocument.ActiveObject.ShapeColor=(col1,col2,col3)
		calpinage.ViewObject.Proxy=0

		tracePieces=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","MasterPieces")
		MasterTracerPieces(tracePieces)
		tracePieces.InfosCalpinage=calpinage
		tracePieces.ViewObject.Proxy=0

		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")   
	def GetResources(self): 
		return {'MenuText': 'Calpinage1D', 'ToolTip': 'Calpinage de barres'} 	   

class MPoints3D:
	def Activated(self): 
		"Import Points 3D"
		if FreeCAD.ActiveDocument==None:
			FreeCAD.newDocument("Points3D")

		oldDocumentObjects=App.ActiveDocument.Objects	
		RetourFichier=LectureFichierPoints3D()

		for n in range(len(RetourFichier)):
			print "\nPoint No ",n+1," :\n  Label : ",RetourFichier[n][0]," \n  X = ",RetourFichier[n][1],"\n  Y = ",RetourFichier[n][2],"\n  Z = ",RetourFichier[n][3]
			Draft.makePoint(X=RetourFichier[n][1], Y=RetourFichier[n][2], Z=RetourFichier[n][3],color=None,name = RetourFichier[n][0], point_size= 4)
			
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
  
	def GetResources(self): 
		return {'MenuText': 'ImportPoints3D', 'ToolTip': 'Import Points 3D'} 	   
		
#	
#	Palette

class MPalette:
	"Creation Palette type Eur"
	def Activated(self): 
		FreeCAD.newDocument("Palette")
		palette=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Palette")
		Palette(palette)
		palette.ViewObject.Proxy=0
		App.ActiveDocument.recompute()
		Gui.SendMsgToActiveView("ViewFit")
	def GetResources(self): 
		return {'MenuText': 'Palette', 'ToolTip': 'Palette'} 



def proceed():
	FreeCAD.newDocument("Palette")
	palette=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Palette")
	Palette(palette)
	palette.ViewObject.Proxy=0
	App.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")

		
FreeCADGui.addCommand('M_Corniere', MCorniere())
FreeCADGui.addCommand('M_TubeCarreRectangle', MTubeCarreRectangle())
FreeCADGui.addCommand('M_TubeCarreRectangleDeco', MTubeCarreRectangleDeco())
FreeCADGui.addCommand('M_ProfilIPN', MProfilIPN())
FreeCADGui.addCommand('M_ToleCorniere', MToleCorniere())
FreeCADGui.addCommand('M_ToleU', MToleU())
FreeCADGui.addCommand('M_ToleBoite', MToleBoite())
FreeCADGui.addCommand('M_ToleZ', MToleZ())
FreeCADGui.addCommand('M_ToleOmega', MToleOmega())
FreeCADGui.addCommand('M_MAP', MAP())
FreeCADGui.addCommand('M_TurnX5Plus', TurnX5Plus())
FreeCADGui.addCommand('M_TurnX5Moins', TurnX5Moins())
FreeCADGui.addCommand('M_TurnY5Plus', TurnY5Plus())
FreeCADGui.addCommand('M_TurnY5Moins', TurnY5Moins())
FreeCADGui.addCommand('M_TurnZ5Plus', TurnZ5Plus())
FreeCADGui.addCommand('M_TurnZ5Moins', TurnZ5Moins())
FreeCADGui.addCommand('M_Extract', MExtract())
FreeCADGui.addCommand('M_InfoVolMasse', MInfoVolMasse())
FreeCADGui.addCommand('M_OldFuse', MOldFuse())
FreeCADGui.addCommand('M_MCalpinage1D', MCalpinage1D())
FreeCADGui.addCommand('M_MPoints3D', MPoints3D())
FreeCADGui.addCommand('M_PlatineEurocode', MPlatineEurocode())
FreeCADGui.addCommand('M_Palette', MPalette())


