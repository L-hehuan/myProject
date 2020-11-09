<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="userim-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				我的主页
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text>我的留言</text>
			</view>

		</view>
		<view>
			<view class="cu-bar bg-white solid-bottom margin-top" style="margin-bottom: 10upx;">
				<view class="action">
					<text class="cuIcon-title text-orange "></text>我的反馈列表
				</view>
			</view>
			<view v-if="message_list.status==0" class="cu-list menu-avatar">
				<view v-for="(item,index) in message_list.data" :key="index" class="cu-item">
					<view class="cu-avatar round lg" style="background-image: url(../../static/img/shequ.png);"></view>
					<view class="content">
						<view class="text-grey">
							<view class="cu-tag round sm" style="margin-left: 20upx;font-weight: 400;font-size: 20upx;">
								反馈标题:{{item.wumessagetitle}}
							</view>
						</view>
						<view class="text-gray text-sm flex">
							<view class="text-cut">
								<text class="text-red margin-right-xs"></text>
								反馈内容:{{item.wumessagecontent}}
							</view>
						</view>
					</view>
					<view class="" style="text-align: center;width: 200upx;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">
						<button @tap="godelete(item.wuserid,item.wumessageid)" style="margin-bottom: 5upx;" class="cu-btn bg-grey ">删除</button>
					</view>
					<view class="action">
						<view class="cu-tag round bg-grey sm">反馈时间</view>
						<view class="text-grey text-xs">{{item.winserttime}}</view>
					</view>
				</view>
			</view>
			<view v-if="message_list.status==1" class="">
				<text>{{message_list.desc}}</text>
			</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				message_list: "",
				mylists: {
					name: "my",
					url: "../my/my",
				}

			}
		},
		onLoad() {
			this.get_message();
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
			this.get_message();
		},
		methods: {
			godelete(userid, mid) {
				uni.showModal({
					title: '提示',
					content: '是否删除?',
					success: function(res) {
						if (res.confirm == true) {
							uni.request({
								url: helper.baseUrl + "//my/remove_message",
								data: {
									mid: mid,
									userid: userid
								},
								method: "POST",
								success: (res) => {
									if (res.data.status == 0) {
										uni.showToast({
											icon: "success",
											title: res.data.desc
										})
										uni.reLaunch({
											url: "./my"
										})
									} else if (res.data.status == 1) {
										uni.showToast({
											icon: "none",
											title: res.data.desc
										})
									}
								}
							})
						} else if (res.cancel == true) {
							uni.showToast({
								icon: "none",
								title: "取消操作"
							})
						}
					}
				});
			},
			gomy() {
				var url = "../my/my";
				if (url != null && url != undefined) {
					uni.switchTab({
						url: url
					});
				}

			},
			get_message() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "//my/wodefankui",
						data: {
							userid: data.wuserid
						},
						method: "POST",
						success: (res) => {
							if (res.data.status == 1) {
								this.message_list = res.data;
							} else if (res.data.status == 0) {
								this.message_list = res.data;
							}
						}
					})
				} else if (data == "") {
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.reLaunch({
									url: "../login/login"
								})
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "取消登录"
								})
							}
						}
					});
				}

			}
		}
	}
</script>

<style>
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
