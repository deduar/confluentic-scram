import enum
from dataclasses import dataclass
from dataclasses_avroschema import AvroModel

from dotenv import load_dotenv


@dataclass
class ConsumerModel(AvroModel):
    "An RAW - {'identifier':'TEST124','amount':'-15,3','date':'2023-08-08','title':'compras Zara','cat_id':77}"
    identifier: str
    amount: float
    date: str
    title: str
    cat_id: int

    class Meta:
        namespace = "Consumer.v1"
        aliases = ["consumer-v1", "super Consumer"]

    def set_identifier(self,identifier):
        self.identifier = identifier

    def set_amount(self,amount):
        self.amount = amount

    def set_date(self,date):
        self.date = date

    def set_title(self,title):
        self.title = title

    def set_cat_id(self,cat_id):
        self.cat_id = cat_id


    def get_identifier(self):
        return self.identifier
    
    def get_amount(self):
        return self.amount
    
    def get_date(self):
        return self.date
    
    def get_title(self):
        return self.title
    
    def get_cat_id(self):
        return self.cat_id


@dataclass
class ProducerModel(AvroModel):
    "An CFP - {'co2': 18.92368421052632, 'ch4': 0.1589589473684211, 'n2o': 0.0005790647368421054, 'h2o': 0, 'sup': 0.0}"
    co2: float
    ch4: float
    n2o: float
    h2o: float
    sup: float

    class Meta:
        namespace = "Producer.v1"
        aliases = ["producer-v1", "super Producer"]

    def set_co2(self,co2):
        self.co2 = co2

    def set_ch4(self,ch4):
        self.ch4 = ch4

    def set_n2o(self,n2o):
        self.n2o = n20
    
    def set_h2o(self,h2o):
        self.h2o = h2o

    def set_sup(self,sup):
        self.sup = sup
