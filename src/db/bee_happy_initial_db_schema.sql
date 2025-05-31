CREATE TABLE "beehives_sensornodes" (
  "sensor_node_id" integer PRIMARY KEY,
  "bee_hive" varchar,
  "sensor_name" varchar,
  "sensor_type" varchar
);

CREATE TABLE "digital_bee_hive_42_s2120" (
  "id" integer PRIMARY KEY,
  "sensor_node_id" integer,
  "time_of_save" timestamp,
  "lightIntensity" integer,
  "pressure" integer,
  "rainGauge" integer,
  "relativeHumidity" integer,
  "temperature" integer,
  "uvIndex" integer,
  "windDirection" integer,
  "windSpeed" integer,
  "entityId" varchar,
  "comments" varchar
);

CREATE TABLE "digital_bee_hive_42_dragino_s31lb" (
  "id" integer PRIMARY KEY,
  "sensor_node_id" integer,
  "time_of_save" timestamp,
  "relativeHumidity" integer,
  "temperature" integer,
  "entityId" varchar,
  "comments" varchar
);

CREATE TABLE "digital_bee_hive_42_dragino_d23_lb" (
  "id" integer PRIMARY KEY,
  "sensor_node_id" integer,
  "time_of_save" timestamp,
  "tempC1" integer,
  "tempC2" integer,
  "tempC3" integer,
  "entityId" varchar,
  "comments" varchar
);

ALTER TABLE "digital_bee_hive_42_s2120" ADD FOREIGN KEY ("sensor_node_id") REFERENCES "beehives_sensornodes" ("sensor_node_id");

ALTER TABLE "digital_bee_hive_42_dragino_s31lb" ADD FOREIGN KEY ("sensor_node_id") REFERENCES "beehives_sensornodes" ("sensor_node_id");

ALTER TABLE "digital_bee_hive_42_dragino_d23_lb" ADD FOREIGN KEY ("sensor_node_id") REFERENCES "beehives_sensornodes" ("sensor_node_id");
