Voor diegene die het gaat nakijken:

De functies die bij de opdracht horen staan in main.py tm ong regel 90 en models staan in models.py. Staat ook een comment bij wanneer de functies starten die niet bij de opdracht horen.  

Er zitten een paar producten in de database, en 1 user. 
Als je hem naar je local cloned, is het volgende genoeg om hem werkend te krijgen(als het goed is):  

```
flask run
```

Voor als je de productiebuild wilt zien:
https://betsy-webshop.herokuapp.com/home

Git repo:  https://github.com/RishaanvB/betsy-webshop_deploy

Ze zijn nagenoeg hetzelfde op wat installatiebestandjes na. En regel 189 is anders in  'template/product_featurette.html'.

Productiebuild is nog wel wat buggy.  
Paar dingen werken niet echt hetzelfde zoals in de devbuild; 

-reset email werkt niet-> 500 error  

-bij foute invoer van een form -->500 error  

en wss nog wat andere dingen. 

Bedankt
