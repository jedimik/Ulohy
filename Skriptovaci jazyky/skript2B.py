import hl7
import json
import sys
#Zisk dat
#cilovePID="2011034"
#cilenycas="20110810093156"
def main(vystup,cilovePID,cilenycas):
    try:
        puvodnidata=open(cilovePID+".txt","r")
    except:
        return ("Zapsal jste neexistujici PID.")
    novadata=""
    for x in puvodnidata:
        novadata+=x
    novadata=novadata.replace("\n","\r")    
    h=hl7.parse(novadata)

    pomoc=0
    prvni_index=0 #prvni index v h[index] pro OBX
    posledni_index=0 #posledni index v h[index] pro OBX
    StartPozice=0
    OBXindex=0
    Pozice=False
    Start=False
    for index,x in enumerate(h):
        if len(h[index])>=7 and str(h[index][7])==str(cilenycas) and Pozice==False:
            Pozice=True
            StartPozice=index
            mehehe=index#pocitani s indexem, kde je poprve cileny cas
        if index>=StartPozice and str(h[index][0])!="MSH" and Pozice==True:
            StartPozice+=1
            if len(h[StartPozice])>1 and str(h[StartPozice][1])=="1" and str(h[StartPozice][0])=="OBX":
                if prvni_index==0:
                    prvni_index=index
                Start=True
            if len(h[StartPozice])>1 and str(h[StartPozice][0])=="MSH" and Start==True:
                if posledni_index==0:
                    posledni_index=StartPozice-1#kvuli te naplnene podmince odecit MSH/ mezera nevadi
                break
    if Pozice==False:
        return("Napsal jste spatny cas, takovy tu neexistuje")
    
    #Zpracovani json
    component=0
    main={"resourceType":"Observation", "subject":cilovePID,\
        "effectiveDateTime":cilenycas,"effectivePeriod":"1","effectiveTiming":"min"}
    for x in range(prvni_index,posledni_index):
        component+=1
        system="http://loinc.org"
        zmenit="zmenit"
        display=str(h[x][3])[13:]
        value=str(h[x][5])
        unit=str(h[x][6]) # Pro dani do code, by bylo potreba namapovat kazdy bpm/min/% zvlast - nedohledal jsem vse
        componenta={"component"+str(component):[{"code":{"coding":[{"system":system,\
        "code":"Kod v Loincu podle vitalniho parametru","display":display}]},"valueQuantity":[{"value":value,\
        "unit":unit,"code":unit}]}]}
        main.update(componenta)
        f = open(vystup+".txt","w")
        f.write(json.dumps(main, indent=4))
        f.close
    return(main)
        
arguments = len(sys.argv) - 1
if arguments==3:
    print(json.dumps(main(sys.argv[1],sys.argv[2],sys.argv[3]), indent=4))
    main(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    print("Musite zadat tri argumenty. Prvni nazev vystup Souboru, Druhy idPacienta a treti pote Cas")

