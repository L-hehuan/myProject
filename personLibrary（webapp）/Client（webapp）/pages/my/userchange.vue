<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;">
			返回我的页面
		</view>
		<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
			<view class="cu-item ">
				<view class="content">
					<text class="text-black"><b>用户名: </b></text>
				</view><input type="text" v-model="form.username" placeholder="请输入要更换的用户名" />
			</view>
			<view class="cu-item ">
				<view class="content">
					<text class="text-black"><b>手机号: </b></text>
					<text class="text-grey"></text>
				</view><input type="text" v-model="form.userphone" placeholder="请输入要更换的手机号" />
			</view>
			<view class="cu-item ">
				<view class="content">
					<text class="text-black"><b>密码: </b></text>
					<text class="text-grey"></text>
				</view><input type="text" v-model="form.userpassword" password="" placeholder="请输入要更换的密码" />
			</view>
			<view class="cu-item ">
				<view class="content">
					<text class="text-black"><b>确认密码: </b></text>
					<text class="text-grey"></text>
				</view><input type="text" v-model="form.userpassword_2" password="" placeholder="请确认密码" />
			</view>
			<view class="cu-item ">
				<button @tap="gotijiao()" type="primary" class="content">
					<text class="text-black"><b>提交修改</b></text>
					<text class="text-grey"></text>
				</button>
			</view>
		</view>


	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				form: {
					username: "",
					userphone: "",
					userpassword: "",
					userpassword_2: "",
				},
				TabCur: 0,
				scrollLeft: 0
			}

		},
		methods: {
			tabSelect(e) {
				this.TabCur = e.currentTarget.dataset.id;
				this.scrollLeft = (e.currentTarget.dataset.id - 1) * 60
			},
			gomy() {
				var url = "./userim";
				if (url != null && url != undefined) {
					uni.navigateTo({
					    url: url,
						animationType:"slide-in-right",
						animationDuration:500
					});
				}

			},
			gotijiao() {
				var data_1 = "";
				var data = "";
				var its = this;
				var user_login = [];
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != 0) {
					if (this.form.username.length < 3) {
						uni.showToast({
							icon: "none",
							title: "请检查输入的用户名是否合法"
						});
						return;
					} else {
						if (this.form.userphone.length != 11) {
							uni.showToast({
								icon: "none",
								title: "请检查输入的手机号是否合法"
							});
							return;
						} else {
							if (this.form.userpassword.length <= 5) {
								uni.showToast({
									icon: "none",
									title: "请检查输入的密码是否合法"
								});
								return;
							} else {
								if (this.form.userpassword != this.form.userpassword_2) {
									uni.showToast({
										icon: "none",
										title: "两次输入的密码不一致"
									});
									return;
								}
							}
						}
					};
					uni.request({
						url:  helper.baseUrl+ "/user/changeim",
						data: {
							userid: data.wuserid,
							username: this.form.username,
							userphone: this.form.userphone,
							userpassword: this.form.userpassword
						},
						method: "POST",
						success: (res) => {
							if (res.data.status == 1) {
								uni.showToast({
									icon: "none",
									title: res.data.desc
								})
							} else if (res.data.status == 0) {
								uni.showToast({
									icon: "success",
									title: res.data.desc
								});
								uni.request({
									url: helper.baseUrl+ "/user/gerenxinxi",
									data: {
										userid: data.wuserid
									},
									method: "POST",
									success: (res) => {
										user_login = JSON.stringify(res.data.data);
										uni.setStorage({
											key: "userim",
											data: user_login,
											success() {
												uni.reLaunch({
													url: "./userim"
												})
											},
											fail() {}
										});
									}

								})
							}


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
</style>
