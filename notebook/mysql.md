- [基础](#基础)
  - [登录MySQL](#登录mysql)
  - [创建数据库](#创建数据库)
  - [创建数据库表](#创建数据库表)
  - [删除数据库表](#删除数据库表)
- [增删改查](#增删改查)
  - [SELECT](#select)
  - [UPDATE](#update)
  - [INSERT](#insert)
  - [DELETE](#delete)
- [关键字](#关键字)
  - [WHERE](#where)
  - [BETWEEN](#between)
  - [AS](#as)
  - [AND, OR 和 NOT](#and-or-和-not)
  - [ORDER BY](#order-by)
  - [GROUP BY](#group-by)
  - [IN](#in)
  - [UNION](#union)
  - [JOIN](#join)
  - [like](#like)
  - [HAVING](#having)
  - [limit](#limit)
- [SQL 函数](#sql-函数)
  - [COUNT](#count)
  - [AVG](#avg)
  - [SUM](#sum)
  - [MAX](#max)
  - [MIN](#min)
- [索引](#索引)
  - [建立索引的时机](#建立索引的时机)
- [其它](#其它)
  - [为每一行数据设定一个唯一的索引值](#为每一行数据设定一个唯一的索引值)
- [创建后表的修改](#创建后表的修改)
  - [添加列](#添加列)
  - [修改列](#修改列)
  - [删除列](#删除列)
  - [重命名表](#重命名表)
  - [清空表数据](#清空表数据)
  - [删除整张表](#删除整张表)
  - [删除整个数据库](#删除整个数据库)

## 基础

### 登录MySQL

```bash
mysql -h 127.0.0.1 -u <用户名> -p<密码>.   # 默认用户名<root>，-p 是密码，⚠️参数后面不需要空格
mysql -D 所选择的数据库名 -h 主机名 -u 用户名 -p
mysql> exit # 退出 使用 “quit;” 或 “\q;” 一样的效果
mysql> status;  # 显示当前mysql的version的各种信息
mysql> select version(); # 显示当前mysql的version信息
mysql> show global variables like 'port'; # 查看MySQL端口号
```

### 创建数据库

对于表的操作需要先进入库use 库名;

```sql
-- 创建一个名为 samp_db 的数据库，数据库字符编码指定为 gbk
create database samp_db character set gbk;
drop database samp_db; -- 删除 库名为 samp_db 的库
show databases;        -- 显示数据库列表。
use samp_db;           -- 选择创建的数据库 samp_db 
show tables;           -- 显示 samp_db 下面所有的表名字
describe 表名;          -- 显示数据表的结构
delete from 表名;       -- 清空表中记录
```

### 创建数据库表

`CREATE TABLE` 语法 语句用于从表中选取数据。

```sql
CREATE TABLE 表名称 (
  列名称1  数据类型,
  列名称2  数据类型,
  列名称3  数据类型,
  ....
);
```

```sql
-- 如果数据库中存在user_accounts表，就把它从数据库中drop掉
DROP TABLE IF EXISTS `user_accounts`;
CREATE TABLE `user_accounts` (
  `id`             int(100) unsigned NOT NULL AUTO_INCREMENT primary key,
  `password`       varchar(32)       NOT NULL DEFAULT '' COMMENT '用户密码',
  `reset_password` tinyint(32)       NOT NULL DEFAULT 0 COMMENT '用户类型：0－不需要重置密码；1-需要重置密码',
  `mobile`         varchar(20)       NOT NULL DEFAULT '' COMMENT '手机',
  `create_at`      timestamp(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `update_at`      timestamp(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  -- 创建唯一索引，不允许重复
  UNIQUE INDEX idx_user_mobile(`mobile`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='用户表信息';
```

数据类型的属性解释

- NULL：数据列可包含NULL值；
- NOT NULL：数据列不允许包含NULL值；
- DEFAULT：默认值；
- PRIMARY KEY：主键；
- AUTO_INCREMENT：自动递增，适用于整数类型；
- UNSIGNED：是指数值类型只能为正数；
- CHARACTER SET name：指定一个字符集；
- COMMENT：对表或者字段说明；

### 删除数据库表

```sql
DROP TABLE 表名称;     -- 用于删除数据库中的现有表。
TRUNCATE TABLE 表名称; -- 用于删除表内的数据，但不删除表本身。
```

## 增删改查

### SELECT

 `SELECT 语法` 语句用于从表中选取数据。

 ```sql
 SELECT 列名称1, 列名称2, ... FROM 表名称;
 SELECT * FROM 表名称;
 ```

```sql
-- 从 Customers 表中选择 CustomerName 和 City 列：
SELECT CustomerName, City FROM Customers;
-- 从 Customers 表中选择所有列：
SELECT * FROM Customers;
-- 表 station 取个别名叫 s，表 station 中不包含 字段 id=13 或者 14 的，并且 id 不等于 4 的 查询出来，只显示 id
SELECT s.id from station s WHERE id in (13,14) and id not in (4);
-- 从表 users 选取 id=3 的数据，并只拉一条数据(据说能优化性能)
SELECT * FROM users where id=3 limit 1
-- 结果集中会自动去重复数据
SELECT DISTINCT Company FROM Orders 
-- 表 Persons 字段 Id_P 等于 Orders 字段 Id_P 的值，
-- 结果集显示 Persons表的 所有字段，Orders表的所有字段
SELECT p.*, o.* FROM Persons p, Orders o WHERE p.Id_P = o.Id_P
select p.*, o.* from Persons p join  Orders o on(p.Id_P = o.Id_P);

select name, concat(price*100, ' cents') from products;
```

### UPDATE

 `Update 语法` 语句用于修改表中的数据。

 ```sql
 UPDATE 表名称 SET 列名称1 = 值1, 列名称2 = 值2, ... WHERE 条件;
 ```

```sql
-- update语句设置字段值为另一个结果取出来的字段
UPDATE user set name = (SELECT name from user1 WHERE user1 .id = 1 )
WHERE id = (SELECT id from user2 WHERE user2 .name='小苏');
-- 更新表 orders 中 id=1 的那一行数据更新它的 title 字段
UPDATE `orders` set title='这里是标题' WHERE id=1;
```

### INSERT

 `INSERT 语法` 用于向表格中插入新的行。

 ```sql
 INSERT INTO 表名称 (列名称1, 列名称2, 列名称3, ...) VALUES (值1, 值2, 值3, ...);
 INSERT INTO 表名称 VALUES (值1, 值2, 值3, ...);
 ```

```sql
-- 向表 Persons 插入一条字段 LastName = JSLite 字段 Address = shanghai
INSERT INTO Persons (LastName, Address) VALUES ('JSLite', 'shanghai');
-- 向表 meeting 插入 字段 a=1 和字段 b=2
INSERT INTO meeting SET a=1,b=2;
-- 
-- SQL实现将一个表的数据插入到另外一个表的代码
-- 如果只希望导入指定字段，可以用这种方法：
-- INSERT INTO 目标表 (字段1, 字段2, ...) SELECT 字段1, 字段2, ... FROM 来源表;
INSERT INTO orders (user_account_id, title) SELECT m.user_id, m.title FROM meeting m where m.id=1;

-- 向表 charger 插入一条数据，已存在就对表 charger 更新 `type`,`update_at` 字段；
INSERT INTO `charger` (`id`,`type`,`create_at`,`update_at`) VALUES (3,2,'2017-05-18 11:06:17','2017-05-18 11:06:17') ON DUPLICATE KEY UPDATE `id`=VALUES(`id`), `type`=VALUES(`type`), `update_at`=VALUES(`update_at`);
```

### DELETE

> `DELETE 语法` 语句用于删除表中的现有记录。
>
> ```sql
> DELETE FROM 表名称 WHERE 条件;
> ```

```sql
-- 在不删除table_name表的情况下删除所有的行，清空表。
DELETE FROM table_name
-- 或者
DELETE * FROM table_name
-- 删除 Person 表字段 LastName = 'JSLite' 
DELETE FROM Person WHERE LastName = 'JSLite' 
-- 删除 表meeting id 为2和3的两条数据
DELETE from meeting where id in (2,3);
```

## 关键字

### WHERE

> `WHERE 语法` 用于仅提取满足指定条件的记录
>
> ```sql
> SELECT 列名称, 列名称, ... FROM 表名称 WHERE 条件1;
> ```

```sql
-- 从表 Persons 中选出 Year 字段大于等于 1965 的数据
SELECT * FROM Persons WHERE Year>=1965
-- 从 Customers 表中选择 CustomerID = 1 的所有数据：
SELECT * FROM Customers WHERE CustomerID=1;
-- Select all the products with a price between $60 and $120.
select * from products where price >= 60 and price <= 120;
```

### BETWEEN

> `BETWEEN 语法` 运算符选择给定范围内的值
>
> ```sql
> SELECT 列名称(s) FROM 表名称 WHERE 列名称 BETWEEN 值1 AND 值2;
> ```

```sql
-- 选择 Products 表中 Price 字段在 10 到 20 之间的所有：
SELECT * FROM Products WHERE Price BETWEEN 10 AND 20;
```

### AS

> `AS 语法` 用于为表或表中的列(字段)提供临时名称(别名)。
>
> ```sql
> SELECT 列名称 AS 别名 FROM 表名称;
> SELECT 列名称(s) FROM 表名称 AS 别名;
> ```

### AND, OR 和 NOT

`WHERE` 子句可以与 `AND`、`OR` 和 `NOT` 运算符组合使用。

`AND` 和 `OR` 运算符用于根据多个条件过滤记录：

- 如果由 `AND` 分隔的所有条件都为 `TRUE`，则 `AND` 运算符将显示一条记录。
- 如果由 `OR` 分隔的任何条件为 `TRUE`，则 `OR` 运算符将显示一条记录。

如果条件不为真，`NOT` 运算符将显示一条记录。

> `AND 语法`
>
> ```sql
> SELECT 列名称, 列名称, ... FROM 表名称 WHERE 条件1 AND 条件2 AND 条件3 ...;
> ```

### ORDER BY

> `ORDER BY 语法` 用于按升序或降序对结果集进行排序。
>
> ```sql
> SELECT 列名称1, 列名称2, ... FROM 表名称 ORDER BY 列名称1, 列名称2, ... ASC|DESC;
> ```
>
> 默认按 `ASC` 升序对记录进行排序。要按降序对记录进行排序，请使用 `DESC` 关键字。

```sql
-- 从 Customers 表中选择所有字段，按 Country 列排序：
SELECT * FROM Customers ORDER BY Country;
-- 从 Orders 表中选择 Company, OrderNumber 字段，按 Company 列排序：
SELECT Company, OrderNumber FROM Orders ORDER BY Company
-- 从 Orders 表中选择 Company, OrderNumber 字段，按 Company 列降序排序：
SELECT Company, OrderNumber FROM Orders ORDER BY Company DESC
-- 从 Orders 表中选择 Company, OrderNumber 字段，按 Company 列降序排序，并 OrderNumber 以顺序显示：
SELECT Company, OrderNumber FROM Orders ORDER BY Company DESC, OrderNumber ASC
```

### GROUP BY

> `GROUP BY 语法` 将具有相同值的行分组到汇总行中
>
> ```sql
> SELECT 列名称(s)
> FROM 表名称
> WHERE 条件
> ORDER BY 列名称(s);
> ```

```sql
-- 列出了 Orders 每个发货人 Shippers 发送的订单 Orders 数量
SELECT Shippers.ShipperName, COUNT(Orders.OrderID) AS NumberOfOrders FROM Orders
LEFT JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID
GROUP BY ShipperName;
```

### IN

> `IN 语法` 运算符允许您在 WHERE 子句中指定多个值。运算符是多个 OR 条件的简写。
>
> ```sql
> SELECT 列名称(s) FROM 表名称 WHERE 列名称 IN (值1, 值2, ...);
> SELECT 列名称(s) FROM 表名称 WHERE 列名称 IN (SELECT STATEMENT);
> ```

```sql
-- 从表 Persons 选取 字段 LastName 等于 Adams、Carter
SELECT * FROM Persons WHERE LastName IN ('Adams','Carter')
-- 从表 Customers 选取 Country 值为 'Germany', 'France', 'UK' 的所有数据
SELECT * FROM Customers WHERE Country IN ('Germany', 'France', 'UK');
-- 从表 Customers 选取 Country 值不为 'Germany', 'France', 'UK' 的所有数据
SELECT * FROM Customers WHERE Country NOT IN ('Germany', 'France', 'UK');
-- 从表 Customers 选取与 Suppliers 表 Country 字段相同的所有数据：
SELECT * FROM Customers WHERE Country IN (SELECT Country FROM Suppliers);
```

### UNION

> `UNION 语法` 操作符用于合并两个或多个 SELECT 语句的结果集
>
> ```sql
> SELECT 列名称(s) FROM 表名称1
> UNION
> SELECT 列名称(s) FROM 表名称2;
> ```

### JOIN

JOIN 子句用于根据两个或多个表之间的相关列组合来自两个或多个表的行。

- `JOIN`: 如果表中有至少一个匹配，则返回行
- `INNER JOIN`:在表中存在至少一个匹配时，INNER JOIN 关键字返回行。
- `LEFT JOIN`: 即使右表中没有匹配，也从左表返回所有的行
- `RIGHT JOIN`: 即使左表中没有匹配，也从右表返回所有的行
- `FULL JOIN`: 只要其中一个表中存在匹配，就返回行(MySQL 是不支持的，通过  `LEFT JOIN + UNION + RIGHT JOIN` 的方式 来实现)

### like

```sql
-- Select all the data of employees whose last name begins with an "S".
select * from employees where LastName like 'S%';
```

### HAVING

HAVING子句通常与GROUP BY子句一起使用，以根据指定的条件过滤分组。如果省略GROUP BY子句，则HAVING子句的行为与WHERE子句类似。请注意，HAVING子句将过滤条件应用于每组分行，而WHERE子句将过滤条件应用于每个单独的行。

```sql
--- Select the names of departments with more than two employees
select b.name 
from departments b
where code in (
select department
from employees
group by department
having count(*)>2
);
```

### limit

```sql
-- Select the name and last name of employees working for departments with second lowest budget.
select name, lastname
from employees
where department =(
select temp.code 
from (select * from departments order by budget limit 2) temp
order by temp.budget desc limit 1
);


/* With subquery */
SELECT e.Name, e.LastName
FROM Employees e 
WHERE e.Department = (
       SELECT sub.Code 
       FROM (SELECT * FROM Departments d ORDER BY d.budget LIMIT 2) sub 
       ORDER BY budget DESC LIMIT 1);

```

## SQL 函数

### COUNT

> `COUNT 语法` 返回与指定条件匹配的行数
>
> ```sql
> SELECT COUNT(列名称) FROM 表名称 WHERE 条件;
> ```

```sql
-- 表 Store_Information 有几笔 store_name 栏不是空白的资料。
-- "IS NOT NULL" 是 "这个栏位不是空白" 的意思。
SELECT COUNT (Store_Name) FROM Store_Information WHERE Store_Name IS NOT NULL; 
-- 获取 Persons 表的总数
SELECT COUNT(1) AS totals FROM Persons;
-- 获取表 station 字段 user_id 相同的总数
select user_id, count(*) as totals from station group by user_id;
```

### AVG

> `AVG 语法` 返回数值列的平均值
>
> ```sql
> SELECT AVG(列名称) FROM 表名称 WHERE 条件;
> ```

```sql
-- 查找 Products 表中所的 Price 平均值：
SELECT AVG(Price) FROM Products;
```

### SUM

> `SUM 语法` 返回数值列的总和
>
> ```sql
> SELECT SUM(列名称) FROM 表名称 WHERE 条件;
> ```

```sql
-- 查找 OrderDetails 表中 Quantity 字段的总和：
SELECT SUM(Quantity) FROM OrderDetails;
```

### MAX

> `MAX 语法` 返回所选列的最大值
>
> ```sql
> SELECT MIN(列名称) FROM 表名称 WHERE 条件;
> ```

```sql
-- 列出表 Orders 字段 OrderPrice 列最大值，
-- 结果集列不显示 OrderPrice 显示 LargestOrderPrice
SELECT MAX(OrderPrice) AS LargestOrderPrice FROM Orders
```

### MIN

> `MIN 语法` 返回所选列的最小值
>
> ```sql
> SELECT MIN(列名称) FROM 表名称 WHERE 条件;
> ```

```sql
-- 查找 Products 表中 Price 字段最小值，并命名 SmallestPrice 别名：
SELECT MIN(Price) AS SmallestPrice FROM Products;
```

## 索引

索引是一种特殊的文件(InnoDB数据表上的索引是表空间的一个组成部分)，它们包含着对数据表里所有记录的引用指针。更通俗的说，数据库索引好比是一本书前面的目录，能加快数据库的查询速度。
索引分为聚簇索引和非聚簇索引两种，聚簇索引是按照数据存放的物理位置为顺序的，而非聚簇索引就不一样了；聚簇索引能提高多行检索的速度，而非聚簇索引对于单行的检索很快
要注意的是，建立太多的索引将会影响更新和插入的速度，因为它需要同样更新每个索引文件。对于一个经常需要更新和插入的表格，就没有必要为一个很少使用的where字句单独建立索引了，对于比较小的表，排序的开销不会很大，也没有必要建立另外的索引

1. 普通索引
    普通索引(由关键字KEY或INDEX定义的索引)的唯一任务是加快对数据的访问速度。因此，应该只为那些最经常出现在查询条件(WHERE column = …)或排序条件(ORDER BY column)中的数据列创建索引。只要有可能，就应该选择一个数据最整齐、最紧凑的数据列(如一个整数类型的数据列)来创建索引。

    ```sql
    -- 直接创建索引(length表示使用名称前1ength个字符)  
    CREATE INDEX index_name ON table_name(column_name(length))  
    -- 修改表结构的方式添加索引  
    ALTER TABLE table_name ADD INDEX index_name ON (column_name)  
    -- 创建表的时候同时创建索引  
    CREATE TABLE table_name (  
    id int(11) NOT NULL AUTO_INCREMENT ,  
    title char(255) NOT NULL ,  
    PRIMARY KEY (id),  
    INDEX index_name (title)  
    ) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;  
    -- 删除索引  
    DROP INDEX index_name ON table_name;  
    ```

2. 唯一索引
    与普通索引类似，不同的就是：索引列的值必须唯一，但允许有空值（注意和主键不同）。如果是组合索引，则列值的组合必须唯一，创建方法和普通索引类似。
    如果能确定某个数据列将只包含彼此各不相同的值，在为这个数据列创建索引的时候就应该用关键字UNIQUE把它定义为一个唯一索引。这么做的好处：一是简化了MySQL对这个索引的管理工作，这个索引也因此而变得更有效率；二是MySQL会在有新记录插入数据表时，自动检查新记录的这个字段的值是否已经在某个记录的这个字段里出现过了；如果是，MySQL将拒绝插入那条新记录。也就是说，唯一索引可以保证数据记录的唯一性。事实上，在许多场合，人们创建唯一索引的目的往往不是为了提高访问速度，而只是为了避免数据出现重复。

    ```sql
    -- 创建唯一索引  
    CREATE UNIQUE INDEX index_name ON table_name(column_name)  
    -- 修改表结构  
    ALTER TABLE table_name ADD UNIQUE index_name ON (column_name)  
    -- 创建表的时候直接指定  
    CREATE TABLE table_name (  
    id int(11) NOT NULL AUTO_INCREMENT ,  
    title char(255) NOT NULL ,  
    PRIMARY KEY (id),  
    UNIQUE index_name (title)  
    );  
    ```

3. 全文索引(FULLTEXT)

    ```sql
    -- 给 user 表中的 description 字段添加全文索引(FULLTEXT)
    ALTER TABLE `user` ADD FULLTEXT (description);
    ```

4. 添加多列索引

    ```sql
    -- 给 user 表中的 name、city、age 字段添加名字为name_city_age的普通索引(INDEX)
    ALTER TABLE user ADD INDEX name_city_age (name(10),city,age); 
    ```

### 建立索引的时机

在`WHERE`和`JOIN`中出现的列需要建立索引，但也不完全如此：

- MySQL只对`<`，`<=`，`=`，`>`，`>=`，`BETWEEN`，`IN`使用索引
- 某些时候的`LIKE`也会使用索引。
- 在`LIKE`以通配符%和_开头作查询时，MySQL不会使用索引。
3.主索引
　　在前面已经反复多次强调过：必须为主键字段创建一个索引，这个索引就是所谓的”主索引”。主索引与唯一索引的唯一区别是：前者在定义时使用的关键字是PRIMARY而不是UNIQUE。

  ```sql
  -- 给 user 表中的 id字段 添加主键索引(PRIMARY key)
  ALTER TABLE `user` ADD PRIMARY key (id);
  ```

4.外键索引
　　如果为某个外键字段定义了一个外键约束条件，MySQL就会定义一个内部索引来帮助自己以最有效率的方式去管理和使用外键约束条件。

## 其它

### 为每一行数据设定一个唯一的索引值

1. 使用自增主键：在创建表时，可以定义一个自增的主键，例如使用AUTO_INCREMENT属性。这样，MySQL会自动为每一行数据分配一  个唯一的主键值。

    ```sql
    CREATE TABLE your_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        column1 VARCHAR(50),
        column2 VARCHAR(50),
        ...
    );
    ```

2. 使用UUID：UUID（Universally Unique Identifier）是一种标准的唯一标识符，可以在应用层生成，然后插入数据库表中。MySQL也提供了UUID()函数来生成UUID。

    ```sql
     CREATE TABLE your_table (
      id VARCHAR(36) PRIMARY KEY,
      column1 VARCHAR(50),
      column2 VARCHAR(50),
      ...
  
    );
  
    INSERT INTO your_table (id, column1, column2, ...)
    VALUES (UUID(), 'value1', 'value2', ...);
    ```

3. 你还可以使用其他唯一标识符生成策略，例如基于时间戳和随机数的组合，或者其他应用程序特定的算法。

## 创建后表的修改

### 添加列

> 语法：`alter table 表名 add 列名 列数据类型 [after 插入位置];`

示例:

```sql
-- 在表students的最后追加列 address: 
alter table students add address char(60);
-- 在名为 age 的列后插入列 birthday: 
alter table students add birthday date after age;
-- 在名为 number_people 的列后插入列 weeks: 
alter table students add column `weeks` varchar(5) not null default "" after `number_people`;
```

### 修改列

> 语法：`alter table 表名 change 列名称 列新名称 新数据类型;`

```sql
-- 将表 tel 列改名为 telphone: 
alter table students change tel telphone char(13) default "-";
-- 将 name 列的数据类型改为 char(16): 
alter table students change name name char(16) not null;
-- 修改 COMMENT 前面必须得有类型属性
alter table students change name name char(16) COMMENT '这里是名字';
-- 修改列属性的时候 建议使用modify,不需要重建表
-- change用于修改列名字，这个需要重建表
alter table meeting modify `weeks` varchar(20) NOT NULL DEFAULT '' COMMENT '开放日期 周一到周日：0~6，间隔用英文逗号隔开';
-- `user`表的`id`列，修改成字符串类型长度50，不能为空，`FIRST`放在第一列的位置
alter table `user` modify COLUMN `id` varchar(50) NOT NULL FIRST ;
```

### 删除列

> 语法：`alter table 表名 drop 列名称;`

```sql
-- 删除表students中的 birthday 列: 
alter table students drop birthday;
```

### 重命名表

> 语法：`alter table 表名 rename 新表名;`

```sql
-- 重命名 students 表为 workmates: 
alter table students rename workmates;
```

### 清空表数据

> 方法一：`delete from 表名;`
> 方法二：`truncate table "表名";`

- `DELETE:`1. DML语言;2. 可以回退;3. 可以有条件的删除;
- `TRUNCATE:`1. DDL语言;2. 无法回退;3. 默认所有的表内容都删除;4. 删除速度比delete快。

```sql
-- 清空表为 workmates 里面的数据，不删除表。 
delete from workmates;
-- 删除workmates表中的所有数据，且无法恢复
truncate table workmates;
```

### 删除整张表

> 语法：`drop table 表名;`

```sql
-- 删除 workmates 表: 
drop table workmates;
```

### 删除整个数据库

> 语法：`drop database 数据库名;`

```sql
-- 删除 samp_db 数据库: 
drop database samp_db;
```
