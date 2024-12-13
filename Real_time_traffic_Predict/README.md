# Real_time_traffic_Predict

## API Détails de l'Incident

### Description
L'API Détails de l'incident fournit des informations sur les incidents de circulation dans une zone de délimitation donnée ou sur ceux qui l'intersectent. 

### Méthodes d'API
- **GET** : Pour récupérer des informations via des coordonnées (bbox) ou des identifiants (ids).
- **POST** : Pour envoyer jusqu'à 100 identifiants d'incidents.

### Requêtes Exemple

#### GET avec BBox
```bash
curl 'https://api.tomtom.com/traffic/services/5/incidentDetails?key=YOUR_API_KEY&bbox=4.885459,52.369343,4.897883,52.374963&fields={incidents{type,geometry{type,coordinates},properties{iconCategory}}}&language=en-GB&t=1111&timeValidityFilter=present'
