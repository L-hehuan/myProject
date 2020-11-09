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
				<text>修改用户名</text>
			</view>
		</view>
		<view class="cu-form-group margin-top">
			<view class="title">用户名</view>
			<input type="text" v-model="username" placeholder="请输入要修改的用户名" />
		</view>
		<view class="flex justify-center " style="margin-top: 40upx;">
			<button @tap="changename" class=" zhuce-button bg-gradual-red" style="width: 220upx;">
				确认修改
			</button>
		</view>

	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
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
			changename() {
				var user_login = [];
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				};
				var us_num = (/^[0-9]+$/.test(this.username));
				if (data != "") {
					if(this.username.length<3 || us_num==true){
						uni.showToast({
							icon:"none",
							title:"用户名格式出错"
						});
						return;
					}else{
						uni.request({
							url: helper.baseUrl + "/my/changeun",
							data: {
								userid: data.wuserid,
								name: this.username,
								old_name:data.wusername
							},
							method: "POST",
							success: (res) => {
								if(res.data.status==0){
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
											uni.showToast({
												icon: "success",
												title: "修改成功",
											})
											this.username = ""
										}
									})
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
					
					// 	} else if (res.cancel == true) {
					// 		uni.showToast({
					// 			icon: "none",
					// 			title: "操作取消"
					// 		})
					// 	}
					// }
					// });
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
