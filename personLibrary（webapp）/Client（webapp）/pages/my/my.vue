<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="zhuce-top">
			<view class="book_place" style="margin-left:319upx;">
				<text>个人中心</text>
			</view>
			<view @tap="goadminser" v-if="adminuser.length!=0" class="book_place_1" style="margin-left: 197upx;">
				<text>管理员页</text>
			</view>
		</view>

		<view style="position: relative;">
			<view class="flex justify-center bg-blue content-top">
				<image src="../../static/bkjpg.jpg" style="position: absolute; width: 750upx; height: 180upx;"></image>
			</view>
			<view class="flex justify-center bg-blue content-top">
				<image src="../../static/bkjpg_2.jpg" style="position: absolute; width: 750upx; height: 180upx;"></image>
			</view>
			<view class="flex justify-center content-header">
				<view class=" bg-white content1" style="z-index: 9999;top: 40upx;position: absolute;">
					<view class="wuser-im">
						<view style="">
							<image class="wuser-log" :src='vue_user!=""?(vue_user.wuserimage==null?"../../static/img/people_img.png":vue_user.wuserimage):"../../static/img/people_img.png"'></image>
						</view>
						<view class="cu-tag bg-white" style="font-weight: bold;font-size: 120%;margin-right: 20upx;"><text>{{vue_user!=""?vue_user.wusername:"未登录"}}<br /><text
								 v-if='vue_user!=""' style="font-size: 80%;font-weight: 500;">用户ID:{{vue_user!=""?vue_user.wuserid:""}}</text></text></view>
					</view>
					<view class="wuser-button flex justify-between">
						<view>
							<view @tap="gouserim()" class="cu-tag radius" style="margin: 20upx 20upx 10upx 0upx;background-color: #e0e0e0;font-size: 110%;">查看我的个人信息<text
								 class="cuIcon-right"></text></view>
						</view>
						<view>
							<view class="cu-tag" style="margin: 20upx 20upx 0upx 10upx;background-color:#FF9700;border-radius: 25px;color: white;font-size: 90%;">敬请期待</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view class="" style="margin-top: 30upx;">
			<view @tap="gopage(i)" v-if="vue_user.walimit!=999" v-for="(p,i) in lists" :key="i" class="wuser-message">
				<image :src="p.url_log"></image>
				<text>{{p.text}}</text>
				<view class="" style="padding-left: 500upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="gologin_exit" v-if="vue_user.walimit!=999" class="wuser-message">
				<image :src="vue_user==''?lists_user[0].url_log:lists_user[1].url_log"></image>
				<text>{{vue_user==''?lists_user[0].text:lists_user[1].text}}</text>
				<view class="" style="padding-left: 500upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>

		</view>

	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				adminuser:"",
				select_true: {
					select_t: false,
					select_f: false
				},
				modalName: null,
				wuser: {
					username: "",
					userphone: "",
					status: 1
				},
				wuser_1: {
					username: "请进行登录",
					userphone: " ",
				},
				modalName: null,
				vue_user: "",
				vue_user_1: "",
				lists_user: [{
					text: "登录账号",
					url_log: "../../static/img/denglu.png",
					url: "../login/login"
				}, {
					text: "退出账号",
					url_log: "../../static/img/zhuxiaodenglu.png",

				}],
				lists: [{
						text: "我的钱包",
						url_log: "../../static/img/qianbao.png"
					},
					{
						text: "留言反馈",
						url_log: "../../static/img/xiaoxizhongxin.png",
						url:"./mytalk"
					},
					{
						text: "我的收藏",
						url_log: "../../static/img/wodeshoucan.png",
						url:"../goods/goods"
					},
					{
						text: "我的留言",
						url_log: "../../static/img/wodefankui.png",
						url:"./mymessage"
					},
					{
						text: "我的发布",
						url_log: "../../static/img/wodetiezl.png",
						url:"./myreturn"
					}, //{
					// 	text: "系统设置",
					// 	url_log: "../../static/img/xitongshezhi.png"
					// },
					{
						text: "关于我们",
						url_log: "../../static/img/guanyuwomen.png",
						url:"./aboutus"
					}
				]
			}
		},
		methods: {
			goadminser(){
				var data=""
				try {
					const res = uni.getStorageSync('adminim');
					data = JSON.parse(res);
					
				} catch (e) {
					//TODO handle the exception
				}
				if(data==""){
					uni.showToast({
						icon:"none",
						title:"系统繁忙"
					})
				}else{
					uni.reLaunch({
						url:"../admin/admin"
					})
				}
			},
			goadmin(){
				var data=""
				try {
					const res = uni.getStorageSync('adminim');
					data = JSON.parse(res);
					
				} catch (e) {
					//TODO handle the exception
				}
				if(data==""){
					this.adminuser="";
				}else{
					this.adminuser=data;
				}
			},
			showModal(e) {
				this.modalName = e.currentTarget.dataset.target;

			},
			hideModal(e) {
				this.modalName = null

			},
			gologin_exit() {
				var data = "";
				var data_admin="";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				try {
					const res = uni.getStorageSync('adminim');
					data_admin = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data.length == 0) {
					var url_1 = this.lists_user[0].url;
					if (url_1 != null && url_1 != undefined) {
						uni.navigateTo({
							url: url_1,
							animationType: "zoom-out",
							animationDuration: 500
						});
					}
				} else {
					var user_status_zhuxiao = "";
					var data_2 = "";
					uni.showActionSheet({
						itemList: ['确认', '取消'],
						success: function(res) {
							if (res.tapIndex == 0) {
								try {
									const res = uni.getStorageSync('userim');
									data_2 = JSON.parse(res);
								} catch (e) {
									//TODO handle the exception
								};
								if (data != "") {
									if(data_admin!=""){
										uni.removeStorage({
											key:"adminim",
											success:function(res){
												
											},
											fail() {
												
											}
										})
									};
									uni.removeStorage({
										key: 'userim',
										success: function(res) {
											uni.showToast({
												icon: null,
												title: "退出成功"
											});
											try {
												uni.clearStorageSync();
											} catch (e) {
												//error
											};
											var url_2 = "../login/login";
											if (url_2 != null && url_2 != undefined) {
												uni.reLaunch({
													url: url_2
												})
											}
										},
										fail() {
											console.log('no user login');
											uni.reLaunch({
												url: "./my/my"
											})
										}
									});
								} else {
									uni.showToast({
										icon: "none",
										title: "您未登录,请登录",
										duration: 2000
									})
								}
							} else {
								uni.showToast({
									icon: "none",
									title: "取消退出",
									duration: 2000
								})
							}

						},
						fail: function(res) {}
					});
				}
			},
			getuserim() {
				var data = [];
				var data_1 = "";
				var user_login = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					this.vue_user = data;
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "/my/userimfor",
						data: {
							id: data.wuserid
						},
						method: "POST",
						success: (res) => {
							user_login = JSON.stringify(res.data.data);
							uni.setStorage({
								key: "userim",
								data: user_login,
								success() {},
								fail() {}
							});
							try {
								const res = uni.getStorageSync('userim');
								data_1 = JSON.parse(res);
								this.vue_user = data_1;
							} catch (e) {
								//TODO handle the exception
							}
						}
					})
				}


			},
			gouserim() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.navigateTo({
						url: "./userim",
						animationType: "slide-in-left",
						animationDuration: 500
					});
				} else {
					uni.showToast({
						icon: "none",
						title: "请先进行登录"
					})
				}
			},
			gopage(item) {
				var data = "";
				var url = this.lists[item].url;
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					if (url != null && url != undefined) {
						if(url=="../goods/goods"){
							uni.reLaunch({
								url:url
							})
						}else{
							uni.navigateTo({
								url: url,
								animationType: "zoom-out",
								animationDuration: 500
							});
						}
						
					} else {
						uni.showToast({
							icon: "none",
							title: "暂未开放"
						}, 1000)
					}
				} else {
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.navigateTo({
									url: '../login/login',
									animationType: "zoom-out",
									animationDuration: 500
								});
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "取消登录"
								})
							}
						}
					});
				}
			},
		},
		onLoad() {
			this.getuserim();
			this.goadmin();
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
			this.getuserim();
			this.goadmin();
		},
		onReady() {

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

	.content-top {
		margin: 0;
		padding: 0;
		width: 750upx;
		height: 180upx;
	}

	.zhuce-top {
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}

	.wuser-im {
		width: 590upx;
		height: 180upx;
		padding: 30upx 0upx 30upx 30upx;
		display: flex;
		align-items: center;
	}

	.wuser-button {
		width: 650upx;
		height: 90upx;
		background-color: #e0e0e0;
		border-bottom-right-radius: 10px;
		border-bottom-left-radius: 10px;
	}

	.wuser-log {
		width: 120upx;
		height: 120upx;
	}

	.content1 {
		width: 650upx;
		height: 270upx;
		border-radius: 10px;
		display: flex;
		flex-direction: column;
	}

	.content2 {
		width: 650upx;
		height: 100upx;
	}

	.wuser-all {
		display: flex;
		justify-content: space-between;
		height: 160upx;
		align-items: center;
		padding-left: 20upx;
		padding-right: 20upx;
	}

	.wuser-message {
		height: 100upx;
		padding: 0upx 10upx 0upx 0upx;
		border-bottom: #e0e0e0 8upx solid;
		background: white;
		display: flex;
		align-items: center;
		border-bottom-right-radius: 10px;
		border-top-right-radius: 10px;
	}

	.wuser-message image {
		width: 75upx;
		height: 50upx;
		margin: 0 10upx;
	}

	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 200upx;
	}
	.book_place_1 {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
</style>
