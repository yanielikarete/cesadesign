# Registro de Cambios

## Cambios Detectados por Git

- `facturacion/templates/guiaremision/create.html`
- `facturacion/templates/guiaremision/factura.html`

## Ejemplo de Código DDL

Una vez que hayas obtenido la información de la columna `pedido_id`, el código DDL para agregar esta columna podría verse algo así:

```sql
ALTER TABLE facturacion_guiaremision
ADD COLUMN pedido_id INTEGER;
```

Este es un ejemplo genérico y puede variar según las opciones específicas que se hayan utilizado al agregar la columna (por ejemplo, restricciones, valores predeterminados, etc.). Asegúrate de revisar cualquier opción adicional que se haya aplicado al momento de agregar la columna.