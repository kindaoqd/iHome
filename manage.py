# -*- coding:utf-8 -*-
from iHome import get_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import models

app = get_app('development')
# 构造migrate实例，关联app与db
Migrate(app, db)
# 创建迁移管理类实例并关联app
manager = Manager(app)
# 添加迁移命令并起别名‘db’
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print app.url_map
    # app.run(debug=True)
    # 使用迁移管理器运行
    manager.run()
