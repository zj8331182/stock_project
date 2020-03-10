<template>
    <div class="content">
        <div class="edit_div">
            <label for="stock_number">请输入股票代码</label><input id="stock_number" v-model="stock_number"
                                                            placeholder="stock number">
            <button v-on:click="get_stock_detail">搜索</button>
        </div>
        <div id="price_chart">
        </div>
        <div id="finance_chart">
        </div>
    </div>
</template>

<script>
    import AxiosInstance from "axios";
    import echarts from 'echarts'

    function transformDataToDate(price_list) {
        const prices = [];
        let date;
        for (let i in price_list) {
            let date_str = price_list[i]['fields']['date'];
            date = new Date();
            // // console.log(date_str.slice(0,4));
            // console.log(date_str.slice(4,6));
            // console.log(date_str.slice(6,8));
            date.setFullYear(Number(date_str.slice(0, 4)), Number(date_str.slice(4, 6)), Number(date_str.slice(6, 8)));
            console.log(date);
            prices.push(date.valueOf())
        }
        return prices
    }

    export default {
        // el: "#home",

        data() {
            return {
                stock_number: '',
                price_list: [],
            }
        },
        methods: {
            get_stock_detail: function () {
                let that = this;
                // let priceChart = echarts.init(document.getElementById('price_chart'));
                // priceChart.setOption(this.option);
                AxiosInstance.get('http://127.0.0.1:8000/api/list_stock_prices?stock_number=' + this.stock_number)
                    .then(function (response) {
                        console.log(response);
                        that.price_list = response.data.price_list;
                    })
            },
        },
        watch: {
            price_list: {
                handler(newVal, oldVal) {
                    let priceChart = echarts.init(document.getElementById('price_chart'));
                    if (priceChart) {
                        if (newVal !== oldVal) {
                            let polar = {
                                legend: {
                                    data: ['开盘价', '收盘价', '最高价', '最低价']
                                },
                                title: {
                                    text: '股票价格表'
                                },
                                xAxis: {
                                    type: 'time',
                                    name: '日期',
                                    data: transformDataToDate(newVal)
                                },
                                yAxis: {
                                    type: 'value',
                                    name: '价格',
                                },
                                tooltip: {
                                    trigger: 'axis'
                                },
                                series: transformDataToClosePrices(newVal),
                            };
                            priceChart.setOption(polar);
                        }
                    }

                },
            }
        }
    }

    function buildData(closeObj, name, prices) {
        closeObj['name'] = name;
        closeObj['type'] = 'line';
        closeObj['data'] = prices;
    }

    function transformDataToClosePrices(price_list) {
        // console.log(price_list);
        const series = [];
        const close_prices = [];
        // const open_prices = [];
        // const high_prices = [];
        // const low_prices = [];
        const closeObj = {};
        // const openObj = {};
        // const highObj = {};
        // const lowObj = {};
        let date;
        for (let i in price_list) {
            let date_str = price_list[i]['fields']['date'];
            date = new Date();
            // // console.log(date_str.slice(0,4));
            // console.log(date_str.slice(4,6));
            // console.log(date_str.slice(6,8));
            date.setFullYear(Number(date_str.slice(0, 4)), Number(date_str.slice(4, 6)) - 1, Number(date_str.slice(6, 8)));
            close_prices.push([date.valueOf(), price_list[i]['fields']['close_price']]);
            // open_prices.push([date.valueOf(), price_list[i]['fields']['open_price']]);
            // high_prices.push([date.valueOf(), price_list[i]['fields']['high_price']]);
            // low_prices.push([date.valueOf(), price_list[i]['fields']['low_price']])
        }
        buildData(closeObj, "收盘价", close_prices);
        // buildData(openObj, "开盘价", open_prices);
        // buildData(highObj, "最高价", high_prices);
        // buildData(lowObj, "最低价", low_prices);

        series.push(closeObj);
        // series.push(openObj);
        // series.push(highObj);
        // series.push(lowObj);
        // console.log(series);
        return series;
    }
</script>

<style>
    .content {
        width: 100%;
        height: 100%;
        flex-direction: column;
    }

    .edit_div {
        width: max-content;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: flex-start;
        align-items: stretch;
        align-content: stretch;
    }

    #price_chart {
        width: 40%;
        height: 480px;
    }
</style>
