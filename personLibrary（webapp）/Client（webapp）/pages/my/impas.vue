<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="userim-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				我的信息
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text>修改密码</text>
			</view>
		</view>
		<view class="" style="padding-top: 10upx;">

		</view>
		<form>
			<view class="cu-form-group">
				<view class="title">旧密码</view>
				<input placeholder="请输入旧密码" password="true" name="input" v-model="form.password"></input>
				<button style="border: 1px solid #2F3640;" :disabled="zcclick" @tap="huoquyzm" class="cu-btn bg-gray">{{zctext}}</button>
			</view>
			<view v-if="zcclick==true" class="cu-form-group">
				<view class="title">验证码</view>
				<input placeholder="请输入正确的验证码" name="input" v-model="form.yz_code"></input>

			</view>
			<view class="cu-form-group">
				<view class="title">新密码</view>
				<input placeholder="请输入新密码" name="input" password="true" v-model="form.password_one"></input>
			</view>
			<view style="border-bottom-left-radius: 10px;border-bottom-right-radius: 10px;" class="cu-form-group">
				<view class="title">确认密码</view>
				<input placeholder="再次输入密码/与新密码一致" name="input" password="true" v-model="form.password_two"></input>
			</view>
			<view class="flex justify-center " style="margin-top: 40upx;">
				<button @tap="changepas" class="round zhuce-button bg-gradual-red" style="width: 650upx;">
					提交修改
				</button>
			</view>
		</form>

	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				zcclick: false,
				zctext: "获取验证码",
				userid: "",
				form: {
					password: "",
					password_one: "",
					password_two: "",
					yz_code: ""
				}
			}
		},
		onLoad(option) {
			this.userid = option.id;
			// console.log(this.userid);
		},
		methods: {
			huoquyzm() {
				var data="";
				var its = this;
				var pd_num = (/^[0-9]+$/.test(this.form.password_two));
				var pd_EN = (/^[a-zA-Z]+$/.test(this.form.password_two));
				if (this.form.password.lenth == 0 || this.form.password_one == 0 || this.form.password_two.length == 0) {
					uni.showToast({
						icon:"none",
						title:"有密码项为空"
					});
					return;
				} else {
					if (this.form.password_one != this.form.password_two) {
						uni.showToast({
							icon: "none",
							title: "两次密码输入不一致"
						})
						return;
					} else {
						if (this.form.password == this.form.password_two) {
							uni.showToast({
								icon: "none",
								title: "新密码与老密码一样"
							})
							return;
						} else {
							if (pd_EN==true || pd_num==true) {
								uni.showToast({
									icon: "none",
									title: "密码强度太低"
								});
								return;
							}else{
								if (this.form.password_two.length <= 6) {
									uni.showToast({
										icon: "none",
										title: "密码太短"
									})
									return;
								} else {
									if (this.zctext == "获取验证码") {
										this.zcclick = true;
									} else {
										return;
									};
									try {
										const res = uni.getStorageSync('userim');
										data = JSON.parse(res);
									} catch (e) {
										//TODO handle the exception
									}
									uni.request({
										url: helper.baseUrl + "/user/phone_change",
										data: {
											phone: data.wuserphone,
											code: this.form.yz_code
										},
										method: "POST",
										dataType: "json",
										success: (res) => {
											if (res.data.status != 0) {
												uni.showToast({
													icon: "none",
													title: res.data.desc
												})
											} else {
												this.yz_code = res.data.code;
												uni.showToast({
													icon:"none",
													title:"获取成功"
												})
											}
										},
										fail: (res) => {
											uni.showToast({
												icon: "none",
												title: "网络连接出错"
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
				}
			},
			changepas() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data == "") {
					uni.showToast({
						icon: "none",
						title: "登陆失效,请重新登录"
					});
					uni.removeStorage({
						key: 'userim',
						success: function(res) {
							uni.reLaunch({
								url: "./my"
							})
						},
					})
				} else {
					var pd_num = (/^[0-9]+$/.test(this.form.password_two));
					var pd_EN = (/^[a-zA-Z]+$/.test(this.form.password_two));
					if (this.form.password_one != this.form.password_two) {
						uni.showToast({
							icon: "none",
							title: "两次密码输入不一致"
						})
						return;
					} else {
						if (this.form.password == this.form.password_two) {
							uni.showToast({
								icon: "none",
								title: "新密码与老密码一样"
							})
							return;
						} else {
							if (pd_EN == true || pd_EN == true) {
								uni.showToast({
									icon: "none",
									title: "密码强度太低"
								})
								return;
							} else {
								if (this.form.password_two.length <= 6) {
									uni.showToast({
										icon: "none",
										title: "密码太短"
									})
									return;
								} else {
									uni.request({
										url: helper.baseUrl + "/my/changipas",
										data: {
											phone:data.wuserphone,
											userid: data.wuserid,
											old_password: this.form.password,
											new_password: this.form.password_two,
											code: this.form.yz_code
										},
										method: "POST",
										success: (res) => {
											if (res.data.status == 0) {
												uni.showToast({
													title: res.data.desc,
													icon: "none",
												});
												uni.request({
													url:helper.baseUrl+"/code/rm",
													data:{
														phone:data.wuserphone
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
												this.form.password = "";
												this.form.password_one = "";
												this.form.password_two = "";
												uni.navigateTo({
													url: "./userim",
													animationDuration: 300,
													animationType: "zoom-out"
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
												title: "网络连接出错"
											})
										}
									})
								}
							}
						}
					}

				}
			},
			gomy() {
				var url = "./userim";
				if (url != null && url != undefined) {
					uni.navigateTo({
						url: url,
						animationType: "slide-in-right",
						animationDuration: 400
					})
				}

			},

		}
	}
</script>

<style>
	.pas-main {
		height: 250upx;

	}

	.userim-top {
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}

	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 120upx;
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
</style>
