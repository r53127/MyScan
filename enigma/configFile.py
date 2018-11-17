import shelve

class Config():
    def __init__(self):
        #班级位数
        self.CLASS_BITS = 0
        #学号位数
        self.STU_BITS = 2
        # 题目行數
        self.ANSWER_ROWS = 20
        # 题目列数
        self.ANSWER_COLS = 3
        # 学号区excel列数
        self.Stuid_AREA_COLS = 7
        # 学号区excel行数
        self.Stuid_AREA_ROWS = 28
        # 学号第一个数字起始X偏移单元格数
        self.ID_X_OFFSET = 2
        # 学号第一个数字起始Y偏移单元格数
        self.ID_Y_OFFSET = 3
        # 每题选项
        self.PER_CHOICE_COUNT = 4
        #每题得分
        self.PER_ANS_SCORE=3
        #部分得分
        self.PART_ANS_SCORE=0
        self.data_path = 'data\config'
        self.loadCfg()

    # shelve是用key来访问的，使用起来和字典类似
    # 也可用shelf.get()默认返回None来检测空字典
    # shelve可以像字典一样同时操作多个名称的数据对象，但pickle只能同时操作一个数据对象
    def saveCfg(self, cfg):
        with shelve.open(self.data_path) as sh:
            sh.writeback = True
            sh['data'] = cfg

    def loadCfg(self):
        with shelve.open(self.data_path) as sh:
            try:
                cfg = sh['data']
            except BaseException:
                return None
            else:
                self.STU_BITS=cfg.STU_BITS
                self.CLASS_BITS=cfg.CLASS_BITS
                self.ANSWER_ROWS = cfg.ANSWER_ROWS
                self.ANSWER_COLS = cfg.ANSWER_COLS
                self.Stuid_AREA_COLS = cfg.Stuid_AREA_COLS
                self.Stuid_AREA_ROWS = cfg.Stuid_AREA_ROWS
                self.ID_X_OFFSET = cfg.ID_X_OFFSET
                self.ID_Y_OFFSET = cfg.ID_Y_OFFSET
                self.PER_CHOICE_COUNT = cfg.PER_CHOICE_COUNT
                self.PART_ANS_SCORE=cfg.PART_ANS_SCORE
                self.PER_ANS_SCORE=cfg.PER_ANS_SCORE



