<template>
    <div id="app">
        <p id="app_title">小丶诸侯的信息站</p>
        <div id="nav">
            <router-link to="/">个股详情</router-link>
            |
            <a href="admin">
                <button>添加股票数据</button>
            </a>
        </div>
        <router-view/>
    </div>
</template>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #app_title {
        color: #2c3e50;
        font-size: large;
        font-weight: bolder;
    }

    #nav {
        padding-bottom: 30px;
    }

    #nav a {
        font-weight: bold;
        color: #2c3e50;
    }

    #nav a.router-link-exact-active {
        color: #42b983;
    }
</style>
