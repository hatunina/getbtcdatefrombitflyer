#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import pandas as pd
from progressbar import ProgressBar
from datetime import datetime as dt
import datetime
import time


class GetBtcDataFromBitflyer(object):

    def __init__(self, count=500, count_limit=200):
        # before id
        self.before_id = 0
        # bit data size
        self.count = count
        # loop size
        self.count_limit = count_limit
        # request url
        self.domain_url = 'https://api.bitflyer.jp'
        self.execution_history_url = '/v1/getexecutions'
        # column array
        self.keys = ['id',
                     'side',
                     'price',
                     'size',
                     'exec_date',
                     'buy_child_order_acceptance_id',
                     'sell_child_order_acceptance_id']

        self.first_time_flag = True

        self.execution_history_params = {'count': self.count,
                                    'before': self.before_id}
        self.arg_date = dt.strptime('2017-11-06 02:50:00', '%Y-%m-%d %H:%M:%S')
        self.change_num_base = 500
        self.target_date_id = 0

    def run(self):
        self.arg_date = self.arg_date.replace(second=0)

        while True:
            start_id, is_find_start_id = self.search_start_id()
            self.execution_history_params['before'] = start_id
            if is_find_start_id:
                self.target_date_id = start_id
                print('The id of the date to be searched was found: {}'.format(self.target_date_id))
                break

        # init DataFrame
        df = pd.DataFrame(columns=self.keys)
        self.execution_history_params['before'] = 0

        while True:
            # init ProgressBar
            p = ProgressBar(0, self.count_limit)
            for progress_num in range(self.count_limit):
                # request execution history
                response = self.execute_api_request(self.execution_history_url, self.execution_history_params)
                time.sleep(0.5)

                btc_list = response.json()

                last_id = btc_list[-1]['id']

                # update parameters with last id
                self.execution_history_params['before'] = last_id

                tmp_df = pd.read_json(response.text)
                df = pd.concat([df, tmp_df])

                result_df = df[df['id'] >= self.target_date_id]

                # show execution progress
                p.update(progress_num)

                if df.shape[0] > result_df.shape[0]:
                    break

            self.save_result_data(result_df)

            if df.shape[0] > result_df.shape[0]:
                break

    # execute api request
    def execute_api_request(self, url, params):
        request_url = self.domain_url + url
        return requests.get(request_url, params=params)

    def format_date(self, date_line):
        tmp_date = date_line.replace('T', ' ')
        tmp_date = tmp_date.split('.')[0]
        date = dt.strptime(tmp_date, '%Y-%m-%d %H:%M:%S')
        date = date.replace(second=0)
        # Adjust ISO format to Japan time
        date = date + datetime.timedelta(hours=9)
        return date

    def save_result_data(self, result_df):
        first_date = self.format_date(result_df['exec_date'].iloc[0])
        last_date = self.format_date(result_df['exec_date'].iloc[-1])

        str_first_date = str(first_date).replace(' ', '-').replace(':00', '')
        str_last_date = str(last_date).replace(' ', '-').replace(':00', '')

        file_name = 'btc_{}_{}.csv'.format(str_first_date, str_last_date)
        result_df.to_csv(file_name, index=False)
        print('save on {}'.format(file_name))

    def search_start_id(self):
        # request execution history
        response = self.execute_api_request(self.execution_history_url, self.execution_history_params)
        time.sleep(0.5)

        search_btc_df = pd.read_json(response.text)

        date = self.format_date(search_btc_df['exec_date'].iloc[0])

        print('looking for date: {}'.format(date))

        start_id, is_find_start_id = self.get_start_id(date, search_btc_df)

        return start_id, is_find_start_id

    def get_start_id(self, date, search_btc_df):
        is_find_start_id = False
        if date < self.arg_date:
            diff_second = (self.arg_date - date).total_seconds()
            change_id_num = self.get_chage_id_num(diff_second)
            start_id = int(search_btc_df['id'][0]) + change_id_num

        elif date > self.arg_date:
            diff_second = (date - self.arg_date).total_seconds()
            change_id_num = self.get_chage_id_num(diff_second)
            start_id = int(search_btc_df['id'][499]) - change_id_num

        else:
            iso_arg_date = self.arg_date - datetime.timedelta(hours=9)
            iso_arg_date = str(iso_arg_date.hour) + ':' + str(iso_arg_date.minute)
            for i, date in enumerate(search_btc_df['exec_date']):
                if iso_arg_date in date:
                    tmp_series = search_btc_df.iloc[i]
                    start_id = tmp_series['id']
            is_find_start_id = True

        return start_id, is_find_start_id

    def get_chage_id_num(self, diff_second):
        diff_minutes = diff_second/60
        diff_hour = diff_minutes/60
        diff_date = diff_hour/24
        diff_week = diff_date/7
        diff_month = diff_week/4
        diff_year = diff_month/12

        if diff_year >= 1:
            # 26,280,000
            # floatだとパラメータが認識されない
            change_id_num = int((self.change_num_base * 60 * 24 * 365) * 0.1)
        elif diff_month >= 1:
            # 4,464,000
            change_id_num = int((self.change_num_base * 60 * 24 * 31) * 0.1)
        elif diff_week >= 1:
            # 10080
            change_id_num = self.change_num_base * 60 * 24 * 7
        elif diff_date >= 1:
            change_id_num = self.change_num_base * 60 * 24
        elif diff_hour >= 1:
            change_id_num = self.change_num_base * 60
        elif diff_minutes >= 1:
            change_id_num = self.change_num_base
        elif diff_minutes == 0:
            change_id_num = 0

        return change_id_num



if __name__ == '__main__':
    get_btc = GetBtcDataFromBitflyer()
    get_btc.run()
