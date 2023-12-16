# ПоисКлиник

ПоисКлиник - это приложение для поиска ближайших медицинских учреждений.
В этом репозитории живет backend этого приложения.  

На текущий момент времени сделано следующее:
* Проект развернут на [удаленном сервере](http://45.86.181.61/api/).
* Настроен workflow, содержащий следующие этапы: проведение тестов по pep-8; 
  доставка backend docker image на Docker Hub; автоматический deploy из 
  ветки develop. 
* Созданы модели Организация (Organization), Специальность (Specialty), 
  Город (Town) и Район (District), настроены связи между ними.
* Реализована первая версия бизнес-логики проекта на ресурсах 
  /api/organizations/, /api/specialties/ и /api/towns/. Примеры запросов и 
  ответов можно найти в [Вики](https://github.com/web-search-for-the-nearest-hospitals/backend/wiki/API).
* Добавлены management-команды по заполнению реальными и тестовыми данными - 
  `fill_test_orgs <num>`, `fill_specialties <path_to_csv>` и 
  `fill_cities_district <path_to_csv>`.
* Начаты проектирование и реализация бизнес-логики Пользователя (User).

Для локального развертывания используется команда из директории `infra` от root
```shell
docker-compose -f docker-compose-local.yml up --build -d
```
Не забыть про миграции и статику.  
Сервис будет доступен на http://localhost:28962.
