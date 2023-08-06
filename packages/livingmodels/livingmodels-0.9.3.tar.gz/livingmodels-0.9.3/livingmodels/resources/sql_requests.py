class SqlRequests:

    """ Хранилище SQL запросов """

    @staticmethod
    def transformation_to_ts_vector():
        """ запрос для генерации в ts_vector JSONB """

        return "to_tsvector('russian', jsonb_path_query_array(service_model_data,'strict $.**.visitor') ||" \
               " jsonb_path_query_array(service_model_data,'strict $.**.phone'))"
