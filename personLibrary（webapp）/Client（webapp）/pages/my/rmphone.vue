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
				<text>验证手机号</text>
			</view>
			<view @tap="yzphone" class=" cu-btn" style="padding-left: 210upx;background-color: #FFFFFF;">
				确认
			</view>
		</view>
		
		<view class="" style="margin: 20upx 20upx 20upx 20upx;">
			<view class="content input-father grid-input" style="justify-content: center;align-items: center;">
				<image class="wuser-log" src="../../static/phone.png"></image>
				<view class="" style="font-size: 35upx;color: gray;">
					原手机号
				</view>
				<text style="float: right;" class="text-grey">{{userim.wuserphone}}</text>
			</view>
			<view class="input-father flex align-center grid-input">
				<image class="wuser-log" src="../../static/phoneyzm.png"></image>
				<input style="border-bottom: 1px solid black;width: 100%;height: 64upx;" class="log-input" placeholder="请输入验证码" v-model="form.yz_code" />
				<button style="border: 1px solid #2F3640;" :disabled="yzmclick" @tap="huoquyzm" class="cu-btn bg-gray">{{yzmtext}}</button>
			</view>
			
		</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				form: {
					phone: "",
					yz_code: "",
				},
				yzmtext: "获取验证码",
				yzmclick: false,
				status: 0, //为0时是密码登录,为1时是验证码登录
				username: "",
				userim: "",
				index: -1,
				picker: ['喵喵喵', '汪汪汪', '哼唧哼唧'],
				userid: "",
				// date: new Date().toISOString().slice(0, 10),
			}
		},
		onLoad(Option) {
			this.userid = Option.id;
			this.getuserim();
		},
		methods: {
			huoquyzm() {
				var its = this;
				var up_num = (/^[0-9]+$/.test(this.userim.wuserphone));
				if (this.userim.wuserphone.length != 11) {
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
						if (this.yzmtext == "获取验证码") {
							this.yzmclick = true;
						} else {
							return;
						};
						//获取验证码的函数
						uni.request({
							url:helper.baseUrl+"/user/phone_code_yz",
							data:{
								phone:this.userim.wuserphone,
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
			yzphone() {
				var user_login = [];
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				};
				var us_num = (/^[0-9]+$/.test(this.userim.wuserphone));
				if (data != "") {
					if (this.userim.wuserphone.length != 11 || us_num == false) {
						uni.showToast({
							icon: "none",
							title: "用户名格式出错"
						});
						return;
					} else {
						uni.request({
							url: helper.baseUrl + "/user/bdwp",
							data: {
								phone: this.userim.wuserphone,
								code: this.form.yz_code
							},
							method: "POST",
							success: (res) => {
								if (res.data.status == 0) {
									// console.log(res.data)
									uni.request({
										url: helper.baseUrl + "/my/userimfor",
										data: {
											id: data.wuserid
										},
										method: "POST",
										success: (res) => {
											if(res.data.status==0){
												user_login = JSON.stringify(res.data.data);
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
												uni.showLoading({
													title: '验证中',
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
																uni.showToast({
																	icon:"none",
																	title:"网络连接失败"
																})
															}
														})
														setTimeout(function() {
															uni.hideLoading();
															uni.reLaunch({
																url: "./userim"
															})
														}, 2000);
													}
												});
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
												title:"网络连接失败"
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
									title: "网络连接出错"
								})
							}
						})
					}
				} else {
					uni.showToast({
						icon: "none",
						title: "请先登录后在操作"
					})
				}
			},
			getuserim() {
				var data = [];
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					this.userim = data;
				} catch (e) {
					//TODO handle the exception
				}
			},
			PickerChange(e) {
				this.index = e.detail.value

			},
			gomy() {
				var url = "./userim";
				if (url != null && url != undefined) {
					uni.reLaunch({
						url: url
					})
				}

			},
		}
	}
</script>

<style>
	.wuser-log {
		width: 62upx;
		height: 62upx;
	}
	.grid-input {
		height: 100upx;
		display: grid;
		grid-template-columns: 1fr 6fr 4fr;

	}

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

	.input-father {
		
	}
</style>
