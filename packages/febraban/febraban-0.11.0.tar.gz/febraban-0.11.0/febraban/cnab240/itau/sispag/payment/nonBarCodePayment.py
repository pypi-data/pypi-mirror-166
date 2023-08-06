from febraban.cnab240.itau.sispag.payment.segmentN import SegmentN


class NonBarCodePayment:
    def __init__(self):
        self.segmentN = SegmentN()
        self.amount = 0
        self.otherAmount = 0
        self.additionAmount = 0
        self.totalAmount = 0

    def toString(self):
        return "\r\n".join((
            self.segmentN.content,
        ))

    def amountInCents(self):
        return self.amount

    def otherAmountInCents(self):
        return self.otherAmount

    def additionAmountInCents(self):
        return self.additionAmount

    def totalAmountInCents(self):
        return self.totalAmount

    def setIdentifier(self, identifier):
        self.segmentN.setIdentifier(identifier)

    def setSender(self, user):
        self.segmentN.setSenderBank(user.bank)

    def setPositionInLot(self, index):
        self.segmentN.setPositionInLot(index)

    def setLot(self, lot):
        self.segmentN.setLot(lot)

