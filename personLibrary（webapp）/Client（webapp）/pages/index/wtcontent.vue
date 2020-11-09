<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="xiding">
			<view class="cu-bar" style="position: fixed;top:3upx;width: 750upx;z-index: 9999;">
				<view @tap="goindex()" class="action anniu">
					<view class="action cuIcon-back text-white" style="font-size: 160%;color: white;">
					</view>
				</view>
			</view>
		</view>
		<view class="flex justify-center align-center bg-grey" style=" height: 100upx;">
			个性推荐
		</view>
		<view v-for="(item,index) in wtbook" :key="index" class="" style="padding-top: 10upx;">
			<view class="flex justify-center align-center" style="padding-top: 10upx;">
				<view class="bg-white" style="width: 700upx; border: 1px solid #e0e0e0;">
					<view class="cu-timeline">
						<view class="cu-time" style="width: 250upx;">{{item.wtinsertdate}}</view>
						<view class="cu-item cur cuIcon-favorfill">
							<view class="content bg-gradual-orange shadow-blur">
								<view @tap="gotodetail(item.wbookid)" class="book_content">
									<image :src="item.wtbookimage"></image>
									<view class="flex justify-center align-center " style="padding-left: 10upx;padding-bottom: 10upx;">
										<text style="text-align: center;font-weight: 900; color: black;">{{item.wtbookname}}</text>
									</view>


								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				wtbook: "",

			}
		},
		onLoad() {
			this.getcontent();
			setTimeout(function() {}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success: function(res) { //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画

		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.getcontent();
		},
		methods: {
			goindex() {
				uni.reLaunch({
					url: "./index",
					animationType: 'pop-in',
					animationDuration: 200
				})
			},
			getcontent() {
				var data = "";
				var userid = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					userid = data.wuserid;
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "/index/displaylist",
						data: {
							userid: userid
						},
						method: "POST",
						success: (res) => {
							this.wtbook = res.data.data;
						}
					})
				} else if (data == "") {
					uni.showModal({
						title: "提示",
						content: "您未登录,是否前往登录?",
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
					})
				}

			},
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata?id=${id}`,
					animationType:"zoom-fade-out",
					animationDuration:500
				})
			},

		}
	}
</script>

<style>
	.anniu {
		width: 80upx;
		height: 80upx;
		border-radius: 80upx;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: rgba(41, 36, 33, 0.2);
	}

	.xiding {
		width: 100%;
		height: var(--status-bar-height);
	}

	.xidengbuttom {
		height: calc(100upx + env(safe-area-inset-bottom) / 2);
		width: 100%;
		min-height: 100upx;

	}

	.book_content {
		height: 200upx;
		line-height: 80upx;
		display: flex;
		background: white;
		border-radius: 7px;
		margin: 10upx 10upx;
		margin-bottom: 10upx;
		padding: 10upx 10upx;
		/* border: 1px solid #e4e4e4; */
	}

	.book_content image {
		width: 120upx;
		height: 180upx;
		/* background: #E5e5e5; */
		margin: 0 20upx;

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
