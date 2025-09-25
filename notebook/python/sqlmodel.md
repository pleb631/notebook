- [pydantic](#pydantic)
  - [1. BaseModel](#1-basemodel)
    - [1.1基本用法](#11基本用法)
    - [1.2 属性方法](#12-属性方法)
    - [1.3 嵌套模型](#13-嵌套模型)
    - [1.4 必填字段](#14-必填字段)
    - [1.5 动态默认值](#15-动态默认值)
  - [2. Field](#2-field)
    - [2.1 参数](#21-参数)
    - [2.2 computed\_field](#22-computed_field)
  - [3. 别名](#3-别名)
    - [3.1 alias](#31-alias)
    - [3.2 别名路径、别名选择](#32-别名路径别名选择)
    - [3.3 别名生成器](#33-别名生成器)
    - [3.4 别名优先级](#34-别名优先级)
    - [3.5 注意](#35-注意)
  - [4. 验证装饰器](#4-验证装饰器)
- [sqlmodel](#sqlmodel)
  - [1. 基本操作](#1-基本操作)
    - [1.1 创建数据库](#11-创建数据库)
    - [1.2 session](#12-session)
    - [1.3 创建实例](#13-创建实例)
  - [2. 增查删改](#2-增查删改)
    - [2.1 select](#21-select)
    - [2.2 where](#22-where)
    - [2.3 索引](#23-索引)
    - [2.4 Limit 和 Offset](#24-limit-和-offset)
    - [2.5 更新和删除](#25-更新和删除)
  - [3.连接表](#3连接表)
    - [3.1 创建模型](#31-创建模型)
    - [3.2 创建联系](#32-创建联系)
    - [3.3 查询](#33-查询)
      - [3.3.1 join](#331-join)
      - [3.3.2 LEFT OUTER](#332-left-outer)
    - [3.4 更新和删除](#34-更新和删除)
  - [4.关系属性](#4关系属性)
    - [4.1创建模型](#41创建模型)
    - [4.2 创建联系](#42-创建联系)
    - [4.3 更新](#43-更新)
    - [4.4 级联删除](#44-级联删除)
      - [4.4.1 ondelete](#441-ondelete)
      - [4.4.2 passive\_deletes](#442-passive_deletes)
  - [5.多对多模型](#5多对多模型)
  - [6. fastapi的使用](#6-fastapi的使用)

# pydantic

## 1. BaseModel

### 1.1基本用法

```pyhon
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
    
user = User(id='123')
```

在这个例子中， `user` 是 `User` 的一个实例。对象的初始化将执行所有的解析和验证。如果没有抛出 `ValidationError` ，你就知道生成的模型实例是有效的。

### 1.2 属性方法

```python
# 返回key的set
.model_fields_set: set[str] 


# 返回实例的复制
.model_copy(
    *,
    update: dict[str, Any] | None = None, # 可以在复制的过程中为新实例更新参数
    deep: bool = False # 深复制
) -> Self

# 返回实例的json字段
.model_dump(
    *,
    mode: Literal["json", "python"] | str = "python", 
    include: IncEx = None, # set,选择哪个参数要被dump
    exclude: IncEx = None, # set,选择哪个参数不被dump
    context: Any | None = None,
    by_alias: bool = False, # 是否使用别名
    exclude_unset: bool = False, # 是否排除未显式设置的字段(显示设置成默认值的不会被排除)。
    exclude_defaults: bool = False, # 是否排除是否设置成默认值的key
    exclude_none: bool = False, # 是否排除是否设置成None的key
    round_trip: bool = False,
    warnings: (
        bool | Literal["none", "warn", "error"]
    ) = True,
    serialize_as_any: bool = False
) -> dict[str, Any]

# 返回实例的json序列化
.model_dump_json(
    *,
    indent: int | None = None,
    include: IncEx = None,
    exclude: IncEx = None,
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    warnings: (
        bool | Literal["none", "warn", "error"]
    ) = True,
    serialize_as_any: bool = False
) -> str


# 返回可序列化的json字典
.model_json_schema(
    by_alias: bool = True,
    ref_template: str = DEFAULT_REF_TEMPLATE,
    schema_generator: type[
        GenerateJsonSchema
    ] = GenerateJsonSchema,
    mode: JsonSchemaMode = "validation",
) -> dict[str, Any]

```

### 1.3 嵌套模型

只要数据格式正确，就可以递归的创建

```python
from typing import List, Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]


m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
"""
print(m.model_dump())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
}
"""
```

### 1.4 必填字段

要声明一个字段为必填字段，您可以使用注解或注解与 `Field` 规范结合使用。`Field` 函数主要用于为属性配置设置，如 `alias` 或 `description`

```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    a: int
    b: int = ...
    c: int = Field(..., alias='C')
```

### 1.5 动态默认值

如果将可变对象用作函数或方法参数的默认值，则每次调用中都会重用同一个实例，如下，这种情况，会报错提醒

```python
class Model(BaseModel):
    item_counts: List[Dict[str, int]] = [{}]
```

正确方法是使用`default_factory`,这样每次调用时都会使用函数创建新的值。

```python
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=datetime_now)


m1 = Model()
m2 = Model()
assert m1.uid != m2.uid
```

## 2. Field

[`Field`](https://pydantic.com.cn/api/fields/#pydantic.fields.Field)函数用于自定义和向模型字段添加元数据。

### 2.1 参数

| 参数                  | 类型              | 描述                                      |
| --------------------- | ----------------- | ----------------------------------------- |
| default               | Any               |                                           |
| default_factory       | Callable[[], Any] | None                                      |
| alias                 | str               |                                           |
| alias_priority        | int               |                                           |
| validation_alias      |                   |                                           |
| serialization_alias   | str               |                                           |
| description           | str               |                                           |
| exclude               | bool              | 是否不参与序列化                          |
| deprecated            | bool              |                                           |
| frozen                | bool              | 是否不允许更改                            |
| validate_default      | bool              | 是否验证默认值                            |
| strict                | bool              | 是否开启strict模式（不能自动格式转换）    |
| gt/ge/lt/le           |                   | 仅适用于数字的比较                        |
| multiple_of           | float             | 是否是xx的倍数                            |
| min_length/max_length | int               | 可迭代对象的长度                          |
| pattern               | str               | 正则表达式                                |
| allow_inf_nan         | bool              | 允许 `inf`、`-inf`、`nan`。仅适用于数字。 |
| max_digits            | int               | 字符串的最大位数                          |
| decimal_places        | int               | 数字允许的最大小数位数                    |

### 2.2 computed_field

可用于在序列化模型或数据类时包含 `property` 或 `cached_property` 属性。这对于从其他字段计算得出的字段或计算成本高的字段很有用

```python
from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    # @deprecated("'volume' is deprecated")
    def volume(self) -> float:
        return self.width * self.height * self.depth


b = Box(width=1, height=2, depth=3)
print(b.model_dump())
#> {'width': 1.0, 'height': 2.0, 'depth': 3.0, 'volume': 6.0}
```

## 3. 别名

### 3.1 alias

有三种定义别名的方法：

- `Field(..., alias='foo')`
- `Field(..., validation_alias='foo')`
- `Field(..., serialization_alias='foo')`

`alias` 参数既用于验证，也用于序列化。如果希望分别为验证和序列化使用不同的别名，可以使用 `validation_alias` 和 `serialization_alias` 参数，它们将仅在各自的用例中应用。

### 3.2 别名路径、别名选择

为了方便在使用 `validation_alias` 时提供了两种特殊类型： `AliasPath` 和 `AliasChoices`

`AliasPath` 用于使用别名指定字段的路径。例如：

```python
from pydantic import BaseModel, Field, AliasPath


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasPath('names', 0))
    last_name: str = Field(validation_alias=AliasPath('names', 1))

user = User.model_validate({'names': ['John', 'Doe']})  # (1)!
print(user)
#> first_name='John' last_name='Doe'
```

在 `'first_name'` 字段中，我们使用别名 `'names'` 和索引 `0` 指定第一个名字的路径。在 `'last_name'` 字段中，我们使用别名 `'names'` 和索引 `1` 指定最后一个名字的路径。

`AliasChoices` 用于指定别名的选择。例如：

```python
from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', 'fname'))
    last_name: str = Field(validation_alias=AliasChoices('last_name', 'lname'))

user = User.model_validate({'fname': 'John', 'lname': 'Doe'})  # (1)!
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'first_name': 'John', 'lname': 'Doe'})  # (2)!
print(user)
#> first_name='John' last_name='Doe'
```

1. 我们正在对这两个字段使用第二个别名选择。
2. 我们正在使用字段 `'first_name'` 的第一个别名选项和字段 `'last_name'` 的第二个别名选项。

也可以混合使用

```python
from pydantic import BaseModel, Field, AliasPath, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', AliasPath('names', 0)))
    last_name: str = Field(validation_alias=AliasChoices('last_name', AliasPath('names', 1)))


user = User.model_validate({'first_name': 'John', 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John', 'Doe']})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John'], 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
```

### 3.3 别名生成器

可以使用`ConfigDict`的 `alias_generator` 参数指定一个可调用对象，该对象将为模型中的所有字段生成别名

Pydantic 提供了三个内置的别名生成器，您可以直接使用：

- to_pascal
- to_camel
- to_snake

基本案例

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Tree(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.upper()
        # alias_generator=to_camel
        populate_by_name=True 
    )

    age: int
    height: float
    kind: str


t = Tree.model_validate({'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'})
print(t.model_dump(by_alias=True))
#> {'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'}
```

### 3.4 别名优先级

可以在字段上设置 `alias_priority` 来更改此行为：

- `alias_priority=2` 别名不会被别名生成器覆盖。

- `alias_priority=1` 别名将被别名生成器覆盖。

- 未设置：

  - 别名已设置：别名不会被别名生成器覆盖。
  - 未设置别名：别名将被别名生成器覆盖。

### 3.5 注意

- 只传 alias → 不需要 `populate_by_name`。
- 使用alias生成器，会改变外部交互的字段名，想让原字段名也可用 → 必须 `populate_by_name=True`。

## 4. 验证装饰器

[`@validate_call`](https://pydantic.com.cn/api/validate_call/#pydantic.validate_call_decorator.validate_call)装饰器允许在调用函数之前，使用函数的注释来解析和验证传递给函数的参数。验证失败会报 `ValidationError`

```python
from pydantic import validate_call


@validate_call
def validate_foo(a: int, b: int):
        return b


foo = validate_foo(a=1, b=2)
print(foo)
#> 2
foo = validate_foo(a=1, b=[1,2,3]) # 报错
```

# sqlmodel

## 1. 基本操作

### 1.1 创建数据库

因为python内置SQLite ，所以以SQLite 为例。

```python
from sqlmodel import Field, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
```

这里使用SQLModel定义了一个`Hero`类,`table=True`意思希望在数据库创建对应的表，然后使用`create_engine`连接数据库，最后用`SQLModel.metadata.create_all(engine)`创建表



engine职责：表示**数据库连接**以及和数据库交互的底层接口。
**作用**：

  - 维护连接池（Connection Pool）
  - 管理与数据库驱动的交互（比如 `psycopg2`、`mysqlclient` 等）
  - 是执行原始 SQL 或创建 Session 的入口。

### 1.2 session

操作数据库需要创建会话窗口session，如下，然后在结束操作时，也要`session.close()`

```python
from sqlmodel import Session


def create_heroes():
    session = Session(engine)
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

    session.add(hero_1)
    session.add(hero_2)

    session.commit()

    session.close()
```



Session职责：表示**一次具体的数据库会话/事务上下文**。
**作用**：
  - 管理对象与数据库之间的同步（增删改查）。
  - 维护对象的“脏”状态，提交事务（`commit`）、回滚事务（`rollback`）。



可以使用`with`来进行上下文管理,就可以自动完成session的回收工作

```python
with Session(engine) as session:
    session.add(hero_1)
    session.commit()
```

### 1.3 创建实例

在创建`Hero`对象时，比如

```python
# id: int | None = Field(default=None, primary_key=True)
hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
```

`Hero` 的 `id` 字段声明了 `primary_key=True`，因此是数据库主键，必须 **NOT NULL**。在插入前数据库尚未生成主键值，所以在 Python 中需要声明为 `int | None`（或 `Optional[int]`）并设 `Field(default=None)`，表示写入前可为 `None`。

如果插入数据库时id为 `None`，数据库会自动自增生成；若手动指定非 `None` 值，则必须保证该值在表中唯一，避免主键冲突。

## 2. 增查删改

### 2.1 select

```python
from sqlmodel import  select

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero) # 建立查询语句
        results = session.exec(statement) # 执行查询
        heroes = results.all()
```

这会让程序获得Hero表的所有数据，上述代码相当于

```sql
SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
```

`results` 对象是一个 可迭代对象，可以用来遍历每一行



1. 如果想要立即获得所有结果，则执行`results.all()`

2. 如果只想获得第一行的数据，则执行`result.first()`
3. 想确保只有 **一个** 行与查询匹配，使用 `.one()` 代替 `.first()`，如果没有或一个以上，则报错
4. 当然，如果知道目标行的id，则可以执行`hero = session.get(Hero, 9001)`就可以快速得到结果



**注意**：**SQLModel** 自己的 `Session` 直接继承自 SQLAlchemy 的 `Session`，并添加了这个额外的方法 `session.exec()`。在底层，它使用相同的 `session.execute()`

如果在 SQLAlchemy 中，需要在这里添加一个 `.scalars()`才能得到相同结果，这是因为SQLAlchemy查询的结果比**SQLModel**的 多一个封装层。

```python
heroes = session.execute(select(Hero)).scalars().all()
```

但是当选择多个事物时，则必须删除它。



### 2.2 where

如果需要筛选数据，则使用`where`

```python
statement = select(Hero).where(Hero.age >= 35)

statement = select(Hero).where(Hero.age >= 35, Hero.age < 40) # And

statement = select(Hero).where(Hero.age >= 35).where(Hero.age < 40) # And
```

或者需要or表达式

```python
from sqlmodel import or_
statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90)) # or
```



如果被筛选参数的有None值，编辑器就会报错，因为`None` 与 `>` 无法进行比较，这需要引入`col`,对该运算进行封装

```python
from sqlmodel import col

statement = select(Hero).where(col(Hero.age) >= 35)
```

### 2.3 索引

如果某个表的数据上千万行，通过非主键的查询就会很消耗时间，此时应对数据建立索引，让数据库对数据的排序等进行优化。



使用索引的方式很简单，就是给指定字段加`index=True`,但不建议给所有字段添加索引，因为这会使维护成本变高

```python
class Hero(SQLModel, table=True):
    ...
    name: str = Field(index=True)
    ...
```

### 2.4 Limit 和 Offset

这个主要用于分页查询，服务于前端翻页浏览，

```python
statement = select(Hero).where(Hero.age > 32).offset(20).limit(10)
```

上面的结果就是查询年龄大于32的对象，跳过前20行，取20-30行的数据

### 2.5 更新和删除

一般用select获取相关对象后，用字段直接修改数据，然后提交

```python
def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Hero:", hero)

        hero.age = 16
        session.add(hero)
        session.commit()
        session.refresh(hero)

```

删除一行

```python
def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        session.delete(hero)
        session.commit()


```



**注意**：sqlmodel有提供insert、update、delete的封装



```python
from sqlmodel import delete, update


rows = [
    {"name": "Hulk", "age": 40},
    {"name": "Black Widow", "age": 32},
]
with Session(engine) as session:
    stmt = delete(Hero).where(Hero.retired == True)
    session.exec(stmt)
    session.commit()
    
    stmt = (
        update(Hero)
        .where(Hero.team == "X-Men")
        .values(age=Hero.age + 1)   
    )
    result = session.exec(stmt)      
    session.commit()
    
    stmt = insert(Hero).values(rows)
    session.exec(stmt)
```

这种做法很高性能，但绕过了ORM的生命周期，直接操作数据库，那么这**不会触发 ORM 级事件/校验/关系级联** 等 Python 侧逻辑



## 3.连接表

### 3.1 创建模型

如果要连接数据，比如**一个**团队可以拥有**多个**英雄。因此，它通常被称为**一对多**或**多对一**关系。

这时可以引入外键`foreign_key`进行关联

```python
from sqlmodel import Field, SQLModel, create_engine


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
```



此时Hero的team_id会和Team的id进行关联，sql语句是

```sql
CREATE TABLE team (
        id INTEGER,
        name VARCHAR NOT NULL,
        headquarters VARCHAR NOT NULL,
        PRIMARY KEY (id)
)

CREATE TABLE hero (
        id INTEGER,
        name VARCHAR NOT NULL,
        secret_name VARCHAR NOT NULL,
        age INTEGER,
        team_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(team_id) REFERENCES team (id)
)
```

### 3.2 创建联系

按照一般创建Hero实例的方式取进行，区别在于team_id的值需要借由已经创建好的team实例的id进行赋值

```python
from sqlmodel import Field, Session, SQLModel, create_engine


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
```

### 3.3 查询

#### 3.3.1 join

如果想要获得hero的信息和他的team的信息，

```python
with Session(engine) as session:
    statement = select(Hero, Team).where(Hero.team_id == Team.id)
```

有一种替代的写法

```python
with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
```

通过join，sqlmodel会自动使用外键进行关联，不再需要where手动关联

此时sql类似于

```sql
SELECT hero.id, hero.name, team.name
FROM hero
JOIN team
ON hero.team_id = team.id
```



不过这种查询只能查到Hero, Team进行关联的数据行，如果`Hero.team_id=NULL`,就查不到

#### 3.3.2 LEFT OUTER

我们希望在结果中包含所有英雄，即使他们没有团队，可以扩展上面使用的 `JOIN` SQL，并在 `JOIN` 之前添加 `LEFT OUTER`

```sql
SELECT hero.id, hero.name, team.name
FROM hero
LEFT OUTER JOIN team
ON hero.team_id = team.id
```

而在sqlmodel里，则变成

```python
with Session(engine) as session:
     statement = select(Hero, Team).join(Team, isouter=True)
```

这相当于先根据Hero表建立结果，再从Team里找能不能和Hero进行关联的部分

### 3.4 更新和删除

就和普通的增查删改一样

```python
hero_spider_boy.team_id = team_preventers.id  # 更新
session.add(hero_spider_boy)
session.commit()
session.refresh(hero_spider_boy)

hero_spider_boy.team_id = None   # 删除
session.add(hero_spider_boy)
session.commit()
session.refresh(hero_spider_boy)
```

当然，这种删除，只是取消了连接，并不是team实例被删除了



## 4.关系属性

### 4.1创建模型

之前是通过where或join以及team_id来连接表的，也可以通过`Relationship`声明一种弱引用的关系属性，直接获取信息

```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")

```

注意：

- `Relationship` 本身只建立单向关系。

- `back_populates` 明确告诉 ORM 两个属性互为镜像，保证对象级别的**双向同步**。

- 如果省略，关系还能查，但对象之间不会自动同步。



### 4.2 创建联系

之前使用外键的时候，需要知道所关联对象的id，此时必须要先提交team实例，再提交hero实例，参考[3.2 创建联系](#32-创建联系)。如果使用`Relationship`,整个过程就只需要commit一次

```python
def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

```

现在我们甚至不必使用 `session.add(team)` 将团队显式放入会话中，因为这些 `Team` 实例**已经与我们确实** `add` 到会话的英雄**关联**。

SQLAlchemy 知道它也必须将这些团队包含在下一次提交中，以便能够正确保存英雄。



当然，也可以先创建hero，再创建team

```python
def create_heroes():
    with Session(engine) as session:

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)

```

### 4.3 更新

更新List就可以使用通用的方法

```python
hero_spider_boy.team = team_preventers
hero_sure_e.team = None

team_wakaland.heroes.append(hero_black_lion)

session.add(hero_spider_boy)
session.add(team_wakaland)
session.add(hero_sure_e)
session.commit()

```

### 4.4 级联删除

#### 4.4.1 ondelete

如果希望在删除某个team实例时，能自动删除相关的hero，则设置`cascade_delete=True`,此时将配置 SQLAlchemy 使用 `cascade="all, delete-orphan"`

```python
heroes: list["Hero"] = Relationship(back_populates="team", cascade_delete=True)
```



这是ORM层面的处理，如果有人 **直接与数据库交互**，而不是python代码，**使用 SQL 删除一个团队** ，则不会发生级联删除，而hero会指向一个不存在的团队team_id。

此时，应配置 `Field()` 中的 `ondelete` 参数，在建立数据库时，让数据集自动处理

```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team", cascade_delete=True)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")
    team: Team | None = Relationship(back_populates="heroes")

```



`ondelete` 参数将在数据库的 **外键列** 中设置 SQL `ON DELETE`。

`ondelete` 可以有以下值

- `CASCADE`：当相关记录（团队）被删除时，**自动删除此记录** （英雄）。
- `SET NULL`：当相关记录被删除时，将此 **外键** (`hero.team_id`) 字段设置为 `NULL`。
- `RESTRICT`：（默认值）如果存在外键值，则通过引发错误 **阻止** 删除此记录（英雄）。



**注意**：cascade_delete和ondelete要配套修改，不是只改一个就行的，ondelete是数据库层面，cascade_delete是ORM层面，还要结合passive_deletes进行。



#### 4.4.2 passive_deletes

如果您知道您的数据库能够仅通过 `ondelete="CASCADE"` 或 `ondelete="SET NULL"` 正确处理删除或更新，您可以在 `Relationship()` 中使用 `passive_deletes="all"` 来告诉 SQLModel（实际上是 SQLAlchemy） **不要在** 为团队发送 `DELETE` 之前 **删除或更新** 这些记录（对于英雄）。

```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, text

SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON")) #sqlite only  # 解除外键约束
        
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team", passive_deletes="all")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(
        default=None, foreign_key="team.id", ondelete="SET NULL"
    )
    team: Team | None = Relationship(back_populates="heroes")

```

## 5.多对多模型

**多对多**关系需要额外建立一个链接表，并且用`link_model`进行关联

```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.teams)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.teams)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.teams)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
```

## 6. fastapi的使用

```python
# 更新
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
```

