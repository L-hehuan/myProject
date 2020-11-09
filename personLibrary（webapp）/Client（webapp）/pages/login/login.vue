<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view style="height: 100upx;">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;">
				返回个人中心
			</view>
		</view>
		<view class="flex flex-direction align-center">
			<image class="logo" src="../../static/img/logo_02.png"></image>
			<view style="margin-top: 10upx;color: grey;" class="">你的颜如玉</view>

		</view>
		<view class="" style="margin-top: 20upx;">
			<view class="input-father">
				<input @input="onInput" class="log-input" placeholder="用户名/手机号" v-model="form.phone" />
			</view>
			<view v-if="status==0" class="input-father flex align-center">
				<input class="log-input" placeholder="请输入密码" v-model="form.password" password="true" />
			</view>
			<view v-if="status==1" class="input-father flex align-center">
				<input class="log-input" placeholder="请输入验证码" v-model="form.yz_code"  />
				<button :disabled="yzmclick" @tap="huoquyzm" class="cu-btn bg-red" v-if="status==1">{{yzmtext}}</button>
			</view>
		</view>
		<view class="flex justify-center" style="margin-top: 40upx;">
			<button @tap="login" class="bg-gradual-red round" style="width: 650upx;">
				登录
			</button>
		</view>
		<view class="flex justify-between input-father" style="margin-top: 30upx;">
			<view>
				忘记密码?
			</view>
			<view @tap="goadmin">
				管理员入口
			</view>
			<view @tap="gozhuce">
				新用户注册
			</view>
		</view>
		<view style="margin-top: 40upx;" class="flex justify-between align-center">
			<view class="line"></view>
			<view style="color: gray;">其他登陆方式</view>
			<view class="line"></view>
		</view>
		<view class="flex justify-around" style="margin-top: 40upx;">
			<view class="flex flex-direction align-center justify-center">
				<image class="anniulogo" src="../../static/img/weixin.png"></image>
				<view style="margin-top: 10upx;">微信登录</view>
			</view>
			<view @tap="changestatus" class="flex flex-direction align-center justify-center">
				<image class="anniulogo" :src="status==0?'../../static/img/shoujidenglu.png':'../../static/img/mimadenglu.png'"></image>
				<view style="margin-top: 10upx;">{{status==0?'验证码':'密码'}}登录</view>
			</view>
		</view>
		<view class="" style="position: fixed;bottom: 10upx;color: gray;text-align: center;width: 750upx;">
			技术支持<text style="color: blue;">@_Wu.</text><br /><text>有问题请联系1413502842@qq.com </text>
		</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				yzmtext: "获取验证码",
				yzmclick: false,
				status: 0, //为0时是密码登录,为1时是验证码登录
				form: {
					phone: "",
					password: "",
					yz_code:"",
				},
				mylists: {
					name: "my",
					url: "../my/my",
				}

			}
		},
		onLoad() {
			this.rm_user();
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
			this.rm_user();
		},
		onShow() {
			let pages = getCurrentPages();
		},
		methods: {
			goadmin(){
				var url="./admin-login"
				if(url!=null || url!=undefined){
					uni.navigateTo({
						url:url,
						animationType:"slide-in-top",
						animationDuration:400
					})
				}
			},
			onInput(e) {
				this.number = e.detail
			},
			rm_user() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					if (data == "") {
						this.form.phone = "";
						this.form.password = "";
					} else {
						this.form.phone = data.wusername;
						// console.log(this.form.phone)
					}
				} catch (e) {
					//TODO handle the exception
				};
			},
			gozhuce() {
				var url = "../zhuce/zhuce";
				if (url != null && url != undefined) {
					uni.navigateTo({
						url: url,
						animationType: "zoom-fade-out",
						animationDuration: 500
					});
				}

			},
			huoquyzm() {
				var its = this;
				var up_num = (/^[0-9]+$/.test(this.form.phone));
				if (this.form.phone.length != 11) {
					uni.showToast({
						icon: "none",
						title: "请输入正确的手机号"
					});
					return;
				}else{
					if(up_num==false){
						uni.showToast({
							icon:"none",
							title:"手机号格式不正确"
						})
					}else{
						if (this.yzmtext == "获取验证码") {
							this.yzmclick = true;
						} else {
							return;
						};
						//获取验证码的函数
						uni.request({
							url:helper.baseUrl+"/user/codelogin",
							data:{
								phone:this.form.phone
							},
							method:"POST",
							dataType:"json",
							success: (res) => {
								if(res.data.status!=0){
									uni.showToast({
										icon:"none",
										title:res.data.desc
									})
								}else{
									this.yz_code=res.data.code;
								}
							},
							fail: (res) => {
								uni.showToast({
									icon:"none",
									title:"获取失败,请检查网络连接"
								})
							}
						})
						var seconds = 60;
						var jishiqi = setInterval(() => {
							seconds--;
							its.yzmtext = seconds + "秒后重发"
							if (seconds <= 0) {
								its.yzmtext = "获取验证码";
								its.yzmclick = false;
								clearInterval(jishiqi);
							}
						}, 1000);
					}
				}


				//获取验证码的函数
				
			},
			changestatus() {
				this.status = this.status == 0 ? 1 : 0;
			},
			gomy() {
				var url = this.mylists.url;
				uni.showLoading({
					title: '加载中',
					mask: true,
					success(res) {
						// console.log(res)
						setTimeout(function() {
							uni.hideLoading();
							if (url != null && url != undefined) {
								uni.reLaunch({
									url:url
								})
							};
						}, 1000);
					}
				});

			},
			login() {
				var data = "";
				var dataid = "";
				var user_login = [];
				var user_status = 1;
				var up_num = (/^[0-9]+$/.test(this.form.phone));
				if(this.status==0){
					uni.request({
						url: helper.baseUrl + "/user/login",
						data: {
							name: this.form.phone,
							phone: this.form.phone,
							password: this.form.password
						},
						method: "POST",
						success: (res) => {
							user_status = res.data.status;
							if (res.data.status == 1) {
								uni.showToast({
									icon: "none",
									title: res.data.desc
								});
							} else if (res.data.status == 0) {
								user_login = JSON.stringify(res.data.info);
								uni.setStorage({
									key: "userim",
									data: user_login,
									success() {},
									fail() {}
								});
								try {
									const res = uni.getStorageSync('userim');
									data = JSON.parse(res);
									dataid = data.wuserid;
								} catch (e) {
									//TODO handle the exception
								};
								uni.request({
									url: helper.baseUrl + "/index/tuijian",
									data: {
										userid: dataid
									},
									method: "POST",
									success: (res) => {
										if (user_status == 0) {
											uni.showLoading({
												title: '加载中',
												mask: true,
												success(res) {
													// console.log(res)
													setTimeout(function() {
														uni.hideLoading();
														uni.reLaunch({
															url: "../my/my"
														})
					
													}, 2000);
												}
											});
					
										}
									}
								})
					
							}
					
						},
						fail: (res) => {
							uni.showToast({
								icon:"none",
								title:"网络连接出错"
							})
						}
					
					})
				}else{
					if (this.form.phone.length != 11) {
						uni.showToast({
							icon: "none",
							title: "请输入正确的手机号"
						});
						return;
					}else{
						if(up_num==false){
							uni.showToast({
								icon:"none",
								title:"手机号格式不正确"
							})
						}else{
							uni.request({
								url: helper.baseUrl+"/user/yzmlogin",
								data:{
									phone:this.form.phone,
									code:this.form.yz_code
								},
								method:"POST",
								success: (res) => {
									user_status = res.data.status;
									if(res.data.status!=0){
										uni.showToast({
											icon:"none",
											title:res.data.desc
										})
									}else{
										user_login = JSON.stringify(res.data.info);
										uni.setStorage({
											key: "userim",
											data: user_login,
											success() {},
											fail() {}
										});
										try {
											const res = uni.getStorageSync('userim');
											data = JSON.parse(res);
											dataid = data.wuserid;
										} catch (e) {
											//TODO handle the exception
										};
										uni.request({
											url: helper.baseUrl + "/index/tuijian",
											data: {
												userid: dataid
											},
											method: "POST",
											success: (res) => {
												if (user_status == 0) {
													uni.showLoading({
														title: '加载中',
														mask: true,
														success(res) {
															uni.request({
																url:helper.baseUrl+"/code/rm",
																data:{
																	phone:data.wuserphone
																},
																method:"POST",
																success: (res) => {
																	
																},
																fail: (res) => {
																	
																}
															})
															setTimeout(function() {
																uni.hideLoading();
																uni.reLaunch({
																	url: "../my/my"
																})
															}, 2000);
														}
													});
															
												}
											},
											fail: (res) => {
												uni.showToast({
													icon:"none",
													title:"网络连接出错"
												})
											}
										})
									}
								},
								fail: (res) => {
									uni.showToast({
										icon:"none",
										title:"网络连接失败"
									})
								}
							})
						}
						}
					
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

	.logo {
		width: 200upx;
		height: 200upx;

	}

	.log-input {
		height: 100upx;
		border-bottom: 1upx solid #DDDDDD;
		flex-grow: 1;
	}

	.input-father {
		padding: 0upx 40upx;
	}

	.line {
		height: 1upx;
		background-color: #DDDDDD;
		flex-grow: 1;
	}

	.anniulogo {
		width: 100upx;
		height: 100upx;
	}
</style>
