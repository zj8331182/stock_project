import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/line'


Vue.config.productionTip = false;

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
Vue.component('v-chart', ECharts);
require('echarts/lib/chart/line');
// 以下的组件按需引入
require('echarts/lib/component/tooltip');   // tooltip组件
require('echarts/lib/component/title');  //  title组件
require('echarts/lib/component/legend');
