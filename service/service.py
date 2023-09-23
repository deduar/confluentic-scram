from coco_cfp_pfm_es.cfp_pfm_es import config_pfm_es, CFP

class SERVICE:

    def __init__(self):
        pass
    
    def cfp_cfp(self,conf):
        return CFP(conf=conf)
    
    def dic_mov(self,dic):
        return CFP().dic_to_mov(dic=dic)

    def run_service(self):

        cfp = CFP(conf=config_bfm_es.load())

        dic = [
            {
            "user_id": "TEST123",
            "amount": "-10.3",
            "date": "2023/01/03",
            "title": "compras Zara",
            "category":"automóvil y transporte",
            "subcategory":"gasolineras"    
            },
            {
            "user_id": "TEST124",
            "amount": "-10.3",
            "date": "2023-08-08",
            "title": "compras Zara",
            "category":"automóvil y transporte",
            "subcategory":"factura gas"    
            },
            {
            "user_id": "TEST124",
            "amount": "-45.3",
            "date": "2023-08-08",
            "title": "compras Zara",
            "category":"automóvil y transporte",
            "subcategory":"restauración"    
            },
            {
            "user_id": "TEST124",
            "amount": "-15.3",
            "date": "2023-08-08",
            "title": "compras Zara",
            "category":"automóvil y transporte",
            "subcategory":"restauración"    
            },
            {
            "user_id": "TEST123",
            "amount": "-10.3",
            "date": "2023-08-08",
            "title": "compras Zara",
            "category":"automóvil y transporte",
            "subcategory":"factura electricidad"    
            }
        ]

        for mov_to in dic:
            mov = cfp.dic_to_mov(dic=mov_to)
            print(cfp.estimateCFP(mov=mov))
