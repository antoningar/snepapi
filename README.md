# SNEPAPI
Une api non officiel de la snep qui vous permet d'acceder à toutes les certifications decernées par la snep.  
Vous pouvez toutes les consulter (100 par requêtes) ou les filtrer via artiste, categorie (albums ou singles) ou certifiaction (or, platine...).  

## Utilisation
Dans un premier temps il vous faudra récupérer un token.  
Ensuite, il vous faudra ajouter dans chacune de vos requêtes votre token dans le header :  
```json
"Authorization": "Bearer <your_token>"
```

## Documentation
L'url de base est :
https://rapdata.fr/api  

### Endpoints
Routes | Description
------------ | -------------
`GET /token` | Récupération d'un token (valable indéfiniment)
`GET /certifications` | Récupération de toutes les certifications (suivre l'attribut next de la reponse pour naviguer 100 par 100)
`GET /certifications/search?{filter}={data}` | Recherche via filtre, remplacer {filter} par "artist", "category" ou "certifications" et {data} par le filtre voulut
