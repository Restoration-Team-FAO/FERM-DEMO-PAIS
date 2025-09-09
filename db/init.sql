CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS restauracion_proyectos;
CREATE TABLE restauracion_proyectos (
  id SERIAL PRIMARY KEY,
  nombre_proyecto TEXT NOT NULL,
  area_ha NUMERIC,
  tipo_actividad TEXT,
  geometry geometry(Polygon, 4326)
);

INSERT INTO restauracion_proyectos (nombre_proyecto, area_ha, tipo_actividad, geometry)
VALUES
('Proyecto Demo 1', 12.5, 'reforestacion',
 ST_GeomFromText('POLYGON((-86.7 14.8,-86.6 14.8,-86.6 14.9,-86.7 14.9,-86.7 14.8))',4326)),
('Proyecto Demo 2', 33.2, 'restauracion',
 ST_GeomFromText('POLYGON((-86.9 14.7,-86.8 14.7,-86.8 14.8,-86.9 14.8,-86.9 14.7))',4326));
