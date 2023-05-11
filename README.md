# Dead simple name-to-structure with PubChem synonyms

Build and run docker image

```
docker build -t n2s --progress plain
docker run -p80:80 n2s
```

Endpoints
- is chemical: http://127.0.0.1/is-chemical/aspirin
- name to structure: http://127.0.0.1/name-to-structure/aspirin