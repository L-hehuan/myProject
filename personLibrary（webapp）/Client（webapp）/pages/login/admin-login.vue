<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="admin-top">
			<view @tap="gouserlogin" class="cuIcon-back cu-btn" style="padding-left: 10upx;background: #FFFFFF;">
				返回
			</view>
			<view class="" style="padding-left: 180upx;text-align: center;">
				管理员登陆
			</view>
		</view>
		<view class="admin-center">
			<view class="" style="text-align: center;font-size: 70upx;margin-bottom: 20upx;padding-top: 20upx;">
				Admin Login
			</view>
			<view class="admin-input">
				<image style="width: 50upx;height: 50upx;margin-left: 10upx;" src="../../static/img/admin-phone.png"></image>
				<input style="margin-left: 10upx;border: 1px solid black;width: 650upx;height: 60upx;padding-left: 10upx;" class=""
				 v-model="form.phone" type="text" placeholder="Enter Your Phone Or adminname" />
			</view>
			<view class="admin-input">
				<image style="width: 50upx;height: 50upx;margin-left: 10upx;" src="../../static/img/admin-mima.png"></image>
				<input style="margin-left: 10upx;border: 1px solid black;width: 650upx;height: 60upx;padding-left: 10upx" v-model="form.password"
				 password="true" class="" type="text" placeholder="Enter Your Password" />
			</view>
			<view class="flex justify-center" style="padding-top: 10upx;padding-bottom: 20upx;">
				<button @tap="gologin" style="border: 1px solid #2F3640;" class="cu-btn bg-white">登录</button>
			</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js"
	export default {
		data() {
			return {
				form: {
					phone: "",
					password: ""
				},


			}
		},
		methods: {
			gouserlogin() {
				uni.navigateTo({
					url: "./login",
					animationType: "slide-in-bottom",
					animationDuration: 400
				})
			},
			gologin() {
				var admin_login = [];
				var user_login = [];
				if (this.form.phone == null || this.form.password == null || this.form.phone == "" || this.form.password == "") {
					uni.showToast({
						icon: "none",
						title: "账号或者密码为空"
					})
				} else {
					uni.request({
						url: helper.baseUrl + "/admin/adminlogin",
						data: {
							phone: this.form.phone,
							password: this.form.password
						},
						method: "POST",
						success: (res) => {
							if (res.data.status == 0) {
								admin_login = JSON.stringify(res.data.data);
								uni.setStorage({
									key: "adminim",
									data: admin_login,
									success() {},
									fail() {}
								});
								uni.request({
									url: helper.baseUrl + "/admin/getmy",
									data: {
										phone: this.form.phone
									},
									method: "POST",
									success: (res) => {
										if (res.data.status == 0) {
											user_login = JSON.stringify(res.data.info)
											uni.setStorage({
												key: "userim",
												data: user_login,
												success() {},
												fail() {}
											});
											uni.showLoading({
												title: '登录成功',
												mask: true,
												success(res) {
													setTimeout(function() {
														uni.hideLoading();
														uni.reLaunch({
															url: "../admin/admin"
														})
													}, 2000);
												}
											})
										}else{
											uni.showToast({
												icon:"none",
												title:"暂未注册用户账户"
											})
										}
									},
									fail: (res) => {
										uni.showToast({
											icon: "none",
											title: "网络连接失败"
										})
									}
								})

							} else {
								uni.showToast({
									icon: "none",
									title: res.data.desc
								})
							}
						},
						fail: (res) => {
							uni.showToast({
								icon: "none",
								title: "网络连接失败"
							})
						}
					})
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

	.admin-top {
		height: 70upx;
		line-height: 70upx;
		display: flex;
		background: #FFFFFF;
		border-bottom: 1px solid #e4e4e4;
	}

	.admin-center {
		margin-top: 20upx;
		background: #FFFFFF;

	}

	.admin-input {
		height: 100upx;
		display: flex;
		align-items: center;
	}
</style>
