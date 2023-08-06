import json
import platform
import subprocess
import sys
import re
from getpass import getpass
import requests
import jwt
import urllib.parse


class PythonApi:
    def version(self):
        try:
            version = platform.python_version_tuple()
            return {
                "str": platform.python_version(),
                "major": int(version[0]),
                "minor": int(version[1]),
                "patch": int(version[2]),
            }
        except Exception as e:
            print(e)
            print('获取 Python 版本失败，建议重新安装 Python！')
            exit(0)


class PipApi:
    python_location = sys.executable

    def call(self, *args, cwd=None):
        try:
            result = subprocess.check_output([self.python_location, "-m", "pip"] + list(args), cwd=cwd)
            return result.decode()
        except subprocess.CalledProcessError as e:
            print(e.output.decode("utf-8"))
            print('pip 指令执行失败，建议重新安装 pip！')
            exit(0)

    def get_installed_packages(self):
        raw_str = self.call("freeze")
        raw_str = re.sub(r'\r*\n+', '\n', raw_str)
        packages = []
        for package_str in raw_str.split('\n'):
            if not package_str or package_str.find('==') == -1:
                continue
            [name, ver] = package_str.split('==')
            packages.append({"name": name, "version": ver})

        return packages


class IcodeApi:
    common_header = {
        'Authorization': ''
    }

    user_id = ''

    icode_url = 'https://api.icode123.cn'

    def _request(self, method, url, data=None, headers=None):
        try:
            if headers:
                headers.update(self.common_header)
            else:
                headers = self.common_header
            return requests.request(method, self.icode_url + url, json=data, headers=headers).json()
        except Exception as e:
            print('请求失败，请检查网络连接')
            exit(0)

    def _get(self, url):
        return self._request('GET', url)

    def _put(self, url, data, headers=None):
        return self._request('PUT', url, data=data, headers=headers)

    def _post(self, url, data, headers=None):
        return self._request('POST', url, data=data, headers=self.common_header)

    def _patch(self, url, data, headers=None):
        return self._request('PATCH', url, data=data, headers=self.common_header)

    def _upload_classroom_packages(self, classroomId, require_packages, installed_packages):
        """ 上传班级依赖 """
        # 筛选出班级中需要的，其它的不上传
        installed = [{
            'name': 'Python',
            'version': PythonApi().version()['str'],
        }]
        for package in installed_packages:
            for require_package in require_packages:
                if package['name'].lower() == require_package['name'].lower() and \
                        package['version'] == require_package['version']:
                    installed.append(package)

        ext_id = urllib.parse.quote(json.dumps({
            'owner': self.user_id,
            'classroom': classroomId,
        }))

        old = self._get('/Requirement/' + ext_id)
        header = {}
        if old.get('_etag', None):
            header['If-Match'] = old['_etag']

        response = self._put('/Requirement/' + ext_id, {
            'classroom': classroomId,
            'packages': installed,
        }, header)
        return response

    def login(self):
        """ 登录 Python123 帐号 """
        while True:
            email = input('请输入 Icode123 邮箱：')
            password = getpass('请输入 Icode123 密码：')
            response = self._put('/Session', {
                'email': email,
                'password': password
            })

            if response.get('token', '') == '':
                print('邮箱或密码错误，请重新输入')
                continue

            token = response["token"]

            # decode token
            payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})

            self.user_id = payload["id"]
            self.common_header["Authorization"] = 'Bearer ' + token
            break

    def get_classrooms(self):
        """ 获取学生所有加入班级 """
        response = self._get('/ClassroomStudent/joined')
        return response.get('_items', []) or []

    def get_classroom_requirements(self, _id):
        requirements = {
            "python_version": None,
            "packages": [],
        }
        """ 获取班级需要安装的依赖 """
        response = self._get('/Classroom/' + _id)
        if response.get('requirement', None) is None:
            return []
        response = self._get('/Requirement/' + response['requirement'])
        packages = response.get('packages', [])

        # 是否需要特定 Python 版本
        need_python = [p for p in packages if p['name'] == 'Python']
        if len(need_python):
            parts = need_python[0]['version'].split('.')
            requirements['python_version'] = {
                'str': need_python[0]['version'],
                'major': int(parts[0]),
                'minor': int(parts[1]) if len(parts) > 1 else 0,
                'patch': int(parts[2]) if len(parts) == 3 else 0,
            }
        # 过滤出 Python 依赖
        requirements['packages'] = [p for p in packages if
                                    (p['language'] == 'python' and str(p['name']).lower() != 'python')]
        return requirements

    def compare_classroom_packages(self, classroomId):
        print('正在检查本机已安装 Python 包...')
        requirement = self.get_classroom_requirements(classroomId)
        require_packages = requirement.get('packages', [])
        installed_packages = PipApi().get_installed_packages()

        require_python_version = requirement['python_version']
        installed_python_version = PythonApi().version()
        if require_python_version:
            if installed_python_version['major'] < require_python_version['major']:
                print('本机已安装 Python%s 版本过低，请重新下载安装 Python%s' % (
                    installed_python_version['str'], requirement['python_version']['str']))
                exit(0)
            elif installed_python_version['major'] == require_python_version['major']:
                if installed_python_version['minor'] < require_python_version['minor']:
                    print('本机已安装 Python%s，如果依赖无法正常安装，建议升级到 Python%s' %
                          (installed_python_version['str'], requirement['python_version']['str']))

        self._upload_classroom_packages(classroomId, require_packages, installed_packages)

        # 比较安装的依赖和班级需要的依赖
        uninstalled = []
        for package in require_packages:
            for installed_package in installed_packages:
                if package['name'].lower() == installed_package['name'].lower():
                    if package['version'] == installed_package['version']:
                        break
                    else:
                        print('{} 版本不匹配'.format(package['name']))
                        uninstalled.append(package)
            else:
                print('{} 未安装'.format(package['name']))
                uninstalled.append(package)
        return uninstalled

    def install_classroom_packages(self, packages):
        """ 安装班级依赖 """
        for package in packages:
            print('正在安装 {}'.format(package['name']))
            ret = PipApi().call('install', package['name'] + '==' + package['version'], '-i',
                                'https://pypi.tuna.tsinghua.edu.cn/simple')
            if ret.find('Successfully installed'):
                print('{} 安装成功'.format(package['name']))


def main():
    python = PythonApi()
    pip = PipApi()
    icode = IcodeApi()
    icode.login()
    joined_classrooms = icode.get_classrooms()
    if not len(joined_classrooms):
        print('请先加入班级后再进行环境配置')
        exit(0)
    for i in range(len(joined_classrooms)):
        print(str(i + 1) + '.' + joined_classrooms[i]['classroomId']['name'])
    select_index = 0
    if len(joined_classrooms) > 1:
        while True:
            try:
                select_index = int(input('请输入班级序号：')) - 1
                if 0 <= select_index < len(joined_classrooms) - 1:
                    break
            except:
                pass
    classroom_id = joined_classrooms[select_index]['classroomId']["_id"]
    need_install = icode.compare_classroom_packages(classroom_id)
    if len(need_install):
        confirm = input('是否安装依赖？(y/n)')
        if confirm == 'y' or confirm == 'Y':
            icode.install_classroom_packages(need_install)
            print('正在重新检查...')
            need_install = icode.compare_classroom_packages(classroom_id)
            if len(need_install):
                print('有依赖无法自动安装，请尝试手动安装')
                exit(0)
    print('\n环境安装完成!')
