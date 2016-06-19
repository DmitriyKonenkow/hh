SELECT
  vacancy_id,
  key_id
FROM vacancy_to_key
WHERE vacancy_id IN (16894195, 17383649);

SELECT description
FROM vacancies;

SELECT
  k.id,
  k.name,
  count(vk.vacancy_id)
FROM key_skills k
  JOIN vacancy_to_key vk ON k.id = vk.key_id
GROUP BY k.id, k.name
HAVING count(vk.vacancy_id) > 550
ORDER BY k.id
LIMIT 11;

--[3, 9, 11, 14, 10, 5, 99, 6, 16, 51, 19]

SELECT
  vacancy_id,
  key_id
FROM vacancy_to_key
WHERE key_id IN (3, 9, 11, 14, 10, 5, 99, 6, 16, 51, 19)
      AND vacancy_id = 11733349;

SELECT
  DISTINCT
  v.id,
  v.description
FROM vacancies v
  JOIN vacancy_to_key vk ON v.id = vk.vacancy_id
WHERE key_id IN (3, 5, 6, 9, 10, 11, 14, 16, 19, 51, 99);


SELECT count(*)
FROM requirements;

UPDATE status_parse
SET status = 2
WHERE status = 3;

SELECT
  r.requirement,
  r.cluster,
  max(r.count) AS max_count_req,
  cluster_count,
  r.key_req_id,
  kr.name
FROM (SELECT
        requirement,
        key_req_id,
        cluster,
        count(*) AS count
      FROM requirements
      WHERE cluster IS NOT NULL
      GROUP BY requirement, cluster, key_req_id
      ORDER BY count
        DESC) r
  JOIN (SELECT
          cluster,
          count(*) AS cluster_count
        FROM requirements
        WHERE cluster IS NOT NULL
        GROUP BY cluster
        ORDER BY cluster_count
          DESC) c ON r.cluster = c.cluster
  LEFT JOIN _key_requirement kr ON r.key_req_id = kr.id
WHERE r.key_req_id IS NULL
GROUP BY r.cluster
ORDER BY cluster_count
  DESC;


SELECT
  cluster,
  requirement,
  count(requirement) AS count
FROM requirements
WHERE cluster = 10
GROUP BY cluster, requirement
ORDER BY count
  DESC;


SELECT count(DISTINCT cluster)
FROM requirements;

UPDATE requirements
SET cluster = NULL
WHERE cluster IS NOT NULL;


SELECT
  r.requirement,
  count(v.id) AS count
FROM requirements r
  JOIN vacancies v ON r.vacancy_id = v.id
  LEFT JOIN requirements r1 ON v.id = r1.vacancy_id
WHERE
  r1.requirement LIKE '%машинн%'
                      COLLATE NOCASE
GROUP BY r.requirement
ORDER BY count
  DESC;

SELECT *
FROM requirements
WHERE requirement LIKE '%машинное%';

UPDATE requirements
SET key_req_id = 7
WHERE cluster = 139;
INSERT INTO _key_requirement (name) VALUES ('tls');
SELECT
  c.cluster,
  c.cluster_count,
  r.requirement,
  r.count
FROM (SELECT
        requirement,
        key_req_id,
        cluster,
        count(*) AS count
      FROM requirements
      WHERE cluster IS NOT NULL
      GROUP BY requirement, cluster, key_req_id
      ORDER BY count
        DESC) r
  JOIN
  (SELECT
     cluster,
     count(*) AS cluster_count
   FROM requirements
   WHERE cluster IS NOT NULL
         AND key_req_id IS NULL
   GROUP BY cluster
   ORDER BY cluster_count
     DESC
   LIMIT 1) c ON c.cluster = r.cluster
LIMIT 20;

SELECT
  ks.id,
  ks.name,
  count(vk.vacancy_id) AS count
FROM key_skills ks
  JOIN vacancy_to_key vk ON ks.id = vk.key_id
WHERE ks.name not LIKE '%1С%'
GROUP BY ks.name
HAVING count(vk.vacancy_id) < 78
ORDER BY count
  DESC;


INSERT INTO vacancy_to_key_req (vacancy_id, key_id, checked)
  SELECT
    DISTINCT
    vk.vacancy_id,
    91 AS key_id,
    1
  FROM vacancy_to_key vk
  WHERE vk.key_id = 101
        AND vk.vacancy_id NOT IN (
    SELECT vacancy_id
    FROM vacancy_to_key_req
    WHERE key_id = 91
  );

SELECT count(*)
FROM vacancy_to_key
WHERE key_id = 3;


SELECT count(*)
FROM vacancy_to_key_req;

INSERT INTO vacancy_to_key_req (vacancy_id, key_id, checked)
SELECT v.id, 67 as key_id, 1
FROM vacancies v
WHERE description like '%maven%'
      AND v.id NOT IN (
  SELECT vacancy_id
  FROM vacancy_to_key_req
  WHERE key_id = 67
)


drop TABLE _key_requirement