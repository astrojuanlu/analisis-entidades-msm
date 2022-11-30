# Datos entidades Mercado Social Madrid

```mermaid
graph LR

    U-->|Usa|M
    U-->|Visita|W

    M-->|Consulta API|HA
    HG-->|"Manda email a entidades\npara crear perfil"|HA
    W-.->|Extrae algunos\nfragmentos HTML|HG

    O-.->|"Operan\n(potencialmente)"|HA

    T-->|Desarrolla|M
    T-->|Desarrolla|HA

    ET-->|Opera|HA
    ET-->|Opera|HG

    TS-->|Mantiene|W

    E-->|"Gestionan\nsu perfil"|HA

    W["fa:fa-desktop Web"]
    M["fa:fa-mobile App Móvil"]

    U(("fa:fa-eye\nConsumidora"))
    E(("fa:fa-chair Entidades"))
    ET(("fa:fa-hard-hat\nEquipo\nTécnico"))
    O(("fa:fa-seedling Otros\nMercados\nSociales"))

    HG["fa:fa-desktop fa:fa-gear HG\n(Herramienta Gestora)"]
    HA["fa:fa-desktop fa:fa-gear HA\n(Herramienta Aplicación)"]

    TS(("fa:fa-briefcase Traficantes\nDe Sueños"))
    T(("fa:fa-briefcase Triskel\nApps"))
```

## TODO

- Cross-check with https://mercadosocial.net/territorios/madrid/

## Preguntas

- ¿Cuál es la fecha de última actualización de cada perfil social?
- ¿Qué entidades tienen LinkedIn?
- ¿Qué entidades tienen tienda online?
- ¿Qué entidades tienen un descuento activo con el MESM? ¿De qué tipo?
- ¿Qué entidades facturan periódicamente por sus servicios?
- ¿Qué entidades tienen tienda física?
- ¿Qué tipologías de ventajas hay? ¿Cuántas son relacionadas con la exención del pago del capital social?
- ¿Qué métodos hay para usar esas ventajas?
  - "Escríbenos a madrid@mercadosocial.net" / "muestra que estás registrada en la app"

## Notas

- Hay 3 categorizaciones diferentes y no coinciden 100 %

## Análisis

### Catálogo

- 175 entidades (2022-11-04)
- 20 categorías
  - Categorías más pobladas: Comunicación / TICs, Desarrollo Comunitario, Educación / Empleo
  - Categorías menos pobladas: Papelería / Consumibles, Complementos / Bisutería, Crianza / Bebés
- Presencia online: Web (97 %), Facebook (77 %), Twitter (58 %), Instagram (40 %), Telegram (12 %)
  - Redes sociales por tamaño: Facebook (2910 MAU), YouTube (2562 MAU), WhatsApp (2000 MAU), Instagram (1478 MAU), Telegram (550 MAU), Twitter (436 MAU) (fuente: https://www.statista.com/statistics/272014/global-social-networks-ranked-by-number-of-users/)
  - ¿Instagram poco aprovechado?
    - Categorías más activas en Instagram: Limpieza / Jardinería / Bricolaje, Textil / Calzado, Educación / Empleo
    - Categorías menos activas en Instagram: Asesoría / Jurídicos, Desarrollo Comunitario, Turismo / Ocio / Cultura
- Beneficios / Descuentos
  - 42 entidades de 175 tienen algún tipo de beneficio (un 25 %) de las cuales
    - 9 mencionan "enseña la app en la tienda" (un 21 %),
    - 35 mencionan "escríbenos al correo para explicarte el procedimiento" (un 83 %),
    - y hay 1 que no menciona ninguna de las dos
    - nótese que hay 3 entidades que mencionan ambas
