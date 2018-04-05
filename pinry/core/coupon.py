# -*- coding: utf-8 -*-
import django
from django.core import serializers


class buyer(object):
    # goods_in_warehouse = [model]
    # goods_in_window = [model]
    def get_market(self):
        import top.api

        req = top.api.TbkDgItemCouponGetRequest()
        req.set_app_info(top.appinfo('24521510', 'cdaf54fdf7f03e78cb70739c6e1e260e'))

        req.adzone_id = 105952310
        req.platform = 1
        # req.cat="16,18"
        req.page_size = 20
        # req.q="女装"
        req.page_no = 1
        try:
            resp = req.getResponse()
            return resp
            # get_item_0 = resp['tbk_dg_item_coupon_get_response']['results']['tbk_coupon'][0]

        except Exception, e:
            print(e)

            # return list of product[json]

    def put_onto_shelf(self, resp):

        pass

    def judge_and_put(self, to_judge_list):

        # 剩余数量少于20%
        # for item in to_judge_list:
        # if item.coupon_remain_count/coupon_total_count < 0.2
        # then goods_in_warehouse.create(goods_id = item.num_iid)
        # then goods_in_window.create(WITH EVERY SINGLE ATTRIBUTE)


        pass


#jack = buyer()
#market = jack.get_market()
#print market
