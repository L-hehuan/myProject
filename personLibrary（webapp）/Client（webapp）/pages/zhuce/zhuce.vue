<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="zhuce-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				登录
			</view>
			<view class="book_place">
				<text>注册页</text>
			</view>
		</view>
		<view class="flex flex-direction align-center">
			<image class="logo" src="../../static/img/logo_02.png"></image>
			<view style="margin-top: 10upx;color: grey;" class="">注册账号</view>

		</view>
		<form @submit="formSubmit">
			<view style="border-top-left-radius: 10px;border-top-right-radius: 10px;" class="cu-form-group margin-top">
				<view class="title">注册名</view>
				<input placeholder="用户名/不少于三位字符" name="input" v-model="form.username"></input>
			</view>
			<view class="cu-form-group">
				<view class="title">手机号码</view>
				<input placeholder="手机号/一号一用户制" name="input" v-model="form.userphone"></input>
				<button style="border: 1px solid #2F3640;" :disabled="zcclick" @tap="huoquyzm" class="cu-btn bg-gray">{{zctext}}</button>
			</view>
			<view v-if="zcclick==true" class="cu-form-group">
				<view class="title">验证码</view>
				<input placeholder="请输入正确的验证码" name="input" v-model="form.yz_code"></input>
			     
			</view>
			<view class="cu-form-group">
				<view class="title">用户密码</view>
				<input placeholder="注册密码/不少于6位字符" name="input" password="true" v-model="form.userpassword"></input>
			</view>
			<view style="border-bottom-left-radius: 10px;border-bottom-right-radius: 10px;" class="cu-form-group">
				<view class="title">确认密码</view>
				<input placeholder="再次输入密码/与注册密码一致" name="input" password="true" v-model="form.true_password"></input>
			</view>
			<view class="flex justify-center " style="margin-top: 40upx;">
				<button :disabled="yzmclick" form-type="submit" @tap="zhuce" class="round zhuce-button bg-gradual-red" style="width: 650upx;">
					{{yzmtext}}
				</button>
			</view>
		</form>
		<view class="" style="position: fixed;bottom: 10upx;color: gray;text-align: center;width: 750upx;">
			技术支持<text style="color: blue;">@_Wu.</text><br/><text >有问题请联系1413502842@qq.com </text>
		</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				zctext: "获取验证码",
				zcclick: false,
				form: {
					username: "",
					userphone: "",
					userpassword: "",
					true_password: "",
					yz_code:""
				},
				yzmclick: false,
				yzmtext: "注册",
				inputValue: "",
				zhuce_states: true,
				netwk:""
			}
		},
		onLoad() {
			this.getnetwork();
		},
		onShow() {
			let pages=getCurrentPages();
			// console.log(pages);
			// console.log(pages.length - 2)
		},
		methods: {
			huoquyzm() {
				var its = this;
				var up_num = (/^[0-9]+$/.test(this.form.userphone));
				var us_num = (/^[0-9]+$/.test(this.form.username));
				if(this.form.username.length<=3){
					uni.showToast({
						icon: "none",
						title: "用户名太短"
					});
					return;
				}else{
					if(us_num==true){
						uni.showToast({
							icon: "none",
							title: "用户名格式有误"
						});
						return;
					}else{
						if (this.form.userphone.length != 11) {
							uni.showToast({
								icon: "none",
								title: "手机号格式有误"
							});
							return;
						}else{
							if(up_num==false){
								uni.showToast({
									icon:"none",
									title:"手机号格式有误"
								})
							}else{
								if (this.zctext == "获取验证码") {
									this.zcclick = true;
								} else {
									return;
								};
								//获取验证码的函数
								uni.request({
									url:helper.baseUrl+"/user/phone_zhuce",
									data:{
										phone:this.form.userphone,
										code:this.form.yz_code
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
											title:"网络连接出错"
										})
									}
								})
								var seconds = 60;
								var jishiqi = setInterval(() => {
									seconds--;
									its.zctext = seconds + "秒后重发"
									if (seconds <= 0) {
										its.zctext = "获取验证码";
										its.zcclick = false;
										clearInterval(jishiqi);
									}
								}, 1000);
							}
						}
					}
				}
				
			
			
				//获取验证码的函数
				
			},
			getnetwork(){
				uni.getNetworkType({
					success:function(res){
						this.netwk=res.networkType;
					}
				})
			},
			formSubmit(e){
				if(this.zhuce_states == true) {
					
				}else if(this.zhuce_states==false){
					this.form.username = "";
					this.form.userphone = "";
					this.form.userpassword = "";
					this.form.true_password = ""
				} 
			},
			gomy() {
				var url = "../login/login";
				uni.showLoading({
				    title: '加载中',
					mask:true,
					success(res) {
						setTimeout(function () {
						    uni.hideLoading();
							if (url != null && url != undefined) {
								uni.navigateTo({
								    url: url,
									animationType:"slide-in-right",
									animationDuration:500
								});
							};
						}, 1000);
					}
				});

			},
			zhuce() {
				//获取验证码的函数
				if (this.yzmtext == "注册") {
					this.yzmclick = true;
					}
				var seconds = 10;
				var jishiqi = setInterval(() => {
					seconds--;
					this.yzmtext = seconds + "秒后再次点击"
					if (seconds <= 0) {
						this.yzmtext = "注册";
						this.yzmclick = false;
						clearInterval(jishiqi);
					}
				}, 1000);
				if (this.form.username.length <= 3) {
					uni.showToast({
						icon: "none",
						title: "用户名太短"
					});
					return;
				} else {
					if (this.form.userphone.length != 11) {
						uni.showToast({
							icon: "none",
							title: "手机号有误"
						});
						return;
					} else {
						if (this.form.userpassword.length <= 6) {
							uni.showToast({
								icon: "none",
								title: "密码长度太短"
							});
							return;
						} else {
							if (this.form.userpassword != this.form.true_password) {
								uni.showToast({
									icon: "none",
									title: "两次密码不一致,请检查"
								});
								return;
							} else {
								var pd_num = (/^[0-9]+$/.test(this.form.userpassword));
								var pd_EN = (/^[a-zA-Z]+$/.test(this.form.userpassword));
								var us_num = (/^[0-9]+$/.test(this.form.username));
								var us_EN = (/^[a-zA-Z]+$/.test(this.form.username));
								var up_num = (/^[0-9]+$/.test(this.form.userphone));
								if (us_num == true) {
									uni.showToast({
										icon: "none",
										title: "用户名不能全是数字"
									});
									return;
								} else {
									if (up_num == false) {
										uni.showToast({
											icon: "none",
											title: "手机号格式不正确"
										});
										return;
									} else {
										if (pd_EN == true || pd_num == true) {
											uni.showToast({
												icon: "none",
												title: "密码强度过低"
											});
											return;
										} else {
											uni.request({
												url: helper.baseUrl + "/user/zhuce",
												data: {
													username: this.form.username,
													userphone: this.form.userphone,
													userpassword: this.form.userpassword,
													true_password: this.form.true_password,
													code:this.form.yz_code
												},
												method: "POST",
												success: (res) => {
													if(res.data.status == 0){
														uni.showToast({
															icon: "none",
															title: res.data.desc,
														});
														this.zhuce_states = false;
														uni.request({
															url:helper.baseUrl+"/code/rm",
															data:{
																phone:this.form.userphone
															},
															method:"POST",
															success: (res) => {
																
															},
															fail: (res) => {
																uni.showToast({
																	icon:"none",
																	title:"网络连接失败"
																})
															}
														});
														uni.reLaunch({
															url: "../login/login"
														});
													}else if(res.data.status==1){
														uni.showToast({
															icon:"none",
															title:res.data.desc
														});
														this.form.username = "";
														this.form.userphone = "";
														this.form.userpassword = "";
														this.form.true_password = ""
													}else{
														uni.showToast({
															icon:"none",
															title:res.data.desc
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

										}
									}
								}

							}
						}
					}
				};
			}
		},
	}
</script>

<style>
	.zhuce-top {
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}

	.zhuce-button:hover {
		background: #ee1077;
		transition: 1s ease;
		color: white;
	}

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
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 200upx;
	}
</style>
