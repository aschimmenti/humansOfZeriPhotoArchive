import rdflib
import pprint
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
import numpy as np 
import matplotlib.pyplot as plt 

g = rdflib.ConjunctiveGraph()
result = g.parse("first_tut/resources/artchives_enhanced.nq", format='nquads')

wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

fototeca_zeri = rdflib.term.URIRef('https://w3id.org/artchives/collectionfototeca-zeri')

for s, p, o in g.triples((fototeca_zeri, None, None)): 
    print("fototeca", p, o)

for s, p, o in g.triples((fototeca_zeri, wdt.P921, None)): 
    print(o)

#queries for each subject present in the fototeca_zeri 

artists = [wd.Q37562, wd.Q42207, wd.Q7814, wd.Q2632216, wd.Q19569585, wd.Q2886111, wd.Q160538, wd.Q3713796]

for a in artists: 
    for s, p, o in g.triples((a, None, None)): 
        print(a, p, o)
#only information is rdf-schema#label 
#maybe add some info about what the fototeca zeri has about it? 

covered_periods = [wd.Q12554, wd.Q7017, wd.Q7016, wd.Q7018]

for c in covered_periods: 
    for s, p, o in g.triples((c, None, None)): 
        print("period properties & objects")
        print(s, p, o)
    for s, p, o in g.triples((None, None, c)): 
        print("period as an object")
        print(s,p,o)


fototeca_photographers = [wd.Q64212, wd.Q449754, wd.Q2412846, wd.Q102280734, wd.Q3441292, wd.Q3160907, wd.Q2412846, wd.Q365683, wd.Q2346257, wd.Q644689]
#Q3160907 is James Anderson; it could also be his son, but we aren't sure 100% 

for f in fototeca_photographers: 
    for s, p, o in g.triples((None, None, f)): 
        print("aaa")
        print(f, p, o)
    for s, p, o in g.triples((f, None, None)): 
        print("aaa")
        print(f, p, o)


Federico = wd.Q1089074
for s, p, o in g.triples((Federico, None, None)):
    print(p, o)



#aggiungere tecniche fotografiche
wd.Q64212 = ["nome= Giorgio Sommer", "anno di nascita= 1834", "anno di morte= 1914", "luogo di nascita=Frankfurt am Main", "cofc=Germany, Kindom of Italy", "occupation= photographer", "work location= Naples - (Rome - Florence)", "main work = Dintorni di Napoli", "subjects = Musei Vaticani, Museo archeologico nazionale di Napoli, Pompei", "has work in the collection=Städel Museum, Minneapolis Institute of Art, Art Institute of Chicago, The Nelson-Atkins Museum of Art, National Gallery of Victoria, National Gallery of Art,  National Gallery of Canada, Musée national des beaux-arts du Québec, Museum of New Zealand Te Papa Tongarewa, Museum of Modern Art, National Museum of World Cultures, Netherlands Photo Museum, Wereldmuseum Rotterdam, Metropolitan Museum of Art, Photography Collection of the New York Public Library, Harry Ransom Center, Cleveland Museum of Art"]

wd.Q449754 = ["nome = Carlo Naya","anno di nascita= 1816", "anno di morte= 1882", "luogo di nascita= Tronzano Vercellese", "cofc= Kingdom of Italy, Kingdom of Sardinia", "occupation= photographer", "work location= Venice", "main work = Vedute di Venezia" "subjects = cappella degli scrovegni (giotto), architettura, venezia", "has work in the collection= Archivio Naya-Bohm, National Gallery of Canada, Metropolitan Museum of Art, Photography Collection of the New York Public Library, National Museum in Warsaw"]

wd.Q2412846 = ["nome = Paolo Lombardi", "anno di nascita= 1827", "anno di morte= 1890", "luogo di nascita= Siena", "cofc= Kingdom of Italy", "occupation=photographer", "work location= Siena", "main work = Pavimento del Duomo di Siena", "subjects = opere d'arte senesi", "has work in the collection= National Gallery of Canada, Museum of Modern Art, Photography Collection of the New York Public Library"]

wd.Q102280734 = ["nome = Eugenio Fiorentini", "anno di nascita= ", "anno di morte=", "luogo di nascita=", "cofc=", "occupation= photographer", "work location=", "has work in the collection="]

wd.Q3441292 = ["nome = Romualdo Moscioni", "anno di nascita= 1849 ", "anno di morte= 1925", "luogo di nascita= Viterbo", "cofc= Kingdom of Italy", "occupation= photographer", "work location= Roma", "main work =  Apulia Monumentale", "subjects = fotografie archeologiche" , "knows = Moscioni, Fratelli Alinari", "has work in the collection= "]

wd.Q3160907 = ["nome = James Anderson" ,"anno di nascita= 1813", "anno di morte= 1877", "luogo di nascita= Cumbria", "cofc= Kingdom of Italy, United Kingdom", "occupation= photographer", "work location= Roma", "subjects = Roma, ancient art, sculpture, architecture, Rinascimento" "related = Getty" "knows = Fratelli Alinari", "has work in the collection= Museo del Prado, The Nelson-Atkins Museum of Art, National Gallery of Art, National Gallery of Canada, Museum of Modern Art, Photography Collection of the New York Public Library"]

wd.Q365683 = ["nome = Adolphe Braun","anno di nascita= 1812", "anno di morte= 1877", "luogo di nascita= Besançon", "cofc= France", "occupation= photographer", "work location=", "subjects = still life, paintings, drawings, lithographs, engravings, sculpture", "has work in the collection= Minneapolis Institute of Art, Art Institute of Chicago, The Nelson-Atkins Museum of Art, National Gallery of Victoria, National Gallery of Art, National Gallery of Canada, Musée national des beaux-arts du Québec, Library of Congress, Museum of Modern Art, National Museum of World Cultures, Victoria and Albert Museum, Photography Collection of the New York Public Library, Metropolitan Museum of Art, Cleveland Museum of Art"]

wd.Q2346257 = ["nome = Giacomo Brogi","anno di nascita= 1822", "anno di morte= 1881", "luogo di nascita= Florence", "cofc= Kingdom of Italy", "occupation= photographer, architectural photographer", "work location= Florence", "subjects = still life, ritratti, opere d'arte", "has work in the collection= National Gallery of Canada, Netherlands Photo Museum, Wereldmuseum Rotterdam, Photography Collection of the New York Public Library"]

wd.Q644689 = ["nome = Fratelli Alinari", "anno di nascita= ", "anno di morte=", "luogo di nascita=", "cofc=", "occupation= photographer", "work location= Florence", "subjects = art, Tuscany, Latium, Uffizi, drawings of Raffaello" "knows = James Anderson, Moscioni", "has work in the collection= National Museum of World Cultures, Wereldmuseum Rotterdam, Netherlands Photo Museum, Museum of New Zealand Te Papa Tongarewa, National Gallery of Victoria, Photography Collection of the New York Public Library"]

#All the objects in this list are the main subjects as of now listed in 
#http://www.wikidata.org/entity/Q37562 #donatello
#http://www.wikidata.org/entity/Q42207  #caravaggio 
#http://www.wikidata.org/entity/Q860861 #scultura
#http://www.wikidata.org/entity/Q2632216 #Scipione Pulzone
#http://www.wikidata.org/entity/Q12554   #Middle Ages
#http://www.wikidata.org/entity/Q19997511 #Evelyn Sandberg Vavalà
#http://www.wikidata.org/entity/Q15711026 #altarpiece 
#http://www.wikidata.org/entity/Q19569585 #Master of the Hartford Still-Life
#http://www.wikidata.org/entity/Q41493  #ancient history
#http://www.wikidata.org/entity/Q1572315 #collotype technique
#http://www.wikidata.org/entity/Q2886111 #Bartolomeo di Tommaso
#http://www.wikidata.org/entity/Q172984 #gelatin silver process
#http://www.wikidata.org/entity/Q207241 #applied arts
#http://www.wikidata.org/entity/Q1278452 #polyptych 
#http://www.wikidata.org/entity/Q1361667 #Roberto Longhi
#http://www.wikidata.org/entity/Q37853 #Baroque 
#http://www.wikidata.org/entity/Q7075 #library 
#http://www.wikidata.org/entity/Q131808 #Mannerism 
#http://www.wikidata.org/entity/Q7017 #16th century
#http://www.wikidata.org/entity/Q3147735 #Christian iconography
#http://www.wikidata.org/entity/Q945313 #cassone 
#http://www.wikidata.org/entity/Q7016 #17th century
#http://www.wikidata.org/entity/Q9134 #mythology 
#http://www.wikidata.org/entity/Q174705 #oil painting
#http://www.wikidata.org/entity/Q1400853 #portrait painting
#http://www.wikidata.org/entity/Q623 #carbon 
#http://www.wikidata.org/entity/Q160538 #Gian Lorenzo Bernini
#http://www.wikidata.org/entity/Q134194 #fresco painting 
#http://www.wikidata.org/entity/Q19754125 #Umberto Gnoli
#http://www.wikidata.org/entity/Q3609940 #Alessandro Contini Bonacossi
#http://www.wikidata.org/entity/Q2245140 #Fra Carnevale 
#http://www.wikidata.org/entity/Q170571 #still life
#http://www.wikidata.org/entity/Q3619936 #Antonio Muñoz 
#http://www.wikidata.org/entity/Q2528876 #Vittorio Cini 
#http://www.wikidata.org/entity/Q7018 #15th century
#http://www.wikidata.org/entity/Q19997512 #Everett Fahy
#http://www.wikidata.org/entity/Q4692 #Renaissance 
#http://www.wikidata.org/entity/Q3713796  #Donato de' Bardi
#http://www.wikidata.org/entity/Q166118 #archives 
#http://www.wikidata.org/entity/Q359047 #Bernard Berenson
#http://www.wikidata.org/entity/Q580807 #albumen print
#http://www.wikidata.org/entity/Q348024 #Carlo Crivelli
#https://w3id.org/artchives/MD1556356158493
#http://www.wikidata.org/entity/Q59529805 #Guglielmo Matthiae
#http://www.wikidata.org/entity/Q7814 #Giotto di Bondone


#probably it's possible to connect the fototeca to other collections with the same time coverage 

x =  """ period as an object
https://w3id.org/artchives/collectionernst-kitzinger-papers- https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q12554
period as an object
https://w3id.org/artchives/collectionnachlass-otto-lehmannbrockhaus http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554
period as an object
https://w3id.org/artchives/collectionfototeca-zeri https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q12554       
period as an object
https://w3id.org/artchives/collectionnachlass-kurt-badt https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q12554  
period as an object
https://w3id.org/artchives/collectionnachlass-werner-cohn https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q12554period as an object
https://w3id.org/artchives/collectionernst-kitzinger-papers- http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554period as an object
http://www.wikidata.org/entity/Q60185 http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554
period as an object
https://w3id.org/artchives/collectionfototeca-zeri http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554
period as an object
https://w3id.org/artchives/collectionnachlass-werner-cohn http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554   
period as an object
https://w3id.org/artchives/collectionnachlass-otto-lehmannbrockhaus https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q12554
period as an object
https://w3id.org/artchives/collectionnachlass-kurt-badt http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q12554     
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.wikidata.org/prop/direct/P582 1600-12-31T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label     16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label              16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label                16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label        16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label            16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.wikidata.org/prop/direct/P580 1501-01-11T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label   16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label          16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label       16th century
period properties & objects
http://www.wikidata.org/entity/Q7017 http://www.w3.org/2000/01/rdf-schema#label                            16th century
period as an object
https://w3id.org/artchives/collectiongustav-ludwigvermachtnis https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectiongustav-ludwigvermachtnis http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017period as an object
https://w3id.org/artchives/collectionfototeca-zeri https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017        
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionfototeca-fahy https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017        
period as an object
https://w3id.org/artchives/collectionfototeca-stefano-tumidei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionnachlass-kurt-badt https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017   
period as an object
https://w3id.org/artchives/collectionfototeca-zeri http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017period as an object
https://w3id.org/artchives/collectionnachlass-wolfgang-lotz https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionjulius-s-held-papers https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017 
period as an object
https://w3id.org/artchives/collectionnachlass-kurt-badt http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017      
period as an object
https://w3id.org/artchives/collectionfototeca-fahy http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionnachlass-wolfgang-lotz http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017  
period as an object
https://w3id.org/artchives/collectionfototeca-stefano-tumidei http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017period as an object
https://w3id.org/artchives/collectionjulius-s-held-papers http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017    
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7017
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7017  
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label                17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label                       17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.wikidata.org/prop/direct/P580 1601-01-01T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label            17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label           17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.wikidata.org/prop/direct/P582 1700-12-31T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label                            17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label          17th century
period properties & objects
http://www.wikidata.org/entity/Q7016 http://www.w3.org/2000/01/rdf-schema#label       17th century
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016  
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-zeri https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016        
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionluigi-salerno-research-papers https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-stefano-tumidei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-zeri http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionluigi-salerno-research-papers http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016period as an object
https://w3id.org/artchives/collectionnachlass-wolfgang-lotz https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016
period as an object
https://w3id.org/artchives/collectionfototeca-stefano-tumidei http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016period as an object
https://w3id.org/artchives/collectionjulius-s-held-papers https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7016 
period as an object
https://w3id.org/artchives/collectionnachlass-wolfgang-lotz http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016  
period as an object
https://w3id.org/artchives/collectionjulius-s-held-papers http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7016    
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label          15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label            15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label           15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.wikidata.org/prop/direct/P582 1500-01-01T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.wikidata.org/prop/direct/P580 1401-01-01T00:00:00+00:00
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label              15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label                            15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label        15th century
period properties & objects
http://www.wikidata.org/entity/Q7018 http://www.w3.org/2000/01/rdf-schema#label                15th century
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionjohn-popehennessy-papers https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionarchivio-luisa-vertova http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018  
period as an object
https://w3id.org/artchives/collectiongustav-ludwigvermachtnis https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionjohn-popehennessy-papers http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018period as an object
https://w3id.org/artchives/collectiongustav-ludwigvermachtnis http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018period as an object
https://w3id.org/artchives/collectionfototeca-zeri https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018        
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionfototeca-fahy https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018        
period as an object
https://w3id.org/artchives/collectionfototeca-stefano-tumidei https://w3id.org/artchives/hasSubjectPeriod http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionnachlass-fritz-heinemann-notizen-zur-venezianischen-malerei http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionfototeca-zeri http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018
period as an object
https://w3id.org/artchives/collectionfototeca-julian-kliemann http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018period as an object
https://w3id.org/artchives/collectionfototeca-fahy http://www.wikidata.org/prop/direct/P921 http://www.wikidata.org/entity/Q7018
period as an object"""



regex_for_Q = "Q[\d]+"
