SELECT email
FROM "students"
WHERE email = :email
  AND status <> 'inactive'
  AND id IN (SELECT max(id) FROM "students" WHERE email = :email)