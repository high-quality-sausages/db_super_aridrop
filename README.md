# db_super_airdrop
## 数据库工具超级空投箱🔧📦
对python常用db库进行整合与封装，目前支持PostgreSQL🐘与redis📦的部分功能，后续将完善功能并添加对MySQL🐳与MongoDB🥭的支持
### 使用方法
#### 1. 进入要引用本工具的项目目录，在.gitignore中添加'db_super_aridrop/'
#### 2. git clone https://github.com/high-quality-sausages/db_super_airdrop.git
#### 3. pip3 install requirements.txt
clone后的目录结构应如下：
```
'yourprojectname'
├── .gitignore(hidden)
└── db_super_airdrop
    ├── README.md
    ├── pg_handle.py
    ├── redis_handle.py
    ├── .gitignore(hidden)
    └── requirements.txt
```
完成上述步骤后即可对XXHandler进行引用，在使用前请确保本地db服务已正常运行<br/>
执行以下代码将在PostgreSQL中新建名为'test_db'的数据库：
``` 
from db_super_airdrop.pg_handle import PgHandler

if __name__ == "__main__":
    pg_handler = PgHandler()
    pg_handler.create_database('test_db')
```
