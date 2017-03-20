# -*- coding: utf-8 -*-
import random
import pickle
import datetime
from numpy import *


my_list2 = open(
    '//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSD5min.txt',
    'rb')
# my_list3数据结构<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>
my_list3 = pickle.load(my_list2)
my_list2.close()


class Strategy:
    account = 10000  # 总额
    equity = 10000  # 净值
    balance = 10000  # 余额
    spread = 3  # 点差
    date = 0
    count = []  # 订单编号
    count_type = []  # 订单类型,buy or sell
    count_finally = []  # 订单最终状态
    count_lot = []  # 订单手数
    count_benefit = []  # 当前订单实时盈亏
    count_Margin = []  # 当前订单占用保证金
    count_all_benifit = 0  # 所有订单盈亏情况合计
    count_all_Margin = 0  # 所有订单占用保证金

    def __init__(self, wave, lot, benefit, loss):
        self.wave = wave
        self.lot = lot
        self.benefit = benefit
        self.loss = loss
        self.count = []  # 订单编号
        self.count_type = []  # 订单类型,buy or sell
        self.count_finally = []  # 订单最终状态
        self.count_lot = []  # 订单手数
        self.count_benefit = []  # 当前订单实时盈亏
        self.count_Margin = []  # 当前订单占用保证金

    # 计算所有订单盈亏
    def def_count_all_benifit(self, x):
        if len(self.count) >0 :
            for b in range(len(self.count)):
                if self.count_finally[b] == 'open':
                    if self.count_type[b] == 'buy':
                        self.count_benefit[b] = (my_list3[x][5] * 10000 - (
                        my_list3[self.count[b]][2] * 10000 + self.spread)) * \
                                                self.count_lot[b]
                    if self.count_type[b] == 'sell':
                        self.count_benefit[b] = ((my_list3[self.count[b]][2] * 10000 - self.spread) - my_list3[x][
                            5] * 10000) * \
                                                self.count_lot[b]
            self.count_all_benifit = 0
            for b in range(len(self.count)):
                if self.count_finally[b] == 'open':
                    self.count_all_benifit = self.count_all_benifit + self.count_benefit[b]

    # 计算所有订单保证金
    def def_count_all_Margin(self):
        if len(self.count) >0 :
            self.count_all_Margin = 0
            for b in range(len(self.count)):
                if self.count_finally[b] == 'open':
                    self.count_all_Margin = self.count_all_Margin + self.count_Margin[b]

    def jiaoyi(self):

        x = 0
        while x < len(my_list3):
            # 更新余额及净值
            # self.def_count_all_benifit(x)
            # self.def_count_all_Margin()
            # self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
            # self.equity = self.account + self.count_all_benifit  # 更新净值

            # 下单模块
            if int((my_list3[x][5] - my_list3[x][2]) * 10000) > self.wave:
                # 更新余额及净值
                self.def_count_all_benifit(x)
                self.def_count_all_Margin()
                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                self.equity = self.account + self.count_all_benifit  # 更新净值
                # 执行买单
                self.count_lot.append(round(self.balance / self.lot, 2))  # 订单手数
                self.count.append(int(x + 1))  # 记录订单编号
                self.count_type.append('buy')  # 记录订单类型
                self.count_finally.append('open')  # 记录订单状态
                self.count_Margin.append(round(self.balance / self.lot, 2) * 1000 * my_list3[x + 1][2])
                self.count_benefit.append((-self.spread) * round(self.balance / self.lot, 2))
                # 更新余额及净值
                self.def_count_all_benifit(x)
                self.def_count_all_Margin()
                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                self.equity = self.account + self.count_all_benifit  # 更新净值

            if int((my_list3[x][2] - my_list3[x][5]) * 10000) > self.wave:
                # 更新余额及净值
                self.def_count_all_benifit(x)
                self.def_count_all_Margin()
                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                self.equity = self.account + self.count_all_benifit  # 更新净值
                # 执行卖单
                self.count_lot.append(round(self.balance / self.lot, 2))  # 订单手数
                self.count.append(int(x + 1))  # 记录订单编号
                self.count_type.append('sell')  # 记录订单类型
                self.count_finally.append('open')  # 记录订单状态
                self.count_Margin.append(round(self.balance / self.lot, 2) * 1000 * my_list3[x + 1][2])
                self.count_benefit.append((-self.spread) * round(self.balance / self.lot, 2))
                # 更新余额及净值
                self.def_count_all_benifit(x)
                self.def_count_all_Margin()
                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                self.equity = self.account + self.count_all_benifit  # 更新净值

            # 平单模块
            if len(self.count) > 0:
                for b in range(len(self.count)):
                    if self.count_finally[b] == 'open':
                        if self.count_type[b] == 'buy':
                            if int(my_list3[self.count[b]][2] * 10000 + self.spread - my_list3[x][
                                4] * 10000) >= self.loss:
                                self.account = self.account - self.count_lot[b] * (
                                int(my_list3[self.count[b]][2] * 10000 + self.spread - my_list3[x][4] * 10000)) * 10
                                self.count_finally[b] = 'close'
                                # 更新余额及净值
                                self.def_count_all_benifit(x)
                                self.def_count_all_Margin()
                                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                                self.equity = self.account + self.count_all_benifit  # 更新净值
                            if int(my_list3[x][3] * 10000 - self.spread - my_list3[self.count[b]][
                                2] * 10000) >= self.benefit:
                                self.account = self.account + self.count_lot[b] * (self.benefit) * 10
                                self.count_finally[b] = 'close'
                                # 更新余额及净值
                                self.def_count_all_benifit(x)
                                self.def_count_all_Margin()
                                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                                self.equity = self.account + self.count_all_benifit  # 更新净值

                        if self.count_type[b] == 'sell':
                            if int(my_list3[x][3] * 10000 - my_list3[self.count[b]][
                                2] * 10000 + self.spread) >= self.loss:
                                self.account = self.account - self.count_lot[b] * (
                                int(my_list3[x][3] * 10000 - my_list3[self.count[b]][2] * 10000 + self.spread)) * 10
                                self.count_finally[b] = 'close'
                                # 更新余额及净值
                                self.def_count_all_benifit(x)
                                self.def_count_all_Margin()
                                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                                self.equity = self.account + self.count_all_benifit  # 更新净值
                            if int(my_list3[self.count[b]][2] * 10000 - my_list3[x][
                                4] * 10000 - self.spread) >= self.benefit:
                                self.account = self.account + self.count_lot[b] * (self.benefit) * 10
                                self.count_finally[b] = 'close'
                                # 更新余额及净值
                                self.def_count_all_benifit(x)
                                self.def_count_all_Margin()
                                self.balance = self.account + self.count_all_benifit - self.count_all_Margin  # 更新余额
                                self.equity = self.account + self.count_all_benifit  # 更新净值
            if self.account < 5000:
                break
            x += 1

# 从上次留存程序开始
my_list5 = open(
    '//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSDcelue201727.txt',
    'rb')
short_program = pickle.load(my_list5)
my_list5.close()

jinhua_count = int(input("执行进化次数_百次")) * 100
a = len(short_program)
begin_count = len(short_program)

# 进化开始，1、2结合，2、3结合
short_program.append([0, 0, 0, 0, 0, 0])
while True:
    if a % 100 < 60:
        # 转置策略列表得到转置后short_program2，
        short_program1 = array(short_program)
        short_program1 = short_program1.transpose()
        short_program2 = list(short_program1)
        short_program[a][0] = random.choice(
            [short_program[a - 100 * (a // 100)][0], random.choice(short_program2[0])])
        short_program[a][1] = random.choice(
            [short_program[a - 100 * (a // 100)][1], random.choice(short_program2[1])])
        short_program[a][2] = random.choice(
            [short_program[a - 100 * (a // 100)][2], random.choice(short_program2[2])])
        short_program[a][3] = random.choice(
            [short_program[a - 100 * (a // 100)][3], random.choice(short_program2[3])])
        strategy = Strategy(
            short_program[a][0],
            short_program[a][1],
            short_program[a][2],
            short_program[a][3])
        strategy.jiaoyi()
        # 赔钱则重新取值交易
        # if strategy.account < 10000:
        #     continue
        # 赚钱则存储，4为终值，5为交易笔数
        short_program[a][4] = round(strategy.equity, 2)
        short_program[a][5] = len(strategy.count)
        a += 1
    else:
        # 随机取值
        short_program[a][0] = random.randint(1, 50)
        short_program[a][1] = random.randint(100, 100000)
        short_program[a][2] = random.randint(1, 1000)
        short_program[a][3] = random.randint(1, 1000)
        # 短线交易得到终值
        strategy = Strategy(
            short_program[a][0],
            short_program[a][1],
            short_program[a][2],
            short_program[a][3])
        strategy.jiaoyi()
        # 赔钱则重新取值交易
        if strategy.account < 10000:
            continue
        if strategy.equity < 10000:
            continu
        if strategy.balance < 10000:
            continue
        # #赚钱则存储，4为终值，5为交易笔数
        short_program[a][4] = round(strategy.equity, 2)
        short_program[a][5] = len(strategy.count)
        a += 1
    if a % 100 == 0:
        short_program = sorted(short_program, key=lambda program: program[4], reverse=True)
        d = int((a - 100) / 100)
        print("进化第 %d 轮结果是：" % d)
        print(short_program[:(10 * (a // 100))])
        print("已获得%e条策略" % int(a))
    if ((a - begin_count) - jinhua_count) >= 0:
        zhongduan = input("是否继续执行进化？yes/no")
        if zhongduan == "no":
            today = datetime.date.today()
            new_address = '//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSDcelue' + \
                          str(today.year) + str(today.month) + str(today.day) + '_1.txt'
            my_list4 = open(new_address, 'wb')
            pickle.dump(short_program, my_list4)
            my_list4.close()
            break
        jinhua_count = int(input("再次执行进化次数_百次")) * 100
        begin_count = len(short_program)
    short_program.append([0, 0, 0, 0, 0, 0])
