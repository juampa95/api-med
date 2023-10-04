<h1>Aplicacion WEB para gestion de pacientes y medicamentos dentro de insitutciones sanitarias </h1>

El objetivo de este repositorio es desarrollar una aplicacion web que permita gestionar los medicamentos 
dentro de una institucion sanitaria. No solamente busca realizar un control de stock, sino que tambien
apunta a un seguimiento de administracion de medicamentos que identifique de manera clara a todos los 
involucrados en el suministro del medicamento especifico. Entre otras cosas, busca detallar:

-  Quien autorizo una receta para un paciente
-  Quien cargo los medicamentos en esa receta
-  Que medicamentos fueron suministrados y cuando
-  A que paciente fueron suministrados

  <h2>Esquema del proyecto</h2>

  - Base de datos POSTGREST (migraciones mediante alembic)
  - API con FastAPI en pyhton 3.9
  - Autenticacion mediante tokens JWT
  - Frontend React (pendiente)

El inicio de este proyecto, parte de el siguiente repositorio propio https://github.com/juampa95/api_vercel en donde
se realizo un desarrollo similar, pero se desplego en Vercel. Actualmente se encuentra activo y es posible 
acceder a su API y realizar diferentes solicitudes. En la version actual del proyecto, estas solicitudes estaran 
limitadas al nivel de acceso que tenga la persona que este logueada en ese momento. 

---

**Este proyecto esta en constante desarrollo e innovacion por lo que no me encuentro obligado a seguir 
usando el esquema propuesto.**

