from yzcore.extensions.aliyun_oss import OssManager
from yzcore.extensions.huawei_obs import ObsManager


class StorageManage(object):
    """
    通用的对象存储封装，根据mode选择oss/obs等等
    mode,
    access_key_id,
    access_key_secret,
    bucket_name,
    endpoint=None,
    cname=None,
    cache_path='.',
    expire_time=30,

    """

    def __new__(cls, **kwargs):
        if kwargs['mode'] == 'obs':
            storage_manage = ObsManager(**kwargs)
        elif kwargs['mode'] == 'oss':
            storage_manage = OssManager(**kwargs)
        else:
            storage_manage = None
        return storage_manage


if __name__ == '__main__':

    oss_conf = {
        'mode': 'oss',
        'access_key_id': 'LTAI4GCahbN1hoc4DBpwoYuK',
        'access_key_secret': 'TpVOzSha6dsyksgZWwTnm7BcAGqqUh',
        'bucket_name': 'realicloud-local',
        'endpoint': 'oss-cn-shenzhen.aliyuncs.com',
        'cache_path': '/tmp/realibox/cache/',
        'expire_time': 30,

    }



    file = 'bdab1dda1357051dd6168a9fa812cc26.png'

    manage_oss = StorageManage(**oss_conf)
    print(manage_oss.cache_path, manage_oss.mode, manage_oss.cname)
    # print(manage_oss.upload(file, key='test/image/bdab1dda1357051dd6168a9fa812cc26.png'))
    # manage_oss.check()
    print(1112, manage_oss.get_sign_url(file))
    '''

    obs_conf = {
        'mode': 'obs',
        'access_key_id': 'VPI2DNDCKPFVWT3B5SV8',
        'access_key_secret': 'r9CXkXxp8QpgzXhJOw6ZwsTL0Dq2YyjpGF65CwO8',
        'bucket_name': 'realibox-test',
        'endpoint': 'obs.cn-south-1.myhuaweicloud.com',
        'cache_path': '/tmp/realibox/cache/',
        'expire_time': 30,
        'asset_domain': 'static-public.test.hw-hub.realibox.com',
        'image_domain': 'static-public.test.hw-hub.realibox.com',
    }

    manage_obs = StorageManage(**obs_conf)
    print(manage_obs.cache_path, manage_obs.mode, manage_obs.cname)
    # print(manage_obs.upload(file))
    # manage_obs.check()
    print(manage_obs.iter_objects('test'))
    '''
    obs_conf = {
        'mode': 'obs',
        'access_key_id': 'VPI2DNDCKPFVWT3B5SV8',
        'access_key_secret': 'r9CXkXxp8QpgzXhJOw6ZwsTL0Dq2YyjpGF65CwO8',
        'bucket_name': 'realibox-test-private',
        'endpoint': 'obs.cn-south-1.myhuaweicloud.com',
        'cache_path': '/tmp/realibox/cache/',
        'expire_time': 30,
        'asset_domain': 'static-private.test.hw-hub.realibox.com',
        'image_domain': 'static-private.test.hw-hub.realibox.com',
        'cname': 'static-public.test.hw-hub.realibox.com',
    }
    manage_obs = StorageManage(**obs_conf)
    print(manage_obs.cache_path, manage_obs.mode, manage_obs.cname)
    # print(manage_obs.upload(file))
    # manage_obs.check()
    print(manage_obs.iter_objects('test'))
    key = '759084f3ad2b149908efdd70eaf2fccd.png'
    url = manage_obs.get_sign_url(key, expire=120)
    print(123, url)
