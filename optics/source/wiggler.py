__author__ = 'labx'


from optics.source.insertion_device import InsertionDevice

class Wiggler(InsertionDevice):

    def __init__(self, K, period_length, periods_number):
        InsertionDevice.__init__(self, K, 0.0, period_length, periods_number)