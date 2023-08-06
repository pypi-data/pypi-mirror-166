import local_plot

class plot:

    def __new__(self, filename, start_date, end_date, para_dict, result_df, gen_name):

        app = local_plot.main().plot(filename, start_date, end_date, para_dict, result_df, gen_name)

        return app
