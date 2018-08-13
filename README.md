# FSND Logs Analysis Project

## Getting Started

Prerequisites:
* Virtual box 5.1
* Vagrant 2.1.2
* FSND Vagrant Configuration: https://github.com/udacity/fullstack-nanodegree-vm

1. After installing Virtual box and Vagrant, clone the FSND vagrant configuration repo.
```
git clone https://github.com/udacity/fullstack-nanodegree-vm
```
2. Then go into the directory where the `Vagrantfile` is.
```
cd fullstack-nanodegree-vm/vagrant
```
3. Run:
```
vagrant up
```
4. After `vagrant up` has finished, run:
```
vagrant ssh
```
5. Download the original data: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
6. Run this command to setup the database:
```
psql -d news -f newsdata.sql
```
7. Connect to the database:
```
psql -d news
```
8. Create views: See **Views Created** section
9. Copy `main.py` into `vagrant/` folder and run:
```
python main.py
```

## Views Created

After connecting to database (step 7), run the four commands below to create the views needed.

```
create view article_views as
select articles.title, count(*) from articles, log
where log.status = '200 OK' and articles.slug = substr(log.path, 10)
group by articles.title order by count desc;
```

```
create view title_author as
select articles.title, authors.name from articles
join authors on (articles.author = authors.id);
```

```
create view total_requests as
select to_char(time, 'FMMonth DD, YYYY') as date, count(*) as request_num from log
group by date;
```

```
create view error_requests as
select to_char(time, 'FMMonth DD, YYYY') as date, count(*) as request_num from log
where status not like '%200%'
group by date;
```
