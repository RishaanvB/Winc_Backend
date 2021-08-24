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
Ik heb zoveel mogelijk gefixt wat ik even snel kon doen, voor zover ik kan zien, werkt alles, behalve de reset email in de productie build.
Die ga/heb ik heb ook weggehaald uit de productiebuild. In de devbuild werkt die wel. 
Bedankt
