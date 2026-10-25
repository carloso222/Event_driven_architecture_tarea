## Uso de IA

Este proyecto se desarrolló con apoyo de Claude (asistente de IA), que generó la mayor parte del código.

Mi participación:
- Definí los requisitos a partir del enunciado de la tarea y el diagrama visto en clase.
- Configuré el entorno (Docker Desktop) y el repositorio en GitHub.
- Ejecuté y probé el sistema en mi computadora, identifiqué errores (líneas corruptas en el log,
  servicios que no se conectaban a RabbitMQ al arrancar) y los reporté para corregirlos.
- Decidí simplificar la implementación para cubrir únicamente lo que pide la tarea.
- Verifiqué que el flujo completo genere todos los eventos esperados.
# Event-Driven Architecture — Place an order for a book

Simulación del flujo marcado en verde del caso visto en clase, con **RabbitMQ** (pika).
Cada servicio y el broker corren en un contenedor separado. No se hacen cobros ni se envían
correos: los servicios solo consumen y generan eventos.

## Flujo

| Servicio | Consume | Produce |
|---|---|---|
| order-placement-service | `place_order` | `order_placed` |
| payment-service | `order_placed` | `payment_applied` |
| order-fulfillment-service | `payment_applied` | `order_fulfilled` |
| shipping-service | `order_fulfilled` | `order_shipped` |
| notification-service | `order_placed`, `order_fulfilled`, `order_shipped` | `email_sent` |

## Estructura de un evento

```json
{
  "event_id": "uuid",
  "event_type": "order_placed",
  "timestamp": "2026-10-25T06:49:01.432+00:00",
  "producer": "order-placement-service",
  "payload": {"order_id": "1a2b3c4d", "book": "Fundamentals of Software Architecture", "quantity": 1, "price": 899.0}
}
```

## Estructura del proyecto

```
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── place_order.py          # genera el initiating event
├── common/
│   ├── events.py           # crea eventos con la estructura de arriba
│   └── broker.py           # conexión a RabbitMQ, publicar, consumir y log en consola
└── services/               # un archivo por servicio
    ├── order_placement.py
    ├── payment.py
    ├── order_fulfillment.py
    ├── shipping.py
    └── notification.py
```

## Cómo correrlo

```bash
docker compose up -d --build                         # broker + servicios
docker compose run --rm app python place_order.py    # initiating event
docker compose logs                                  # evidencia del flujo
docker compose down
```

## Evidencia

Cada servicio imprime en consola una línea por cada evento que produce o consume, con el formato
`service - action - event_type`. Se ve con `docker compose logs` (o `docker compose logs -f` en vivo):

```
order-placement-service-1  | order-placement-service - consumed - place_order
order-placement-service-1  | order-placement-service - produced - order_placed
payment-service-1          | payment-service - consumed - order_placed
payment-service-1          | payment-service - produced - payment_applied
...
```
