class Conversions:

    @staticmethod
    def dispatch(data):
        if data['phonetic_name'] == 'handbrake_status':
            return Conversions._handbrake_status(data)

    @staticmethod
    def _handbrake_status(data):
        r = (((data['dec_data'][1] - 208) * 256) + data['dec_data'][0]) / 16
        print(r)

