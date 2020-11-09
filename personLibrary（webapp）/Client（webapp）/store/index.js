import Vue from "vue"
import Vuex from "vuex"
import helper from "../common/until.js"
Vue.use(Vuex);
const store=new Vuex.Store({
	state:{ //超全局变量,任何一个页面都可以调用,不允许直接修改
		
	},
	mutations:{
		//必须是同步函数
		//this.$store.commit("INIT_CARTS",[])
		INIT_CARTS(state,data){
			
		}
	},
	actions:{
		//异步函数可以写到这里面
		init_carts(context){
			uni.request({
				url:this.helper.baseUrl+"/cart/init",
				success: (res) => {
					context.commit("INIT_CARTS",res.data);
				}
			})
			
		}
	}
})
export default store