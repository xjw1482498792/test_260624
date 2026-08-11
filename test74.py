#反射
class UserService:
    def create(self):
        return "创建用户"

    def delete(self):
        return "删除用户"


service = UserService()
action = "create"

if hasattr(service, action):
    method = getattr(service, action)
    result = method()
    print(result)