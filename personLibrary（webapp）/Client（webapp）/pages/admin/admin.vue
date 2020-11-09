<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="book_place">
			<text>管理员中心</text>
		</view>
		
		<view class="main-grid">
			<view class="main-top" style="background-image: url(../../static/bkjpg.jpg);">
				<image src="../../static/img/admin-phone.png" style="width: 100upx;height: 100upx;"></image>
				<view class="" style="width: 250upx;height: 47.2upx;">
					管理员ID:{{adminuser==""?"":adminuser.waid}}
				</view>
				<view class="" style="width: 250upx;height: 47.2upx;">
					管理员名:{{adminuser==""?"":adminuser.wadminname}}
				</view>
			</view>
			<view class="main-admin">
				<view @tap="goitem(p.url)" style="border: 1px solid gray;" class="grid-item bg-white" v-for="(p,i) in list_item" :key="i">
					<image :src="p.url_log" style="width: 80upx;height: 80upx;margin-right: 10upx;margin-bottom: -20upx;margin-top: -20upx;margin-left: -10upx;"></image>
					<text>{{p.text}}</text>
				</view>
				
			</view>
		</view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				adminuser:"",
				list_item:[
					{
						text:"用户管理",
						url_log:"../../static/adminlog/usermanage.png",
						url:"./user_manage"
					},
					{
						text:"图书管理",
						url_log:"../../static/adminlog/bookmanage.png",
						url:"./book_manage"
					},
					{
						text:"读书广场",
						url_log:"../../static/adminlog/placemanage.png",
						url:"./place_manage"
					},
					{
						text:"用户留言",
						url_log:"../../static/adminlog/liuyanmanage.png",
						url:"./liuyan_manage"
					},
					{
						text:"公告管理",
						url_log:"../../static/adminlog/gonggaomanage.png",
						url:"./gongao_manage"
					},
					{
						text:"书籍上传",
						url_log:"../../static/adminlog/bookshangc.png",
						url:"./book_update"
					},
					{
						text:"站内消息",
						url_log:"../../static/adminlog/zhanneisixin.png",
						url:"./admin_message"
					},{
						text:"关于我们",
						url_log:"../../static/adminlog/guanyuwoema.png",
						url:"./guanyuwomen"
					},{
						text:"图书首页",
						url_log:"../../static/adminlog/bookshouye.png",
						url:"../index/index"
						
					},{
						text:"退出登录",
						url_log:"../../static/adminlog/exitlogin.png",
					}
				]
			}
		},
		onLoad() {
			this.getad();
			setTimeout(function() {
				// console.log('start pulldown');
			}, 1000);
			uni.startPullDownRefresh({
				success: function(res) {
					// console.log(res); //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画
		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			// console.log('refresh');
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.getad();
		},
		methods: {
			goitem(url){
				var data=""
				try{
					const res=uni.getStorageSync("adminim");
					data =JSON.parse(res);
				} catch(e){
					
				}
				if(data!=""){
					if(url!=null || url!=undefined){
						if(url=="./user_manage"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="./book_manage"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="./place_manage"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="./liuyan_manage"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="./gongao_manage"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="./book_update"){
							uni.showToast({
								icon:"none",
								title:"暂未开放"
							})
							// uni.navigateTo({
							// 	url:url,
							// 	animationType:"slide-in-bottom",
							// 	animationDuration:400
							// })
						}else if(url=="./guanyuwomen"){
							uni.navigateTo({
								url:url,
								animationType:"slide-in-bottom",
								animationDuration:400
							})
						}else if(url=="../index/index"){
							uni.reLaunch({
								url:url
							})
						}else if(url=="./admin_message"){
							uni.showToast({
								icon:"none",
								title:"暂未开放"
							})
							// uni.navigateTo({
							// 	url:url,
							// 	animationType:"slide-in-bottom",
							// 	animationDuration:400
							// })
						}
						
					}else{
						uni.showActionSheet({
							itemList: ['确认', '取消'],
							success: function(res) {
								if(res.tapIndex==0){
									uni.removeStorage({
										key:"adminim",
										success:function(res){
											
										},
										fail() {
											
										}
									});
									uni.removeStorage({
										key:"userim",
										success:function(res){
											
										},
										fail() {
											
										}
									});
									uni.reLaunch({
										url:"../login/admin-login"
									})
								}else{
									uni.showToast({
										icon:"none",
										title:"操作取消"
									})
								}
								},
								})
								
					}
				}else{
					uni.showToast({
						icon:"none",
						title:"登录失效"
					});
					uni.removeStorage({
						key:"adminim",
						success:function(res){
							
						},
						fail() {
							
						}
					});
					uni.removeStorage({
						key:"userim",
						success:function(res){
							
						},
						fail() {
							
						}
					});
					uni.reLaunch({
						url:"../login/admin-login"
					})
					
				}
			},
			getad(){
				var data = "";
				try {
					const res = uni.getStorageSync('adminim');
					data = JSON.parse(res);
					this.adminuser=data;
				} catch (e) {
					//TODO handle the exception
				}
			}
			
		}
	}
</script>

<style>
	.status_bar {
		height: var(--status-bar-height);
		width: 100%;
		background-color: #F8F8F8;
	}
	.top_view {
		height: var(--status-bar-height);
		width: 100%;
		position: fixed;
		background-color: #F8F8F8;
		top: 0;
		z-index: 999;
	}
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
	.main-top{
		display: grid;
		height: 200upx;
		margin: 20upx;
		grid-template-columns: 1fr;
		background: #FFFFFF;
		justify-items: center;
	}
	.main-admin{
		display: grid;
		grid-template-columns: 1fr 1fr;
		height: 400upx;
		margin-top: 20upx;
		margin-left: 20upx;
		margin-right: 20upx;
		column-gap: 10upx;
		row-gap: 10upx;
	}
	.grid-item{
		font-size: 50upx;
		border-radius: 5px;
		text-align: center;
		line-height: 92.5upx;
		color: white;
		background-color: rgb(0,0,0,0.1);
	}
	.grid-item:hover{
		background-color: #FFFFFF;
		color: #333333;
	}
	.grid-item-1{
		margin: 30upx 20upx 0upx 20upx ;
		height: 95.2upx;
		font-size: 50upx;
			border-radius: 5px;
			text-align: center;
			line-height: 95.2upx;
			color: white;
			background-color: rgb(0,0,0,0.1);
	}
</style>
