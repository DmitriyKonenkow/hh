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
  requirement,
  cluster,
  max(count) AS max_count
FROM (SELECT
        requirement,
        cluster,
        count(*) AS count
      FROM requirements
      WHERE cluster IS NOT NULL
      GROUP BY requirement, cluster
      ORDER BY count DESC )
GROUP BY cluster
ORDER BY max_count DESC ;

UPDATE requirements
SET cluster = NULL
WHERE cluster IS NOT NULL;