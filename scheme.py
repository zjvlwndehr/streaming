class time_scheme:
    hh = 0
    mm = 0
    ss = 0
    def __init__(self, hh = 0, mm = 0, ss = 0):
        if hh < 0 or mm < 0 or ss < 0:
            raise ValueError('Time scheme cannot be less than 0')
        if hh >= 24:
            raise ValueError('Time scheme cannot be bigger than 24')
        if mm >= 60:
            hh += mm // 60
            mm = mm % 60
        if ss >= 60:
            mm += ss // 60
            ss = ss % 60

        self.hh = hh
        self.mm = mm
        self.ss = ss
    
    def __str__(self) -> str:
        return f'{self.hh}:{self.mm}:{self.ss}'
    
    def __to_seconds__(self) -> int:
        return int(self.hh)*3600 + int(self.mm)*60 + int(self.ss)
    
    def __to_str_seconds__(self) -> str:
        return str(self.__to_seconds__())