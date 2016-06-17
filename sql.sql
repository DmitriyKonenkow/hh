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
  LEFT JOIN key_requirement kr ON r.key_req_id = kr.id
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
WHERE requirement like '%машинное%';

UPDATE requirements
SET key_req_id = 7
WHERE cluster = 139;
INSERT INTO key_requirement (name) VALUES ('tls');
SELECT c.cluster, c.cluster_count, r.requirement, r.count
from (SELECT
        requirement,
        key_req_id,
        cluster,
        count(*) AS count
      FROM requirements
      WHERE cluster IS NOT NULL
      GROUP BY requirement, cluster, key_req_id
      ORDER BY count
        DESC) r JOIN
  (SELECT
     cluster,
     count(*) AS cluster_count
   FROM requirements
   WHERE cluster IS NOT NULL
         and key_req_id is NULL
   GROUP BY cluster
   ORDER BY cluster_count
     DESC
   LIMIT 1) c on c.cluster = r.cluster
LIMIT 20;