import os

from spt_factory import MongoFactory


if __name__ == '__main__':
    print(os.getenv('SSLROOT'))
    f = MongoFactory(
        mongo_url="mongodb://core-user:vomtug-vagqYt-4gorqu@rc1b-m2glgmwr3860oxfr.mdb.yandexcloud.net:27018/?replicaSet=rs01&authSource=spt",
        tlsCAFile=os.getenv('SSLROOT'),
    )

    # print(f'moniback-telegram = {f.get_any_creds_credentials(type="moniback-telegram")}')
    # print(f'moniback-mlg = {f.get_any_creds_credentials(type="moniback-mlg")}')
    # print(f'postgres = {f.get_postgres_credentials()}')
    #
    # print(f.get_postgres_credentials(**{
    #     'host': 'localhost',
    #     'port': '5432',
    #     'dbname': 'moniback'
    # }))

    # one object, two links
    model_manager_1 = f.get_model_manager()
    # model_manager_2 = f.get_model_manager()

    pipeline_manager = f.get_pipeline_manager()

    tfidf_config = model_manager_1.get_model(model_id='eeb199e8d436749610b298d8ccf88352150358a095be6f750baefbeb0ed16fcb')

    print(tfidf_config)