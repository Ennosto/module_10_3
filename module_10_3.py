import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        kolvo = 100
        while kolvo:
            summa = random.randint(50, 500)
            self.balance += summa
            print(f'Пополнение: {summa}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            time.sleep(0.001)
            kolvo -= 1

    def take(self):
        kolvo = 100
        while kolvo:
            summa = random.randint(50, 500)
            print(f'Запрос на {summa}')
            if summa <= self.balance:
                self.balance -= summa
                print(f'Снятие: {summa}. Баланс: {self.balance}')
            else:
                print(f'Запрос отклонен. Недостаточно средств')
                self.lock.acquire()
            kolvo -= 1


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
